# Anti-Inflammatory Kitchen · 抗炎厨房

<table><tr><td><a href="README.md">简体中文</a></td><td><strong>English</strong></td></tr></table>

**For people who want to follow an anti-inflammatory diet and eat healthy, clean meals.**

Anti-Inflammatory Kitchen is your AI meal-planning assistant, built around **a healthy anti-inflammatory eating plan and what is in your kitchen right now**. Based on a Mediterranean-style eating pattern, it draws on nutrition research to organize its ingredient list and meal-combination rules. It brings these together with your kitchen inventory, preferences, and recorded meals to tell you **what to eat, how to cook, and what to buy**.

To get started, tell it what is in your kitchen. After that, whenever you shop, type, speak, or send a photo of your groceries or receipt. After cooking, tell it what you ate and what ran out. It updates your kitchen state from that information, so the next recommendation starts with your latest inventory.

Ask “What should I eat today?”, “Give me three breakfast options”, or “What should I stock up on this weekend?” It prioritizes ingredients already in your kitchen and fridge to suggest recipes you can start cooking right away, balancing meal composition with fresh ideas and options. Anything you need to buy is listed separately, so you know what you can make now and what to plan for your next shop.

I now use it every day and wouldn't want to do without it.

[Choose your AI tool](#choose-your-ai-tool) · [Download plugin](downloads/anti-inflammatory-kitchen-plugin.zip) · [Claude Skill ZIP](downloads/kitchen.zip) · [Full installation guide](docs/installation.en.md)

## What you can do

| Task | Say or do this | What you get |
|---|---|---|
| **1. Organize fridge and pantry inventory** | Type or speak your ingredients, photograph groceries or a receipt, or upload a screenshot: “I bought these; organize them.” | AI-recognized ingredients, confirmed before updating fridge, freezer, and pantry stock; all 19 categories, including empty ones |
| **2. Decide what to eat** | “What should I have for breakfast/lunch/dinner?” or “I feel like fish tonight.” | One meal combination using available ingredients, or a meal built around your preference with sides and a staple suited to the eating plan |
| **3. Learn how to cook it** | “Let's make that. Tell me how.” | Ingredients, order, timing, heat, and doneness cues; weeknight defaults aim for 25 minutes and at most two pans |
| **4. Know what to buy** | “What am I missing for the next three meals?” | Only ingredients needed by the plan and missing from inventory, with their purpose and planned meals |
| **5. Plan the rest of the day** | “I ate these foods today. How should I plan the next two meals?” | Daily and weekly coverage used to vary upcoming meals; a meal-plan page when supported |
| **6. Record meals and save recipes** | “I ate this, used up the spinach, and want to save it as Wednesday fish soup.” | Separate updates to actual meal records, confirmed depleted stock, and recipes you explicitly save |
| **7. Use up perishables** | “The spinach needs using. Build a dish around it.” | A meal prioritizing ingredients that need attention, reducing waste |
| **8. Review the week** | “Review seven days and help plan next week's meals and shopping.” | Observations from recorded meals and practical suggestions for variety, preparation, and purchasing |

Voice, photo, and receipt recognition depend on the host AI. Unclear items are checked first. While you list stock, it listens; when you ask what to eat, it recommends a meal directly, offering alternatives when you want them. Planned meals are not logged as eaten, and shopping lists are not stock already owned.

## Choose your AI tool

One set of kitchen rules, with different installation paths. **Native installation and importing a guide into a conversation are different experiences.**

| Your tool | Installation or import | Start here |
|---|---|---|
| Claude accounts with custom Skills | Download the ZIP, upload in Customize → Skills, and enable | [Claude upload](docs/installation.en.md#claude-upload) |
| Claude Code | Add this repository as a marketplace and install the plugin | [Plugin installation](docs/installation.en.md#plugins) |
| Codex / local desktop environment | Install through the repository marketplace; standalone skill also supported | [Plugin installation](docs/installation.en.md#plugins) |
| Native ChatGPT web/mobile plugin | Package provided; publisher upload, testing, and platform publication still required. Not listed yet | [ChatGPT publishing and mobile checks](docs/installation.en.md#chatgpt-plugin) |
| Cursor | Agent Plugins-compatible package; standalone skill available before marketplace publication | [Plugin compatibility](docs/installation.en.md#plugins) |
| Gemini CLI | Install the packaged extension, or use standalone skill installation | [Plugin/extension installation](docs/installation.en.md#plugins) |
| Other Agent Skills-compatible tools | Import the complete `kitchen/` folder into the tool's skill directory | [Agent Skills](docs/installation.en.md#agent-skills) |
| ChatGPT web/mobile, Gemini, Kimi, DeepSeek, and other chat interfaces | Upload the single-file guide if text attachments are supported, or paste its contents | [Chat import and mobile](docs/installation.en.md#chat-import) |

**For phone users:** a native plugin package is now provided, but this project has not published an installable Kitchen plugin in the ChatGPT directory. Chat import can be tried without a computer staying online, but it provides guidance to the current conversation; it does not install a native skill or guarantee cross-chat memory or script execution. A Plugins menu does not mean this project is listed there.

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

Expect the **v5.3 inventory with 19 categories**, including empty ones. The skill defaults to Chinese; ask for English and it can add translations beside the canonical Chinese category labels. With chat import, attach the guide first and explicitly request that it be followed. See the [verification steps](docs/installation.en.md#verify).

## How meal guidance works

### Start with the eating pattern, then use what you have

Kitchen focuses on an overall pattern: varied produce and whole grains for fiber and micronutrients; fish, legumes, eggs, and poultry for protein variety; and liquid plant oils, nuts, and fish for unsaturated fats. Garlic, herbs, lemon, and vinegar add flavor while reducing reliance on large amounts of salt and sugar, frequent deep-frying, and processed meat. Chinese cooking fits this approach.

| Planning layer | What the assistant does |
|---|---|
| **Build a complete meal** | Breakfast usually combines a staple, protein, and produce. Lunch/dinner combine vegetables, protein, a staple, and suitable cooking fat. Adjust to appetite, servings, and activity; do not remove staples or serve only vegetables to improve category counts |
| **Check actual stock and preferences** | Read current inventory; prioritize what you want, already own, and need to use soon. Respect allergies and restrictions. Mark missing ingredients or offer substitutions, including for seasonings |
| **Vary food across days and weeks** | Use 8 daily and 6 weekly categories to notice less represented foods. Add variety through sides, another meal, or the next shop; do not squeeze every category into one meal |
| **Give a simple next action** | Recommend one meal when asked what to eat, steps when asked how, and only missing ingredients when asked what to buy. Weeknight defaults aim for 25 minutes and at most two pans |
| **Update from feedback** | Confirmed purchases, depletion, and disposal update stock; confirmed eaten meals update the log. Recompute the next recommendation without treating plans as intake or a meal as proof that all its seasonings ran out |

For example, with salmon, bok choy, and brown rice in stock, it can directly recommend a dinner using all three, checking available oil and seasonings before detailing the method. Bok choy covers both leafy and cruciferous categories. Missing ingredients are identified rather than invented; a recorded coverage gap alone does not justify a long shopping list.

### How the 19-category checklist supports planning

| Group | Includes | Default planning frequency |
|---|---|---|
| 8 daily categories | Healthy fats, nuts/seeds, fermented foods, dark leafy greens, whole grains, berries/citrus, tea, herbs/spices | Cover each daily |
| 6 weekly categories | Oily fish, legumes/soy, cruciferous vegetables, red/orange produce, mushrooms, dark chocolate/cocoa | 3 / 5 / 4 / 5 / 3 / 2 times respectively |
| 4 other protein categories | Eggs, white fish/seafood, poultry, red meat | Record meal occurrences |
| 1 neutral category | Other produce, milk, seaweed, tubers, and more | Display without adding coverage |

A category counts at most once per meal; an ingredient can cover multiple categories. The helper flags unknown ingredients for review. Without code tools, the assistant follows the same rules manually and says so.

**These frequencies are project planning conventions, not medical thresholds or inflammation scores.** Neutral foods still have nutritional value. Missing a category is not a dietary failure. See the [nutrition-planning rules](kitchen/references/nutrition-plan.md) and [food table](kitchen/references/food-table.md). The overall pattern draws on [AHA dietary guidance](https://professional.heart.org/en/science-news/2021-dietary-guidance-to-improve-cardiovascular-health/top-things-to-know); that guidance does not validate the project's frequencies or individual anti-inflammatory effects.

## Where your information goes

- **Local agents:** the selected project's `.kitchen-state/`. Reopen the same project in a new chat.
- **Cloud tools with persistent storage:** the assistant confirms the actual available location and reports saving only after a successful write.
- **Conversation-only tools:** keep records in that conversation, then export inventory, recipes, and meal-log snapshots to bring into the next chat.

Different AI tools do not automatically synchronize private records. Downloads contain no personal inventory or dietary history. Keep private state out of public GitHub repositories. [Storage rules](kitchen/references/state-files.md)

## Development, examples, and contributions

The skill itself needs no API key. Local helpers require Python 3.10+ and only the standard library. Host subscriptions, permissions, and capabilities depend on the platform.

[Examples and project structure](docs/development.en.md) · [Contributing](CONTRIBUTING.md) · [Changelog](CHANGELOG.md) · [MIT License](LICENSE)

Kitchen supports everyday food planning. It does not diagnose conditions, interpret lab results, or advise medication or supplement doses.
