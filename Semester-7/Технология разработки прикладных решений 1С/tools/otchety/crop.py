#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Обрезает пустое поле на скриншотах 1С: снизу всегда, справа — только если
содержимое окна занимает лишь левую часть экрана (узкие формы обработок)."""
import os, sys
from PIL import Image

src, dst = sys.argv[1], sys.argv[2]
os.makedirs(dst, exist_ok=True)

for name in sorted(os.listdir(src)):
    if not name.endswith('.png'):
        continue
    im = Image.open(os.path.join(src, name)).convert('RGB')
    w, h = im.size
    rgb = im.load()

    def content(x, y):
        r, gg, b = rgb[x, y]
        if (r * 299 + gg * 587 + b * 114) // 1000 < 150:
            return True
        # цветные пиксели — это диаграммы и подсветка, их тоже считаем содержимым
        return max(r, gg, b) - min(r, gg, b) > 40
    right_scan = int(w * 0.68)     # справа водяной знак «Активация Windows»
    limit = h - 80                 # снизу рамка окна и панель задач

    bottom = 0
    for y in range(limit, 0, -1):
        cnt = 0
        for x in range(0, right_scan, 3):
            if content(x, y):
                cnt += 1
                if cnt >= 10:
                    break
        if cnt >= 10:
            bottom = y
            break
    bottom = min(h, max(bottom + 40, 300))

    xmax = 0
    for x in range(int(w * 0.95) - 1, 0, -1):
        cnt = 0
        for y in range(130, bottom, 2):
            if content(x, y):
                cnt += 1
                if cnt >= 3:
                    break
        if cnt >= 3:
            xmax = x
            break
    right = w if xmax > w * 0.55 else min(w, max(xmax + 150, int(w * 0.5)))

    im.crop((0, 0, right, bottom)).save(os.path.join(dst, name))
    print(name, '%dx%d -> %dx%d' % (w, h, right, bottom))
