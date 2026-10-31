"""Rook (Oct 31, box pipeline): residential exterior list v1 #44 paving tile kit (pearl promenade + warm plaza); after the 5:04 AM road cut it also paves
the former Spin St / lane beds as pedestrian walkways. Five candidate kits; each kit = 2 tiling GLBs:
  ext_paving_promenade_0N.glb (pearl, cyan accents) + ext_paving_plaza_0N.glb (warm composite stone, amber accents)  -> design/assets/ext_paving_kit/
Tile 2.0 (X, axial, flat) x 2.0 (Z, arc length on the R 185.5 floor, bent like the walking floor) x 0.05. Pavers stop 3 mm inside the tile edge
(6 mm joints between tiles, 6 mm internal joints). Consecutive tiles: +2.0 m in X; along Z rotate 0.6177 deg (2/185.5 rad) about the spin axis.
Paving top y 0.05. #41 curb sits on the paving top (embedded 3 mm, y 0.047, any orientation; joints may cross). #16 platform kerb (y 0..0.30) stands on the
road-base level y 0 - paving butts its back/ends with a 4 mm gap; platform infill behind the kerb (Z -16.6..-15.5 at y 0.30) is NOT in this kit (flag).
Decal/inlay pieces float 2 mm above or sit in real joints. Zero wood, wordless. Run: python3 ext_paving_kit_generator.py"""
import os, sys, json, numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import ext_street_furniture_generator as sf
from ext_street_furniture_generator import Pod, FMAT, _PBR, G, S, T, A, E
from ext_road_curved_generator import bend, rect, PL, CY
FMAT["a7_warm"] = _PBR(name="A7_WarmComposite", baseColorFactor=(0xC8/255, 0xA0/255, 0x7A/255, 1), metallicFactor=0.05, roughnessFactor=0.75)
FMAT["a7_warm2"] = _PBR(name="A7_WarmComposite_Dark", baseColorFactor=(0xA8/255, 0x7C/255, 0x5C/255, 1), metallicFactor=0.05, roughnessFactor=0.8)
WM, WD = "a7_warm", "a7_warm2"; H = .05; TE = .997; J = .003   # tile half-extent, half-joint

def pav(x0, x1, z0, z1, h=H): n = max(1, int(round((z1 - z0) / 1.0))); return bend(rect(x0, x1, 0, h), z0, z1, n)
def dec(x0, x1, z0, z1, t=.002, h=H): n = max(1, int(round((z1 - z0) / 1.0))); return bend(rect(x0, x1, h + .002, h + .002 + t), z0, z1, n)
def grid(xs, zs):  # paver rectangles from cut lines (tile edges +/-1.0), joints 6 mm
    return [(xs[i] + J, xs[i+1] - J, zs[j] + J, zs[j+1] - J) for i in range(len(xs) - 1) for j in range(len(zs) - 1)]

def tile(v, kind):
    warm = kind == "plaza"; p = Pod(f"ext_paving_{kind}_0{v}"); M = WM if warm else PL; M2 = WD if warm else S; ACC = A if warm else CY
    if v == 1:  # Grid Slab: 2x2 large square slabs
        p.add("Pavers", M, *[pav(*r) for r in grid([-1, 0, 1], [-1, 0, 1])])
    elif v == 2:  # Running Bond: 4 rows of 0.5 m pavers along X, alternate rows half-offset (half pieces at the tile edges)
        rs = []
        for j, z in enumerate([-1, -.5, 0, .5]):
            xs = [-1, 0, 1] if j % 2 == 0 else [-1, -.5, .5, 1]
            rs += [(xs[i] + J, xs[i+1] - J, z + J, z + .5 - J) for i in range(len(xs) - 1)]
        p.add("Pavers", M, *[pav(*r) for r in rs[::2]]); p.add("Pavers_Alt", M2, *[pav(*r) for r in rs[1::2]])
    elif v == 3:  # Titanium Inlay Cross: 4 slabs with titanium inlay strips set inside the centre joints (1 mm clear each side)
        p.add("Pavers", M, *[pav(*r) for r in grid([-1, -.002, .002, 1], [-1, -.002, .002, 1]) if r[1] - r[0] > .1 and r[3] - r[2] > .1])
        il = lambda x0, x1, z0, z1: bend(rect(x0, x1, .01, H - .008), z0, z1, max(1, int(round((z1 - z0)))))
        p.add("Inlay", T, il(-.0025, .0025, -TE, TE), il(-TE, -.006, -.0025, .0025), il(.006, TE, -.0025, .0025))
    elif v == 4:  # Tactile Guidance: 2 side slabs + a centre guidance strip of raised bars (wayfinding for the new walkways)
        p.add("Pavers", M, pav(-TE, -.15 - J, -TE, TE), pav(.15 + J, TE, -TE, TE))
        p.add("Guide_Strip", M2, pav(-.15 + J, .15 - J, -TE, TE))
        p.add("Tactile_Bars", ACC, *[dec(x - .02, x + .02, -TE + .02, TE - .02, .004) for x in (-.08, 0, .08)])
    elif v == 5:  # Lit Joint: two long slabs split by a real glow channel (cyan / amber emissive) along Z
        p.add("Pavers", M, pav(-TE, -.03, -TE, TE), pav(.03, TE, -TE, TE))
        p.add("Glow_Channel", ACC, pav(-.024, .024, -TE, TE, H - .008))
        p.add("Edge_Bands", M2, *[dec(s * .9 - .05, s * .9 + .05, -TE + .01, TE - .01) for s in (1, -1)])
    return p
ITERS = [(1, "Grid_Slab"), (2, "Running_Bond"), (3, "Titanium_Inlay_Cross"), (4, "Tactile_Guidance"), (5, "Lit_Joint")]
for kind in ("promenade", "plaza"):
    sf.ASSETS[kind] = (f"ext_paving_{kind}", (lambda k: (lambda v: tile(v, k)))(kind), ITERS, 200,
                       f"#44 paving {'pearl promenade' if kind == 'promenade' else 'warm plaza'} tile 2.0x2.0x0.05 on R 185.5")

def tiling_check(v, kind):
    from ext_curb_generator import curb
    from ext_street_furniture_generator import xf
    import ext_clip_check as cc
    a = 2.0 / 185.5; asm = {}
    for i, dx in enumerate((-1.0, 1.0)):
        for j, k_ in enumerate((0, 1)):
            for k, (mk, m) in tile(v, kind).P.items():
                m.apply_translation((dx, 0, 0))
                if k_: Rm = np.eye(4); Rm[1:3, 1:3] = [[np.cos(a), np.sin(a)], [-np.sin(a), np.cos(a)]]; m.apply_translation((0, -185.5, 0)); xf(m, R=Rm); m.apply_translation((0, 185.5, 0))
                asm[f"T{i}{j}_{k}"] = (mk, m)
    for k, (mk, m) in curb(1).P.items(): m.apply_translation((-.6, H - .003, -.4)); asm["C_" + k] = (mk, m)   # curb on paving top, across a tile joint
    r = cc.check(asm); return dict(bad=[o for o in r["overlap"] if not o[3]], coplanar=r["coplanar"], open=r["open"])

if __name__ == "__main__":
    import validate_models as vm; out = {}
    for kind in ("promenade", "plaza"):
        for r, (v, nm) in zip(sf.build(kind), ITERS):
            r["validate"] = vm.validate_file(os.path.join(sf.ROOT, r["glb"]), require_textures=False); r["tiling_curb"] = tiling_check(v, kind)
            out[r["cand"]] = r; print("RES", r["cand"], r["tris"], r["clip_pass"], r["worst_overlap"], r["coplanar"][:2], r["validate"], json.dumps(r["tiling_curb"])[:300])
    json.dump(out, open(os.path.join(sf.ROOT, "design/assets/ext_paving_kit_checks.json"), "w"), indent=1)
