import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'kitchen/scripts/kitchen.py'
spec = importlib.util.spec_from_file_location('kitchen', SCRIPT)
k = importlib.util.module_from_spec(spec)
spec.loader.exec_module(k)


def log(items, date='2026-09-07'):
    return f'## {date}\n- [stated] 早 | {items}\n'


class ScoringTests(unittest.TestCase):
    def test_half_and_full_are_order_independent(self):
        a = k.score(log('花生酱 核桃 枸杞 番茄'))
        b = k.score(log('番茄 枸杞 核桃 花生酱'))
        self.assertEqual(a, b)
        self.assertEqual(a['dailyMetDays']['nutsSeeds'], 1)
        self.assertEqual(a['weeklyCounts']['redOrange'], 1)

    def test_half_servings_accumulate_between_meals(self):
        out = k.score(log('花生酱') + '- [stated] 加 | 花生酱\n')
        self.assertEqual(out['dailyMetDays']['nutsSeeds'], 1)
        self.assertEqual(k.score(log('花生酱 花生酱'))['dailyMetDays']['nutsSeeds'], 0)

    def test_multi_category_and_per_meal_deduplication(self):
        out = k.score(log('小白菜 西蓝花 小白菜'))
        self.assertEqual(out['dailyMetDays']['leafy'], 1)
        self.assertEqual(out['weeklyCounts']['cruciferous'], 1)

    def test_empty_dates_and_archive_are_not_meals(self):
        text = log('菠菜') + '## 2026-09-08\n## 归档\n- 旧记录 | 核桃\n'
        out = k.score(text, '2026-09-08')
        self.assertEqual(out['daysWithRecord'], 1)
        self.assertEqual(out['dailyMetDays']['nutsSeeds'], 0)
        self.assertEqual(out['dailyMatrix']['leafy'][-1], 'none')

    def test_limits_only_day_and_duplicate_limit(self):
        out = k.score(log('限制:tooSalty,tooSalty'))
        self.assertEqual(out['daysWithRecord'], 1)
        self.assertEqual(out['limitsHit'], {'tooSalty': 1})

    def test_aliases_and_punctuation(self):
        out = k.score(log('西兰花、小番茄，松茸,蒜'))
        self.assertEqual(out['weeklyCounts']['cruciferous'], 1)
        self.assertEqual(out['weeklyCounts']['redOrange'], 1)
        self.assertEqual(out['weeklyCounts']['mushrooms'], 1)
        self.assertEqual(out['dailyMetDays']['spices'], 1)
        self.assertEqual(out['unrecognizedItems'], [])

    def test_unknown_food_is_explicit(self):
        out = k.score(log('神秘食材'))
        self.assertEqual(out['unrecognizedItems'], ['神秘食材'])
        self.assertEqual(sum(out['dailyMetDays'].values()), 0)

    def test_plant_milk_and_tubers_do_not_count_as_whole_grains(self):
        out = k.score(log('燕麦奶 杏仁奶 山药 土豆'))
        self.assertEqual(out['dailyMetDays']['wholeGrain'], 0)
        self.assertEqual(out['dailyMetDays']['nutsSeeds'], 0)
        self.assertEqual(len(out['neutralList']), 4)

    def test_seven_day_window_excludes_older_meals(self):
        out = k.score(log('菠菜', '2026-08-31') + log('燕麦'), '2026-09-07')
        self.assertEqual(out['weekStart'], '2026-09-01')
        self.assertEqual(out['daysWithRecord'], 1)
        self.assertEqual(out['dailyMetDays']['leafy'], 0)

    def test_no_records(self):
        out = k.score('', '2026-09-07')
        self.assertEqual(out['daysWithRecord'], 0)
        self.assertTrue(all(c == 'none' for row in out['dailyMatrix'].values() for c in row))

    def test_unknown_tuna_is_not_automatically_fatty_fish(self):
        out = k.score(log('金枪鱼'))
        self.assertEqual(out['weeklyCounts']['fattyFish'], 0)
        self.assertEqual(out['otherProtein']['whiteFishSeafood'], 1)


class InventoryTests(unittest.TestCase):
    def test_saved_state_ignores_frontmatter_and_empty_rows(self):
        text = '---\nname: kitchen-fridge\ndescription: 示例\nsources: [chat]\n---\n## 每日必有\n- [stated] 茶饮：空\n- [stated] 深色绿叶菜：菠菜\n'
        items = k.parse_fridge(text)
        self.assertEqual(items, ['菠菜'])
        result = k.render_fridge(items)
        self.assertNotIn('kitchen-fridge', result)
        self.assertNotIn('待确认', result)
        rows = [line for line in result.splitlines() if line.startswith('| ') and not line.startswith('| 类别')]
        self.assertEqual(len(rows), 19)

    def test_inventory_round_trip(self):
        first = k.render_fridge(['菠菜', '小白菜', '手抓饼', '未知食材'])
        second = k.render_fridge(k.parse_fridge(first))
        self.assertEqual(first, second)

    def test_common_receipt_noise(self):
        self.assertEqual(k.clean('有机菠菜 250g'), '菠菜')
        self.assertEqual(k.clean('红薯（2026-09-21）'), '红薯')
        self.assertEqual(k.clean('冷冻虾仁 1kg'), '虾仁')

    def test_unknown_is_not_neutral(self):
        self.assertEqual(k.classify('未知食材'), (None, False))
        self.assertIn('待确认', k.render_fridge(['未知食材']))

    def test_multi_category_inventory(self):
        out = k.render_fridge(['小白菜', '松茸'])
        self.assertIn('| 深色绿叶菜 | 小白菜 |', out)
        self.assertIn('| 十字花科 | 小白菜 |', out)
        self.assertIn('| 菌菇 | 松茸 |', out)


class PersonalPlanTests(unittest.TestCase):
    def rows(self, text, frequencies):
        result = k.score(text, '2026-09-07', {'frequencies': frequencies})
        return {row['key']: row for row in result['personalPlan']}

    def test_frequency_changes_do_not_change_food_counts_or_defaults(self):
        text = log('豆腐 菠菜 绿茶')
        original = k.score(text, '2026-09-07')
        result = k.score(text, '2026-09-07', {'frequencies': {
            'legumes': {'period': 'week', 'target': 6}, 'tea': None}})
        self.assertEqual({key: result[key] for key in original}, original)
        rows = {row['key']: row for row in result['personalPlan']}
        self.assertEqual(rows['legumes']['frequency']['target'], 6)
        self.assertEqual(rows['legumes']['recordedCount'], 1)
        self.assertIsNone(rows['tea']['frequency'])
        self.assertEqual(rows['tea']['recordedCount'], 1)
        self.assertEqual(rows['fattyFish']['frequency']['target'], 3)
        self.assertIsNone(rows['otherProtein']['frequency'])
        self.assertEqual(k.score(text, '2026-09-07'), original)

    def test_daily_category_can_become_weekly_and_weekly_can_be_daily(self):
        text = log('菠菜 豆腐', '2026-09-06') + log('菠菜 豆腐') + '- [stated] 晚 | 豆腐\n'
        rows = self.rows(text, {'leafy': {'period': 'week', 'target': 5},
                               'legumes': {'period': 'day', 'target': 2}})
        self.assertEqual(rows['leafy']['recordedCount'], 2)
        self.assertNotIn('metDays', rows['leafy'])
        self.assertEqual(rows['legumes']['metDays'], 1)
        self.assertEqual(rows['legumes']['dailyCounts'], [None] * 5 + [1, 2])

    def test_other_proteins_combined_count_meals_without_crowding_fish_or_soy(self):
        text = log('鸡蛋 鸡胸 三文鱼 豆腐') + '- [stated] 晚 | 牛肉 虾\n'
        rows = self.rows(text, {'otherProtein': {'period': 'week', 'target': 4}})
        self.assertEqual(rows['otherProtein']['recordedCount'], 2)
        self.assertEqual(rows['fattyFish']['recordedCount'], 1)
        self.assertEqual(rows['legumes']['recordedCount'], 1)
        self.assertEqual(rows['legumes']['frequency']['target'], 5)
        self.assertEqual(self.rows(log('三文鱼 豆腐'), {})['otherProtein']['recordedCount'], 0)

    def test_personal_plan_keeps_half_weights_and_unrecorded_days(self):
        rows = self.rows(log('花生酱') + '- [stated] 晚 | 花生酱\n',
                         {'nutsSeeds': {'period': 'week', 'target': 3}})
        self.assertEqual(rows['nutsSeeds']['recordedCount'], 1)
        rows = self.rows('', {'nutsSeeds': {'period': 'day', 'target': 1}})
        self.assertEqual(rows['nutsSeeds']['dailyCounts'], [None] * 7)
        self.assertEqual(rows['nutsSeeds']['metDays'], 0)

    def test_invalid_personal_targets_fail_instead_of_silently_using_defaults(self):
        bad = [None, [], {'goals': 'more vegetables'}, {'frequencies': []},
               {'frequencies': {'neutral': {'period': 'week', 'target': 3}}},
               {'frequencies': {'typo': None}}]
        for target in (0, -1, True, '3', float('nan'), float('inf')):
            bad.append({'frequencies': {'tea': {'period': 'day', 'target': target}}})
        bad.append({'frequencies': {'tea': {'period': 'month', 'target': 3}}})
        for profile in bad:
            with self.subTest(profile=profile), self.assertRaises(ValueError):
                k.profile_frequencies(profile)


class CommandTests(unittest.TestCase):
    def run_cli(self, *args):
        return subprocess.run([sys.executable, str(SCRIPT), *args], capture_output=True, text=True)

    def test_missing_arguments_are_actionable(self):
        for command, flag in [('score', '--log'), ('fridge', '--items'), ('day', '--json')]:
            out = self.run_cli(command)
            self.assertEqual(out.returncode, 2)
            self.assertIn(flag, out.stderr)
            self.assertNotIn('Traceback', out.stderr)

    def test_invalid_date_is_actionable(self):
        out = self.run_cli('score', '--log', str(ROOT / 'examples/meal-log.md'), '--end', 'invalid')
        self.assertEqual(out.returncode, 2)
        self.assertNotIn('Traceback', out.stderr)

    def test_schema_only_lists_supported_commands(self):
        out = self.run_cli('schema')
        self.assertEqual(out.returncode, 0)
        self.assertNotIn('kitchen.py nutri', out.stdout)

    def test_render_escapes_text_and_computes_coverage(self):
        data = json.loads((ROOT / 'examples/day.json').read_text())
        data['title'] = '<script>alert(1)</script>'
        data['score'] = {'n': 999, 'pct': 999}
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'day.json'
            path.write_text(json.dumps(data))
            out = self.run_cli('day', '--json', str(path))
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertNotIn('<script>', out.stdout)
        self.assertIn('&lt;script&gt;', out.stdout)
        self.assertNotIn('999', out.stdout)
        self.assertIn('3/8', out.stdout)
        self.assertNotIn('fonts.googleapis.com', out.stdout)

    def test_invalid_daily_categories_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'day.json'
            path.write_text('{"daily": []}')
            out = self.run_cli('day', '--json', str(path))
        self.assertEqual(out.returncode, 2)
        self.assertIn('eight daily categories', out.stderr)

    def test_score_to_week_pipeline(self):
        with tempfile.TemporaryDirectory() as folder:
            result = Path(folder) / 'week.json'
            out = self.run_cli('score', '--log', str(ROOT / 'examples/meal-log.md'), '-o', str(result))
            self.assertEqual(out.returncode, 0, out.stderr)
            stats = json.loads(result.read_text())
            self.assertEqual(stats['daysWithRecord'], 2)
            out = self.run_cli('week', '--json', str(result))
            self.assertEqual(out.returncode, 0, out.stderr)
            self.assertIn('2026-09-01', out.stdout)
            self.assertIn('7 天里有 2 天记录', out.stdout)

    def test_personal_profile_auto_load_explicit_override_and_week_render(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            meal_log = root / 'kitchen-log.md'
            meal_log.write_text(log('豆腐 绿茶 鸡蛋'), encoding='utf-8')
            profile = root / 'kitchen-profile.json'
            profile.write_text(json.dumps({'frequencies': {
                'legumes': {'period': 'week', 'target': 6}, 'tea': None}}), encoding='utf-8')
            before = (meal_log.read_bytes(), profile.read_bytes())
            output = root / 'week.json'
            result = self.run_cli('score', '--log', str(meal_log), '-o', str(output))
            self.assertEqual(result.returncode, 0, result.stderr)
            result = self.run_cli('week', '--json', str(output))
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn('每周 6 次 · 已记录 1 次', result.stdout)
            self.assertIn('茶饮</strong><br>不设频次', result.stdout)
            self.assertNotIn('每日必有 8 类 · 达标天数', result.stdout)
            self.assertEqual((meal_log.read_bytes(), profile.read_bytes()), before)
            alternate = root / 'alternate.json'
            alternate.write_text('{}', encoding='utf-8')
            result = self.run_cli('score', '--log', str(meal_log), '--profile', str(alternate))
            rows = {r['key']: r for r in json.loads(result.stdout)['personalPlan']}
            self.assertEqual(rows['legumes']['frequency']['target'], 5)
            profile.write_text('null', encoding='utf-8')
            result = self.run_cli('score', '--log', str(meal_log))
            self.assertEqual(result.returncode, 2)
            self.assertIn('profile must be a JSON object', result.stderr)
            self.assertNotIn('Traceback', result.stderr)

    def test_archive_contains_only_installable_skill(self):
        spec = importlib.util.spec_from_file_location('package_skill', ROOT / 'scripts/package_skill.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        with tempfile.TemporaryDirectory() as folder:
            path = module.package(Path(folder) / 'skill.zip')
            first = path.read_bytes()
            module.package(path)
            self.assertEqual(first, path.read_bytes())
            with ZipFile(path) as archive:
                self.assertIn('kitchen/SKILL.md', archive.namelist())
                self.assertTrue(all(n.startswith('kitchen/') for n in archive.namelist()))
                self.assertFalse(any('__pycache__' in n or 'kitchen-log.md' in n for n in archive.namelist()))


if __name__ == '__main__':
    unittest.main()
