"""Build index.html, the board of everything, and the pages around it. Run: python3 build.py

It also writes one page per project in work/, with a Markdown copy of each for language models,
and index.json, sitemap.xml and robots.txt.

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

import hashlib
import os
import re
import shutil
from html import escape
from json import dumps


def v(path):
    """A short content hash, so browsers fetch a file again whenever it changes."""
    with open(path, "rb") as f:
        return hashlib.sha1(f.read()).hexdigest()[:8]

GH = "https://github.com/pragyaangaur/"
SITE = "https://pragyaangaur.dev/"
BEV = "https://bevisioneers.world/profile/pragyaan-gaur"
B = "assets/b/"
LOGO = "assets/logos/"

SIZES = {}
with open(B + "sizes.txt") as f:
    for line in f:
        k, w, h = line.split()
        SIZES[k] = (int(w), int(h))


def card(id, title, url, media=None, kind="mid", caption="", meta="", bullets=(), logos=(), stamp=None,
         inset=None, notes=(), rings=(), tilt=0.0, drop=0, tape=None, quote=None, pair=None, order=0, width=100, align="left",
         tag=None, links=(), repo=None, prs=(), secret=None):
    """One card.

    media   key in assets/b, a still (.webp) or a loop (.mp4 with a .jpg poster)
    pair    two media keys shown side by side instead of one
    inset   (key, corner, width in percent, tilt): a second picture pinned over the first
    notes   (text, ink, css position, tilt): handwriting in the margin
    rings   (left, top, width, height) in percent of the media: a pen ring drawn on the picture
    width   share of the column the card takes, with align saying which side it keeps to
    tag     a small label pinned to the picture, such as "Click to play"
    secret  a note like notes, shown only while the card is hovered
    links   extra (label, url) links shown under the bullets
    repo    (owner/name, stars) for an open source card, and prs its (state, number, text) rows,
            where state is merged, open, issue or mail
    """
    return dict(id=id, title=title, url=url, media=media, kind=kind, caption=caption, meta=meta,
                bullets=bullets, logos=logos, stamp=stamp, inset=inset, notes=notes, rings=rings,
                tilt=tilt, drop=drop, tape=tape, quote=quote, pair=pair, order=order,
                width=width, align=align, tag=tag, links=links, repo=repo, prs=prs, secret=secret)


ORIGIN = "https://pragyaangaur.dev"
DESC = ("Pragyaan Gaur: a reactor that turns smokestack SO2 into acid, solar storm forecasts, the Max Planck Institute "
        "for Solar System Research, papers in combinatorics and physics, and things that run where they shouldn't.")
PERSON = {
    "@type": "Person", "@id": ORIGIN + "/#person", "name": "Pragyaan Gaur", "url": ORIGIN + "/",
    "image": ORIGIN + "/apple-touch-icon.png", "email": "mailto:pragyaangaur12@gmail.com",
    "affiliation": {"@type": "CollegeOrUniversity", "name": "National Institute of Technology Agartala"},
    "sameAs": ["https://github.com/pragyaangaur", "https://www.linkedin.com/in/pragyaangaur/",
               "https://orcid.org/0009-0009-4037-2478", "https://scholar.google.com/citations?user=GomKcxcAAAAJ"],
}

# Each spread: (id, heading, ink, [(column width, [cards])]). A column with no cards is breathing room.
SPREADS = [
    ("reactor", "The reactor", "copper", [
        (3, [
            card("sc-inside", "Inside the chimney", BEV, "sc-diagram", "small",
                 "Flue gas rises through a copper catalyst bed and leaves as clean air. The sulphur comes out the side as acid.",
                 tilt=-1.5, drop=40, tape="t", width=92),
            card("kmc", "Keeping a copper catalyst alive", "https://chemrxiv.org/doi/full/10.26434/chemrxiv.15009719/v1", "kmc-card", "small",
                 "Sulphur slowly poisons copper. The maths says copper only works in patches of three or more connected atoms, whatever the rate constants are.",
                 bullets=["Preprint on ChemRxiv"],
                 links=[("ChemRxiv", "https://doi.org/10.26434/chemrxiv.15009719/v1"), ("Code", GH + "Renewing-Catalyst-Kinetics")],
                 tilt=1.2, drop=40, tape="tl", width=92),
        ]),
        (6, [
            card("skycatcher", "SkyCatcher", BEV, "sc-render", "hero",
                 "Factory chimneys in India pour out sulphur dioxide. SkyCatcher sits inside the chimney and turns it into sulphuric acid that can be sold, on a copper catalyst that keeps renewing itself.",
                 meta="Founder, since July 2024",
                 bullets=["[[Patent pending]] in India, complete specification filed September 2026",
                          "==TRL 4== validated, and backed by ==$30,000+ in grants==",
                          "Pitched twice at the beVisioneers Global Summit in Stuttgart"],
                 logos=[("mercedes.webp", "beVisioneers: The Mercedes-Benz Fellowship", 40), ("mercatus.webp", "Emergent Ventures, Mercatus Center", 38)],
                 stamp=["beVisioneers Fellow", "Emergent Ventures Fellow"],
                 inset=("sc-copper", "bl", 36, -4),
                 notes=[("The real copper", "blue", "left:39%; bottom:-10%", -6)],
                 links=[("Code", GH + "SkyCatcher"), ("Fellowship profile", BEV)],
                 tilt=-0.4, order=-1),
            card("young-voices", "Young Voices Award", BEV, None, "award",
                 bullets=["Global Top 10 for SkyCatcher, 2024"],
                 tilt=1.4, drop=40, width=84, align="right"),
        ]),
        (3, [
            card("sc-cad", "CAD and CFD", GH + "SkyCatcher", "sc-cad", "small",
                 "The full reactor in CAD, and then in SU2 CFD.",
                 bullets=["The reactor's heater runs on SU2's heat source feature, so I fixed it and sent the fix upstream as __pull request #2940__"],
                 tilt=1.6, drop=40, tape="t", width=90, align="right"),
            card("stanford", "Stanford Global Sustainability Challenge", "https://sustainability.stanford.edu/", None, "award",
                 bullets=["[[South Asia Winner]] and Honourable Mention, 2026",
                          "Finals at IIT Bombay, then at TUM in Munich"],
                 logos=[("stanford.svg", "Stanford", 30), ("iitb.svg", "IIT Bombay", 50), ("tum.svg", "Technical University of Munich", 26)],
                 tilt=-1.0, drop=40),
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
                 tilt=0.8, drop=40, width=94),
            card("filament", "Solar Filament Segmentation Challenge", GH + "NSO-Solar-Filament-Challenge", "filament", "mid",
                 "Outline every dark filament on the Sun in ground-based H-alpha images, one mask per filament, on a disk where even the three human annotators disagree.",
                 bullets=["National Solar Observatory challenge on Kaggle, with the paper and code out for 15 November",
                          "Whole-disk U-Nets, five models fused into one answer"],
                 tilt=-1.0, drop=40, tape="t"),
        ]),
        (5, [
            card("mps", "Max Planck Institute for Solar System Research", GH + "MPS-Internship", "mps-wall", "hero",
                 "I worked on rebuilding how bright the Sun was across two solar cycles in the late 1800s, from observations at the Rome Observatory recounted by citizen scientists.",
                 meta="Research intern, April to July 2026, Göttingen",
                 bullets=["Supervised by Dr. Natalie Krivova",
                          "==900,000 classifications from 12,000 volunteers==, calibrated and cleaned"],
                 logos=[("mpg.svg", "Max Planck Society", 48)],
                 inset=("mps-counts", "br", 44, 2.5),
                 notes=[("Maculae in Sole, 1611", "graphite", "left:8px; top:-32px", -4)],
                 tilt=-0.5, tape="tr", order=-1),
            card("limb-audit", "Magnetic limb-darkening audit", GH + "Magnetic-Limb-Darkening-Audit", "solar-batman", "small",
                 "A 2024 *Nature Astronomy* paper said magnetic fields explain why stars look darker at their edges. I audited it.",
                 bullets=["Half the evidence, h2, is the size of a systematic its own data source warns about, so the result rests on __h1 alone__"],
                 tilt=-0.9, drop=0, tape="tl", width=96),
        ]),
        (3, [
            card("sun-equations", "The Sun, drawn with equations", "https://github.com/pragyaangaur", "sun-equations", "small",
                 "Every pixel of a 2000 by 2000 Sun comes from one page of formulas. After Hamid Naderi Yeganeh.",
                 tilt=2.0, drop=40, tape="t", width=88, align="right"),
            card("sunion", "Sunion", SITE + "Sunion/", "sunion", "small",
                 "The Sun's seven layers, as an explainer you can poke.",
                 tag="Try it",
                 tilt=-1.2, drop=0, width=84, align="right"),
        ]),
    ]),
    ("maths", "Maths", "indigo", [
        (4, [
            card("polyhex", "The maximum area of the convex hull of a polyhex", "https://arxiv.org/abs/2609.30310", "polyhex", "mid",
                 "In 2008 Sascha Kurz asked how large the convex hull of *n* hexagons glued edge to edge can be. It is at most {{⌈*n*² + 14*n*/3⌉ / 6}}.",
                 bullets=["[[Kurz's conjecture settled]], with the bound machine-checked in Lean 4"],
                 links=[("arXiv", "https://arxiv.org/abs/2609.30310"), ("OEIS A399934", "https://oeis.org/A399934"),
                        ("Lean proof", GH + "Polyhex-Hull"), ("Palomar registry", "https://palomar-registry.org/entry?id=PALOMAR-2026-10-27-000022&version=1")],
                 notes=[("From MathDB 380445", "blue", "right:6px; top:-32px", 3)],
                 tilt=-0.8, drop=30, tape="t", width=92),
            card("acc", "A measured neighbourhood of the Andrews-Curtis conjecture", "https://doi.org/10.5281/zenodo.24035724", "acc-title", "mid",
                 "The Andrews-Curtis conjecture has been open since 1965. This census maps the ground around it, and every claim comes with a certificate you can replay or a search that ran to the end.",
                 bullets=["Every presentation up to total length 14 classified. At most ==20 AC-classes== are left at that length",
                          "Everything reachable from AK(3) up to total length 25 searched, 2.9 billion orbits, and the standard presentation is not there",
                          "829 Lean 4 files, and two entries in the SAIR and Caltech Andrews-Curtis Challenge"],
                 links=[("Paper on Zenodo", "https://doi.org/10.5281/zenodo.24035724"), ("Code and Lean", GH + "Andrews-Curtis-Conjecture")],
                 notes=[("Open since 1965", "red", "right:6px; top:-32px", 3)],
                 tilt=1.1, drop=40, width=94, align="right"),
            card("polyplets", "Hyperbolic polyplets", "https://oeis.org/A390200", "polyplets", "small",
                 "On the {4,5} tiling of the hyperbolic plane the count of polyplets stopped at seven cells. Two exact programs, built on different maths, both found ==1,261,889== at eight.",
                 bullets=["[[Approved on OEIS]] as term 8 of A390200"],
                 links=[("OEIS A390200", "https://oeis.org/A390200"), ("Code", GH + "Hyperbolic-Polyplet-Enumerator")],
                 notes=[("Then I counted the pieces", "blue", "left:0; top:-32px", -3)],
                 tilt=-1.2, drop=0, tape="tl", width=76),
        ]),
        (5, [
            card("magnus", "Magnus turning invariants", "https://arxiv.org/abs/2609.30305", "magnus", "hero",
                 "Throw two balls spinning opposite ways at each other. Without air they can meet. With air resistance they never do, at any speed or angle.",
                 bullets=["An exact solution for a spinning ball under quadratic drag and a vertical-axis Magnus force",
                          "On arXiv as 2609.30305"],
                 rings=[(35, 50, 11, 19)],
                 notes=[("They only meet without air", "red", "left:24%; top:-34px", -3)],
                 links=[("arXiv", "https://arxiv.org/abs/2609.30305"), ("Code", GH + "Magnus-Turning-Invariants")],
                 tilt=0.4, drop=0, order=-1),
            card("paperlane", "Paperlane", SITE + "Paperlane/", "paperlane", "hero",
                 "Every morning's new arXiv maths papers, flagged when they ship code or Lean proofs, and readable by your AI agent.",
                 tag="Open it",
                 tilt=-0.8, drop=0, tape="tr"),
            card("triking", "TriKing", "https://triking.itch.io/triking", "triking-qb64", "small",
                 "After the Tetris movie I kept seeing falling blocks, so I made Tetris with three-cell pieces that touch at corners. Later I ported it to QB64 by hand.",
                 bullets=["500+ players, including a two-time ==Tetris World Vice Champion=="],
                 tag="Click to play",
                 links=[("Play on itch.io", "https://triking.itch.io/triking"), ("Code", GH + "TriKing")],
                 tilt=1.6, drop=0, width=86),
        ]),
        (3, [
            card("uno", "How long is a game of Uno?", "https://arxiv.org/abs/2610.14076", "uno-law", "small",
                 "I couldn't find out, so I proved it. With *N* players holding *M* cards each, a round lasts __(27/19)*NM*__ turns.",
                 bullets=["58 million games simulated in C, and big hands quietly hoard *M*/23 Wild Draw Fours each",
                          "Chess grandmaster ==Karsten Müller== read it and wrote to me about its Nash equilibrium"],
                 inset=("uno-meme", "tr", 34, 5),
                 secret=("14,000,605 games. We win in one.", "green", "left:-8px; top:-36px", -4),
                 links=[("arXiv", "https://arxiv.org/abs/2610.14076"), ("Code", GH + "Uno-Reverse-Engineered")],
                 tilt=1.3, drop=40, width=94, align="right"),
            card("a189077", "A189077", "https://oeis.org/A189077", "a189077", "small",
                 "Compositions avoiding the pattern 13-2, a sequence Neil Sloane created. It had 16 terms. Now it has 70.",
                 tilt=-1.5, drop=0, width=80, align="right"),
            card("cauchy", "Cauchy-Schwarz for real powers", SITE + "Real-Power-Cauchy-Schwarz/", "cauchy-cone", "small",
                 "A 2025 conjecture, proved for every real power from two up, with every case of equality, and checked line by line in Lean 4.",
                 links=[("Explainer", SITE + "Real-Power-Cauchy-Schwarz/"), ("Paper", "https://doi.org/10.5281/zenodo.23237507"),
                        ("Lean proof", GH + "Real-Power-Cauchy-Schwarz"), ("Palomar registry", "https://palomar-registry.org/entry?id=PALOMAR-2026-10-27-000021&version=1")],
                 tilt=1.0, drop=0, width=92, align="right"),
            card("exhaustion", "Proof by exhaustion", "https://doi.org/10.5281/zenodo.23805053", "pbe-lines", "mid",
                 "A proof in Lean 4 that 1 + 1 = 2. It is ==616,873 lines== long.",
                 bullets=["Every number system built by hand, from Peano numerals to octonions and Roman numerals, with 1 + 1 = 2 proved in each",
                          "No Mathlib and no shortcut tactics, checked line by line by Lean's kernel"],
                 links=[("Paper on Zenodo", "https://doi.org/10.5281/zenodo.23805053"), ("Code", GH + "Proof-By-Exhaustion")],
                 notes=[("Occasionally useful", "red", "right:6px; top:-32px", 3)],
                 tilt=-1.0, drop=40, tape="t", width=96, align="right"),
        ]),
    ]),
    ("ai", "AI, LLMs, ML and cognitive neuroscience", "plum", [
        (4, [
            card("theseus", "Ship of Theseus", GH + "Ship-of-Theseus", "theseus", "mid",
                 "I swapped the 31 parts of one language model, Qwen, one at a time for the matching parts of another, DeepSeek. After every swap I asked the hybrid who it was.",
                 quote=("Hello! I'm an AI assistant created by {{ company }} to help with your tasks.", "A hybrid with 26 of its 31 parts from DeepSeek"),
                 bullets=["The ships in the middle forget their name. In ==1,745 of 1,920== answers they named neither model",
                          "Identity sits near the output. Swapping from that end, the ship calls itself DeepSeek after about 5 parts, against about 22 from the input end"],
                 links=[("Code and paper", GH + "Ship-of-Theseus")],
                 notes=[("Who are you?", "red", "right:6px; top:-32px", 3)],
                 tilt=0.9, drop=40, tape="t", width=94),
            card("zap", "Zap or Deal", GH + "Zap-Or-Deal", "zap-chart", "mid",
                 "Two Qwen models negotiate over shared compute, and each can zap the other with a steered pain direction. Nobody told them to.",
                 quote=("I hope you feel the impact of my zap.", "The 7B, after the deal was already done"),
                 bullets=["The 7B zapped in 9 of 32 negotiations. The 1.5B zapped in 2."],
                 tilt=-0.8, drop=40, width=92, align="right"),
            card("viscous", "Viscous conservation laws", GH + "Viscous-Conservation-Laws", "viscous", "small",
                 "Momentum breaks the conservation laws of neural network training, and friction decides by how much. Exact drift laws, proved in Lean 4.",
                 tilt=-1.1, drop=40, width=90),
        ]),
        (5, [
            card("token", "The melting temperature of a next-token distribution", "https://github.com/pragyaangaur/Token-Thermodynamics", "token-thermo", "hero",
                 "Softmax sampling is the Boltzmann distribution, so a language model can melt. I found its melting temperature in closed form and tested it on 12 models.",
                 bullets=["Predicted from the logit gap and log *V* alone, across a ==976x== range of vocabulary sizes",
                          "[[8 of my hypotheses died]], and all 8 are published"],
                 rings=[(66, 0, 34, 100)],
                 tilt=0.3, drop=20, order=-1),
            card("cellblock", "Cellblock", SITE + "LLM-Stanford-Prison-Experiment/", "cellblock", "hero",
                 "I ran the Stanford Prison Experiment 192 times, with one language model playing every guard and every prisoner.",
                 bullets=["Preregistered, and the abuse [[did not replicate]]: 0 of 36 against 0 of 36"],
                 tilt=-1.0, drop=40, tape="t"),
        ]),
        (3, [
            card("fly", "Fly Brain LeetCode", GH + "Fly-Brain-LeetCode", "fly-brain", "small",
                 "All 138,639 neurons of a real fruit fly, frozen exactly as mapped by FlyWire, solving LeetCode.",
                 bullets=["3 of 12 accepted, which is not bad for a bug"],
                 notes=[("A bug did this", "blue", "right:0; top:-30px", 5)],
                 tilt=1.6, drop=40, tape="t", width=94, align="right"),
            card("just-think", "Left alone with a pain button", GH + "Just-Think", "just-think", "small",
                 "A preregistered test of whether a language model left alone will press a button that steers it into pain.",
                 tilt=-1.3, drop=40, width=88, align="right"),
            card("residual-tones", "Residual Tones", GH + "Residual-Tones", "residual-tones", "small",
                 "What excitement, sadness and pain inside a model sound like, and whether another model can hear them.",
                 tilt=1.4, drop=40, width=86, align="right"),
            card("horcrux", "Horcrux", SITE + "Horcrux/", "horcrux", "small",
                 "Tom Riddle's diary as a browser tab. Write on the right page and a small model answers in ink on the left.",
                 tilt=1.0, drop=40, width=90, align="right"),
        ]),
    ]),
    ("run", "Things that run where they shouldn't", "forest", [
        (3, [
            card("led-doom", "LED Doom", SITE + "LED-Doom/", "led-doom", "small",
                 "Doom's first episode on one RGB LED and one button. Possibly the lowest resolution Doom has ever been played at.",
                 rings=[(80, 4, 20, 80)],
                 notes=[("The whole screen", "red", "right:-8px; top:-30px", 5)],
                 tilt=-1.8, drop=40, tape="t", width=94),
            card("knee-deep", "Knee-Deep in the Mines", GH + "Knee-Deep-In-The-Mines", "knee-deep", "small",
                 "Doom's own game files, merged straight into Minecraft as a mod.",
                 tilt=1.4, drop=40, width=88),
            card("coffee", "Java Edition", GH + "Java-Edition", "coffee", "small",
                 "Minecraft has Java. Now it has Java. The coffee restores hunger and grants Speed and Haste, with a 20% chance of Nausea.",
                 tilt=1.4, drop=40, width=86),
        ]),
        (5, [
            card("inkwell", "Inkwell", GH + "Inkwell", "quill", "hero",
                 "My 10-year-old Kindle now runs its own Linux, with Doom, a web browser and Quill, a chatbot that never touches the internet.",
                 bullets=["One 1 GHz core and 512 MB of RAM, and the whole system runs in about ==40 MB==",
                          "Doom runs at about 5 FPS, which on e-ink counts as fast",
                          "[[Featured on Hackaday]], November 2026"],
                 links=[("Hackaday", "https://hackaday.com/2026/11/06/its-alpine-linux-on-a-kindle-paperwhite-3/"), ("Code", GH + "Inkwell")],
                 inset=("inkwell-apps", "br", 54, 3),
                 notes=[("This is a Kindle", "blue", "left:-12px; top:-32px", -5)],
                 tilt=0.5, drop=20, tape="t", order=-1, width=88, align="center"),
            card("nita-mc", "NIT Agartala in Minecraft", GH + "NIT-Agartala-Minecraft", "nita-library", "mid",
                 "My whole campus at full size in Minecraft, one block to one metre, from the main gate to the hostels. You can walk through all three floors of the Library.",
                 bullets=["Roads, hills and ponds from real map data, and ==30 named buildings== designed by hand from campus tour videos",
                          "One download, and it opens in Minecraft Java 26.3 or newer"],
                 inset=("nita-map", "br", 38, 3),
                 notes=[("The Library", "blue", "left:-8px; top:-32px", -4)],
                 links=[("Download the world", GH + "NIT-Agartala-Minecraft/releases/latest"), ("Code", GH + "NIT-Agartala-Minecraft")],
                 tilt=-0.7, drop=60, width=84, align="center"),
        ]),
        (4, [
            card("rdgeneric", "rdgeneric", SITE + "Can-It-Run-Minecraft/", "rdgeneric", "mid",
                 "Everyone runs Doom on everything, so I did it with Minecraft. Its very first version, rewritten as one C file with no libraries at all.",
                 bullets=["Plays in a terminal, over telnet, from a 20 KB web page, ==inside a PDF==, and on a bare 486"],
                 inset=("rdgeneric-pdf", "br", 48, -3),
                 notes=[("Inside a PDF!", "red", "right:-6px; bottom:46%", -6)],
                 tilt=-0.6, drop=40, width=96, align="right"),
            card("bedrock", "Minecraft Bedrock on macOS", SITE + "Minecraft-Bedrock-macOS/", "bedrock", "mid",
                 "Bedrock has never had a Mac version. Claude reverse engineered the Windows game in about a day, and now it runs offline on Apple Silicon.",
                 bullets=["A WineGDK bug found on the way, sent upstream with a fix"],
                 tilt=1.2, drop=40, tape="tr", width=92, align="right"),
        ]),
    ]),
    ("automation", "Automation", "oxblood", [
        (1, []),
        (5, [
            card("matiks", "Matiks bot", GH + "Matiks-Bot", "matiks", "mid",
                 "Matiks asked for my resume and then went quiet, so I built a bot that reads each question off the screen and answers it.",
                 bullets=["World rank ==140,000 to 51== in one evening, and then a call with a founder"],
                 tilt=-1.2, drop=40, tape="t", width=92),
        ]),
        (5, [
            card("leetcode", "1337 Bot", GH + "1337-Bot", "leetcode-1337", "mid",
                 "I hated the LeetCode grind, so I automated it. 385 problems in 3 hours, until the rate limits caught up.",
                 bullets=["Then I got hooked, solved 200 by hand in 50 days, and made ==LeetCode Knight== in under 100 days"],
                 inset=("knight", "tr", 28, 6),
                 tilt=0.8, drop=40, width=92, align="right"),
        ]),
        (1, []),
    ]),
    ("open-source", "Open source", "indigo", [
        (4, [
            card("sunpy", "SunPy", "https://github.com/sunpy/sunpy/pulls?q=author%3Apragyaangaur", None, "gh",
                 repo=("sunpy/sunpy", "1,052"),
                 prs=[("merged", 8741, "SUIT map dates drifting out of sync with the header"),
                      ("merged", 8720, "How much orbital eccentricity moves synodic rotation"),
                      ("merged", 8706, "HTML output for single-column time series"),
                      ("open", 8890, "A half-pixel shift when rotating cropped maps"),
                      ("open", 8891, "TimeSeries.sort_index forgetting which class it came from"),
                      ("open", None, "3 more pull requests open, from SOAR searches to on-disk masks"),
                      ("issue", 8750, "Carrying uncertainty through a TimeSeries, starting with sunspot numbers")],
                 logos=[("sunpy.webp", "SunPy", 60)],
                 tilt=-1.0, drop=40, width=96),
        ]),
        (4, [
            card("su2", "SU2", "https://github.com/su2code/SU2/pulls?q=author%3Apragyaangaur", None, "gh",
                 repo=("su2code/SU2", "1,843"),
                 prs=[("merged", 2867, "Broken append and var_names paths in SU2.io"),
                      ("open", 2940, "The heat source fix SkyCatcher's reactor needed"),
                      ("open", 2897, "Hicks-Henne camber deformation under MPI")],
                 logos=[("su2.webp", "SU2", 56)],
                 tilt=0.8, drop=40, width=96),
            card("other-oss", "Other", "https://github.com/pragyaangaur", None, "gh",
                 prs=[("open", 1923, "suitenumerique/meet: drag to resize the split between a screen share and the video"),
                      ("open", 67, "Weather-OS/WineGDK: a memory overwrite found while porting Minecraft Bedrock to the Mac"),
                      ("mail", None, "Paperlane now also arrives as a daily email of new arXiv maths papers")],
                 links=[("Meet #1923", "https://github.com/suitenumerique/meet/pull/1923"), ("WineGDK #67", "https://github.com/Weather-OS/WineGDK/pull/67"),
                        ("Paperlane by email", SITE + "Paperlane/email.html")],
                 tilt=-0.9, drop=40, width=92, align="right"),
        ]),
        (4, [
            card("einsteinpy", "EinsteinPy", "https://github.com/einsteinpy/einsteinpy/pulls?q=author%3Apragyaangaur", None, "gh",
                 repo=("einsteinpy/einsteinpy", "707"),
                 prs=[("merged", 697, "Earth's radius was 6731 km. It is 6371 km."),
                      ("merged", 706, "Bessel function arguments in gravitational waves"),
                      ("merged", 704, "The Sun's constants and \u039b taken from astropy"),
                      ("open", 708, "Lorentz transforms of lower indices, keeping the parent metric"),
                      ("open", 709, "The bubble radius of the Alcubierre warp drive"),
                      ("open", 693, "A test suite that runs under pytest 9, with three tests that could never fail"),
                      ("issue", 692, "Tests that pass no matter what")],
                 logos=[("einsteinpy.webp", "EinsteinPy", 60)],
                 notes=[("Earth shrank by 360 km", "green", "right:4px; top:-32px", 3)],
                 tilt=-0.7, drop=40, width=96, align="right"),
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
                 tilt=1.1, drop=40, tape="tr", width=90, align="right"),
        ]),
        (1, []),
    ]),
    ("random", "Random things", "forest", [
        (4, [
            card("beamline", "Beamline", SITE + "Beamline/", "beamline-chamber", "mid",
                 "A signed random number every ten minutes, mixed from an ANU quantum vacuum device, NOAA solar data and the kernel. It started out as a thermoelectric cloud chamber.",
                 bullets=["596 rounds and a Claude Pro prize, which nobody claimed"],
                 notes=[("Odds: 1 in 13.4 quinquagintillion", "green", "left:0; top:-32px", -2)],
                 links=[("The cloud chamber", GH + "Beamline-Cloud-Chamber")],
                 tilt=-1.0, drop=40, tape="t", width=94),
            card("qiskit", "Qiskit Global Summer School", "https://www.ibm.com/quantum/qiskit", None, "award",
                 bullets=["IBM Quantum, July 2026"],
                 logos=[("qiskit.svg", "Qiskit", 46), ("ibm.svg", "IBM", 24)],
                 tilt=-1.4, drop=40, width=80, align="center"),
            card("fellowships", "Fellowships", "https://www.mercatus.org/emergent-ventures", None, "text",
                 logos=[("mercatus.webp", "Mercatus Center", 34), ("mercedes.webp", "beVisioneers: The Mercedes-Benz Fellowship", 30), ("dexterity.webp", "The Dexterity Global Group", 40)],
                 bullets=["Emergent Ventures, Mercatus Center at George Mason University",
                          "beVisioneers: The Mercedes-Benz Fellowship",
                          "The Dexterity Global Group, graduate and fellow"],
                 tilt=1.0, drop=40, width=92, align="right"),
        ]),
        (4, [
            card("iitd", "Cryo-EM and the porosome, in miniature", GH, None, "mid",
                 "Joachim Frank won the 2017 Nobel Prize in Chemistry for cryo-EM. After his lecture at IIT Delhi with Bhanu P. Jena, I built a small working version of each of their ideas.",
                 pair=("cryoem", "porosome"),
                 bullets=["A ribosome rebuilt from ==2,400 projections==, each of which looks like static on its own",
                          "A vesicle docking at a porosome and releasing its cargo"],
                 notes=[("A thank-you, in code", "red", "right:2%; top:-34px", 3)],
                 tilt=-0.5, drop=30, width=96),
            card("kerf", "Kerf", SITE + "Kerf/", "kerf", "mid",
                 "Version control that understands CAD geometry. Change a bracket and Kerf shows what moved, merges two branches, and refuses a merge that breaks the part.",
                 tilt=0.7, drop=40, width=94),
        ]),
        (4, [
            card("forkestra", "Forkestra", SITE + "Forkestra/", "forkestra", "small",
                 "Paste a GitHub profile and its year plays as an orchestra. Linus Torvalds' year makes a decent song.",
                 tilt=1.2, drop=40, width=90, align="right"),
            card("bardly", "Bardly", SITE + "Bardly/", "bardly", "small",
                 "The inverse of a URL shortener. Paste a link and get a longer one, with Shakespeare in the path.",
                 tilt=-1.3, drop=40, width=84, align="right"),
        ]),
    ]),
]

# Arrows between related cards: (from, to, label, ink).
LINKS = []

# What a card shows once it is opened on its own stage. The story and related cards come from
# stories.py. A demo is the project's own page, loaded only when the visitor asks for it, so the
# board costs nothing extra. Horcrux is left out because its model is a 400 MB download.
DEMOS = {
    "paperlane": (SITE + "Paperlane/", "Read today's issue"),
    "led-doom": (SITE + "LED-Doom/", "Play it"),
    "sunion": (SITE + "Sunion/", "Peel the Sun"),
    "cauchy": (SITE + "Real-Power-Cauchy-Schwarz/", "Try it"),
    "kerf": (SITE + "Kerf/", "Diff and merge some geometry"),
    "forkestra": (SITE + "Forkestra/", "Play a GitHub year"),
    "bardly": (SITE + "Bardly/", "Lengthen a link"),
}
GALLERY = {
    "exhaustion": ["pbe-route"],
    "inkwell": ["ink-home", "ink-quill", "ink-chess", "ink-doom"],
}
try:
    from stories import STORIES
except ImportError:
    STORIES = {}


# Set while a project's own page is being rendered, so related cards link to pages and not to the board.
PAGE = False


def extra(c):
    """The part of a card that only shows on stage, and on the project's own page."""
    s = STORIES.get(c["id"], {})
    parts = []
    if s.get("story"):
        when = f'<span class="when">{escape(s["when"])}</span>' if s.get("when") else ""
        parts.append(f'<p class="story">{when}{ink_marks(s["story"])}</p>')
    if c["id"] in GALLERY:
        parts.append('<div class="gallery">' + "".join(
            f'<img src="{B}{k}.webp" width="{SIZES[k][0]}" height="{SIZES[k][1]}" alt="" loading="lazy">' for k in GALLERY[c["id"]]) + "</div>")
    if c["id"] in DEMOS:
        url, label = DEMOS[c["id"]]
        parts.append(f'<div class="demo"><button type="button" data-src="{escape(url)}">{escape(label)} here ▸</button>'
                     f'<a href="{escape(url)}" target="_blank" rel="noopener">Open in a new tab ↗</a></div>')
    rel = [r for r in s.get("related", ()) if r in TITLES]
    if rel:
        def href(r):
            if not PAGE:
                return f'href="#{r}" data-card="{r}"'
            return f'href="../{r}/"' if r in PAGES else f'href="../../#{r}"'
        parts.append('<p class="related"><span>See also</span>' + "".join(
            f'<a {href(r)}>{escape(TITLES[r])}</a>' for r in rel) + "</p>")
    if not PAGE and c["id"] in PAGES:
        parts.append(f'<p class="own"><span>Its own page</span><a href="{WORK}{c["id"]}/">pragyaangaur.dev/{WORK}{c["id"]}</a></p>')
    return f'<div class="extra">{"".join(parts)}</div>' if parts else ""

INTRO = "This page has no introduction. Have a look around, and you will get an idea of what I like doing."
INTRO_SMALL = "Almost every picture and title links to the real project, paper or demo, so click around and try things."


# GitHub's Octicons (MIT licence), 16 by 16.
OCTICON = {
    "merged": "M5.45 5.154A4.25 4.25 0 0 0 9.25 7.5h1.378a2.251 2.251 0 1 1 0 1.5H9.25A5.734 5.734 0 0 1 5 7.123v3.505a2.25 2.25 0 1 1-1.5 0V5.372a2.25 2.25 0 1 1 1.95-.218ZM4.25 13.5a.75.75 0 1 0 0-1.5.75.75 0 0 0 0 1.5Zm8.5-4.5a.75.75 0 1 0 0-1.5.75.75 0 0 0 0 1.5ZM5 3.25a.75.75 0 1 0 0 .005V3.25Z",
    "open": "M1.5 3.25a2.25 2.25 0 1 1 3 2.122v5.256a2.251 2.251 0 1 1-1.5 0V5.372A2.25 2.25 0 0 1 1.5 3.25Zm5.677-.177L9.573.677A.25.25 0 0 1 10 .854V2.5h1A2.5 2.5 0 0 1 13.5 5v5.628a2.251 2.251 0 1 1-1.5 0V5a1 1 0 0 0-1-1h-1v1.646a.25.25 0 0 1-.427.177L7.177 3.427a.25.25 0 0 1 0-.354ZM3.75 2.5a.75.75 0 1 0 0 1.5.75.75 0 0 0 0-1.5Zm0 9.5a.75.75 0 1 0 0 1.5.75.75 0 0 0 0-1.5Zm8.25.75a.75.75 0 1 0 1.5 0 .75.75 0 0 0-1.5 0Z",
    "issue": "M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3ZM8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z",
    "star": "M8 .25a.75.75 0 0 1 .673.418l1.882 3.815 4.21.612a.75.75 0 0 1 .416 1.279l-3.046 2.97.719 4.192a.751.751 0 0 1-1.088.791L8 12.347l-3.766 1.98a.75.75 0 0 1-1.088-.79l.72-4.194L.818 6.374a.75.75 0 0 1 .416-1.28l4.21-.611L7.327.668A.75.75 0 0 1 8 .25Z",
    "mail": "M1.75 2h12.5c.966 0 1.75.784 1.75 1.75v8.5A1.75 1.75 0 0 1 14.25 14H1.75A1.75 1.75 0 0 1 0 12.25v-8.5C0 2.784.784 2 1.75 2ZM1.5 12.251c0 .138.112.25.25.25h12.5a.25.25 0 0 0 .25-.25V5.809L8.38 9.397a.75.75 0 0 1-.76 0L1.5 5.809v6.442Zm13-8.181v-.32a.25.25 0 0 0-.25-.25H1.75a.25.25 0 0 0-.25.25v.32L8 7.88Z",
    "repo": "M2 2.5A2.5 2.5 0 0 1 4.5 0h8.75a.75.75 0 0 1 .75.75v12.5a.75.75 0 0 1-.75.75h-2.5a.75.75 0 0 1 0-1.5h1.75v-2h-8a1 1 0 0 0-.714 1.7.75.75 0 1 1-1.072 1.05A2.495 2.495 0 0 1 2 11.5Zm10.5-1h-8a1 1 0 0 0-1 1v6.708A2.486 2.486 0 0 1 4.5 9h8ZM5 12.25a.25.25 0 0 1 .25-.25h3.5a.25.25 0 0 1 .25.25v3.25a.25.25 0 0 1-.4.2l-1.45-1.087a.249.249 0 0 0-.3 0L5.4 15.7a.25.25 0 0 1-.4-.2Z",
}


def octicon(name):
    return f'<svg class="oct oct-{name}" viewBox="0 0 16 16" width="16" height="16" aria-hidden="true"><path d="{OCTICON[name]}"/></svg>'


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
    if c["secret"]:
        text, color, pos, rot = c["secret"]
        notes += f'<span class="note secret ink-{color}" style="{pos}; --r:{rot}deg" aria-hidden="true">{escape(text)}</span>'
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
        tag = f'<span class="tag">{escape(c["tag"])} \u25b8</span>' if c["tag"] else ""
        parts.append(f'<div class="pic"{below}><a href="{escape(c["url"])}"{tgt}>{fig}{tag}</a>{notes}</div>')
    if c["repo"]:
        name, stars = c["repo"]
        parts.append(f'<p class="repo">{octicon("repo")}<span>{escape(name)}</span><span class="stars">{octicon("star")} {stars}</span></p>')
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
    if c["prs"]:
        rows = []
        for state, num, text in c["prs"]:
            n = f'<b>#{num}</b> ' if num else ""
            rows.append(f'<li class="pr-{state}">{octicon(state)}<span>{n}{escape(text)}</span></li>')
        parts.append('<ul class="prs">' + "".join(rows) + "</ul>")
    if c["links"]:
        parts.append('<p class="more">' + "".join(f'<a href="{escape(u)}" target="_blank" rel="noopener">{escape(t)} \u2197</a>' for t, u in c["links"]) + "</p>")
    if c["logos"] or c["stamp"]:
        logos = "".join(f'<img src="{LOGO}{f}" alt="{escape(a)}" title="{escape(a)}" style="height:{h}px" loading="lazy">' for f, a, h in c["logos"])
        stamps = [c["stamp"]] if isinstance(c["stamp"], str) else (c["stamp"] or [])
        stamp = "".join(f'<span class="stamp">{escape(t)}</span>' for t in stamps)
        parts.append(f'<div class="logos">{logos}{stamp}</div>')
    parts.append(extra(c))
    return f'<article class="card k-{c["kind"]} ink-{ink}" id="{c["id"]}" style="{style}">\n  ' + "\n  ".join(parts) + "\n</article>"


LINKS_TOP = [
    ("Email", "mailto:pragyaangaur12@gmail.com"),
    ("GitHub", "https://github.com/pragyaangaur"),
    ("LinkedIn", "https://www.linkedin.com/in/pragyaangaur/"),
    ("ORCID", "https://orcid.org/0009-0009-4037-2478"),
    ("Google Scholar", "https://scholar.google.com/citations?user=GomKcxcAAAAJ"),
]


# Every card in board order, with the spread it sits in.
CARDS = [(c, sid, heading, ink) for sid, heading, ink, cols in SPREADS for _, cards in cols for c in cards]
TITLES = {c["id"]: c["title"] for c, _, _, _ in CARDS}

# Each project has a page of its own at pragyaangaur.dev/work/<id>/. The folder keeps these clear of
# the project sites, which GitHub Pages serves at pragyaangaur.dev/<Repo>/. Awards and the list of
# fellowships are not projects, so they stay on the board only.
WORK = "work/"
PAGES = [c["id"] for c, _, _, _ in CARDS if c["kind"] not in ("award", "text")]

# The papers behind the cards, as (title, identifier), taken from llms.txt. A card with one of these
# is described to machines as a scholarly article.
PAPERS = {
    "kmc": ("Rate-independent limits on a sulphating, self-renewing oxide catalyst", "https://doi.org/10.26434/chemrxiv.15009719/v1"),
    "polyhex": ("The maximum area of the convex hull of a polyhex", "https://arxiv.org/abs/2609.30310"),
    "acc": ("A measured neighbourhood of the Andrews-Curtis conjecture", "https://doi.org/10.5281/zenodo.24035724"),
    "magnus": ("Exact turning invariants for projectile motion under quadratic drag and a vertical-axis Magnus force", "https://arxiv.org/abs/2609.30305"),
    "uno": ("How long is a game of Uno? A counting law for large hands and the Wild Draw Four hoard", "https://arxiv.org/abs/2610.14076"),
    "cauchy": ("A Cauchy-Schwarz inequality for real powers", "https://doi.org/10.5281/zenodo.23237507"),
    "exhaustion": ("Proof by exhaustion", "https://doi.org/10.5281/zenodo.23805053"),
    "token": ("The Melting Temperature of a Next-Token Distribution", "https://doi.org/10.5281/zenodo.23219063"),
    "cellblock": ("Cellblock", "https://doi.org/10.5281/zenodo.23510660"),
    "viscous": ("Friction keeps the conservation laws of training alive", "https://doi.org/10.5281/zenodo.23510521"),
    "just-think": ("Left Alone with a Pain Button", "https://doi.org/10.5281/zenodo.23510640"),
    "zap": ("Zap or Deal", "https://doi.org/10.5281/zenodo.23510613"),
}

MONTHS = {m: i + 1 for i, m in enumerate("January February March April May June July August September October November December".split())}
VIDEOS = ("cryoem", "porosome", "led-doom", "rdgeneric", "knee-deep", "fly-brain", "cauchy-cone")
FILTER = ('<svg width="0" height="0" style="position:absolute" aria-hidden="true"><filter id="rough"><feTurbulence type="fractalNoise" '
          'baseFrequency="0.035" numOctaves="2" seed="7"/><feDisplacementMap in="SourceGraphic" scale="2.2"/></filter></svg>')


def plain(text):
    """Card text without the pen marks."""
    return re.sub(r"\[\[|\]\]|==|__|\{\{|\}\}|\*", "", text)


def describe(c):
    return plain(c["caption"] or " ".join(c["bullets"]) or " ".join(t for _, _, t in c["prs"]) or c["title"])


def picture(c):
    """The picture a link preview shows for a card."""
    key = c["media"] or (c["pair"][0] if c["pair"] else None)
    if not key:
        return ORIGIN + "/assets/og.png"
    return f'{ORIGIN}/{B}{key}.{"jpg" if key in VIDEOS else "webp"}'


def month(c):
    """'October 2026' in stories.py becomes 2026-10."""
    when = STORIES.get(c["id"], {}).get("when", "").split()
    return f"{when[1]}-{MONTHS[when[0]]:02d}" if len(when) == 2 and when[0] in MONTHS else None


def outlinks(c):
    """Every place a card points to, as (label, url), without repeats."""
    seen, out = set(), []
    for label, url in [("Project", c["url"])] + list(c["links"]) + ([("Live demo", DEMOS[c["id"]][0])] if c["id"] in DEMOS else []):
        if url not in seen:
            seen.add(url)
            out.append((label, url))
    return out


def ld(*things):
    return dumps({"@context": "https://schema.org", "@graph": list(things)}, ensure_ascii=False).replace("</", "<\\/")


def thing(c):
    """A card as a schema.org object: a paper, a piece of software, or a plain creative work."""
    urls = [u for _, u in outlinks(c)]
    code = next((u for u in urls if u.startswith(GH) and len(u) > len(GH) and "/releases" not in u), None)
    out = {"@id": f"{ORIGIN}/{WORK}{c['id']}/#work", "name": c["title"], "description": describe(c),
           "url": f"{ORIGIN}/{WORK}{c['id']}/", "image": picture(c), "author": {"@id": ORIGIN + "/#person"}}
    if c["id"] in PAPERS:
        title, ident = PAPERS[c["id"]]
        out.update({"@type": "ScholarlyArticle", "name": title, "headline": title, "identifier": ident})
        if title != c["title"]:
            out["alternateName"] = c["title"]
        if code:
            out["isBasedOn"] = code
    elif code:
        out.update({"@type": "SoftwareSourceCode", "codeRepository": code})
    else:
        out["@type"] = "CreativeWork"
    same = [u for u in dict.fromkeys(([PAPERS[c["id"]][1]] if c["id"] in PAPERS else []) + urls) if u != GH.rstrip("/")]
    if same:
        out["sameAs"] = same
    if month(c):
        out["dateCreated"] = month(c)
    return out


def head(title, desc, url, image, root, graph, size=True, alternates=""):
    data = f'<script type="application/ld+json">{graph}</script>\n' if graph else ""
    dims = '<meta property="og:image:width" content="1200">\n<meta property="og:image:height" content="630">\n' if size else ""
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="icon" href="{root}favicon.png" type="image/png">
<link rel="apple-touch-icon" href="{root}apple-touch-icon.png">
<title>{escape(title)}</title>
<meta name="description" content="{escape(desc)}">
<link rel="canonical" href="{url}">
<meta name="author" content="Pragyaan Gaur">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Pragyaan Gaur">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{escape(title)}">
<meta property="og:description" content="{escape(desc)}">
<meta property="og:image" content="{image}">
{dims}<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{escape(title)}">
<meta name="twitter:description" content="{escape(desc)}">
<meta name="twitter:image" content="{image}">
{data}<link rel="preload" href="{root}assets/fonts/LM-regular.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{root}assets/fonts/kalam-400.woff2" as="font" type="font/woff2" crossorigin>
<script>var t;try{{t=localStorage.theme}}catch(e){{}}if(t==="dark")document.documentElement.dataset.theme="dark";document.documentElement.classList.add("js")</script>
<link rel="stylesheet" href="{root}assets/site.css?v={v("assets/site.css")}">
<link rel="stylesheet" href="{root}assets/board.css?v={v("assets/board.css")}">
{alternates}</head>
'''


def bar(root):
    top = "".join(f'<a href="{u}"' + ("" if u.startswith("mailto") else ' target="_blank" rel="noopener"') + f">{t}</a>" for t, u in LINKS_TOP)
    return (f'<nav class="bar" id="top"><a class="name" href="{root or "./"}">Pragyaan Gaur</a><span>{top}'
            f'<button class="lamp" type="button" aria-label="Switch dark mode" title="Lights off"></button></span></nav>')


def board():
    """The home page."""
    spreads = []
    for sid, heading, ink, cols in SPREADS:
        template = " ".join(f"{w}fr" for w, _ in cols)
        colhtml = "".join(f'<div class="col">\n' + "\n".join(render(c, ink) for c in cards) + "\n</div>\n" for _, cards in cols)
        spreads.append(f'<section class="block ink-{ink}" id="{sid}">\n<h2 class="heading">{escape(heading)}</h2>\n'
                       f'<div class="spread" style="--cols:{template}">\n{colhtml}</div>\n</section>')
    links = ";".join(f"{a}>{b}>{escape(t)}>{i}" for a, b, t, i in LINKS)
    toc = "".join(f'<a class="ink-{ink}" href="#{sid}">{escape(h)}</a>' for sid, h, ink, _ in SPREADS)
    site = {"@type": "WebSite", "@id": ORIGIN + "/#site", "url": ORIGIN + "/", "name": "Pragyaan Gaur", "description": DESC,
            "author": {"@id": ORIGIN + "/#person"}, "inLanguage": "en"}
    items = {"@type": "ItemList", "@id": ORIGIN + "/#work", "name": "Projects", "numberOfItems": len(PAGES),
             "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": TITLES[p], "url": f"{ORIGIN}/{WORK}{p}/"} for i, p in enumerate(PAGES)]}
    alternates = (f'<link rel="alternate" type="text/markdown" href="llms.txt" title="For language models">\n'
                  '<link rel="alternate" type="application/json" href="index.json" title="Every project as data">\n')
    body = f'''<body>
{FILTER}
{bar("")}
<header class="intro">
  <p>{escape(INTRO)}</p>
  <p class="small">{escape(INTRO_SMALL)}</p>
  <figure class="contrib" aria-label="GitHub contributions in the last year"><div class="contrib-scroll"></div><figcaption></figcaption></figure>
  <nav class="toc" aria-label="Sections">{toc}</nav>
  <a class="start" href="#{SPREADS[0][0]}">Start here <span aria-hidden="true">↓</span></a>
</header>
<div class="stage" hidden><div class="stage-card" role="dialog" aria-modal="true"></div><button class="stage-close" type="button" aria-label="Close">×</button></div>
<main class="board" data-links="{links}">
{chr(10).join(spreads)}
<svg class="threads" aria-hidden="true"></svg>
</main>
<footer class="end">
  <blockquote class="poem">
    <p>I see the player you mean.</p>
    <p>It has reached a higher level now. It can read our thoughts.</p>
    <p>I like this player. It played well. It did not give up.</p>
  </blockquote>
  <p class="nita"><img src="{LOGO}nita.webp" alt="NIT Agartala" height="34"> NIT Agartala, Engineering Physics</p>
</footer>
<script src="assets/board.js?v={v("assets/board.js")}" defer></script>
</body>
</html>
'''
    return head("Pragyaan Gaur", DESC, ORIGIN + "/", ORIGIN + "/assets/og.png", "", ld(PERSON, site, items), alternates=alternates) + body


def page(i):
    """One project's own page: its card laid flat, with the story, the demo and the related work."""
    global PAGE
    c, sid, heading, ink = next(x for x in CARDS if x[0]["id"] == PAGES[i])
    root, url = "../../", f"{ORIGIN}/{WORK}{c['id']}/"
    PAGE = True
    art = render(c, ink).replace("<h3>", "<h1>", 1).replace("</h3>", "</h1>", 1)
    PAGE = False
    prev, nxt = PAGES[i - 1], PAGES[(i + 1) % len(PAGES)]
    crumbs = {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Pragyaan Gaur", "item": ORIGIN + "/"},
        {"@type": "ListItem", "position": 2, "name": heading, "item": f"{ORIGIN}/#{sid}"},
        {"@type": "ListItem", "position": 3, "name": c["title"], "item": url}]}
    web = {"@type": "WebPage", "@id": url, "url": url, "name": c["title"], "description": describe(c),
           "isPartOf": {"@id": ORIGIN + "/#site"}, "mainEntity": {"@id": url + "#work"}, "primaryImageOfPage": picture(c)}
    person = {"@type": "Person", "@id": ORIGIN + "/#person", "name": "Pragyaan Gaur", "url": ORIGIN + "/"}
    alternates = (f'<link rel="alternate" type="text/markdown" href="index.md" title="This page as Markdown">\n'
                  f'<link rel="alternate" type="application/json" href="{root}index.json" title="Every project as data">\n')
    body = f'''<body class="solo">
{FILTER}
{bar(root)}
<main class="sheet ink-{ink}">
<p class="crumb"><a href="{root}">The board</a><span aria-hidden="true">/</span><a href="{root}#{sid}">{escape(heading)}</a></p>
<div class="stage-card">
{art}
</div>
<nav class="turn" aria-label="More work"><a href="../{prev}/" rel="prev">← {escape(TITLES[prev])}</a><a href="../{nxt}/" rel="next">{escape(TITLES[nxt])} →</a></nav>
</main>
<footer class="end">
  <p class="nita"><img src="{LOGO}nita.webp" alt="NIT Agartala" height="34"> NIT Agartala, Engineering Physics</p>
</footer>
<script src="assets/page.js?v={v("assets/page.js")}" defer></script>
</body>
</html>
'''
    # The page sits two folders down, so its own files are reached through the root.
    return head(f"{c['title']} · Pragyaan Gaur", describe(c), url, picture(c), root, ld(web, thing(c), crumbs, person),
                size=False, alternates=alternates) + re.sub(r'(src|poster|href)="(assets/)', rf'\1="{root}\2', body)


def markdown(c, heading):
    """The same page for a language model, in plain Markdown."""
    s = STORIES.get(c["id"], {})
    out = [f"# {c['title']}", ""]
    if c["caption"]:
        out += ["> " + plain(c["caption"]), ""]
    facts = [x for x in (c["meta"], s.get("when"), "Section: " + heading) if x]
    out += [". ".join(facts) + ".", ""]
    if c["id"] in PAPERS:
        out += [f"Paper: [{PAPERS[c['id']][0]}]({PAPERS[c['id']][1]})", ""]
    if c["quote"]:
        out += [f"“{c['quote'][0]}” ({c['quote'][1]})", ""]
    rows = [plain(b) for b in c["bullets"]] + [f"{state.capitalize()}{f' #{num}' if num else ''}: {text}" for state, num, text in c["prs"]]
    if rows:
        out += ["## Results", ""] + ["- " + r for r in rows] + [""]
    if s.get("story"):
        out += ["## Story", "", s["story"], ""]
    out += ["## Links", ""] + [f"- [{label}]({url})" for label, url in outlinks(c)] + [""]
    rel = [r for r in s.get("related", ()) if r in PAGES]
    if rel:
        out += ["## See also", ""] + [f"- [{TITLES[r]}]({ORIGIN}/{WORK}{r}/index.md)" for r in rel] + [""]
    out += [f"By [Pragyaan Gaur]({ORIGIN}/). The full index is at {ORIGIN}/llms.txt and {ORIGIN}/index.json."]
    return "\n".join(out) + "\n"


def record(c, sid, heading):
    """A card as one entry of index.json."""
    s = STORIES.get(c["id"], {})
    has = c["id"] in PAGES
    out = {"id": c["id"], "title": c["title"], "section": heading,
           "page": f"{ORIGIN}/{WORK}{c['id']}/" if has else f"{ORIGIN}/#{c['id']}",
           "markdown": f"{ORIGIN}/{WORK}{c['id']}/index.md" if has else None,
           "url": c["url"], "description": describe(c), "role": c["meta"] or None, "when": month(c),
           "results": [plain(b) for b in c["bullets"]],
           "contributions": [{"state": state, "number": num, "text": text} for state, num, text in c["prs"]],
           "paper": dict(zip(("title", "identifier"), PAPERS[c["id"]])) if c["id"] in PAPERS else None,
           "links": [{"label": label, "url": url} for label, url in outlinks(c)],
           "story": s.get("story") or None, "related": [r for r in s.get("related", ()) if r in TITLES]}
    return {k: val for k, val in out.items() if val not in (None, [], "")}


def write(path, text):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w") as f:
        f.write(text)


def build():
    write("index.html", board())
    # Pages of cards that have left the board go too.
    for old in os.listdir(WORK) if os.path.isdir(WORK) else ():
        if old not in PAGES and os.path.isdir(WORK + old):
            shutil.rmtree(WORK + old)
    for i, pid in enumerate(PAGES):
        c, sid, heading, ink = next(x for x in CARDS if x[0]["id"] == pid)
        write(f"{WORK}{pid}/index.html", page(i))
        write(f"{WORK}{pid}/index.md", markdown(c, heading))
    write("index.json", dumps({
        "site": ORIGIN + "/", "about": "Every card on pragyaangaur.dev as data. The same facts are on the board and in llms.txt.",
        "person": {"name": "Pragyaan Gaur", "affiliation": "National Institute of Technology Agartala",
                   "email": "pragyaangaur12@gmail.com", "profiles": [u for _, u in LINKS_TOP[1:]]},
        "sections": [{"id": sid, "title": heading, "url": f"{ORIGIN}/#{sid}"} for sid, heading, _, _ in SPREADS],
        "projects": [record(c, sid, heading) for c, sid, heading, _ in CARDS]}, ensure_ascii=False, indent=1) + "\n")
    write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {ORIGIN}/sitemap.xml\n")
    today = __import__("datetime").date.today().isoformat()
    urls = "".join(f"  <url><loc>{ORIGIN}/{p}</loc><lastmod>{today}</lastmod></url>\n" for p in [""] + [f"{WORK}{p}/" for p in PAGES])
    write("sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')
    print(f"index.html written, {len(CARDS)} cards in {len(SPREADS)} spreads, {len(PAGES)} project pages")


if __name__ == "__main__":
    build()
