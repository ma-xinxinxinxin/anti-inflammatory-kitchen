# 安装抗炎厨房

**简体中文** · [English](installation.en.md) · [返回首页](../README.md)

选一个与你实际工具对应的入口即可，不要在同一工具里同时装多份 `kitchen`。安装的是规则与脚本，私人库存不会随安装迁移。平台说明核对于 2026-10-04；账号、版本、管理员策略可能影响入口。

<a id="claude-upload"></a>
## Claude：上传安装包

1. [下载 kitchen.zip](../downloads/kitchen.zip)。在 GitHub 文件页面点击下载按钮；不需要自己安装 Python 或重新打包。
2. 根据账号权限，在 Settings → Capabilities 开启 Code execution and file creation。
3. 进入 **Customize → Skills → + → Create skill → Upload a skill**，上传 ZIP 并启用。
4. 新开聊天，说「用抗炎厨房，告诉我版本和分类数量」。应为 v5.2、19 类。

以账号实际界面为准。ZIP 内为 `kitchen/SKILL.md` 和必要参考、脚本文件。上传到普通聊天只是附件，不等于完成 Skills 安装。手机上的安装入口与调用能力仍需在该账号实测，不承诺所有客户端一致。

依据：[Claude 官方安装说明](https://support.claude.com/en/articles/12512180-use-skills-in-claude)。

<a id="local-install"></a>
## Codex、Claude Code、Cursor：本地安装

从 GitHub 选择 **Code → Download ZIP** 并解压，或克隆仓库。在解压后的仓库根目录运行下面一种命令。需要 Python 3.10+；Windows 可将 `python3` 换成 `py -3`。

```bash
# 只选你使用的工具
python3 scripts/install_skill.py --tool codex
python3 scripts/install_skill.py --tool claude
python3 scripts/install_skill.py --tool cursor
python3 scripts/install_skill.py --tool gemini
```

| 参数 | 默认个人安装位置 |
|---|---|
| `codex` | `~/.agents/skills/kitchen/`；检测到已有 `~/.codex/skills/kitchen/` 时沿用旧位置 |
| `claude` | `~/.claude/skills/kitchen/` |
| `cursor` | `~/.cursor/skills/kitchen/` |
| `gemini` | `~/.gemini/skills/kitchen/` |
| `agents` | `~/.agents/skills/kitchen/`，用于支持这个共享目录的工具 |

`~` 表示你的用户主目录。脚本只复制所需文件，不改 AI 工具配置，不联网，不安装依赖。

只给某一个项目安装：

```bash
python3 scripts/install_skill.py --tool cursor --scope project --project "/path/to/your/project"
```

这会安装到该项目 `.cursor/skills/kitchen/`；其他工具使用相应的目录。项目必须已存在。安装后打开新会话：Claude Code 用 `/kitchen`，Codex 用 `$kitchen`，Cursor 在 `/` 菜单查找 kitchen；也可以直接要求「使用抗炎厨房」。

**Codex 另一个入口：** 在已有 Skill Installer 的本地环境中发送「用 Skill Installer 安装 https://github.com/ma-xinxinxinxin/anti-inflammatory-kitchen 的 kitchen 目录」。Skill Installer 可能使用 `~/.codex/skills/`；与本脚本二选一，避免重复安装。

依据：[Claude Code](https://code.claude.com/docs/en/skills) · [Codex](https://learn.chatgpt.com/docs/build-skills) · [Cursor](https://cursor.com/help/customization/skills)。

<a id="gemini-cli"></a>
## Gemini CLI：原生安装命令

在支持 Agent Skills 的 Gemini CLI 版本中：

```bash
gemini skills install https://github.com/ma-xinxinxinxin/anti-inflammatory-kitchen.git --path kitchen
```

按工具提示确认，再用 `/skills list` 检查并在需要时 `/skills reload`。也可使用上节的 `--tool gemini` 安装。这是 **Gemini CLI** 的能力，不等于 Gemini 手机 App 原生支持同一安装方式。

依据：[Gemini CLI 官方说明](https://geminicli.com/docs/cli/skills/)。

<a id="agent-skills"></a>
## 其他 Agent Skills 工具

解压 [kitchen.zip](../downloads/kitchen.zip)，把完整 `kitchen/` 文件夹放到该工具文档规定的目录。不能只复制 `SKILL.md`，参考文件和脚本也需要保留。

若明确支持共享 `.agents/skills/` 目录，可以使用 `--tool agents`。并非所有叫“AI 助手”的产品都支持这个标准；没有相关入口时使用下面的对话导入方式。

<a id="chat-import"></a>
## ChatGPT 手机/网页及其他聊天工具：对话导入

适用于当前界面能读取文本附件或接受足够长文本的 ChatGPT、Gemini、Kimi、DeepSeek 等。这里提供**可尝试的通用方式，不声称已在所有产品、套餐上实测**。

1. 打开 [kitchen-chat-guide.md](../downloads/kitchen-chat-guide.md)，下载原始文件；也可打开 Raw 复制全文。
2. 在手机或网页新开聊天，上传文件或粘贴全文。不要只发送一个未必能读取的 GitHub 链接。
3. 发送：

   ```text
   请按附件里的抗炎厨房指南工作，使用中文。
   先告诉我：能否读取完整指南、能否跨聊天保存库存、能否运行脚本。
   没有脚本时按指南手算；没有持久存储时只维护当前聊天，并提供可复制的状态快照。
   现在等我报冰箱里的食材，不要生成菜谱。
   ```

4. 确认助手确实读到 **v5.2、每日 8 类、每周 6 类、总计 19 类**，然后再开始。
5. 要换聊天时，让它导出库存、常用菜谱和饮食记录，连同指南一起带入。不要把旧聊天能看到误认为状态一定同步。

单文件已包含完整工作流、食材表、状态规则、菜谱规则与视觉说明；**不附 Python 脚本**。手算与 Markdown 表是默认降级方式。若文件太长、上传不支持或模型无法完整读取，当前工具不能完成该导入，不应宣称已安装。

**ChatGPT 原生插件状态：未发布。** 手机出现「插件」入口不表示可以在那里找到抗炎厨房。仓库 ZIP 不是插件发布包，本地 Codex 安装也不会自动变成云端安装。原生手机分发需要独立的插件/工作区发布及验收。参考 [OpenAI skills 文档](https://learn.chatgpt.com/docs/build-skills) 与[插件发布流程](https://developers.openai.com/plugins/deploy/submission)。

<a id="verify"></a>
## 装完怎么验证

使用虚构数据，不用先提供完整私人库存：

| 发送内容 | 应观察到 |
|---|---|
| 「你是哪一版？有多少类？」 | v5.2；每日 8、每周 6、其他蛋白 4、中性 1 |
| 「我有菠菜。」 | 接收本批信息，不抢着出菜谱 |
| 「还有豆腐、三文鱼。就这些，列库存。」 | 19 行完整库存，包含空类别 |
| 「用这些规划晚餐，但还没吃。」 | 给候选；不写成已吃、不默认库存用完 |
| 「我已经吃了小白菜和豆腐，今天和本周还缺什么？」 | 同时说明每日/每周覆盖；小白菜可计入绿叶与十字花科 |
| 新会话读取库存 | 只有确认有持久存储的环境才应自动找回；否则应要求带入快照 |

**验证范围：** 自动检查覆盖安装路径、完整文件复制、拒绝覆盖、升级备份、打包一致性，以及 Python 计数行为。并不等于所有 AI 产品的模型行为、手机 UI、账号同步都通过了实机测试。

## 更新与卸载

先拉取/下载新版仓库，再查看安装目标：

```bash
python3 scripts/install_skill.py --tool cursor --update --dry-run
python3 scripts/install_skill.py --tool cursor --update
```

`--update` 会先把旧版保存在该工具目录中的 `skill-backups/`，再替换 skill；不修改工作区里的 `.kitchen-state/`。已有同名安装时默认停止，不静默覆盖。对原生上传安装，在该平台替换旧版并核对版本；对话导入需带入新指南。

卸载可删除对应的 `kitchen` 安装文件夹，或用平台自带的移除操作。私人状态单独处理，不会随 skill 安装/升级自动迁移。
