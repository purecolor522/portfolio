# 生成「Project on a Page」圖解 SVG（淺色、終端風、可在卡片與詳情頁顯示）
W, H = 1280, 960
BG="#f4f3ef"; CARD="#ffffff"; LINE="#e2e0d9"; INK="#1b1b1f"; MUT="#6c6c72"; GRN="#0f7a50"; TINT="#e9f3ed"
MONO="'JetBrains Mono','SFMono-Regular',monospace"
CJK="'Noto Sans TC','PingFang TC','Microsoft JhengHei',sans-serif"
def esc(s): return s.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
def wrap(s, n):
    out=[]; line=''
    for ch in s:
        line+=ch
        if len(line)>=n and ch in '、，。 ）':
            out.append(line); line=''
        elif len(line)>=n+3:
            out.append(line); line=''
    if line: out.append(line)
    return out
cards=[
 ("01","是什麼 · 服務誰","WHAT / WHO","戶外草地福音音樂節：音樂演出 × 市集 × 文青生命故事。對象是福音朋友與多間夥伴教會家人。"),
 ("02","目標","GOAL","用低壓力的同樂，和福音朋友建立關係、串連夥伴教會——不是純聚會，而是「來得舒服、留得下來」。"),
 ("03","時程","TIMELINE","11 月起籌備、確認名單與攤位 → 12/14 當天 13:30 場佈、12:30 起試音、16:00 開演、20:00 收場。"),
 ("04","我的角色 · 節目統籌","MY ROLE — PROGRAM LEAD","確認 13 組演出名單、設計試音時間表、掌控現場換場與器材／音響規格，並親自擔任 DJ。"),
 ("05","規模 · 製作","SCOPE","13 組演出、約 48 位表演者；完整舞台音響（主喇叭、6 路監聽、6 支無線麥、鼓／鍵盤／貝斯收音）；3 間教會協作。"),
 ("06","成果 · 復盤","OUTCOME / RETRO","4 小時節目準時跑完、換場用市集與主持填補不冷場。復盤：下次更早鎖定器材需求。〔人數與回饋待補〕"),
]
s=[]
s.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="{CJK}">')
s.append(f'<rect width="{W}" height="{H}" fill="{BG}"/>')
# 細格線底紋
for gx in range(0,W,48): s.append(f'<line x1="{gx}" y1="0" x2="{gx}" y2="{H}" stroke="{LINE}" stroke-width="1" opacity="0.5"/>')
for gy in range(0,H,48): s.append(f'<line x1="0" y1="{gy}" x2="{W}" y2="{gy}" stroke="{LINE}" stroke-width="1" opacity="0.5"/>')
PADX=56
# Header
s.append(f'<text x="{PADX}" y="74" font-family="{MONO}" font-size="20" letter-spacing="4" fill="{GRN}">// PROJECT ON A PAGE · 活動統籌</text>')
s.append(f'<text x="{PADX}" y="130" font-size="52" font-weight="700" fill="{INK}">光の慶典 · 草地敬拜音樂節</text>')
s.append(f'<text x="{PADX}" y="172" font-family="{MONO}" font-size="22" fill="{MUT}">2024 / 12 / 14 · 台南浸信會大草地 · 16:00–20:00</text>')
s.append(f'<line x1="{PADX}" y1="200" x2="{W-PADX}" y2="200" stroke="{INK}" stroke-width="2"/>')
# 6 cards: 2 cols x 3 rows
gx0, gy0 = PADX, 228
cw, ch = (W-2*PADX-32)//2, 200
gap=24
for i,(num,zh,en,body) in enumerate(cards):
    col=i%2; row=i//2
    x=gx0+col*(cw+32); y=gy0+row*(ch+gap)
    s.append(f'<rect x="{x}" y="{y}" width="{cw}" height="{ch}" fill="{CARD}" stroke="{LINE}" stroke-width="1.5"/>')
    s.append(f'<rect x="{x}" y="{y}" width="6" height="{ch}" fill="{GRN}"/>')
    s.append(f'<text x="{x+28}" y="{y+44}" font-family="{MONO}" font-size="26" font-weight="700" fill="{GRN}">{num}</text>')
    s.append(f'<text x="{x+72}" y="{y+44}" font-size="25" font-weight="700" fill="{INK}">{esc(zh)}</text>')
    s.append(f'<text x="{x+72}" y="{y+64}" font-family="{MONO}" font-size="13" letter-spacing="2" fill="{MUT}">{en}</text>')
    ty=y+102
    for ln in wrap(body, 21):
        s.append(f'<text x="{x+28}" y="{ty}" font-size="21" fill="{INK}">{esc(ln)}</text>'); ty+=30
# Footer
fy=H-30
s.append(f'<line x1="{PADX}" y1="{H-58}" x2="{W-PADX}" y2="{H-58}" stroke="{LINE}" stroke-width="1.5"/>')
s.append(f'<text x="{PADX}" y="{fy}" font-family="{MONO}" font-size="18" fill="{MUT}">蘇雅軒 · 節目統籌 / Program Lead</text>')
s.append(f'<text x="{W-PADX}" y="{fy}" text-anchor="end" font-family="{MONO}" font-size="18" fill="{MUT}">TBC · TNGNC · TKCH 跨教會協作</text>')
s.append('</svg>')
open("images/light-festival.svg","w",encoding="utf-8").write("\n".join(s))
print("✅ images/light-festival.svg 產生完成（", len("\n".join(s))//1024, "KB )")
