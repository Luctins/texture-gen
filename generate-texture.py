#!/bin/env python

import sys
import random
import PIL
from PIL import Image, ImageChops

import argparse
from random import randint


parser = argparse.ArgumentParser(
    prog="texture generator",
    description="Semi-random texture generator"
)

# -----------------------------------------------------------------------------
# Arg""s

parser.add_argument("stamp_image")
parser.add_argument("output_file")

parser.add_argument("-l", "--light", action="store_true")
parser.add_argument("--no_stamp_color", action="store_true")

parser.add_argument("-x", "--width", default=2560, type=int)
parser.add_argument("-y", "--height", default=1080, type=int)
parser.add_argument("-a", "--stamp_alpha", default=0.7, type=float)
parser.add_argument("-s", "--stamp_scale", default=0.5, type=float)
parser.add_argument("-d", "--density", default=0.9, type=float)

args = parser.parse_args()

print(args)

# -----------------------------------------------------------------------------
# base textures

texture = Image.open(args.stamp_image).convert('RGBA')

# split alpha and multiply it by value
r, g, b, a = texture.split()
a = a.point(lambda i: i * args.stamp_alpha)

texture = Image.merge(
    'RGBA',
    (r, g, b, a) if not args.no_stamp_color else (a, a, a, a)
)

texture_size = (
    int(texture.size[0] * args.stamp_scale),
    int(texture.size[1] * args.stamp_scale)
)

# -----------------------------------------------------------------------------
# canvas
base_color = 255 if args.light else 0
canvas = Image.new(
    "RGBA",
    (args.width, args.height),
    (base_color, base_color, base_color, 255)
)

# -----------------------------------------------------------------------------
# Loop parameters

stamp_w = texture_size[0]
stamp_h = texture_size[1]

hofs_max = int( (stamp_h / 2) * 0.5)
vofs_max = int( (stamp_w / 2) * 0.5)

# these 2 depend on each other because otherwise there's no overlap between
# stamp images
h_step = int(stamp_h * args.density)
v_step = int(stamp_w * args.density)

v_max = args.width
h_max = args.height

print("image size:", texture.size, "mode", texture.mode, "canvas size:",
      canvas.size, "mode", canvas.mode)
print("step:", h_step, v_step);

def random_opacity(image, maxo, mino, monochrome=False):
    _, _, _, a = image.split()
    a = a.point(lambda i: i * (mino + maxo * random.random()))
    return Image.merge('RGBA', (a, a, a, a))


for v in range(0, int(v_max), v_step):
    sys.stdout.write(f"\r{100.0*v/v_max:2.1f} %")
    sys.stdout.flush()

    for h in range(0, int(h_max), h_step):
        # print(v, h)
        v_pos = v + randint(-vofs_max, vofs_max)
        h_pos = h + randint(-hofs_max, hofs_max)
        rotation = random.random() * 360.0
        scale = 0.7 + random.random() * 0.3

        texture_alpha = random_opacity(texture, 0.4, 0.8, args.no_stamp_color)

        rot_texture = texture_alpha \
        .rotate(rotation) \
        .resize((int(texture_size[0] * scale), int(texture_size[1] * scale)))

        # canvas = ImageChops.multiply(canvas, rot_texture)
        canvas.alpha_composite(rot_texture, (v_pos, h_pos))

canvas.save(args.output_file)
print("\ndone")
