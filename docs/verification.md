# v5.3 验证记录 / Verification record

2026-10-04。所有库存测试使用虚构数据。All inventory fixtures are fictional.

| 检查 / Check | 结果 / Result |
|---|---|
| Python 回归检查 / Python regression suite | 41 项本地通过；覆盖计数、路径、完整复制、备份、下载一致性、marketplace 路径、插件独立运行 / 41 local tests passed |
| Skill 和 Codex 插件结构 / Skill and Codex manifest | 系统验证器通过 / validators passed |
| Claude Code 插件与市场 / Plugin and marketplace | 官方 CLI 严格验证通过；隔离配置安装成功，5.3.0 已启用；发现 kitchen skill / strict validation and isolated install passed, one skill discovered |
| Codex 插件实际安装 / Actual plugin install | 本机注册仓库市场并安装 5.3.0 成功 / local repository marketplace registration and installation passed |
| Cursor | Agent Plugins 和 Cursor manifest 已提供；未做客户端安装或公开上架 / package provided, client installation and listing untested |
| Gemini CLI | 扩展 manifest 已提供；未做客户端实际安装 / manifest provided, client installation untested |
| Claude 手机 / Claude mobile | 本次未做 v5.3 手机验收 / v5.3 mobile acceptance not run |
| ChatGPT 手机及公开目录 / ChatGPT mobile and public listing | 尚未提交、上架或手机实测 / not submitted, listed, or device-tested |
| 语音、照片、小票的模型行为 / Voice, photo, and receipt behavior | 规则已更新；无全平台实测结论 / instructions updated, no all-platform behavior claim |

## 安装后应逐项验证 / Manual acceptance

1. 文字库存：菠菜、豆腐、糙米；先接收，明确汇总后显示 19 类。
2. 食材照片或小票：识别食材，模糊项先核对；未购买的购物车不入库。
3. 清楚语音：正确增删；听不清时询问，不编造。
4. 「今晚吃什么？」：直接一套现有食材搭配，不先强迫选多个候选；过敏、忌口优先。
5. 「怎么做？」：步骤、时间、火候；不凭空假设库存或调料。
6. 「只是计划，还没吃」：不写实际饮食日志、不扣库存。
7. 「吃完了，菠菜用完了」：记录这餐并移除菠菜；不假设豆腐、糙米或油都用完。
8. 「买什么？」：按未来餐食与现有库存列真正缺少的食材。
9. 新聊天与手机重开：根据实际存储恢复；无持久能力时要求带入状态，不能装作已永久保存。

English: verify typed inventory, photo/receipt clarification, voice recognition, one direct meal recommendation, usable cooking steps, no intake logged for plans, explicit stock depletion, plan-based shopping, and honest persistence across new chats/devices.

这些是待在各产品逐项执行的行为场景，不是“模型已经全部通过”的声明。These scenarios are a manual checklist, not a claim that every model or device passed them.
