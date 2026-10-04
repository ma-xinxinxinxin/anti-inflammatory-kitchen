# 抗炎厨房 · Anti-Inflammatory Kitchen

**从冰箱里有什么，到今天吃什么。**

一个以地中海饮食为基础的中文 Agent Skill：整理食材、一起定菜谱、记录吃过什么，再看每天与每周的搭配。无需称重、计算卡路里或连续打卡。

支持 Claude 和具备本地 skill 能力的 ChatGPT 桌面 / Codex 环境。脚本仅依赖 **Python 3.10+ 标准库**，没有 API key、数据库或付费服务要求。

[快速开始](#快速开始) · [19 类食物](#一张清单两种节奏) · [运行示例](#运行示例) · [English](docs/README.en.md) · [更新记录](CHANGELOG.md)

## 你可以直接这样说

| 想做什么 | 发给助手 |
|---|---|
| 更新冰箱 | 「买了菠菜、豆腐和三文鱼，豆浆用完了。就这些，更新库存。」 |
| 决定晚餐 | 「想吃鱼，结合冰箱给两个 25 分钟内能做的方案。」 |
| 展开做法 | 「选第二个，展开做法，告诉我怎么判断火候。」 |
| 保存菜谱 | 「存下来，以后叫它周三鱼汤。」 |
| 看缺口 | 「今天和本周还可以补哪些类别？只看已经吃过的。」 |
| 安排今天 | 「用现有食材规划今天剩下两餐，做成一张卡片。」 |
| 补货或清库 | 「只买缺的」或「菠菜快坏了，先围绕它做一道菜。」 |
| 周复盘 | 「复盘截至 9 月 7 日的七天，给三个下周能做的动作。」 |

先给候选，再展开做法；你在报库存时不会抢着给菜谱。库存始终显示 19 行，空的类别也看得见。

## 快速开始

### ChatGPT 桌面 / Codex 本地 skill

在支持 Skill Installer 的本地环境中发送：

```text
用 Skill Installer 安装 https://github.com/ma-xinxinxinxin/anti-inflammatory-kitchen 的 kitchen 目录。
```

安装后可用 `$kitchen` 或在 skill 选择器中选择「抗炎厨房」。新安装的 skill 会在下一轮可用；未出现时重新打开会话。适用范围与分发方式见 [OpenAI 官方 skill 文档](https://learn.chatgpt.com/docs/build-skills)。**本地安装不等于向 ChatGPT 网页或移动端账号同步安装**；跨这些平台的分发需要相应插件或工作区能力。

### Claude

- **Claude Code**：克隆仓库，确保 `~/.claude/skills/` 存在，将整个 `kitchen/` 文件夹放入其中。已有同名 skill 时先备份再替换。
- **支持上传 skill 的 Claude 环境**：运行下方打包命令，上传 `dist/kitchen.zip`。具体入口以当前产品为准。

```bash
git clone https://github.com/ma-xinxinxinxin/anti-inflammatory-kitchen.git
cd anti-inflammatory-kitchen
python3 scripts/package_skill.py
```

### 第一次使用

在固定项目里打开对话，先说：「用抗炎厨房，先记一下冰箱……」。本地环境把三份状态放在该项目的 `.kitchen-state/`。换聊天时继续使用同一个项目。

有持久 memory 工具的平台可使用其实际项目存储；没有持久存储时，助手会提供状态文件供下次上传。**安装 skill 不会导入任何人的冰箱、菜谱或饮食记录，也不会自动同步 Claude 与 ChatGPT 的私人数据。**

## 一张清单，两种节奏

| 分组 | 类别 | 默认记录目标 |
|---|---|---|
| 每日必有 · 8 | 优质脂肪、坚果种子、发酵食品、深色绿叶菜、全谷主食、浆果柑橘、茶饮、香辛料 | 每类 ≥1 计数单位/日 |
| 每周达标 · 6 | 高脂深海鱼、豆类与豆制品、十字花科、红橙色蔬果、菌菇、黑巧可可 | 分别 3 / 5 / 4 / 5 / 3 / 2 次 |
| 其他优质蛋白 · 4 | 蛋、白肉鱼海鲜、禽肉、红肉 | 只记餐次 |
| 中性食物 · 1 | 其他蔬果、奶、海藻、薯类等 | 展示，不增加覆盖数 |

「每日必有」是清单名称，**不是每个人每天都必须吃齐的医学要求**。19 类与频次是本项目的规划约定，不是经临床验证的抗炎评分。中性食物也有营养价值。

同餐同类最多计一次；同一种食材可覆盖多类。小白菜同时覆盖深色绿叶菜和十字花科。半份权重、食材别名、未知食材处理与研究依据见 [食材表](kitchen/references/food-table.md)。

## 运行示例

在仓库根目录运行：

```bash
# 19 行库存表：自动去掉常见规格；无法归类的单列待确认
python3 kitchen/scripts/kitchen.py fridge --items "有机菠菜 250g, 西兰花, 松茸, 手抓饼"

# 演示日志 → 七天统计 → 手机宽度的连续长页
python3 kitchen/scripts/kitchen.py score --log examples/meal-log.md --end 2026-09-07 -o /tmp/kitchen-week.json
python3 kitchen/scripts/kitchen.py week --json /tmp/kitchen-week.json -o /tmp/kitchen-week.html

# 计划餐单与预计覆盖；不会写入实际摄入日志
python3 kitchen/scripts/kitchen.py day --json examples/day.json -o /tmp/kitchen-today.html

# 参数与输入结构
python3 kitchen/scripts/kitchen.py schema
```

示例完全为演示编写。生成的 HTML 可离线打开，不加载远程字体。脚本只读取传入文件、输出结果；不会自己改库存或调用模型。自然语言理解、照片识别和菜谱建议由宿主助手完成。

记录不全时显示实际记录天数。未知食材会出现在统计结果的 `unrecognizedItems` 中，不能把未识别当作没吃。

## 自定义与贡献

默认中文，上海采买渠道只是示例，直接告诉助手你的城市和常用商店即可。偏好、忌口和状态属于个人工作区；分享 skill 时不用携带它们。

运行回归测试：

```bash
python3 -m unittest discover -s tests -v
```

欢迎改进食材别名、示例与兼容性。修改类别、频次或健康表述前，请阅读 [贡献指南](CONTRIBUTING.md)，同步文档、脚本和测试。

## 边界与隐私

这是饮食搭配助手，不诊断疾病、不解读化验、不给药物或补剂剂量。饮食研究的结果不等于本工具能降低某个人的炎症指标。

仓库忽略私有状态目录和三份状态文件。公开 issue、截图或 PR 前仍请检查是否含私人信息；宿主 AI 对上传内容的处理由所用平台决定。

[MIT License](LICENSE)
