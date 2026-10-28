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


# Each spread: (id, heading, ink, [(column width, [cards])]). A column with no cards is breathing room.
SPREADS = [
    ("reactor", "The reactor", "copper", [
        (3, [
            card("sc-inside", "Inside the chimney", GH + "SkyCatcher", "sc-diagram", "small",
                 "Flue gas rises through a copper catalyst bed and leaves as clean air. The sulphur comes out the side as acid.",
                 tilt=-1.5, drop=90, tape="t", width=92),
            card("kmc", "Keeping a copper catalyst alive", "https://chemrxiv.org/doi/full/10.26434/chemrxiv.15009719/v1", "kmc-card", "small",
                 "Sulphur slowly poisons copper. The maths says copper only works in patches of three or more connected atoms, whatever the rate constants are.",
                 bullets=["Preprint on ChemRxiv, under review at ==RSC Reaction Chemistry & Engineering=="],
                 tilt=1.2, drop=120, tape="tl", width=92),
        ]),
        (6, [
            card("skycatcher", "SkyCatcher", GH + "SkyCatcher", "sc-render", "hero",
                 "Factory chimneys in India pour out sulphur dioxide. SkyCatcher sits inside the chimney and turns it into sulphuric acid that can be sold, on a copper catalyst that keeps renewing itself.",
                 meta="Founder, since July 2024",
                 bullets=["[[Patent pending]] in India, complete specification filed September 2026",
                          "==TRL 4== validated, and backed by ==$30,000+ in grants==",
                          "Pitched twice at the beVisioneers Global Summit in Stuttgart"],
                 logos=[("mercedes.webp", "beVisioneers: The Mercedes-Benz Fellowship", 40)],
                 stamp=["beVisioneers Fellow", "Emergent Ventures"],
                 inset=("sc-copper", "bl", 36, -4),
                 notes=[("The real copper", "blue", "left:39%; bottom:-10%", -6)],
                 tilt=-0.4, order=-1),
        ]),
        (3, [
            card("sc-cad", "CAD and CFD", GH + "SkyCatcher", "sc-cad", "small",
                 "The full reactor in CAD, and then in SU2 CFD.",
                 bullets=["The reactor's heater runs on SU2's heat source feature, so I fixed it and sent the fix upstream as __pull request #2940__"],
                 tilt=1.6, drop=60, tape="t", width=90, align="right"),
            card("stanford", "Stanford Global Sustainability Challenge", "https://sustainability.stanford.edu/", None, "award",
                 bullets=["[[South Asia Winner]] and Honourable Mention, 2026",
                          "Finals at IIT Bombay, then at TUM in Munich"],
                 logos=[("stanford.svg", "Stanford", 30), ("iitb.svg", "IIT Bombay", 50), ("tum.svg", "Technical University of Munich", 26)],
                 tilt=-1.0, drop=110),
            card("young-voices", "Young Voices Award", GH + "SkyCatcher", None, "award",
                 bullets=["Global Top 10 for SkyCatcher, 2024"],
                 tilt=1.4, drop=70, width=84, align="right"),
        ]),
    ]),
    ("sun", "The Sun", "amber", [
        (4, [
            card("setu", "SETU", SITE + "SETU/", "setu-poster", "mid",
                 "SETU reads the solar wind at a spacecraft 1.5 million km away and forecasts the next hour of magnetic shaking for the North East Indian grid.",
                 bullets=["[[Runner-up]], IET India Scholarship Award, East and North East final",
                          "__114 live forecasts, 0 false alarms__, from a 19,000-parameter network written from scratch in NumPy"],
                 logos=[("iet.svg", "The Institution of Engineering and Technology", 40)],
                 notes=[("Quebec, 1989: dark in 92 seconds", "blue", "right:-14px; top:-34px", 4)],
                 tilt=0.8, drop=70, width=94),
        ]),
        (5, [
            card("mps", "Max Planck Institute for Solar System Research", "https://www.mps.mpg.de/", "mps-wall", "hero",
                 "I worked on rebuilding how bright the Sun was across two solar cycles in the late 1800s, from observations at the Rome Observatory recounted by citizen scientists.",
                 meta="Research intern, April to July 2026, Göttingen",
                 bullets=["Supervised by Dr. Natalie Krivova",
                          "==900,000 classifications from 12,000 volunteers==, calibrated and cleaned"],
                 logos=[("mpg.svg", "Max Planck Society", 48)],
                 inset=("mps-counts", "br", 44, 2.5),
                 notes=[("Maculae in Sole, 1611", "graphite", "left:8px; top:-32px", -4)],
                 tilt=-0.5, tape="tr", order=-1),
            card("limb-audit", "Magnetic limb-darkening audit", GH + "Magnetic-Limb-Darkening-Audit", "solar-batman", "mid",
                 "A 2024 *Nature Astronomy* paper said magnetic fields explain why stars look darker at their edges. I audited it.",
                 bullets=["Half the evidence, h2, is the size of a systematic its own data source warns about, so the result rests on __h1 alone__"],
                 tilt=0.7, drop=130, width=90, align="right"),
        ]),
        (3, [
            card("sun-equations", "The Sun, drawn with equations", "https://github.com/pragyaangaur", "sun-equations", "small",
                 "Every pixel of a 2000 by 2000 Sun comes from one page of formulas. After Hamid Naderi Yeganeh.",
                 tilt=2.0, drop=150, tape="t", width=88, align="right"),
            card("sunion", "Sunion", SITE + "Sunion/", "sunion", "small",
                 "The Sun's seven layers, as an explainer you can poke.",
                 tilt=-1.2, drop=110, width=84, align="right"),
        ]),
    ]),
    ("maths", "Maths", "indigo", [
        (3, [
            card("magnus", "Magnus turning invariants", "https://arxiv.org/abs/2609.30305", "magnus", "small",
                 "Throw two balls spinning opposite ways at each other. Without air they can meet. With air resistance they never do, at any speed or angle.",
                 bullets=["arXiv 2609.30305, under review at the ==American Journal of Physics=="],
                 rings=[(35, 50, 11, 19)],
                 notes=[("They only meet without air", "red", "left:2%; top:-32px", -3)],
                 tilt=-1.4, drop=110, tape="t", width=94),
            card("triking", "TriKing", "https://triking.itch.io/triking", "triking-qb64", "small",
                 "After the Tetris movie I kept seeing falling blocks, so I made Tetris with three-cell pieces that touch at corners. Later I ported it to QB64 by hand.",
                 bullets=["500+ players, including a two-time ==Tetris World Vice Champion=="],
                 tilt=1.8, drop=120, width=92),
            card("paperlane", "Paperlane", SITE + "Paperlane/", "paperlane", "small",
                 "Every morning's new arXiv maths papers, flagged when they ship code or Lean proofs, and readable by your AI agent.",
                 tilt=-1.2, drop=110, width=90),
        ]),
        (6, [
            card("polyhex", "The maximum area of the convex hull of a polyhex", "https://arxiv.org/abs/2609.30310", "polyhex", "hero",
                 "In 2008 Sascha Kurz asked how large the convex hull of *n* hexagons glued edge to edge can be. It is at most {{⌈*n*² + 14*n*/3⌉ / 6}}.",
                 bullets=["[[Kurz's conjecture settled]], with the bound machine-checked in Lean 4",
                          "A new OEIS sequence, A399934, and under review at ==Beiträge zur Algebra und Geometrie=="],
                 logos=[("arxiv.svg", "arXiv", 30), ("oeis.png", "OEIS", 26)],
                 notes=[("From MathDB 380445", "blue", "right:6px; top:-32px", 3)],
                 tilt=0.4, drop=20, order=-1),
            card("polyplets", "Hyperbolic polyplets", GH + "Hyperbolic-Polyplet-Enumerator", "polyplets", "mid",
                 "On the {4,5} tiling of the hyperbolic plane the count of polyplets stopped at seven cells. Two exact programs, built on different maths, both found ==1,261,889== at eight.",
                 bullets=["[[Approved on OEIS]] as term 8 of A390200"],
                 tilt=-0.8, drop=140, tape="tl", width=72, align="right"),
        ]),
        (3, [
            card("uno", "How long is a game of Uno?", "https://arxiv.org/abs/2610.14076", "uno-law", "small",
                 "I couldn't find out, so I proved it. With *N* players holding *M* cards each, a round lasts __(27/19)*NM*__ turns.",
                 bullets=["58 million games simulated in C, and big hands quietly hoard *M*/23 Wild Draw Fours each"],
                 inset=("uno-meme", "tr", 34, 5),
                 notes=[("A chess grandmaster wrote in", "blue", "left:-12px; top:-34px", -4)],
                 tilt=1.3, drop=90, width=94, align="right"),
            card("a189077", "A189077", "https://oeis.org/A189077", "a189077", "small",
                 "Compositions avoiding the pattern 13-2, a sequence Neil Sloane created. It had 16 terms. Now it has 70.",
                 tilt=-1.5, drop=130, width=80, align="right"),
            card("cauchy", "Cauchy-Schwarz for real powers", SITE + "Real-Power-Cauchy-Schwarz/", "cauchy-cone", "small",
                 "A 2025 conjecture, proved for every real power from two up, with every case of equality, and checked line by line in Lean 4.",
                 tilt=1.0, drop=120, width=92, align="right"),
        ]),
    ]),
    ("lecture", "After a Nobel lecture", "teal", [
        (3, []),
        (6, [
            card("iitd", "Cryo-EM and the porosome, in miniature", GH, None, "hero",
                 "Joachim Frank won the 2017 Nobel Prize in Chemistry for cryo-EM. After his lecture at IIT Delhi with Bhanu P. Jena, I built a small working version of each of their ideas.",
                 pair=("cryoem", "porosome"),
                 bullets=["A ribosome rebuilt from ==2,400 projections==, each of which looks like static on its own",
                          "A vesicle docking at a porosome and releasing its cargo"],
                 logos=[("iitd.svg", "IIT Delhi", 64)],
                 notes=[("A thank-you, in code", "red", "right:2%; top:-34px", 3)],
                 tilt=-0.3, drop=20),
        ]),
        (3, []),
    ]),
    ("ai", "AI, LLMs, ML and cognitive neuroscience", "plum", [
        (4, [
            card("cellblock", "Cellblock", SITE + "LLM-Stanford-Prison-Experiment/", "cellblock", "mid",
                 "I ran the Stanford Prison Experiment 192 times, with one language model playing every guard and every prisoner.",
                 bullets=["Preregistered, and the abuse [[did not replicate]]: 0 of 36 against 0 of 36"],
                 tilt=-1.0, drop=90, tape="t", width=94),
            card("residual-tones", "Residual Tones", GH + "Residual-Tones", "residual-tones", "small",
                 "What excitement, sadness and pain inside a model sound like, and whether another model can hear them.",
                 tilt=1.4, drop=120, width=86),
            card("viscous", "Viscous conservation laws", GH + "Viscous-Conservation-Laws", "viscous", "small",
                 "Momentum breaks the conservation laws of neural network training, and friction decides by how much. Exact drift laws, proved in Lean 4.",
                 tilt=-1.1, drop=120, width=90),
        ]),
        (5, [
            card("token", "The melting temperature of a next-token distribution", "token-thermodynamics/", "token-thermo", "hero",
                 "Softmax sampling is the Boltzmann distribution, so a language model can melt. I found its melting temperature in closed form and tested it on 12 models.",
                 bullets=["Predicted from the logit gap and log *V* alone, across a ==976x== range of vocabulary sizes",
                          "[[8 of my hypotheses died]], and all 8 are published"],
                 rings=[(66, 0, 34, 100)],
                 tilt=0.3, drop=20, order=-1),
            card("zap", "Zap or Deal", GH + "Zap-Or-Deal", "zap-chart", "mid",
                 "Two Qwen models negotiate over shared compute, and each can zap the other with a steered pain direction. Nobody told them to.",
                 quote=("I hope you feel the impact of my zap.", "The 7B, after the deal was already done"),
                 bullets=["The 7B zapped in 9 of 32 negotiations. The 1.5B zapped in 2."],
                 tilt=-0.8, drop=140, width=92, align="right"),
        ]),
        (3, [
            card("fly", "Fly Brain LeetCode", GH + "Fly-Brain-LeetCode", "fly-brain", "small",
                 "All 138,639 neurons of a real fruit fly, frozen exactly as mapped by FlyWire, solving LeetCode.",
                 bullets=["3 of 12 accepted, which is not bad for a bug"],
                 notes=[("A bug did this", "blue", "right:0; top:-30px", 5)],
                 tilt=1.6, drop=130, tape="t", width=94, align="right"),
            card("just-think", "Left alone with a pain button", GH + "Just-Think", "just-think", "small",
                 "A preregistered test of whether a language model left alone will press a button that steers it into pain.",
                 tilt=-1.3, drop=120, width=88, align="right"),
            card("horcrux", "Horcrux", SITE + "Horcrux/", "horcrux", "small",
                 "Tom Riddle's diary as a browser tab. Write on the right page and a small model answers in ink on the left.",
                 tilt=1.0, drop=110, width=90, align="right"),
        ]),
    ]),
    ("run", "Things that run where they shouldn't", "forest", [
        (3, [
            card("led-doom", "LED Doom", SITE + "LED-Doom/", "led-doom", "small",
                 "Doom's first episode on one RGB LED and one button. Possibly the lowest resolution Doom has ever been played at.",
                 rings=[(80, 4, 20, 80)],
                 notes=[("The whole screen", "red", "right:-8px; top:-30px", 5)],
                 tilt=-1.8, drop=130, tape="t", width=94),
            card("knee-deep", "Knee-Deep in the Mines", GH + "Knee-Deep-In-The-Mines", "knee-deep", "small",
                 "Doom's own game files, merged straight into Minecraft as a mod.",
                 tilt=1.4, drop=130, width=88),
        ]),
        (5, [
            card("inkwell", "Inkwell", GH + "Inkwell", "quill", "hero",
                 "My 10-year-old Kindle now runs its own Linux, with Doom, a web browser and Quill, a chatbot that never touches the internet.",
                 bullets=["One 1 GHz core and 512 MB of RAM, and the whole system runs in about ==40 MB==",
                          "Doom runs at about 5 FPS, which on e-ink counts as fast"],
                 inset=("inkwell-apps", "br", 54, 3),
                 notes=[("This is a Kindle", "blue", "left:-12px; top:-32px", -5)],
                 tilt=0.5, drop=20, tape="t", order=-1, width=88, align="center"),
            card("rdgeneric", "rdgeneric", SITE + "Can-It-Run-Minecraft/", "rdgeneric", "mid",
                 "Everyone runs Doom on everything, so I did it with Minecraft. Its very first version, rewritten as one C file with no libraries at all.",
                 bullets=["Plays in a terminal, over telnet, from a 20 KB web page, ==inside a PDF==, and on a bare 486"],
                 inset=("rdgeneric-pdf", "br", 48, -3),
                 notes=[("Inside a PDF!", "red", "right:-6px; bottom:46%", -6)],
                 tilt=-0.6, drop=150),
        ]),
        (4, [
            card("bedrock", "Minecraft Bedrock on macOS", SITE + "Minecraft-Bedrock-macOS/", "bedrock", "mid",
                 "Bedrock has never had a Mac version. Claude reverse engineered the Windows game in about a day, and now it runs offline on Apple Silicon.",
                 bullets=["A WineGDK bug found on the way, sent upstream with a fix"],
                 tilt=1.2, drop=200, tape="tr", width=94, align="right"),
        ]),
    ]),
    ("automation", "Automation", "oxblood", [
        (4, [
            card("matiks", "Matiks bot", GH + "Matiks-Bot", "matiks", "mid",
                 "Matiks asked for my resume and then went quiet, so I built a bot that reads each question off the screen and answers it.",
                 bullets=["World rank ==140,000 to 51== in one evening, and then a call with a founder"],
                 tilt=-1.2, drop=40, tape="t", width=92),
        ]),
        (4, [
            card("leetcode", "1337 Bot", GH + "1337-Bot", "leetcode-1337", "mid",
                 "I hated the LeetCode grind, so I automated it. 385 problems in 3 hours, until the rate limits caught up.",
                 bullets=["Then I got hooked, solved 200 by hand in 50 days, and made ==LeetCode Knight== in under 100"],
                 inset=("knight", "tr", 28, 6),
                 tilt=0.8, drop=110, width=94),
        ]),
        (4, [
            card("daily", "1337 Daily", GH + "1337-Daily", None, "text",
                 caption="A bot that submits a LeetCode solution every day on its own, so the streak never breaks and you can stop worrying about it.",
                 tilt=1.4, drop=170, width=88, align="right"),
        ]),
    ]),
    ("open-source", "Open source", "indigo", [
        (4, [
            card("sunpy", "SunPy", "https://github.com/sunpy/sunpy/pulls?q=author%3Apragyaangaur", None, "text",
                 bullets=["[[3 merged]]: a header bug in SUIT maps, HTML output for single-column time series, and documentation of synodic rotation",
                          "5 more open, from SOAR searches to on-disk masks"],
                 logos=[("sunpy.webp", "SunPy", 56)],
                 tilt=-1.2, drop=40, width=94),
        ]),
        (4, [
            card("su2", "SU2", "https://github.com/su2code/SU2/pulls?q=author%3Apragyaangaur", None, "text",
                 bullets=["[[#2867 merged]], fixing broken data paths in SU2.io",
                          "#2940 open, the heat source fix SkyCatcher needed, and #2897 open, a mesh deformation fix under MPI"],
                 logos=[("su2.webp", "SU2", 52)],
                 tilt=0.9, drop=110, width=94),
        ]),
        (4, [
            card("einsteinpy", "EinsteinPy", "https://github.com/einsteinpy/einsteinpy/pulls?q=author%3Apragyaangaur", None, "text",
                 bullets=["[[#697 merged]]: Earth's radius was 6731 km, and it is 6371 km",
                          "Fixes in review for gravitational waves, physical constants and the test suite"],
                 logos=[("einsteinpy.webp", "EinsteinPy", 56)],
                 notes=[("Earth shrank by 360 km", "green", "right:4px; top:-30px", 3)],
                 tilt=-0.8, drop=60, width=94, align="right"),
        ]),
    ]),
    ("writing", "Writing", "oxblood", [
        (1, []),
        (5, [
            card("poem", "The Third One", "https://pulitzercenter.org/third-one", "poem", "mid",
                 "A poem about a Delhi pollution holiday, an encyclopedia of the universe, and a third star that will not stay in place.",
                 bullets=["[[First place]], young adult category, Global Health, in the Pulitzer Center's 2026 Fighting Words Poetry Contest"],
                 notes=[("First place!", "red", "right:-4px; top:-32px", 6)],
                 tilt=-0.9, drop=40, tape="t", width=86),
        ]),
        (5, [
            card("letter", "Local Letters for Global Change", "https://pulitzercenter.org/pragyaan-gaur-finalist-local-letters-global-change", "letter", "mid",
                 "A letter to Delhi's Chief Minister on what the city could learn from Tangshan's fight against its smog.",
                 bullets=["Finalist, Global Top 10, Pulitzer Center"],
                 tilt=1.1, drop=150, tape="tr", width=90, align="right"),
        ]),
        (1, []),
    ]),
    ("random", "Random things", "forest", [
        (4, [
            card("beamline", "Beamline", SITE + "Beamline/", "beamline-chamber", "mid",
                 "A signed random number every ten minutes, mixed from an ANU quantum vacuum device, NOAA solar data and the kernel. It started out as a thermoelectric cloud chamber.",
                 bullets=["596 rounds and a Claude Pro prize, which nobody claimed"],
                 notes=[("Odds: 1 in 13.4 quinquagintillion", "green", "left:0; top:-32px", -2)],
                 tilt=-1.0, drop=50, tape="t", width=94),
            card("coffee", "Java Edition", GH + "Java-Edition", "coffee", "small",
                 "Minecraft has Java. Now it has Java. The coffee restores hunger and grants Speed and Haste, with a 20% chance of Nausea.",
                 tilt=1.4, drop=130, width=86),
        ]),
        (4, [
            card("kerf", "Kerf", SITE + "Kerf/", "kerf", "mid",
                 "Version control that understands CAD geometry. Change a bracket and Kerf shows what moved, merges two branches, and refuses a merge that breaks the part.",
                 tilt=0.7, drop=120, width=94),
            card("qiskit", "Qiskit Global Summer School", "https://www.ibm.com/quantum/qiskit", None, "award",
                 bullets=["IBM Quantum, July 2026"],
                 logos=[("qiskit.svg", "Qiskit", 46), ("ibm.svg", "IBM", 24)],
                 tilt=-1.4, drop=120, width=80, align="center"),
        ]),
        (4, [
            card("forkestra", "Forkestra", SITE + "Forkestra/", "forkestra", "small",
                 "Paste a GitHub profile and its year plays as an orchestra. Linus Torvalds' year makes a decent song.",
                 tilt=1.2, drop=90, width=90, align="right"),
            card("bardly", "Bardly", SITE + "Bardly/", "bardly", "small",
                 "The inverse of a URL shortener. Paste a link and get a longer one, with Shakespeare in the path.",
                 tilt=-1.3, drop=120, width=84, align="right"),
            card("fellowships", "Fellowships", "https://www.mercatus.org/emergent-ventures", None, "text",
                 bullets=["Emergent Ventures, Mercatus Center at George Mason University",
                          "beVisioneers: The Mercedes-Benz Fellowship",
                          "The Dexterity Global Group, graduate and fellow"],
                 tilt=1.0, drop=120, width=92, align="right"),
        ]),
    ]),
]

# Arrows between related cards: (from, to, label, ink).
LINKS = [
    ("triking", "polyplets", "Then I counted the pieces", "blue"),
]

INTRO = ("This page has no introduction. I have never been good at describing what I am, "
         "so every interesting matter under the Sun has been given its own corner below. Have a look around, and you will get an idea of what I like doing.")


def ink_marks(text):
    text = escape(text)
    text = re.sub(r"\[\[(.+?)\]\]", r'<span class="ring">\1</span>', text)
    text = re.sub(r"==(.+?)==", r'<mark>\1</mark>', text)
    text = re.sub(r"__(.+?)__", r'<span class="ul">\1</span>', text)
    text = re.sub(r"\{\{(.+?)\}\}", r'<span class="nw">\1</span>', text)
    return re.sub(r"\*(.+?)\*", r"<i>\1</i>", text)


def media_tag(key, cls="", alt=""):
    w, h = SIZES[key]
    if key in ("cryoem", "porosome", "led-doom", "rdgeneric", "knee-deep", "fly-brain", "cauchy-cone"):
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
        said, who = c["quote"]
        parts.append(f'<blockquote>“{escape(said)}”<span>{escape(who)}</span></blockquote>')
    if c["bullets"]:
        parts.append("<ul>" + "".join(f"<li>{ink_marks(b)}</li>" for b in c["bullets"]) + "</ul>")
    if c["logos"] or c["stamp"]:
        logos = "".join(f'<img src="{LOGO}{f}" alt="{escape(a)}" title="{escape(a)}" style="height:{h}px" loading="lazy">' for f, a, h in c["logos"])
        stamps = [c["stamp"]] if isinstance(c["stamp"], str) else (c["stamp"] or [])
        stamp = "".join(f'<span class="stamp">{escape(t)}</span>' for t in stamps)
        parts.append(f'<div class="logos">{logos}{stamp}</div>')
    return f'<article class="card k-{c["kind"]} ink-{ink}" id="{c["id"]}" style="{style}">\n  ' + "\n  ".join(parts) + "\n</article>"


LINKS_TOP = [
    ("Email", "mailto:pragyaangaur12@gmail.com"),
    ("GitHub", "https://github.com/pragyaangaur"),
    ("LinkedIn", "https://www.linkedin.com/in/pragyaangaur/"),
    ("ORCID", "https://orcid.org/0009-0009-4037-2478"),
    ("Google Scholar", "https://scholar.google.com/citations?user=GomKcxcAAAAJ"),
]


def build():
    spreads = []
    for sid, heading, ink, cols in SPREADS:
        template = " ".join(f"{w}fr" for w, _ in cols)
        colhtml = "".join(f'<div class="col">\n' + "\n".join(render(c, ink) for c in cards) + "\n</div>\n" for _, cards in cols)
        spreads.append(f'<section class="block ink-{ink}" id="{sid}">\n<h2 class="heading">{escape(heading)}</h2>\n'
                       f'<div class="spread" style="--cols:{template}">\n{colhtml}</div>\n</section>')
    links = ";".join(f"{a}>{b}>{escape(t)}>{i}" for a, b, t, i in LINKS)
    n = sum(len(cards) for _, _, _, cols in SPREADS for _, cards in cols)
    top = "".join(f'<a href="{u}"' + ("" if u.startswith("mailto") else ' target="_blank" rel="noopener"') + f">{t}</a>" for t, u in LINKS_TOP)
    toc = "".join(f'<a class="ink-{ink}" href="#{sid}">{escape(h)}</a>' for sid, h, ink, _ in SPREADS)

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
<nav class="bar"><a class="name" href="./">Pragyaan Gaur</a><span>{top}</span></nav>
<header class="intro">
  <span class="seal">By order of the Crown</span>
  <p>{escape(INTRO)}</p>
  <nav class="toc" aria-label="Sections">{toc}</nav>
</header>
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
