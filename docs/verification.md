# 兼容性与验证 · Compatibility & verification

本页区分可自动验证的安装包行为与需要在实际 AI 产品中检查的体验。提供兼容格式不代表已经上架该平台的公共目录。

This page distinguishes reproducible package checks from behavior that needs testing in an AI product. A compatible package does not imply a public marketplace listing.

## 支持范围 / Compatibility

| 使用方式 / Route | 已验证范围 / Verified scope | 仍需确认 / Still to verify |
|---|---|---|
| 本地 skill 安装器 / Local skill installer | Codex、Claude Code、Cursor、Gemini CLI 目录选择、完整复制、升级备份及状态保留 / paths, complete copying, backups and state preservation | 各客户端模型行为 / host-model behavior |
| 插件包 / Plugin package | 各 manifest 与技能内容一致，解压后可独立运行脚本 / consistent manifests and skill content; standalone helper execution | 每个平台的账号安装与目录发布 / account installation and marketplace publication |
| Claude Code / Codex 插件 | v5.3 曾完成本地安装；后续包由自动检查验证 / local installation verified for v5.3; later packages checked automatically | 新版客户端实际安装 / current client installation |
| 单文件对话指南 / Conversation guide | 参考材料完整内嵌，无需外部脚本 / self-contained references, no script required | 附件读取、上下文长度与记忆能力 / attachment, context and memory capabilities |
| Claude / ChatGPT 手机 / Mobile | 提供安装或导入说明 / instructions provided | 未完成手机实机验收；ChatGPT 公共目录尚未上架 / device acceptance not completed; ChatGPT listing not published |

## 可复现检查 / Reproducible checks

```bash
python3 -m unittest discover -s tests -v
python3 scripts/package_skill.py --check
```

47 项自动测试覆盖食材计数、缺失记录、个人频次、其他蛋白合计去重、安装与备份、私有状态隔离、离线渲染和分发一致性。持续集成在 Linux（Python 3.10 / 3.13）和 Windows（Python 3.13）运行；最新结果以 [GitHub Actions](https://github.com/ma-xinxinxinxin/anti-inflammatory-kitchen/actions/workflows/checks.yml) 为准。

The 47-test suite covers food counts, missing records, personal frequencies, combined protein counts, installation and backups, private-state isolation, offline rendering, and distribution consistency. CI runs on Linux (Python 3.10 / 3.13) and Windows (Python 3.13); see GitHub Actions for current results.

## 体验检查 / Try it in your AI tool

在独立测试项目中使用虚构食材，避免混入日常库存。
Use fictional ingredients in a separate test project.

- 设置忌口和频次，重开项目后核对 / Set restrictions and frequencies, then reopen the project.
- 查看库存、添加购买的食材、移除明确用完的食材 / Check stock, add purchases, remove finished items.
- 上传照片或小票，核对模糊项 / Upload a photo or receipt and check uncertain items.
- 要一套晚餐、三个早餐选项及具体做法 / Request dinner, three breakfast options, and cooking steps.
- 保存常用菜谱，按名字找回 / Save a favorite recipe and retrieve it by name.
- 确认计划不计作已吃，采购清单不计作已有库存 / Keep planned meals and shopping separate from actual intake and stock.
- 核对个人目标、已有存货与购物建议是否一致 / Check that suggestions follow personal goals and current stock.

这些是使用者可执行的检查场景，并非所有模型或手机都已通过的保证。
These are checks you can perform, not a guarantee that every model or mobile client has passed.
