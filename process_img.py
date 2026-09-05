# -*- coding: utf-8 -*-
"""把简笔画 JPG 白底抠成透明 PNG。"""
from PIL import Image
from collections import deque

src = r"E:\a-kimi\桌宠\微信图片_20260905184017_3695_962.jpg"
img = Image.open(src).convert("RGBA")
print("原图尺寸:", img.size, "模式:", img.mode)

THRESHOLD = 230
mask = img.convert("L")
px = img.load()
w, h = img.size

visited = set()
q = deque()
for x in range(0, w):
    q.append((x, 0)); q.append((x, h - 1))
for y in range(0, h):
    q.append((0, y)); q.append((w - 1, y))

bg = set()
while q:
    x, y = q.popleft()
    if (x, y) in visited:
        continue
    visited.add((x, y))
    if mask.getpixel((x, y)) < THRESHOLD:
        continue
    bg.add((x, y))
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        nx, ny = x + dx, y + dy
        if 0 <= nx < w and 0 <= ny < h and (nx, ny) not in visited:
            q.append((nx, ny))

print("背景像素数:", len(bg), "/", w * h)

for (x, y) in bg:
    r, g, b, a = px[x, y]
    px[x, y] = (r, g, b, 0)

bbox = img.getbbox()
print("内容边界 bbox:", bbox)
cropped = img.crop(bbox)

out = r"E:\a-kimi\桌宠\pet_transparent.png"
cropped.save(out)
print("已保存:", out, "新尺寸:", cropped.size)

big = cropped.resize((cropped.size[0] * 2, cropped.size[1] * 2), Image.LANCZOS)
big_out = r"E:\a-kimi\桌宠\pet_big.png"
big.save(big_out)
print("放大版:", big_out, big.size)
