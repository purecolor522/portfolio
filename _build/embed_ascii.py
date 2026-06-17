import math, random, re, textwrap
random.seed(11)
W, H = 72, 50
ramp = " .:-=+*#%@"
cx, cy = W*0.5, H*0.27
rx, ry = W*0.16, H*0.185
bx, by = W*0.5, H*1.0
brx, bry = W*0.32, H*0.56
neck_top, neck_bot = cy+ry*0.74, H*0.50
neck_hw = W*0.066
v=(-0.55,-0.7,0.66); m=math.sqrt(sum(c*c for c in v)); L=tuple(c/m for c in v)
def ch(b): b=max(0.,min(1.,b)); return ramp[int(b*(len(ramp)-1)+0.5)]
rows=[]
for y in range(H):
    r=[]
    for x in range(W):
        c=' '; nx,ny=(x+.5-cx)/rx,(y+.5-cy)/ry; r2=nx*nx+ny*ny
        if r2<=1.: nz=math.sqrt(max(0,1-r2)); b=(nx*L[0]+ny*L[1]+nz*L[2]+.28)/1.12+random.uniform(-.05,.05); c=ch(b)
        else:
            ex,ey=(x+.5-bx)/brx,(y+.5-by)/bry
            if ex*ex+ey*ey<=1. and (y+.5)>=neck_top: c=ch(0.72-((x+.5-cx)/(W*.5))*.5-((y+.5)-neck_top)*.004+random.uniform(-.06,.06))
            elif neck_top<=(y+.5)<neck_bot and abs(x+.5-cx)<=neck_hw: c=ch(0.46-((x+.5-cx)/(W*.11))*.22+random.uniform(-.05,.05))
        r.append(c)
    rows.append(''.join(r).rstrip())
while rows and not rows[0].strip(): rows.pop(0)
while rows and not rows[-1].strip(): rows.pop()
art="\n".join(textwrap.dedent("\n".join(rows)).split("\n"))
# 嵌入 index.html（取代 picsum 肖像）
html=open("index.html",encoding="utf-8").read()
old='''            <div class="overflow-hidden rounded-2xl border border-line aspect-[4/5]">
              <img src="https://picsum.photos/seed/yian-pm-portrait-studio/900/1125" alt="蘇雅軒 工作肖像" class="w-full h-full object-cover" loading="eager" />
            </div>'''
new='''            <div class="overflow-hidden rounded-2xl border border-line aspect-[4/5] bg-surface grid place-items-center px-2">
              <pre aria-hidden="true" class="ascii-art text-accent select-none">'''+art+'''</pre>
            </div>'''
assert old in html, "找不到肖像區塊"
open("index.html","w",encoding="utf-8").write(html.replace(old,new))
print("✅ 已嵌入 ASCII 肖像（",len(rows),"行 )")
