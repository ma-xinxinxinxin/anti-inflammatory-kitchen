# Anti-Inflammatory Kitchen · 抗炎厨房

<table><tr><td><a href="README.md">简体中文</a></td><td><strong>English</strong></td></tr></table>

**For home cooks who want more varied meals—and spend too much time deciding what to eat.**

Anti-Inflammatory Kitchen is a portable skill for AI assistants. Inspired by Mediterranean-style eating, it combines what you feel like eating, what is in your fridge, and the meals you have recorded to suggest your next meal, plan shopping, and review your week. **No weighing, calorie counting, or daily streaks.**

You tell it what you have, what you want, and what you actually ate. It turns that information into practical dishes and clear food-group guidance.

[Choose your AI tool](#choose-your-ai-tool) · [Download skill ZIP](downloads/kitchen.zip) · [Download chat guide](downloads/kitchen-chat-guide.md) · [Full installation guide](docs/installation.en.md)

## What you can do

| Task | Try saying | What you get |
|---|---|---|
| Organize your fridge | “I bought spinach, tofu, and salmon. The soy milk is finished.” | Inventory in consistent food categories, including empty ones |
| Save favorite recipes | “Save this as Wednesday fish soup.” | A recipe you can recall by name; cross-chat storage depends on your tool |
| Choose your next meal | “I feel like fish. Give me two options using my fridge.” | Two or three candidates before you choose |
| Get cooking instructions | “The second one. Explain the steps and how to judge doneness.” | Ingredients, timing, steps, and cooking cues |
| Plan today's meals | “What could I add today? Plan dinner too.” | Daily and weekly coverage gaps; a continuous meal-plan page when supported |
| Shop for what is missing | “Only buy what is missing, enough for three meals.” | A list based on recorded meals and current inventory |
| Use up perishables | “The spinach needs using. Build a dish around it.” | Ideas that prioritize the ingredients you specify |
| Review the week | “Review these seven days and give me three actions for next week.” | Recorded-meal statistics and practical next steps |

While you list ingredients, it listens rather than jumping into recipes. Planned meals never count as meals already eaten, and missing records are not treated as proof that you skipped a food.

## Choose your AI tool

One set of kitchen rules, with different installation paths. **Native installation and importing a guide into a conversation are different experiences.**

| Your tool | Installation or import | Start here |
|---|---|---|
| Claude accounts with custom Skills | Download the ZIP, upload in Customize → Skills, and enable | [Claude upload](docs/installation.en.md#claude-upload) |
| Claude Code | Install into `.claude/skills/kitchen` | [Local installation](docs/installation.en.md#local-install) |
| Codex / local Codex in ChatGPT desktop | Skill Installer, or install into `.agents/skills/kitchen` | [Local installation](docs/installation.en.md#local-install) |
| Cursor | Install into `.cursor/skills/kitchen` | [Local installation](docs/installation.en.md#local-install) |
| Gemini CLI | Official install command, or `.gemini/skills/kitchen` | [Gemini CLI](docs/installation.en.md#gemini-cli) |
| Other Agent Skills-compatible tools | Import the complete `kitchen/` folder into the tool's skill directory | [Agent Skills](docs/installation.en.md#agent-skills) |
| ChatGPT web/mobile, Gemini, Kimi, DeepSeek, and other chat interfaces | Upload the single-file guide if text attachments are supported, or paste its contents | [Chat import and mobile](docs/installation.en.md#chat-import) |

**For phone users:** this project has not published an installable Kitchen plugin in the ChatGPT directory. Chat import can be tried without a computer staying online, but it provides guidance to the current conversation; it does not install a native skill or guarantee cross-chat memory or script execution. A Plugins menu does not mean this project is listed there.

### Prefer not to use a terminal?

- **Claude Skills:** [download kitchen.zip](downloads/kitchen.zip) and follow the upload instructions.
- **Ordinary AI chat:** [open the single-file guide](downloads/kitchen-chat-guide.md), download the raw file from GitHub, and attach it to a chat. Alternatively, open Raw and paste its complete contents.
- **A local AI agent:** give a file-capable assistant this request:

```text
Install the kitchen skill from https://github.com/ma-xinxinxinxin/anti-inflammatory-kitchen.
Read docs/installation.en.md first and choose the native path for this tool.
Preserve existing installations and private records. If native skills are unavailable,
explain that and use the single-file conversation guide instead.
```

### Start with one small task

```text
Use Anti-Inflammatory Kitchen and respond in English.
First tell me whether this environment can save inventory across chats.
I have spinach, tofu, and salmon. That is everything.
Only update inventory for now; do not suggest recipes yet.
```

Expect the **v5.2 inventory with 19 categories**, including empty ones. The skill defaults to Chinese; ask for English and it can add translations beside the canonical Chinese category labels. With chat import, attach the guide first and explicitly request that it be followed. See the [verification steps](docs/installation.en.md#verify).

## How meal guidance works

Your preference comes first, then available ingredients, then gaps in your recorded meals. Weeknight recipes default to about 25 minutes and at most two pans. Chinese cooking fits the approach; dishes do not need to be Western.

| Group | Includes | Default planning frequency |
|---|---|---|
| 8 daily categories | Healthy fats, nuts/seeds, fermented foods, dark leafy greens, whole grains, berries/citrus, tea, herbs/spices | Cover each daily |
| 6 weekly categories | Oily fish, legumes/soy, cruciferous vegetables, red/orange produce, mushrooms, dark chocolate/cocoa | 3 / 5 / 4 / 5 / 3 / 2 times respectively |
| 4 other protein categories | Eggs, white fish/seafood, poultry, red meat | Record meal occurrences |
| 1 neutral category | Other produce, milk, seaweed, tubers, and more | Display without adding coverage |

A category counts at most once per meal; an ingredient can cover multiple categories. The helper flags unknown ingredients for review. Without code tools, the assistant follows the same rules manually and says so.

**These frequencies are project planning conventions, not medical thresholds or inflammation scores.** Neutral foods still have nutritional value. Missing a category is not a dietary failure. See the [food table and sources](kitchen/references/food-table.md) for the detailed rules.

## Where your information goes

- **Local agents:** the selected project's `.kitchen-state/`. Reopen the same project in a new chat.
- **Cloud tools with persistent storage:** the assistant confirms the actual available location and reports saving only after a successful write.
- **Conversation-only tools:** keep records in that conversation, then export inventory, recipes, and meal-log snapshots to bring into the next chat.

Different AI tools do not automatically synchronize private records. Downloads contain no personal inventory or dietary history. Keep private state out of public GitHub repositories. [Storage rules](kitchen/references/state-files.md)

## Development, examples, and contributions

The skill itself needs no API key. Local helpers require Python 3.10+ and only the standard library. Host subscriptions, permissions, and capabilities depend on the platform.

[Examples and project structure](docs/development.en.md) · [Contributing](CONTRIBUTING.md) · [Changelog](CHANGELOG.md) · [MIT License](LICENSE)

Kitchen supports everyday food planning. It does not diagnose conditions, interpret lab results, or advise medication or supplement doses.
