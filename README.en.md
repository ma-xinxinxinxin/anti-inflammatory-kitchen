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
<tr><td><strong>1. Organize fridge and pantry inventory</strong></td><td><strong>Check stock:</strong> “What is in my fridge?”<br><br><strong>Add groceries:</strong> say “I bought tomatoes and eggs,” or photograph your groceries or receipt.<br><br><strong>Remove finished items:</strong> “I finished the spinach” or “The olive oil has run out.”</td><td>View fridge, freezer, and pantry stock; update it after purchases or confirmed depletion; check photo recognition before saving, with all 19 categories shown, including empty ones</td></tr>
<tr><td><strong>2. Decide what to eat</strong></td><td>“What should I have for breakfast/lunch/dinner?”<br><br>“I feel like fish tonight.”<br><br>“Give me 3 breakfast options.”</td><td>One meal combination using available ingredients, or a meal built around your preference with sides and a staple suited to the eating plan; multiple options when requested</td></tr>
<tr><td><strong>3. Learn how to cook it</strong></td><td>“Let's make that. Tell me how.”</td><td>Ingredients, order, timing, heat, and doneness cues; weeknight defaults aim for 25 minutes and at most two pans</td></tr>
<tr><td><strong>4. Know what to buy</strong></td><td>“What am I missing for the next three meals?”</td><td>Suggestions based on the anti-inflammatory eating plan, personal goals, and current stock: only missing ingredients needed for planned meals, with their purpose and planned use</td></tr>
<tr><td><strong>5. Plan the rest of the day</strong></td><td>“I ate these foods today. How should I plan the next two meals?”</td><td>Upcoming meals based on the anti-inflammatory eating plan, your frequency settings, recorded meals, and current stock; a meal-plan page when supported</td></tr>
<tr><td><strong>6. Record meals and save favorite recipes</strong></td><td><strong>Log a meal:</strong> “I had this fish soup for dinner.”<br><br><strong>Save a favorite:</strong> “Save this as a favorite recipe called ‘Wednesday fish soup.’”</td><td>Record meals you confirm eating and save recipes you choose, so you can retrieve their instructions by name later</td></tr>
<tr><td><strong>7. Use up perishables</strong></td><td>“The spinach needs using. Build a dish around it.”</td><td>A meal prioritizing ingredients that need attention, reducing waste</td></tr>
<tr><td><strong>8. Review the week</strong></td><td>“Review seven days and help plan next week's meals and shopping.”</td><td>Observations from recorded meals and practical suggestions for variety, preparation, and purchasing</td></tr>
<tr><td><strong>9. Set preferences and goals</strong></td><td>“I avoid cilantro and want more plant protein.”<br><br>“Set legumes and soy to 6 times a week, with no frequency target for tea.”<br><br>“Set other proteins to 4 meals a week combined,” or “No target for other proteins.”</td><td>Save dietary restrictions, allergies, nutrition goals, and personal frequencies; set them at the start, skip them, or change them later, with future meals, shopping, and reviews following your settings</td></tr>
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

### Install it, then set up your kitchen

1. **Install the skill.** Choose a method above; for chat import, upload the guide and ask the assistant to follow it.
2. **Create a dedicated “Anti-Inflammatory Kitchen” Project.** Keep inventory, meals, recipes, and shopping conversations there; enable project memory where supported. If your tool has no Projects feature, start with one ongoing chat.
3. **Set preferences and goals (optional).** Share allergies, dietary restrictions, nutrition goals, and any food frequencies you want to change. Skip this to start with the defaults; you can adjust them later.
4. **Add your real kitchen inventory.** Type, speak, or send grocery and receipt photos, then say “That is everything; organize my inventory.” It organizes fridge, freezer, and pantry ingredients; after that, just tell it what you bought or used up.

Then ask “What should I eat today?” or “Give me 3 breakfast options.” See [where your information goes](#where-your-information-goes) for continuity and [installation checks](docs/installation.en.md#verify) if you need to verify the setup. The skill defaults to Chinese; ask for English to use translated labels alongside the canonical categories.

## How meal guidance works

### Anti-inflammatory food checklist and default frequencies

The 8 daily and 6 weekly categories share one checklist. These are starting points: adjust daily or weekly frequencies to your restrictions, nutrition goals, and habits, or leave a category without a target. Future suggestions follow your confirmed settings.

<table width="100%">
<thead><tr><th width="25%">Category</th><th width="18%">Default frequency</th><th width="57%">Ingredients</th></tr></thead>
<tbody>
<tr><td>Healthy fats</td><td>Once daily</td><td>Extra-virgin olive oil, olive oil, avocado, olives</td></tr>
<tr><td>Nuts and seeds</td><td>Once daily</td><td>Walnuts, almonds, pistachios, pumpkin seeds, ground flaxseed, chia seeds, Brazil nuts, sesame seeds, sesame paste, almond butter; peanut butter counts as 0.5</td></tr>
<tr><td>Fermented foods</td><td>Once daily</td><td>Greek yogurt, unsweetened yogurt, kefir, natto, miso, kimchi, kombucha</td></tr>
<tr><td>Dark leafy greens</td><td>Once daily</td><td>Spinach, kale, watercress, garland chrysanthemum, pea shoots, amaranth greens, Chinese lettuce, young bok choy greens, water spinach, lettuce, bok choy, Chinese broccoli, rapeseed greens</td></tr>
<tr><td>Whole-grain staples</td><td>Once daily</td><td>Oats, brown rice, quinoa, millet, predominantly whole-grain buckwheat noodles, whole-wheat bread, whole-wheat pita</td></tr>
<tr><td>Berries and citrus</td><td>Once daily</td><td>Blueberries, raspberries, strawberries, blackberries, cranberries, oranges, pomelo, kiwifruit, pomegranate, cherries; açaí powder counts as 0.5</td></tr>
<tr><td>Tea</td><td>Once daily</td><td>Green tea, oolong, white tea, black tea, matcha, hibiscus tea</td></tr>
<tr><td>Herbs and spices</td><td>Once daily</td><td>Scallions, garlic, ginger, onions, turmeric powder, black pepper, rosemary, oregano, thyme, cloves, cinnamon, cumin</td></tr>
<tr><td>Oily fish</td><td>3 times/week</td><td>Salmon, mackerel, sardines, anchovies, Pacific saury</td></tr>
<tr><td>Legumes and soy foods</td><td>5 times/week</td><td>Chickpeas, lentils, edamame, black beans, red kidney beans, tofu, pressed tofu, dried tofu skin, unsweetened soy milk, tempeh</td></tr>
<tr><td>Cruciferous vegetables</td><td>4 times/week</td><td>Broccoli, cauliflower, cabbage, red cabbage, arugula, bok choy, young bok choy greens, daikon, Brussels sprouts, Chinese broccoli, rapeseed greens</td></tr>
<tr><td>Red and orange produce</td><td>5 times/week</td><td>Tomatoes/cherry tomatoes, carrots, pumpkin, red peppers, yellow peppers, sweet potatoes, purple sweet potatoes; goji berries count as 0.5</td></tr>
<tr><td>Mushrooms</td><td>3 times/week</td><td>Shiitake, maitake/hen-of-the-woods, oyster mushrooms, wood ear mushrooms, king oyster mushrooms, matsutake, button mushrooms, enoki</td></tr>
<tr><td>Dark chocolate and cocoa</td><td>2 times/week</td><td>Dark chocolate, natural cocoa powder; prefer low added sugar and choose according to tolerance</td></tr>
</tbody>
</table>

### Other proteins and neutral foods

**The default plan includes protein every day while preserving the planned frequencies for oily fish and legumes/soy.** You may set a combined frequency for eggs, white fish/seafood, poultry, and red meat, or leave it unset. These four categories add variety; they do not require an extra daily serving of “other protein,” and their targets should not crowd out fish or soy foods. Allergies and dietary restrictions take priority, with affected categories adjusted and alternatives planned. Neutral foods have no frequency target.

<table width="100%">
<thead><tr><th width="25%">Category</th><th width="23%">Frequency</th><th width="52%">Ingredients</th></tr></thead>
<tbody>
<tr><td>Eggs</td><td>Optional combined target; none by default</td><td>Eggs, boiled eggs, fried eggs</td></tr>
<tr><td>White fish and seafood</td><td>Optional combined target; none by default</td><td>Cod, sea bass, mandarin fish, shrimp, scallops, clams, cuttlefish, squid, tuna of unspecified species</td></tr>
<tr><td>Poultry</td><td>Optional combined target; none by default</td><td>Chicken legs, chicken breast, chicken, duck breast, duck</td></tr>
<tr><td>Red meat</td><td>Optional combined target; none by default</td><td>Beef shank, beef tenderloin, beef brisket, beef, steak, lamb leg, lamb</td></tr>
<tr><td>Neutral foods</td><td>No target</td><td>Seaweed, other fruit and vegetables, dairy and plant milks, cheese, dried fruit, potatoes, Chinese yam, taro, lotus root, pork, honey, and more</td></tr>
</tbody>
</table>

### How it combines them

It starts with your latest kitchen inventory, preferences, and dietary restrictions, prioritizing ingredients you already have or need to use soon to build a complete meal with produce, protein, a staple, and suitable cooking fat. It then checks daily and weekly meal records and adds less represented categories through sides, the next meal, or the next shop, encouraging variety without fitting every category into one meal. Confirmed purchases, depletion, and eaten meals update inventory and meal records separately, informing the next suggestion for what to eat, how to cook, and what is still missing.

**These frequencies are project planning conventions, not medical thresholds or inflammation scores.** A category counts at most once per meal, and one ingredient can cover multiple categories; 0.5 is a logging weight, not a recommended serving size. Neutral foods still have nutritional value; pork retains its original storage category but is nutritionally red meat. See the [nutrition-planning rules](kitchen/references/nutrition-plan.md) and [food table](kitchen/references/food-table.md); the overall eating pattern draws on [AHA dietary guidance](https://professional.heart.org/en/science-news/2021-dietary-guidance-to-improve-cardiovascular-health/top-things-to-know), which does not validate the project's frequencies or individual anti-inflammatory effects.

## Where your information goes

**Create a dedicated “Anti-Inflammatory Kitchen” Project and use it for your everyday kitchen conversations.** Use the skill there, or add the conversation-import guide; keep inventory updates, meal records, recipes, and shopping discussions in that same project. If your tool supports project memory, enable it according to the platform's settings so later conversations can refer to earlier records and food preferences, reducing repeated setup.

Project memory helps carry context forward; the latest confirmed records remain the source of truth for inventory and meal logs. Periodically ask the AI to prepare a snapshot of your personal settings, current inventory, meal log, and saved recipes, and save it in the project's files or sources. If the assistant cannot save it directly, download and upload it yourself. When starting a new chat, ask it to read the latest records before planning. [ChatGPT project guidance](https://learn.chatgpt.com/docs/projects)

- **Local agents:** the selected project's `.kitchen-state/`. Reopen the same project in a new chat.
- **Cloud tools with persistent storage:** the assistant confirms the actual available location and reports saving only after a successful write.
- **Conversation-only tools:** keep records in that conversation, then export personal settings, inventory, recipes, and meal-log snapshots to bring into the next chat.

Different AI tools do not automatically synchronize private records. Downloads contain no personal inventory or dietary history. Keep private state out of public GitHub repositories. [Storage rules](kitchen/references/state-files.md)

## Development, examples, and contributions

The skill itself needs no API key. Local helpers require Python 3.10+ and only the standard library. Host subscriptions, permissions, and capabilities depend on the platform.

[Examples and project structure](docs/development.en.md) · [Contributing](CONTRIBUTING.md) · [Changelog](CHANGELOG.md) · [MIT License](LICENSE)

Kitchen supports everyday food planning. It does not diagnose conditions, interpret lab results, or advise medication or supplement doses.
