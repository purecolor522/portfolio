import re, io, urllib.request, tempfile, os
from fontTools.ttLib import TTFont
from fontTools.subset import Subsetter, Options
from fontTools.merge import Merger

BASE = "https://cdn.jsdelivr.net/gh/VdustR/taipei-sans-tc@0.1.1/packages/core/dist/Regular/"
CSS  = BASE + "TaipeiSansTCBeta-Regular.css"

# --- 1) 大標題字元集合 ---
static_headlines = [
    "把模糊的需求，整理成可信任的產品。",
    "精選作品", "產品與網頁", "平面設計", "專案統籌",
    "我怎麼工作。",
    "設計背景出身，在做產品的路上學會用 AI。",
    "經歷",
    "一起把點子，做成值得信任的產品。",
    "找不到這件作品",          # work.html 404 標題
    "下一件作品 所有作品",      # 安全字
    "問題 過程 成果 畫面",      # 安全字（之後若要套用）
]
# 從 data.js 取出所有作品 title（詳情頁大標題是動態的）
data = open("data.js", encoding="utf-8").read()
titles = re.findall(r"title:\s*'([^']*)'", data)
# 自動從 HTML 抓所有 font-tp 大標題用字（跨電腦編輯也不漏字）
html_all = open("index.html",encoding="utf-8").read() + open("work.html",encoding="utf-8").read()
tp_text = "".join(re.sub(r"<[^>]+>"," ", m.group(2)) for m in re.finditer(r"<(h1|h2|h3)\b[^>]*font-tp[^>]*>(.*?)</\1>", html_all, re.S))
chars = set("".join(static_headlines) + "".join(titles) + tp_text + " AI0123456789+%。，、（）")
chars = {c for c in chars if c.strip() != ""} | {" "}
print(f"大標題不重複字元數：{len(chars)}")

# --- 2) 解析 CSS：每個 @font-face 的 檔名 + unicode-range ---
css = urllib.request.urlopen(CSS).read().decode("utf-8")
blocks = re.findall(r"@font-face\s*{(.*?)}", css, re.S)
chunkmap = []  # (filename, set_of_codepoints_ranges)
for b in blocks:
    fn = re.search(r"url\(['\"]?([^'\")]+)['\"]?\)", b)
    ur = re.search(r"unicode-range:\s*([^;}]+)", b)
    if not fn or not ur: continue
    fname = fn.group(1).split("/")[-1]
    ranges = []
    for tok in ur.group(1).split(","):
        tok = tok.strip().replace("U+", "")
        if "-" in tok:
            a, z = tok.split("-"); ranges.append((int(a,16), int(z,16)))
        else:
            ranges.append((int(tok,16), int(tok,16)))
    chunkmap.append((fname, ranges))

def chunk_for(cp):
    for fname, ranges in chunkmap:
        for a, z in ranges:
            if a <= cp <= z: return fname
    return None

# --- 3) 每個字 -> 需要的 chunk ---
need = {}
for ch in chars:
    fn = chunk_for(ord(ch))
    if fn: need.setdefault(fn, set()).add(ch)
    else:  print("⚠ 無對應 chunk:", repr(ch), hex(ord(ch)))
print(f"需要下載的 chunk 數：{len(need)}")

# --- 4) 下載每個 chunk、瘦身到該 chunk 的字，存暫存 ttf ---
tmp = tempfile.mkdtemp()
parts = []
for fname, cs in need.items():
    raw = urllib.request.urlopen(BASE + fname).read()
    font = TTFont(io.BytesIO(raw))           # 直接讀 woff2（需 brotli）
    opt = Options(); opt.glyph_names = True; opt.notdef_outline = True
    opt.layout_features = []; opt.name_IDs = []; opt.recalc_bounds = True
    ss = Subsetter(options=opt); ss.populate(text="".join(cs)); ss.subset(font)
    p = os.path.join(tmp, fname.replace(".woff2","")+".ttf")
    font.flavor = None; font.save(p); parts.append(p)

# --- 5) 合併所有片段 -> 一個字型，輸出 woff2 ---
out = "fonts/TaipeiSansTC-headline.woff2"
if len(parts) == 1:
    f = TTFont(parts[0])
else:
    f = Merger().merge(parts)
f.flavor = "woff2"
f.save(out)

# --- 6) 驗證：cmap 是否涵蓋所有字 ---
chk = TTFont(out); cmap = chk.getBestCmap()
missing = [c for c in chars if ord(c) not in cmap]
print(f"輸出：{out}  大小：{os.path.getsize(out)//1024} KB")
print("缺字：", "".join(missing) if missing else "無 ✅")
