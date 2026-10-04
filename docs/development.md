# 开发与示例

**简体中文** · [English](development.en.md) · [返回首页](../README.md)

普通用户从[安装说明](installation.md)开始即可。以下命令供想检查脚本、改规则或维护发行文件的人使用，需要 Python 3.10+，没有第三方依赖。Windows 可用 `py -3` 替代 `python3`；在终端显示中文时建议启用 Python UTF-8 模式。

## 运行示例

在仓库根目录运行；先打包创建 `dist/`，示例输出也放在这个被 Git 忽略的目录中：

```bash
python3 scripts/package_skill.py
python3 kitchen/scripts/kitchen.py fridge --items "有机菠菜 250g, 西兰花, 松茸, 手抓饼"
python3 kitchen/scripts/kitchen.py score --log examples/meal-log.md --end 2026-09-07 -o dist/week.json
python3 kitchen/scripts/kitchen.py week --json dist/week.json -o dist/week.html
python3 kitchen/scripts/kitchen.py day --json examples/day.json -o dist/today.html
python3 kitchen/scripts/kitchen.py schema
```

示例是虚构数据。HTML 可离线打开，不加载远程字体。脚本只读取传入文件并输出结果，不会自己修改库存或调用模型。自然语言理解、照片识别和菜谱建议由宿主助手完成。脚本食材词表以中文为主；其他语言的食材需由助手先映射到表中的规范名称，不能假定脚本会自动翻译。

记录不全时显示实际记录天数；未知食材列在 `unrecognizedItems`，不把未识别当作没吃。

个人设置保存在日志同目录的 `kitchen-profile.json`，`score` 会自动读取，也可用 `--profile` 指定其他文件；格式见[状态规则](../kitchen/references/state-files.md)。有设置时用 `personalPlan` 中的频次与记录做规划和周卡；旧输出字段保留默认口径供兼容。默认日卡的八类圆环不适用于个人频次，改用个人目标表。

## 项目结构

| 路径 | 用途 |
|---|---|
| `kitchen/SKILL.md` | 各平台共用的工作流与版本 |
| `kitchen/references/` | 食材、状态、菜谱和视觉规则 |
| `kitchen/scripts/kitchen.py` | 库存表、计数、日卡与周卡 |
| `scripts/install_skill.py` | 按工具选择路径；升级前备份 |
| `scripts/package_skill.py` | 从同一套源文件生成发行文件 |
| `downloads/` | 用户直接下载的 skill ZIP、插件 ZIP 与单文件聊天指南 |
| `plugins/anti-inflammatory-kitchen/` | 共用插件包；`.codex-plugin/plugin.json` 为元数据源，其他格式及 skill 副本由构建生成 |
| `.agents/plugins/`、`.claude-plugin/`、`.cursor-plugin/` | 各平台仓库插件目录 |
| `examples/`、`tests/` | 虚构演示与回归检查 |
| `.kitchen-state/` | 用户私人状态，忽略提交，不参与打包 |

## 构建和验证

```bash
python3 -m unittest discover -s tests -v
python3 scripts/package_skill.py --publish
python3 scripts/package_skill.py --check
```

默认打包输出到 `dist/`。`--publish` 只重新生成仓库内的 `downloads/`，不会联网发布；源文件改动后应同时提交新的下载文件。`--check` 检查下载文件与源文件逐字节一致，避免用户下载到过期规则。ZIP 使用明确的文件白名单，不携带状态、缓存、演示或仓库管理文件。聊天指南嵌入参考内容，但不包含 Python 脚本。

CI 检查 Linux（Python 3.10、3.13）和 Windows（Python 3.13）。这些检查验证文件与脚本，不替代真实 AI 产品、手机和账号的安装验收；手动场景见[安装验收](installation.md#verify)。

改动约定和手动行为检查见[贡献指南](../CONTRIBUTING.md)。不要把个人库存、聊天导出或健康资料用于公开测试。

插件 skill 源文件仍只有 `kitchen/` 一份。改规则后运行 `--publish` 同步插件副本；修改插件名称需同时更新各平台 marketplace。`--check` 同时检查下载包与插件目录。实际安装与手机验收范围见[验证记录](verification.md)。
