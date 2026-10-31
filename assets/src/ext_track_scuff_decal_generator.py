"""Rook: #51 maglev track & scuff decals (guideway dust + stator wear streaks, platform-edge foot scuffs, kerb scuffs at the stop).
Sprocket's existing wheel-track decals (apron X 1..5.6, Z 9..11.65 + service door jamb, +Z side) are NOT touched; we assert no overlap.
Per candidate NN two overlay GLBs, each sharing its host's pivot (place with the host's exact transform):
  ext_track_scuff_guideway_NN.glb -> on ext_maglev_guideway.glb (10 m module; rot 0, origin Z -20.077)
  ext_track_scuff_kerb_NN.glb     -> on ext_tram_platform_kerb.glb (rot 180, origin Z -17.55), used on the stop kerbs
Decals: alpha BLEND quads 3 mm off the host surface (+1.5 mm per extra layer)."""
import numpy as np, trimesh, json
from PIL import Image, ImageDraw, ImageFilter
OUT = "design/assets/ext_track_scuff_decal"; OFF, DY = .003, .0015
GUN, SLATE, TI, AMB, PEARL, CY = (26,30,36), (40,46,56), (150,156,164), (255,149,0), (226,228,222), (0,200,230)
HOST = {"guideway": "godot/assets/models/ext_maglev_guideway.glb", "kerb": "godot/assets/models/ext_tram_platform_kerb.glb"}
WORLD = {"guideway": (0, -20.077, 0), "kerb": (15.0, -17.55, 180)}  # (x, z, yaw) representative instance
SPROCKET = (1.0, 5.6, 9.0, 11.65)  # apron XZ rect; door jamb at X 3.2 on +Z wall (Z ~11.65+)
# surfaces: name -> (axis, plane value, u-range, v-range)  axis 'y' = horizontal (u=x, v=z), 'z' = vertical front (u=x, v=y)
SURF = {"bed_s": ("y", .040, (-4.9, 4.9), (-1.30, -.45)), "bed_n": ("y", .040, (-4.9, 4.9), (.80, 1.30)),
        "flange": ("y", .160, (-4.9, 4.9), (-.36, .12)), "deck": ("y", .294, (-.95, .95), (-.90, .36)),
        "edge": ("y", .294, (-.95, .95), (.70, .79)), "face": ("z", .940, (-.95, .95), (.06, .26))}

def tex(kind, rgb, seed, a):
    rng = np.random.default_rng(seed); H, W = 128, 512; arr = np.zeros((H, W, 4), np.uint8); arr[..., :3] = rgb
    if kind == "dust":  # soft fine dust film, periodic in u so modules tile
        n = rng.random((8, 16)); n = np.array(Image.fromarray((n*255).astype(np.uint8)).resize((W, H), Image.BICUBIC))/255
        al = (.5 + .5*n) * a; al[:, :24] *= np.linspace(0, 1, 24); al[:, -24:] *= np.linspace(1, 0, 24)
    elif kind == "streak":  # long stator wear streaks along X
        al = np.zeros((H, W)); 
        for _ in range(6): y = rng.integers(10, H-10); al[y-2:y+2] += rng.uniform(.5, 1)
        al = np.clip(al, 0, 1) * a
    else:  # scuff: short arcs / sole smudges
        im = Image.new("L", (W, H)); d = ImageDraw.Draw(im)
        for _ in range(26 if kind == "feet" else 14):
            x, y = rng.integers(20, W-20), rng.integers(10, H-10); d.ellipse([x-14, y-6, x+14, y+6] if kind == "feet" else [x-30, y-3, x+30, y+3], fill=int(255*rng.uniform(.4, 1)))
        al = np.array(im)/255 * a
    arr[..., 3] = (np.clip(al, 0, 1)*255).astype(np.uint8); return Image.fromarray(arr).filter(ImageFilter.GaussianBlur(2))

def quad(surf, f0, f1, lay, im):
    ax, p, (u0, u1), (v0, v1) = SURF[surf]; a, b = v0 + (v1-v0)*f0, v0 + (v1-v0)*f1; o = p + OFF + lay*DY
    if ax == "y": V = np.array([[u0, o, a], [u1, o, a], [u1, o, b], [u0, o, b]]); F = [[0, 2, 1], [0, 3, 2]]
    else: V = np.array([[u0, a, o], [u1, a, o], [u1, b, o], [u0, b, o]]); F = [[0, 1, 2], [0, 2, 3]]
    m = trimesh.Trimesh(V, F, process=False)
    m.visual = trimesh.visual.TextureVisuals(uv=np.array([[0, 0], [1, 0], [1, 1], [0, 1]]),
        material=trimesh.visual.material.PBRMaterial(baseColorTexture=im, alphaMode="BLEND", roughnessFactor=.8, metallicFactor=0)); return m

HOSTOF = {"bed_s": "guideway", "bed_n": "guideway", "flange": "guideway", "deck": "kerb", "edge": "kerb", "face": "kerb"}
# items: (surface, f0, f1, layer, kind, rgb, alpha)
CANDS = {
 "01": ("Fine Dust", "light slate dust film on the guideway bed + faint sole scuffs at the edge; most restrained, clean-hab read",
        [("bed_s", 0, 1, 0, "dust", SLATE, .35), ("bed_n", 0, 1, 0, "dust", SLATE, .35), ("edge", 0, 1, 0, "feet", GUN, .35)]),
 "02": ("Stator Burnish", "titanium burnish streaks on the flange top where the car's magnets ride + dust + edge scuffs; reads as maglev, not wheels",
        [("flange", 0, 1, 0, "streak", TI, .55), ("bed_s", 0, 1, 0, "dust", SLATE, .3), ("bed_n", 0, 1, 0, "dust", SLATE, .3), ("edge", 0, 1, 0, "feet", GUN, .45)]),
 "03": ("Boarding Wear", "heavy foot scuffs at the boarding edge and on the deck + gunmetal kerb-face scuffs; tells the stop is busy",
        [("edge", 0, 1, 0, "feet", GUN, .6), ("deck", .55, 1, 0, "feet", GUN, .4), ("face", 0, 1, 0, "scuff", GUN, .55), ("bed_s", 0, 1, 0, "dust", SLATE, .25)]),
 "04": ("Amber Strike", "amber-tinted stator wear (heat-tinted by the drive) + kerb face scuffs; ties to the Aegis amber accent",
        [("flange", 0, 1, 0, "streak", AMB, .4), ("flange", 0, 1, 1, "dust", GUN, .25), ("face", 0, 1, 0, "scuff", SLATE, .5), ("edge", 0, 1, 0, "feet", GUN, .4)]),
 "05": ("Full Wear Set", "all four beats layered: bed dust, stator burnish over dust, edge + deck foot scuffs, kerb face scuffs; densest story",
        [("bed_s", 0, 1, 0, "dust", SLATE, .4), ("bed_n", 0, 1, 0, "dust", SLATE, .4), ("flange", 0, 1, 0, "dust", GUN, .3), ("flange", 0, 1, 1, "streak", TI, .5),
         ("edge", 0, 1, 0, "feet", GUN, .5), ("deck", .6, 1, 0, "feet", GUN, .3), ("face", 0, 1, 0, "scuff", GUN, .5)]),
}

def build(c):
    sc = {"guideway": trimesh.Scene(), "kerb": trimesh.Scene()}
    for k, (sf, f0, f1, lay, kind, rgb, a) in enumerate(CANDS[c][2]):
        sc[HOSTOF[sf]].add_geometry(quad(sf, f0, f1, lay, tex(kind, rgb, k + 7*int(c), a)), geom_name=f"{sf}_{kind}_{k}_L{lay}")
    return sc

def check(sc):
    r = {"tris": 0, "min_clear_m": 1., "inside_hits": 0, "coplanar_pairs": 0, "uv_blend": True, "sprocket_overlap": 0, "gap_ok": True}
    for h, s in sc.items():
        if not s.geometry: continue
        host = trimesh.load(HOST[h]); hall = trimesh.util.concatenate(list(host.geometry.values()))
        hp = [p for g in host.geometry.values() for p in g.split(only_watertight=False) if p.is_watertight]
        gs = list(s.geometry.items()); wx, wz, yaw = WORLD[h]
        for n, g in gs:
            r["tris"] += len(g.faces); r["uv_blend"] &= g.visual.uv is not None and g.visual.material.alphaMode == "BLEND"
            P = np.vstack([g.vertices, trimesh.sample.sample_surface(g, 500, seed=2)[0]])
            r["min_clear_m"] = min(r["min_clear_m"], float(trimesh.proximity.closest_point(hall, P)[1].min()))
            r["inside_hits"] += sum(int(p.contains(P).sum()) for p in hp)
            ax, pl = SURF[n.split("_")[0] if not n.startswith("bed") else "_".join(n.split("_")[:2])][:2]
            lay = int(n[-1]); val = g.vertices[0, 1 if ax == "y" else 2]; r["gap_ok"] &= abs(val - (pl + OFF + lay*DY)) < 1e-6
            s_ = -1 if yaw == 180 else 1; X = wx + s_*g.vertices[:, 0]; Z = wz + s_*g.vertices[:, 2]
            if X.max() > SPROCKET[0] and X.min() < SPROCKET[1] and Z.max() > SPROCKET[2] - .5 and Z.min() < SPROCKET[3] + .5: r["sprocket_overlap"] += 1
        for i, (na, a) in enumerate(gs):
            for nb, b in gs[i+1:]:
                lo, hi = np.maximum(a.bounds[0], b.bounds[0]), np.minimum(a.bounds[1], b.bounds[1]); d = hi - lo
                if (np.sort(d)[1:] > 0).all() and np.sort(np.abs(d))[0] <= .001: r["coplanar_pairs"] += 1
    r["min_clear_m"] = round(r["min_clear_m"], 4)
    r["pass"] = (r["tris"] < 6000 and r["min_clear_m"] >= .002 and r["inside_hits"] == 0 and r["coplanar_pairs"] == 0
                 and r["uv_blend"] and r["sprocket_overlap"] == 0 and r["gap_ok"])
    return r

if __name__ == "__main__":
    rep = {}
    for c in CANDS:
        sc = build(c)
        for h, s in sc.items(): s.export(f"{OUT}/ext_track_scuff_{h}_{c}.glb")
        rep[c] = check(sc); print(c, rep[c])
    json.dump(rep, open(f"{OUT}/ext_track_scuff_decal_report.json", "w"), indent=1, default=lambda o: o.item())
    # contact sheet: per candidate, top view of a 2 m guideway slice (left), kerb deck top (mid), kerb front face (right)
    S = 220; cells = []
    BASE = {"bed_s": (60, 66, 76), "bed_n": (60, 66, 76), "flange": (110, 116, 124), "deck": (70, 76, 86), "edge": (70, 76, 86), "face": (40, 46, 56)}
    for c in CANDS:
        im = Image.new("RGBA", (int(7.2*S), int(3.6*S)), (14, 16, 20, 255)); d = ImageDraw.Draw(im)
        orig = {"guideway": (.2*S, 1.8*S), "kerb": (3.0*S, 1.8*S)}
        def R(sf, f0=0, f1=1):
            ax, _, (u0, u1), (v0, v1) = SURF[sf]; u0, u1 = max(u0, -1), min(u1, 1); a, b = v0+(v1-v0)*f0, v0+(v1-v0)*f1
            if sf == "face": ox, oy = 5.4*S, 2.4*S; return (ox+(u0+1)*S*.8, oy-b*S*4, ox+(u1+1)*S*.8, oy-a*S*4)
            ox, oy = orig[HOSTOF[sf]]; return (ox+(u0+1)*S, oy-b*S, ox+(u1+1)*S, oy-a*S)
        for sf in SURF: d.rectangle(R(sf), fill=BASE[sf])
        for k, (sf, f0, f1, lay, kind, rgb, a) in enumerate(CANDS[c][2]):
            x0, y0, x1, y1 = [int(v) for v in R(sf, f0, f1)]; t = tex(kind, rgb, k + 7*int(c), a)
            im.alpha_composite(t.crop((0, 0, t.width*2//10 if sf not in ("deck", "edge", "face") else t.width, t.height)).resize((x1-x0, y1-y0)), (x0, y0))
        d.text((10, 10), f"{c} {CANDS[c][0]}  {rep[c]['tris']} tris  {'PASS' if rep[c]['pass'] else 'FAIL'}   [guideway 2 m slice | kerb deck | kerb face x4 height]", fill=AMB)
        cells.append(im.convert("RGB"))
    sheet = Image.new("RGB", (cells[0].width, sum(i.height for i in cells))); y = 0
    for i in cells: sheet.paste(i, (0, y)); y += i.height
    sheet.save(f"{OUT}/ext_track_scuff_decal_contact_sheet.png")
