"""Rook (Oct 30, box pipeline): residential exterior list v1 #17 tram rail module (twin-rail axial track, x10), 10 W x 3.5 D x 0.2 H, ~400 tris.
Five candidates -> design/assets/ext_tram_rail_module/ext_tram_rail_module_01..05.glb + contact sheet.
Track runs along X (axial). Standard gauge 1.435 m (rail centres z = +/-0.7535 with 0.072 heads), top of rail (TOR) y = 0.20.
Tiles end-to-end at a 10.000 m pitch: bed ends at x +/-4.994, rails at +/-4.997 (12 mm bed joint, 6 mm rail gap; all repeats at 2.0 / 2.5 m divide 10).
Placement (same orientation as #16 kerb): module +Z edge = platform side. Rotate 180 deg about Y, centre at Z -20.25 -> covers Z -18.5..-22.0,
abutting the kerb front at Z -18.5, road at y 0. TOR 0.20 + low-floor height 0.10 = 0.30 = platform level (level boarding; car 2.6 wide ->
0.45 m from kerb face; #19 should add a 0.35 m boarding sill/step or we shift the track +0.35 m).
Zero wood: slab / composite / steel only. Aegis-7 + amber emissive markers, Civic cyan edge. Joints embed 0.004 m.
Run: python3 ext_tram_rail_module_generator.py"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import ext_street_furniture_generator as sf
from ext_street_furniture_generator import Pod, box, blk, FMAT, _PBR, G, S, T, A, E
FMAT["a7_pearl"] = _PBR(name="A7_PearlAlabaster", baseColorFactor=(0xD8/255, 0xDE/255, 0xE4/255, 1), metallicFactor=0.15, roughnessFactor=0.45)
FMAT["a7_cyan"] = _PBR(name="A7_CivicCyan", baseColorFactor=(0x38/255, 0xB8/255, 0xC8/255, 1), metallicFactor=0.1, roughnessFactor=0.4)
PL, CY = "a7_pearl", "a7_cyan"
XB, XR, ZH, TOR = 4.994, 4.997, 1.75, .20
RZ = (-.7535, .7535); HW = .036; ZP = 1.396   # rail centres, head half-width

def rails(p, y0, foot=None):
    p.add("Rails", T, *[box(-XR, XR, y0, TOR, z - HW, z + HW) for z in RZ])
    if foot: p.add("Rail_Feet", G, *[box(-XR + .001, XR - .001, foot, y0 + E, z - .07, z + .07) for z in RZ])

def track(v):
    p = Pod(f"ext_tram_rail_module_0{v}")
    if v == 1:  # Embedded Street Slab: slate base, top slab cut around rails (10 mm flangeways), rails flush-ish, cyan edge bands
        p.add("Base_Slab", G, box(-XB + .003, XB - .003, 0, .12, -ZH + .01, ZH - .01))
        zs = [-ZH, RZ[0] - HW - .012, RZ[0] + HW + .012, RZ[1] - HW - .012, RZ[1] + HW + .012, ZH]
        p.add("Top_Slab", S, *[box(-XB, XB, .12 - E, .19, zs[i], zs[i+1]) for i in (0, 2, 4)])
        rails(p, .12 - E)
        p.add("Edge_Bands", CY, *[box(-XB + .01, XB - .01, .19 - E, .194, z - .05, z + .05) for z in (-ZH + .1, ZH - .1)])
    elif v == 2:  # Composite Sleeper Block: gunmetal slab, five slate composite sleepers at 2.0 m, rails on gunmetal feet, amber clip hardware
        p.add("Base_Slab", G, box(-XB, XB, 0, .06, -ZH, ZH))
        p.add("Sleepers", S, *[box(x - .14, x + .14, .06 - E, .12, -1.2, 1.2) for x in (-4, -2, 0, 2, 4)])
        rails(p, .13, foot=.12 - E)
        p.add("Clip_Hardware", A, *[box(x - .04, x + .04, .12 - E, .145, z + s * .075, z + s * .105) if s > 0 else box(x - .04, x + .04, .12 - E, .145, z - .105, z - .075) for x in (-4, 0, 4) for z in RZ for s in (1, -1)])
    elif v == 3:  # Civic Lit Bed: pearl paved bed, slate rail strips, cyan edge kerbs, amber inset guide lights every 2.5 m
        p.add("Bed", PL, box(-XB, XB, 0, .17, -ZH, ZH))
        p.add("Rail_Strips", S, *[box(-XB + .002, XB - .002, .17 - E, .18, z - .2, z + .2) for z in RZ])
        rails(p, .18 - E)
        p.add("Edge_Kerbs", CY, *[box(-XB + .002, XB - .002, .17 - E, .2, z - .06, z + .06) for z in (-ZH + .08, ZH - .08)])
        p.add("Guide_Lights", A, *[box(x - .1, x + .1, .17 - E, .176, -.04, .04) for x in (-3.75, -1.25, 1.25, 3.75)])
    elif v == 4:  # Steel Ladder Track: twin titanium longitudinal beams tied by gunmetal cross-ties every 2.0 m on a carbon-slate trough
        p.add("Trough", S, box(-XB, XB, 0, .08, -ZH, ZH))
        p.add("Long_Beams", G, *[box(-XB + .001, XB - .001, .08 - E, .14, z - .16, z + .16) for z in RZ])
        p.add("Cross_Ties", G, *[box(x - .08, x + .08, .078, .12, RZ[0] + .16 - E, RZ[1] - .16 + E) for x in (-4, -2, 0, 2, 4)])
        rails(p, .14 - E)
        p.add("Edge_Stripes", A, *[box(-XB + .01, XB - .01, .08 - E, .084, z - .03, z + .03) for z in (-ZH + .15, ZH - .15)])
    elif v in (5, 6):  # 6 = 05 trimmed: platform-side (+Z) bed edge cut 0.35 m (ZP = 1.396 from track centre)  # Ground Power Rail: gunmetal slab, slate grooved deck, central titanium/amber ground-power strip (no catenary needed), cyan side lines
        zp = ZH if v == 5 else ZP
        p.add("Base_Slab", G, box(-XB + .003, XB - .003, 0, .12, -ZH + .01, zp - .01))
        g = .012; zs = [-ZH, RZ[0] - HW - g, RZ[0] + HW + g, -.06, .06, RZ[1] - HW - g, RZ[1] + HW + g, zp]
        p.add("Deck", S, *[box(-XB, XB, .12 - E, .19, zs[i], zs[i+1]) for i in (0, 2, 4, 6)])
        rails(p, .12 - E)
        p.add("Power_Rail", T, box(-XR, XR, .12 - E, .185, -.045, .045))
        p.add("Power_Markers", A, *[box(x - .2, x + .2, .185 - E, .19, -.03, .03) for x in (-3, -1, 1, 3)])
        p.add("Side_Lines", CY, *[box(-XB + .01, XB - .01, .19 - E, .194, z - .04, z + .04) for z in (-ZH + .2, zp - .2)])
    return p
ITERS = [(1, "Embedded_Street_Slab"), (2, "Composite_Sleeper_Block"), (3, "Civic_Lit_Bed"), (4, "Steel_Ladder_Track"), (5, "Ground_Power_Rail")]
sf.ASSETS["rail"] = ("ext_tram_rail_module", track, ITERS, 400, "#17 tram rail module 10x3.5 (gauge 1.435, TOR 0.20, tiles @10 m)")

if __name__ == "__main__":
    rep = sf.build("rail")
    import validate_models as vm
    for r in rep: print(r["cand"], "validate", vm.validate_file(os.path.join(sf.ROOT, r["glb"]), require_textures=False))
