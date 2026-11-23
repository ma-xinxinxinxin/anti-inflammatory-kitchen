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

# ---------- 食材表（来源：references/lexicon.json） ----------
LEXICON_PATH = Path(__file__).resolve().parent.parent / "references" / "lexicon.json"
LEX = json.loads(LEXICON_PATH.read_text(encoding="utf-8"))
DAILY = [(c["key"], c["name"], " ".join(c["words"])) for c in LEX["daily"]]
HALF = {w: c["key"] for c in LEX["daily"] for w in c.get("half", [])}
WEEK_HALF = {w: c["key"] for c in LEX["weekly"] for w in c.get("half", [])}
WEEKLY = [(c["key"], c["name"], c["target"], " ".join(c["words"])) for c in LEX["weekly"]]
OTHERP = [(c["key"], c["name"], " ".join(c["words"])) for c in LEX["otherProtein"]]
NEUTRAL = list(LEX["neutral"])
LIMITS = [(x["key"], x["name"]) for x in LEX["limits"]]
EN_NAME = {c["key"]: c["en"] for group in ("daily", "weekly", "otherProtein") for c in LEX[group]}
EN_NAME["neutral"] = "Neutral foods"
T2S = str.maketrans(LEX.get("traditional", {}))

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
ALIASES = dict(LEX["aliases"])
for alias, canonical in ALIASES.items():
    VOCAB[alias] = list(VOCAB[canonical])
DAILY_KEYS = [k for k, _, _ in DAILY]
NAME = {k: n for k, n, _ in DAILY}
NAME.update({k: n for k, n, _, _ in WEEKLY})
NAME.update({k: n for k, n, _ in OTHERP})
LIMNAME = dict(LIMITS)
LIMNAME_EN = {x["key"]: x.get("en", x["name"]) for x in LEX["limits"]}
UPF_EN = list(LEX.get("processedEn", []))
# 规范名 -> 英文名（取词典里第一个英文别名）
EN_FOOD = {}
for _alias, _canon in LEX["aliases"].items():
    if re.search(r"[a-z]", _alias):
        EN_FOOD.setdefault(_canon, _alias)

# ---------- 语言 ----------
LANG = "zh"  # CLI --lang 设置；en 时所有输出为英文
EN_UI = {
    "每日必有": "Daily essentials", "每周达标": "Weekly goals", "其他 · 中性": "Other · neutral",
    "类别": "Category", "有什么": "In stock", "空": "none", "空着：": "Empty: ",
    "加工品（不计入类别）：": "Processed (not counted): ", "待确认（未归类）：": "To confirm (unclassified): ",
    "今天的餐单": "Today's meals", "我": "Me", "每日类别覆盖": "Daily category coverage",
    "按所列食材计算；计划餐单不代表已经吃过": "Based on the listed ingredients; planned meals are not meals eaten",
    "今日抗炎分数": "Daily coverage", "早餐": "Breakfast", "午餐": "Lunch", "晚餐": "Dinner", "加餐": "Snack",
    "还空着": "Not planned yet", "今日抗炎营养": "Today's anti-inflammatory mix", "缺 ›": "Missing ›",
    "每周达标 6 项": "Weekly goals · 6", "今天吃到的已算进去": "Includes today",
    "其他优质蛋白": "Other quality protein", "今天吃到的": "Eaten today", "其他中性食物": "Other neutral foods",
    "不算格子": "Not counted", "今天未记录到": "Nothing logged today", "限制项": "Limits",
    "今天踩中的": "Logged today", "今天未记录到限制项": "No limits logged today",
    "复盘": "Weekly review", "个人频次与记录": "Your targets and records",
    "次数是规划约定，不是营养剂量；未记录不等于没吃。": "Counts are planning targets, not nutrient doses. Not logged does not mean not eaten.",
    "每日必有 8 类 · 达标天数": "8 daily essentials · days met", "达标": "Met", "有记录未达标": "Logged, not met",
    "没记录": "Not logged", "其他优质蛋白 · 中性食物": "Other protein · neutral foods",
    "这周未记录到": "Nothing logged this week", "这周未记录到限制项": "No limits logged this week",
    "待核对食材": "Ingredients to confirm", "未计入覆盖": "Not counted", "这周怎么样": "How this week went",
    "以上为记录统计；具体观察与下周动作由助手结合库存补充。": "These are logging statistics. Observations and next week's actions come from the assistant, using your stock.",
    "做得好的两点": "Two things that went well", "最该补的三项": "Top three gaps", "下周三件事": "Three things for next week",
    "只给三条。做完了下周再生成。": "Three at most. Make new ones next week.",
    "抗炎厨房 · 周复盘": "Anti-Inflammatory Kitchen · Weekly", "这周吃得怎么样": "How I ate this week",
    "覆盖度是记录指标，不是健康评分": "Coverage is a logging measure, not a health score",
    "不数卡路里 · 不打卡": "No calories · No streaks",
    "抗炎指数": "Anti-inflammatory index", "本周实际": "This week", "每周目标": "Weekly target",
    "从最重要的开始": "Most important first", "；目标按记录天数折算": "; targets scaled to logged days",
    "抗炎指数按记录计算，反映搭配完整度，不是医学评分": "Based on logged meals · not a medical score",
    "候选来自记录缺口与库存；按用户计划的餐次挑选，不必全部买齐。记录少于 3 天时只作参考。":
        "Candidates come from logged gaps and current stock. Pick by the meals planned; no need to buy everything. With fewer than 3 logged days, treat this as a rough guide.",
    "7 天里有 {n} 天记录，按记了的算": "{n} of 7 days logged; counted from what was logged",
    "{n} 天有记录": "{n} days logged", "踩中 {n} 次": "{n} logged", "{n} 类": "{n} categories", " / 8 类": " / 8",
    "{a}/{b} 天": "{a}/{b} days", "{a}/{b} 次": "{a}/{b} times",
    "不设频次 · 已记录 {n} 次": "No target · logged {n} times", "每天至少 {n} 次": "At least {n} a day",
    "{label} · 有记录的 {logged} 天中 {met} 天达到设定频次": "{label} · met on {met} of {logged} logged days",
    "每周至少 {t} 次 · 已记录 {n} 次": "At least {t} a week · logged {n} times",
}


def t(zh, **kw):
    """界面文字：zh 为键；LANG=en 时取英文。"""
    text = EN_UI.get(zh, zh) if LANG == "en" else zh
    return text.format(**kw) if kw else text


def nm(key):
    """类别显示名。"""
    if LANG == "en":
        return EN_NAME.get(key) or LIMNAME_EN.get(key, key)
    return NAME.get(key) or LIMNAME.get(key, key)


def limname(key):
    return LIMNAME_EN.get(key, key) if LANG == "en" else LIMNAME.get(key, key)


def sep():
    return ", " if LANG == "en" else "、"


def html_lang():
    return "en" if LANG == "en" else "zh-CN"


# ---------- 英文词组匹配 ----------
EN_DROP = {"fresh", "frozen", "organic", "canned", "can", "tin", "tinned", "raw", "cooked", "roasted", "roast",
           "grilled", "steamed", "baked", "boiled", "poached", "sliced", "chopped", "diced", "mashed", "homemade",
           "a", "an", "some", "of", "the", "and", "with", "on", "in", "cup", "cups", "handful", "bowl", "slice",
           "slices", "piece", "pieces", "fillet", "fillets", "glass", "mug", "tbsp", "tsp", "pack", "bag", "bottle",
           "small", "large", "big", "little", "few", "bunch", "pcs", "pc", "lb", "lbs", "oz", "g", "kg", "ml"}


EN_SOFT = {"baby", "plain", "natural", "light", "mini", "whole", "wild", "ripe", "lean", "skinless",
           "boneless", "low", "fat", "full", "extra", "virgin", "greek", "style", "unsweetened", "mixed"}


def _en_key(phrase):
    """英文词组 -> 词典里的键；依次尝试原形与常见复数还原。"""
    tries = [phrase]
    head, _, last = phrase.rpartition(" ")
    pre = head + " " if head else ""
    if last.endswith("ies"): tries.append(pre + last[:-3] + "y")
    if last.endswith("oes"): tries.append(pre + last[:-2])
    if last.endswith("es"): tries.append(pre + last[:-2])
    if last.endswith("s"): tries.append(pre + last[:-1])
    for c in tries:
        if c in VOCAB:
            return c
    return None


def en_items(piece):
    """一段英文 -> [已识别键或未识别词组]；最长词组优先，修饰词与数量忽略。"""
    words = [w for w in re.findall(r"[a-z0-9%]+", piece.lower().replace("-", " "))
             if w not in EN_DROP and not re.fullmatch(r"x?\d+[a-z]*", w)]
    out, unknown, i = [], [], 0
    while i < len(words):
        for size in range(min(4, len(words) - i), 0, -1):
            key = _en_key(" ".join(words[i:i + size]))
            if key:
                if unknown: out.append(" ".join(unknown)); unknown = []
                out.append(key); i += size
                break
        else:
            unknown.append(words[i]); i += 1
    if unknown: out.append(" ".join(unknown))
    # 同一段里已识别出食材时，只剩修饰词的碎片不再报待确认（baby spinach、plain greek yogurt）。
    if any(x in VOCAB for x in out):
        out = [x for x in out if x in VOCAB or not set(x.split()) <= EN_SOFT]
    return out


def split_items(segment):
    """日志一段 -> 食材列表。中文按空格/顿号切；英文按逗号切再做词组匹配。"""
    items = []
    for piece in (x.strip() for x in re.split(r"[,，、;；]+", segment)):
        if not piece:
            continue
        if re.search(r"[A-Za-z]", piece):
            items += en_items(piece)
        else:
            items += [x for x in piece.split() if x]
    return items


def normalize(name):
    """繁体转简体、英文转小写并合并空白；不做模糊翻译。"""
    t = (name or "").translate(T2S).strip()
    if re.search(r"[A-Za-z]", t):
        t = re.sub(r"\s+", " ", t.lower())
    return t


def canonical(name):
    """别名 -> 规范名；未收录时原样返回。"""
    n = normalize(name)
    return ALIASES.get(n, n)


UPF = list(LEX["processed"])
NOISE = re.compile(r"(有机|日日鲜|冰鲜|冷冻|新鲜|进口|云南|挪威|智利|特级初榨(?=橄榄油))")
QTY = re.compile(r"[\d.]+\s*(g|kg|克|千克|ml|毫升|升|盒|袋|把|根|颗|个|块|段|片|罐|瓶|只|条|包|份|x|X|\*)")
EN_QTY = re.compile(r"(?i)\b[x×]\s*\d+\b|^\s*\d+\s+(?=[a-z])|\b(?:fresh|frozen|organic)\s+"
                    r"|\b\d+(?:\.\d+)?\s*(?:pcs?|pieces?|packs?|cans?|bottles?|bags?|lbs?|oz|cups?)\b")
DATE = re.compile(r"[·・]?\s*(到|至|到期|保质期?)?\s*[（(]?(?:\d{4}[-/.])?\d{1,2}[-/.]\d{1,2}[）)]?|\d+\s*天")

def clean(raw):
    """一条原始条目 -> 干净食材名"""
    t = re.sub(r"^\s*[-*•]?\s*\[\w+\]\s*", "", raw.translate(T2S))
    t = re.sub(r"[·・]\s*(常备|冷冻常备).*$", "", t)
    t = t.strip().strip("·-—•*").strip()
    t = DATE.sub("", t); t = QTY.sub("", t)
    t = re.sub(r"[（(].*?[）)]", "", t)
    t = NOISE.sub("", t)
    t = EN_QTY.sub("", t)
    t = re.sub(r"[·・]?\s*(到|至|到期|保质期?)\s*$", "", t)
    return t.strip(" 、,，:：·-")

def classify(name):
    """干净名 -> (类别key, 是否加工品)。先精确后包含。"""
    if not name: return None, False
    name = normalize(name)
    if name in VOCAB: return VOCAB[name][0][0], False
    if re.search(r"[a-z]", name):
        if any(re.search(r"\b" + re.escape(u) + r"s?\b", name) for u in UPF_EN):
            return None, True
        for item in en_items(name):
            if item in VOCAB:
                return VOCAB[item][0][0], False
        return None, False
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
            hit = normalize(n) if normalize(n) in VOCAB else next(
                (x for x in en_items(normalize(n)) if x in VOCAB), None) if re.search(r"[A-Za-z]", n) else None
            keys = [key for key, _ in VOCAB[hit]] if hit else [k]
            for key in keys:
                buckets.setdefault(key, []).append(n)
    out, empty = [], []
    for title, keys in FRIDGE_ROWS:
        out.append(f"**{t(title)}**\n\n| {t('类别')} | {t('有什么')} |\n|---|---|")
        for k in keys:
            v = buckets.get(k) or []
            if not v: empty.append(nm(k))
            out.append(f"| {nm(k)} | {sep().join(dict.fromkeys(v)) if v else t('空')} |")
        out.append("")
    if empty: out.append("> " + t("空着：") + " · ".join(empty))
    if upf: out.append("> " + t("加工品（不计入类别）：") + sep().join(dict.fromkeys(upf)))
    if unknown: out.append("> " + t("待确认（未归类）：") + sep().join(dict.fromkeys(unknown)))
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
            if len(cells) != 2 or cells[0] not in set(NAME.values()) | set(EN_NAME.values()):
                continue
            line = cells[1]
        elif line.startswith(">"):
            if line.startswith(("> 空着", "> Empty")):
                continue
            if not line.startswith(("> 加工品", "> 待确认", "> Processed", "> To confirm")):
                continue
            line = re.split(r"[：:]", line, maxsplit=1)[-1]
        else:
            line = re.sub(r"^[-*•]\s*(?:\[\w+\]\s*)?", "", line)
            line = re.sub(r"^[^：:]{1,32}[：:]", "", line)
        items.extend(x.strip() for x in re.split(r"[,，、;；\n]", line)
                     if x.strip() and x.strip().lower() not in ("空", "---", "none", "-", "—"))
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
            low = p.lower()
            if p.startswith(("限制:", "限制：")) or low.startswith(("limit:", "limits:")):
                lim_here = [x.strip() for x in re.split(r"[,，]", re.split(r"[:：]", p, maxsplit=1)[-1]) if x.strip()]
            elif p.startswith("外食") or low.startswith(("eating out", "eat out", "takeout", "take-out")):
                continue
            else:
                meal_items += split_items(p)
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
            for it in dict.fromkeys(normalize(x) for x in items):
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
    result["weeklyIndex"] = weekly_index(result)["score"]
    return result

# ---------- 视觉 ----------
HEAD = """<!doctype html><html lang="LANG_ATTR"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<style>
 *{box-sizing:border-box;margin:0}
 body{background:#F6F2E8;color:#2A2A24;font-family:"Noto Sans SC",system-ui,sans-serif;
      padding:22px;max-width:430px;margin:0 auto}
 .num{font-family:"Space Grotesk",monospace}
 .col{display:flex;flex-direction:column;gap:13px}
 .card{background:#EFEADB;border-radius:18px;padding:13px 15px}
 .h1{font:700 22px/1.35 "Noto Sans SC",system-ui,sans-serif}
 .sub{font:400 11px/1.6 "Noto Sans SC",system-ui,sans-serif;color:#6B6857}
 .sect{font:500 12.5px "Noto Sans SC",system-ui,sans-serif;color:#6B6857;margin-bottom:9px}
 .pill{display:inline-flex;align-items:center;border-radius:12px;padding:4px 10px;font:400 11.5px "Noto Sans SC",system-ui,sans-serif}
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
 .tip b{font:500 11px "Noto Sans SC",system-ui,sans-serif;color:#8A4A28;display:block;margin-bottom:3px}
 .tip p{font:400 12.5px/1.7 "Noto Sans SC",system-ui,sans-serif;color:#8A6A4E}
 .g2{display:grid;grid-template-columns:1fr 1fr;gap:6px}
 .wk{border-radius:12px;padding:7px 10px;display:flex;justify-content:space-between;align-items:center;
     font:400 11.5px "Noto Sans SC",system-ui,sans-serif;background:#EFEADB}
 .wk.on{background:#3D5A3F;color:#F6F2E8}
 .meal{background:#EFEADB;border-radius:18px;padding:11px;display:flex;gap:11px;align-items:center}
 .ph{width:48px;height:48px;border-radius:14px;flex:none;
     background:repeating-linear-gradient(45deg,#DCD3BE 0 6px,#D3C9B1 6px 12px)}
 .body{font:400 13px/1.85 "Noto Sans SC",system-ui,sans-serif;color:#3A382C}
 ol{margin:0;padding-left:0;list-style:none}
</style>"""

def ring(pct, label, big=58):
    inner = big - 13
    return (f'<div style="width:{big}px;height:{big}px;flex:none;border-radius:50%;'
            f'background:conic-gradient(#E8D9A8 0 {pct}%,rgba(246,242,232,.2) 0);'
            f'display:flex;align-items:center;justify-content:center">'
            f'<div style="width:{inner}px;height:{inner}px;border-radius:50%;background:#3D5A3F;'
            f'display:flex;align-items:center;justify-content:center;font:700 15px \'Space Grotesk\',ui-monospace,monospace;'
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
                         f'<span style="font:500 14px \'Noto Sans SC\',system-ui,sans-serif;color:#F6F2E8">{c["name"]}</span>'
                         f'<span style="font:400 11.5px \'Noto Sans SC\',system-ui,sans-serif;color:rgba(246,242,232,.8);text-align:right">{by}</span></div>')
        else:
            cells.append(f'<div style="border:1px dashed rgba(42,42,36,.3);border-radius:16px;padding:14px 16px;'
                         f'display:flex;justify-content:space-between;align-items:center">'
                         f'<span style="font:500 14px \'Noto Sans SC\',system-ui,sans-serif;color:{INK}">{c["name"]}</span>'
                         f'<span style="font:500 12px \'Noto Sans SC\',system-ui,sans-serif;color:{CLAY}">{t("缺 ›")}</span></div>')
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
                    f'<span style="font:500 13.5px \'Noto Sans SC\',system-ui,sans-serif;color:{tc}">{w["name"]}</span>'
                    f'<span class="num" style="font-size:13px;font-weight:500;color:{nc}">{n:g}/{t:g}</span></div>')
    return f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:9px">{"".join(rows)}</div>'

def _pill_block(title, note, items, bg, fg, empty):
    body = "".join(f'<span style="background:{bg};color:{fg};border-radius:13px;padding:6px 13px;'
                   f'font:400 12.5px \'Noto Sans SC\',system-ui,sans-serif">{x}</span>' for x in items) or (
           f'<span style="background:{CARD};color:{MUT};border-radius:13px;padding:6px 13px;'
           f'font:400 12.5px \'Noto Sans SC\',system-ui,sans-serif">{empty}</span>')
    return (f'<div><div style="display:flex;align-items:baseline;gap:8px;margin-bottom:8px">'
            f'<span style="font:700 15px \'Noto Sans SC\',system-ui,sans-serif">{title}</span>'
            f'<span style="font:400 11.5px \'Noto Sans SC\',system-ui,sans-serif;color:{MUT}">{note}</span></div>'
            f'<div style="display:flex;flex-wrap:wrap;gap:7px">{body}</div></div>')

def render_day(d):
    """一整页：今天的餐单 + 今日抗炎营养"""
    h = [HEAD.replace("LANG_ATTR", html_lang()), '<div class="col" style="gap:14px">']
    h.append(f'<div style="display:flex;align-items:flex-start;gap:12px">'
             f'<div style="flex:1"><div style="font:400 11.5px \'Noto Sans SC\',system-ui,sans-serif;color:{MUT};margin-bottom:1px">{d.get("dateLabel","")}</div>'
             f'<div class="h1">{d.get("title") or t("今天的餐单")}</div></div>'
             f'<div style="width:34px;height:34px;flex:none;border-radius:50%;background:{CARD};display:flex;'
             f'align-items:center;justify-content:center;font:500 11px \'Space Grotesk\',ui-monospace,monospace;color:{G}">{t("我")}</div></div>')
    if d.get("week"):
        h.append('<div style="display:flex;gap:7px">' + "".join(
            f'<div style="flex:1;border-radius:14px;padding:9px 0;text-align:center;background:{G if x.get("on") else CARD}">'
            f'<div style="font:400 10.5px \'Noto Sans SC\',system-ui,sans-serif;color:{"rgba(246,242,232,.75)" if x.get("on") else MUT}">{x["w"]}</div>'
            f'<div class="num" style="font-size:15px;font-weight:700;color:{"#F6F2E8" if x.get("on") else INK}">{x["d"]}</div></div>'
            for x in d["week"]) + '</div>')
    met = sum(1 for c in d["daily"] if c.get("by"))
    sc = {"n": f"{met}/8", "pct": met / 8 * 100, "title": t("每日类别覆盖"),
          "sub": t("按所列食材计算；计划餐单不代表已经吃过")}
    sc.update({k: v for k, v in (d.get("score") or {}).items() if k in ("title", "sub")})
    if sc:
        h.append(f'<div style="background:{G};border-radius:20px;padding:18px 20px;display:flex;align-items:center;gap:16px">'
                 f'<div style="width:74px;height:74px;flex:none;border-radius:50%;'
                 f'background:conic-gradient(#E8D9A8 0 {sc.get("pct",0)}%,rgba(246,242,232,.22) 0);'
                 f'display:flex;align-items:center;justify-content:center">'
                 f'<div style="width:58px;height:58px;border-radius:50%;background:{G};display:flex;align-items:center;'
                 f'justify-content:center;font:700 24px \'Space Grotesk\',ui-monospace,monospace;color:#F6F2E8">{sc.get("n","")}</div></div>'
                 f'<div style="flex:1;display:flex;flex-direction:column;gap:5px">'
                 f'<span style="font:700 17px \'Noto Sans SC\',system-ui,sans-serif;color:#F6F2E8">{sc.get("title") or t("今日抗炎分数")}</span>'
                 f'<span style="font:400 12.5px/1.6 \'Noto Sans SC\',system-ui,sans-serif;color:rgba(246,242,232,.8)">{sc.get("sub","")}</span></div></div>')
    meals = {m["slot"]: m for m in d.get("meals", [])}
    cards = []
    for key, label in SLOTS:
        label = t(label)
        m = meals.get(key)
        if m:
            right = (f'<span style="font:400 12px \'Noto Sans SC\',system-ui,sans-serif;color:{CLAY}">{m["flag"]}</span>' if m.get("flag")
                     else f'<span class="num" style="font-size:13px;font-weight:500;color:{MUT}">{t("{n} 类", n=m.get("n",""))}</span>')
            cards.append(f'<div style="background:{CARD};border-radius:18px;padding:13px;display:flex;gap:13px;align-items:center">'
                         + _ph() + f'<div style="flex:1;display:flex;flex-direction:column;gap:3px">'
                         f'<span style="font:400 11px \'Noto Sans SC\',system-ui,sans-serif;color:{MUT}">{label} · {m.get("time","")}</span>'
                         f'<span style="font:500 15px \'Noto Sans SC\',system-ui,sans-serif">{m["title"]}</span></div>{right}</div>')
        else:
            cards.append(f'<div style="border:1px dashed rgba(42,42,36,.24);border-radius:18px;padding:13px;'
                         f'display:flex;gap:13px;align-items:center">'
                         f'<div style="width:48px;height:48px;flex:none;border-radius:14px;background:{CARD};display:flex;'
                         f'align-items:center;justify-content:center;font:300 22px \'Noto Sans SC\',system-ui,sans-serif;color:{MUT}">+</div>'
                         f'<div style="flex:1;display:flex;flex-direction:column;gap:3px">'
                         f'<span style="font:400 11px \'Noto Sans SC\',system-ui,sans-serif;color:{MUT}">{label}</span>'
                         f'<span style="font:500 15px \'Noto Sans SC\',system-ui,sans-serif;color:{MUT}">{t("还空着")}</span></div>'
                         f'<span style="color:{MUT};font-size:15px">→</span></div>')
    h.append(f'<div style="display:flex;flex-direction:column;gap:9px">{"".join(cards)}</div>')
    # ---- 下半页 · 今日抗炎营养 ----
    met = sum(1 for c in d["daily"] if c.get("by"))
    h.append(f'<div style="border-top:1px solid rgba(42,42,36,.09);margin-top:8px;padding-top:20px;'
             f'display:flex;align-items:flex-start;gap:12px">'
             f'<div style="flex:1"><div class="h1">{t("今日抗炎营养")}</div></div>'
             f'<div style="text-align:right"><div>'
             f'<span class="num" style="font-size:26px;font-weight:700">{met}</span>'
             f'<span class="num" style="font-size:15px;font-weight:500;color:{MUT}">{t(" / 8 类")}</span></div>'
             f'<div style="font:400 11px \'Noto Sans SC\',system-ui,sans-serif;color:{MUT}">{t("每日必有")}</div></div></div>')
    h.append(_daily_grid(d["daily"]))
    if d.get("caption"):
        h.append(f'<div style="font:400 12.5px/1.7 \'Noto Sans SC\',system-ui,sans-serif;color:{MUT}">{d["caption"]}</div>')
    if d.get("weekly"):
        h.append(f'<div><div style="display:flex;justify-content:space-between;align-items:baseline;margin-bottom:9px">'
                 f'<span style="font:700 15px \'Noto Sans SC\',system-ui,sans-serif">{t("每周达标 6 项")}</span>'
                 f'<span style="font:400 11.5px \'Noto Sans SC\',system-ui,sans-serif;color:{MUT}">{d.get("weekNote") or t("今天吃到的已算进去")}</span></div>'
                 + _weekly_grid(d["weekly"]) + '</div>')
    h.append(_pill_block(t("其他优质蛋白"), t("今天吃到的"), d.get("otherProtein") or [], OLB, OLT, t("今天未记录到")))
    h.append(_pill_block(t("其他中性食物"), t("不算格子"), d.get("neutral") or [], OLB, OLT, t("今天未记录到")))
    h.append(_pill_block(t("限制项"), t("今天踩中的"), d.get("limits") or [], "rgba(181,100,60,.16)", "#8A4A28", t("今天未记录到限制项")))
    h.append('</div></html>')
    return "\n".join(h)

def render_week(w):
    """一整页：复盘矩阵 + 这周怎么样"""
    logged = w.get("daysWithRecord", 0)
    w.setdefault("rangeLabel", f'{w.get("weekStart", "")} – {w.get("weekEnd", "")}')
    h = [HEAD.replace("LANG_ATTR", html_lang()), '<div class="col" style="gap:15px">']
    h.append(f'<div class="h1">{w.get("title") or t("复盘")}</div>')
    h.append(f'<div style="background:{G};border-radius:22px;padding:11px;text-align:center;'
             f'color:#F6F2E8">{w.get("rangeLabel", "")}</div>')
    h.append(f'<div style="font:400 12px \'Noto Sans SC\',system-ui,sans-serif;color:{MUT};margin-top:-6px">'
             f'{t("7 天里有 {n} 天记录，按记了的算", n=logged)}</div>')
    if "personalPlan" in w:
        h.append(f'<div class="card"><div class="sect">{t("个人频次与记录")}</div>')
        for row in w["personalPlan"]:
            rule = row["frequency"]
            if rule is None:
                detail = t("不设频次 · 已记录 {n} 次", n=f'{row["recordedCount"]:g}')
            elif rule["period"] == "day":
                label = t("每日必有") if rule["target"] == 1 else t("每天至少 {n} 次", n=f'{rule["target"]:g}')
                detail = t("{label} · 有记录的 {logged} 天中 {met} 天达到设定频次",
                           label=label, logged=logged, met=row["metDays"])
            else:
                detail = t("每周至少 {t} 次 · 已记录 {n} 次", t=f'{rule["target"]:g}', n=f'{row["recordedCount"]:g}')
            h.append(f'<p class="body"><strong>{nm(row["key"]) if LANG == "en" else row["name"]}</strong><br>{detail}</p>')
        h.append(f'<p class="sub">{t("次数是规划约定，不是营养剂量；未记录不等于没吃。")}</p></div>')
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
                        f'<span style="width:{112 if LANG == "en" else 82}px;flex:none;font:400 12.5px \'Noto Sans SC\',system-ui,sans-serif">{nm(k)}</span>'
                        f'<span style="flex:1;display:flex;gap:6px">{sq}</span>'
                        f'<span class="num" style="width:32px;text-align:right;font-size:12.5px;font-weight:500;color:{col}">{met}/{logged}</span></div>')
        h.append(f'<div><div style="font:700 15px \'Noto Sans SC\',system-ui,sans-serif;margin-bottom:10px">{t("每日必有 8 类 · 达标天数")}</div>'
                 f'<div style="display:flex;flex-direction:column;gap:7px">{"".join(rows)}</div>'
                 f'<div style="display:flex;gap:14px;margin-top:10px;font:400 11px \'Noto Sans SC\',system-ui,sans-serif;color:{MUT}">'
                 f'<span><span style="display:inline-block;width:9px;height:9px;border-radius:2px;background:{G};'
                 f'margin-right:5px;vertical-align:0"></span>{t("达标")}</span>'
                 f'<span><span style="display:inline-block;width:9px;height:9px;border-radius:2px;background:#E4E1D2;'
                 f'margin-right:5px"></span>{t("有记录未达标")}</span>'
                 f'<span><span style="display:inline-block;width:9px;height:9px;border-radius:2px;'
                 f'border:1px dashed rgba(42,42,36,.35);margin-right:5px"></span>{t("没记录")}</span></div></div>')
        wk = [{"name": nm(k), "n": w["weeklyCounts"].get(k, 0), "t": w.get("weeklyTargets", {}).get(k, target),
               "behind": w["weeklyCounts"].get(k, 0) < target * 2 / 3} for k, n, target, _ in WEEKLY]
        h.append(f'<div><div style="font:700 15px \'Noto Sans SC\',system-ui,sans-serif;margin-bottom:9px">{t("每周达标 6 项")}</div>'
                 + _weekly_grid(wk) + '</div>')
    op = [f'{nm(k)} {v}' for k, v in (w.get("otherProtein") or {}).items() if v]
    if w.get("neutralList"): op = op + [" · ".join(w["neutralList"])]
    h.append(_pill_block(t("其他优质蛋白 · 中性食物"), "", op, OLB, OLT, t("这周未记录到")))
    lm = [f'{limname(k)} {v}' for k, v in (w.get("limitsHit") or {}).items() if v]
    tot = sum((w.get("limitsHit") or {}).values())
    h.append(_pill_block(t("限制项"), t("踩中 {n} 次", n=tot) if tot else "", lm,
                         "rgba(181,100,60,.16)", "#8A4A28", t("这周未记录到限制项")))
    if w.get("unrecognizedItems"):
        h.append(_pill_block(t("待核对食材"), t("未计入覆盖"), w["unrecognizedItems"], CLAYP, CLAY, ""))
    # ---- 下半页 · 这周怎么样 ----
    r = w.get("review") or {}
    h.append(f'<div style="border-top:1px solid rgba(42,42,36,.09);margin-top:8px;padding-top:20px;'
             f'display:flex;align-items:center;gap:12px">'
             f'<div style="flex:1"><div class="h1">{t("这周怎么样")}</div></div>'
             '</div>')
    h.append(f'<div style="font:400 12.5px \'Noto Sans SC\',system-ui,sans-serif;color:{MUT};margin-top:-8px">'
             f'{w.get("rangeLabel","").replace(" 本周","")} · {t("{n} 天有记录", n=logged)}</div>')
    if not r:
        h.append(f'<p style="color:{MUT};font-size:12px">{t("以上为记录统计；具体观察与下周动作由助手结合库存补充。")}</p>')
    if r.get("wins"):
        h.append(f'<div><div style="font:400 12.5px \'Noto Sans SC\',system-ui,sans-serif;color:{MUT};margin-bottom:7px">{t("做得好的两点")}</div>'
                 f'<div style="font:400 15px/1.85 \'Noto Sans SC\',system-ui,sans-serif;color:{INK}">{"<br>".join(r["wins"])}</div></div>')
    if r.get("topGaps"):
        h.append(f'<div style="border-top:1px solid rgba(42,42,36,.09);padding-top:15px">'
                 f'<div style="font:400 12.5px \'Noto Sans SC\',system-ui,sans-serif;color:{MUT};margin-bottom:9px">{t("最该补的三项")}</div>'
                 + "".join(f'<div style="display:flex;gap:10px;font:400 15px/1.8 \'Noto Sans SC\',system-ui,sans-serif;margin-bottom:7px">'
                           f'<span class="num" style="flex:none;color:{INK}">{i+1} ·</span><span>{x}</span></div>'
                           for i, x in enumerate(r["topGaps"])) + '</div>')
    if r.get("actions"):
        h.append(f'<div style="border-top:1px solid rgba(42,42,36,.09);padding-top:15px">'
                 f'<div style="font:400 12.5px \'Noto Sans SC\',system-ui,sans-serif;color:{MUT};margin-bottom:11px">{t("下周三件事")}</div>'
                 + "".join(f'<div style="display:flex;gap:12px;align-items:flex-start;margin-bottom:11px">'
                           f'<span style="width:19px;height:19px;flex:none;border-radius:5px;'
                           f'border:1.5px solid rgba(42,42,36,.3);margin-top:3px"></span>'
                           f'<span style="font:400 15px/1.6 \'Noto Sans SC\',system-ui,sans-serif">{x}</span></div>' for x in r["actions"])
                 + f'<div style="font:400 12.5px \'Noto Sans SC\',system-ui,sans-serif;color:{MUT};margin-top:4px">{t("只给三条。做完了下周再生成。")}</div></div>')
    h.append('</div></html>')
    return "\n".join(h)

# ---------- 补货闭环 ----------
def fridge_by_category(items):
    """原始库存条目 -> {类别key: [食材名]}；一个食材可进多类。"""
    out = {}
    for raw in items:
        n = clean(raw)
        key = normalize(n)
        for k, _ in VOCAB.get(key, []):
            out.setdefault(k, []).append(n)
    return {k: list(dict.fromkeys(v)) for k, v in out.items()}


NO_PADDING = {"tea", "darkChocolate", "goodFat"}


def _restricted(word, restrictions):
    return any(word and word in r for r in restrictions)


def restock(log_text, fridge_text, end=None, profile=None, limit=3):
    """周记录缺口 × 当前库存 -> 先用现有的 / 值得补买的。只给候选，不替用户下单。"""
    week = score(log_text, end, profile)
    logged = week["daysWithRecord"]
    stock = fridge_by_category(parse_fridge(fridge_text))
    restrictions = (profile or {}).get("restrictions", [])
    gaps = []
    if "personalPlan" in week:
        for row in week["personalPlan"]:
            rule, key = row["frequency"], row["key"]
            if rule is None or key == "otherProtein":
                continue
            if rule["period"] == "day":
                short = logged - row["metDays"]
                if logged and short > 0:
                    gaps.append((key, short / logged, t("{a}/{b} 天", a=row["metDays"], b=logged)))
            elif row["recordedCount"] < rule["target"]:
                gaps.append((key, 1 - row["recordedCount"] / rule["target"],
                             t("{a}/{b} 次", a=f'{row["recordedCount"]:g}', b=f'{rule["target"]:g}')))
    else:
        for key in DAILY_KEYS:
            met = week["dailyMetDays"][key]
            if logged and met < logged:
                gaps.append((key, (logged - met) / logged, t("{a}/{b} 天", a=met, b=logged)))
        for key, _, target, _ in WEEKLY:
            n = week["weeklyCounts"][key]
            if n < target:
                gaps.append((key, 1 - n / target, t("{a}/{b} 次", a=f"{n:g}", b=target)))
    # 规则：不为凑格子额外喝茶、吃巧克力或加油，这三类排在最后。
    gaps.sort(key=lambda g: (g[0] in NO_PADDING, -g[1]))
    examples = {k: s.split() for k, _, s in DAILY}
    examples.update({k: s.split() for k, _, _, s in WEEKLY})
    use, buy = [], []
    for key, _, record in gaps:
        entry = {"key": key, "category": nm(key), "record": record}
        if stock.get(key):
            use.append({**entry, "inStock": stock[key]})
        elif len(buy) < limit:
            options = [w for w in examples[key]
                       if not _restricted(w, restrictions) and not _restricted(EN_FOOD.get(w, ""), restrictions)]
            if LANG == "en":
                options = [EN_FOOD[w] for w in options if w in EN_FOOD]
            options = options[:3]
            buy.append({**entry, "options": options})
    return {
        "weekStart": week["weekStart"], "weekEnd": week["weekEnd"], "daysWithRecord": logged,
        "evidence": "insufficient" if logged < 3 else "ok",
        "useWhatYouHave": use, "worthBuying": buy,
        "unrecognizedItems": week["unrecognizedItems"],
        "note": t("候选来自记录缺口与库存；按用户计划的餐次挑选，不必全部买齐。记录少于 3 天时只作参考。"),
    }


# ---------- 抗炎指数与分享卡 ----------
# 从最重要的开始：每周最该保证的放在最上面。
IMPORTANCE = ["fattyFish", "goodFat", "leafy", "cruciferous", "legumes", "berryCitrus", "nutsSeeds",
              "wholeGrain", "fermented", "redOrange", "mushrooms", "spices", "tea", "darkChocolate"]


def _half(x):
    return round(x * 2) / 2


def weekly_index(w):
    """14 类：每周目标 vs 本周实际 -> 0–100 抗炎指数。

    每日类别按每周 7 份计（实际 = 达标天数）；每周类别用默认或个人目标。
    记录不满 7 天时目标按记录天数折算，未记录不等于没吃。不设频次的类别只展示，不计分。
    这是按记录计算的搭配完整度，不是医学评分。
    """
    logged = w.get("daysWithRecord", 0)
    factor = logged / 7 if logged else 0
    plan = {r["key"]: r for r in w.get("personalPlan", [])}
    rows = []
    for k in IMPORTANCE:
        daily = k in DAILY_KEYS
        if k in plan:
            rule = plan[k]["frequency"]
            if rule is None:
                full, actual = None, plan[k]["recordedCount"]
            elif rule["period"] == "day":
                full, actual = 7, plan[k].get("metDays", 0)
            else:
                full, actual = rule["target"], plan[k]["recordedCount"]
        elif daily:
            full, actual = 7, w["dailyMetDays"][k]
        else:
            full = w.get("weeklyTargets", {}).get(k) or dict((x, t) for x, _, t, _ in WEEKLY)[k]
            actual = w["weeklyCounts"].get(k, 0)
        target = None if full is None else max(0.5, _half(full * factor)) if logged else full
        rows.append({"key": k, "name": nm(k), "target": target, "weeklyTarget": full,
                     "actual": actual, "met": target is not None and actual >= target})
    scored = [r for r in rows if r["target"]]
    value = round(100 * sum(min(r["actual"] / r["target"], 1) for r in scored) / len(scored)) \
        if logged and scored else None
    return {"score": value, "daysWithRecord": logged, "prorated": 0 < logged < 7, "rows": rows}


def _fmt(x):
    return f"{x:g}"


def render_card(w):
    """1080×1440 周复盘分享卡：14 类按重要性排列，每行目标与实际同轴，右上角抗炎指数。
    只含记录统计与下周三件事，不含库存、忌口、个人设置或健康信息。"""
    idx = weekly_index(w)
    logged = idx["daysWithRecord"]
    rng = w.get("rangeLabel") or f'{w.get("weekStart", "")} – {w.get("weekEnd", "")}'
    scale = max([7] + [min(r["actual"], 9) for r in idx["rows"]])
    rows = []
    for r in idx["rows"]:
        tgt, act = r["target"], r["actual"]
        fill = min(act, scale) / scale * 100
        box = (f'<i class="tg" style="width:{tgt / scale * 100:.2f}%"></i>' if tgt else "")
        mark = (f'<i class="mk" style="left:calc({tgt / scale * 100:.2f}% - 2px)"></i>' if tgt else "")
        num = (f'<b class="{"ok" if r["met"] else ""}">{_fmt(act)}</b><span>/{_fmt(tgt)}</span>'
               if tgt else f'<b>{_fmt(act)}</b><span>/—</span>')
        rows.append(f'<div class="r"><span class="n">{r["name"]}</span>'
                    f'<span class="tr">{box}<i class="ac" style="width:{fill:.2f}%"></i>{mark}</span>'
                    f'<span class="v num">{num}</span></div>')
    sub = t("7 天里有 {n} 天记录，按记了的算", n=logged)
    if idx["prorated"]:
        sub += t("；目标按记录天数折算")
    score = "—" if idx["score"] is None else idx["score"]
    actions = (w.get("review") or {}).get("actions") or []
    act = "".join(f'<div class="a"><b></b><span>{x}</span></div>' for x in actions[:3])
    return f"""<!doctype html><html lang="{html_lang()}"><meta charset="utf-8">
<style>
*{{box-sizing:border-box;margin:0}}
body{{background:#DCD6C2}}
.card{{width:1080px;height:1440px;background:#F6F2E8;color:#2A2A24;padding:68px 80px 56px;
  font-family:"Noto Sans SC",system-ui,sans-serif;display:flex;flex-direction:column;gap:26px;overflow:hidden}}
.num{{font-family:"Space Grotesk",ui-monospace,monospace}}
.top{{display:flex;justify-content:space-between;align-items:flex-start;gap:30px}}
.k{{font-size:27px;color:#6B6857}}
.t{{font-weight:700;font-size:64px;line-height:1.15;margin:6px 0 18px}}
.rg{{display:inline-block;background:#3D5A3F;color:#F6F2E8;border-radius:40px;padding:10px 26px;font-size:26px}}
.sub{{font-size:24px;color:#6B6857;margin-top:14px}}
.sc{{flex:none;width:236px;height:236px;border-radius:50%;background:#3D5A3F;color:#F6F2E8;
  display:flex;flex-direction:column;align-items:center;justify-content:center}}
.sc .big{{font-size:96px;font-weight:700;line-height:1}}
.sc .lb{{font-size:{19 if LANG == "en" else 24}px;opacity:.85;margin-top:8px;text-align:center;line-height:1.25;width:170px}}
.lg{{display:flex;gap:30px;font-size:22px;color:#6B6857;align-items:center}}
.lg i{{display:inline-block;width:34px;height:16px;border-radius:5px;margin-right:10px;vertical-align:-1px}}
.rows{{display:flex;flex-direction:column;gap:13px}}
.r{{display:flex;align-items:center;gap:22px;height:36px}}
.n{{width:{290 if LANG == "en" else 210}px;flex:none;font-size:{25 if LANG == "en" else 27}px}}
.tr{{flex:1;height:26px;border-radius:8px;background:#ECE6D6;position:relative}}
.tr i{{position:absolute;left:0;top:0;bottom:0;border-radius:8px}}
.tg{{border:2.5px dashed rgba(61,90,63,.55);background:rgba(61,90,63,.06)}}
.ac{{background:#3D5A3F}}
.tr i.mk{{width:4px;top:-6px;bottom:-6px;border-radius:2px;background:#2A2A24}}
.v{{width:96px;flex:none;text-align:right;font-size:26px;color:#6B6857}}
.v b{{color:#B5643C;font-weight:600}} .v b.ok{{color:#3D5A3F}}
.a{{display:flex;gap:18px;align-items:flex-start;font-size:26px;line-height:1.45;margin-bottom:6px}}
.a b{{width:28px;height:28px;flex:none;border-radius:7px;border:2.5px solid rgba(42,42,36,.3);margin-top:5px}}
.f span:last-child{{white-space:nowrap}}
.f{{margin-top:auto;display:flex;justify-content:space-between;gap:20px;font-size:21px;color:#6B6857;
  border-top:2px solid rgba(42,42,36,.09);padding-top:22px}}
</style>
<div class="card">
 <div class="top">
  <div><div class="k">{t("抗炎厨房 · 周复盘")}</div><div class="t">{w.get("title") or t("这周吃得怎么样")}</div>
   <span class="rg num">{rng}</span><div class="sub">{sub}</div></div>
  <div class="sc"><span class="big num">{score}</span><span class="lb">{t("抗炎指数")}</span></div>
 </div>
 <div class="lg"><span><i style="background:#3D5A3F"></i>{t("本周实际")}</span>
  <span><i style="border:2.5px dashed rgba(61,90,63,.55);position:relative"><em style="position:absolute;right:-3px;top:-6px;bottom:-6px;width:4px;border-radius:2px;background:#2A2A24"></em></i>{t("每周目标")}</span>
  <span>{t("从最重要的开始")}</span></div>
 <div class="rows">{"".join(rows)}</div>
 {f'<div><div class="k" style="margin-bottom:12px">{t("下周三件事")}</div>{act}</div>' if act else ''}
 <div class="f"><span>{t("抗炎指数按记录计算，反映搭配完整度，不是医学评分")}</span><span>{t("不数卡路里 · 不打卡")}</span></div>
</div></html>"""


SCHEMA = """
Commands (add --lang en for English output; default zh):
  fridge --items "菠菜, 西兰花" | fridge --log kitchen-fridge.md
  score --log kitchen-log.md [--end YYYY-MM-DD] [--profile kitchen-profile.json]
  day --json day.json [-o today.html]
  week --json week.json [-o review.html]
  card --json week.json [-o card.html]        1080x1440 shareable weekly card (no inventory or health data)
  restock --log kitchen-log.md --fridge kitchen-fridge.md [--end YYYY-MM-DD] [--profile ...]
      -> JSON: useWhatYouHave (gaps already in stock) and worthBuying (up to 3 gaps, 3 options each)

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
    ap.add_argument("cmd", choices=["score", "day", "week", "card", "restock", "fridge", "schema"])
    ap.add_argument("--fridge", help="restock 使用的库存文件")
    ap.add_argument("--lang", choices=["zh", "en"], default="zh", help="输出语言 / output language")
    ap.add_argument("--log"); ap.add_argument("--json"); ap.add_argument("--end"); ap.add_argument("-o")
    ap.add_argument("--profile", help="个人设置 JSON；默认读取日志同目录的 kitchen-profile.json")
    ap.add_argument("--items", help="逗号或换行分隔的原始食材条目")
    a = ap.parse_args(argv)
    global LANG
    LANG = a.lang
    if a.cmd == "schema":
        print(SCHEMA)
        return
    if a.cmd == "fridge" and (a.items is None) == (a.log is None):
        ap.error("fridge requires exactly one of --items or --log")
    if a.cmd == "score" and not a.log:
        ap.error("score requires --log")
    if a.cmd == "restock" and not (a.log and a.fridge):
        ap.error("restock requires --log and --fridge")
    if a.cmd in ("day", "week", "card") and not a.json:
        ap.error(f"{a.cmd} requires --json")
    if a.profile and a.cmd not in ("score", "restock"):
        ap.error("--profile is supported by score and restock; use score output with week")
    try:
        if a.cmd == "fridge":
            raw = a.items if a.items is not None else Path(a.log).read_text(encoding="utf-8")
            out = render_fridge(parse_fridge(raw))
        elif a.cmd in ("score", "restock"):
            profile_path = Path(a.profile) if a.profile else Path(a.log).with_name("kitchen-profile.json")
            profile = None
            if a.profile or profile_path.exists():
                profile = json.loads(profile_path.read_text(encoding="utf-8"))
                profile_frequencies(profile)
            log_text = Path(a.log).read_text(encoding="utf-8")
            if a.cmd == "score":
                result = score(log_text, a.end, profile)
            else:
                result = restock(log_text, Path(a.fridge).read_text(encoding="utf-8"), a.end, profile)
            out = json.dumps(result, ensure_ascii=False, indent=2)
        else:
            data = json.loads(Path(a.json).read_text(encoding="utf-8"))
            if a.cmd == "day":
                names = [c["name"] for c in data["daily"]]
                if len(names) != 8 or set(names) != {NAME[k] for k in DAILY_KEYS}:
                    raise ValueError("daily must contain each of the eight daily categories exactly once")
            data = escaped_text(data)
            out = render_day(data) if a.cmd == "day" else render_card(data) if a.cmd == "card" else render_week(data)
        if a.o:
            Path(a.o).write_text(out, encoding="utf-8")
            print(a.o)
        else:
            print(out)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        ap.error(str(exc))


if __name__ == "__main__":
    main()
