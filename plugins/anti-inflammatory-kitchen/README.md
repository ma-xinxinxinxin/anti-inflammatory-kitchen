# 抗炎厨房 · Anti-Inflammatory Kitchen

给想遵循抗炎饮食、吃得健康和干净的人。以地中海式饮食计划和最新厨房库存为基础，帮助你整理食材、决定吃什么、按步骤做饭、只买缺少的食材。

An anti-inflammatory meal-planning assistant built around your latest kitchen inventory: organize stock, decide what to eat, cook it, and buy only what is missing.

## Start / 开始

安装后，单独创建一个「抗炎厨房」Project；支持时启用项目记忆。可先设置忌口、营养目标和食物频次，也可跳过，然后用文字、语音或照片录入真实库存。以后买回或用完食材时更新，所有记录继续放在同一项目。

After installation, create a dedicated Kitchen Project and enable project memory where supported. Optionally set dietary restrictions, nutrition goals, and food frequencies, then add your real inventory by text, voice, or photo. Update purchases and used-up ingredients in that same project.

Then ask / 然后问：`今天晚饭吃什么？` / `What should I eat for dinner?`，或 `给我 3 个早餐选项` / `Give me 3 breakfast options`。

## Install / 安装

This folder contains portable Agent Plugins, Codex, Claude Code, Cursor, and Gemini CLI manifests, plus the complete `skills/kitchen/` workflow. Install using the host's plugin/extension controls; see the [full installation guide](https://github.com/ma-xinxinxinxin/anti-inflammatory-kitchen/blob/main/docs/installation.en.md).

本文件夹包含各平台格式与完整厨房规则。安装步骤见[中文安装说明](https://github.com/ma-xinxinxinxin/anti-inflammatory-kitchen/blob/main/docs/installation.md)。Claude 网页/手机的 Skills 上传入口使用仓库另一个 `kitchen.zip`；本插件 ZIP 用于插件宿主或发布流程。

This is a skills-only plugin. It has no bundled MCP server, external account connection, background inventory monitoring, or automatic cross-platform synchronization. The host supplies input recognition, tools, and any persistent storage. No new API key is required by this package.

这是纯 skill 插件，不含外部服务、后台库存监控或自动跨平台同步。库存依据用户确认的信息更新；图片、语音、文件和持久存储由宿主提供。安装与公开目录上架是不同步骤；ChatGPT 手机原生调用仍需账号可用的分发与实际验收。

Dietary coverage is a planning aid, not an inflammation measurement or medical treatment. 19 类覆盖度是规划工具，不是炎症检测或治疗方案。
