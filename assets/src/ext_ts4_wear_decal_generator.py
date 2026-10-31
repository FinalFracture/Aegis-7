"""Rook: #49 TS-4 wear decal set (patch tape + mismatched liner decals + dead-foliage material swap).
Candidates -> design/assets/ext_ts4_wear_decal/ext_ts4_wear_decal_NN.glb (decal overlay) + ext_ts4_dead_foliage_NN.glb (TS-4 with
dead-foliage material swap). Overlay shares the TS-4 pivot (bottom-centre, +Z front): place it with the SAME transform as the planter.
Decals sit 3 mm in front (+Z) of the TS-4 riser faces (z 0.200 / 0.059 / -0.061); tape layer is +1.5 mm over the liner layer.
Zones avoid the latches (x 0, +/-1.5) and lids."""
import numpy as np, trimesh, json, copy
from PIL import Image, ImageDraw, ImageFilter
SRC = "godot/assets/models/hydro_planter_tiered_exterior.glb"; OUT = "design/assets/ext_ts4_wear_decal"
OFF, DY = 0.003, 0.0015
GUN, SLATE, TI, AMB, PEARL = (26,30,36), (40,46,56), (150,156,164), (255,149,0), (226,228,222)
RISERS = {1: (0.200, .213, .247), 2: (0.059, .262, .375), 3: (-0.061, .440, .565)}  # z face, y0, y1 (clear of latches/lids)
XWIN = [(-1.95, -1.55), (-1.45, -.05), (.05, 1.45), (1.55, 1.95)]

def tex(kind, rgb, seed, a=.9):
    rng = np.random.default_rng(seed); im = Image.new("RGBA", (256, 128), rgb + (0,)); d = ImageDraw.Draw(im)
    if kind == "tape":  # torn-end amber tape strip, wordless
        d.rectangle([6, 20, 250, 108], fill=rgb + (int(a*255),))
        for x in (6, 250):
            for y in range(20, 108, 8): d.polygon([(x, y), (x + (8 if x == 6 else -8), y + 4), (x, y + 8)], fill=rgb + (0,))
        d.line([6, 40, 250, 44], fill=(255, 190, 90, int(a*200)), width=3)
    elif kind == "liner":  # mismatched panel with seam + edge grime
        d.rectangle([4, 4, 252, 124], fill=rgb + (int(a*255),)); d.rectangle([4, 4, 252, 124], outline=GUN + (220,), width=5)
        d.line([128 + rng.integers(-30, 30), 4, 128, 124], fill=GUN + (160,), width=2)
    elif kind == "bolted":  # liner with rivet dots
        d.rectangle([4, 4, 252, 124], fill=rgb + (int(a*255),))
        for x in (16, 240):
            for y in (16, 112): d.ellipse([x-5, y-5, x+5, y+5], fill=TI + (255,))
    return im.filter(ImageFilter.GaussianBlur(.8))

def quad(x0, x1, y0, y1, z, im):
    V = np.array([[x0, y0, z], [x1, y0, z], [x1, y1, z], [x0, y1, z]]); F = [[0, 1, 2], [0, 2, 3]]  # +Z facing
    m = trimesh.Trimesh(V, F, process=False)
    mat = trimesh.visual.material.PBRMaterial(baseColorTexture=im, alphaMode="BLEND", roughnessFactor=.8, metallicFactor=0)
    m.visual = trimesh.visual.TextureVisuals(uv=np.array([[0, 0], [1, 0], [1, 1], [0, 1]]), material=mat); return m

# each item: (layer 0=liner/1=tape, riser, xwindow idx, frac start, frac end, kind, colour, seed)
CANDS = {
 "01": ("Amber Field Patch", "two amber tape strips across riser cracks + one slate liner; minimum story, strongest amber read",
        [(1,1,1,.2,.5,"tape",AMB,1),(1,2,2,.4,.7,"tape",AMB,2),(0,3,1,.3,.6,"liner",SLATE,3)], (92,78,52)),
 "02": ("Mismatched Pearl", "civic-pearl spare liners on the white-composite tiers (wrong shade, wrong era) taped at seams",
        [(0,2,1,.1,.5,"liner",PEARL,4),(1,2,1,.08,.18,"tape",AMB,5),(0,3,2,.5,.9,"liner",PEARL,6),(1,3,2,.82,.92,"tape",AMB,7)], (110,92,60)),
 "03": ("Riveted Repair", "gunmetal bolted repair plates (rivets in titanium) + tape on the lip; reads as engineered make-do",
        [(0,2,2,.2,.6,"bolted",GUN,8),(0,3,0,.0,1.,"bolted",GUN,9),(1,1,2,.3,.6,"tape",AMB,10)], (84,72,58)),
 "04": ("Layered Bodge", "liner over liner over tape across all three tiers; heaviest wear, the 'dead planter' looks long neglected",
        [(0,1,1,.1,.9,"liner",SLATE,11),(1,1,1,.4,.55,"tape",AMB,12),(0,2,1,.0,.6,"liner",PEARL,13),(1,2,1,.5,.7,"tape",AMB,14),
         (0,3,2,.1,.6,"liner",SLATE,15),(1,3,2,.3,.4,"tape",AMB,16),(0,3,3,.0,1.,"liner",GUN,17)], (70,62,50)),
 "05": ("Single Scar", "one long amber tape seal along the mid tier + one small slate liner; subtle, lets the dead foliage carry the beat",
        [(1,2,2,.05,.95,"tape",AMB,18),(0,3,0,.1,.9,"liner",SLATE,19)], (118,98,66)),
}

def build(c):
    s = trimesh.Scene()
    for k, (lay, r, w, f0, f1, kind, col, seed) in enumerate(CANDS[c][2]):
        z, y0, y1 = RISERS[r]; a, b = XWIN[w]; x0, x1 = a + (b-a)*f0, a + (b-a)*f1
        s.add_geometry(quad(x0, x1, y0, y1, z + OFF + lay*DY, tex(kind, col, seed)), geom_name=f"{kind}_{k}_L{lay}")
    return s

def dead(c):
    s = trimesh.load(SRC); s = copy.deepcopy(s); base = CANDS[c][3]
    for n, g in s.geometry.items():
        if n.startswith("Foliage"):
            m = g.visual.material if hasattr(g.visual, "material") else None
            col = list(base) + [255] if n == "Foliage" else [min(255, v + 18) for v in base] + [255]
            g.visual = trimesh.visual.TextureVisuals(uv=getattr(g.visual, "uv", None),
                material=trimesh.visual.material.PBRMaterial(name="DeadFoliage", baseColorFactor=col, roughnessFactor=.95, metallicFactor=0))
    return s

def check(s):
    host = trimesh.load(SRC); hparts = []
    for n, g in host.geometry.items(): hparts += [(n, p) for p in g.split(only_watertight=False)]
    hall = trimesh.util.concatenate([g for g in host.geometry.values()])
    r = dict(tris=0, min_clear_m=1., inside_hits=0, host_gap_ok=True, coplanar_pairs=0, uv=True, blend=True)
    gs = list(s.geometry.items())
    for n, g in gs:
        r["tris"] += len(g.faces); r["uv"] &= g.visual.uv is not None; r["blend"] &= g.visual.material.alphaMode == "BLEND"
        P = np.vstack([g.vertices, trimesh.sample.sample_surface(g, 400, seed=1)[0]])
        _, d, _ = trimesh.proximity.closest_point(hall, P); r["min_clear_m"] = min(r["min_clear_m"], float(d.min()))
        for hn, hp in hparts:
            if hp.is_watertight and hp.volume > 0: r["inside_hits"] += int(hp.contains(P).sum())
        z = g.vertices[0, 2]; lay = int(n[-1]); r["host_gap_ok"] &= any(abs(z - (rz + OFF + lay*DY)) < 1e-6 for rz, _, _ in RISERS.values())
    for i, (na, a) in enumerate(gs):  # overlapping decals must differ in z by >1 mm
        for nb, b in gs[i+1:]:
            ov = (np.minimum(a.bounds[1], b.bounds[1]) - np.maximum(a.bounds[0], b.bounds[0]))[:2]
            if (ov > 0).all() and abs(a.vertices[0, 2] - b.vertices[0, 2]) <= .001: r["coplanar_pairs"] += 1
    r["min_clear_m"] = round(r["min_clear_m"], 4)
    r["pass"] = r["tris"] < 6000 and r["min_clear_m"] >= .002 and r["inside_hits"] == 0 and r["host_gap_ok"] and r["coplanar_pairs"] == 0 and r["uv"] and r["blend"]
    return r

if __name__ == "__main__":
    rep = {}
    for c in CANDS:
        s = build(c); s.export(f"{OUT}/ext_ts4_wear_decal_{c}.glb"); dead(c).export(f"{OUT}/ext_ts4_dead_foliage_{c}.glb")
        rep[c] = check(s); print(c, rep[c])
    json.dump(rep, open(f"{OUT}/ext_ts4_wear_decal_report.json", "w"), indent=1)
