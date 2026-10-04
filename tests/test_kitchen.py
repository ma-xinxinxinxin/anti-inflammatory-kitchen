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
