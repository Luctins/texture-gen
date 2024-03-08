Texture Generator
------------

"Wallpaper" (as in the image that goes in paper that is glued to a wall) generator, using a 'stamp image' over a larger image, applying random, offsets, rotation and opacity.

# How to use

Example:
```bash
./generate-texture.py -x$((2560*1)) -y$((1080*1)) -d 0.7 -s 0.3 -a 0.8 -m 0.1 --no_stamp_color ./stamp_image.png ./output_image.png
```
