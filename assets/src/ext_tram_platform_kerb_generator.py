"""Rook (Oct 30, box pipeline): residential exterior list v1 #16 tram platform kerb module (x6 along X 9..21), 2.0 W x 1.9 D x 0.3 H, ~300 tris.
Five candidates -> design/assets/ext_tram_platform_kerb/ext_tram_platform_kerb_01..05.glb + contact sheet.
Tiles end-to-end along X at a 2.000 m pitch: nothing passes x = +/-0.997 (6 mm joint between modules). +Z = track edge.
Placement: modules cover the platform front Z -18.5..-16.6 (track edge at -18.5, rotate 180 deg); top surface = platform level y 0.30,
so ext_tram_shelter (Z -16.9..-15.6) sits at y 0.30 with its front 0.30 m strip on module 2-5 backs (X 12..18 = modules 2..5).
Aegis-7 + Civic pearl/cyan, amber emissive edge/tactile, zero wood, wordless. Joints embed 0.004 m.
Run: python3 ext_tram_platform_kerb_generator.py"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import ext_street_furniture_generator as sf
from ext_street_furniture_generator import Pod, box, blk, FMAT, _PBR, G, S, T, A, GL, E
FMAT["a7_pearl"] = _PBR(name="A7_PearlAlabaster", baseColorFactor=(0xD8/255, 0xDE/255, 0xE4/255, 1), metallicFactor=0.15, roughnessFactor=0.45)
FMAT["a7_cyan"] = _PBR(name="A7_CivicCyan", baseColorFactor=(0x38/255, 0xB8/255, 0xC8/255, 1), metallicFactor=0.1, roughnessFactor=0.4)
PL, CY = "a7_pearl", "a7_cyan"
X, XB, ZB, ZF, H = .997, .99, -.95, .95, .30   # deck half-width, body half-width (inset), back, front, height

def kerb(v):
    p = Pod(f"ext_tram_platform_kerb_0{v}")
    if v == 1:  # Pearl Deck: slate body, pearl deck, titanium nosing, amber edge line
        p.add("Body", S, box(-XB, XB, 0, .26 + E, ZB + .01, ZF - .052))
        p.add("Deck", PL, box(-X, X, .26, H - .01, ZB, ZF - .05))
        p.add("Nosing", T, box(-X, X, .02, H, ZF - .05 - E, ZF))
        p.add("Edge_Light", A, box(-.95, .95, H - .01 - E, H - .004, ZF - .15, ZF - .1))
    elif v == 2:  # Cyan Tactile: gunmetal body, pearl deck, raised cyan tactile bars, amber safety line
        p.add("Body", G, box(-XB, XB, 0, .27 + E, ZB + .01, ZF - .01))
        p.add("Deck", PL, box(-X, X, .27, H - .006, ZB, ZF))
        p.add("Tactile_Bars", CY, *[box(-.95, .95, H - .006 - E, H, z - .02, z + .02) for z in (.42, .5, .58, .66)])
        p.add("Safety_Line", A, box(-.95, .95, H - .006 - E, H - .002, ZF - .14, ZF - .08))
    elif v == 3:  # Overhang Lip: slate body set back, gunmetal lip cantilevered to the track with an amber under-glow
        p.add("Body", S, box(-XB, XB, 0, .24 + E, ZB + .01, ZF - .202))
        p.add("Deck", S, box(-X, X, .24, H - .01, ZB, ZF - .2))
        p.add("Lip", G, box(-X, X, .2, H, ZF - .2 - E, ZF))
        p.add("Under_Glow", A, box(-.9, .9, .2 - .015, .2 + E, ZF - .14, ZF - .1))
        p.add("Edge_Strip", CY, box(-.95, .95, H - E, H + .004, ZF - .12, ZF - .06))
    elif v == 4:  # Drain Grate: deck split around a real titanium drainage grate cut-out, amber edge, pearl back strip
        p.add("Body", G, box(-XB, XB, 0, .26 + E, ZB + .01, ZF - .01))
        p.add("Deck", S, box(-X, X, .26, H - .008, ZB, -.1), box(-X, X, .26, H - .008, .1, ZF))
        p.add("Grate_Frame", T, box(-X + .002, X - .002, .261, H - .01, -.1 - E, .1 + E))
        p.add("Grate_Bars", T, *[box(-.94, .94, H - .01 - E, H - .004, z - .012, z + .012) for z in (-.06, -.02, .02, .06)])
        p.add("Back_Strip", PL, box(-.95, .95, H - .008 - E, H - .004, ZB + .05, ZB + .15))
        p.add("Edge_Light", A, box(-.95, .95, H - .008 - E, H - .002, ZF - .12, ZF - .07))
    elif v == 5:  # Chevron Wayfinding: pearl deck, wordless cyan boarding chevrons, chamfered titanium nosing, amber edge
        p.add("Body", S, box(-XB, XB, 0, .27 + E, ZB + .01, ZF - .044))
        p.add("Deck", PL, blk(-X, X, .27, H - .006, ZB, ZF - .04, .004, 1))
        p.add("Nosing", T, sf.loft(sf.np.array([(X, .02), (-X, .02), (-X, -.02), (X, -.02)]), [(.02, 1, 1), (H - .01, 1, 1), (H - .002, 1, .5)]))
        p.P["Nosing"][1].apply_translation((0, 0, ZF - .02 - E/2)); p.P["Nosing"][1].metadata["uv"] = p.P["Nosing"][1].metadata["uv"]
        for x in (-.5, .5):
            p.add("Chevrons", CY, sf.xf(sf.loft(sf.np.array([(0, .12), (-.12, -.04), (-.06, -.04), (0, .04), (.06, -.04), (.12, -.04)]), [(H - .006 - E, 1, 1), (H, 1, 1)]), t=(x, 0, .3)))
        p.add("Edge_Light", A, box(-.95, .95, H - .006 - E, H - .002, ZF - .14, ZF - .09))
    return p
ITERS = [(1, "Pearl_Deck"), (2, "Cyan_Tactile"), (3, "Overhang_Lip"), (4, "Drain_Grate"), (5, "Chevron_Wayfinding")]
sf.ASSETS["kerb"] = ("ext_tram_platform_kerb", kerb, ITERS, 300, "#16 tram platform kerb 2.0x1.9x0.3 (tiles @2.0 m, +Z track)")

if __name__ == "__main__":
    rep = sf.build("kerb")
    import validate_models as vm
    for r in rep: print(r["cand"], "validate", vm.validate_file(os.path.join(sf.ROOT, r["glb"]), require_textures=False))
