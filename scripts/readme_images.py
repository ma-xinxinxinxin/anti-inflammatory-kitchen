#!/usr/bin/env python3
"""Build the README images (English and Simplified Chinese) from fictional example data.

    python3 scripts/readme_images.py            # HTML + PNG (PNG needs Chrome or Chromium)
    python3 scripts/readme_images.py --html     # HTML only

Outputs docs/images/{weekly,breakfasts,foods}-{en,zh}.png. To use real breakfast photos,
put breakfast-1.jpg, breakfast-2.jpg and breakfast-3.jpg in docs/images/photos/ and run again.
"""
import argparse
import base64
import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "images"
PHOTOS = OUT / "photos"
spec = importlib.util.spec_from_file_location("kitchen", ROOT / "kitchen/scripts/kitchen.py")
k = importlib.util.module_from_spec(spec)
spec.loader.exec_module(k)

BASE_CSS = """*{box-sizing:border-box;margin:0}
body{background:#F6F2E8;color:#2A2A24;font-family:"Noto Sans SC",system-ui,sans-serif}
.num{font-family:"Space Grotesk",ui-monospace,monospace}"""

# ---------- Fictional example content ----------
FRIDGE = {
    "zh": ["希腊酸奶", "蓝莓", "核桃", "奇亚籽", "燕麦", "苹果", "肉桂", "鸡蛋", "菠菜", "小番茄", "全麦面包", "橄榄油"],
    "en": ["Greek yogurt", "blueberries", "walnuts", "chia seeds", "oats", "apple", "cinnamon", "eggs",
           "spinach", "cherry tomatoes", "whole wheat bread", "olive oil"],
}
BREAKFASTS = [
    {"zh": "蓝莓核桃酸奶碗", "en": "Blueberry walnut yogurt bowl", "min": 5,
     "items": {"zh": ["希腊酸奶", "蓝莓", "核桃", "奇亚籽"], "en": ["Greek yogurt", "blueberries", "walnuts", "chia seeds"]},
     "hits": ["fermented", "berryCitrus", "nutsSeeds"], "art": "bowl"},
    {"zh": "菠菜番茄炒蛋配全麦吐司", "en": "Spinach & tomato eggs on toast", "min": 10,
     "items": {"zh": ["鸡蛋", "菠菜", "小番茄", "全麦面包", "橄榄油"],
               "en": ["eggs", "spinach", "cherry tomatoes", "whole wheat bread", "olive oil"]},
     "hits": ["leafy", "redOrange", "wholeGrain", "goodFat"], "art": "plate"},
    {"zh": "肉桂苹果燕麦粥", "en": "Cinnamon apple oats", "min": 8,
     "items": {"zh": ["燕麦", "苹果", "核桃", "肉桂"], "en": ["oats", "apple", "walnuts", "cinnamon"]},
     "hits": ["wholeGrain", "nutsSeeds", "spices"], "art": "oats"},
]
ACTIONS = {
    "zh": ["周二晚饭加一份菌菇：香菇豆腐煲", "早餐坚果换成核桃加亚麻籽", "周四备一盒烤西蓝花和红椒"],
    "en": ["Add mushrooms Tuesday: shiitake and tofu pot", "Breakfast nuts: walnuts plus ground flaxseed",
           "Thursday: roast a tray of broccoli and peppers"],
}
TEXT = {
    "zh": {"fridge": "冰箱里有", "title": "今天早餐吃什么？", "sub": "只用冰箱里现有的，三个抗炎早餐",
           "min": "分钟", "need": "用到", "hits": "覆盖",
           "foods": "抗炎食物清单", "foods_sub": "从最重要的开始 · 每周目标份数 · 代表食材",
           "daily": "每天", "per_week": "每周 {n} 份", "other": "其他优质蛋白",
           "other_freq": "轮换，不设目标", "neutral": "中性食物", "neutral_freq": "不计入目标",
           "other_foods": "鸡蛋、鳕鱼、虾、鸡肉、鸭肉、牛肉", "neutral_foods": "香蕉、苹果、黄瓜、土豆、牛奶、海带",
           "note": "频次是规划目标，可以按自己的情况调整；不是医学阈值。"},
    "en": {"fridge": "In the fridge", "title": "What's for breakfast?", "sub": "Three anti-inflammatory breakfasts from what's already there",
           "min": "min", "need": "Uses", "hits": "Covers",
           "foods": "The anti-inflammatory food list", "foods_sub": "Most important first · servings per week · example foods",
           "daily": "Daily", "per_week": "{n} a week", "other": "Other quality protein",
           "other_freq": "Rotate, no target", "neutral": "Neutral foods", "neutral_freq": "Not counted",
           "other_foods": "eggs, cod, shrimp, chicken, duck, beef", "neutral_foods": "banana, apple, cucumber, potato, milk, kelp",
           "note": "Targets are planning defaults you can adjust, not medical thresholds."},
}

# ---------- Illustrations (placeholders until real photos are added) ----------
ART = {
    "bowl": """<svg viewBox="0 0 400 300" preserveAspectRatio="xMidYMid slice" xmlns="http://www.w3.org/2000/svg"><rect width="400" height="300" fill="#E9E1CC"/>
<ellipse cx="200" cy="168" rx="150" ry="118" fill="#D8CBAE"/><ellipse cx="200" cy="160" rx="138" ry="106" fill="#FBF8F1"/>
<ellipse cx="200" cy="160" rx="118" ry="88" fill="#F3EEE3"/>
<g fill="#3E4A8C"><circle cx="150" cy="130" r="13"/><circle cx="172" cy="118" r="12"/><circle cx="160" cy="152" r="13"/><circle cx="185" cy="140" r="11"/><circle cx="140" cy="160" r="11"/><circle cx="198" cy="122" r="12"/></g>
<g fill="#6070B8" opacity=".55"><circle cx="146" cy="126" r="4"/><circle cx="168" cy="114" r="4"/><circle cx="156" cy="148" r="4"/><circle cx="194" cy="118" r="4"/></g>
<g fill="#A87B4F"><path d="M235 140c10-12 30-8 34 4s-8 22-20 20-22-12-14-24z"/><path d="M250 180c8-10 26-6 28 4s-8 18-18 16-17-10-10-20z"/><path d="M220 196c6-8 20-6 22 3s-6 14-14 13-14-8-8-16z"/></g>
<g fill="#2A2A24" opacity=".7"><circle cx="210" cy="170" r="2.4"/><circle cx="218" cy="160" r="2.4"/><circle cx="200" cy="184" r="2.4"/><circle cx="226" cy="176" r="2.4"/><circle cx="192" cy="168" r="2.4"/><circle cx="230" cy="158" r="2.4"/></g>
<path d="M250 110c14-10 30-6 34 0-10 6-22 8-34 0z" fill="#6E8B4E"/></svg>""",
    "plate": """<svg viewBox="0 0 400 300" preserveAspectRatio="xMidYMid slice" xmlns="http://www.w3.org/2000/svg"><rect width="400" height="300" fill="#E4DCC8"/>
<ellipse cx="200" cy="160" rx="160" ry="124" fill="#FBF8F1"/><ellipse cx="200" cy="160" rx="136" ry="102" fill="#F4EFE4"/>
<rect x="72" y="108" width="118" height="104" rx="22" fill="#B98A55"/><rect x="82" y="118" width="98" height="84" rx="16" fill="#D7AE78"/>
<g fill="#F2C94C"><path d="M200 120c20-18 60-12 70 6s-6 40-30 42-56-10-52-26 2-12 12-22z"/><path d="M215 165c18-10 46-4 50 10s-14 26-34 24-30-24-16-34z"/></g>
<g fill="#FBE8A6"><circle cx="230" cy="135" r="9"/><circle cx="246" cy="178" r="7"/></g>
<g fill="#3F6B3A"><path d="M262 205c14-22 44-24 54-10-10 18-38 24-54 10z"/><path d="M285 120c10-18 36-20 44-8-8 16-32 20-44 8z"/><path d="M180 222c10-16 34-18 42-6-8 14-30 18-42 6z"/></g>
<g fill="#C8442E"><circle cx="300" cy="160" r="16"/><circle cx="276" cy="232" r="14"/><circle cx="150" cy="228" r="13"/></g>
<g fill="#E9806A"><circle cx="300" cy="160" r="9"/><circle cx="276" cy="232" r="7"/><circle cx="150" cy="228" r="6"/></g>
<path d="M95 135c20 6 40-2 60 4" stroke="#F0D9A8" stroke-width="5" fill="none" stroke-linecap="round" opacity=".7"/></svg>""",
    "oats": """<svg viewBox="0 0 400 300" preserveAspectRatio="xMidYMid slice" xmlns="http://www.w3.org/2000/svg"><rect width="400" height="300" fill="#E8DFC9"/>
<ellipse cx="200" cy="168" rx="150" ry="118" fill="#A9BFA0"/><ellipse cx="200" cy="160" rx="138" ry="106" fill="#FBF8F1"/>
<ellipse cx="200" cy="160" rx="118" ry="88" fill="#E7D3A8"/>
<g fill="#D9C08C" opacity=".8"><ellipse cx="150" cy="190" rx="10" ry="5"/><ellipse cx="240" cy="200" rx="10" ry="5"/><ellipse cx="200" cy="215" rx="9" ry="4"/><ellipse cx="270" cy="170" rx="9" ry="4"/><ellipse cx="128" cy="150" rx="9" ry="4"/></g>
<g><path d="M150 120c30-22 80-18 96 4-30 12-66 14-96-4z" fill="#F6EBCB" stroke="#C0392B" stroke-width="6"/>
<path d="M176 146c30-22 80-18 96 4-30 12-66 14-96-4z" fill="#F6EBCB" stroke="#B83A2A" stroke-width="6"/>
<path d="M162 172c26-18 70-14 84 4-26 10-58 12-84-4z" fill="#F6EBCB" stroke="#C0392B" stroke-width="6"/></g>
<g fill="#A87B4F"><path d="M120 176c8-10 26-6 28 4s-8 18-18 16-17-10-10-20z"/><path d="M266 196c8-10 26-6 28 4s-8 18-18 16-17-10-10-20z"/></g>
<g fill="#8A4A28" opacity=".55"><circle cx="210" cy="130" r="2"/><circle cx="230" cy="190" r="2"/><circle cx="180" cy="200" r="2"/><circle cx="250" cy="150" r="2"/><circle cx="160" cy="160" r="2"/><circle cx="200" cy="175" r="2"/><circle cx="222" cy="210" r="2"/></g></svg>""",
}


def photo_or_art(i, art):
    for ext in ("jpg", "jpeg", "png", "webp"):
        p = PHOTOS / f"breakfast-{i}.{ext}"
        if p.exists():
            mime = "jpeg" if ext in ("jpg", "jpeg") else ext
            data = base64.b64encode(p.read_bytes()).decode()
            return f'<img src="data:image/{mime};base64,{data}" alt="">'
    return ART[art]


def breakfasts_html(lang):
    T = TEXT[lang]
    k.LANG = lang
    sep = ", " if lang == "en" else "、"
    chips = "".join(f'<span class="chip">{x}</span>' for x in FRIDGE[lang])
    cards = []
    for i, b in enumerate(BREAKFASTS, 1):
        hits = "".join(f'<span class="hit">{k.nm(h)}</span>' for h in b["hits"])
        cards.append(f'''<div class="bf"><div class="pic">{photo_or_art(i, b["art"])}
<span class="time num">{b["min"]} {T["min"]}</span></div>
<div class="body"><div class="name">{b[lang]}</div>
<div class="lab">{T["need"]}</div><div class="items">{sep.join(b["items"][lang])}</div>
<div class="lab">{T["hits"]}</div><div class="hits">{hits}</div></div></div>''')
    return f"""<!doctype html><html lang="{k.html_lang()}"><meta charset="utf-8"><style>{BASE_CSS}
.wrap{{width:1600px;height:1000px;padding:56px 72px;display:flex;flex-direction:column;gap:34px}}
.head{{display:flex;justify-content:space-between;align-items:flex-end}}
.t{{font-size:52px;font-weight:700}} .s{{font-size:24px;color:#6B6857;margin-top:8px}}
.fr{{background:#EFEADB;border-radius:24px;padding:22px 26px;display:flex;gap:18px;align-items:flex-start}}
.fr .k{{flex:none;font-size:22px;font-weight:600;color:#3D5A3F;padding-top:8px;width:{150 if lang == 'en' else 110}px}}
.chips{{display:flex;flex-wrap:wrap;gap:10px}}
.chip{{background:#F6F2E8;border-radius:20px;padding:7px 16px;font-size:{19 if lang == 'en' else 21}px}}
.row{{display:grid;grid-template-columns:1fr 1fr 1fr;gap:30px;flex:1}}
.bf{{background:#FFFDF8;border-radius:28px;overflow:hidden;display:flex;flex-direction:column;
  box-shadow:0 2px 0 rgba(42,42,36,.06)}}
.pic{{height:250px;position:relative;overflow:hidden}} .pic svg,.pic img{{width:100%;height:100%;object-fit:cover;display:block}}
.time{{position:absolute;top:18px;right:18px;background:#3D5A3F;color:#F6F2E8;border-radius:30px;
  padding:8px 18px;font-size:24px;font-weight:600}}
.body{{padding:22px 26px;display:flex;flex-direction:column;gap:6px}}
.name{{font-size:{27 if lang == 'en' else 30}px;font-weight:700;line-height:1.25;margin-bottom:4px}}
.lab{{font-size:18px;color:#6B6857;margin-top:4px}}
.items{{font-size:{20 if lang == 'en' else 22}px;line-height:1.4}}
.hits{{display:flex;flex-wrap:wrap;gap:8px}}
.hit{{background:#E6E8CC;color:#55602F;border-radius:14px;padding:5px 13px;font-size:19px}}
</style><div class="wrap">
<div class="head"><div><div class="t">{T["title"]}</div><div class="s">{T["sub"]}</div></div></div>
<div class="fr"><span class="k">{T["fridge"]}</span><div class="chips">{chips}</div></div>
<div class="row">{"".join(cards)}</div></div></html>"""


def _foods(cat, lang, n=5):
    """Representative foods: first names in lexicon order, skipping near-duplicates (olive oil / EVOO)."""
    out = []
    for w in dict.fromkeys(cat["words"]):
        name = k.EN_FOOD.get(w) if lang == "en" else w
        if name and lang == "en":
            name = name.replace("greek", "Greek")
        if not name or name.startswith("85%") or name in ("熟番茄", "沙丁鱼罐头", "灰树花"):
            continue
        if any(name in x or x in name for x in out):
            continue
        out.append(name)
    return out[:n]


def foods_html(lang):
    T = TEXT[lang]
    k.LANG = lang
    sep = ", " if lang == "en" else "、"
    cats = {c["key"]: (c, 7) for c in k.LEX["daily"]}
    cats.update({c["key"]: (c, c["target"]) for c in k.LEX["weekly"]})
    rows = []
    for key in k.IMPORTANCE:
        cat, n = cats[key]
        dots = "".join(f'<i class="{"on" if j < n else ""}"></i>' for j in range(7))
        freq = T["daily"] if n == 7 else T["per_week"].format(n=n)
        rows.append(f'<div class="r"><span class="n">{k.nm(key)}</span><span class="d">{dots}</span>'
                    f'<span class="f">{freq}</span><span class="w">{sep.join(_foods(cat, lang))}</span></div>')
    for name, freq, foods in ((T["other"], T["other_freq"], T["other_foods"]),
                              (T["neutral"], T["neutral_freq"], T["neutral_foods"])):
        rows.append(f'<div class="r m"><span class="n">{name}</span><span class="d"></span>'
                    f'<span class="f">{freq}</span><span class="w">{foods}</span></div>')
    name_w = 300 if lang == "en" else 190
    return f"""<!doctype html><html lang="{k.html_lang()}"><meta charset="utf-8"><style>{BASE_CSS}
.wrap{{width:1600px;padding:56px 72px 52px;display:flex;flex-direction:column;gap:12px}}
.t{{font-size:44px;font-weight:700}} .s{{font-size:22px;color:#6B6857;margin:6px 0 18px}}
.r{{display:flex;align-items:center;gap:24px;padding:13px 22px;border-radius:16px;background:#EFEADB}}
.r.m{{background:transparent;border:2px dashed rgba(42,42,36,.14)}}
.n{{width:{name_w}px;flex:none;font-size:24px;font-weight:600}}
.d{{width:196px;flex:none;display:flex;gap:6px}}
.d i{{width:22px;height:22px;border-radius:6px;background:#DCD6C2}} .d i.on{{background:#3D5A3F}}
.f{{width:{200 if lang == 'en' else 170}px;flex:none;font-size:21px;color:#3D5A3F;font-weight:600}}
.w{{flex:1;font-size:21px;color:#4A473C;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
.note{{font-size:19px;color:#6B6857;margin-top:12px}}
</style><div class="wrap"><div class="t">{T["foods"]}</div><div class="s">{T["foods_sub"]}</div>
{"".join(rows)}<div class="note">{T["note"]}</div></div></html>"""


def weekly_html(lang):
    k.LANG = lang
    w = k.score((ROOT / "examples/week-log.md").read_text(encoding="utf-8"))
    w["review"] = {"actions": ACTIONS[lang]}
    return k.render_card(k.escaped_text(w))


def chrome():
    for name in ("google-chrome", "chromium", "chromium-browser", "chrome"):
        if shutil.which(name):
            return shutil.which(name)
    mac = Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
    return str(mac) if mac.exists() else None


def shoot(browser, html_path, png_path, width, height):
    subprocess.run([browser, "--headless=new", "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
                    f"--window-size={width},{height}", f"--screenshot={png_path}", html_path.as_uri()],
                   check=True, capture_output=True)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--html", action="store_true", help="write HTML only")
    a = ap.parse_args(argv)
    browser = None if a.html else chrome()
    if not a.html and not browser:
        print("Chrome/Chromium not found; writing HTML only.", file=sys.stderr)
    OUT.mkdir(parents=True, exist_ok=True)
    jobs = [("weekly", weekly_html, 1080, 1440), ("breakfasts", breakfasts_html, 1600, 1000),
            ("foods", foods_html, 1600, {"en": 1330, "zh": 1440})]
    with tempfile.TemporaryDirectory() as tmp:
        for name, build, width, height in jobs:
            for lang in ("en", "zh"):
                html = build(lang)
                target = (Path(tmp) if browser else OUT) / f"{name}-{lang}.html"
                target.write_text(html, encoding="utf-8")
                if browser:
                    h = height[lang] if isinstance(height, dict) else height
                    shoot(browser, target, OUT / f"{name}-{lang}.png", width, h)
                    print(f"docs/images/{name}-{lang}.png")
                else:
                    print(f"docs/images/{name}-{lang}.html")
    k.LANG = "zh"


if __name__ == "__main__":
    main()
