# Anti-Inflammatory Kitchen

**English** · [简体中文](README.zh-CN.md)

[![Checks](https://github.com/ma-xinxinxinxin/anti-inflammatory-kitchen/actions/workflows/checks.yml/badge.svg)](https://github.com/ma-xinxinxinxin/anti-inflammatory-kitchen/actions/workflows/checks.yml) [![License: MIT](https://img.shields.io/badge/License-MIT-3D5A3F.svg)](LICENSE)

**An AI kitchen assistant for anti-inflammatory eating, built around what's already in your fridge.**

Tell it once what's in your kitchen. From then on it suggests meals from what you have, shows how to cook them, tells you what to buy, and reviews your week. No calorie counting, no streaks, no guilt.

**[Get started](#get-started)** · [Plugin](downloads/anti-inflammatory-kitchen-plugin.zip) · [Claude Skill ZIP](downloads/kitchen.zip) · [Chat guide](downloads/kitchen-chat-guide.md)

<p align="center"><img src="docs/images/carousel/en-1-cover.jpg" width="440" alt="Start from your fridge, not a recipe. No cooking skills or nutrition knowledge needed. Just ask."></p>

## What it does

<table>
<tr>
<td width="50%"><img src="docs/images/carousel/en-2-log.jpg" alt="Just say what you bought, by voice or a receipt photo, and your stock is updated"></td>
<td width="50%"><img src="docs/images/carousel/en-3-breakfast.jpg" alt="Ask for 3 breakfast options and get meals made only from what's already in your kitchen"></td>
</tr>
<tr>
<td width="50%"><img src="docs/images/carousel/en-4-cook.jpg" alt="Can't cook? Get a step-by-step recipe card with timing and heat"></td>
<td width="50%"><img src="docs/images/carousel/en-5-restock.jpg" alt="Ask what to buy: use up what you have first, then a short list worth buying"></td>
</tr>
<tr>
<td width="50%"><img src="docs/images/carousel/en-6-review.jpg" alt="Weekly review with an anti-inflammatory index, weekly target vs this week"></td>
<td width="50%"><img src="docs/images/carousel/en-7-open-source.jpg" alt="Free and open source. Works with Claude, ChatGPT, Gemini and more"></td>
</tr>
</table>

| | Ask | You get |
|---|---|---|
| **Your fridge** | "Bought salmon, spinach and blueberries" · "The olive oil's finished" · or send a photo of groceries or a receipt | Your stock sorted into 19 food groups, updated as you buy and use things |
| **What to eat** | "What's for dinner?" · "Give me 3 breakfast options" · "I'm at a hawker centre, what should I order?" | Meals made only from what you already have, with nothing extra to buy; eating out or cooking from your own cookbooks works too |
| **How to cook it** | "How do I make that?" · "My spinach is about to go off, what can I cook?" · "Save this as my Wednesday fish soup" | Step-by-step recipes with timing and heat cues, clear-out meals for things about to spoil, and your favorites saved by name |
| **What to buy** | "What should I buy this week?" | What's already at home to use first, then up to three things worth buying |
| **Weekly review** | "How did I eat this week?" | An anti-inflammatory index, your gaps and three actions for next week, as a shareable image |
| **Meal prep** | "I want to prep once for the week" | Three bases in 90 minutes, 10-minute meals on weekdays |

Everything follows your settings: tell it your allergies, foods you avoid, goals like more plant protein, or how often you want each food group, and it plans around them. Works fully in English or Chinese. Planned meals never count as eaten, and a shopping cart never counts as stock.


## Get started

| Your AI tool | How |
|---|---|
| Claude (with custom Skills) | Upload [kitchen.zip](downloads/kitchen.zip) and turn it on · [steps](docs/installation.en.md#claude-upload) |
| Claude Code · Codex · Cursor · Gemini CLI | Install the plugin or the skill folder · [steps](docs/installation.en.md) |
| ChatGPT, Gemini, Kimi, DeepSeek and other chats | Upload the [chat guide](downloads/kitchen-chat-guide.md) to a project or chat · [steps](docs/installation.en.md#chat-import) |
| Any other Agent Skills tool | Import the `kitchen/` folder · [steps](docs/installation.en.md#agent-skills) |

1. Install it, then create a project called "Anti-Inflammatory Kitchen" and turn on memory if your tool has it.
2. Optional: tell it your allergies, restrictions and goals.
3. Tell it what's in your kitchen (type, talk or send photos), then ask "What's for breakfast?"

## Your data

Your stock, meal log, recipes and settings stay in your own project or workspace. The download contains no one's personal data; never commit yours to a public repo. Different AI tools don't sync with each other. [How state is saved](kitchen/references/state-files.md)

## Contribute

No API key needed. Local helpers need Python 3.10+ (standard library only). The skill's instructions are in Chinese; read the [English translation](kitchen/SKILL.en.md).

[Examples and structure](docs/development.en.md) · [Contributing](CONTRIBUTING.md) · [Changelog](CHANGELOG.md) · [MIT License](LICENSE) · [Open an issue](https://github.com/ma-xinxinxinxin/anti-inflammatory-kitchen/issues/new) (use fictional examples, no personal health data)

## Appendix: the full food list

<p align="center"><img src="docs/images/foods-en.png" alt="The full anti-inflammatory food list: 14 groups from most important, weekly servings and every food in each group"></p>

Every food the skill recognizes, by group. Targets are a starting point; change any of them. Details: [nutrition plan](kitchen/references/nutrition-plan.md) · [food table](kitchen/references/food-table.md). The overall pattern follows the [AHA dietary guidance](https://professional.heart.org/en/science-news/2021-dietary-guidance-to-improve-cardiovascular-health/top-things-to-know); the frequencies here are this project's planning defaults, not clinically validated.

---

For everyday meal planning only. It does not diagnose conditions, interpret lab results, or advise on medication or supplement doses.
