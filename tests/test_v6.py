"""v6: lexicon data file, regional aliases, restock loop and share card."""
import importlib.util
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('kitchen_v6', ROOT / 'kitchen/scripts/kitchen.py')
k = importlib.util.module_from_spec(spec)
spec.loader.exec_module(k)
LEX = json.loads((ROOT / 'kitchen/references/lexicon.json').read_text(encoding='utf-8'))


def log(items, date='2026-09-07'):
    return f'## {date}\n- [stated] 早 | {items}\n'


class LexiconTests(unittest.TestCase):
    def test_nineteen_categories_and_default_targets(self):
        self.assertEqual(len(LEX['daily']), 8)
        self.assertEqual([c['target'] for c in LEX['weekly']], [3, 5, 4, 5, 3, 2])
        self.assertEqual(len(LEX['otherProtein']), 4)

    def test_every_alias_points_to_a_known_food(self):
        for alias, canonical in LEX['aliases'].items():
            self.assertIn(alias, k.VOCAB, alias)
            self.assertEqual(k.VOCAB[alias], k.VOCAB[canonical], alias)

    def test_canonical_words_are_documented_in_food_table(self):
        table = (ROOT / 'kitchen/references/food-table.md').read_text(encoding='utf-8')
        for group in ('daily', 'weekly'):
            for cat in LEX[group]:
                self.assertIn(cat['name'], table)

    def test_regional_and_traditional_names(self):
        out = k.score(log('地瓜 高麗菜 鮭魚 酪梨 奇异果 青江菜'))
        self.assertEqual(out['unrecognizedItems'], [])
        self.assertEqual(out['weeklyCounts']['redOrange'], 1)
        self.assertEqual(out['weeklyCounts']['fattyFish'], 1)
        self.assertEqual(out['weeklyCounts']['cruciferous'], 1)  # same meal, capped once
        self.assertEqual(out['dailyMetDays']['leafy'], 1)        # 青江菜 inherits both categories

    def test_english_inventory_keeps_user_wording(self):
        table = k.render_fridge(k.parse_fridge('Greek yogurt, Olive Oil, bok choy'))
        self.assertIn('| 发酵食品 | Greek yogurt |', table)
        self.assertIn('bok choy', table.split('十字花科')[1].split('\n')[0])

    def test_aliases_never_turn_plant_milk_into_grains(self):
        out = k.score(log('燕麦奶 杏仁奶'))
        self.assertEqual(out['dailyMetDays']['wholeGrain'], 0)
        self.assertEqual(out['dailyMetDays']['nutsSeeds'], 0)


FRIDGE = '- [stated] 豆类与豆制品：鹰嘴豆\n- [stated] 深色绿叶菜：菠菜\n'


class RestockTests(unittest.TestCase):
    def test_in_stock_gaps_are_used_before_buying(self):
        out = k.restock(log('燕麦 蓝莓'), FRIDGE, '2026-09-07')
        used = {x['key'] for x in out['useWhatYouHave']}
        bought = {x['key'] for x in out['worthBuying']}
        self.assertIn('legumes', used)
        self.assertIn('leafy', used)
        self.assertFalse(used & bought)
        self.assertLessEqual(len(out['worthBuying']), 3)

    def test_no_padding_categories_come_last(self):
        out = k.restock(log('燕麦'), '', '2026-09-07', limit=19)
        order = [x['key'] for x in out['worthBuying']]
        tail = [key for key in order if key in k.NO_PADDING]
        self.assertEqual(order[-len(tail):], tail)

    def test_restrictions_are_never_suggested(self):
        profile = {'restrictions': ['三文鱼过敏', '不吃鲭鱼']}
        out = k.restock(log('燕麦'), '', '2026-09-07', profile, limit=19)
        fish = next(x for x in out['worthBuying'] if x['key'] == 'fattyFish')
        self.assertNotIn('三文鱼', fish['options'])
        self.assertNotIn('鲭鱼', fish['options'])

    def test_personal_null_frequency_is_not_a_gap(self):
        out = k.restock(log('燕麦'), '', '2026-09-07', {'frequencies': {'darkChocolate': None, 'tea': None}}, limit=19)
        keys = {x['key'] for x in out['worthBuying'] + out['useWhatYouHave']}
        self.assertNotIn('darkChocolate', keys)
        self.assertNotIn('tea', keys)

    def test_little_evidence_is_flagged(self):
        self.assertEqual(k.restock(log('燕麦'), '', '2026-09-07')['evidence'], 'insufficient')

    def test_cli(self):
        import subprocess, sys, tempfile
        with tempfile.TemporaryDirectory() as d:
            (Path(d) / 'log.md').write_text(log('燕麦'), encoding='utf-8')
            (Path(d) / 'fridge.md').write_text(FRIDGE, encoding='utf-8')
            r = subprocess.run([sys.executable, str(ROOT / 'kitchen/scripts/kitchen.py'), 'restock',
                                '--log', str(Path(d) / 'log.md'), '--fridge', str(Path(d) / 'fridge.md')],
                               capture_output=True, text=True, encoding='utf-8')
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertIn('worthBuying', r.stdout)


class CardTests(unittest.TestCase):
    def week(self):
        w = k.score(log('菠菜 三文鱼 番茄'), '2026-09-07')
        w['review'] = {'actions': ['<b>一</b>', '二', '三', '四']}
        return k.escaped_text(w)

    def test_card_is_fixed_size_and_only_three_actions(self):
        html = k.render_card(self.week())
        self.assertIn('width:1080px;height:1440px', html)
        self.assertEqual(html.count('<div class="a">'), 3)
        self.assertNotIn('<b>一</b>', html)

    def test_card_carries_no_inventory_or_restrictions(self):
        w = self.week()
        w['restrictions'] = ['PRIVATE']
        self.assertNotIn('PRIVATE', k.render_card(w))
        self.assertIn('不是健康评分', k.render_card(w))
        self.assertNotRegex(k.render_card(w), r'[\U0001F300-\U0001FAFF]')


if __name__ == '__main__':
    unittest.main()
