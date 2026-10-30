"""Rook (Oct 30, box pipeline): residential exterior list v1 #15 tram stop shelter (lived-in), 6.0 W x 1.3 D x 2.8 H, <=5,800 tris.
Five candidates -> design/assets/ext_tram_shelter/ext_tram_shelter_01..05.glb + contact sheet. Placed X 12..18, Z -16.9..-15.6 (plan v1.2).
Aegis-7: zero wood; gunmetal/carbon-slate/titanium, amber #FF9500 emissive, Civic cyan #38B8C8 + pearl alabaster #D8DEE4 (civic);
BLEND glass; wordless signage. Y-up, bottom-centre (0,0,0) pivot, +Z = open front (faces the track). Rear timetable panel sits in a
real cut-out (glass/cladding split around it). Joints embed 0.004 m. Script nodes for Gage:
  Timetable_Screen (emissive, swap texture / blink), Arrival_Beacon (amber, pulse on tram approach), Roof_Downlight (night on/off).
Run: python3 ext_tram_shelter_generator.py"""
import os, sys, numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import ext_street_furniture_generator as sf
from ext_street_furniture_generator import Pod, box, blk, cyl, ring, xf, FMAT, _PBR, G, S, T, A, GL, E
FMAT["a7_pearl"] = _PBR(name="A7_PearlAlabaster", baseColorFactor=(0xD8/255, 0xDE/255, 0xE4/255, 1), metallicFactor=0.15, roughnessFactor=0.45)
FMAT["a7_cyan"] = _PBR(name="A7_CivicCyan", baseColorFactor=(0x38/255, 0xB8/255, 0xC8/255, 1), metallicFactor=0.1, roughnessFactor=0.4)
PL, CY = "a7_pearl", "a7_cyan"
W2, ZR, ZF = 3.0, -.55, .55   # half width, rear / front post line

def posts(p, xs, zs, y1, w=.1, d=.1, mat=G, name="Posts"):
    p.add(name, mat, *[box(x - w/2, x + w/2, 0, y1, z - d/2, z + d/2) for x in xs for z in zs])
def wall_glass(p, xs, z, y0, y1, pw=.1, skip=(), name="Rear_Glass"):  # panes between posts, ends embedded E
    for i in range(len(xs) - 1):
        if i in skip: continue
        p.add(name, GL, box(xs[i] + pw/2 - E, xs[i+1] - pw/2 + E, y0, y1, z - .006, z + .006))
def kick(p, xs, z, y0=.12, y1=.3, pw=.1, mat=G, dz=.03, name="Kick_Rails"):
    for i in range(len(xs) - 1): p.add(name, mat, box(xs[i] + pw/2 - E, xs[i+1] - pw/2 + E, y0, y1, z - dz, z + dz))
def timetable(p, x0, x1, z, y0=1.0, y1=1.9, pw=.1):  # framed panel filling the bay: real cut-out, glass split above/below
    p.add("Timetable_Frame", S, box(x0 + pw/2 - E, x1 - pw/2 + E, y0, y1, z - .04, z + .04))
    p.add("Timetable_Screen", CY, box(x0 + pw/2 + .08, x1 - pw/2 - .08, y0 + .1, y1 - .1, z + .04 - E, z + .046))
    for k in range(3): p.add("Route_Pips", A, box(x0 + pw/2 + .12 + k*.09, x0 + pw/2 + .18 + k*.09, y0 + .03, y0 + .08, z + .038, z + .05))
def lean(p, xs, z, y=.8, pw=.1, pd=.1):  # titanium lean rail per bay, ends + back embedded in posts (lived-in)
    zf = z + pd/2
    for i in range(len(xs) - 1): p.add("Lean_Rail", T, box(xs[i] + pw/2 - E, xs[i+1] - pw/2 + E, y - .02, y + .02, zf - .006, zf + .03))
def hooks(p, xs, z, y=1.55):  # bag/coat hooks on posts (lived-in hardware)
    p.add("Hook_Hardware", T, *[box(x - .015, x + .015, y, y + .05, z + .05 - E, z + .1) for x in xs])

def shelter(v):
    p = Pod(f"ext_tram_shelter_0{v}")
    if v == 1:  # Civic Canopy: 4 gunmetal posts per line, slate flat roof, cyan fascia, rear glass + timetable bay, half side screens
        xs = [-2.9, -1.0, 1.0, 2.9]; posts(p, xs, [ZR], 2.6 + E); posts(p, [-2.9, 2.9], [ZF], 2.6 + E)
        kick(p, xs, ZR); wall_glass(p, xs, ZR, .3 - E, 2.4 + E, skip=(1,)); timetable(p, -1.0, 1.0, ZR)
        p.add("Rear_Glass", GL, box(-.952, .952, .3 - E, 1.0 + E, ZR - .006, ZR + .006), box(-.952, .952, 1.9 - E, 2.4 + E, ZR - .006, ZR + .006))
        kick(p, xs, ZR, 2.4, 2.47, name="Head_Rail")
        for x in (-2.9, 2.9): p.add("Side_Glass", GL, box(x - .006, x + .006, .3, 2.4, ZR + .05 - E, .15))
        p.add("Roof", S, blk(-W2, W2, 2.6, 2.7, -.65, .62, .03, 1))
        p.add("Fascia", CY, box(-W2 - .01, W2 + .01, 2.58, 2.72, .616, .65))
        p.add("Roof_Downlight", A, box(-2.5, 2.5, 2.585, 2.6 + E, .1, .16))
        p.add("Arrival_Beacon", A, box(2.4, 2.8, 2.6, 2.68, .65 - E, .665))
        lean(p, xs, ZR); hooks(p, [-1.0, 1.0], ZR)
    elif v == 2:  # Rear Spine Cantilever: rear posts only, gunmetal cantilever beams, titanium roof, pearl fascia, open sides
        xs = [-2.8, -.95, .95, 2.8]; posts(p, xs, [ZR], 2.5 + E, d=.14)
        p.add("Cantilever_Beams", G, *[box(x - .06, x + .06, 2.5, 2.6, -.65, .58) for x in xs])
        p.add("Roof", T, blk(-W2, W2, 2.6 - E, 2.66, -.66, .6, .02, 1))
        p.add("Fascia", PL, box(-W2 - .01, W2 + .01, 2.56, 2.7, .596, .63))
        p.add("Civic_Stripe", CY, box(-W2 - .01, W2 + .01, 2.6, 2.64, .63 - E, .636))
        kick(p, xs, ZR); wall_glass(p, xs, ZR, .3 - E, 2.502, skip=(0,))
        timetable(p, -2.8, -.95, ZR, 1.0, 1.9)
        p.add("Rear_Glass", GL, box(-2.752, -.998, .3 - E, 1.0 + E, ZR - .006, ZR + .006), box(-2.752, -.998, 1.9 - E, 2.502, ZR - .006, ZR + .006))
        p.add("Roof_Downlight", A, *[box(-2.75 + i*1.85 + .15, -2.75 + (i+1)*1.85 - .25, 2.585, 2.6 + E, .2, .26) for i in range(3)])
        p.add("Arrival_Beacon", A, ring(.06, 2.66 - E, 2.76, 10, x=2.8, z=-.55))
        lean(p, xs, ZR, pd=.14); hooks(p, [-.95, .95], ZR + .02)
    elif v == 3:  # Mono-Pitch Skylight: slim posts, titanium-framed roof pitched 5 deg down to the front with a BLEND glass skylight in a real cut-out
        xs = [-2.9, 0.0, 2.9]; a = np.radians(5)
        Rm = np.eye(4); Rm[:3, :3] = [[1, 0, 0], [0, np.cos(a), np.sin(a)], [0, -np.sin(a), np.cos(a)]]  # +z end drops
        y0 = 2.62; uy = lambda z: y0 - z * np.tan(a)  # roof underside height at z
        def R(m): m.apply_translation((0, -y0, 0)); xf(m, R=Rm); m.apply_translation((0, y0, 0)); return m
        for z in (ZR, ZF): posts(p, xs, [z], 0, w=.08, d=.06)
        p.P.pop("Posts")
        for z in (ZR, ZF): p.add("Posts", G, *[box(x - .04, x + .04, 0, uy(z) + .0035, z - .03, z + .03) for x in xs])
        fr = [box(-W2, W2, y0, y0 + .08, -.66, -.3), box(-W2, W2, y0, y0 + .08, .3, .64), box(-W2, -2.6, y0, y0 + .08, -.3 - E, .3 + E),
              box(2.6, W2, y0, y0 + .08, -.3 - E, .3 + E), box(-.15, .15, y0, y0 + .08, -.3 - E, .3 + E)]
        p.add("Roof_Frame", T, *[R(m) for m in fr])
        p.add("Skylight_Glass", GL, *[R(box(x0 - E, x1 + E, y0 + .03, y0 + .05, -.302, .302)) for x0, x1 in ((-2.6, -.15), (.15, 2.6))])
        p.add("Fascia", CY, R(box(-W2 - .01, W2 + .01, y0 - .03, y0 + .1, .636, .67)))
        kick(p, xs, ZR, pw=.08, dz=.024); wall_glass(p, xs, ZR, .3 - E, 2.45, pw=.08, skip=(1,)); timetable(p, 0.0, 2.9, ZR, 1.0, 1.9, pw=.08)
        p.add("Rear_Glass", GL, box(.038, 2.862, .3 - E, 1.0 + E, ZR - .006, ZR + .006), box(.038, 2.862, 1.9 - E, 2.45, ZR - .006, ZR + .006))
        for x in (-2.9, 2.9): p.add("Side_Glass", GL, box(x - .006, x + .006, .3, 2.4, ZR + .03 - E, ZF - .03 + E))
        p.add("Roof_Downlight", A, R(box(-2.5, 2.5, y0 - .015, y0 + E, -.5, -.44)))
        p.add("Arrival_Beacon", A, box(2.94 - E, 2.97, 2.0, 2.3, ZF - .02, ZF + .02))
        lean(p, xs, ZR, pw=.08, pd=.06)
    elif v == 4:  # Pearl Kiosk Wall: pearl-clad solid rear wall with cyan band + clerestory glass, timetable in a wall cut-out, gunmetal roof, amber edge glow
        xs = [-2.9, 2.9]; posts(p, xs, [ZR, ZF], 2.6 + E)
        wz = ZR; t = .04
        p.add("Wall_Cladding", PL, box(-2.85 - E, 2.85 + E, .02, 1.0, wz - t, wz + t),                       # below panel
              box(-2.85 - E, -.9, .998, 1.902, wz - t, wz + t), box(.9, 2.85 + E, .998, 1.902, wz - t, wz + t),  # beside panel
              box(-2.85 - E, 2.85 + E, 1.9, 2.1, wz - t, wz + t))
        p.add("Civic_Band", CY, box(-2.854, 2.854, 2.1 - E, 2.18, wz - t - .004, wz + t + .004))
        p.add("Clerestory_Glass", GL, box(-2.85 - E, 2.85 + E, 2.18 - E, 2.6 + E, wz - .006, wz + .006))
        p.add("Timetable_Frame", S, box(-.9 - E, .9 + E, 1.0 - E, 1.9 + E, wz - .046, wz + .046))
        p.add("Timetable_Screen", CY, box(-.8, .8, 1.1, 1.8, wz + .042, wz + .052))
        p.add("Route_Pips", A, *[box(-.76 + k*.09, -.7 + k*.09, 1.03, 1.08, wz + .043, wz + .056) for k in range(3)])
        for x in xs: p.add("Side_Glass", GL, box(x - .006, x + .006, .3, 2.4, ZR + .05 - E, ZF - .05 + E))
        p.add("Roof", G, blk(-W2, W2, 2.6, 2.7, -.65, .65, .04, 2))
        p.add("Edge_Glow", A, box(-2.9, 2.9, 2.57, 2.6 + E, .605, .635))
        p.add("Roof_Downlight", A, box(-2.4, 2.4, 2.585, 2.6 + E, -.2, -.14))
        p.add("Arrival_Beacon", A, cyl(2.9, ZF, .035, 2.6 + E - .0, 2.6 + E, 8)) if False else p.add("Arrival_Beacon", A, box(2.95 - E, 2.99, 2.2, 2.5, ZF - .02, ZF + .02))
        p.add("Lean_Rail", T, box(-2.85 - E, 2.85 + E, .78, .82, wz + t - E, wz + t + .03))
        hooks(p, [-2.0, 2.0], wz - .01)
    elif v == 5:  # Glass Pavilion: slender titanium mullions, glass rear + full sides + half front windbreak, pearl roof wrapped in a cyan band
        xs = [-2.9, -1.45, 0.0, 1.45, 2.9]; posts(p, xs, [ZR], 2.556, w=.06, d=.06, mat=T, name="Mullions")
        posts(p, [-2.9, -1.45, 2.9], [ZF], 2.556, w=.06, d=.06, mat=T, name="Mullions")
        kick(p, xs, ZR, .12, .26, pw=.06, mat=S, dz=.024)
        wall_glass(p, xs, ZR, .26 - E, 2.552, pw=.06, skip=(2,)); timetable(p, 0.0, 1.45, ZR, 1.0, 1.9, pw=.06)
        p.add("Rear_Glass", GL, box(.028, 1.422, .26 - E, 1.0 + E, ZR - .006, ZR + .006), box(.028, 1.422, 1.9 - E, 2.552, ZR - .006, ZR + .006))
        for x in (-2.9, 2.9): p.add("Side_Glass", GL, box(x - .006, x + .006, .26, 2.552, ZR + .03 - E, ZF - .03 + E))
        p.add("Front_Windbreak", GL, box(-2.87 - E, -1.48 + E, .26, 2.2, ZF - .006, ZF + .006))
        p.add("Roof", PL, blk(-W2, W2, 2.55, 2.6, -.64, .64, .05, 2), blk(-W2, W2, 2.66, 2.7, -.64, .64, .05, 2))
        p.add("Civic_Band", CY, blk(-W2 - .012, W2 + .012, 2.6 - E, 2.66 + E, -.652, .652, .06, 2))
        p.add("Roof_Downlight", A, box(-2.6, 2.6, 2.535, 2.55 + E, -.05, .05))
        p.add("Arrival_Beacon", A, ring(.05, 2.7 - E, 2.8, 10, x=2.75, z=.45))
        lean(p, xs, ZR, pw=.06, pd=.06); hooks(p, [-1.45, 1.45], ZR - .02)
    return p
ITERS = [(1, "Civic_Canopy"), (2, "Rear_Spine_Cantilever"), (3, "Mono_Pitch_Skylight"), (4, "Pearl_Kiosk_Wall"), (5, "Glass_Pavilion")]
sf.ASSETS["tram_shelter"] = ("ext_tram_shelter", shelter, ITERS, 5800, "#15 tram stop shelter 6.0x1.3x2.8")

if __name__ == "__main__":
    rep = sf.build("tram_shelter")
    import validate_models as vm
    for r in rep: print(r["cand"], "validate", vm.validate_file(os.path.join(sf.ROOT, r["glb"]), require_textures=False, require_blend_glass=True))
