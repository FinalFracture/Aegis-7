"""Rook (Oct 30, box pipeline): list v1 #29 RFID tag rack, #30 violet field lamp, #31 offering set (memorial nook),
#27 pump + tank cabinet, #28 grow-light rack, #23a Tiered Steps TS-2, #48 shelter sleeper set.
Same rules/pattern as ext_street_furniture_generator.py. Science violet #7B5CFF on the memorial pieces (per list v1), grow lights violet.
No wood: flower stems/bedroll are composite/fabric. Inserts (stems, plants) stand in open-topped vessels, never buried in solids.
Run: python3 ext_memorial_hydro_generator.py [tagrack|lamp|offering|pump|growrack|ts2|sleeper]"""
import os, sys, numpy as np, trimesh
sys.path.insert(0, os.path.dirname(__file__))
import ext_street_furniture_generator as sf
from ext_street_furniture_generator import G, S, T, A, GL, E, ring, box, blk, Pod, loft, xf, FMAT, _PBR
from folding_counter_generator import xcyl
from cycler_route_generator import cyl_z
import hydro_planter_generator as hp
from kitchen_counter_generator import bev
FMAT["a7_violet"] = _PBR(name="A7_ScienceViolet", baseColorFactor=(0x7B/255, 0x5C/255, 1.0, 1), metallicFactor=0.0, roughnessFactor=0.4, emissiveFactor=(0x7B/255, 0x5C/255, 1.0))
FMAT["a7_violet_matte"] = _PBR(name="A7_VioletMatte", baseColorFactor=(0x7B/255, 0x5C/255, 1.0, 1), metallicFactor=0.0, roughnessFactor=0.8)
FMAT["a7_fabric"] = _PBR(name="A7_SlateFabric", baseColorFactor=(0x2A/255, 0x30/255, 0x38/255, 1), metallicFactor=0.0, roughnessFactor=0.9)
V, VM, FB = "a7_violet", "a7_violet_matte", "a7_fabric"

def seg(p0, p1, r, n=6):  # cylinder between two points (with UVs)
    m = trimesh.creation.cylinder(radius=r, segment=[p0, p1], sections=n); m.metadata["uv"] = m.vertices[:, [0, 1]]; return m
def ball(x, y, z, r, sub=0):
    m = trimesh.creation.icosphere(sub, r); m.apply_translation((x, y, z)); m.metadata["uv"] = m.vertices[:, [0, 2]]; return m
def frame2(p, W, H, D=.06, mat=G, foot=True):  # two posts + top rail (+ floor feet); returns post inner x
    if foot: p.add("Feet", mat, *[box(s * W / 2 - .06, s * W / 2 + .06 if s > 0 else s * W / 2 + .06, 0, .02, -.15, .15) for s in (-1, 1)])
    p.add("Posts", mat, *[box(s * W / 2 - .025 + (0 if s > 0 else 0), s * W / 2 + .025, .02 - E if foot else 0, H - .04 + E, -.025, .025) for s in (-1, 1)])
    p.add("Top_Rail", T, box(-W / 2 - .03, W / 2 + .03, H - .04, H, -.03, .03)); return W / 2 - .025

# ---------------- #29 wire rack with hanging RFID tags 1.2 x 0.3 x 1.8, <=1500 ----------------
def tags_on(p, x0, x1, y, z, n, rng, mats=(T, VM), r=.004):
    p.add("Wires", T, xcyl(x0 - E, x1 + E, y, z, r, 6))
    for k, x in enumerate(np.linspace(x0 + .05, x1 - .05, n) + rng.uniform(-.015, .015, n)):
        h = rng.uniform(.05, .08); p.add("Tags_" + ("Ti" if mats[k % len(mats)] == T else "Violet"), mats[k % len(mats)], box(x - .018, x + .018, y - h, y + r * .5, z - .0015, z + .0015))
def tagrack(v):
    p = Pod(f"ext_memorial_tag_rack_0{v}"); rng = np.random.default_rng(29 + v); W = 1.08
    if v in (1, 2, 5):
        xi = frame2(p, W, 1.8)
        ys = (1.55, 1.3, 1.05, .8) if v != 5 else (1.55, 1.3, 1.05)
        for i, y in enumerate(ys): tags_on(p, -xi, xi, y, (.0 if v != 5 else (-.06 + .04 * i)), 13 if v == 1 else 11, rng)
        if v == 2: p.add("Lamp_Strip", V, box(-W / 2, W / 2, 1.8 - E, 1.815, -.02, .02))
        if v == 5: p.add("Candle_Shelf", G, box(-xi - E, xi + E, .5, .53, -.1, .1)); p.add("Candles", V, *[ring(.02, .53 - E, .53 + h, 8, x=x) for x, h in ((-.3, .08), (-.1, .12), (.15, .06), (.35, .1))])
    elif v == 3:  # A-frame: splayed leg pairs, two wire faces
        for s in (-1, 1):
            p.add("Legs", G, seg((s * .57, 0, -.14), (s * .57, 1.744, -.01), .02, 6), seg((s * .57, 0, .14), (s * .57, 1.744, .01), .02, 6))
        p.add("Top_Rail", T, box(-.6, .6, 1.74, 1.8, -.04, .04))
        for y in (1.5, 1.2, .9):
            dz = .14 * (1 - y / 1.76) - .01 * y / 1.76
            for sz in (-1, 1): tags_on(p, -.55, .55, y, sz * (dz + .03), 10, rng)
    elif v == 4:  # wall grid panel: gunmetal frame + titanium grid bars, tags on the horizontals
        p.add("Panel_Frame", G, box(-.6, .6, 0, .06, -.04, .04), box(-.6, .6, 1.74, 1.8, -.04, .04), box(-.6, -.55, .06 - E, 1.74 + E, -.04, .04), box(.55, .6, .06 - E, 1.74 + E, -.04, .04))
        p.add("Grid_Verticals", T, *[box(x - .006, x + .006, .06 - E, 1.74 + E, -.012, .0) for x in np.linspace(-.4, .4, 5)])
        for y in (1.5, 1.2, .9, .6): tags_on(p, -.55, .55, y, .01, 12, rng)
    return p
TAG = [(1, "Four_Wire_Frame"), (2, "Lit_Frame"), (3, "A_Frame"), (4, "Wall_Grid"), (5, "Staggered_Candle_Shelf")]

# ---------------- #30 violet field lamp 0.3 x 0.3 x 1.2, <=600 ----------------
def lantern(p, y0, s=.09, h=.22, cage=True):  # open glass lantern: base + top plates, 4 glass panes, violet core (core stands clear of the panes)
    p.add("Lantern_Plates", G, box(-s - .01, s + .01, y0, y0 + .02, -s - .01, s + .01), box(-s - .01, s + .01, y0 + h - .02, y0 + h, -s - .01, s + .01))
    p.add("Panes", GL, *[box(-s, s, y0 + .02 - E, y0 + h - .02 + E, z - .003, z + .003) for z in (-s + .005, s - .005)], *[box(x - .003, x + .003, y0 + .02 - E, y0 + h - .02 + E, -s + .012, s - .012) for x in (-s + .005, s - .005)])
    p.add("Violet_Core", V, ring(.035, y0 + .02 - E, y0 + h - .06, 8))
def lamp(v):
    p = Pod(f"ext_violet_field_lamp_0{v}")
    if v == 1:  # Stake Lantern: ground disc, slim stake, square lantern
        p.add("Ground_Disc", G, ring(.12, 0, .02, 12)); p.add("Stake", T, ring(.018, .02 - E, .9 + E, 8)); lantern(p, .9, h=.3)
    elif v == 2:  # Cage Column: violet core column inside 4 titanium cage bars
        p.add("Base", G, ring(.14, 0, .1, 8, flat=True)); p.add("Core", V, ring(.045, .1 - E, 1.1 + E, 8))
        p.add("Cage_Bars", T, *[box(x - .008, x + .008, .1 - E, 1.1 + E, z - .008, z + .008) for x in (-.09, .09) for z in (-.09, .09)])
        p.add("Cap", G, ring(.13, 1.1, 1.2, 8, 1, .6, flat=True))
    elif v == 3:  # Tripod: three splayed legs, lantern on top
        for a in (90, 210, 330):
            t = np.radians(a); p.add("Legs", G, seg((.13 * np.cos(t), 0, .13 * np.sin(t)), (.03 * np.cos(t), .9 + E, .03 * np.sin(t)), .012, 6))
        p.add("Hub", T, ring(.06, .88, .92, 8)) if False else None
        lantern(p, .9, s=.08, h=.3)
    elif v == 4:  # Shepherd Hook: post + arm, lantern hanging on a chain rod
        p.add("Ground_Disc", G, ring(.12, 0, .02, 12)); p.add("Post", T, box(-.1 - .012, -.1 + .012, .02 - E, 1.2, -.012, .012))
        p.add("Arm", T, box(-.1 + .012 - E, .06, 1.17, 1.196, -.01, .01)); p.add("Hanger", G, ring(.005, .9 - E, 1.17 + E, 6, x=.04))
        p.add("Lantern_Plates", G, box(-.015, .095, .66, .68, -.055, .055), box(-.015, .095, .88, .9, -.055, .055))
        p.add("Panes", GL, *[box(-.01, .09, .68 - E, .88 + E, z - .003, z + .003) for z in (-.05, .05)])
        p.add("Violet_Core", V, ring(.025, .68 - E, .84, 8, x=.04))
    elif v == 5:  # Beacon Candles: gunmetal tray, three violet candles, tall violet beacon stake
        p.add("Tray", G, box(-.15, .15, 0, .03, -.15, .15))
        p.add("Candles", V, *[ring(.025, .03 - E, .03 + h, 8, x=x, z=z) for x, z, h in ((-.08, .08, .1), (.08, .07, .14), (-.06, -.08, .07))])
        p.add("Stake", T, ring(.015, .03 - E, 1.1, 8, x=.07, z=-.07)); p.add("Beacon", V, ring(.04, 1.1 - E, 1.2, 8, 1, .5, x=.07, z=-.07))
    return p
LAMP = [(1, "Stake_Lantern"), (2, "Cage_Column"), (3, "Tripod_Lantern"), (4, "Shepherd_Hook"), (5, "Beacon_Candles")]

# ---------------- #31 dried flower / offering set 0.6 x 0.3 x 0.3, <=800 ----------------
def vase(p, x, z, w=.07, h=.16, mat=T, y0=0):  # open-topped square vase (4 walls + base): stems stand on the base inside
    t = .006
    p.add("Vases", mat, box(x - w / 2, x + w / 2, y0, y0 + .012, z - w / 2, z + w / 2),
          box(x - w / 2, x + w / 2, y0 + .012 - E, y0 + h, z + w / 2 - t, z + w / 2), box(x - w / 2, x + w / 2, y0 + .012 - E, y0 + h, z - w / 2, z - w / 2 + t),
          box(x - w / 2, x - w / 2 + t, y0 + .012 - E, y0 + h, z - w / 2 + t - E, z + w / 2 - t + E), box(x + w / 2 - t, x + w / 2, y0 + .012 - E, y0 + h, z - w / 2 + t - E, z + w / 2 - t + E))
    return y0 + .012
def flowers(p, x, z, yb, n, top, rng, spread=.022):
    for k in range(n):
        ang = 2 * np.pi * k / n; dx, dz = spread * np.cos(ang) * .6, spread * np.sin(ang) * .6
        hx, hz, hy = x + dx * 2.2, z + dz * 2.2, top + rng.uniform(-.03, .02)
        p.add("Stems", S, seg((x + dx, yb - E, z + dz), (hx, hy, hz), .003, 4))
        p.add("Dried_Petals", VM if k % 2 == 0 else T, ball(hx, hy + .012, hz, .016, 0))
def offering(v):
    p = Pod(f"ext_offering_set_0{v}"); rng = np.random.default_rng(31 + v)
    if v == 1:  # Twin Vases: two vases with dried flowers, violet candle, slate note
        for x, n in ((-.2, 5), (.05, 4)): yb = vase(p, x, 0, y0=0); flowers(p, x, 0, yb, n, .25, rng)
        p.add("Candle", V, ring(.025, 0, .08, 8, x=.22)); p.add("Folded_Note", S, box(.12, .2, 0, .012, .04, .1))
    elif v == 2:  # Tray Offering: gunmetal tray carrying a vase, two candles and an RFID tag
        p.add("Tray", G, box(-.3, .3, 0, .02, -.15, .15)); yb = vase(p, -.15, 0, y0=.02 - E); flowers(p, -.15, 0, yb, 6, .25, rng)
        p.add("Candles", V, ring(.022, .02 - E, .09, 8, x=.08, z=.05), ring(.022, .02 - E, .12, 8, x=.15, z=-.05))
        p.add("RFID_Tag", T, box(.2, .26, .02 - E, .026, .02, .1))
    elif v == 3:  # Bundled Bouquet: tied bouquet lying on a slate plinth, violet ribbon band, candle
        p.add("Plinth", S, box(-.28, .28, 0, .04, -.12, .12))
        for k in range(5):
            zz = -.04 + .02 * k; p.add("Stems", T, seg((-.2, .052, zz * .3), (.12, .05 + .004 * k, zz), .004, 4)); p.add("Dried_Petals", VM, ball(.14, .056 + .004 * k, zz, .02, 0))
        p.add("Ribbon", V, box(-.1, -.06, .04 - E, .046, -.03, .05)); p.add("Candle", V, ring(.025, .04 - E, .13, 8, x=.22, z=.06))
    elif v == 4:  # Tall Cylinder Vase: single tall square vase, many stems, candles in a row
        yb = vase(p, -.18, 0, w=.09, h=.22); flowers(p, -.18, 0, yb, 7, .25, rng, .028)
        p.add("Candles", V, *[ring(.02, 0, h, 8, x=x) for x, h in ((0, .06), (.1, .09), (.2, .12))])
    elif v == 5:  # Stone Row: three titanium tea-light cups with violet glow, vase, tag
        for x in (-.25, -.15, -.05): p.add("Cups", T, ring(.035, 0, .04, 10, x=x)); p.add("Glow", V, ring(.025, .04 - E, .052, 8, x=x))
        yb = vase(p, .15, 0); flowers(p, .15, 0, yb, 5, .25, rng); p.add("RFID_Tag", T, box(.22, .28, 0, .006, -.12, -.06))
    return p
OFF = [(1, "Twin_Vases"), (2, "Tray_Offering"), (3, "Bundled_Bouquet"), (4, "Tall_Vase_Candles"), (5, "Tea_Light_Row")]

# ---------------- #27 pump + water tank cabinet 1.2 x 0.8 x 1.8, <=1200 ----------------
def pipe_y(x, z, y0, y1, r=.025): return ring(r, y0, y1, 8, x=x, z=z)
def pump(v):
    p = Pod(f"ext_hydro_pump_tank_0{v}")
    p.add("Skid", G, box(-.6, .6, 0, .06, -.4, .4))
    if v == 1:  # Side Tank: tall titanium tank beside a slate pump cabinet, emerald status
        p.add("Tank", T, ring(.28, .06 - E, 1.7, 16, x=-.3, top=(1.8, .5, .5)))
        p.add("Cabinet", S, blk(.04, .58, .06 - E, 1.1, -.35, .35, .02, 1)); p.add("Status", "green", box(.4, .5, .95, .98, .35 - E, .356))
        p.add("Pipes", G, xcyl(-.3 + .27, .04 + E, .4, .1, .03, 8))
    elif v == 2:  # Tank On Top: low pump cabinet carrying a horizontal-ish vertical drum on top
        p.add("Cabinet", S, blk(-.58, .58, .06 - E, .7, -.38, .38, .02, 1)); p.add("Tank", T, ring(.36, .7 - E, 1.7, 16, top=(1.8, .6, .6)))
        p.add("Status", "green", box(.4, .5, .55, .58, .38 - E, .386)); p.add("Sight_Glass", GL, box(-.025, .025, .9, 1.5, .355, .38))
    elif v == 3:  # Twin Tanks: two tanks, pump box between with pipes
        for x in (-.38, .38): p.add("Tanks", T, ring(.2, .06 - E, 1.6, 12, x=x, z=-.12, top=(1.7, .5, .5)))
        p.add("Pump_Box", S, box(-.16, .16, .06 - E, .5, .05, .38)); p.add("Pipes", G, xcyl(-.38 + .19, -.16 + E, .3, .12 - .0, .03, 8), xcyl(.16 - E, .38 - .19, .3, .12, .03, 8))
        p.add("Status", "green", box(-.05, .05, .42, .45, .38 - E, .386))
    elif v == 4:  # Enclosed Cabinet: full-height slate cabinet, glass sight tube held off the face in clips, amber valve hatch
        F4 = .36; p.add("Cabinet", S, blk(-.58, .58, .06 - E, 1.74, -.38, F4, .02, 1)); p.add("Roof", T, blk(-.6, .6, 1.74 - E, 1.8, -.4, .4, .02, 1))
        p.add("Sight_Tube", GL, ring(.02, .3 - E, 1.5 + E, 8, x=.45, z=F4 + .024))
        p.add("Tube_Clips", G, *[box(.42, .48, y0, y1, F4 - E, F4 + .05) for y0, y1 in ((.27, .3), (1.5, 1.53))])
        p.add("Valve_Hatch", A, box(-.3, .1, .3, .6, F4 - E, F4 + .006)); p.add("Doors", G, box(-.5, -.35, .3, 1.6, F4 - E, F4 + .006))
    elif v == 5:  # Horizontal Tank: horizontal tank on cradles above a pump box
        p.add("Pump_Box", S, box(-.4, .4, .06 - E, .6, -.3, .3))
        p.add("Cradles", G, *[box(x - .04, x + .04, .6 - E, .9, -.3, .3) for x in (-.4, .4)])
        t = loft(hp_circle(.36), [(-.58, 1, 1), (.58, 1, 1)]); t.apply_transform(np.array([[0, 1, 0, 0], [1, 0, 0, 0], [0, 0, -1, 0], [0, 0, 0, 1]], float)); uv = t.metadata["uv"]; t.apply_translation((0, .9 - E + .36, 0)); t.metadata["uv"] = uv
        p.add("Tank", T, t); p.add("Status", "green", box(.2, .3, .45, .48, .3 - E, .306))
    return p
def hp_circle(r, n=16): from dining_chair_generator import circle; return circle(r, n)
PUMP = [(1, "Side_Tank"), (2, "Tank_On_Top"), (3, "Twin_Tanks"), (4, "Enclosed_Cabinet"), (5, "Horizontal_Tank")]

# ---------------- #28 grow-light rack 10 x 0.2 x 2.2, <=700 ----------------
def growrack(v):
    p = Pod(f"ext_grow_light_rack_0{v}"); L = 10.0; xs = np.linspace(-L / 2 + .03, L / 2 - .03, 5)
    p.add("Feet", G, *[box(x - .06 if abs(x) < 4.9 else (x - .03 if x > 0 else x - .03), x + .03 if abs(x) >= 4.9 else x + .06, 0, .02, -.1, .1) for x in xs]) if False else p.add("Feet", G, *[box(x - .03, x + .03, 0, .02, -.1, .1) for x in xs])
    p.add("Posts", G if v != 3 else T, *[box(x - .025, x + .025, .02 - E, 2.16 + E, -.025, .025) for x in xs])
    p.add("Top_Beam", T if v != 3 else G, box(-L / 2, L / 2, 2.16, 2.2, -.04, .04))
    yl = {1: 1.9, 2: 1.7, 3: 1.95, 4: 1.85, 5: 1.8}[v]
    for k in range(4):
        x0, x1 = xs[k] + .025 + .05, xs[k + 1] - .025 - .05
        if v == 2:  # twin bars
            for z in (-.06, .06): p.add("Light_Bars", V, box(x0, x1, yl, yl + .03, z - .025, z + .025))
            p.add("Hangers", T, *[box(x - .006, x + .006, yl + .045 - E, 2.16 + E, -.006, .006) for x in (x0 + .2, x1 - .2)])
            p.add("Bar_Yokes", T, *[box(x - .015, x + .015, yl + .03 - E, yl + .045, -.09, .09) for x in (x0 + .2, x1 - .2)])
        else:
            p.add("Light_Bars", V, box(x0, x1, yl, yl + .035, -.04, .04))
            p.add("Hangers", T, *[box(x - .006, x + .006, (yl + .05 if v == 4 else yl + .035) - E, 2.16 + E, -.006, .006) for x in (x0 + .2, x1 - .2)])
            if v == 4: p.add("Reflectors", T, box(x0 - .01, x1 + .01, yl + .035 - E, yl + .05, -.07, .07))
            if v == 5: p.add("Emerald_Tags", "green", box(x0 + .3, x0 + .36, yl + .005, yl + .03, .04 - E, .046))
    if v == 3: p.add("Cross_Braces", G, *[box(xs[k] + .025 - E, xs[k + 1] - .025 + E, .4, .44, -.02, .02) for k in range(4)])
    return p
GROW = [(1, "Single_Bar"), (2, "Twin_Bar"), (3, "Braced_Titanium"), (4, "Reflector_Hood"), (5, "Tagged_Bars")]

# ---------------- #23a Tiered Steps TS-2 (2.0 x 0.41 x 0.70, ~1500): cut-down of approved TS-4 ----------------
def ts2(v):
    p = Pod(f"hydro_planter_tiered_ts2_0{v}"); FT = .06; W = 2.0; hp.rng = np.random.default_rng(23 + v)
    p.add("Base_Frame", "gunmetal", blk(-W / 2 + .05, W / 2 - .05, FT - .03, FT, -.19, .19, .006, 1))
    counts = {1: (4, 3, 2), 2: (4, 3, 2), 3: (4, 3, 2), 4: (3, 2, 2), 5: (0, 0, 0)}[v]
    for i, (y, z) in enumerate(((.2, .12), (.36, 0), (.52, -.12))):
        p.add("Tiers", "white", bev(W, .16, FT, y + FT, .03, .01, 2, 0, z))
        x0, x1 = -W / 2 + .04, W / 2 - .04; yy = y + FT
        p.add("Tier_Lids", "slate", box(x0, x1, yy - .01, yy + .006, z - .07, z + .07))
        p.add("Tier_Latches", "amber", *[box(x - .02, x + .02, yy - .012, yy - .004, z + .07, z + .076) for x in (-.7, .7)])
        if counts[i]: hp.lean_plants(p, np.linspace(-.8, .8, counts[i]), yy, z, .075 if v != 4 else .055)
    if v in (2, 3):  # end cap panel on the run end (left for 2, right for 3)
        s = -1 if v == 2 else 1; p.add("End_Cap", "slate", box(s * W / 2 - (.012 if s > 0 else -0) + (0 if s > 0 else -.012) if False else (W / 2 if s > 0 else -W / 2 - .012), (W / 2 + .012) if s > 0 else -W / 2, FT - .03, .6, -.19, .19))
    p.add("Reservoir", "slate", box(-.9, .9, FT + .02, FT + .14, .2, .206)); p.add("Reservoir_Seal", "alloy", box(-.9, .9, FT + .14, FT + .15, .2, .206))
    feet = [(x, z) for x in (-.85, .85) for z in (-.14, .14)]
    p.add("Levelling_Jacks", "alloy", *[hp.cyl(x, z, .018, .02 - E, FT - .03 + E, 8) for x, z in feet])
    p.add("Clamp_Shoes", "gunmetal", *[box(x - .06, x + .06, 0, .02, z - .045, z + .045) for x, z in feet])
    p.add("Shoe_Bolts_Hardware", "alloy", *[hp.cyl(x + dx, z, .008, .02 - E, .03, 6) for x, z in feet for dx in (-.04, .04)])
    return p
TS2 = [(1, "Straight_Cut", ), (2, "Left_End_Cap"), (3, "Right_End_Cap"), (4, "Young_Plants"), (5, "Lidded_Bed_End")]

# ---------------- #48 shelter sleeper set (bedroll + hot plate + crate), <=1500 ----------------
def sleeper(v):
    p = Pod(f"ext_shelter_sleeper_set_0{v}"); rng = np.random.default_rng(48 + v)
    def mat(x0, x1, z0, z1, rolled_end=True):
        p.add("Bedroll_Mat", FB, blk(x0, x1, 0, .05, z0, z1, .03, 2))
        if rolled_end: p.add("Bedroll_Roll", FB, xf(cyl_z(0, 0, .09, z0 + .02, z1 - .02, 10), t=(x1 - .12, .05 - E + .09, 0)))
    def hotplate(x, z):
        p.add("Hot_Plate", G, box(x - .14, x + .14, 0, .06, z - .12, z + .12)); p.add("Hot_Coil", A, ring(.08, .06 - E, .066, 12, x=x, z=z))
        p.add("Pot", T, ring(.07, .066 - E, .17, 10, x=x, z=z)) if v in (2, 5) else None
    def crate(x, z, w=.5, d=.35, h=.35, lid=True):
        p.add("Crate", S, blk(x - w / 2, x + w / 2, 0, h, z - d / 2, z + d / 2, .015, 1))
        if lid: p.add("Crate_Lid", G, blk(x - w / 2 - .01, x + w / 2 + .01, h - E, h + .03, z - d / 2 - .01, z + d / 2 + .01, .015, 1))
        p.add("Crate_Latches", A, *[box(xx - .025, xx + .025, h - .06, h - .01, z + d / 2 - E, z + d / 2 + .008) for xx in (x - w / 4, x + w / 4)])
    if v == 1: mat(-1.0, .9, -.35, .35); hotplate(1.15, -.15); crate(1.25, .25, .4, .3, .3)
    elif v == 2: mat(-.9, .9, -.32, .32, False); p.add("Pillow", FB, blk(-.85, -.55, .05 - E, .12, -.2, .2, .04, 2)); crate(1.2, 0, .5, .4, .4); hotplate(1.2, -.0) if False else hotplate(.0, .6)
    elif v == 3: mat(-1.0, .8, -.35, .35); crate(1.15, 0, .5, .35, .35, lid=True); p.add("Hot_Plate", G, box(1.0, 1.3, .38 - E, .42, -.1, .1)); p.add("Hot_Coil", A, ring(.06, .42 - E, .426, 12, x=1.15))
    elif v == 4: mat(-.9, .9, -.35, .35); p.add("Blanket_Fold", FB, blk(-.3, .5, .05 - E, .1, -.33, .33, .03, 2)); hotplate(1.2, .3); crate(1.2, -.2, .45, .3, .3)
    elif v == 5: mat(-.95, .85, -.3, .3); hotplate(1.15, .25); crate(1.15, -.2, .45, .3, .3, lid=False); p.add("Crate_Contents", T, box(1.0, 1.1, .02, .2, -.3, -.12))
    return p
SLEEP = [(1, "Roll_Plate_Crate"), (2, "Pillow_And_Pot"), (3, "Crate_Table"), (4, "Folded_Blanket"), (5, "Open_Crate")]

sf.ASSETS.update({"tagrack": ("ext_memorial_tag_rack", tagrack, TAG, 1500, "#29 RFID tag rack 1.2x0.3x1.8"),
                  "lamp": ("ext_violet_field_lamp", lamp, LAMP, 600, "#30 violet field lamp 0.3x0.3x1.2"),
                  "offering": ("ext_offering_set", offering, OFF, 800, "#31 offering set 0.6x0.3x0.3"),
                  "pump": ("ext_hydro_pump_tank", pump, PUMP, 1200, "#27 pump + tank cabinet 1.2x0.8x1.8"),
                  "growrack": ("ext_grow_light_rack", growrack, GROW, 700, "#28 grow-light rack 10x0.2x2.2"),
                  "ts2": ("hydro_planter_tiered_ts2", ts2, TS2, 1500, "#23a Tiered Steps TS-2 2.0x0.41x0.70 (~1500)"),
                  "sleeper": ("ext_shelter_sleeper_set", sleeper, SLEEP, 1500, "#48 shelter sleeper set (bedroll+hot plate+crate)")})
if __name__ == "__main__":
    for k in sys.argv[1:]: sf.build(k)
