#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""抗炎厨房 · 确定性打分与视觉渲染

用法：
  python3 kitchen.py score  --log kitchen-log.md [--end 2026-09-07]     -> JSON 到 stdout
  python3 kitchen.py day    --json day.json      -o today.html
  python3 kitchen.py week   --json week.json     -o review.html

day.json / week.json 的字段见文件末尾 SCHEMA 说明。
score 的输出可直接当 week.json 用（再补上 review 三段文字）。
"""
import sys, json, re, argparse, datetime as dt
import math
from html import escape
from pathlib import Path

# ---------- 食材表 ----------
DAILY = [
    ("goodFat", "优质脂肪", "特级初榨橄榄油 橄榄油 牛油果 橄榄"),
    ("nutsSeeds", "坚果种子", "核桃 杏仁 开心果 南瓜籽 亚麻籽粉 奇亚籽 巴西坚果 芝麻酱 杏仁酱 芝麻 坚果"),
    ("fermented", "发酵食品", "希腊酸奶 无糖酸奶 开菲尔 纳豆 味噌 泡菜 康普茶"),
    ("leafy", "深色绿叶菜", "菠菜 羽衣甘蓝 西洋菜 茼蒿 豌豆尖 苋菜 油麦菜 鸡毛菜 空心菜 生菜 小白菜 芥蓝 油菜"),
    ("wholeGrain", "全谷主食", "燕麦 糙米 藜麦 荞麦面 全麦面包 全麦皮塔 小米"),
    ("berryCitrus", "浆果柑橘", "蓝莓 树莓 草莓 黑莓 蔓越莓 橙 柚子 猕猴桃 石榴 樱桃"),
    ("tea", "茶饮", "绿茶 乌龙茶 白茶 红茶 抹茶 洛神花茶"),
    ("spices", "香辛料", "大蒜 洋葱 生姜 姜黄粉 黑胡椒 迷迭香 牛至 百里香 丁香 肉桂 孜然"),
]
HALF = {"巴西莓粉": "berryCitrus", "花生酱": "nutsSeeds"}
WEEK_HALF = {"枸杞": "redOrange"}
WEEKLY = [
    ("fattyFish", "高脂深海鱼", 3, "三文鱼 鲭鱼 青花鱼 沙丁鱼罐头 凤尾鱼 秋刀鱼"),
    ("legumes", "豆类与豆制品", 5, "鹰嘴豆 扁豆 毛豆 黑豆 红腰豆 豆腐 豆干 腐竹 无糖豆浆 天贝"),
    ("cruciferous", "十字花科", 4, "西蓝花 花椰菜 卷心菜 紫甘蓝 芝麻菜 小白菜 白萝卜 抱子甘蓝 芥蓝 油菜 鸡毛菜"),
    ("redOrange", "红橙色蔬果", 5, "熟番茄 番茄 胡萝卜 南瓜 红椒 黄椒 红薯 紫薯"),
    ("mushrooms", "菌菇", 3, "香菇 舞茸 灰树花 平菇 木耳 杏鲍菇 松茸 蘑菇 金针菇"),
    ("darkChocolate", "黑巧可可", 2, "85%黑巧克力 黑巧克力 天然可可粉 可可粉"),
]
OTHERP = [
    ("eggs", "蛋", "鸡蛋 水煮蛋 煎蛋"),
    ("whiteFishSeafood", "白肉鱼海鲜", "鳕鱼 鲈鱼 鳜鱼 虾 虾仁 扇贝 蛤蜊 乌贼 鱿鱼 金枪鱼"),
    ("poultry", "禽肉", "鸡腿 鸡胸 鸡肉 鸭胸 鸭肉"),
    ("redMeat", "红肉", "牛腱 牛里脊 牛腩 牛肉 牛排 羊腿 羊肉"),
]
NEUTRAL = ("香蕉 苹果 梨 葡萄 桃 西瓜 黄瓜 茄子 莴笋 豆角 冬瓜 玉米 丝瓜 牛奶 燕麦奶 杏仁奶 "
           "海带 紫菜 裙带菜 奶酪 帕玛森 红枣 葡萄干 土豆 山药 芋头 莲藕 猪里脊 猪肉 蜂蜜 榴莲 椰子水 火龙果 芒果 柠檬").split()
LIMITS = [("processedMeat", "加工肉"), ("sugaryDrink", "含糖饮料"), ("ultraProcessed", "超加工"),
          ("transFat", "复炸油"), ("refinedGrainMeal", "白米白面"), ("deepFried", "油炸"),
          ("tooSalty", "偏咸"), ("alcohol", "酒精")]

# 一个食材可命中多个类别（小白菜 = 绿叶 + 十字花科）；同餐同类只计一次
VOCAB = {}
def _add(w, k, wt=1.0):
    VOCAB.setdefault(w, []).append((k, wt))
for k, n, s in DAILY:
    for w in dict.fromkeys(s.split()): _add(w, k)
for w, k in HALF.items(): _add(w, k, 0.5)
for k, n, t, s in WEEKLY:
    for w in dict.fromkeys(s.split()): _add(w, k)
for w, k in WEEK_HALF.items(): _add(w, k, 0.5)
for k, n, s in OTHERP:
    for w in dict.fromkeys(s.split()): _add(w, k)
for w in NEUTRAL: _add(w, "neutral")
# Aliases are exact: plant milk must not become nuts or whole grains.
ALIASES = {"西兰花": "西蓝花", "小番茄": "番茄", "圣女果": "番茄",
           "蒜": "大蒜", "蒜头": "大蒜", "姜": "生姜", "葱": "洋葱",
           "小葱": "洋葱", "红洋葱": "洋葱", "低盐泡菜": "泡菜",
           "沙丁鱼": "沙丁鱼罐头", "黑巧": "黑巧克力"}
for alias, canonical in ALIASES.items():
    VOCAB[alias] = list(VOCAB[canonical])
DAILY_KEYS = [k for k, _, _ in DAILY]
NAME = {k: n for k, n, _ in DAILY}
NAME.update({k: n for k, n, _, _ in WEEKLY})
NAME.update({k: n for k, n, _ in OTHERP})
LIMNAME = dict(LIMITS)


UPF = "手抓饼 苏打饼干 蟹肉棒 火腿 培根 香肠 午餐肉 speck 薯片 泡面 速冻饺子 沙拉酱 番茄酱".split()
NOISE = re.compile(r"(有机|日日鲜|冰鲜|冷冻|新鲜|进口|云南|挪威|智利|特级初榨(?=橄榄油))")
QTY = re.compile(r"[\d.]+\s*(g|kg|克|千克|ml|毫升|升|盒|袋|把|根|颗|个|块|段|片|罐|瓶|只|条|包|份|x|X|\*)")
DATE = re.compile(r"[·・]?\s*(到|至|到期|保质期?)?\s*[（(]?(?:\d{4}[-/.])?\d{1,2}[-/.]\d{1,2}[）)]?|\d+\s*天")

def clean(raw):
    """一条原始条目 -> 干净食材名"""
    t = re.sub(r"^\s*[-*•]?\s*\[\w+\]\s*", "", raw)
    t = re.sub(r"[·・]\s*(常备|冷冻常备).*$", "", t)
    t = t.strip().strip("·-—•*").strip()
    t = DATE.sub("", t); t = QTY.sub("", t)
    t = re.sub(r"[（(].*?[）)]", "", t)
    t = NOISE.sub("", t)
    t = re.sub(r"[·・]?\s*(到|至|到期|保质期?)\s*$", "", t)
    return t.strip(" 、,，:：·-")

def classify(name):
    """干净名 -> (类别key, 是否加工品)。先精确后包含。"""
    if not name: return None, False
    if name in VOCAB: return VOCAB[name][0][0], False
    for u in UPF:
        if u in name: return None, True
    hits = [(w, v[0][0]) for w, v in VOCAB.items() if w in name and len(w) >= 2]
    if hits:
        hits.sort(key=lambda x: -len(x[0]))
        return hits[0][1], False
    return None, False

FRIDGE_ROWS = [("每日必有", DAILY_KEYS),
               ("每周达标", [k for k, _, _, _ in WEEKLY]),
               ("其他 · 中性", [k for k, _, _ in OTHERP] + ["neutral"])]
NAME["neutral"] = "中性食物"

def render_fridge(items):
    """items: 原始字符串列表 -> 19 行 markdown"""
    buckets, upf, unknown = {}, [], []
    for raw in items:
        n = clean(raw)
        if not n: continue
        k, is_upf = classify(n)
        if is_upf:
            upf.append(n)
        elif k is None:
            unknown.append(n)
        else:
            keys = [key for key, _ in VOCAB[n]] if n in VOCAB else [k]
            for key in keys:
                buckets.setdefault(key, []).append(n)
    out, empty = [], []
    for title, keys in FRIDGE_ROWS:
        out.append(f"**{title}**\n\n| 类别 | 有什么 |\n|---|---|")
        for k in keys:
            v = buckets.get(k) or []
            if not v: empty.append(NAME[k])
            out.append(f"| {NAME[k]} | {'、'.join(dict.fromkeys(v)) if v else '空'} |")
        out.append("")
    if empty: out.append("> 空着：" + " · ".join(empty))
    if upf: out.append("> 加工品（不计入类别）：" + "、".join(dict.fromkeys(upf)))
    if unknown: out.append("> 待确认（未归类）：" + "、".join(dict.fromkeys(unknown)))
    return "\n".join(out)


def parse_fridge(text):
    """Read raw lists, saved state or rendered tables without treating metadata as food."""
    text = re.sub(r"\A\s*---\s*\n.*?\n---\s*(?:\n|$)", "", text, count=1, flags=re.S)
    items = []
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith(("#", "**")):
            continue
        if line.startswith("|"):
            cells = [x.strip() for x in line.strip("|").split("|")]
            if len(cells) != 2 or cells[0] not in NAME.values():
                continue
            line = cells[1]
        elif line.startswith(">"):
            if line.startswith("> 空着"):
                continue
            if not line.startswith(("> 加工品", "> 待确认")):
                continue
            line = line.split("：", 1)[-1]
        else:
            line = re.sub(r"^[-*•]\s*(?:\[\w+\]\s*)?", "", line)
            line = re.sub(r"^[^：:]{1,12}[：:]", "", line)
        items.extend(x.strip() for x in re.split(r"[,，、\n]", line)
                     if x.strip() and x.strip() not in ("空", "---"))
    return items

# ---------- 打分 ----------
def parse_log(text):
    """-> {date: [ [items...], ... ]}, {date: {limitKey: n}}"""
    days, lims, cur = {}, {}, None
    for line in text.splitlines():
        line = line.strip()
        m = re.match(r"^##\s*(\d{4}-\d{2}-\d{2})", line)
        if m:
            cur = m.group(1)
            dt.date.fromisoformat(cur)
            continue
        if line.startswith("##"):
            cur = None
            continue
        if not cur or not line.startswith("-"): continue
        body = re.sub(r"^-\s*(\[\w+\]\s*)?", "", line)
        parts = [p.strip() for p in body.split("|")]
        meal_items, lim_here = [], []
        for p in parts[1:] if len(parts) > 1 else []:
            if p.startswith("限制:") or p.startswith("限制："):
                lim_here = [x.strip() for x in re.split(r"[,，]", p.split(":", 1)[-1].split("：")[-1]) if x.strip()]
            elif p.startswith("外食"):
                continue
            else:
                meal_items += [x for x in re.split(r"[\s,，、]+", p) if x]
        if meal_items or lim_here:
            days.setdefault(cur, []).append(meal_items)
            lims.setdefault(cur, {})
        for l in set(lim_here): lims[cur][l] = lims[cur].get(l, 0) + 1
    return days, lims

def week_dates(end):
    e = dt.date.fromisoformat(end)
    return [(e - dt.timedelta(days=i)).isoformat() for i in range(6, -1, -1)]

def profile_frequencies(profile):
    """Resolve explicit personal targets without mutating defaults or user settings."""
    frequencies = {k: {"period": "day", "target": 1} for k in DAILY_KEYS}
    frequencies.update({k: {"period": "week", "target": t} for k, _, t, _ in WEEKLY})
    frequencies.update({k: None for k, _, _ in OTHERP})
    frequencies["otherProtein"] = None
    if not isinstance(profile, dict):
        raise ValueError("profile must be a JSON object")
    for field in ("restrictions", "preferences", "goals"):
        value = profile.get(field, [])
        if not isinstance(value, list) or any(not isinstance(x, str) for x in value):
            raise ValueError(f"profile {field} must be a list of text values")
    overrides = profile.get("frequencies", {})
    if not isinstance(overrides, dict):
        raise ValueError("profile frequencies must be an object")
    for key, rule in overrides.items():
        if key not in frequencies:
            raise ValueError(f"Unknown frequency category: {key}; neutral foods have no target")
        if rule is not None:
            if not isinstance(rule, dict) or set(rule) != {"period", "target"}:
                raise ValueError(f"{key}: use period and target, or null for no target")
            target = rule["target"]
            if (rule["period"] not in ("day", "week") or isinstance(target, bool)
                    or not isinstance(target, (int, float)) or not math.isfinite(target) or target <= 0):
                raise ValueError(f"{key}: period must be day/week and target positive; use null for no target")
        frequencies[key] = rule
    return frequencies


def personal_plan(frequencies, counts, dates, recorded):
    """Keep daily thresholds per day; never let extra meals erase an unrecorded day."""
    result = []
    for key, rule in frequencies.items():
        values = [round(counts[d].get(key, 0), 1) if d in recorded else None for d in dates]
        row = {"key": key, "name": "其他蛋白合计" if key == "otherProtein" else NAME[key],
               "frequency": rule, "dailyCounts": values,
               "recordedCount": round(sum(v for v in values if v is not None), 1)}
        if rule and rule["period"] == "day":
            row["metDays"] = sum(v is not None and v >= rule["target"] for v in values)
        result.append(row)
    return result


def score(text, end=None, profile=None):
    frequencies = profile_frequencies(profile) if profile is not None else None
    days, lims = parse_log(text)
    end = end or (max(days) if days else dt.date.today().isoformat())
    dates = week_dates(end)
    matrix = {k: [] for k in DAILY_KEYS}
    met_days = {k: 0 for k in DAILY_KEYS}
    weekly = {k: 0.0 for k, _, _, _ in WEEKLY}
    other = {k: 0 for k, _, _ in OTHERP}
    limits = {}
    logged = 0
    unknown, neutral = set(), set()
    counts = {d: {} for d in dates}
    for d in dates:
        meals = days.get(d)
        if meals is None:
            for k in DAILY_KEYS: matrix[k].append("none")
            continue
        logged += 1
        acc = {k: 0.0 for k in DAILY_KEYS}
        for items in meals:
            # Take the largest weight per category, independent of ingredient order.
            meal_weights = {}
            for it in dict.fromkeys(items):
                if it not in VOCAB:
                    unknown.add(it)
                for k, wt in VOCAB.get(it, []):
                    meal_weights[k] = max(meal_weights.get(k, 0), wt)
                    if k == "neutral": neutral.add(it)
            for k, wt in meal_weights.items():
                counts[d][k] = counts[d].get(k, 0) + wt
                if k in acc: acc[k] += wt
                elif k in weekly: weekly[k] += wt
                elif k in other: other[k] += 1
            if any(k in meal_weights for k in other):
                counts[d]["otherProtein"] = counts[d].get("otherProtein", 0) + 1
        for k in DAILY_KEYS:
            ok = acc[k] >= 1.0
            matrix[k].append("met" if ok else "recorded")
            if ok: met_days[k] += 1
        for lk, n in lims.get(d, {}).items():
            limits[lk] = limits.get(lk, 0) + n
    result = {
        "weekStart": dates[0], "weekEnd": dates[-1], "daysWithRecord": logged,
        "dailyMatrix": matrix, "dailyMetDays": met_days,
        "weeklyCounts": {k: round(v, 1) for k, v in weekly.items()}, "weeklyTargets": {k: t for k, _, t, _ in WEEKLY},
        "otherProtein": other, "limitsHit": limits,
        "neutralList": sorted(neutral), "unrecognizedItems": sorted(unknown),
    }
    if frequencies is not None:
        result["personalPlan"] = personal_plan(frequencies, counts, dates, days)
    return result

# ---------- 视觉 ----------
HEAD = """<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<style>
 *{box-sizing:border-box;margin:0}
 body{background:#F6F2E8;color:#2A2A24;font-family:"Noto Sans SC",system-ui,sans-serif;
      padding:22px;max-width:430px;margin:0 auto}
 .num{font-family:"Space Grotesk",monospace}
 .col{display:flex;flex-direction:column;gap:13px}
 .card{background:#EFEADB;border-radius:18px;padding:13px 15px}
 .h1{font:700 22px/1.35 "Noto Sans SC"}
 .sub{font:400 11px/1.6 "Noto Sans SC";color:#6B6857}
 .sect{font:500 12.5px "Noto Sans SC";color:#6B6857;margin-bottom:9px}
 .pill{display:inline-flex;align-items:center;border-radius:12px;padding:4px 10px;font:400 11.5px "Noto Sans SC"}
 .p-green{background:#3D5A3F;color:#F6F2E8}
 .p-dash{border:1px dashed rgba(42,42,36,.24);color:#6B6857}
 .p-olive{background:#E6E8CC;color:#55602F}
 .p-clay{background:rgba(181,100,60,.16);color:#8A4A28}
 .row{display:flex;align-items:center;gap:8px}
 .wrapf{display:flex;flex-wrap:wrap;gap:6px}
 .dot{width:15px;height:15px;border-radius:50%;flex:none}
 .d-met{background:#3D5A3F}.d-rec{background:#DCD6C2}
 .d-none{border:1px dashed rgba(42,42,36,.3)}
 .d-open{border:1px solid rgba(42,42,36,.3)}.d-miss{border:1px solid #B5643C}
 .hair{height:1px;background:rgba(42,42,36,.09);margin:2px 0}
 .tip{background:#FAF1E9;border-radius:16px;padding:11px 13px}
 .tip b{font:500 11px "Noto Sans SC";color:#8A4A28;display:block;margin-bottom:3px}
 .tip p{font:400 12.5px/1.7 "Noto Sans SC";color:#8A6A4E}
 .g2{display:grid;grid-template-columns:1fr 1fr;gap:6px}
 .wk{border-radius:12px;padding:7px 10px;display:flex;justify-content:space-between;align-items:center;
     font:400 11.5px "Noto Sans SC";background:#EFEADB}
 .wk.on{background:#3D5A3F;color:#F6F2E8}
 .meal{background:#EFEADB;border-radius:18px;padding:11px;display:flex;gap:11px;align-items:center}
 .ph{width:48px;height:48px;border-radius:14px;flex:none;
     background:repeating-linear-gradient(45deg,#DCD3BE 0 6px,#D3C9B1 6px 12px)}
 .body{font:400 13px/1.85 "Noto Sans SC";color:#3A382C}
 ol{margin:0;padding-left:0;list-style:none}
</style>"""

def ring(pct, label, big=58):
    inner = big - 13
    return (f'<div style="width:{big}px;height:{big}px;flex:none;border-radius:50%;'
            f'background:conic-gradient(#E8D9A8 0 {pct}%,rgba(246,242,232,.2) 0);'
            f'display:flex;align-items:center;justify-content:center">'
            f'<div style="width:{inner}px;height:{inner}px;border-radius:50%;background:#3D5A3F;'
            f'display:flex;align-items:center;justify-content:center;font:700 15px \'Space Grotesk\';'
            f'color:#F6F2E8">{label}</div></div>')

G, CLAY, INK, MUT = "#3D5A3F", "#B5643C", "#2A2A24", "#6B6857"
CARD, CLAYP, OLB, OLT = "#EFEADB", "#FAF1E9", "#E6E8CC", "#55602F"
SLOTS = [("b", "早餐"), ("l", "午餐"), ("d", "晚餐"), ("s", "加餐")]

def _ph(sz=48, r=14):
    return (f'<div style="width:{sz}px;height:{sz}px;flex:none;border-radius:{r}px;'
            f'background:repeating-linear-gradient(45deg,#DCD3BE 0 6px,#D3C9B1 6px 12px)"></div>')

def _daily_grid(daily):
    cells = []
    for c in daily:
        by = c.get("by")
        if by:
            cells.append(f'<div style="background:{G};border-radius:16px;padding:14px 16px;display:flex;'
                         f'justify-content:space-between;align-items:center;gap:8px">'
                         f'<span style="font:500 14px \'Noto Sans SC\';color:#F6F2E8">{c["name"]}</span>'
                         f'<span style="font:400 11.5px \'Noto Sans SC\';color:rgba(246,242,232,.8);text-align:right">{by}</span></div>')
        else:
            cells.append(f'<div style="border:1px dashed rgba(42,42,36,.3);border-radius:16px;padding:14px 16px;'
                         f'display:flex;justify-content:space-between;align-items:center">'
                         f'<span style="font:500 14px \'Noto Sans SC\';color:{INK}">{c["name"]}</span>'
                         f'<span style="font:500 12px \'Noto Sans SC\';color:{CLAY}">缺 ›</span></div>')
    return f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:9px">{"".join(cells)}</div>'

def _weekly_grid(weekly, big=False):
    rows = []
    for w in weekly:
        n, t = w.get("n", 0), w.get("t", 3)
        if n >= t:            bg, tc, nc = G, "#F6F2E8", "#F6F2E8"
        elif w.get("behind"): bg, tc, nc = CLAYP, INK, CLAY
        else:                 bg, tc, nc = CARD, INK, MUT
        rows.append(f'<div style="background:{bg};border-radius:16px;padding:13px 16px;display:flex;'
                    f'justify-content:space-between;align-items:center">'
                    f'<span style="font:500 13.5px \'Noto Sans SC\';color:{tc}">{w["name"]}</span>'
                    f'<span class="num" style="font-size:13px;font-weight:500;color:{nc}">{n}/{t}</span></div>')
    return f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:9px">{"".join(rows)}</div>'

def _pill_block(title, note, items, bg, fg, empty):
    body = "".join(f'<span style="background:{bg};color:{fg};border-radius:13px;padding:6px 13px;'
                   f'font:400 12.5px \'Noto Sans SC\'">{x}</span>' for x in items) or (
           f'<span style="background:{CARD};color:{MUT};border-radius:13px;padding:6px 13px;'
           f'font:400 12.5px \'Noto Sans SC\'">{empty}</span>')
    return (f'<div><div style="display:flex;align-items:baseline;gap:8px;margin-bottom:8px">'
            f'<span style="font:700 15px \'Noto Sans SC\'">{title}</span>'
            f'<span style="font:400 11.5px \'Noto Sans SC\';color:{MUT}">{note}</span></div>'
            f'<div style="display:flex;flex-wrap:wrap;gap:7px">{body}</div></div>')

def render_day(d):
    """一整页：今天的餐单 + 今日抗炎营养"""
    h = [HEAD, '<div class="col" style="gap:14px">']
    h.append(f'<div style="display:flex;align-items:flex-start;gap:12px">'
             f'<div style="flex:1"><div style="font:400 11.5px \'Noto Sans SC\';color:{MUT};margin-bottom:1px">{d.get("dateLabel","")}</div>'
             f'<div class="h1">{d.get("title","今天的餐单")}</div></div>'
             f'<div style="width:34px;height:34px;flex:none;border-radius:50%;background:{CARD};display:flex;'
             f'align-items:center;justify-content:center;font:500 11px \'Space Grotesk\';color:{G}">我</div></div>')
    if d.get("week"):
        h.append('<div style="display:flex;gap:7px">' + "".join(
            f'<div style="flex:1;border-radius:14px;padding:9px 0;text-align:center;background:{G if x.get("on") else CARD}">'
            f'<div style="font:400 10.5px \'Noto Sans SC\';color:{"rgba(246,242,232,.75)" if x.get("on") else MUT}">{x["w"]}</div>'
            f'<div class="num" style="font-size:15px;font-weight:700;color:{"#F6F2E8" if x.get("on") else INK}">{x["d"]}</div></div>'
            for x in d["week"]) + '</div>')
    met = sum(1 for c in d["daily"] if c.get("by"))
    sc = {"n": f"{met}/8", "pct": met / 8 * 100, "title": "每日类别覆盖",
          "sub": "按所列食材计算；计划餐单不代表已经吃过"}
    sc.update({k: v for k, v in (d.get("score") or {}).items() if k in ("title", "sub")})
    if sc:
        h.append(f'<div style="background:{G};border-radius:20px;padding:18px 20px;display:flex;align-items:center;gap:16px">'
                 f'<div style="width:74px;height:74px;flex:none;border-radius:50%;'
                 f'background:conic-gradient(#E8D9A8 0 {sc.get("pct",0)}%,rgba(246,242,232,.22) 0);'
                 f'display:flex;align-items:center;justify-content:center">'
                 f'<div style="width:58px;height:58px;border-radius:50%;background:{G};display:flex;align-items:center;'
                 f'justify-content:center;font:700 24px \'Space Grotesk\';color:#F6F2E8">{sc.get("n","")}</div></div>'
                 f'<div style="flex:1;display:flex;flex-direction:column;gap:5px">'
                 f'<span style="font:700 17px \'Noto Sans SC\';color:#F6F2E8">{sc.get("title","今日抗炎分数")}</span>'
                 f'<span style="font:400 12.5px/1.6 \'Noto Sans SC\';color:rgba(246,242,232,.8)">{sc.get("sub","")}</span></div></div>')
    meals = {m["slot"]: m for m in d.get("meals", [])}
    cards = []
    for key, label in SLOTS:
        m = meals.get(key)
        if m:
            right = (f'<span style="font:400 12px \'Noto Sans SC\';color:{CLAY}">{m["flag"]}</span>' if m.get("flag")
                     else f'<span class="num" style="font-size:13px;font-weight:500;color:{MUT}">{m.get("n","")} 类</span>')
            cards.append(f'<div style="background:{CARD};border-radius:18px;padding:13px;display:flex;gap:13px;align-items:center">'
                         + _ph() + f'<div style="flex:1;display:flex;flex-direction:column;gap:3px">'
                         f'<span style="font:400 11px \'Noto Sans SC\';color:{MUT}">{label} · {m.get("time","")}</span>'
                         f'<span style="font:500 15px \'Noto Sans SC\'">{m["title"]}</span></div>{right}</div>')
        else:
            cards.append(f'<div style="border:1px dashed rgba(42,42,36,.24);border-radius:18px;padding:13px;'
                         f'display:flex;gap:13px;align-items:center">'
                         f'<div style="width:48px;height:48px;flex:none;border-radius:14px;background:{CARD};display:flex;'
                         f'align-items:center;justify-content:center;font:300 22px \'Noto Sans SC\';color:{MUT}">+</div>'
                         f'<div style="flex:1;display:flex;flex-direction:column;gap:3px">'
                         f'<span style="font:400 11px \'Noto Sans SC\';color:{MUT}">{label}</span>'
                         f'<span style="font:500 15px \'Noto Sans SC\';color:{MUT}">还空着</span></div>'
                         f'<span style="color:{MUT};font-size:15px">→</span></div>')
    h.append(f'<div style="display:flex;flex-direction:column;gap:9px">{"".join(cards)}</div>')
    # ---- 下半页 · 今日抗炎营养 ----
    met = sum(1 for c in d["daily"] if c.get("by"))
    h.append(f'<div style="border-top:1px solid rgba(42,42,36,.09);margin-top:8px;padding-top:20px;'
             f'display:flex;align-items:flex-start;gap:12px">'
             f'<div style="flex:1"><div class="h1">今日抗炎营养</div></div>'
             f'<div style="text-align:right"><div>'
             f'<span class="num" style="font-size:26px;font-weight:700">{met}</span>'
             f'<span class="num" style="font-size:15px;font-weight:500;color:{MUT}"> / 8 类</span></div>'
             f'<div style="font:400 11px \'Noto Sans SC\';color:{MUT}">每日必有</div></div></div>')
    h.append(_daily_grid(d["daily"]))
    if d.get("caption"):
        h.append(f'<div style="font:400 12.5px/1.7 \'Noto Sans SC\';color:{MUT}">{d["caption"]}</div>')
    if d.get("weekly"):
        h.append(f'<div><div style="display:flex;justify-content:space-between;align-items:baseline;margin-bottom:9px">'
                 f'<span style="font:700 15px \'Noto Sans SC\'">每周达标 6 项</span>'
                 f'<span style="font:400 11.5px \'Noto Sans SC\';color:{MUT}">{d.get("weekNote","今天吃到的已算进去")}</span></div>'
                 + _weekly_grid(d["weekly"]) + '</div>')
    h.append(_pill_block("其他优质蛋白", "今天吃到的", d.get("otherProtein") or [], OLB, OLT, "今天未记录到"))
    h.append(_pill_block("其他中性食物", "不算格子", d.get("neutral") or [], OLB, OLT, "今天未记录到"))
    h.append(_pill_block("限制项", "今天踩中的", d.get("limits") or [], "rgba(181,100,60,.16)", "#8A4A28", "今天未记录到限制项"))
    h.append('</div></html>')
    return "\n".join(h)

def render_week(w):
    """一整页：复盘矩阵 + 这周怎么样"""
    logged = w.get("daysWithRecord", 0)
    w.setdefault("rangeLabel", f'{w.get("weekStart", "")} – {w.get("weekEnd", "")}')
    h = [HEAD, '<div class="col" style="gap:15px">']
    h.append(f'<div class="h1">{w.get("title","复盘")}</div>')
    h.append(f'<div style="background:{G};border-radius:22px;padding:11px;text-align:center;'
             f'color:#F6F2E8">{w.get("rangeLabel", "")}</div>')
    h.append(f'<div style="font:400 12px \'Noto Sans SC\';color:{MUT};margin-top:-6px">'
             f'7 天里有 {logged} 天记录，按记了的算</div>')
    if "personalPlan" in w:
        h.append('<div class="card"><div class="sect">个人频次与记录</div>')
        for row in w["personalPlan"]:
            rule = row["frequency"]
            if rule is None:
                detail = f'不设频次 · 已记录 {row["recordedCount"]:g} 次'
            elif rule["period"] == "day":
                label = '每日必有' if rule["target"] == 1 else f'每天至少 {rule["target"]:g} 次'
                detail = (f'{label} · 有记录的 {logged} 天中 '
                          f'{row["metDays"]} 天达到设定频次')
            else:
                detail = f'每周至少 {rule["target"]:g} 次 · 已记录 {row["recordedCount"]:g} 次'
            h.append(f'<p class="body"><strong>{row["name"]}</strong><br>{detail}</p>')
        h.append('<p class="sub">次数是规划约定，不是营养剂量；未记录不等于没吃。</p></div>')
    else:
        # 矩阵
        rows = []
        for k in DAILY_KEYS:
            cells = w["dailyMatrix"][k]; met = w["dailyMetDays"][k]
            col = MUT if logged == 0 else (G if met == logged else INK)
            sq = "".join(
                f'<span style="flex:1;height:24px;border-radius:7px;'
                + ('background:%s"></span>' % G if c == "met" else
                   'background:#E4E1D2"></span>' if c == "recorded" else
                   'border:1px dashed rgba(42,42,36,.3)"></span>')
                for c in cells)
            rows.append(f'<div style="display:flex;align-items:center;gap:9px">'
                        f'<span style="width:82px;flex:none;font:400 12.5px \'Noto Sans SC\'">{NAME[k]}</span>'
                        f'<span style="flex:1;display:flex;gap:6px">{sq}</span>'
                        f'<span class="num" style="width:32px;text-align:right;font-size:12.5px;font-weight:500;color:{col}">{met}/{logged}</span></div>')
        h.append(f'<div><div style="font:700 15px \'Noto Sans SC\';margin-bottom:10px">每日必有 8 类 · 达标天数</div>'
                 f'<div style="display:flex;flex-direction:column;gap:7px">{"".join(rows)}</div>'
                 f'<div style="display:flex;gap:14px;margin-top:10px;font:400 11px \'Noto Sans SC\';color:{MUT}">'
                 f'<span><span style="display:inline-block;width:9px;height:9px;border-radius:2px;background:{G};'
                 f'margin-right:5px;vertical-align:0"></span>达标</span>'
                 f'<span><span style="display:inline-block;width:9px;height:9px;border-radius:2px;background:#E4E1D2;'
                 f'margin-right:5px"></span>有记录未达标</span>'
                 f'<span><span style="display:inline-block;width:9px;height:9px;border-radius:2px;'
                 f'border:1px dashed rgba(42,42,36,.35);margin-right:5px"></span>没记录</span></div></div>')
        wk = [{"name": n, "n": w["weeklyCounts"].get(k, 0), "t": w.get("weeklyTargets", {}).get(k, t),
               "behind": w["weeklyCounts"].get(k, 0) < t * 2 / 3} for k, n, t, _ in WEEKLY]
        h.append(f'<div><div style="font:700 15px \'Noto Sans SC\';margin-bottom:9px">每周达标 6 项</div>'
                 + _weekly_grid(wk) + '</div>')
    op = [f'{NAME[k]} {v}' for k, v in (w.get("otherProtein") or {}).items() if v]
    if w.get("neutralList"): op = op + [" · ".join(w["neutralList"])]
    h.append(_pill_block("其他优质蛋白 · 中性食物", "", op, OLB, OLT, "这周未记录到"))
    lm = [f'{LIMNAME.get(k,k)} {v}' for k, v in (w.get("limitsHit") or {}).items() if v]
    tot = sum((w.get("limitsHit") or {}).values())
    h.append(_pill_block("限制项", f"踩中 {tot} 次" if tot else "", lm,
                         "rgba(181,100,60,.16)", "#8A4A28", "这周未记录到限制项"))
    if w.get("unrecognizedItems"):
        h.append(_pill_block("待核对食材", "未计入覆盖", w["unrecognizedItems"], CLAYP, CLAY, ""))
    # ---- 下半页 · 这周怎么样 ----
    r = w.get("review") or {}
    h.append(f'<div style="border-top:1px solid rgba(42,42,36,.09);margin-top:8px;padding-top:20px;'
             f'display:flex;align-items:center;gap:12px">'
             f'<div style="flex:1"><div class="h1">这周怎么样</div></div>'
             '</div>')
    h.append(f'<div style="font:400 12.5px \'Noto Sans SC\';color:{MUT};margin-top:-8px">'
             f'{w.get("rangeLabel","").replace(" 本周","")} · {logged} 天有记录</div>')
    if not r:
        h.append(f'<p style="color:{MUT};font-size:12px">以上为记录统计；具体观察与下周动作由助手结合库存补充。</p>')
    if r.get("wins"):
        h.append(f'<div><div style="font:400 12.5px \'Noto Sans SC\';color:{MUT};margin-bottom:7px">做得好的两点</div>'
                 f'<div style="font:400 15px/1.85 \'Noto Sans SC\';color:{INK}">{"<br>".join(r["wins"])}</div></div>')
    if r.get("topGaps"):
        h.append(f'<div style="border-top:1px solid rgba(42,42,36,.09);padding-top:15px">'
                 f'<div style="font:400 12.5px \'Noto Sans SC\';color:{MUT};margin-bottom:9px">最该补的三项</div>'
                 + "".join(f'<div style="display:flex;gap:10px;font:400 15px/1.8 \'Noto Sans SC\';margin-bottom:7px">'
                           f'<span class="num" style="flex:none;color:{INK}">{i+1} ·</span><span>{x}</span></div>'
                           for i, x in enumerate(r["topGaps"])) + '</div>')
    if r.get("actions"):
        h.append(f'<div style="border-top:1px solid rgba(42,42,36,.09);padding-top:15px">'
                 f'<div style="font:400 12.5px \'Noto Sans SC\';color:{MUT};margin-bottom:11px">下周三件事</div>'
                 + "".join(f'<div style="display:flex;gap:12px;align-items:flex-start;margin-bottom:11px">'
                           f'<span style="width:19px;height:19px;flex:none;border-radius:5px;'
                           f'border:1.5px solid rgba(42,42,36,.3);margin-top:3px"></span>'
                           f'<span style="font:400 15px/1.6 \'Noto Sans SC\'">{x}</span></div>' for x in r["actions"])
                 + f'<div style="font:400 12.5px \'Noto Sans SC\';color:{MUT};margin-top:4px">只给三条。做完了下周再生成。</div></div>')
    h.append('</div></html>')
    return "\n".join(h)

SCHEMA = """
Commands:
  fridge --items "菠菜, 西兰花" | fridge --log kitchen-fridge.md
  score --log kitchen-log.md [--end YYYY-MM-DD] [--profile kitchen-profile.json]
  day --json day.json [-o today.html]
  week --json week.json [-o review.html]

day.json:
  daily: exactly eight {"name": category name, "by": ingredient or null} entries.
  meals: [{"slot": "b|l|d|s", "title": "dish", "time": "08:00", "n": 3}].
  Optional: dateLabel, title, weekly [{name,n,t}], caption, weekNote,
            otherProtein [text], neutral [text], limits [text].
  The coverage ring is derived from daily, never a separate health score.
  Planned meals must be labeled as plans and must not be written to the meal log.

score automatically reads kitchen-profile.json next to the log when present.
  --profile selects an explicit file; invalid settings fail instead of reverting silently.
  A profile has optional restrictions/preferences/goals text lists and frequencies:
  {"legumes": {"period": "week", "target": 6}, "tea": null}.
  Omitted categories use defaults; null removes a target; neutral has no target.
  otherProtein counts meals containing any of the four other protein categories once.
  With a profile, personalPlan is authoritative; legacy fields retain default comparisons.
  Daily plans with custom frequencies should use a personal-goal table, not day's fixed ring.

week.json: output from score, optionally supplemented with title, rangeLabel,
  review: {"wins": [text], "topGaps": [text], "actions": [text]}.
  unrecognizedItems must be reviewed before interpreting missing categories.
  All text is plain text, not HTML. See repository examples/ for runnable inputs.
"""


def escaped_text(value):
    if isinstance(value, str): return escape(value, quote=True)
    if isinstance(value, list): return [escaped_text(x) for x in value]
    if isinstance(value, dict): return {k: escaped_text(v) for k, v in value.items()}
    return value


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", choices=["score", "day", "week", "fridge", "schema"])
    ap.add_argument("--log"); ap.add_argument("--json"); ap.add_argument("--end"); ap.add_argument("-o")
    ap.add_argument("--profile", help="个人设置 JSON；默认读取日志同目录的 kitchen-profile.json")
    ap.add_argument("--items", help="逗号或换行分隔的原始食材条目")
    a = ap.parse_args(argv)
    if a.cmd == "schema":
        print(SCHEMA)
        return
    if a.cmd == "fridge" and (a.items is None) == (a.log is None):
        ap.error("fridge requires exactly one of --items or --log")
    if a.cmd == "score" and not a.log:
        ap.error("score requires --log")
    if a.cmd in ("day", "week") and not a.json:
        ap.error(f"{a.cmd} requires --json")
    if a.profile and a.cmd != "score":
        ap.error("--profile is supported by score; use its output with week")
    try:
        if a.cmd == "fridge":
            raw = a.items if a.items is not None else Path(a.log).read_text(encoding="utf-8")
            out = render_fridge(parse_fridge(raw))
        elif a.cmd == "score":
            profile_path = Path(a.profile) if a.profile else Path(a.log).with_name("kitchen-profile.json")
            profile = None
            if a.profile or profile_path.exists():
                profile = json.loads(profile_path.read_text(encoding="utf-8"))
                profile_frequencies(profile)
            out = json.dumps(score(Path(a.log).read_text(encoding="utf-8"), a.end, profile), ensure_ascii=False, indent=2)
        else:
            data = json.loads(Path(a.json).read_text(encoding="utf-8"))
            if a.cmd == "day":
                names = [c["name"] for c in data["daily"]]
                if len(names) != 8 or set(names) != {NAME[k] for k in DAILY_KEYS}:
                    raise ValueError("daily must contain each of the eight daily categories exactly once")
            data = escaped_text(data)
            out = render_day(data) if a.cmd == "day" else render_week(data)
        if a.o:
            Path(a.o).write_text(out, encoding="utf-8")
            print(a.o)
        else:
            print(out)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        ap.error(str(exc))


if __name__ == "__main__":
    main()
