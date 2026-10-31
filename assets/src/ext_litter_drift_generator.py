"""Rook: #50 litter / spill drift set (Coriolis tell: drifts ANTISPINWARD = -Z along the Spin St walkways).
Candidates -> design/assets/ext_litter_drift/ext_litter_drift_01..05.glb. Patch footprint ~1.2 x 3.0 m (X x Z).
Pivot bottom-centre (0,0,0); +Z = spinward (heads of streaks), tails trail to -Z. Solid litter rests on y 0 (place at paving
y 0.05); spill/streak decal quads at local y 0.003 (+1.5 mm per extra layer). Litter never overlaps decals or other litter."""
import sys, json, numpy as np, trimesh
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, "assets/src"); import ext_clip_check as cc
OUT = "design/assets/ext_litter_drift"; OFF, DY = .003, .0015
GUN, SLATE, TI, AMB, PEARL, CY = (26,30,36), (40,46,56), (150,156,164), (255,149,0), (226,228,222), (0,200,230)

def solid_tex(rgb):
    im = Image.new("RGB", (32, 32), rgb); ImageDraw.Draw(im).rectangle([0, 26, 31, 31], fill=tuple(int(v*.7) for v in rgb)); return im
def uvmap(m, rgb, blend=False, im=None):
    v = m.vertices; uv = np.c_[(v[:, 0]-v[:, 0].min())/max(np.ptp(v[:, 0]), 1e-6), (v[:, 2]-v[:, 2].min()+v[:, 1])/max(np.ptp(v[:, 2])+np.ptp(v[:, 1]), 1e-6)]
    mat = trimesh.visual.material.PBRMaterial(baseColorTexture=im or solid_tex(rgb), alphaMode="BLEND" if blend else "OPAQUE", roughnessFactor=.7, metallicFactor=0)
    m.visual = trimesh.visual.TextureVisuals(uv=uv, material=mat); return m

def piece(kind, rng):
    if kind == "can":    # lying can, r .033 l .12
        m = trimesh.creation.cylinder(.033, .12, sections=12); m.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2, [0, 1, 0])); col = TI if rng.random() < .5 else CY
    elif kind == "cup":  # lying tapered cup
        m = trimesh.creation.cone(.045, .11, sections=12); m.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2, [0, 1, 0])); col = PEARL
    elif kind == "wrap": # crumpled wrapper (subdivided jittered box)
        m = trimesh.creation.box([.09, .025, .07]).subdivide(); m.vertices += rng.normal(0, .004, m.vertices.shape); col = AMB
    elif kind == "flat": # flattened packet
        m = trimesh.creation.box([.14, .006, .09]); col = SLATE if rng.random() < .5 else AMB
    else:                # sealed ration pouch
        m = trimesh.creation.box([.10, .018, .14]); col = GUN
    m.apply_transform(trimesh.transformations.rotation_matrix(rng.uniform(-.5, .5) + (np.pi/2 if kind in "can cup" else 0), [0, 1, 0]))
    m.apply_translation([0, -m.bounds[0][1], 0]); return m, col

def streak(L, w, rgb, a, seed, drops=False):
    rng = np.random.default_rng(seed); H, Wp = 512, 128; arr = np.zeros((H, Wp, 4), np.uint8); arr[..., :3] = rgb
    y = np.linspace(1, 0, H)[:, None]  # top of texture (=+Z head) opaque, fading to -Z tail
    x = np.abs(np.linspace(-1, 1, Wp))[None] / (0.35 + .65*y)
    al = np.clip(1-x, 0, 1) * (.25 + .75*y) * a
    if drops: al *= (1 + .6*np.sin(np.arange(H)[:, None]/9 + rng.random()*6)) / 1.6
    arr[..., 3] = (np.clip(al, 0, 1)*255).astype(np.uint8); return Image.fromarray(arr).filter(ImageFilter.GaussianBlur(2))

def dquad(cx, cz, w, L, y, im):
    V = np.array([[cx-w/2, y, cz-L/2], [cx+w/2, y, cz-L/2], [cx+w/2, y, cz+L/2], [cx-w/2, y, cz+L/2]])
    m = trimesh.Trimesh(V, [[0, 2, 1], [0, 3, 2]], process=False)
    mat = trimesh.visual.material.PBRMaterial(baseColorTexture=im, alphaMode="BLEND", roughnessFactor=.4, metallicFactor=0)
    m.visual = trimesh.visual.TextureVisuals(uv=np.array([[0, 0], [1, 0], [1, 1], [0, 1]]), material=mat); return m

# (name, why, decals [(cx, cz, w, L, rgb, alpha, drops, layer)], litter kinds, n_litter, seed)
CANDS = {
 "01": ("Gutter Drift", "litter only, bunched against the -Z end like it piled up downstream; clearest Coriolis read with zero decals",
        [], ["can", "cup", "wrap", "flat", "pouch"], 14, 1),
 "02": ("Spill Comet", "one big dark spill streak with a cup at its +Z head and the tail smearing antispinward; single strong tell",
        [(0, -0.1, .55, 2.4, GUN, .65, False, 0)], ["cup", "can", "wrap"], 5, 2),
 "03": ("Drip Trail", "dotted amber drip line trailing -Z from a dropped can + scattered wrappers; reads at walking distance",
        [(-.25, -.1, .18, 2.5, AMB, .55, True, 0), (.35, -.2, .3, 1.6, SLATE, .5, False, 1)], ["can", "wrap", "flat"], 7, 3),
 "04": ("Layered Smear", "old faded slate smear under a fresh gunmetal streak (1.5 mm above): shows repeated spills, all bending -Z",
        [(0, -.1, .8, 2.6, SLATE, .4, False, 0), (.1, .2, .35, 1.8, GUN, .6, False, 1)], ["cup", "pouch", "wrap", "flat"], 6, 4),
 "05": ("Cyan Coolant", "civic-cyan coolant/drink spill streak + titanium cans: Aegis-coloured mess that still says 'drift'",
        [(.15, -.1, .4, 2.4, CY, .45, True, 0)], ["can", "can", "cup", "flat"], 6, 5),
}

def build(c):
    _, _, decs, kinds, n, seed = CANDS[c]; rng = np.random.default_rng(seed)
    dq = [dquad(cx, cz, w, L, OFF + lay*DY, streak(L, w, rgb, a, seed+k, dr)) for k, (cx, cz, w, L, rgb, a, dr, lay) in enumerate(decs)]
    rects = [(cx-w/2-.01, cx+w/2+.01, cz-L/2-.01, cz+L/2+.01) for cx, cz, w, L, *_ in decs]
    heads = [(cx, cz+L/2+.12) for cx, cz, w, L, *_ in decs]  # litter source at each streak's +Z head
    placed, tries, k = [], 0, 0
    while len(placed) < n and tries < 5000:
        tries += 1; m, col = piece(kinds[len(placed) % len(kinds)], rng)
        if len(placed) < len(heads) and tries < 200*(len(placed)+1): x, z = heads[len(placed)][0] + rng.normal(0, .03), heads[len(placed)][1] + rng.normal(0, .02)
        else:  # density biased to -Z (drift end)
            z = -1.45 + 2.9*rng.random()**2.2; x = rng.uniform(-.55, .55)
        mm = m.copy(); mm.apply_translation([x, 0, z]); b = mm.bounds
        if b[0][0] < -.6 or b[1][0] > .6 or b[0][2] < -1.5 or b[1][2] > 1.5: continue
        if any(b[0][0] < r[1] and b[1][0] > r[0] and b[0][2] < r[3] and b[1][2] > r[2] for r in rects): continue
        if any(b[0][0] < p.bounds[1][0]+.02 and b[1][0] > p.bounds[0][0]-.02 and b[0][2] < p.bounds[1][2]+.02 and b[1][2] > p.bounds[0][2]-.02 for p, _ in placed): continue
        placed.append((mm, col))
    s = trimesh.Scene(); P = {}
    for i, (m, col) in enumerate(placed): s.add_geometry(uvmap(m, col), geom_name=f"Litter_{i}"); P[f"Litter_{i}"] = (None, m)
    for i, q in enumerate(dq): s.add_geometry(q, geom_name=f"Decal_{i}")
    # recentre XZ so the AABB is bottom-centre
    V = np.vstack([g.vertices for g in s.geometry.values()]); sh = -np.r_[(V.min(0)[0]+V.max(0)[0])/2, 0, (V.min(0)[2]+V.max(0)[2])/2]
    for g in s.geometry.values(): g.apply_translation(sh)
    return s, P, dq

def check(c, s, P, dq):
    r = {}
    for seed in (0, 1, 2):
        cr = cc.check(P, seed=seed); r.setdefault("clip_runs", []).append(dict(overlap=cr["overlap"], coplanar=cr["coplanar"], open=cr["open"]))
    lit = [m for _, m in P.values()]
    r["litter_n"] = len(lit); r["tris"] = int(sum(len(g.faces) for g in s.geometry.values()))
    r["floor_contact"] = [round(float(m.bounds[0][1]), 4) for m in lit]
    r["floor_ok"] = all(abs(v) <= .005 for v in r["floor_contact"])
    r["watertight"] = all(m.is_watertight for m in lit)
    inter = 0
    for i, a in enumerate(lit):
        for b in lit[i+1:]:
            if (a.bounds[0] < b.bounds[1]).all() and (b.bounds[0] < a.bounds[1]).all(): inter += 1
    r["litter_intersections"] = inter
    dec_hits = sum(int(m.contains(q.vertices).sum()) + int(((q.bounds[0][[0, 2]] < m.bounds[1][[0, 2]]) & (m.bounds[0][[0, 2]] < q.bounds[1][[0, 2]])).all()) for q in dq for m in lit)
    r["decal_litter_hits"] = dec_hits
    ys = sorted(q.vertices[0, 1] for q in dq); r["decal_offsets"] = [round(float(y), 4) for y in ys]
    r["decal_offset_ok"] = all(.002 <= y <= .0065 for y in ys) and all(np.diff(ys) > .001) if ys else True
    V = np.vstack([g.vertices for g in s.geometry.values()]); lo, hi = V.min(0), V.max(0)
    r["pivot"] = dict(min_y=round(float(lo[1]), 4), cx=round(float((lo[0]+hi[0])/2), 4), cz=round(float((lo[2]+hi[2])/2), 4)); r["size"] = (hi-lo).round(3).tolist()
    r["uv_blend"] = all(g.visual.uv is not None for g in s.geometry.values()) and all(q.visual.material.alphaMode == "BLEND" for q in dq)
    clip_ok = all(all(ok for *_, ok in x["overlap"]) and not x["coplanar"] and not x["open"] for x in r["clip_runs"])
    r["pass"] = (clip_ok and r["floor_ok"] and r["watertight"] and inter == 0 and dec_hits == 0 and r["decal_offset_ok"] and r["tris"] < 6000
                 and abs(lo[1]) <= .005 and abs(r["pivot"]["cx"]) <= .005 and abs(r["pivot"]["cz"]) <= .005 and r["uv_blend"])
    return r

if __name__ == "__main__":
    rep = {}
    for c in CANDS:
        s, P, dq = build(c); s.export(f"{OUT}/ext_litter_drift_{c}.glb"); rep[c] = check(c, s, P, dq)
        print(c, {k: v for k, v in rep[c].items() if k != "clip_runs"}, "clip:", [(len(x["overlap"]), len(x["coplanar"]), len(x["open"])) for x in rep[c]["clip_runs"]])
    json.dump(rep, open(f"{OUT}/ext_litter_drift_report.json", "w"), indent=1, default=str)
    # contact sheet: top-down ortho (+Z up the page, drift arrow down)
    S = 300; cells = []
    for c in CANDS:
        s, _, _ = build(c); im = Image.new("RGBA", (int(1.4*S), int(3.3*S)), (58, 64, 74, 255)); d = ImageDraw.Draw(im)
        px = lambda x, z: ((x+.7)*S, (1.65-z)*S)
        for n, g in sorted(s.geometry.items(), key=lambda kv: kv[0].startswith("Litter")):
            if n.startswith("Decal"):
                v = g.vertices; t = g.visual.material.baseColorTexture.convert("RGBA")
                w, h = int(np.ptp(v[:, 0])*S), int(np.ptp(v[:, 2])*S); x0, y0 = px(v[:, 0].min(), v[:, 2].max())
                im.alpha_composite(t.resize((max(w, 1), max(h, 1))), (int(x0), int(y0))); continue
            col = g.visual.material.baseColorTexture.getpixel((5, 5))
            for t, fn in sorted(zip(g.triangles, g.face_normals), key=lambda q: q[0][:, 1].mean()):
                if fn[1] > 0: d.polygon([px(p[0], p[2]) for p in t], fill=tuple(int(v*(.6+.4*fn[1])) for v in col[:3]))
        d.line([S*1.3, S*.3, S*1.3, S*1.2], fill=AMB, width=3); d.polygon([(S*1.27, S*1.2), (S*1.33, S*1.2), (S*1.3, S*1.28)], fill=AMB)
        cell = Image.new("RGB", (im.width+10, im.height+40), (12, 14, 18)); cell.paste(im.convert("RGB"), (5, 5))
        ImageDraw.Draw(cell).text((8, im.height+14), f"{c} {CANDS[c][0]} {rep[c]['tris']} tris {'PASS' if rep[c]['pass'] else 'FAIL'}  (arrow = antispinward -Z)", fill=AMB)
        cells.append(cell)
    sheet = Image.new("RGB", (sum(c.width for c in cells), cells[0].height)); x = 0
    for c in cells: sheet.paste(c, (x, 0)); x += c.width
    sheet.save(f"{OUT}/ext_litter_drift_contact_sheet.png")
