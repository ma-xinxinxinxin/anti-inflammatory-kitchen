# Anti-Inflammatory Kitchen · 抗炎厨房

<table><tr><td><a href="README.md">简体中文</a></td><td><strong>English</strong></td></tr></table>

**For people who want to follow an anti-inflammatory diet and eat healthy, clean meals.**

Anti-Inflammatory Kitchen is your AI meal-planning assistant, built around **a healthy anti-inflammatory eating plan and what is in your kitchen right now**. Based on a Mediterranean-style eating pattern, it draws on nutrition research to organize its ingredient list and meal-combination rules. It brings these together with your kitchen inventory, preferences, and recorded meals to tell you **what to eat, how to cook, and what to buy**.

To get started, tell it what is in your kitchen. After that, whenever you shop, type, speak, or send a photo of your groceries or receipt. After cooking, tell it what you ate and what ran out. It updates your kitchen state from that information, so the next recommendation starts with your latest inventory.

Ask “What should I eat today?”, “Give me three breakfast options”, or “What should I stock up on this weekend?” It prioritizes ingredients already in your kitchen and fridge to suggest recipes you can start cooking right away, balancing meal composition with fresh ideas and options. Anything you need to buy is listed separately, so you know what you can make now and what to plan for your next shop.

I now use it every day and wouldn't want to do without it.

[Choose your AI tool](#choose-your-ai-tool) · [Download plugin](downloads/anti-inflammatory-kitchen-plugin.zip) · [Claude Skill ZIP](downloads/kitchen.zip) · [Full installation guide](docs/installation.en.md)

## What you can do

<table width="100%">
<thead>
<tr>
<th width="30%">Task</th>
<th width="32%">Say or do this</th>
<th width="38%">What you get</th>
</tr>
</thead>
<tbody>
<tr><td><strong>1. Organize fridge and pantry inventory</strong></td><td>Type or speak your ingredients, photograph groceries or a receipt, or upload a screenshot: “I bought these; organize them.”</td><td>AI-recognized ingredients, confirmed before updating fridge, freezer, and pantry stock; all 19 categories, including empty ones</td></tr>
<tr><td><strong>2. Decide what to eat</strong></td><td>“What should I have for breakfast/lunch/dinner?” or “I feel like fish tonight.”</td><td>One meal combination using available ingredients, or a meal built around your preference with sides and a staple suited to the eating plan</td></tr>
<tr><td><strong>3. Learn how to cook it</strong></td><td>“Let's make that. Tell me how.”</td><td>Ingredients, order, timing, heat, and doneness cues; weeknight defaults aim for 25 minutes and at most two pans</td></tr>
<tr><td><strong>4. Know what to buy</strong></td><td>“What am I missing for the next three meals?”</td><td>Only ingredients needed by the plan and missing from inventory, with their purpose and planned meals</td></tr>
<tr><td><strong>5. Plan the rest of the day</strong></td><td>“I ate these foods today. How should I plan the next two meals?”</td><td>Daily and weekly coverage used to vary upcoming meals; a meal-plan page when supported</td></tr>
<tr><td><strong>6. Record meals and save recipes</strong></td><td>“I ate this, used up the spinach, and want to save it as Wednesday fish soup.”</td><td>Separate updates to actual meal records, confirmed depleted stock, and recipes you explicitly save</td></tr>
<tr><td><strong>7. Use up perishables</strong></td><td>“The spinach needs using. Build a dish around it.”</td><td>A meal prioritizing ingredients that need attention, reducing waste</td></tr>
<tr><td><strong>8. Review the week</strong></td><td>“Review seven days and help plan next week's meals and shopping.”</td><td>Observations from recorded meals and practical suggestions for variety, preparation, and purchasing</td></tr>
</tbody>
</table>

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

### 8 daily categories

The default plan covers each category daily, adjusted for preferences, allergies, and tolerance.

| Category | Ingredients |
|---|---|
| Healthy fats | Extra-virgin olive oil, olive oil, avocado, olives |
| Nuts and seeds | Walnuts, almonds, pistachios, pumpkin seeds, ground flaxseed, chia seeds, Brazil nuts, sesame seeds, sesame paste, almond butter; peanut butter counts as 0.5 |
| Fermented foods | Greek yogurt, unsweetened yogurt, kefir, natto, miso, kimchi, kombucha |
| Dark leafy greens | Spinach, kale, watercress, garland chrysanthemum, pea shoots, amaranth greens, Chinese lettuce, young bok choy greens, water spinach, lettuce, bok choy, Chinese broccoli, rapeseed greens |
| Whole-grain staples | Oats, brown rice, quinoa, millet, predominantly whole-grain buckwheat noodles, whole-wheat bread, whole-wheat pita |
| Berries and citrus | Blueberries, raspberries, strawberries, blackberries, cranberries, oranges, pomelo, kiwifruit, pomegranate, cherries; açaí powder counts as 0.5 |
| Tea | Green tea, oolong, white tea, black tea, matcha, hibiscus tea |
| Herbs and spices | Scallions, garlic, ginger, onions, turmeric powder, black pepper, rosemary, oregano, thyme, cloves, cinnamon, cumin |

### 6 weekly categories

| Category | Default times/week | Ingredients |
|---|---|---|
| Oily fish | 3 | Salmon, mackerel, sardines, anchovies, Pacific saury |
| Legumes and soy foods | 5 | Chickpeas, lentils, edamame, black beans, red kidney beans, tofu, pressed tofu, dried tofu skin, unsweetened soy milk, tempeh |
| Cruciferous vegetables | 4 | Broccoli, cauliflower, cabbage, red cabbage, arugula, bok choy, young bok choy greens, daikon, Brussels sprouts, Chinese broccoli, rapeseed greens |
| Red and orange produce | 5 | Tomatoes/cherry tomatoes, carrots, pumpkin, red peppers, yellow peppers, sweet potatoes, purple sweet potatoes; goji berries count as 0.5 |
| Mushrooms | 3 | Shiitake, maitake/hen-of-the-woods, oyster mushrooms, wood ear mushrooms, king oyster mushrooms, matsutake, button mushrooms, enoki |
| Dark chocolate and cocoa | 2 | Dark chocolate, natural cocoa powder; prefer low added sugar and choose according to tolerance |

### 4 other protein categories and 1 neutral category

Other proteins are recorded by meal occurrence. Neutral foods appear in inventory without adding to target coverage.

| Category | Ingredients |
|---|---|
| Eggs | Eggs, boiled eggs, fried eggs |
| White fish and seafood | Cod, sea bass, mandarin fish, shrimp, scallops, clams, cuttlefish, squid, tuna of unspecified species |
| Poultry | Chicken legs, chicken breast, chicken, duck breast, duck |
| Red meat | Beef shank, beef tenderloin, beef brisket, beef, steak, lamb leg, lamb |
| Neutral foods | Seaweed, other fruit and vegetables, dairy and plant milks, cheese, dried fruit, potatoes, Chinese yam, taro, lotus root, pork, honey, and more |

### How it combines them

It starts with your latest kitchen inventory, preferences, and dietary restrictions, prioritizing ingredients you already have or need to use soon to build a complete meal with produce, protein, a staple, and suitable cooking fat. It then checks daily and weekly meal records and adds less represented categories through sides, the next meal, or the next shop, encouraging variety without fitting every category into one meal. Confirmed purchases, depletion, and eaten meals update inventory and meal records separately, informing the next suggestion for what to eat, how to cook, and what is still missing.

**These frequencies are project planning conventions, not medical thresholds or inflammation scores.** A category counts at most once per meal, and one ingredient can cover multiple categories; 0.5 is a logging weight, not a recommended serving size. Neutral foods still have nutritional value; pork retains its original storage category but is nutritionally red meat. See the [nutrition-planning rules](kitchen/references/nutrition-plan.md) and [food table](kitchen/references/food-table.md); the overall eating pattern draws on [AHA dietary guidance](https://professional.heart.org/en/science-news/2021-dietary-guidance-to-improve-cardiovascular-health/top-things-to-know), which does not validate the project's frequencies or individual anti-inflammatory effects.

## Where your information goes

**Create a dedicated “Anti-Inflammatory Kitchen” Project and use it for your everyday kitchen conversations.** Use the skill there, or add the conversation-import guide; keep inventory updates, meal records, recipes, and shopping discussions in that same project. If your tool supports project memory, enable it according to the platform's settings so later conversations can refer to earlier records and food preferences, reducing repeated setup.

Project memory helps carry context forward; the latest confirmed records remain the source of truth for inventory and meal logs. Periodically ask the AI to prepare a snapshot of your current inventory, meal log, and saved recipes, and save it in the project's files or sources. If the assistant cannot save it directly, download and upload it yourself. When starting a new chat, ask it to read the latest records before planning. [ChatGPT project guidance](https://learn.chatgpt.com/docs/projects)

- **Local agents:** the selected project's `.kitchen-state/`. Reopen the same project in a new chat.
- **Cloud tools with persistent storage:** the assistant confirms the actual available location and reports saving only after a successful write.
- **Conversation-only tools:** keep records in that conversation, then export inventory, recipes, and meal-log snapshots to bring into the next chat.

Different AI tools do not automatically synchronize private records. Downloads contain no personal inventory or dietary history. Keep private state out of public GitHub repositories. [Storage rules](kitchen/references/state-files.md)

## Development, examples, and contributions

The skill itself needs no API key. Local helpers require Python 3.10+ and only the standard library. Host subscriptions, permissions, and capabilities depend on the platform.

[Examples and project structure](docs/development.en.md) · [Contributing](CONTRIBUTING.md) · [Changelog](CHANGELOG.md) · [MIT License](LICENSE)

Kitchen supports everyday food planning. It does not diagnose conditions, interpret lab results, or advise medication or supplement doses.
