#!/usr/bin/env python3
"""Symuluje rysunek programu Scratch (ten sam algorytm) i zapisuje PNG."""
import math
import sys
from PIL import Image, ImageDraw

n = int(sys.argv[1]) if len(sys.argv) > 1 else 12
SCALE = 2
W, H = 480 * SCALE, 360 * SCALE

img = Image.new("RGB", (W, H), "white")
draw = ImageDraw.Draw(img, "RGBA")


def to_px(x, y):
    return W / 2 + x * SCALE, H / 2 - y * SCALE


kierunek = 0.0
transparency = 0.0
for i in range(n):
    x, y = 0.0, 0.0
    d = kierunek
    krok = 1.0
    alpha = int(255 * (1 - transparency / 100))
    for _ in range(45):  # ta sama petla co w Scratchu
        nx = x + math.sin(math.radians(d)) * krok
        ny = y + math.cos(math.radians(d)) * krok
        draw.line([to_px(x, y), to_px(nx, ny)],
                  fill=(160, 60, 60, alpha), width=2 * SCALE)
        x, y = nx, ny
        d += 8
        krok += 0.4
    kierunek += 360 / n
    transparency += 75 / n

img.save("scratch/podglad.png")
print("Zapisano scratch/podglad.png")
