#!/usr/bin/env python3
"""Turn wiki-sourced character art into uniform dex portraits.

Input : images/wiki/<slug>.<ext>   (art pulled from the member's Wikipedia article)
Output: images/heroes/<slug>.jpg   (720x720, artwork centred on the member's own
                                   crest palette so every card matches)

Each source file is recorded in images/wiki/CREDITS.json as
    { "<slug>": { "article": "<wikipedia url>", "file": "<original name>" } }
so the artwork stays attributed. Re-run after adding new files:
    python3 tools/prep_wiki_art.py
"""
import json, os, subprocess, sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
WIKI = os.path.join(ROOT, "images", "wiki")
OUT = os.path.join(ROOT, "images", "heroes")
CREDITS = os.path.join(WIKI, "CREDITS.json")
SIZE = 720


def accents():
    """slug -> (deep, accent) from the generated crest palette file."""
    out = {}
    path = os.path.join(ROOT, "js", "accents.js")
    if not os.path.exists(path):
        return out
    for line in open(path):
        line = line.strip()
        if not line.startswith('"'):
            continue
        slug = line.split('"')[1]
        acc = line.split('accent: "')[1].split('"')[0]
        deep = line.split('deep: "')[1].split('"')[0]
        out[slug] = (deep, acc)
    return out


def run(cmd):
    subprocess.run(cmd, check=True)


def main():
    if not os.path.isdir(WIKI):
        print("no images/wiki directory yet")
        return
    pal = accents()
    credits = json.load(open(CREDITS)) if os.path.exists(CREDITS) else {}
    os.makedirs(OUT, exist_ok=True)
    made = 0
    for name in sorted(os.listdir(WIKI)):
        slug, ext = os.path.splitext(name)
        if ext.lower() not in (".jpg", ".jpeg", ".png", ".webp", ".gif"):
            continue
        src = os.path.join(WIKI, name)
        dst = os.path.join(OUT, slug + ".jpg")
        deep, accent = pal.get(slug, ("#0b1020", "#c9a227"))
        raw, ground, art, flat = ("/tmp/jldex_raw.png", "/tmp/jldex_ground.png",
                                  "/tmp/jldex_art.png", "/tmp/jldex_flat.png")
        # 1. drop the white page, keep the figure only
        run(["convert", src, "-background", "white", "-alpha", "remove",
             "-fuzz", "8%", "-trim", "+repage", "-fuzz", "8%", "-transparent", "white",
             "-channel", "A", "-threshold", "12%", "+channel", raw])
        # 2. dark panel ground with a muted glow of the member's own crest accent
        run(["convert", "-size", "%dx%d" % (SIZE, SIZE),
             "radial-gradient:%s-%s" % (accent, deep),
             "-modulate", "42,62,100", "-blur", "0x14", ground])
        # 3. figure scaled to fill ~92% of the panel, then centred
        run(["convert", raw, "-resize", "%dx%d" % (int(SIZE * 0.92), int(SIZE * 0.92)), art])
        run(["convert", ground, art, "-gravity", "center", "-composite",
             "-quality", "86", dst])
        made += 1
        print("prepared", slug)
    print("portraits prepared:", made)
    if credits:
        print("credits recorded:", len(credits))


if __name__ == "__main__":
    main()
