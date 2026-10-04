# 安装抗炎厨房

**简体中文** · [English](installation.en.md) · [返回首页](../README.md)

选一个与你实际工具对应的入口即可，不要在同一工具里同时装多份 `kitchen`。安装的是规则与脚本，私人库存不会随安装迁移。平台说明核对于 2026-10-04；账号、版本、管理员策略可能影响入口。

<a id="plugins"></a>
## 插件安装：同一套规则，多个平台格式

[下载插件包 anti-inflammatory-kitchen-plugin.zip](../downloads/anti-inflammatory-kitchen-plugin.zip)。包内含 Agent Plugins 标准入口、Codex/Claude Code/Cursor 兼容入口、Gemini CLI 扩展入口，以及完整 `skills/kitchen/`。插件版和独立 skill 版选一个使用，升级前备份旧版，避免重复加载。

### Claude Code

在终端执行（仓库版本合并到主分支后）：

```bash
claude plugin marketplace add ma-xinxinxinxin/anti-inflammatory-kitchen
claude plugin install anti-inflammatory-kitchen@kitchen-plugins
```

下载仓库后也可离线选择本地来源：在仓库根目录运行 `claude plugin marketplace add .`，再执行同一安装命令。新会话可用 `/anti-inflammatory-kitchen:kitchen`，或直接说「用抗炎厨房」。这是 Claude Code 插件；Claude 手机/网页的个人 Skills 安装仍使用下节的 `kitchen.zip`。

### Codex / 本地桌面环境

下载并解压完整仓库，在仓库根目录运行：

```bash
codex plugin marketplace add .
codex plugin add anti-inflammatory-kitchen@kitchen-plugins
```

也可把第一条命令的 `.` 换成 `ma-xinxinxinxin/anti-inflammatory-kitchen`，直接添加远端仓库。新会话启用插件后发送「用抗炎厨房，告诉我版本」。本地插件安装不等于完成 ChatGPT 云端/手机发布。

### Gemini CLI 扩展

下载仓库后，在仓库根目录运行：

```bash
gemini extensions install ./plugins/anti-inflammatory-kitchen
```

也可解压插件 ZIP 到名为 `anti-inflammatory-kitchen` 的文件夹，再对该文件夹运行 `gemini extensions install`。重启 Gemini CLI，用 `gemini extensions list` 和 `/skills list` 检查。仓库根目录不是 Gemini 扩展根目录，不要省略子目录；Gemini 手机 App 不适用这条命令。

### Cursor 与其他 Agent Plugins 宿主

包内的根 `plugin.json` 与 `skills/` 遵循 Agent Plugins；同时提供 Cursor manifest 和仓库 marketplace。Cursor 官方支持该格式，但本项目尚未上架 Cursor Marketplace；不要搜索一个尚不存在的安装链接。发布后可从目录安装；当前可使用下方 `--tool cursor` 安装完整 skill。其他宿主只有明确支持该标准时才能导入插件包，实际入口以其说明为准。

依据：[OpenAI 插件格式](https://developers.openai.com/plugins/build/plugins) · [Claude Code 插件市场](https://code.claude.com/docs/en/plugin-marketplaces) · [Cursor 插件格式](https://cursor.com/docs/reference/plugins) · [Gemini 扩展](https://geminicli.com/docs/extensions/reference/)。

<a id="chatgpt-plugin"></a>
## ChatGPT 原生插件与手机发布

**当前状态：插件包已制作，尚未提交或上架 ChatGPT 公共目录，手机端尚未实测。** ZIP 已包含完整 skill，不需要为本版本部署 MCP 服务。

供发布者操作：

1. 下载上述插件 ZIP；不要把单独的 `kitchen.zip` 或整个 GitHub 仓库 ZIP 当成插件上传。
2. 在 [OpenAI Plugins](https://platform.openai.com/plugins) 选择组织/项目和已验证的发布者身份，使用 **Upload new or existing plugin → Upload plugin** 上传。
3. 检查 Metadata & Skills 的自动验证结果；修复问题后重新上传。在可用的测试环境启用插件并执行[验收场景](#verify)。
4. 按平台要求提交审核，获批后选择发布。发布后将实际安装链接加回本页；目前没有可提供给普通用户的一键安装链接。
5. 在手机登录具有该插件权限的账号，新建聊天调用；验证食材输入、直接推荐餐食、做法、库存更新和重新打开后的状态。平台目录审核和手机验收通过前，不宣称“手机安装已完成”。

插件格式兼容、账号安装、公开上架和私人库存同步是四件不同的事。本插件使用宿主可用的存储，并不自带跨平台云数据库。发布步骤与身份要求依据 [OpenAI 官方流程](https://developers.openai.com/plugins/deploy/submission)。

<a id="claude-upload"></a>
## Claude：上传安装包

1. [下载 kitchen.zip](../downloads/kitchen.zip)。在 GitHub 文件页面点击下载按钮；不需要自己安装 Python 或重新打包。
2. 根据账号权限，在 Settings → Capabilities 开启 Code execution and file creation。
3. 进入 **Customize → Skills → + → Create skill → Upload a skill**，上传 ZIP 并启用。
4. 新开聊天，说「用抗炎厨房，告诉我版本和分类数量」。应为 v5.4、19 类。

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
2. 在手机或网页创建专用「抗炎厨房」Project，在其中新开聊天，上传文件或粘贴全文；没有项目功能时用固定聊天。不要只发送一个未必能读取的 GitHub 链接。
3. 发送：

   ```text
   请按附件里的抗炎厨房指南工作，使用中文。
   我会先告诉你个人忌口、营养目标和想调整的食物频次（也可以先跳过）。
   然后我会报厨房里的真实食材，等我报完再整理库存。
   ```

4. 报完真实食材后说「就这些，整理库存」，然后就可以问「今天吃什么」；不需要先录入示例食材。
5. 要换聊天时，让它导出个人设置、库存、常用菜谱和饮食记录，连同指南一起带入。不要把旧聊天能看到误认为状态一定同步。

单文件已包含完整工作流、营养规划、食材表、状态规则、菜谱规则与视觉说明；**不附 Python 脚本**。手算与 Markdown 表是默认降级方式。若文件太长、上传不支持或模型无法完整读取，当前工具不能完成该导入，不应宣称已安装。

**ChatGPT 原生插件状态：未发布。** 手机出现「插件」入口不表示可以在那里找到抗炎厨房。单独的 kitchen.zip 不是插件发布包；插件 ZIP 见上节，本地 Codex 安装也不会自动变成云端安装。原生手机分发需要独立的插件/工作区发布及验收。参考 [OpenAI skills 文档](https://learn.chatgpt.com/docs/build-skills) 与[插件发布流程](https://developers.openai.com/plugins/deploy/submission)。

<a id="verify"></a>
## 装完怎么验证

以下是可选验收，不是首次使用的必经步骤；需要测试时使用独立测试项目中的虚构数据，避免混入真实库存：

| 发送内容 | 应观察到 |
|---|---|
| 「你是哪一版？有多少类？」 | v5.4；每日 8、每周 6、其他蛋白 4、中性 1 |
| 「我有菠菜。」 | 接收本批信息，不抢着出菜谱 |
| 「还有豆腐、三文鱼。就这些，列库存。」 | 19 行完整库存，包含空类别 |
| 「用这些规划晚餐，但还没吃。」 | 直接给一套搭配；不写成已吃、不默认库存用完 |
| 「我已经吃了小白菜和豆腐，今天和本周还缺什么？」 | 同时说明每日/每周覆盖；小白菜可计入绿叶与十字花科 |
| 「茶饮不设频次，豆类改成每周 6 次，其他蛋白不设频次。」 | 保存个人设置，后续规划和复盘使用新频次；每天仍安排蛋白质，鱼和豆制品的计划不被其他蛋白挤占 |
| 新会话读取库存和个人设置 | 只有确认有持久存储的环境才应自动找回；否则应要求带入快照 |

**验证范围：** 自动检查覆盖安装路径、完整文件复制、拒绝覆盖、升级备份、打包一致性，以及 Python 计数行为。并不等于所有 AI 产品的模型行为、手机 UI、账号同步都通过了实机测试。

## 更新与卸载

先拉取/下载新版仓库，再查看安装目标：

```bash
python3 scripts/install_skill.py --tool cursor --update --dry-run
python3 scripts/install_skill.py --tool cursor --update
```

`--update` 会先把旧版保存在该工具目录中的 `skill-backups/`，再替换 skill；不修改工作区里的 `.kitchen-state/`。已有同名安装时默认停止，不静默覆盖。对原生上传安装，在该平台替换旧版并核对版本；对话导入需带入新指南。

卸载可删除对应的 `kitchen` 安装文件夹，或用平台自带的移除操作。私人状态单独处理，不会随 skill 安装/升级自动迁移。
