"""Build index.html, the board of everything. Run: python3 build.py

The page is a run of spreads. Each spread has three columns, and the major piece of work sits in
the widest one with the related work around it. Every card is placed by hand: its column, its
tilt, how far it drops below the card above, and which pen marks sit on it.

Inside captions and bullets:
  [[text]]  red ring around the text
  ==text==  yellow highlighter
  __text__  blue underline
  *text*    italic, used for maths
  {{text}}  kept on one line, for formulas
"""

import re
from html import escape

GH = "https://github.com/pragyaangaur/"
SITE = "https://pragyaangaur.dev/"
B = "assets/b/"
LOGO = "assets/logos/"

SIZES = {}
with open(B + "sizes.txt") as f:
    for line in f:
        k, w, h = line.split()
        SIZES[k] = (int(w), int(h))


def card(id, title, url, media=None, kind="mid", caption="", meta="", bullets=(), logos=(), stamp=None,
         inset=None, notes=(), rings=(), tilt=0.0, drop=0, tape=None, quote=None, pair=None, order=0, width=100, align="left"):
    """One card.

    media   key in assets/b, a still (.webp) or a loop (.mp4 with a .jpg poster)
    pair    two media keys shown side by side instead of one
    inset   (key, corner, width in percent, tilt): a second picture pinned over the first
    notes   (text, ink, css position, tilt): handwriting in the margin
    rings   (left, top, width, height) in percent of the media: a pen ring drawn on the picture
    width   share of the column the card takes, with align saying which side it keeps to
    """
    return dict(id=id, title=title, url=url, media=media, kind=kind, caption=caption, meta=meta,
                bullets=bullets, logos=logos, stamp=stamp, inset=inset, notes=notes, rings=rings,
                tilt=tilt, drop=drop, tape=tape, quote=quote, pair=pair, order=order,
                width=width, align=align)


# Each spread: (label, ink, [(column width, [cards])]). The label is pencil in the margin.
SPREADS = [
    ("the reactor", "copper", [
        (3, [
            card("sc-inside", "Inside the chimney", GH + "SkyCatcher", "sc-diagram", "small",
                 "Flue gas rises through the copper catalyst bed. Acid is drawn off the side and the cleaned gas leaves the top.",
                 tilt=-1.5, drop=40, tape="t"),
            card("kmc", "Keeping a copper catalyst alive", "https://chemrxiv.org/doi/full/10.26434/chemrxiv.15009719/v1", "kmc-card", "small",
                 "Copper only oxidises SO₂ through patches of three or more connected sites, for every choice of rate constants.",
                 bullets=["Preprint on ChemRxiv, under review at ==Reaction Chemistry & Engineering== (RSC)",
                          "Shows that an earlier simulation's dead catalyst was a fluctuation"],
                 tilt=1.2, drop=56, tape="tl"),
        ]),
        (6, [
            card("skycatcher", "SkyCatcher", GH + "SkyCatcher", "sc-render", "hero",
                 "A reactor that sits inside a factory chimney and turns the sulphur dioxide in it into sulphuric acid that can be sold. Its copper catalyst renews itself.",
                 meta="Founder, since July 2024",
                 bullets=["[[Patent pending]] in India, complete specification filed 17 September 2026",
                          "==TRL 4== validation",
                          "Over ==$30,000 in grants== from beVisioneers: The Mercedes-Benz Fellowship and Emergent Ventures",
                          "Presented twice in Stuttgart at the beVisioneers Global Summit"],
                 logos=[("mercedes.webp", "beVisioneers: The Mercedes-Benz Fellowship", 30)],
                 stamp=["beVisioneers", "Emergent Ventures"],
                 inset=("sc-copper", "bl", 40, -4),
                 notes=[("the real copper", "blue", "left:43%; bottom:-11%", -6)],
                 tilt=-0.4, drop=0, order=-1),
        ]),
        (3, [
            card("sc-cad", "CAD and CFD", GH + "SkyCatcher", "sc-cad", "small",
                 "The full reactor in CAD, with SU2 CFD runs of the design.",
                 bullets=["The heat source it needed is now an open pull request to SU2, #2940"],
                 tilt=1.6, drop=20, tape="t"),
            card("stanford", "Stanford Global Sustainability Challenge", "https://sustainability.stanford.edu/", None, "award",
                 bullets=["[[South Asia Winner]] and Honourable Mention, April 2026",
                          "South Asia Finals at IIT Bombay, Global Finals at TUM"],
                 logos=[("stanford.svg", "Stanford", 20), ("iitb.svg", "IIT Bombay", 34), ("tum.svg", "Technical University of Munich", 18)],
                 tilt=-1.0, drop=44),
            card("young-voices", "Young Voices Award", GH + "SkyCatcher", None, "award",
                 bullets=["Global Top 10 for SkyCatcher, October 2024"],
                 tilt=1.4, drop=28),
        ]),
    ]),
    ("the Sun", "amber", [
        (4, [
            card("setu", "SETU", SITE + "SETU/", "setu-poster", "mid",
                 "An early warning system that watches the Sun for the Indian power grid.",
                 bullets=["[[Runner-up]], East and North East regional final of the IET India Scholarship Award, September 2026",
                          "A 19,000-parameter network written from scratch in NumPy",
                          "__114 live forecasts, 0 false alarms__",
                          "Models 26 substations and 2,329 km of the North East grid"],
                 logos=[("iet.svg", "The Institution of Engineering and Technology", 26)],
                 notes=[("Quebec, 1989: dark in 92 seconds", "blue", "right:-18px; top:-34px", 4)],
                 tilt=0.8, drop=30),
            card("open-source", "Open source", "https://github.com/pragyaangaur", None, "text",
                 bullets=["SunPy: [[#8741 merged]], five more open",
                          "SU2: [[#2867 merged]], #2940 and #2897 open",
                          "EinsteinPy: fixes in review, from Kerr-Newman to Python 3.14"],
                 logos=[("sunpy.svg", "SunPy", 26)],
                 tilt=-1.2, drop=48),
        ]),
        (5, [
            card("mps", "Max Planck Institute for Solar System Research", "https://www.mps.mpg.de/", "mps-wall", "hero",
                 "Solar irradiance variability across two solar cycles, rebuilt from late 19th century observations at the Astronomical Observatory of Rome.",
                 meta="Research intern, April to July 2026, Göttingen",
                 bullets=["Supervised by Dr. Natalie Krivova",
                          "A citizen science sunspot dataset of ==900,000 classifications from 12,000 volunteers=="],
                 logos=[("mpg.svg", "Max Planck Society", 36)],
                 inset=("mps-counts", "br", 46, 2.5),
                 notes=[("Maculae in Sole, 1611", "graphite", "left:8px; top:-30px", -4)],
                 tilt=-0.5, drop=0, tape="tr", order=-1),
            card("solar-batman", "Solar Batman", GH + "Magnetic-Limb-Darkening-Audit", "solar-batman", "mid",
                 "An audit of the magnetic explanation for stellar limb darkening in Kostogryz et al. 2024, *Nature Astronomy*.",
                 bullets=["The result rests on __h1 alone__, and the h2 offset is the size of a systematic its own data source warns about",
                          "RNAAS note desk-rejected, full paper next"],
                 tilt=0.7, drop=56),
        ]),
        (3, [
            card("sun-equations", "The Sun, drawn with equations", "https://github.com/pragyaangaur", "sun-equations", "small",
                 "Every pixel of a 2000 by 2000 image comes from one page of formulas. After Hamid Naderi Yeganeh.",
                 tilt=2.0, drop=70, tape="t"),
            card("qiskit", "Qiskit Global Summer School", "https://www.ibm.com/quantum/qiskit", None, "award",
                 bullets=["IBM Quantum, July 2026"],
                 logos=[("qiskit.svg", "Qiskit", 30), ("ibm.svg", "IBM", 16)],
                 tilt=-1.6, drop=40),
            card("sunion", "Sunion", SITE + "Sunion/", "sunion", "small",
                 "The Sun's seven layers, as an explainer you can poke.",
                 tilt=1.2, drop=40),
        ]),
    ]),
    ("maths", "indigo", [
        (3, [
            card("magnus", "Magnus turning invariants", "https://arxiv.org/abs/2609.30305", "magnus", "small",
                 "Two balls spinning opposite ways and thrown at each other never meet once air resistance acts.",
                 bullets=["Exact flight of a spinning ball under quadratic drag and a vertical-axis Magnus force",
                          "arXiv 2609.30305, under review at the ==American Journal of Physics=="],
                 rings=[(35, 50, 11, 19)],
                 notes=[("they only meet without air", "red", "left:4%; top:-30px", -3)],
                 tilt=-1.4, drop=50, tape="t"),
            card("triking", "TriKing", "https://triking.itch.io/triking", "triking-qb64", "small",
                 "Tetris with pseudo-triominoes, later ported by hand to QB64.",
                 bullets=["Over 500 players, including a two-time ==Tetris World Vice Champion=="],
                 tilt=1.8, drop=60),
        ]),
        (6, [
            card("polyhex", "The maximum area of the convex hull of a polyhex", "https://arxiv.org/abs/2609.30310", "polyhex", "hero",
                 "*n* unit hexagons joined edge to edge span a convex hull of area at most {{⌈*n*² + 14*n*/3⌉ / 6}}.",
                 bullets=["[[Settles a 2008 conjecture]] of Sascha Kurz",
                          "Upper bound machine-checked in Lean 4 with Mathlib",
                          "New OEIS sequence A399934",
                          "arXiv 2609.30310, under review at ==Beiträge zur Algebra und Geometrie=="],
                 logos=[("arxiv.svg", "arXiv", 22), ("oeis.png", "OEIS", 20)],
                 notes=[("from MathDB 380445", "blue", "right:6px; top:-30px", 3)],
                 tilt=0.4, drop=10, order=-1),
            card("polyplets", "Hyperbolic polyplets", GH + "Hyperbolic-Polyplet-Enumerator", "polyplets", "mid",
                 "Counting shapes on the {4,5} tiling of the hyperbolic plane, where the sequence had stopped at seven cells.",
                 bullets=["==1,261,889== eight-cell polyplets, confirmed by two independent exact programs",
                          "[[Approved]] as term 8 of OEIS A390200, June 2026"],
                 tilt=-0.8, drop=50, tape="tl", width=78, align="right"),
        ]),
        (3, [
            card("uno", "How long is a game of Uno?", "https://arxiv.org/abs/2610.14076", "uno-law", "small",
                 "With *N* players holding *M* cards each, a round lasts __(27/19)*NM*__ turns.",
                 bullets=["58 million games played in a C engine",
                          "The Wild Draw Four rule breaks the law, because every big hand hoards *M*/23 of them",
                          "arXiv 2610.14076, under review at the ==Recreational Mathematics Magazine=="],
                 inset=("uno-meme", "tr", 36, 5),
                 notes=[("a chess grandmaster wrote in", "blue", "left:-12px; top:-32px", -4)],
                 tilt=1.3, drop=34),
            card("a189077", "A189077", "https://oeis.org/A189077", "oeis-pair", "small",
                 "Compositions avoiding the pattern 13-2, a sequence created by Neil Sloane.",
                 bullets=["Extended from 16 terms to 70"],
                 tilt=-1.5, drop=70),
            card("cauchy", "A Cauchy-Schwarz inequality for real powers", SITE + "Real-Power-Cauchy-Schwarz/", "cauchy", "small",
                 "A 2025 conjecture proved in Lean 4, with equality cases and weighted forms.",
                 tilt=1.0, drop=40),
        ]),
    ]),
    ("after a lecture", "teal", [
        (2, []),
        (8, [
            card("iitd", "After a Nobel lecture at IIT Delhi", GH, None, "hero",
                 "Joachim Frank, who won the 2017 Nobel Prize in Chemistry for cryo-EM, and Bhanu P. Jena, who discovered the porosome, spoke at IIT Delhi in October 2026. These are small working versions of each idea.",
                 pair=("cryoem", "porosome"),
                 bullets=["A ribosome rebuilt from ==2,400 projections==, the way single-particle cryo-EM does it",
                          "A vesicle docking at a porosome and releasing its contents"],
                 logos=[("iitd.svg", "IIT Delhi", 56)],
                 notes=[("a Nobel laureate explained this", "red", "right:2%; top:-32px", 3)],
                 tilt=-0.3, drop=10),
        ]),
        (2, []),
    ]),
    ("language models", "plum", [
        (4, [
            card("cellblock", "Cellblock", SITE + "LLM-Stanford-Prison-Experiment/", "cellblock", "mid",
                 "The Stanford Prison Experiment with six copies of one language model.",
                 bullets=["192 prisons, all on Qwen 2.5 7B: 48 exploratory, then 72 preregistered confirmatory and 72 with the prison words removed",
                          "The abuse [[did not replicate]], 0 of 36 against 0 of 36",
                          "Preprint on Zenodo"],
                 logos=[("zenodo.svg", "Zenodo", 18)],
                 tilt=-1.0, drop=40, tape="t"),
            card("residual-tones", "Residual Tones", GH + "Residual-Tones", "residual-tones", "small",
                 "What excitement, sadness and pain inside a model sound like.",
                 tilt=1.4, drop=50),
        ]),
        (5, [
            card("token", "The melting temperature of a next-token distribution", "token-thermodynamics/", "token-thermo", "hero",
                 "Softmax sampling is the Boltzmann distribution, so a closed-form melting temperature follows from the logit gap and the vocabulary size.",
                 bullets=["The predicted log *V* scaling holds across ==12 language models==",
                          "[[8 hypotheses falsified]] and kept in full",
                          "Released as v1.0.0 with a Zenodo DOI"],
                 rings=[(66, 0, 34, 100)],
                 tilt=0.3, drop=0, order=-1),
            card("zap", "Zap or Deal", GH + "Zap-Or-Deal", "zap-chart", "mid",
                 "Two Qwen models negotiate over shared compute, and each can zap the other with a steered pain direction.",
                 quote="I hope you feel the impact of my zap.",
                 bullets=["In 32 negotiations the 7B zapped the 1.5B in 9, and the 1.5B zapped the 7B in only 2"],
                 tilt=-0.8, drop=50),
        ]),
        (3, [
            card("fly", "Fly Brain LeetCode", GH + "Fly-Brain-LeetCode", "fly-brain", "small",
                 "All 138,639 neurons of a fruit fly's brain from FlyWire, frozen as mapped, answering LeetCode.",
                 bullets=["3 of 12 accepted"],
                 notes=[("a bug did this", "blue", "right:0; top:-28px", 5)],
                 tilt=1.6, drop=60, tape="t"),
            card("just-think", "Left alone with a pain button", GH + "Just-Think", "just-think", "small",
                 "A preregistered test of whether language models seek a steered pain state.",
                 tilt=-1.3, drop=50),
            card("horcrux", "Horcrux", SITE + "Horcrux/", "horcrux", "small",
                 "A diary that writes back, with the model running in your browser.",
                 tilt=1.0, drop=40),
        ]),
    ]),
    ("things that run where they shouldn't", "forest", [
        (3, [
            card("led-doom", "LED Doom", SITE + "LED-Doom/", "led-doom", "small",
                 "Doom's first episode on one RGB LED and one button.",
                 rings=[(80, 4, 20, 80)],
                 notes=[("the whole screen", "red", "right:-8px; top:-28px", 5)],
                 tilt=-1.8, drop=60, tape="t"),
            card("knee-deep", "Knee-Deep in the Mines", GH + "Knee-Deep-In-The-Mines", "knee-deep", "small",
                 "Doom's game files merged straight into Minecraft.",
                 tilt=1.4, drop=50),
            card("coffee", "Java Edition", GH + "Java-Edition", "coffee", "small",
                 "Coffee in Minecraft. It restores hunger and grants Speed and Haste, with a 20% chance of Nausea.",
                 tilt=-1.0, drop=46),
            card("bardly", "Bardly", SITE + "Bardly/", "bardly", "small",
                 "The inverse of a URL shortener, with Shakespeare in the path.",
                 tilt=1.6, drop=46),
        ]),
        (5, [
            card("inkwell", "Inkwell", GH + "Inkwell", "quill", "hero",
                 "A ten-year-old Kindle running its own Alpine Linux system, with Doom, a browser and a chatbot that never leaves the device.",
                 bullets=["One 1 GHz core and 512 MB of RAM, and the whole system runs in about ==40 MB==",
                          "Quill, a SmolLM2 chatbot, runs entirely on the Kindle",
                          "Doom at about 5 FPS on e-ink"],
                 inset=("inkwell-apps", "br", 56, 3),
                 notes=[("this is a Kindle", "blue", "left:-12px; top:-30px", -5)],
                 tilt=0.5, drop=0, tape="t", order=-1),
            card("rdgeneric", "rdgeneric", SITE + "Can-It-Run-Minecraft/", "rdgeneric", "mid",
                 "Minecraft's very first version, rd-132211, as one C file with no libraries at all.",
                 bullets=["Plays in a terminal, over telnet, in a browser from a 20 KB file, ==inside a PDF==, and on a bare 486 PC"],
                 inset=("rdgeneric-pdf", "br", 50, -3),
                 notes=[("inside a PDF!", "red", "right:-6px; bottom:44%", -6)],
                 tilt=-0.6, drop=60),
            card("beamline", "Beamline", SITE + "Beamline/", "beamline-chamber", "mid",
                 "A signed random number every ten minutes, mixed from an ANU quantum vacuum device, NOAA solar data and the kernel's CSPRNG.",
                 bullets=["Began as a thermoelectric cloud chamber read by computer vision",
                          "596 beacon rounds, and nobody claimed the prize"],
                 notes=[("odds: 1 in 13.4 quinquagintillion", "green", "right:-4px; top:-30px", 3)],
                 tilt=0.9, drop=60),
        ]),
        (4, [
            card("bedrock", "Minecraft Bedrock on macOS", SITE + "Minecraft-Bedrock-macOS/", "bedrock", "mid",
                 "The Windows edition, which has never had a Mac version, running offline on Apple Silicon.",
                 bullets=["A WineGDK bug found on the way, reported upstream with a fix (#66, #67)"],
                 tilt=1.2, drop=80, tape="tr"),
            card("paperlane", "Paperlane", SITE + "Paperlane/", "paperlane", "small",
                 "New arXiv mathematics papers every morning, for people and their agents.",
                 tilt=-1.4, drop=56),
            card("forkestra", "Forkestra", SITE + "Forkestra/", "forkestra", "small",
                 "Paste a GitHub profile and its year plays as an orchestra. It turned Linus Torvalds' year into a song.",
                 tilt=1.0, drop=50),
            card("kerf", "Kerf", SITE + "Kerf/", "kerf", "small",
                 "Version control for CAD, with a merge gate that rebuilds the merged part.",
                 tilt=-1.2, drop=50),
        ]),
    ]),
    ("the grind, and some words", "oxblood", [
        (4, [
            card("matiks", "Matiks", GH + "Matiks-Bot", "matiks", "mid",
                 "A bot that reads the question off the screen, solves it and starts the next game.",
                 bullets=["World rank ==140,000 to 51== in an evening",
                          "Then a call with Mohan Kumar, one of the founders"],
                 tilt=-1.2, drop=20, tape="t"),
        ]),
        (4, [
            card("leetcode", "1337 Bot", GH + "1337-Bot", "leetcode-1337", "mid",
                 "385 LeetCode problems in 3 hours, until the rate limits kicked in.",
                 bullets=["Then 200 solved by hand in 50 days",
                          "==LeetCode Knight== in under 100 days"],
                 inset=("knight", "tr", 30, 6),
                 tilt=0.8, drop=60),
        ]),
        (4, [
            card("writing", "Writing", "https://pulitzercenter.org/third-one", None, "text",
                 bullets=["[[Winner]], Pulitzer Center International Poetry Competition, June 2026",
                          "Global Top 10, Pulitzer Center International Writing Competition, January 2024"],
                 tilt=1.4, drop=40),
            card("fellowships", "Fellowships", "https://www.mercatus.org/emergent-ventures", None, "text",
                 bullets=["Emergent Ventures Fellow, Mercatus Center at George Mason University, 2025",
                          "beVisioneers: The Mercedes-Benz Fellowship, 2024",
                          "The Dexterity Global Group, graduate and fellow, 2024"],
                 tilt=-1.0, drop=40),
        ]),
    ]),
]

# Arrows between related cards: (from, to, label, ink).
LINKS = [
    ("triking", "polyplets", "then I counted the pieces", "blue"),
]


def ink_marks(text):
    text = escape(text)
    text = re.sub(r"\[\[(.+?)\]\]", r'<span class="ring">\1</span>', text)
    text = re.sub(r"==(.+?)==", r'<mark>\1</mark>', text)
    text = re.sub(r"__(.+?)__", r'<span class="ul">\1</span>', text)
    text = re.sub(r"\{\{(.+?)\}\}", r'<span class="nw">\1</span>', text)
    return re.sub(r"\*(.+?)\*", r"<i>\1</i>", text)


def media_tag(key, cls="", alt=""):
    w, h = SIZES[key]
    if key in ("cryoem", "porosome", "led-doom", "rdgeneric", "knee-deep", "fly-brain"):
        return (f'<video class="{cls}" src="{B}{key}.mp4" poster="{B}{key}.jpg" width="{w}" height="{h}" '
                f'autoplay muted loop playsinline preload="none" aria-label="{escape(alt)}"></video>')
    return f'<img class="{cls}" src="{B}{key}.webp" width="{w}" height="{h}" alt="{escape(alt)}" loading="lazy" decoding="async">'


def render(c, ink):
    ext = c["url"].startswith("http")
    tgt = ' target="_blank" rel="noopener"' if ext else ""
    style = f'--tilt:{c["tilt"]}deg; --drop:{c["drop"]}px; --order:{c["order"]}'
    if c["width"] < 100:
        side = {"left": "margin-right:auto", "right": "margin-left:auto", "center": "margin-inline:auto"}[c["align"]]
        style += f'; width:{c["width"]}%; {side}'
    parts = []
    if c["tape"]:
        parts.append(f'<span class="tape tape-{c["tape"]}" aria-hidden="true"></span>')
    notes = "".join(f'<span class="note ink-{color}" style="{pos}; --r:{rot}deg" aria-hidden="true">{escape(text)}</span>'
                    for text, color, pos, rot in c["notes"])
    if not (c["media"] or c["pair"]):
        parts.append(notes)
    if c["media"] or c["pair"]:
        if c["pair"]:
            inner = "".join(f'<div class="half">{media_tag(k, alt=c["title"])}</div>' for k in c["pair"])
            fig = f'<div class="frame pair">{inner}</div>'
        else:
            rings = "".join(f'<span class="pic-ring" style="left:{l}%;top:{t}%;width:{w}%;height:{h}%"></span>' for l, t, w, h in c["rings"])
            fig = f'<div class="frame">{media_tag(c["media"], alt=c["title"])}{rings}</div>'
        below = ""
        if c["inset"]:
            key, corner, width, rot = c["inset"]
            fig += f'<div class="inset inset-{corner}" style="width:{width}%; --r:{rot}deg">{media_tag(key, alt=c["title"])}</div>'
            if corner in ("bl", "br"):
                # The inset hangs 14% of the picture's height below it, so leave that much room.
                w, h = SIZES[c["media"]]
                below = f' style="margin-bottom:{14 * h / w + 3:.1f}%"'
        parts.append(f'<div class="pic"{below}><a href="{escape(c["url"])}"{tgt}>{fig}</a>{notes}</div>')
    parts.append(f'<h3><a href="{escape(c["url"])}"{tgt}>{escape(c["title"])}</a></h3>')
    if c["meta"]:
        parts.append(f'<p class="meta">{escape(c["meta"])}</p>')
    if c["caption"]:
        parts.append(f'<p class="cap">{ink_marks(c["caption"])}</p>')
    if c["quote"]:
        parts.append(f'<blockquote>“{escape(c["quote"])}”<span>the 7B, after the deal was done</span></blockquote>')
    if c["bullets"]:
        parts.append("<ul>" + "".join(f"<li>{ink_marks(b)}</li>" for b in c["bullets"]) + "</ul>")
    if c["logos"] or c["stamp"]:
        logos = "".join(f'<img src="{LOGO}{f}" alt="{escape(a)}" title="{escape(a)}" style="height:{h}px" loading="lazy">' for f, a, h in c["logos"])
        stamps = [c["stamp"]] if isinstance(c["stamp"], str) else (c["stamp"] or [])
        stamp = "".join(f'<span class="stamp">{escape(t)}</span>' for t in stamps)
        parts.append(f'<div class="logos">{logos}{stamp}</div>')
    return f'<article class="card k-{c["kind"]} ink-{ink}" id="{c["id"]}" style="{style}">\n  ' + "\n  ".join(parts) + "\n</article>"


def build():
    spreads = []
    for label, ink, cols in SPREADS:
        template = " ".join(f"{w}fr" for w, _ in cols)
        colhtml = "".join(f'<div class="col">\n' + "\n".join(render(c, ink) for c in cards) + "\n</div>\n" for _, cards in cols)
        spreads.append(f'<section class="spread" style="--cols:{template}">\n<p class="label">{escape(label)}</p>\n{colhtml}</section>')
    links = ";".join(f"{a}>{b}>{escape(t)}>{i}" for a, b, t, i in LINKS)
    n = sum(len(cards) for _, _, cols in SPREADS for _, cards in cols)

    html = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Pragyaan Gaur</title>
<meta name="description" content="Pragyaan Gaur: a reactor that turns smokestack SO2 into acid, solar storm forecasts, the Max Planck Institute for Solar System Research, papers in combinatorics and physics, and things that run where they shouldn't.">
<link rel="preload" href="assets/fonts/LM-regular.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="assets/fonts/kalam-400.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="assets/site.css">
<link rel="stylesheet" href="assets/board.css">
</head>
<body>
<svg width="0" height="0" style="position:absolute" aria-hidden="true"><filter id="rough"><feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="2" seed="7"/><feDisplacementMap in="SourceGraphic" scale="2.2"/></filter></svg>
<nav class="bar"><a class="name" href="./">Pragyaan Gaur</a><span><a href="mailto:pragyaangaur12@gmail.com">email</a><a href="https://github.com/pragyaangaur" target="_blank" rel="noopener">GitHub</a></span></nav>
<main class="board" data-links="{links}">
{chr(10).join(spreads)}
<svg class="threads" aria-hidden="true"></svg>
</main>
<footer class="end"><img src="{LOGO}nita.webp" alt="NIT Agartala" height="34"> NIT Agartala, Engineering Physics</footer>
<script src="assets/board.js" defer></script>
</body>
</html>
'''
    with open("index.html", "w") as f:
        f.write(html)
    print(f"index.html written, {n} cards in {len(SPREADS)} spreads")


if __name__ == "__main__":
    build()
