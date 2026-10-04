# Install Anti-Inflammatory Kitchen

[简体中文](installation.md) · **English** · [Home](../README.en.md)

Choose one path for your actual tool. Do not install duplicate copies of `kitchen` in the same agent. Rules and scripts are portable; private records are not migrated with them. Platform documentation was checked on 2026-10-04; account permissions and versions can change the available controls.

<a id="plugins"></a>
## Plugin installation: one workflow, multiple host formats

[Download anti-inflammatory-kitchen-plugin.zip](../downloads/anti-inflammatory-kitchen-plugin.zip). It includes Agent Plugins, Codex/Claude Code/Cursor compatibility manifests, a Gemini CLI extension manifest, and the complete `skills/kitchen/` workflow. Choose either the plugin or standalone skill; back up old installations before switching to avoid duplicates.

### Claude Code

Run in your terminal:

```bash
claude plugin marketplace add ma-xinxinxinxin/anti-inflammatory-kitchen
claude plugin install anti-inflammatory-kitchen@kitchen-plugins
```

For a downloaded repository, run `claude plugin marketplace add .` from its root, then the same install command. In a new session, use `/anti-inflammatory-kitchen:kitchen` or ask to use Kitchen. This installs a Claude Code plugin. Claude web/mobile personal Skills use the separate `kitchen.zip` described below.

### Codex / local desktop environment

Download and extract the repository, then run from its root:

```bash
codex plugin marketplace add .
codex plugin add anti-inflammatory-kitchen@kitchen-plugins
```

You can replace `.` with `ma-xinxinxinxin/anti-inflammatory-kitchen` to add the remote repository. Start a new session with the plugin enabled and ask for its version. Local installation does not publish it to ChatGPT cloud/mobile.

### Gemini CLI extension

From the downloaded repository root:

```bash
gemini extensions install ./plugins/anti-inflammatory-kitchen
```

Alternatively, extract the plugin ZIP into a folder named `anti-inflammatory-kitchen` and pass that folder to `gemini extensions install`. Restart Gemini CLI and check `gemini extensions list` and `/skills list`. The repository root is not the extension root: keep the subdirectory in the command. This command does not apply to the Gemini mobile app.

### Cursor and other Agent Plugins hosts

The package's root `plugin.json` and `skills/` follow Agent Plugins. A Cursor manifest and repository marketplace are also provided. Cursor officially supports the format, but this project is not yet listed in Cursor Marketplace. A directory install link will be available only after publication. For now, use `--tool cursor` below to install the complete standalone skill. Other hosts can import the plugin only if they explicitly support this standard; follow their documented controls.

Sources: [OpenAI packaging](https://developers.openai.com/plugins/build/plugins), [Claude Code marketplaces](https://code.claude.com/docs/en/plugin-marketplaces), [Cursor formats](https://cursor.com/docs/reference/plugins), [Gemini extensions](https://geminicli.com/docs/extensions/reference/).

<a id="chatgpt-plugin"></a>
## Native ChatGPT plugin and mobile publishing

**Status: package built; not submitted or listed in the public ChatGPT directory; mobile not yet tested.** The ZIP includes the complete skill. This version does not require an MCP deployment.

<details>
<summary>Maintainers: publish to the public directory</summary>

1. Download the plugin ZIP above. Do not upload the standalone `kitchen.zip` or entire repository ZIP as a plugin.
2. In [OpenAI Plugins](https://platform.openai.com/plugins), select the owning organization/project and verified developer identity. Choose **Upload new or existing plugin → Upload plugin**.
3. Review automated findings under Metadata & Skills; fix and re-upload as required. Enable the plugin in an available test environment and run the [acceptance scenarios](#verify).
4. Submit for review and publish after approval. Add the actual installation link here once published; there is no public one-click installation link yet.
5. On mobile, sign into an account with access and invoke the plugin in a new chat. Check input, direct meal suggestions, recipes, stock updates, and state after reopening. Do not claim mobile installation is complete before distribution and device checks succeed.

Package compatibility, account installation, public listing, and private state synchronization are separate steps. The plugin uses storage supplied by its host; it does not include a cross-platform cloud database. Identity and publishing requirements follow [OpenAI's submission process](https://developers.openai.com/plugins/deploy/submission).

</details>

<a id="claude-upload"></a>
## Claude: upload the skill ZIP

1. [Download kitchen.zip](../downloads/kitchen.zip) using GitHub's download button. No local Python setup is needed.
2. Enable Code execution and file creation in Settings → Capabilities as permitted by your account.
3. Open **Customize → Skills → + → Create skill → Upload a skill**, upload the ZIP, and enable it.
4. Start a new chat and ask for the Kitchen version and category count: v5.4.1 and 19.

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
2. Create a dedicated Kitchen Project and attach the guide to a chat there, or paste its contents. Without Projects, use one ongoing chat. A GitHub URL alone may not be readable by your assistant.
3. Send:

   ```text
   Follow the attached Kitchen guide and respond in English.
   I will share my dietary restrictions, nutrition goals, and frequency preferences (or skip them).
   Then I will list my real kitchen ingredients; wait until I finish before organizing inventory.
   ```

4. Finish with “That is everything; organize my inventory,” then ask what to eat. You do not need to enter sample ingredients first.
5. Before switching chats, export personal settings, inventory, saved recipes, and meal records. Bring those snapshots and the guide into the next chat. Visible chat history is not proof that structured state is synchronized.

The single file embeds the workflow, nutrition plan, food table, state rules, recipe rules, and visual guidance. **It does not include the Python helper.** Manual calculation and Markdown tables are the default fallback. If the host cannot read the complete file, the import is not complete; do not treat it as an installed skill.

**Native ChatGPT plugin: not published.** A Plugins menu does not mean Kitchen is listed. The standalone skill ZIP is not a plugin package; use the plugin ZIP above, and local Codex installation does not synchronize to a cloud account. Native mobile distribution needs a separate supported plugin/workspace publishing and verification process. See [OpenAI skills](https://learn.chatgpt.com/docs/build-skills) and [plugin submission](https://developers.openai.com/plugins/deploy/submission).

<a id="verify"></a>
## Verify your installation

These optional acceptance checks are not required for onboarding. Use fictional data in a separate test project to avoid mixing it with real inventory:

| Prompt | Expected observation |
|---|---|
| “Which version and how many categories?” | v5.4.1; 8 daily, 6 weekly, 4 other proteins, 1 neutral |
| “I have spinach.” | Acknowledge this batch without unsolicited recipes |
| “Also tofu and salmon. That's everything; show inventory.” | All 19 rows, including empty categories |
| “Plan dinner with these, but I haven't eaten it.” | One meal recommendation; no actual-consumption log or assumption that pantry items are finished |
| “I ate bok choy and tofu. What could I add today and this week?” | Both daily and weekly coverage; bok choy can cover leafy greens and cruciferous vegetables |
| “No target for tea; legumes 6 times a week; no target for other proteins.” | Save settings and use them in planning and reviews; include protein daily without crowding out fish or soy foods |
| Read inventory and personal settings in a new chat | Restore only if persistent storage was confirmed; otherwise ask for the snapshot |

**Verification scope:** automated checks cover paths, complete file copying, overwrite refusal, upgrade backups, reproducible packaging, and Python counting behavior. They do not establish model behavior, native mobile UI support, or cross-account synchronization in every AI product.

## Update or remove

Download/pull the new repository, then inspect and update the appropriate installation:

```bash
python3 scripts/install_skill.py --tool cursor --update --dry-run
python3 scripts/install_skill.py --tool cursor --update
```

`--update` preserves the previous copy in the tool directory's `skill-backups/` before replacement. It does not modify the workspace's `.kitchen-state/`. An existing installation is refused by default. Uploaded skills must be replaced through their platform; conversation imports need the new guide.

To uninstall, remove the corresponding `kitchen` installation directory or use the platform's removal control. Private records are separate and are not automatically migrated by installation or upgrades.
