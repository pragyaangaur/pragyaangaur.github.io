"""Copy and compress every picture the board uses into assets/b/.

Still images become WebP no wider than their slot needs. GIFs become short H.264 MP4 loops with a
JPEG poster, which is usually a tenth of the size. Sources stay where they are in each project.
Run from the repository root: python3 tools/media.py
"""

import os
import subprocess
import sys

from PIL import Image, ImageChops, ImageFilter

P = "/Users/pragyaangaur/Claude Code Projects/"
HOME = os.path.expanduser("~/")
PDF = sys.argv[1] if len(sys.argv) > 1 else ""  # folder of images pulled from the LinkedIn export
UP = sys.argv[2] if len(sys.argv) > 2 else ""   # folder of images sent in chat
OUT = "assets/b/"

# name, source, max width, and optionally a crop as fractions (left, top, right, bottom)
STILLS = [
    ("sc-render", UP + "1.png", 1100),
    ("sc-copper", UP + "2.png", 900),
    ("sc-diagram", P + "SkyCatcher Patent/LinkedIn/SkyCatcher_LinkedIn.png", 900),
    ("sc-cad", P + "SkyCatcher Simulations/integration/figures/cad_way1_cutaway.png", 700),
    ("kmc-card", PDF + "img-027.jpg", 800),
    ("setu-poster", P + "IET Project/presentation/linkedin/setu_linkedin.png", 1200),
    ("setu-map", P + "IET Project/docs/figures/02_direction_and_map.png", 900),
    ("mps-wall", PDF + "img-064.jpg", 1000),
    ("mps-counts", "assets/plates/mps.png", 1000),
    ("sun-equations", P + "Mathematics/Math Art/sun.png", 700),
    ("solar-batman", P + "Solar Batman/results/figures/systematics_budget.png", 1000),
    ("token-thermo", P + "Entropy Hallucination Problem/figs/fig7_vocab.png", 1200),
    ("uno-law", P + "Uno/figures/fluid_limit.png", 900),
    ("uno-meme", P + "Uno/submission/linkedin-meme.png", 700),
    ("magnus", PDF + "img-031.jpg", 1000),
    ("polyhex", PDF + "img-041.jpg", 900),
    ("oeis-pair", PDF + "img-036.jpg", 900),
    ("a189077", PDF + "img-036.jpg", 700, (0.555, 0, 1, 1)),  # the A189077 half of the OEIS card
    ("kerf", "tools/sources/kerf-diff.png", 750),
    ("poem", "tools/sources/pulitzer-poem.png", 560),
    ("letter", "tools/sources/pulitzer-letter-crop.png", 760),
    ("polyplets", P + "Mathematics/../Personal Website/assets/plates/polyplets.png", 800),
    ("triking-qb64", PDF + "img-007.jpg", 900),
    ("triking-oeis", PDF + "img-068.jpg", 900),
    ("quill", PDF + "img-009.png", 600, (0, 0, 1, 0.885)),  # drops the video player's 4x badge
    ("inkwell-apps", P + "Kindle Jailbreak/inkwell-screens.png", 800),
    ("bedrock", PDF + "img-015.png", 900),
    ("cellblock", "assets/plates/site-LLM-Stanford-Prison-Experiment.png", 800),
    ("zap-chart", P + "AI Boredom Pain Experiment/crossfire/results/main/fig_hostility_rounds.png", 800),
    ("just-think", P + "AI Boredom Pain Experiment/just-think/results/qwen7b-fp16/figures/fig1_press_rate.png", 700),
    ("residual-tones", P + "AI Boredom Pain Experiment/residual-tones/video/poster.jpg", 700),
    ("horcrux", PDF + "img-048.jpg", 800),
    ("beamline-chamber", PDF + "img-052.jpg", 800),
    ("forkestra", PDF + "img-054.png", 800),
    ("matiks", PDF + "img-055.jpg", 700),
    ("leetcode-1337", PDF + "img-061.jpg", 700),
    ("knight", PDF + "img-020.jpg", 400),
    ("bardly", PDF + "img-058.jpg", 600),
    ("coffee", PDF + "img-067.png", 700),
    ("paperlane", P + "Paperlane/docs/home.png", 800),
    ("skywatch", "assets/plates/site-Skywatch.png", 700),
    ("sunion", "assets/plates/site-Sunion.png", 700),
    ("viscous", P + "Viscosity ML/paper/fig_dichotomy.png", 800),
    ("rdgeneric-pdf", P + "Miniaturised Minecraft/docs/pdf-chromium.png", 800),
]

# Small sources that sit large on the page get a Lanczos upscale and a light sharpen.
UPSCALE = {"sc-render": 2}

# name, source GIF, max width
LOOPS = [
    ("cryoem", P + "Random Stuff/IIT Delhi Lecture Mementos/cryoem.gif", 640),
    ("porosome", P + "Random Stuff/IIT Delhi Lecture Mementos/porosome.gif", 640),
    ("led-doom", P + "Doom LED/docs/gameplay.gif", 640),
    ("rdgeneric", P + "Miniaturised Minecraft/docs/rdgeneric.gif", 600, 9),
    ("knee-deep", P + "Minecraft Doom/docs/gameplay.gif", 640),
    ("fly-brain", P + "Fly Brain LeetCode/media/fly_brain_leetcode.gif", 720),
]


def still(name, src, width, crop=None):
    im = Image.open(src)
    if crop:
        l, t, r, b = crop
        im = im.crop((round(l * im.width), round(t * im.height), round(r * im.width), round(b * im.height)))
    im = im.convert("RGBA" if im.mode in ("RGBA", "LA", "P") else "RGB")
    if src.startswith(UP) and UP:
        # Pictures sent in chat arrive on a grey matte. Crop to where the picture differs from it.
        rgb = im.convert("RGB")
        grey = Image.new("RGB", im.size, rgb.getpixel((im.width - 2, im.height - 2)))
        box = ImageChops.difference(rgb, grey).convert("L").point(lambda v: 255 if v > 18 else 0).getbbox()
        if box:
            im = im.crop(box)
    if name in UPSCALE:
        k = UPSCALE[name]
        im = im.resize((im.width * k, im.height * k), Image.LANCZOS).filter(ImageFilter.UnsharpMask(radius=2, percent=60, threshold=2))
    if im.width > width:
        im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    im.save(OUT + name + ".webp", "WEBP", quality=84, method=6)
    return im.size


def loop(name, src, width, seconds=None):
    scale = f"scale='min({width},iw)':-2:flags=lanczos"
    trim = ["-t", str(seconds)] if seconds else []
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *trim, "-i", src, "-vf", scale + ",format=yuv420p",
                    "-c:v", "libx264", "-preset", "slow", "-crf", "28", "-movflags", "+faststart", "-an",
                    OUT + name + ".mp4"], check=True)
    # The poster comes from a third of the way in, because several loops start on a black frame.
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                                OUT + name + ".mp4"], capture_output=True, text=True).stdout or 0)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{dur / 3:.2f}", "-i", OUT + name + ".mp4", "-frames:v", "1",
                    "-q:v", "4", OUT + name + ".jpg"], check=True)
    w, h = Image.open(OUT + name + ".jpg").size
    return w, h


def cone():
    # Fourteen seconds of the Manim explainer for the Cauchy-Schwarz paper, where the point moves into the
    # cone of positive semidefinite matrices, with the caption strip cropped off.
    src = P + "Mathematics/Principia Math/Fall Competition/exposition/video/real_power_cauchy_schwarz.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", "262", "-t", "14", "-i", src, "-vf",
                    "crop=iw:ih*0.74:0:0,scale=720:-2:flags=lanczos,format=yuv420p", "-c:v", "libx264", "-preset", "slow",
                    "-crf", "28", "-an", "-movflags", "+faststart", OUT + "cauchy-cone.mp4"], check=True)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", "10", "-i", OUT + "cauchy-cone.mp4", "-frames:v", "1",
                    "-q:v", "4", OUT + "cauchy-cone.jpg"], check=True)
    return Image.open(OUT + "cauchy-cone.jpg").size


def main():
    os.makedirs(OUT, exist_ok=True)
    sizes = {}
    for name, src, width, *crop in STILLS:
        sizes[name] = still(name, src, width, *crop)
    for name, src, width, *rest in LOOPS:
        sizes[name] = loop(name, src, width, *rest)
    sizes["cauchy-cone"] = cone()
    with open(OUT + "sizes.txt", "w") as f:
        for k, (w, h) in sizes.items():
            f.write(f"{k} {w} {h}\n")
    total = sum(os.path.getsize(OUT + f) for f in os.listdir(OUT))
    print(f"{len(sizes)} items, {total / 1e6:.1f} MB in {OUT}")


if __name__ == "__main__":
    main()
