# -*- coding: utf-8 -*-
from PIL import Image

p = r"E:\a-kimi\桌宠\pet_transparent.png"
img = Image.open(p).convert("RGBA")
w, h = img.size
print("尺寸:", img.size, "模式:", img.mode)

# 角落 alpha 应接近 0
for pos in [(0,0),(w-1,0),(0,h-1),(w-1,h-1),(w//2,0),(w//2,h-1)]:
    print(pos, img.getpixel(pos))

# 统计完全不透明(RGB白)像素 / 完全透明像素
opaque_white = 0
transparent = 0
total_white = 0
px = img.load()
for y in range(h):
    for x in range(w):
        r,g,b,a = px[x,y]
        if a == 0:
            transparent += 1
        if r>240 and g>240 and b>240:
            total_white += 1
            if a > 128:
                opaque_white += 1
print("完全透明像素:", transparent)
print("白色且不透明(应接近0):", opaque_white)
