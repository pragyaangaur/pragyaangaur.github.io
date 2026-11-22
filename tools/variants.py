"""Make smaller copies of each board picture for srcset: name-480.webp and name-800.webp.

A copy is only made when the original is clearly wider than it, so small pictures get none.
build.py reads the same widths, so change them in one place. Run from the repository root:
python3 tools/variants.py
"""

import glob
import os

from PIL import Image

WIDTHS = (480, 800)


def make(path):
    """Write the smaller copies of one picture and return the widths that now exist for it."""
    base = path[:-5]
    im = Image.open(path)
    made = []
    for w in WIDTHS:
        if im.width > w * 1.2:
            im.resize((w, round(im.height * w / im.width)), Image.LANCZOS).save(f"{base}-{w}.webp", "WEBP", quality=82, method=6)
            made.append(w)
    return made


if __name__ == "__main__":
    for p in sorted(glob.glob("assets/b/*.webp")):
        if not p[:-5].endswith(tuple(f"-{w}" for w in WIDTHS)):
            print(os.path.basename(p), make(p))
