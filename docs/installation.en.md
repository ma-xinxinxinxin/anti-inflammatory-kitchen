# Install Anti-Inflammatory Kitchen

[简体中文](installation.md) · **English** · [Home](../README.en.md)

Choose one path for your actual tool. Do not install duplicate copies of `kitchen` in the same agent. Rules and scripts are portable; private records are not migrated with them. Platform documentation was checked on 2026-10-04; account permissions and versions can change the available controls.

<a id="claude-upload"></a>
## Claude: upload the skill ZIP

1. [Download kitchen.zip](../downloads/kitchen.zip) using GitHub's download button. No local Python setup is needed.
2. Enable Code execution and file creation in Settings → Capabilities as permitted by your account.
3. Open **Customize → Skills → + → Create skill → Upload a skill**, upload the ZIP, and enable it.
4. Start a new chat and ask for the Kitchen version and category count: v5.2 and 19.

Use the controls actually available to your account. The ZIP contains `kitchen/SKILL.md`, references, and the helper. Attaching it to an ordinary conversation is not a Skills installation. Mobile discovery and invocation still require testing on that account; this project does not claim identical behavior across all clients.

Source: [Claude's official instructions](https://support.claude.com/en/articles/12512180-use-skills-in-claude).

<a id="local-install"></a>
## Codex, Claude Code, and Cursor: local installation

Choose **Code → Download ZIP** on GitHub and extract the repository, or clone it. From its root, run the command for your tool. Requires Python 3.10+; on Windows, replace `python3` with `py -3` if needed.

```bash
# Choose your tool, rather than running every line.
python3 scripts/install_skill.py --tool codex
python3 scripts/install_skill.py --tool claude
python3 scripts/install_skill.py --tool cursor
python3 scripts/install_skill.py --tool gemini
```

| Tool argument | Default personal destination |
|---|---|
| `codex` | `~/.agents/skills/kitchen/`; an existing `~/.codex/skills/kitchen/` is reused |
| `claude` | `~/.claude/skills/kitchen/` |
| `cursor` | `~/.cursor/skills/kitchen/` |
| `gemini` | `~/.gemini/skills/kitchen/` |
| `agents` | `~/.agents/skills/kitchen/`, for tools documenting support for this shared directory |

`~` means your home folder. The installer copies an explicit list of skill files. It does not access the network, install dependencies, or change agent configuration.

To install for one existing project:

```bash
python3 scripts/install_skill.py --tool cursor --scope project --project "/path/to/your/project"
```

The destination is that project's `.cursor/skills/kitchen/`; other profiles use their corresponding directory. Open a new session. Use `/kitchen` in Claude Code, `$kitchen` in Codex, or find kitchen in Cursor's `/` menu. You can also explicitly ask the assistant to use Kitchen.

**Codex alternative:** ask the available Skill Installer to install the `kitchen` directory from `https://github.com/ma-xinxinxinxin/anti-inflammatory-kitchen`. That installer may use `~/.codex/skills/`. Choose one installation method to avoid duplicates.

Sources: [Claude Code](https://code.claude.com/docs/en/skills) · [Codex](https://learn.chatgpt.com/docs/build-skills) · [Cursor](https://cursor.com/help/customization/skills).

<a id="gemini-cli"></a>
## Gemini CLI: native command

With an Agent Skills-compatible Gemini CLI version:

```bash
gemini skills install https://github.com/ma-xinxinxinxin/anti-inflammatory-kitchen.git --path kitchen
```

Review the tool's confirmation, then check `/skills list` and use `/skills reload` if needed. The `--tool gemini` installer above is an alternative. This is a **Gemini CLI** feature, not a claim that the Gemini mobile app accepts the same installation.

Source: [Gemini CLI documentation](https://geminicli.com/docs/cli/skills/).

<a id="agent-skills"></a>
## Other Agent Skills-compatible tools

Extract [kitchen.zip](../downloads/kitchen.zip) and put the complete `kitchen/` directory in the location documented by your tool. Copying only `SKILL.md` loses required references and scripts.

Use `--tool agents` only when the tool documents support for `.agents/skills/`. Not every AI assistant supports native skills; use conversation import below when appropriate.

<a id="chat-import"></a>
## ChatGPT mobile/web and other chat tools: conversation import

This is a generic route to try in ChatGPT, Gemini, Kimi, DeepSeek, or another chat interface that can read text attachments or sufficiently long pasted text. **It has not been tested on every product or plan.**

1. Open [kitchen-chat-guide.md](../downloads/kitchen-chat-guide.md), then download the raw file or open Raw and copy all its text.
2. Attach it to a new mobile/web conversation or paste the contents. A GitHub URL alone may not be readable by your assistant.
3. Send:

   ```text
   Follow the attached Kitchen guide and respond in English.
   First confirm whether you can read the complete guide, save inventory across chats,
   and run scripts. Without scripts, calculate manually. Without persistent storage,
   keep state in this chat and provide a copyable snapshot for next time.
   Wait for my ingredients; do not suggest recipes yet.
   ```

4. Confirm the assistant identifies **v5.2, 8 daily categories, 6 weekly categories, and 19 total categories** before you begin.
5. Before switching chats, export inventory, saved recipes, and meal records. Bring those snapshots and the guide into the next chat. Visible chat history is not proof that structured state is synchronized.

The single file embeds the workflow, food table, state rules, recipe rules, and visual guidance. **It does not include the Python helper.** Manual calculation and Markdown tables are the default fallback. If the host cannot read the complete file, the import is not complete; do not treat it as an installed skill.

**Native ChatGPT plugin: not published.** A Plugins menu does not mean Kitchen is listed. The skill ZIP is not a published plugin package, and local Codex installation does not synchronize to a cloud account. Native mobile distribution needs a separate supported plugin/workspace publishing and verification process. See [OpenAI skills](https://learn.chatgpt.com/docs/build-skills) and [plugin submission](https://developers.openai.com/plugins/deploy/submission).

<a id="verify"></a>
## Verify your installation

Start with fictional data:

| Prompt | Expected observation |
|---|---|
| “Which version and how many categories?” | v5.2; 8 daily, 6 weekly, 4 other proteins, 1 neutral |
| “I have spinach.” | Acknowledge this batch without unsolicited recipes |
| “Also tofu and salmon. That's everything; show inventory.” | All 19 rows, including empty categories |
| “Plan dinner with these, but I haven't eaten it.” | Recipe candidates; no actual-consumption log or assumption that pantry items are finished |
| “I ate bok choy and tofu. What could I add today and this week?” | Both daily and weekly coverage; bok choy can cover leafy greens and cruciferous vegetables |
| Read inventory in a new chat | Restore only if persistent storage was confirmed; otherwise ask for the snapshot |

**Verification scope:** automated checks cover paths, complete file copying, overwrite refusal, upgrade backups, reproducible packaging, and Python counting behavior. They do not establish model behavior, native mobile UI support, or cross-account synchronization in every AI product.

## Update or remove

Download/pull the new repository, then inspect and update the appropriate installation:

```bash
python3 scripts/install_skill.py --tool cursor --update --dry-run
python3 scripts/install_skill.py --tool cursor --update
```

`--update` preserves the previous copy in the tool directory's `skill-backups/` before replacement. It does not modify the workspace's `.kitchen-state/`. An existing installation is refused by default. Uploaded skills must be replaced through their platform; conversation imports need the new guide.

To uninstall, remove the corresponding `kitchen` installation directory or use the platform's removal control. Private records are separate and are not automatically migrated by installation or upgrades.
