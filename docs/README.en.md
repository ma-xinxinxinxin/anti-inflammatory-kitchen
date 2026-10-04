# Anti-Inflammatory Kitchen · 抗炎厨房

A Chinese-language agent skill for turning the food in your fridge into practical meals. It supports inventory updates, saved recipes, meal suggestions, cooking instructions, daily plans, shopping lists, using up perishables, and weekly reviews.

No calorie counting, weighing, streaks, or weight targets. The assistant offers a few dishes before expanding a recipe, and keeps all 19 inventory categories visible, including empty ones.

## Install

- **Local ChatGPT desktop / Codex skills:** ask Skill Installer to install the `kitchen` folder from `https://github.com/ma-xinxinxinxin/anti-inflammatory-kitchen`. Invoke `$kitchen` or select 抗炎厨房.
- **Claude Code:** place the entire `kitchen/` folder in `~/.claude/skills/`, backing up an existing installation first.
- **Claude environments supporting skill uploads:** run `python3 scripts/package_skill.py` from the repository root and upload `dist/kitchen.zip`.

Local installation does not imply installation in ChatGPT web or mobile. See [OpenAI's skill documentation](https://learn.chatgpt.com/docs/build-skills) for distribution options.

Python helpers require Python 3.10+ and the standard library only. The host assistant provides language understanding, image recognition, and recipe generation; no additional API key is required by this repository.

## Try it

Ask: “Use kitchen. I have spinach, tofu, and salmon. Suggest two dinners that take under 25 minutes.” Responses default to Chinese; you can request another language, while retaining canonical Chinese category labels for consistency.

Or run the fictional examples:

```bash
python3 kitchen/scripts/kitchen.py fridge --items "菠菜, 西兰花, 松茸"
python3 kitchen/scripts/kitchen.py score --log examples/meal-log.md --end 2026-09-07 -o /tmp/week.json
python3 kitchen/scripts/kitchen.py week --json /tmp/week.json -o /tmp/week.html
python3 kitchen/scripts/kitchen.py day --json examples/day.json -o /tmp/today.html
python3 -m unittest discover -s tests -v
```

## What the numbers mean

Eight daily categories track food-group coverage. Six weekly categories have planning targets: oily fish 3, legumes and soy foods 5, cruciferous vegetables 4, red/orange produce 5, mushrooms 3, and dark chocolate/cocoa 2. Four other protein categories and one neutral category are recorded without coverage targets.

These are project conventions, not clinically validated thresholds or an inflammation score. “Neutral” does not mean nutritionally unhelpful. Unknown ingredients are flagged for review; missing records are not treated as proof that a food was not eaten. Plans never count as meals already eaten.

## Storage and privacy

Local assistants keep private state in the current project's `.kitchen-state/`. Continue in the same project to reuse it. Other environments may offer persistent memory tools; without those, export the state files and upload them next time. Installing the skill does not migrate or synchronize personal data between Claude and ChatGPT.

Private state is excluded from version control. Public examples are fictional. The HTML reports work offline and do not load remote fonts. The skill does not diagnose conditions, interpret lab results, or advise medication or supplement doses.

[Chinese guide](../README.md) · [Evidence and counting rules](../kitchen/references/food-table.md) · [Contributing](../CONTRIBUTING.md) · [MIT license](../LICENSE)
