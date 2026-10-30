"""Rook (Oct 30, box pipeline): list v1 signage: #37 Sector-4 lit sign, #38 wayfinding totem, #39 street name blade, #20 stop totem, #52 pictogram board.
Wordless: geometric glyphs only (numeral 4, arrows, tram/pictogram marks). Same rules/pattern as ext_street_furniture_generator.py.
Glyph strokes of one glyph share a part (abutting, same material). Run: python3 ext_signage_generator.py [sign|totem|blade|stop|board]"""
import os, sys, numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import ext_street_furniture_generator as sf
from ext_street_furniture_generator import G, S, T, A, GL, E, ring, box, blk, Pod, loft, xf

def rects(R, z, t=.006): return [box(x0, x1, y0, y1, z - E, z + t) for x0, x1, y0, y1 in R]
def four(cx, cy, h):  # numeral 4 from abutting strokes
    w = h * .12
    return [(cx + .1 * h, cx + .1 * h + w, cy - h / 2, cy + h / 2), (cx - .3 * h, cx + .1 * h, cy - .1 * h, cy - .1 * h + w),
            (cx + .1 * h + w, cx + .3 * h, cy - .1 * h, cy - .1 * h + w), (cx - .3 * h, cx - .3 * h + w, cy - .1 * h + w, cy + h / 2)]
def tri(pts, z0, z1):  # prism from a 2D (x, y) polygon extruded along Z
    o = np.array([(x, -y) for x, y in pts]); c = o.mean(0); m = loft(o - c, [(z0, 1, 1), (z1, 1, 1)])  # loft caps fan from the origin: centre first
    R = np.array([[1, 0, 0, 0], [0, 0, -1, 0], [0, 1, 0, 0], [0, 0, 0, 1]], float); return xf(xf(m, R=R), t=(c[0], -c[1], 0))
def arrow(cx, cy, L, h, z, d=1):  # shaft + head pointing +X (d=1) or -X (d=-1)
    tip = cx + d * L / 2; base = tip - d * min(.35 * L, 1.1 * h)
    sh = box(min(cx - d * L / 2, base), max(cx - d * L / 2, base), cy - h * .18, cy + h * .18, z - E, z + .006)
    hd = tri([(base, cy - h / 2), (tip, cy), (base, cy + h / 2)] if d > 0 else [(base, cy + h / 2), (tip, cy), (base, cy - h / 2)], z - E, z + .006)
    return [sh, hd]
def tram(cx, cy, s, z):  # tram pictogram: body, window band gap via two blocks, wheels, pantograph
    R = [(cx - s, cx + s, cy - .3 * s, cy + .2 * s), (cx - s, cx + s, cy + .3 * s, cy + .45 * s),
         (cx - .7 * s, cx - .45 * s, cy - .5 * s, cy - .3 * s), (cx + .45 * s, cx + .7 * s, cy - .5 * s, cy - .3 * s), (cx - .04 * s, cx + .04 * s, cy + .45 * s, cy + .75 * s)]
    return rects(R, z)

# ---------------- #37 Sector-4 lit sign 2.6 W x 0.1 D x 0.5 H, <=300 (wall-mounted, back = -Z) ----------------
def sign(v):
    p = Pod(f"ext_sector4_sign_0{v}"); zf = .03
    if v == 1:  # Slate Panel: slate panel, amber 4 + spin chevrons, titanium top/bottom strips
        p.add("Panel", S, box(-1.29, 1.29, .01, .49, -.05, zf))
        p.add("Trim", T, box(-1.3, 1.3, 0, .01 + E, -.047, .02), box(-1.3, 1.3, .49 - E, .5, -.047, .02))
        p.add("Glyph_4", A, *rects(four(-.9, .25, .3), zf)); p.add("Chevrons", A, *arrow(.4, .25, 1.4, .26, zf))
    elif v == 2:  # Glass Lightbox: gunmetal tray, amber backlight sheet, BLEND glass face with slate 4
        p.add("Tray", G, box(-1.3, 1.3, 0, .5, -.05, .0))
        p.add("Backlight", A, box(-1.26, 1.26, .04, .46, -E, .008))
        p.add("Glass_Face", GL, box(-1.27, 1.27, .03, .47, .008 - E, .03))
        p.add("Glyph_4", S, *rects(four(-.95, .25, .3), .03))
        p.add("Chevrons", S, *arrow(.4, .25, 1.2, .24, .03))
    elif v == 3:  # Edge-Lit Frame: gunmetal panel ringed by amber edge bars, titanium 4
        p.add("Panel", G, box(-1.25, 1.25, .04, .46, -.05, zf))
        p.add("Edge_Bars", A, box(-1.3, 1.3, 0, .04 + E, -.047, .02), box(-1.3, 1.3, .46 - E, .5, -.047, .02), box(-1.3, -1.25 + E, .04 - E, .46 + E, -.047, .02), box(1.25 - E, 1.3, .04 - E, .46 + E, -.047, .02))
        p.add("Glyph_4", T, *rects(four(0, .25, .32), zf))
    elif v == 4:  # Split Stripe: slate field + amber sector stripe block with gunmetal 4
        p.add("Panel", S, box(-1.3, .5, 0, .5, -.05, zf)); p.add("Sector_Block", A, box(.5 - E, 1.3, .003, .497, -.047, zf + .002))
        p.add("Glyph_4", G, *rects(four(.9, .25, .3), zf + .002)); p.add("Chevrons", A, *arrow(-.4, .25, 1.2, .24, zf))
    elif v == 5:  # Standoff Letters: titanium rail on gunmetal standoffs, amber 4 block and chevrons floating proud
        p.add("Rail", T, box(-1.3, 1.3, .2, .3, -.05, -.02))
        p.add("Standoffs_Hardware", G, *[box(x - .02, x + .02, .22, .28, -.02 - E, E) for x in (-.9, 0, .9)])
        p.add("Glyph_Plate", G, box(-1.1, -.6, 0, .5, 0, .02)); p.add("Glyph_4", A, *rects(four(-.85, .25, .32), .02))
        p.add("Chevron_Plate", G, box(.2, 1.3, .1, .4, 0, .02)); p.add("Chevrons", A, *arrow(.75, .25, .9, .24, .02))
    return p
SIGN = [(1, "Slate_Panel"), (2, "Glass_Lightbox"), (3, "Edge_Lit_Frame"), (4, "Split_Stripe"), (5, "Standoff_Letters")]

# ---------------- #38 wayfinding totem 0.5 W x 0.3 D x 2.2 H, <=800; spinward (+X) / antispinward (-X) arrows on both faces ----------------
def faces(p, mat, zf, y0=1.2, y1=1.9, L=.34):  # arrows on front (+Z) and back (-Z)
    for sgn in (1, -1):
        ms = arrow(0, y1 - .15, L, .16, zf, 1) + arrow(0, y0 + .15, L, .16, zf, -1)
        if sgn < 0: ms = [_flipz(m) for m in ms]
        p.add("Arrows", mat, *ms)
def _flipz(m):
    m = m.copy(); uv = m.metadata["uv"]; m.apply_transform(np.diag([-1, 1, -1, 1.0])); m.metadata["uv"] = uv; return m
def totem(v):
    p = Pod(f"ext_wayfinding_totem_0{v}")
    if v == 1:  # Slate Slab: slate slab, titanium cap, gunmetal plinth, amber arrows both faces
        p.add("Plinth", G, box(-.24, .24, 0, .1, -.14, .14)); p.add("Slab", S, blk(-.23, .23, .1 - E, 2.15, -.12, .12, .02, 1))
        p.add("Cap", T, blk(-.25, .25, 2.15 - E, 2.2, -.15, .15, .02, 1)); faces(p, A, .12)
    elif v == 2:  # Glass Panel: gunmetal frame posts holding a BLEND glass panel with amber arrows
        p.add("Feet", G, *[box(x - .03, x + .03, 0, .02, -.15, .15) for x in (-.22, .22)])
        p.add("Posts", G, *[box(x - .028, x + .028, .02 - E, 2.2, -.05, .05) for x in (-.22, .22)])
        p.add("Glass_Panel", GL, box(-.19 - E, .19 + E, .5 - E, 2.05, -.015, .015)); p.add("Base_Bar", T, box(-.192 - E, .192 + E, .03, .5 + E, -.04, .04))
        faces(p, A, .015)
    elif v == 3:  # Lit Spine: slate slab with a vertical amber light spine on each edge and titanium arrows
        p.add("Slab", S, box(-.22, .22, 0, 2.2, -.12, .12))
        p.add("Spines", A, *[box(min(s * (.22 - E), s * (.25)), max(s * (.22 - E), s * .25), .1, 2.1, -.06, .06) for s in (-1, 1)])
        faces(p, T, .12)
    elif v == 4:  # Pictogram Column: octagonal gunmetal column with a flat slate sign face carrying arrows
        p.add("Column", G, ring(.15, 0, 2.2, 8, flat=True)); ap = .15 * np.cos(np.pi / 8)
        p.add("Sign_Faces", S, box(-.25, .25, 1.1, 2.0, -.15, .15)) if False else None
        for sgn in (1, -1): p.add("Sign_Faces", S, box(-.13, .13, 1.1, 2.0, (ap - E) if sgn > 0 else -ap - .012, (ap + .012) if sgn > 0 else -ap + E))
        faces(p, A, ap + .012, L=.22)
        p.add("Halo", A, ring(.16, 2.12, 2.15, 8, flat=True)) if False else None
    elif v == 5:  # Leaning Blade: titanium blade on a gunmetal foot with amber top light
        p.add("Foot", G, box(-.25, .25, 0, .06, -.15, .15)); p.add("Blade", T, box(-.2, .2, .06 - E, 2.12, -.04, .04))
        p.add("Top_Light", A, box(-.2, .2, 2.12 - E, 2.2, -.035, .035)) if False else p.add("Top_Light", A, box(-.21, .21, 2.12 - E, 2.2, -.045, .045))
        faces(p, S, .04)
    return p
TOTEM = [(1, "Slate_Slab"), (2, "Glass_Panel"), (3, "Lit_Spine"), (4, "Pictogram_Column"), (5, "Titanium_Blade")]

# ---------------- #39 street name blade 0.8 W x 0.05 D x 0.2 H, <=100 (pictogram code, wordless) ----------------
def blade(v):
    p = Pod(f"ext_street_blade_0{v}")
    if v == 1:  # Slate + amber edge
        p.add("Blade", S, box(-.4, .4, 0, .17, -.02, .02)); p.add("Edge", A, box(-.397, .397, .17 - E, .2, -.022, .022))
        p.add("Glyph", T, *rects([(-.3, -.22, .05, .12), (-.18, -.1, .05, .12)], .02))
    elif v == 2:  # Titanium blade, slate arrow both faces
        p.add("Blade", T, box(-.4, .4, 0, .2, -.015, .015)); p.add("Arrow", S, *arrow(0, .1, .5, .12, .015), *[_flipz(m) for m in arrow(0, .1, .5, .12, .015)])
    elif v == 3:  # Lightbox blade: gunmetal frame with amber lit core
        p.add("Frame", G, box(-.4, .4, 0, .2, -.025, -.01), box(-.4, .4, 0, .2, .01, .025)); p.add("Core", A, box(-.39, .39, .01, .19, -.01 - E, .01 + E))
    elif v == 4:  # Banded: slate blade with amber end tab and titanium spin bars
        p.add("Blade", S, box(-.4, .3, 0, .2, -.02, .02)); p.add("End_Tab", A, box(.3 - E, .4, .003, .197, -.025, .025))
        p.add("Spin_Bars", T, *rects([(-.3, -.05, .06, .08), (-.3, -.05, .12, .14)], .02))
    elif v == 5:  # Chevron cut blade: gunmetal blade with pointed spinward end, amber chevron
        p.add("Blade", G, tri([(-.4, 0), (.3, 0), (.4, .1), (.3, .2), (-.4, .2)], -.02, .02)); p.add("Chevron", A, *rects([(-.3, .1, .09, .11)], .02))
    return p
BLADE = [(1, "Slate_Amber_Edge"), (2, "Titanium_Arrow"), (3, "Lightbox"), (4, "Banded_Tab"), (5, "Chevron_Point")]

# ---------------- #20 stop totem / timetable 0.5 W x 0.3 D x 2.4 H, <=500 ----------------
def stop(v):
    p = Pod(f"ext_stop_totem_0{v}"); zf = .12
    p.add("Plinth", G, box(-.24, .24, 0, .08, -.14, .14))
    body = {1: S, 2: G, 3: S, 4: T, 5: G}[v]
    p.add("Body", body, box(-.22, .22, .08 - E, 2.3, -.12, .12))
    p.add("Cap", T if v != 4 else G, box(-.25, .25, 2.3 - E, 2.4, -.15, .15))
    # roundel with tram pictogram near the top
    if v in (1, 3, 5): p.add("Roundel", A, ring(.16, zf - E, zf + .015, 16, x=0, z=0) if False else _zdisc(0, 2.05, .16, zf - E, zf + .012, 16)); p.add("Tram_Glyph", G, *tram(0, 2.05, .09, zf + .012))
    else: p.add("Roundel_Plate", A, box(-.18, .18, 1.88, 2.22, zf - E, zf + .012)); p.add("Tram_Glyph", G if v == 4 else S, *tram(0, 2.05, .1, zf + .012))
    # timetable: BLEND glass case over a slate dot-matrix plate (dots = small amber bars)
    if v != 5:
        p.add("Timetable_Plate", S if body != S else G, box(-.17, .17, 1.0, 1.7, zf - E, zf + .008))
        p.add("Timetable_Bars", A, *rects([(-.13, -.13 + w, y, y + .02) for y, w in zip(np.linspace(1.08, 1.6, 5), (.2, .14, .24, .1, .18))], zf + .008, .003))
        if v in (1, 2, 3):  # BLEND glass cover held off the plate by top/bottom bezel bars (glass back 1.5 mm clear of the bars)
            p.add("Timetable_Glass", GL, box(-.19, .19, .98 - E, 1.72 + E, zf + .0125, zf + .02))
            p.add("Bezel", G if body != G else T, box(-.2, .2, .96, .98, zf - E, zf + .024), box(-.2, .2, 1.72, 1.74, zf - E, zf + .024))
    else:  # 5: lit amber screen strip + call button
        p.add("Screen", GL, box(-.16, .16, 1.2, 1.6, zf - E, zf + .01)); p.add("Screen_Back", A, box(-.15, .15, 1.21, 1.59, zf - E - .006, zf - E + .002)) if False else None
        p.add("Call_Button", A, _zdisc(0, 1.05, .04, zf - E, zf + .015, 10))
    if v == 3: p.add("Side_Light", A, *[box(s * .22 - .008, s * .22 + .008, .3, 1.8, -.06, .06) for s in (-1, 1)])
    return p
def _zdisc(x, y, r, z0, z1, n):
    from cycler_route_generator import cyl_z
    return cyl_z(x, y, r, z0, z1, n)
STOP = [(1, "Slate_Roundel"), (2, "Gunmetal_Plate"), (3, "Edge_Lit"), (4, "Titanium_Column"), (5, "Screen_Call")]

# ---------------- #52 pictogram notice board 1.0 W x 0.1 D x 1.4 H, <=400 (wordless) ----------------
def board(v):
    p = Pod(f"ext_notice_board_0{v}"); zf = .02
    tiles = [(-.38, -.14, .78, 1.02), (-.1, .14, .78, 1.02), (.18, .42, .78, 1.02), (-.38, -.14, .5, .74), (-.1, .14, .5, .74), (.18, .42, .5, .74)]
    if v in (1, 2, 3):
        p.add("Legs", G, *[box(x - .03, x + .03, 0, .45 + E, -.03, .03) for x in (-.42, .42)])
        p.add("Board", S if v != 2 else G, box(-.5, .5, .45, 1.32, -.04, zf)); p.add("Header", T if v != 3 else A, box(-.5, .5, 1.32 - E, 1.4, -.05, .03))
    elif v == 4:  # wall-hung slab
        p.add("Board", S, box(-.5, .5, 0, 1.4, -.05, zf))
        tiles = [(a, b, c - .1, d - .1) for a, b, c, d in tiles] + [(a, b, c - .66, d - .66) for a, b, c, d in tiles[:3]]
    else:  # 5: single titanium post, board cantilevered
        p.add("Post", T, box(-.04, .04, 0, 1.4, -.05, -.01)); p.add("Board", G, box(-.48, .48, .47, 1.3, -.01 - E, zf))
    p.add("Tiles", A if v != 3 else T, *rects(tiles, zf))
    p.add("Tile_Glyphs", G, *rects([(x0 + .08, x1 - .08, y0 + .06, y1 - .06) for x0, x1, y0, y1 in tiles], zf + .006))
    if v in (2, 4):  # BLEND glass cover 1.5 mm clear of the glyphs, held by top/bottom bezel bars
        y0 = .46 if v == 2 else .02
        p.add("Glass_Cover", GL, box(-.46, .46, y0 + .02 - E, 1.06 + E, zf + .0135, zf + .022))
        p.add("Bezel", T, box(-.47, .47, y0, y0 + .02, zf - E, zf + .026), box(-.47, .47, 1.06, 1.08, zf - E, zf + .026))
    return p
BOARD = [(1, "Slate_Legs"), (2, "Glazed_Case"), (3, "Amber_Header"), (4, "Wall_Slab"), (5, "Cantilever_Post")]

sf.ASSETS.update({"sign": ("ext_sector4_sign", sign, SIGN, 300, "#37 Sector-4 lit sign 2.6x0.1x0.5"),
                  "totem": ("ext_wayfinding_totem", totem, TOTEM, 800, "#38 wayfinding totem 0.5x0.3x2.2"),
                  "blade": ("ext_street_blade", blade, BLADE, 100, "#39 street name blade 0.8x0.05x0.2"),
                  "stop": ("ext_stop_totem", stop, STOP, 500, "#20 stop totem / timetable 0.5x0.3x2.4"),
                  "board": ("ext_notice_board", board, BOARD, 400, "#52 pictogram notice board 1.0x0.1x1.4")})
if __name__ == "__main__":
    for k in (sys.argv[1:] or ["sign", "totem", "blade", "stop", "board"]): sf.build(k)
