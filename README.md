# 抗炎厨房 · Anti-Inflammatory Kitchen

<table><tr><td><strong>简体中文</strong></td><td><a href="README.en.md">English</a></td></tr></table>

**给经常自己做饭、想吃得更多样，却每天都在纠结吃什么的人。**

抗炎厨房是一个可带到不同 AI 助手里的饮食搭配 skill。它以地中海饮食为基础，结合你想吃的东西、冰箱库存和已经记录的饮食，帮你决定下一顿、列补货清单、回顾一周。**不用称重、算卡路里或每天打卡。**

你负责告诉它有什么、想吃什么、实际吃了什么；它负责把这些信息变成好做的菜和清楚的搭配建议。

[选择安装方式](#选择你的-ai-工具) · [下载 skill ZIP](downloads/kitchen.zip) · [下载对话指南](downloads/kitchen-chat-guide.md) · [完整安装说明](docs/installation.md)

## 它能帮你做什么

| 操作 | 你可以这样说 | 你会得到什么 |
|---|---|---|
| 整理冰箱 | 「买了菠菜、豆腐和三文鱼，豆浆用完了。」 | 按固定食物类别整理的库存，空缺也显示 |
| 保存常用菜谱 | 「存下来，以后叫它周三鱼汤。」 | 下次能按名字找回的菜谱；能否跨聊天保存取决于工具 |
| 决定下一顿 | 「今天想吃鱼，结合冰箱给两个方案。」 | 先给 2–3 个候选，由你选择 |
| 展开具体做法 | 「选第二个，告诉我怎么做、怎么判断火候。」 | 食材、步骤、时间与烹饪判断节点 |
| 规划今日搭配 | 「今天还缺什么？顺便安排晚餐。」 | 每日与每周的搭配缺口；支持时生成连续长页餐单 |
| 生成补货清单 | 「只买现在缺的，够接下来三顿。」 | 结合饮食记录和库存的补货建议 |
| 优先清库 | 「菠菜快坏了，围绕它做一道菜。」 | 优先用掉指定食材的方案 |
| 复盘一周 | 「回顾这七天，给三个下周能做的动作。」 | 基于已记录餐次的统计和具体行动 |

你还在报库存时，它先接收，不抢着出菜谱。计划的饭不会算成已经吃过；没记的饭也不会被当作没吃。

## 选择你的 AI 工具

同一份厨房规则，按工具能力选择使用方式。**原生安装和对话导入不是一回事。**

| 你使用的工具 | 安装或导入方式 | 从这里开始 |
|---|---|---|
| Claude（有自定义 Skills 入口的账号） | 下载 ZIP，在 Customize → Skills 上传并启用 | [Claude 上传步骤](docs/installation.md#claude-upload) |
| Claude Code | 安装到 `.claude/skills/kitchen` | [本地安装](docs/installation.md#local-install) |
| Codex / ChatGPT 桌面的本地 Codex 环境 | Skill Installer，或安装到 `.agents/skills/kitchen` | [本地安装](docs/installation.md#local-install) |
| Cursor | 安装到 `.cursor/skills/kitchen` | [本地安装](docs/installation.md#local-install) |
| Gemini CLI | 官方安装命令，或安装到 `.gemini/skills/kitchen` | [Gemini CLI](docs/installation.md#gemini-cli) |
| 其他支持 Agent Skills 的工具 | 导入整个 `kitchen/` 目录到该工具的 skill 目录 | [通用 Agent Skills](docs/installation.md#agent-skills) |
| ChatGPT 网页/手机、Gemini、Kimi、DeepSeek 等聊天界面 | 在能读取文本附件的会话上传单文件指南，或复制全文 | [对话导入与手机使用](docs/installation.md#chat-import) |

**手机用户先看这里：** 本仓库尚未发布可在 ChatGPT 插件目录安装的抗炎厨房插件。手机可尝试“对话导入”，不依赖电脑在线，但它只为当前对话提供规则，不等于原生安装，不保证跨聊天记忆或自动执行脚本。界面有「插件」入口也不代表本项目已经上架。

### 不想碰命令行？

- **Claude Skills 用户：** [下载 kitchen.zip](downloads/kitchen.zip)，按上传步骤安装。
- **普通聊天用户：** [打开单文件指南](downloads/kitchen-chat-guide.md)，在 GitHub 点击下载原始文件的按钮，上传到对话；也可打开 Raw 后复制全文。
- **本地 AI 工具用户：** 将下面的话交给有文件访问权限的助手：

```text
请从 https://github.com/ma-xinxinxinxin/anti-inflammatory-kitchen 安装 kitchen skill。
先读取 docs/installation.md，按当前工具选择原生安装路径。
保留已有安装和私人记录；如果当前环境不支持原生 skill，请说明并使用单文件对话指南。
```

### 安装后，先完成一件小事

```text
用抗炎厨房。先告诉我这里能否跨聊天保存库存。
冰箱有菠菜、豆腐和三文鱼，就这些。请只更新库存，先不要给菜谱。
```

应看到 **v5.2 的 19 类库存**，包括空类别。如果是对话导入，先上传指南，并明确要求按附件工作。所有使用方式的验证步骤见[安装验收](docs/installation.md#verify)。

## 它如何判断搭配

先尊重你想吃什么，再看现有食材，最后考虑饮食记录中的缺口。默认工作日晚餐尽量在 25 分钟、两个锅以内完成。中式做法也适用，不要求做成西餐。

| 分组 | 内容 | 默认规划频率 |
|---|---|---|
| 每日 8 类 | 优质脂肪、坚果种子、发酵食品、深色绿叶菜、全谷主食、浆果柑橘、茶饮、香辛料 | 每类每天覆盖一次 |
| 每周 6 类 | 高脂深海鱼、豆类与豆制品、十字花科、红橙色蔬果、菌菇、黑巧可可 | 分别 3 / 5 / 4 / 5 / 3 / 2 次 |
| 其他蛋白 4 类 | 蛋、白肉鱼海鲜、禽肉、红肉 | 记录餐次 |
| 中性食物 1 类 | 其他蔬果、奶、海藻、薯类等 | 展示，不增加覆盖数 |

同餐同类最多计一次，同一种食材可以覆盖多类。脚本无法识别的食材会列出待核对。没有代码工具时按相同规则手算，并说明限制。

**这些频率是本项目的规划约定，不是医学阈值，也不是炎症评分。** 中性食物仍有营养价值，没吃齐不意味着饮食失败。完整食材与依据见[食材表](kitchen/references/food-table.md)。

## 库存和记录保存在哪

- **本地工具：** 保存在你选定项目的 `.kitchen-state/`，新聊天继续使用同一项目。
- **有持久存储的云端工具：** 由助手确认实际可用的保存位置，写入成功后才确认保存。
- **只有对话：** 在当前聊天维护记录；结束时导出库存、菜谱和日志快照，下次带入。

不同 AI 工具不会自动同步私人记录。下载包没有任何人的库存或饮食历史；你的私人状态不应提交到公开 GitHub。[存储规则](kitchen/references/state-files.md)

## 开发、示例与贡献

核心助手不需要 API key；本地辅助脚本需要 Python 3.10+，只使用标准库。AI 工具自身的订阅、权限和能力由各平台决定。

[运行示例与项目结构](docs/development.md) · [贡献指南](CONTRIBUTING.md) · [更新记录](CHANGELOG.md) · [MIT License](LICENSE)

抗炎厨房用于日常饮食搭配，不诊断疾病、不解读化验，也不给药物或补剂剂量。
