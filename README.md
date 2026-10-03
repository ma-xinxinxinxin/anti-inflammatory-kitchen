# 抗炎厨房 · Anti-Inflammatory Kitchen

一个给 Claude 用的 skill：把抗炎饮食（地中海底盘）变成每天能执行的厨房助手——管冰箱、出菜谱、算缺口、做周复盘。

> **English summary** — A Claude Agent Skill (Chinese-language) that turns an anti-inflammatory, Mediterranean-style diet into a daily kitchen routine: fridge inventory from chat / grocery screenshots / food photos, recipe suggestions driven by what's in the fridge and what's missing this week, and a deterministic weekly review. No calorie counting, no weighing, no streaks. Install the `kitchen/` folder as a skill in Claude (claude.ai, Claude Desktop / Cowork, or Claude Code).

## 它做什么

八件事，一次只做你要的那一件：

1. **更新冰箱** —— 对话、超市订单截图、食物照片都行，归到固定的 19 个类别
2. **记住常用菜谱** —— 「这个存下来，以后叫它周三鱼汤」
3. **生成每顿菜谱** —— 先给 2–3 个候选，按「你想吃什么 > 冰箱里有什么 > 今天/本周缺什么」排
4. **展开完整做法** —— 带火候和判断节点，不写「炒熟即可」
5. **今天的三餐与营养** —— 渲染成一张手机卡片
6. **补货建议** —— 只列缺口对应、冰箱里又没有的
7. **清库菜谱** —— 围绕最快坏的两三样出菜
8. **一周复盘** —— 先用脚本算数，再给三个能直接执行的下周动作

## 抗炎清单（v5 · 19 类）

| 分组 | 类别 | 目标 |
|---|---|---|
| 每日必有（8） | 优质脂肪、坚果种子、发酵食品、深色绿叶菜、全谷主食、浆果柑橘、茶饮、香辛料 | 每天各 ≥1 份 |
| 每周达标（6） | 高脂深海鱼 3、豆类与豆制品 5（≥3 次整豆）、十字花科 4、红橙色蔬果 5、菌菇 3、黑巧可可 2 | 次/周 |
| 其他优质蛋白（4） | 蛋 ≤5、白肉鱼海鲜、禽肉、红肉 ≤2 | 只计次 |
| 中性食物（1） | 海藻、普通蔬果、奶、奶酪、干果、其他淀粉、猪肉、蜂蜜 | 不计分 |

计数规则：一道菜可以同时命中多个类别（小白菜 = 深色绿叶菜 + 十字花科），但同一餐里同一类别只计一次。

完整口径见 [`kitchen/references/food-table.md`](kitchen/references/food-table.md)。

## 设计原则

- 不称重、不算卡路里、不设体重目标、不打卡、不发徽章
- 达标判定是确定性计算（`scripts/kitchen.py`），不靠模型印象
- 看一周，不看一顿；记录不全是常态，按记了的算
- 语气直接，不说教

## 安装

**Claude.ai / Claude 桌面版（含 Cowork）**：把 `kitchen/` 文件夹打成 zip，在设置里的 Skills 页面上传。

**Claude Code**：

```bash
git clone https://github.com/ma-xinxinxinxin/anti-inflammatory-kitchen.git
cp -r anti-inflammatory-kitchen/kitchen ~/.claude/skills/
```

建议放在一个固定的 Claude Project 里用——冰箱、菜谱、饮食记录三份状态存在 Claude 的 memory 里，跨对话保留。

## 换成你的城市

默认本地化是上海（盒马 / Ole / 本地菜场）。改两处即可：

- `kitchen/SKILL.md` 的「本地化」一节：换成你常用的采买渠道
- `kitchen/references/food-table.md` 末尾的「本地采买备注」：换成本地版本

## 脚本

`kitchen/scripts/kitchen.py` 只依赖 Python 3 标准库：

```bash
python3 kitchen/scripts/kitchen.py fridge --items "有机菠菜 250g, 云南蓝莓 125g, 手抓饼"
python3 kitchen/scripts/kitchen.py score  --log kitchen-log.md
```

## 边界

这是饮食搭配层面的工具，不诊断疾病、不解读化验、不给用药或补剂剂量。表里的「每周 3 次」「每天 1 份」都是操作性约定，不是临床阈值。有健康问题请咨询医生或注册营养师。

## License

[MIT](LICENSE)
