#!/usr/bin/env python3
"""Symuluje rysunek programu Scratch (ten sam algorytm) i zapisuje PNG."""
import math
import sys
from PIL import Image, ImageDraw

n = int(sys.argv[1]) if len(sys.argv) > 1 else 8
SCALE = 2
W, H = 480 * SCALE, 360 * SCALE

img = Image.new("RGB", (W, H), "white")
draw = ImageDraw.Draw(img, "RGBA")

x = y = 0.0
d = 0.0
pen = False
color = (160, 60, 60, 255)


def to_px(px_, py_):
    return W / 2 + px_ * SCALE, H / 2 - py_ * SCALE


def move(steps):
    global x, y
    nx = x + math.sin(math.radians(d)) * steps
    ny = y + math.cos(math.radians(d)) * steps
    if pen:
        draw.line([to_px(x, y), to_px(nx, ny)], fill=color, width=2 * SCALE)
    x, y = nx, ny


def turn(deg):
    global d
    d += deg


kierunek = 0.0
transparency = 0.0
for i in range(n):
    x, y = 0.0, 0.0
    d = kierunek
    color = (160, 60, 60, int(255 * (1 - transparency / 100)))
    pen = True
    for _ in range(36):           # duzy luk (kopula)
        move(6); turn(5)
    turn(180)                     # zawrot
    for _ in range(36):           # prawy maly garb
        move(3); turn(-5)
    turn(180)                     # zawrot w dziobku
    for _ in range(36):           # lewy maly garb
        move(3); turn(-5)
    pen = False
    kierunek += 360 / n
    transparency += 75 / n

img.save("scratch/podglad.png")
print("Zapisano scratch/podglad.png")
