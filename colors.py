#!/usr/bin/env python

import os
import sys
import shutil

from PIL import Image

from kmeans import kmeans, Point


def get_points(img: Image.Image) -> list[Point]:
    w, h = img.size
    return [Point(color, 3, count) for count, color in img.getcolors(w * h)]


def rgb_to_hex(rgb: list[int]) -> str:
    hex_val = "".join(f"{int(p):02x}" for p in rgb)
    return f"#{hex_val}"


def extract_colors(filename: str, n: int = 3) -> list[list[int]]:
    img = Image.open(filename)
    img.thumbnail((100, 100))
    w, h = img.size

    points = get_points(img)
    clusters = kmeans(points, n)
    return [c.center.coords for c in clusters]


def generate_output(image_height_px: int, num_colors: int, colors: list[str]):
    swatch_height = image_height_px / num_colors
    swatch_width = swatch_height / 1.618

    print(
        f"""
<!DOCTYPE html>
<html>
    <head>
        <style>
            li{{width:{swatch_width}px;height:{swatch_height}px;}}
            img{{float:left;height:{image_height_px}px;}}
            ul{{float:left;list-style:none;margin:0px;padding:0px;}}
        </style>
    </head>
    <body>
        <ul>
"""
    )

    for color in colors:
        print(f'<li style="background: {color};"></li>')

    print("</ul>")
    print(f'<img src="{copied_image_filename}" />')
    print("</body></html>")


def human_perception(color: list[int]) -> float:
    return (color[0] * 299 + color[1] * 587 + color[2] * 114) / 1000


def check_usage():
    if len(sys.argv) != 4:
        sys.exit("Usage: colors.py <image> <num colors> <image display height in px>")


if __name__ == "__main__":
    check_usage()

    filename, ext = sys.argv[1].split(".")
    num_colors = int(sys.argv[2])
    image_height_px = int(sys.argv[3])

    copied_image_filename = f"{os.path.basename(filename)}.copy.{ext}"
    shutil.copyfile(f"{filename}.{ext}", copied_image_filename)

    colors = extract_colors(copied_image_filename, n=num_colors)
    colors = sorted(colors, key=human_perception, reverse=True)
    hex_colors = [rgb_to_hex(color) for color in colors]
    generate_output(image_height_px, num_colors, hex_colors)
