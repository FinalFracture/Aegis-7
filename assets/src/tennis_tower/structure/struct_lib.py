"""Rook: Tennis Tower structural blockout library (spec design/strip5_tennis_tower_v1.md Rev 2.9).
Reusable generators in BUILDING coordinates (X axial, Z across, Y up; F1 = 0, F2 = +6.1, F3 = +12.2, origin SW corner).
Every element is an axis box (12 tris). Chunks are exported through the modlib pipeline (recenter -> bottom-centre pivot,
+Z front, export_final + finish_glb, clip check A1-A5, validate_models) and their WORLD offset is written to
godot/assets/models/tt_struct_layout.json so the level can drop them back in place.
Glass rule (§3.12.6): only the F3 Glass Box envelope (corner closures) keeps the BLEND 'Glass' material; guards and nets
use TT_GlassScissor / TT_NetScissor = alphaMode MASK with an embedded dither / mesh-grid alpha texture."""
import os, sys, io, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
from modlib import *                       # noqa: F401,F403  (box, Part, export_final, finish_glb, cc, vm, FMAT, _m ...)
import modlib as ML
GODOT_MODELS = os.path.join(ROOT, "godot/assets/models")
LAYOUT = os.path.join(GODOT_MODELS, "tt_struct_layout.json")
F1, F2, F3 = 0.0, 6.1, 12.2
SLAB = {F1: .40, F2: .40, F3: .50}          # slab depth below each floor top
# ---- scissor materials (alpha-scissor glass guard / ball net) ----
ML._m("tt_scr", "TT_GlassScissor", (.72, .86, .93), 0, .08)
ML._m("tt_net", "TT_NetScissor", (.10, .12, .15), .3, .7)
ML._m("tt_pad", "TT_PadTeal", (.10, .42, .44), 0, .9)
ML._m("tt_conc", "TT_StructConcrete", (.55, .57, .60), 0, .85)
SCR, NET, PAD, CON = "tt_scr", "tt_net", "tt_pad", "tt_conc"
ML.TEXMAP.setdefault("TT_StructConcrete", "facade_titanium_gunmetal_hull.png")

def _tex_png(kind):
    from PIL import Image
    n = 64; a = np.zeros((n, n), np.uint8)
    if kind == "dither":                    # 30% opaque ordered dither + opaque 4 px frit edge band
        bay = np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]) / 16.0
        a = ((np.tile(bay, (n // 4, n // 4))) < .30).astype(np.uint8) * 255; a[:4, :] = a[-4:, :] = a[:, :4] = a[:, -4:] = 255
        rgb = (184, 219, 237)
    else:                                   # ball net: 2 px cords on a 16 px mesh
        a[(np.arange(n) % 16) < 2, :] = 255; a[:, (np.arange(n) % 16) < 2] = 255; rgb = (26, 30, 38)
    im = Image.new("RGBA", (n, n), rgb + (0,)); im.putalpha(Image.fromarray(a)); b = io.BytesIO(); im.save(b, "PNG"); return b.getvalue()

def finish_scissor(path):
    """MASK + cutoff 0.5 + embedded alpha texture for TT_GlassScissor / TT_NetScissor."""
    import pygltflib as pg
    g = pg.GLTF2().load(path); blob = bytearray(g.binary_blob()); hit = False
    for m in g.materials:
        kind = {"TT_GlassScissor": "dither", "TT_NetScissor": "net"}.get(m.name)
        if not kind: continue
        hit = True; data = _tex_png(kind)
        while len(blob) % 4: blob.append(0)
        if not g.samplers: g.samplers.append(pg.Sampler(magFilter=9728, minFilter=9728, wrapS=10497, wrapT=10497))
        g.bufferViews.append(pg.BufferView(buffer=0, byteOffset=len(blob), byteLength=len(data))); blob.extend(data)
        g.images.append(pg.Image(bufferView=len(g.bufferViews) - 1, mimeType="image/png")); g.textures.append(pg.Texture(source=len(g.images) - 1, sampler=0))
        m.alphaMode = "MASK"; m.alphaCutoff = .5; m.doubleSided = True
        m.pbrMetallicRoughness.baseColorTexture = pg.TextureInfo(index=len(g.textures) - 1)
    if hit:
        while len(blob) % 4: blob.append(0)
        g.buffers[0].byteLength = len(blob); g.set_binary_blob(bytes(blob)); g.save_binary(path)

# ---------------- plan geometry helpers ----------------
def rect_minus(r, holes):
    """r=(x0,x1,z0,z1) minus hole rects -> list of disjoint rects (grid split, then row-merge, then column-merge)."""
    x0, x1, z0, z1 = r; hs = [(max(a, x0), min(b, x1), max(c, z0), min(d, z1)) for a, b, c, d in holes]
    hs = [h for h in hs if h[0] < h[1] - 1e-6 and h[2] < h[3] - 1e-6]
    xs = sorted({x0, x1, *[v for h in hs for v in h[:2]]}); zs = sorted({z0, z1, *[v for h in hs for v in h[2:]]})
    cell = lambda i, j: not any(h[0] <= xs[i] + 1e-6 and xs[i + 1] <= h[1] + 1e-6 and h[2] <= zs[j] + 1e-6 and zs[j + 1] <= h[3] + 1e-6 for h in hs)
    rows = []
    for j in range(len(zs) - 1):           # merge along X per row
        i = 0
        while i < len(xs) - 1:
            if not cell(i, j): i += 1; continue
            k = i
            while k + 1 < len(xs) - 1 and cell(k + 1, j): k += 1
            rows.append([xs[i], xs[k + 1], zs[j], zs[j + 1]]); i = k + 1
    out = []                                # merge equal-X spans along Z
    for r_ in sorted(rows, key=lambda q: (q[0], q[1], q[2])):
        if out and abs(out[-1][0] - r_[0]) < 1e-6 and abs(out[-1][1] - r_[1]) < 1e-6 and abs(out[-1][3] - r_[2]) < 1e-6: out[-1][3] = r_[3]
        else: out.append(r_)
    return [tuple(o) for o in out]

def slab(r, holes, ytop, depth):
    return [box(a, b, ytop - depth, ytop, c, d) for a, b, c, d in rect_minus(r, holes)]

def wall(a, b, y0, y1, t=.3, axis="x", line=0.0, openings=(), side=0, piers=()):
    """straight wall along X (axis='x', at Z=line) or Z (axis='z', at X=line) from a..b.
    openings=[(s0,s1,head)] full-width door/window cuts (sill via (s0,s1,head,sill)); piers=[(s0,s1)] full-height gaps (columns).
    side: 0 centred on line, +1 entirely on the + side, -1 on the - side."""
    o0, o1 = (line - t/2, line + t/2) if side == 0 else ((line, line + t) if side > 0 else (line - t, line))
    cuts = sorted([(s0, s1, y0 + .0, y1) for s0, s1 in piers] + [(op[0], op[1], op[3] if len(op) > 3 else y0, op[2]) for op in openings])
    segs = []; s = a
    for c0, c1, cy0, cy1 in cuts:
        if c1 <= a or c0 >= b: continue
        if c0 > s: segs.append((s, c0, y0, y1))
        if cy0 > y0 + 1e-6: segs.append((max(c0, a), min(c1, b), y0, cy0))     # sill
        if cy1 < y1 - 1e-6: segs.append((max(c0, a), min(c1, b), cy1, y1))     # lintel
        s = max(s, c1)
    if s < b: segs.append((s, b, y0, y1))
    out = []
    for s0, s1, u0, u1 in segs:
        if s1 - s0 < .02: continue
        out.append(box(s0, s1, u0, u1, o0, o1) if axis == "x" else box(o0, o1, u0, u1, s0, s1))
    return out

def column(x, z, y0, y1, w=.6, d=None):
    d = d or w; return box(x - w/2, x + w/2, y0, y1, z - d/2, z + d/2)

def pads(x, z, y0, h, w, t=.06):
    """4 impact pads around a w x w column (separate plates embedded E, so no enclosing overlap)."""
    h2 = w/2
    return [box(x - h2 - t + E, x + h2 + t - E, y0, y0 + h, z + h2 - E, z + h2 + t), box(x - h2 - t + E, x + h2 + t - E, y0, y0 + h, z - h2 - t, z - h2 + E),
            box(x + h2 - E, x + h2 + t, y0, y0 + h, z - h2 + E + .001, z + h2 - E - .001), box(x - h2 - t, x - h2 + E, y0, y0 + h, z - h2 + E + .001, z + h2 - E - .001)]

def steps(x0, x1, z0, rise, n, run=.28, y0=0.0, direction=1, axis="z"):
    """solid flight: n risers from y0, climbing toward +axis (direction=1) or -axis from z0 (or x0 when axis='x')."""
    h = rise / n; out = []
    for i in range(n):
        a, b = z0 + direction*run*i, z0 + direction*run*(i + 1); a, b = min(a, b) - (E if i else 0), max(a, b) + (E if i else 0)
        if direction < 0: a, b = z0 - run*(i + 1), z0 - run*i + (E if i else 0)
        out.append(box(x0, x1, y0, y0 + h*(i + 1), a, b) if axis == "z" else box(a, b, y0, y0 + h*(i + 1), x0, x1))
    return out

# ---------------- chunk export ----------------
def tri_count(meshes): return int(sum(len(m.faces) for m in meshes))

def export_chunk(name, parts, colliders=None, report=None, tri_max=TRI_MAX, layout=None, note=""):
    """parts: [(PartName, matkey, [meshes])]; colliders: [(Name-colonly, [meshes])] (go in as visual-material 'tt_slate' nodes,
    filtered by name). Recentres to bottom-centre, exports, finishes BLEND/scissor, checks, records world offset."""
    p = Part(name)
    for pn, mk, ms in parts:
        ms = [m for m in ms if m is not None]
        if ms: p.add(pn, mk, *ms)
    for cn, ms in (colliders or []):
        if ms: p.add(cn, SL, *ms)
    V = np.vstack([m.vertices for k, (_, m) in p.P.items() if "colonly" not in k]); lo, hi = V.min(0), V.max(0)
    world = [round(float((lo[0] + hi[0]) / 2), 4), round(float(lo[1]), 4), round(float((lo[2] + hi[2]) / 2), 4)]
    p = recenter(p)
    vis = {k: v for k, v in p.P.items() if "colonly" not in k}
    chk = cc.check(vis, n_samp=60)
    gp = os.path.join(GODOT_MODELS, f"{name}.glb"); tris, geo = export_final(p.P, [gp]); finish_glb(gp); finish_scissor(gp)
    try: ok_v = vm.validate_file(gp, check_tri_range=(1, tri_max), require_textures=False, require_blend_glass=any(mk == GL for mk, _ in p.P.values()))
    except AssertionError as e: print("VALIDATE FAIL", e); ok_v = False
    r = dict(asset=name, tris=int(tris), world_offset=world, size=chk["size"], clip_pass=chk["pass"], worst_overlap=chk["worst_overlap"],
             bad=[o for o in chk["overlap"] if not o[3]][:5], coplanar=chk["coplanar"][:5], open=chk["open"][:5], pivot=chk["pivot"],
             names_ok=name_rule(p), validate=bool(ok_v), note=note)
    r["passed"] = bool(ok_v and chk["pass"] and tris <= tri_max and r["names_ok"])
    print(json.dumps({k: r[k] for k in ("asset", "tris", "passed", "worst_overlap", "world_offset")}))
    if not r["passed"]: print("   detail", json.dumps(r, default=str)[:800])
    if report is not None: report.append(r)
    if layout is not None: layout[name] = dict(world_offset=world, note=note)
    return r, geo

def pack(name, items, report, layout, budget=5600, collide=True, note="", key=lambda m: m.bounds.mean(0)[0]):
    """auto-chunk [(PartName, mat, mesh)] into <= budget tris (incl. colliders) along X -> name_a, name_b, ..."""
    items = sorted(items, key=lambda it: key(it[2])); chunks = [[]]; t = 0; per = 2 if collide else 1
    for it in items:
        n = len(it[2].faces) * (per if it[1] not in (CY, AM, PAD, NET, SCR, GL, LF, LF2) else 1)
        if t + n > budget and chunks[-1]: chunks.append([]); t = 0
        chunks[-1].append(it); t += n
    out = []
    for i, ch in enumerate(chunks):
        nm = name if len(chunks) == 1 else f"{name}_{chr(97 + i)}"; groups = {}
        for pn, mk, m in ch: groups.setdefault((pn, mk), []).append(m)
        col = [(f"Struct-colonly", [m for (pn, mk), ms in groups.items() if mk in (SL, G, ST, CON, SSL, WH) for m in ms] and [m.copy() for (pn, mk), ms in groups.items() if mk in (SL, G, ST, CON, SSL, WH) for m in ms])] if collide else []
        out.append(export_chunk(nm, [(pn, mk, ms) for (pn, mk), ms in groups.items()], col, report, layout=layout, note=note))
    return out
