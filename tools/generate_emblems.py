#!/usr/bin/env python3
"""Generate JL-Dex member emblem art (512x512 SVG) into images/.

Each member gets a unique crest: hero colour gradient, halftone field and a
bold vector emblem drawn on a 100x100 grid scaled into the 512px canvas.
Run:  python3 tools/generate_emblems.py
"""
import os, math

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "images")

# ---------------------------------------------------------------- glyphs ----
def g_shield(fg, badge):
    return f'''<path d="M50 6 L90 22 V54 C90 76 70 90 50 96 C30 90 10 76 10 54 V22 Z"
      fill="{fg}"/>
      <path d="M50 16 L80 28 V53 C80 70 65 81 50 86 C35 81 20 70 20 53 V28 Z" fill="{badge}"/>
      <path d="M64 34 C50 26 36 32 38 44 C40 53 60 53 63 62 C66 72 50 76 38 68"
        fill="none" stroke="{fg}" stroke-width="7" stroke-linecap="round"/>'''

def g_bat(fg, badge):
    return f'''<path d="M50 20 C48 30 44 36 38 40 C28 32 16 32 6 40 C12 44 14 50 14 58
      C22 52 30 52 36 58 C40 62 44 68 46 78 C48 70 49 62 50 56 C51 62 52 70 54 78
      C56 68 60 62 64 58 C70 52 78 52 86 58 C86 50 88 44 94 40 C84 32 72 32 62 40
      C56 36 52 30 50 20 Z" fill="{fg}"/>
      <path d="M40 66 L46 60 L50 68 L54 60 L60 66 L50 80 Z" fill="{badge}"/>'''

def g_w(fg, badge):
    return f'''<path d="M14 26 L32 78 L50 44 L68 78 L86 26 L74 26 L64 58 L52 30 L48 30 L36 58 L26 26 Z"
      fill="{fg}"/>
      <path d="M20 8 L36 20 L50 6 L64 20 L80 8 L78 24 L50 16 L22 24 Z" fill="{badge}"/>'''

def g_bolt(fg, badge):
    return f'''<path d="M60 4 L24 52 L44 52 L36 96 L76 44 L54 44 L66 4 Z" fill="{fg}"/>
      <path d="M60 4 L54 44 L66 44 L76 44 L56 74 L44 52 L60 4 Z" fill="{badge}" opacity="0.35"/>'''

def g_lantern(fg, badge):
    return f'''<circle cx="50" cy="26" r="9" fill="{fg}"/>
      <path d="M30 36 H70 L66 44 H34 Z" fill="{fg}"/>
      <path d="M32 48 H68 L64 84 C64 88 60 92 50 92 C40 92 36 88 36 84 Z" fill="{fg}"/>
      <path d="M40 56 H60 L58 80 C58 82 55 84 50 84 C45 84 42 82 42 80 Z" fill="{badge}"/>
      <path d="M50 92 V98" stroke="{fg}" stroke-width="5" stroke-linecap="round"/>
      <circle cx="84" cy="70" r="12" fill="none" stroke="{badge}" stroke-width="5"/>
      <circle cx="50" cy="30" r="4" fill="{badge}"/>'''

def g_trident(fg, badge):
    return f'''<path d="M48 22 H52 V92 H48 Z" fill="{fg}"/>
      <path d="M18 14 V44 C18 56 30 62 50 62 C70 62 82 56 82 44 V14 H74 V44
        C74 52 64 56 50 56 C36 56 26 52 26 44 V14 Z" fill="{fg}"/>
      <path d="M28 6 H36 V40 H28 Z M64 6 H72 V40 H64 Z M46 4 H54 V22 H46 Z" fill="{badge}"/>
      <circle cx="50" cy="76" r="6" fill="{badge}"/>'''

def g_mars(fg, badge):
    return f'''<path d="M50 8 C27 8 15 25 15 47 C15 63 19 75 25 88 L34 75
      C38 79 62 79 66 75 L75 88 C81 75 85 63 85 47 C85 25 73 8 50 8 Z" fill="{fg}"/>
      <path d="M28 22 L50 6 L72 22" stroke="{badge}" stroke-width="5" fill="none" stroke-linecap="round"/>
      <circle cx="37" cy="45" r="7" fill="{badge}"/>
      <circle cx="63" cy="45" r="7" fill="{badge}"/>
      <path d="M38 64 C44 70 56 70 62 64" stroke="{badge}" stroke-width="5" fill="none" stroke-linecap="round"/>'''

def g_cyborg(fg, badge):
    return f'''<path d="M50 8 C26 8 10 26 10 50 C10 74 26 92 50 92 C74 92 90 74 90 50 C90 26 74 8 50 8 Z"
      fill="none" stroke="{fg}" stroke-width="7"/>
      <path d="M50 8 V92 M50 30 H90 M50 70 H90 M70 8 V92 M30 20 H50 M30 70 H50" stroke="{badge}"
        stroke-width="4" opacity="0.85"/>
      <circle cx="32" cy="48" r="9" fill="{fg}"/>
      <circle cx="68" cy="48" r="9" fill="{fg}"/>
      <path d="M34 68 H66" stroke="{fg}" stroke-width="6" stroke-linecap="round"/>'''

def g_arrow(fg, badge):
    return f'''<path d="M34 6 C10 32 10 68 34 94" fill="none" stroke="{fg}" stroke-width="9"
        stroke-linecap="round"/>
      <path d="M34 6 L34 94" stroke="{badge}" stroke-width="3" opacity="0.9"/>
      <path d="M20 50 H82" stroke="{fg}" stroke-width="8" stroke-linecap="round"/>
      <path d="M94 50 L74 39 L74 61 Z" fill="{badge}"/>
      <path d="M20 50 L34 40 M20 50 L34 60 M30 50 L44 40 M30 50 L44 60" stroke="{badge}"
        stroke-width="5" fill="none" stroke-linecap="round"/>'''

def g_bird(fg, badge):
    return f'''<path d="M14 62 C26 60 36 52 44 40 L38 26 L52 34 L62 20 L64 36 C76 40 84 50 86 62
      C74 58 62 60 54 68 C44 78 30 80 20 74 Z" fill="{fg}"/>
      <path d="M62 20 L84 10 L70 24 Z" fill="{badge}"/>
      <circle cx="58" cy="38" r="4" fill="{badge}"/>
      <path d="M50 46 L50 60 M58 44 L56 60 M66 46 L62 60" stroke="{badge}" stroke-width="4"/>'''

def g_wing(fg, badge):
    return f'''<path d="M8 46 C30 36 54 42 84 66 C70 64 58 64 48 68 C40 82 26 88 12 86
      C20 76 22 62 20 52 C16 49 12 47 8 46 Z" fill="{fg}"/>
      <path d="M24 54 C40 54 52 58 66 68" stroke="{badge}" stroke-width="5" fill="none"/>
      <path d="M26 64 C40 64 48 68 58 76" stroke="{badge}" stroke-width="5" fill="none"/>
      <circle cx="70" cy="26" r="13" fill="{fg}"/>
      <path d="M80 26 L96 32 L80 40 Z" fill="{badge}"/>
      <path d="M66 14 L60 4 M74 14 L80 4" stroke="{badge}" stroke-width="5" stroke-linecap="round"/>'''

def g_hat(fg, badge):
    return f'''<path d="M28 46 H72 V16 H28 Z" fill="{fg}"/>
      <path d="M18 46 H82 V56 H18 Z" fill="{fg}"/>
      <path d="M32 48 H68 V22 H32 Z" fill="{badge}"/>
      <path d="M40 44 L50 26 L60 44 Z" fill="{fg}"/>
      <path d="M72 62 L88 88" stroke="{fg}" stroke-width="7" stroke-linecap="round"/>
      <path d="M76 24 L80 34 L90 34 L82 40 L85 50 L76 44 L67 50 L70 40 L62 34 L72 34 Z" fill="{badge}"/>'''

def g_ankh(fg, badge):
    return f'''<circle cx="50" cy="28" r="18" fill="none" stroke="{fg}" stroke-width="9"/>
      <path d="M46 44 H54 V94 H46 Z" fill="{fg}"/>
      <path d="M20 58 H80 V68 H20 Z" fill="{fg}"/>
      <circle cx="50" cy="28" r="8" fill="{badge}"/>
      <circle cx="50" cy="63" r="5" fill="{badge}"/>'''

def g_atom(fg, badge):
    return f'''<ellipse cx="50" cy="50" rx="40" ry="16" fill="none" stroke="{fg}" stroke-width="6"/>
      <ellipse cx="50" cy="50" rx="40" ry="16" fill="none" stroke="{fg}" stroke-width="6"
        transform="rotate(60 50 50)"/>
      <ellipse cx="50" cy="50" rx="40" ry="16" fill="none" stroke="{fg}" stroke-width="6"
        transform="rotate(-60 50 50)"/>
      <circle cx="50" cy="50" r="12" fill="{fg}"/>
      <circle cx="50" cy="50" r="6" fill="{badge}"/>'''

def g_flame(fg, badge):
    return f'''<path d="M50 6 C64 26 78 38 78 58 C78 78 66 92 50 92 C34 92 22 78 22 58
      C22 42 34 32 40 20 C42 34 48 40 52 44 C52 32 50 20 50 6 Z" fill="{fg}"/>
      <circle cx="50" cy="66" r="10" fill="{badge}"/>
      <ellipse cx="50" cy="66" rx="20" ry="7" fill="none" stroke="{badge}" stroke-width="3"
        transform="rotate(35 50 66)"/>
      <ellipse cx="50" cy="66" rx="20" ry="7" fill="none" stroke="{badge}" stroke-width="3"
        transform="rotate(-35 50 66)"/>'''

def g_fox(fg, badge):
    return f'''<path d="M14 22 L30 40 L50 44 L70 40 L86 22 L84 50 C84 74 68 92 50 92
      C32 92 16 74 16 50 Z" fill="{fg}"/>
      <path d="M30 58 L42 68 L50 56 L58 68 L70 58" fill="none" stroke="{badge}" stroke-width="6"
        stroke-linecap="round"/>
      <circle cx="36" cy="48" r="4" fill="{badge}"/>
      <circle cx="64" cy="48" r="4" fill="{badge}"/>'''

def g_star(fg, badge, points=6):
    pts = []
    for i in range(points * 2):
        r = 46 if i % 2 == 0 else 18
        a = -math.pi / 2 + i * math.pi / points
        pts.append(f"{50 + r * math.cos(a):.1f},{50 + r * math.sin(a):.1f}")
    poly = " ".join(pts)
    return f'<polygon points="{poly}" fill="{fg}"/><circle cx="50" cy="50" r="10" fill="{badge}"/>'

def g_beetle(fg, badge):
    return f'''<ellipse cx="50" cy="56" rx="26" ry="34" fill="{fg}"/>
      <path d="M50 22 V90" stroke="{badge}" stroke-width="4"/>
      <path d="M50 32 C38 26 30 18 28 10" stroke="{badge}" stroke-width="4" fill="none"/>
      <path d="M50 32 C62 26 70 18 72 10" stroke="{badge}" stroke-width="4" fill="none"/>
      <path d="M24 40 L10 30 M24 56 L8 54 M24 72 L10 82 M76 40 L90 30 M76 56 L92 54
        M76 72 L90 82" stroke="{fg}" stroke-width="6" stroke-linecap="round"/>
      <circle cx="36" cy="38" r="5" fill="{badge}"/>
      <circle cx="64" cy="38" r="5" fill="{badge}"/>'''

def g_scarab(fg, badge):
    return f'''<ellipse cx="50" cy="58" rx="22" ry="30" fill="{fg}"/>
      <circle cx="50" cy="26" r="14" fill="{fg}"/>
      <path d="M50 14 L50 6 M38 18 L30 8 M62 18 L70 8" stroke="{fg}" stroke-width="5"
        stroke-linecap="round"/>
      <path d="M28 40 L8 30 L20 50 L6 56 L24 62 L14 84 L32 74" fill="{fg}"/>
      <path d="M72 40 L92 30 L80 50 L94 56 L76 62 L86 84 L68 74" fill="{fg}"/>
      <circle cx="50" cy="58" r="8" fill="{badge}"/>
      <path d="M50 30 V86 M40 44 H60" stroke="{badge}" stroke-width="3"/>'''

def g_hammer(fg, badge):
    return f'''<path d="M46 30 H54 V94 H46 Z" fill="{fg}"/>
      <path d="M14 10 H86 V34 H14 Z" fill="{fg}"/>
      <path d="M24 18 H76 V26 H24 Z" fill="{badge}"/>
      <path d="M20 34 H80 L74 44 H26 Z" fill="{fg}"/>
      <circle cx="50" cy="86" r="7" fill="{badge}"/>'''

def g_paw(fg, badge):
    return f'''<circle cx="50" cy="66" r="22" fill="{fg}"/>
      <ellipse cx="24" cy="46" rx="9" ry="12" fill="{fg}"/>
      <ellipse cx="40" cy="32" rx="9" ry="13" fill="{fg}"/>
      <ellipse cx="60" cy="32" rx="9" ry="13" fill="{fg}"/>
      <ellipse cx="76" cy="46" rx="9" ry="12" fill="{fg}"/>
      <path d="M40 66 H60 M50 56 V78" stroke="{badge}" stroke-width="5" stroke-linecap="round"/>'''

def g_leaf(fg, badge):
    return f'''<path d="M50 8 C74 22 88 44 88 62 C88 80 72 92 50 92 C28 92 12 80 12 62
      C12 44 26 22 50 8 Z" fill="{fg}"/>
      <path d="M50 12 V86" stroke="{badge}" stroke-width="5"/>
      <path d="M50 34 L34 26 M50 34 L66 26 M50 52 L30 44 M50 52 L70 44 M50 70 L34 62 M50 70 L66 62"
        stroke="{badge}" stroke-width="4" fill="none"/>'''

def g_sigil(fg, badge):
    return f'''<circle cx="50" cy="50" r="40" fill="none" stroke="{fg}" stroke-width="6"/>
      <path d="M50 12 L78 78 H22 Z" fill="none" stroke="{fg}" stroke-width="6"/>
      <path d="M50 12 V78" stroke="{badge}" stroke-width="4"/>
      <circle cx="50" cy="50" r="12" fill="{fg}"/>
      <path d="M50 50 L78 78 M50 50 L22 78 M50 50 L50 12" stroke="{badge}" stroke-width="3"/>'''

def g_waves(fg, badge):
    return f'''<circle cx="50" cy="50" r="12" fill="{fg}"/>
      <path d="M26 26 C14 38 14 62 26 74 M74 26 C86 38 86 62 74 74" stroke="{fg}"
        stroke-width="7" fill="none" stroke-linecap="round"/>
      <path d="M12 12 C-6 32 -6 68 12 88 M88 12 C106 32 106 68 88 88" stroke="{badge}"
        stroke-width="6" fill="none" stroke-linecap="round"/>
      <path d="M50 62 V84" stroke="{badge}" stroke-width="5" stroke-linecap="round"/>'''

def g_snow(fg, badge):
    arms = []
    for i in range(6):
        a = i * 60
        arms.append(f'<g transform="rotate({a} 50 50)"><path d="M50 50 V10" stroke="{fg}" '
                    f'stroke-width="6" stroke-linecap="round"/>'
                    f'<path d="M50 22 L40 14 M50 22 L60 14 M50 36 L42 30 M50 36 L58 30" '
                    f'stroke="{fg}" stroke-width="5" stroke-linecap="round"/></g>')
    return "".join(arms) + f'<circle cx="50" cy="50" r="10" fill="{badge}"/>'

def g_hex(fg, badge, inner):
    return f'''<path d="M50 6 L88 28 V72 L50 94 L12 72 V28 Z" fill="{fg}"/>
      <path d="M50 16 L79 33 V67 L50 84 L21 67 V33 Z" fill="{badge}"/>
      {inner}'''

def g_skull(fg, badge):
    return f'''<path d="M50 10 C30 10 18 24 18 44 C18 58 24 66 30 72 C33 75 34 80 34 86
      H66 C66 80 67 75 70 72 C76 66 82 58 82 44 C82 24 70 10 50 10 Z" fill="{fg}"/>
      <circle cx="38" cy="44" r="8" fill="{badge}"/>
      <circle cx="62" cy="44" r="8" fill="{badge}"/>
      <path d="M50 56 L44 66 H56 Z" fill="{badge}"/>
      <path d="M40 86 V94 M50 86 V96 M60 86 V94" stroke="{fg}" stroke-width="5"
        stroke-linecap="round"/>'''

def g_burst(fg, badge):
    rays = []
    for i in range(12):
        a = i * 30
        rays.append(f'<g transform="rotate({a} 50 50)"><path d="M50 2 L56 26 L44 26 Z" fill="{fg}"/></g>')
    return "".join(rays) + f'<circle cx="50" cy="50" r="24" fill="{fg}"/><circle cx="50" cy="50" r="12" fill="{badge}"/>'

def g_raven(fg, badge):
    return f'''<path d="M16 78 C30 74 40 64 46 50 L40 32 L56 40 L70 22 L68 44 C82 50 88 62 90 78
      C76 72 60 74 48 82 C38 88 24 86 16 78 Z" fill="{fg}"/>
      <circle cx="52" cy="34" r="4" fill="{badge}"/>
      <path d="M44 60 L38 74 M52 60 L48 76" stroke="{badge}" stroke-width="4"/>
      <path d="M30 26 L40 16 L44 30 L58 20 L60 34" stroke="{badge}" stroke-width="4" fill="none"/>'''

def g_tornado(fg, badge):
    return f'''<path d="M10 20 H90 L74 34 H26 Z" fill="{fg}"/>
      <path d="M22 40 H78 L64 54 H36 Z" fill="{fg}"/>
      <path d="M32 60 H68 L58 74 H42 Z" fill="{fg}"/>
      <circle cx="50" cy="86" r="8" fill="{badge}"/>
      <path d="M16 20 C40 14 62 26 84 20" stroke="{badge}" stroke-width="4" fill="none"/>'''

def g_ribbon(fg, badge):
    return f'''<path d="M12 64 C12 22 34 12 50 24 C66 36 60 62 78 62 C90 62 94 50 94 40"
      fill="none" stroke="{fg}" stroke-width="14" stroke-linecap="round"/>
      <circle cx="16" cy="66" r="10" fill="{fg}"/>
      <circle cx="86" cy="36" r="9" fill="{badge}"/>
      <path d="M36 30 C48 40 44 56 60 56" stroke="{badge}" stroke-width="4" fill="none"/>'''

def g_loop(fg, badge):
    return f'''<path d="M22 84 C22 40 34 16 50 16 C66 16 78 40 78 84" fill="none"
      stroke="{fg}" stroke-width="13" stroke-linecap="round"/>
      <circle cx="22" cy="84" r="11" fill="{fg}"/>
      <circle cx="78" cy="84" r="11" fill="{fg}"/>
      <circle cx="50" cy="20" r="9" fill="{badge}"/>
      <path d="M32 62 H68" stroke="{badge}" stroke-width="5" stroke-dasharray="6 8"/>'''

def g_shield_bolt(fg, badge):
    return f'''<path d="M50 6 L90 22 V54 C90 76 70 90 50 96 C30 90 10 76 10 54 V22 Z" fill="{fg}"/>
      <path d="M50 16 L80 28 V53 C80 70 65 81 50 86 C35 81 20 70 20 53 V28 Z" fill="{badge}"/>
      <path d="M58 30 L38 56 L50 56 L44 82 L64 52 L51 52 Z" fill="{fg}"/>'''

def g_wingman(fg, badge):  # nightwing-style wing chevron
    return f'''<path d="M50 6 L84 26 L64 40 L88 56 L60 54 L66 86 L50 66 L34 86 L40 54
      L12 56 L36 40 L16 26 Z" fill="{fg}"/>
      <circle cx="50" cy="48" r="10" fill="{badge}"/>'''

def g_mask(fg, badge):
    return f'''<path d="M8 40 C24 26 40 22 50 30 C60 22 76 26 92 40 C82 62 68 74 50 74
      C32 74 18 62 8 40 Z" fill="{fg}"/>
      <path d="M22 40 C28 36 34 36 38 40 C34 44 28 44 22 40 Z" fill="{badge}"/>
      <path d="M62 40 C66 36 72 36 78 40 C72 44 66 44 62 40 Z" fill="{badge}"/>'''

def g_boot(fg, badge):  # generic hero rune
    return f'''<path d="M50 6 L62 34 L92 34 L68 54 L78 88 L50 68 L22 88 L32 54 L8 34 L38 34 Z"
      fill="{fg}"/>
      <circle cx="50" cy="52" r="12" fill="{badge}"/>'''

GLYPHS = {
    "shield": g_shield, "bat": g_bat, "w": g_w, "bolt": g_bolt, "lantern": g_lantern,
    "trident": g_trident, "mars": g_mars, "cyborg": g_cyborg, "arrow": g_arrow,
    "bird": g_bird, "wing": g_wing, "hat": g_hat, "ankh": g_ankh, "atom": g_atom,
    "flame": g_flame, "fox": g_fox, "star": g_star, "beetle": g_beetle, "scarab": g_scarab,
    "hammer": g_hammer, "paw": g_paw, "leaf": g_leaf, "sigil": g_sigil, "waves": g_waves,
    "snow": g_snow, "hex": g_hex, "skull": g_skull, "burst": g_burst, "raven": g_raven,
    "tornado": g_tornado, "ribbon": g_ribbon, "loop": g_loop, "shield_bolt": g_shield_bolt,
    "wingman": g_wingman, "mask": g_mask, "boot": g_boot,
}

# --------------------------------------------------------------- members ----
# slug: (c1, c2, glyph, fg, badge, extra-glyph-arg)
M = {
 "superman":              ("#0b3d91", "#d81f2a", "shield", "#ffe14d", "#0b3d91", None),
 "batman":                ("#111111", "#3b3f5c", "bat", "#f2c21b", "#111111", None),
 "wonder-woman":          ("#a4182a", "#0b3d91", "w", "#ffd23f", "#a4182a", None),
 "flash-barry":           ("#8f1b12", "#d8a300", "bolt", "#ffe14d", "#8f1b12", None),
 "green-lantern-hal":     ("#0a3d24", "#0f7a3d", "lantern", "#6df28a", "#0a3d24", None),
 "aquaman":               ("#06344a", "#0aa0a8", "trident", "#ffd98a", "#06344a", None),
 "martian-manhunter":     ("#0d3a2e", "#2f9f77", "mars", "#8df0c2", "#0d3a2e", None),
 "cyborg":                ("#12203a", "#2f6fe4", "cyborg", "#8fd0ff", "#12203a", None),
 "green-arrow":           ("#14401f", "#4cb04a", "arrow", "#8bf08a", "#14401f", None),
 "black-canary":          ("#12121e", "#2b2b52", "bird", "#ffd23f", "#12121e", None),
 "flash-wally":           ("#7d1010", "#e2b100", "bolt", "#fff0a0", "#7d1010", None),
 "green-lantern-john":    ("#08301c", "#12924a", "lantern", "#7bff9e", "#08301c", None),
 "green-lantern-kyle":    ("#0a2540", "#1f9c6b", "lantern", "#9ef7c0", "#0a2540", None),
 "green-lantern-guy":     ("#123a1a", "#57a72e", "lantern", "#d6ff7a", "#123a1a", None),
 "hawkgirl":              ("#2a1420", "#a8332b", "wing", "#f4d58d", "#2a1420", None),
 "hawkman":               ("#241a10", "#7a5230", "wing", "#f0c583", "#241a10", None),
 "zatanna":               ("#1a1030", "#6c34c9", "hat", "#e8d7ff", "#1a1030", None),
 "doctor-fate":           ("#0d1f3a", "#1f4fa8", "ankh", "#ffd75e", "#0d1f3a", None),
 "atom":                  ("#101c33", "#2fa7a0", "atom", "#9ff2ee", "#101c33", None),
 "shazam":                ("#7a1010", "#f0b400", "bolt", "#fff3a8", "#7a1010", None),
 "plastic-man":           ("#7a1515", "#e05a1e", "ribbon", "#ffe0b0", "#7a1515", None),
 "elongated-man":         ("#5a1030", "#c94b7a", "loop", "#ffe1ee", "#5a1030", None),
 "red-tornado":           ("#5a0d0d", "#b52a2a", "tornado", "#ffd9b0", "#5a0d0d", None),
 "firestorm":             ("#8a2b06", "#f0a000", "flame", "#ffe79a", "#8a2b06", None),
 "vixen":                 ("#7a4a08", "#d99a1f", "fox", "#ffe6b0", "#7a4a08", None),
 "booster-gold":          ("#123a6b", "#f2c21b", "star", "#ffe14d", "#123a6b", None),
 "blue-beetle-ted":       ("#0b2a66", "#2f6fe4", "beetle", "#8fc4ff", "#0b2a66", None),
 "blue-beetle-jaime":     ("#0a2b5c", "#3a86ff", "scarab", "#a9d6ff", "#0a2b5c", None),
 "supergirl":             ("#0b3d91", "#c0283a", "shield", "#ffe14d", "#0b3d91", None),
 "power-girl":            ("#1b1230", "#c02a6a", "shield_bolt", "#ffe9f2", "#1b1230", None),
 "batgirl":               ("#161a2e", "#6b3fa0", "mask", "#f2c21b", "#161a2e", None),
 "nightwing":             ("#0a1030", "#1f4fd8", "wingman", "#7fb0ff", "#0a1030", None),
 "steel":                 ("#3a2a12", "#b7862b", "hammer", "#ffe1a0", "#3a2a12", None),
 "animal-man":            ("#123126", "#3f9c5a", "paw", "#d8ffcf", "#123126", None),
 "swamp-thing":           ("#10261a", "#2f7a3a", "leaf", "#c8ffb8", "#10261a", None),
 "constantine":           ("#241a10", "#7a5a2a", "sigil", "#ffe1a0", "#241a10", None),
 "black-lightning":       ("#101828", "#2f4fd8", "bolt", "#a9c4ff", "#101828", None),
 "vibe":                  ("#102a3a", "#e0a020", "waves", "#ffe6a0", "#102a3a", None),
 "killer-frost":          ("#0a2a4a", "#7fd8ff", "snow", "#d8f6ff", "#0a2a4a", None),
 "lex-luthor":            ("#1a1a1a", "#5a5a5a", "hex", "#e8e8e8", "#1a1a1a", "L"),
 "lobo":                  ("#1a1020", "#5a2a6a", "skull", "#e8d8f0", "#1a1020", None),
 "starfire":              ("#5a1030", "#e06a1e", "burst", "#ffe0a0", "#5a1030", None),
 "raven":                 ("#150a2a", "#4a2a8a", "raven", "#d8c8ff", "#150a2a", None),
 "beast-boy":             ("#0f3a1a", "#4ac04a", "paw", "#d8ffbf", "#0f3a1a", None),
 "green-lantern-simon":   ("#0a3a24", "#159a4a", "lantern", "#8bffae", "#0a3a24", None),
 "green-lantern-jessica": ("#0c2a4a", "#1f9a7a", "lantern", "#a8ffe0", "#0c2a4a", None),
 "hawkgirl-kendra":       ("#2a1a10", "#c05a2a", "wing", "#ffd8a0", "#2a1a10", None),
 "doctor-fate-khalid":    ("#10203a", "#2f6fc0", "ankh", "#ffd75e", "#10203a", None),
 "zatara":                ("#160c2a", "#5a2ab0", "hat", "#e0d0ff", "#160c2a", None),
 "captain-cold":          ("#0a2440", "#4fb8e8", "snow", "#d0f0ff", "#0a2440", None),
}

def inner_letter(ch, fg):
    # simple blocky monogram built from strokes (no font dependency)
    if ch == "L":
        return (f'<path d="M38 34 V66 H64" stroke="{fg}" stroke-width="9" fill="none" '
                f'stroke-linecap="square"/>')
    return ""

HALFTONE = ("<pattern id='dots' width='16' height='16' patternUnits='userSpaceOnUse'>"
            "<circle cx='4' cy='4' r='1.6' fill='#ffffff' opacity='0.10'/></pattern>")

def svg(slug, c1, c2, glyph, fg, badge, extra):
    fn = GLYPHS[glyph]
    if glyph == "hex":
        art = fn(fg, badge, inner_letter(extra or "L", fg))
    else:
        art = fn(fg, badge)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512" role="img" aria-label="{slug}">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/>
    </linearGradient>
    <radialGradient id="glow" cx="50%" cy="38%" r="62%">
      <stop offset="0" stop-color="#ffffff" stop-opacity="0.30"/>
      <stop offset="1" stop-color="#ffffff" stop-opacity="0"/>
    </radialGradient>
    {HALFTONE}
  </defs>
  <rect width="512" height="512" fill="url(#bg)"/>
  <rect width="512" height="512" fill="url(#dots)"/>
  <circle cx="256" cy="200" r="210" fill="url(#glow)"/>
  <path d="M0 420 L512 300 L512 512 L0 512 Z" fill="#000000" opacity="0.22"/>
  <g opacity="0.25" stroke="#ffffff" stroke-width="3" fill="none">
    <path d="M0 96 L512 96" opacity="0.25"/><path d="M0 128 L512 128" opacity="0.18"/>
  </g>
  <circle cx="256" cy="246" r="176" fill="none" stroke="#ffffff" stroke-opacity="0.20" stroke-width="4"/>
  <circle cx="256" cy="246" r="164" fill="none" stroke="#000000" stroke-opacity="0.18" stroke-width="2"/>
  <g transform="translate(56,46) scale(4)">{art}</g>
  <g opacity="0.9">
    <path d="M24 480 H488" stroke="#ffffff" stroke-opacity="0.15" stroke-width="2"/>
    <circle cx="24" cy="480" r="4" fill="#ffffff" opacity="0.5"/>
    <circle cx="256" cy="480" r="4" fill="#ffffff" opacity="0.5"/>
    <circle cx="488" cy="480" r="4" fill="#ffffff" opacity="0.5"/>
  </g>
</svg>
'''

def main():
    os.makedirs(OUT, exist_ok=True)
    for slug, (c1, c2, glyph, fg, badge, extra) in M.items():
        with open(os.path.join(OUT, slug + ".svg"), "w") as fh:
            fh.write(svg(slug, c1, c2, glyph, fg, badge, extra))
    print("wrote %d emblems to %s" % (len(M), os.path.normpath(OUT)))

if __name__ == "__main__":
    main()
