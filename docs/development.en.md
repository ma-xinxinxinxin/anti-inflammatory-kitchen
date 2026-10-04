# Development and examples

[简体中文](development.md) · **English** · [Home](../README.en.md)

Most users can start with the [installation guide](installation.en.md). This page is for inspecting helpers, changing rules, or maintaining downloads. Python 3.10+ is required, with no third-party dependencies. On Windows, use `py -3` instead of `python3`; Python UTF-8 mode is recommended for Chinese terminal output.

## Run the examples

Run from the repository root. Packaging first creates `dist/`, a Git-ignored directory also used for demo output:

```bash
python3 scripts/package_skill.py
python3 kitchen/scripts/kitchen.py fridge --items "有机菠菜 250g, 西兰花, 松茸, 手抓饼"
python3 kitchen/scripts/kitchen.py score --log examples/meal-log.md --end 2026-09-07 -o dist/week.json
python3 kitchen/scripts/kitchen.py week --json dist/week.json -o dist/week.html
python3 kitchen/scripts/kitchen.py day --json examples/day.json -o dist/today.html
python3 kitchen/scripts/kitchen.py schema
```

Examples use fictional data. Generated HTML works offline without remote fonts. The helper reads supplied files and writes results; it does not independently change inventory or call a model. The host assistant handles natural language, photos, and recipe suggestions. The helper's ingredient vocabulary is primarily Chinese: the assistant should map other-language ingredients to canonical table entries before invoking it, rather than assume automatic translation.

Incomplete logs show the actual number of recorded days. Unknown ingredients appear in `unrecognizedItems`; unrecognized does not mean uneaten.

## Repository structure

| Path | Purpose |
|---|---|
| `kitchen/SKILL.md` | Shared workflow and version |
| `kitchen/references/` | Food, state, recipe, and visual rules |
| `kitchen/scripts/kitchen.py` | Inventory tables, counts, daily and weekly cards |
| `scripts/install_skill.py` | Tool-specific destinations and upgrade backups |
| `scripts/package_skill.py` | Generate distributions from the same sources |
| `downloads/` | Ready-to-download ZIP and single-file chat guide |
| `examples/`, `tests/` | Fictional examples and regression checks |
| `.kitchen-state/` | Private user state, ignored by Git and excluded from packages |

## Build and verify

```bash
python3 -m unittest discover -s tests -v
python3 scripts/package_skill.py --publish
python3 scripts/package_skill.py --check
```

Default packaging writes to `dist/`. `--publish` only rebuilds the repository's `downloads/`; it does not publish online. Commit refreshed downloads alongside source changes. `--check` compares downloads with generated content byte for byte, preventing stale rules from shipping. An explicit ZIP allowlist excludes state, caches, demos, and repository administration files. The chat guide embeds references but not the Python helper.

CI checks Linux (Python 3.10 and 3.13) and Windows (Python 3.13). These checks validate files and scripts, not installation inside every AI product, phone, or account. See [manual acceptance scenarios](installation.en.md#verify).

See the [contribution guide](../CONTRIBUTING.md) for change conventions and behavioral checks. Never use personal inventory, chat exports, or health records as public test fixtures.
