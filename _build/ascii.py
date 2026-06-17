import math, random
random.seed(11)
W, H = 72, 50
ramp = " .:-=+*#%@"
cx, cy = W*0.5, H*0.27
rx, ry = W*0.16, H*0.185
bx, by = W*0.5, H*1.0
brx, bry = W*0.32, H*0.56          # 身體橢圓頂端 ≈ 0.44H，與脖子相接
neck_top, neck_bot = cy+ry*0.74, H*0.50
neck_hw = W*0.066
def L_norm():
    v=(-0.55,-0.7,0.66); m=math.sqrt(sum(c*c for c in v)); return tuple(c/m for c in v)
L=L_norm()
def ch(b):
    b=max(0.0,min(1.0,b)); return ramp[int(b*(len(ramp)-1)+0.5)]
out=[]
for y in range(H):
    row=[]
    for x in range(W):
        c=' '
        nx,ny=(x+0.5-cx)/rx,(y+0.5-cy)/ry
        r2=nx*nx+ny*ny
        if r2<=1.0:                                   # 頭：球面明暗
            nz=math.sqrt(max(0,1-r2)); n=(nx,ny,nz)
            b=sum(n[i]*L[i] for i in range(3)); b=(b+0.28)/1.12
            b+=random.uniform(-0.05,0.05); c=ch(b)
        else:
            ex,ey=(x+0.5-bx)/brx,(y+0.5-by)/bry
            if ex*ex+ey*ey<=1.0 and (y+0.5)>=neck_top:  # 身體/肩膀（左上來光）
                b=0.72-((x+0.5-cx)/(W*0.5))*0.5-((y+0.5)-neck_top)*0.004
                b+=random.uniform(-0.06,0.06); c=ch(b)
            elif neck_top<=(y+0.5)<neck_bot and abs(x+0.5-cx)<=neck_hw:  # 脖子
                b=0.46-((x+0.5-cx)/(W*0.11))*0.22+random.uniform(-0.05,0.05); c=ch(b)
        row.append(c)
    out.append(''.join(row).rstrip())
# 去掉最上/下全空行
while out and not out[0].strip(): out.pop(0)
while out and not out[-1].strip(): out.pop()
print('\n'.join(out))
print("\n--- 行數:", len(out), "最大寬:", max(len(r) for r in out))
