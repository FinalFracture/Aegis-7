"""temp-Courts: F3-BB basketball kit — court floor+decals, hoop, scorer table, scoreboard.
Hall X 39.5..103.5, Z 24.5..54.5, y=12.2. Two 28x15 courts end-to-end along X, 2 m end runoff, 4 m mid gap.
No wood, no planters, no BLEND. Scissor only on hoop backboard/net. Y-up, +Z front, bottom-centre pivot.
Run: python3 basketball.py [--render]  (from this folder or tennis_tower/)"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
TT = os.path.abspath(os.path.join(HERE, "..", ".."))
if os.path.basename(os.path.normpath(TT)) != "tennis_tower":
    TT = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, TT)
from modlib import *
import pygltflib as pg

def _fallback_scissor():
    global SCR, NET, finish_scissor
    import modlib as _ML
    _ML._m("tt_scr", "TT_GlassScissor", (.72, .86, .93), 0, .08, a=1.0)
    _ML._m("tt_net", "TT_NetScissor", (.10, .12, .15), .3, .7, a=1.0)
    SCR, NET = "tt_scr", "tt_net"
    def _tex_png(kind):
        from PIL import Image
        n = 64; a = np.zeros((n, n), np.uint8)
        if kind == "dither":
            bay = np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]) / 16.0
            a = ((np.tile(bay, (n // 4, n // 4))) < .30).astype(np.uint8) * 255
            a[:4, :] = a[-4:, :] = a[:, :4] = a[:, -4:] = 255; rgb = (184, 219, 237)
        else:
            a[(np.arange(n) % 16) < 2, :] = 255; a[:, (np.arange(n) % 16) < 2] = 255; rgb = (26, 30, 38)
        im = Image.new("RGBA", (n, n), rgb + (0,)); im.putalpha(Image.fromarray(a))
        b = io.BytesIO(); im.save(b, "PNG"); return b.getvalue()
    def finish_scissor(path):
        g = pg.GLTF2().load(path); blob = bytearray(g.binary_blob()); hit = False
        for m in g.materials:
            kind = {"TT_GlassScissor": "dither", "TT_NetScissor": "net"}.get(m.name)
            if not kind: continue
            hit = True; data = _tex_png(kind)
            while len(blob) % 4: blob.append(0)
            if not g.samplers: g.samplers.append(pg.Sampler(magFilter=9728, minFilter=9728, wrapS=10497, wrapT=10497))
            g.bufferViews.append(pg.BufferView(buffer=0, byteOffset=len(blob), byteLength=len(data))); blob.extend(data)
            g.images.append(pg.Image(bufferView=len(g.bufferViews) - 1, mimeType="image/png"))
            g.textures.append(pg.Texture(source=len(g.images) - 1, sampler=0))
            m.alphaMode = "MASK"; m.alphaCutoff = .5; m.doubleSided = True
            bc = m.pbrMetallicRoughness.baseColorFactor
            m.pbrMetallicRoughness.baseColorFactor = [*(bc or [.72, .86, .93])[:3], 1.0]
            m.pbrMetallicRoughness.baseColorTexture = pg.TextureInfo(index=len(g.textures) - 1)
        if hit:
            while len(blob) % 4: blob.append(0)
            g.buffers[0].byteLength = len(blob); g.set_binary_blob(bytes(blob)); g.save_binary(path)
try:
    sys.path.insert(0, os.path.join(TT, "structure"))
    from struct_lib import SCR, NET, finish_scissor  # noqa: E402
except Exception:
    _fallback_scissor()

GODOT = os.path.join(ROOT, "godot/assets/models")
RENDER_DIR = "/workspace/renders/tennis_tower/rooms/temp-Courts"
GAP, TH, LINE_Y, LW = .008, .04, .043, .05
CL, CW = 28.0, 15.0  # FIBA

def _line(x0, x1, z0, z1, y0=LINE_Y, y1=LINE_Y + .003, t=None):
    if t is None: t = LW
    # axis-aligned paint strip; caller passes already-inset coords
    return box(x0, x1, y0, y1, z0, z1)

def _arc_boxes(cx, cz, r, y0, y1, a0, a1, n=12, w=.05):
    an = np.linspace(a0, a1, n + 1); out = []
    for a, b in zip(an[:-1], an[1:]):
        mx, mz = np.cos((a + b) / 2), np.sin((a + b) / 2)
        px, pz = cx + r * mx, cz + r * mz
        # short tangent box
        t = (b - a) * r * .55
        # local along tangent (-sin, cos)
        tx, tz = -mz, mx
        # corners
        hx, hz, hw = tx * t, tz * t, w / 2
        # use a thin box aligned by placing an AABB approx (good enough for decals)
        xs = [px - hx - mx * hw, px - hx + mx * hw, px + hx - mx * hw, px + hx + mx * hw]
        zs = [pz - hz - mz * hw, pz - hz + mz * hw, pz + hz - mz * hw, pz + hz + mz * hw]
        out.append(box(min(xs), max(xs), y0, y1, min(zs), max(zs)))
    return out

def court(q=None):
    """28 x 15 m painted court; +Z is a sideline outward? Front +Z = +sideline (towards +Z, length along X)."""
    p = Part(); L, W = CL, CW
    x0, x1, z0, z1 = -L / 2, L / 2, -W / 2, W / 2
    p.add("Court_Pad", SL, box(x0, x1, 0, TH, z0, z1))
    p.add("Court-colonly", SL, box(x0, x1, 0, TH, z0, z1))
    y0, y1 = TH + GAP, TH + GAP + .003
    # boundary (inset so paint sits on pad, not coplanar with edge)
    inset = .02
    lines = [
        box(x0 + inset, x1 - inset, y0, y1, z0 + inset, z0 + inset + LW),  # -Z sideline
        box(x0 + inset, x1 - inset, y0, y1, z1 - inset - LW, z1 - inset),
        box(x0 + inset, x0 + inset + LW, y0, y1, z0 + inset + LW, z1 - inset - LW),
        box(x1 - inset - LW, x1 - inset, y0, y1, z0 + inset + LW, z1 - inset - LW),
        box(-LW / 2, LW / 2, y0, y1, z0 + inset + LW, z1 - inset - LW),  # mid line
    ]
    # keys: 4.9 wide, 5.8 deep from each baseline
    kw, kd = 4.9, 5.8
    for s in (-1, 1):
        xb = x0 + inset + LW if s < 0 else x1 - inset - LW
        xk = x0 + kd if s < 0 else x1 - kd
        xa, xb2 = sorted((xb, xk))
        lines += [
            box(xa, xb2, y0, y1, -kw / 2, -kw / 2 + LW),
            box(xa, xb2, y0, y1, kw / 2 - LW, kw / 2),
            box(xk - LW / 2 if s < 0 else xk - LW / 2, xk + LW / 2, y0, y1, -kw / 2 + LW, kw / 2 - LW),
        ]
        # FT circle half, centre at 5.8 from baseline, r=1.8
        ftc = (x0 + kd) if s < 0 else (x1 - kd)
        a0, a1 = (0, np.pi) if s < 0 else (np.pi, 2 * np.pi)
        # actually free-throw circle is towards midcourt from FT line
        if s < 0: lines += _arc_boxes(ftc, 0, 1.8, y0, y1, -np.pi / 2, np.pi / 2, 10, LW)
        else: lines += _arc_boxes(ftc, 0, 1.8, y0, y1, np.pi / 2, 3 * np.pi / 2, 10, LW)
        # 3pt approx r=6.75 from hoop; hoop 1.575 in from baseline
        hx = (x0 + 1.575) if s < 0 else (x1 - 1.575)
        if s < 0: lines += _arc_boxes(hx, 0, 6.75, y0, y1, -1.05, 1.05, 12, LW)
        else: lines += _arc_boxes(hx, 0, 6.75, y0, y1, np.pi - 1.05, np.pi + 1.05, 12, LW)
    # centre circle r=1.8
    lines += _arc_boxes(0, 0, 1.8, y0, y1, 0, 2 * np.pi, 16, LW)
    p.add("Lane_Paint", WH, *lines)
    # marks sit 8 mm above paint, inset from mid/FT lines
    ym0, ym1 = y1 + GAP, y1 + GAP + .003
    p.add("Centre_Mark", CY, box(-.07, .07, ym0, ym1, .12, .26))
    p.add("Amber_Dots", AM, box(-5.5, -5.38, ym0, ym1, .20, .32),
          box(5.38, 5.5, ym0, ym1, -.32, -.20))
    # moss tuft at corners outside paint (nature, not a planter)
    p.add("Moss_Tufts", LF2,
          clump((x0 + .25, TH + .01, z0 + .25), .04, seed=2),
          clump((x1 - .25, TH + .01, z1 - .25), .04, seed=3))
    return p

def hoop(q=None):
    """Support behind baseline (local -Z); backboard/rim into court (+Z). Rim 3.05 m."""
    p = Part()
    # base + post (behind baseline)
    p.add("Base_Pad", SL, box(-.35, .35, 0, .08, -.85, -.15))
    p.add("Post", G, box(-.08, .08, .08 + GAP, 3.15, -.62, -.46))
    # arm stops 8 mm shy of the board back face at z=1.12
    p.add("Arm", G, box(-.06, .06, 2.92, 3.12, -.46 + GAP, 1.12 - GAP))
    p.add("Board_Frame", ST,
          box(-.92, .92, 2.55, 3.62, 1.12, 1.16),
          box(-.92, -.80, 2.58, 3.59, 1.16 + GAP, 1.20),
          box(.80, .92, 2.58, 3.59, 1.16 + GAP, 1.20),
          box(-.80, .80, 3.50, 3.59, 1.16 + GAP, 1.20),
          box(-.80, .80, 2.58, 2.67, 1.16 + GAP, 1.20))
    p.add("Board_Scissor", SCR, box(-.78, .78, 2.69, 3.48, 1.172, 1.180))
    # rim centre well clear of the board front (z=1.20)
    rc, rr, rw = 1.20 + .28, .225, .016
    ring = []
    n = 10
    for i in range(n):
        a = 2 * np.pi * i / n; b = 2 * np.pi * (i + 1) / n
        x0, z0 = rr * np.cos(a), rc + rr * np.sin(a)
        x1, z1 = rr * np.cos(b), rc + rr * np.sin(b)
        ring.append(box(min(x0, x1) - rw, max(x0, x1) + rw, 3.04, 3.07, min(z0, z1) - rw, max(z0, z1) + rw))
    p.add("Rim", ST, *ring)
    nets = []
    for i in range(8):
        a = 2 * np.pi * i / 8
        x, z = rr * .85 * np.cos(a), rc + rr * .85 * np.sin(a)
        nets.append(box(x - .008, x + .008, 2.62, 3.04 - GAP, z - .008, z + .008))
    p.add("Rim_Net_Scissor", NET, *nets)
    # wrap around the post with a 10 mm air gap
    p.add("Pad_Wrap", WH, box(-.18, -.10, .10, 1.35, -.70, -.38), box(.10, .18, .10, 1.35, -.70, -.38))
    p.add("Ball_Cap", BA, node((0, 3.22, -.54), .05, 0))
    p.add("Leaf_Crest", LF, leaf_dir((0.12, 3.28, -.54), (0.3, 1, 0), .14, .05, t=.008))
    p.add("Moss_Tufts", LF2, clump((.22, .09, -.70), .035, seed=4), clump((-.22, .09, -.22), .03, seed=5))
    p.add("Post-colonly", G, box(-.35, .35, 0, .08, -.85, -.15), box(-.08, .08, .08, 3.15, -.62, -.46),
          box(-.06, .06, 2.92, 3.12, -.46, 1.11), box(-.92, .92, 2.55, 3.62, 1.12, 1.20))
    return p

def scorer(q=None):
    p = Part()
    p.add("Table_Top", SL, box(-1.8, 1.8, .78, .85, -.35, .35))
    p.add("Table_Apron", G, box(-1.78, 1.78, .62, .78 - GAP, -.33, .33))
    p.add("Legs", ST,
          box(-1.7, -1.58, 0, .62 - GAP, -.28, -.16), box(1.58, 1.7, 0, .62 - GAP, -.28, -.16),
          box(-1.7, -1.58, 0, .62 - GAP, .16, .28), box(1.58, 1.7, 0, .62 - GAP, .16, .28))
    p.add("Monitor", G, box(-.55, .55, .85 + GAP, 1.35, -.12, -.04))
    p.add("Monitor_Face", CY, box(-.50, .50, .90, 1.30, -.04 + GAP, -.02))
    p.add("Cyan_Edge", CY, box(-1.8, 1.8, .85 + GAP, .86, -.35, -.33))
    p.add("Amber_Mark", AM, box(-.08, .08, .85 + GAP, .87, .30, .34))
    p.add("Leaf_Ends", LF, leaf_dir((-1.82, .86, 0), (-.2, 1, 0), .16, .06, t=.008),
          leaf_dir((1.82, .86, 0), (.2, 1, 0), .16, .06, t=.008))
    p.add("Moss_Tufts", LF2, clump((-1.6, .02, -.30), .03, seed=6))
    p.add("Table-colonly", SL, box(-1.8, 1.8, .78, .85, -.35, .35),
          box(-1.7, -1.58, 0, .62, -.28, -.16), box(1.58, 1.7, 0, .62, -.28, -.16),
          box(-1.7, -1.58, 0, .62, .16, .28), box(1.58, 1.7, 0, .62, .16, .28))
    return p

def scoreboard(q=None):
    p = Part()
    p.add("Body", G, box(-2.0, 2.0, 0, 1.15, -.16, .16))
    p.add("Face_A", CY, box(-1.7, -.18, .20, .95, .16 + GAP, .19))
    p.add("Face_B", CY, box(.18, 1.7, .20, .95, .16 + GAP, .19))
    p.add("Face_A_Back", CY, box(-1.7, -.18, .20, .95, -.19, -.16 - GAP))
    p.add("Face_B_Back", CY, box(.18, 1.7, .20, .95, -.19, -.16 - GAP))
    p.add("Centre_Amber", AM, box(-.10, .10, .28, .88, .16 + GAP, .19))
    p.add("Hang_Eyes", ST, box(-.8, -.7, 1.15 + GAP, 1.28, -.04, .04), box(.7, .8, 1.15 + GAP, 1.28, -.04, .04))
    p.add("Ball_Caps", BA, node((-1.9, 1.20, 0), .05, 0), node((1.9, 1.20, 0), .05, 0))
    p.add("Leaf_Crest", LF, leaf_dir((0, 1.18, 0), (0, 1, 0), .22, .08, t=.008))
    p.add("Body-colonly", G, box(-2.0, 2.0, 0, 1.15, -.16, .16))
    return p

def _check_normals(path):
    tm = trimesh.load(path, force="scene")
    geoms = list(tm.geometry.values()) if hasattr(tm, "geometry") else [tm]
    bad = 0; total = 0
    for g in geoms:
        if g is None or not hasattr(g, "faces") or len(g.faces) == 0: continue
        try: n = g.face_normals
        except Exception: g.rezero(); n = g.face_normals
        lens = np.linalg.norm(n, axis=1); total += len(lens); bad += int(np.sum(lens < 1e-8))
        if getattr(g, "vertex_normals", None) is not None and len(g.vertex_normals):
            vl = np.linalg.norm(g.vertex_normals, axis=1); total += len(vl); bad += int(np.sum(vl < 1e-8))
    return dict(normals_ok=(bad == 0), normals_bad=bad, normals_checked=total)

def _check_scissor_mats(path):
    g = pg.GLTF2().load(path); bad = []; blend = []
    for m in g.materials or []:
        if m.alphaMode == "BLEND": blend.append(m.name)
        if m.name not in ("TT_GlassScissor", "TT_NetScissor"): continue
        if m.alphaMode != "MASK" or abs((m.alphaCutoff or 0) - .5) > 1e-6: bad.append(f"{m.name}:mode")
        bc = (m.pbrMetallicRoughness.baseColorFactor or [1, 1, 1, 1])
        if abs(bc[3] - 1.0) > 1e-6: bad.append(f"{m.name}:alpha")
    return dict(scissor_ok=(not bad and not blend), scissor_bad=bad, blend=blend)

def promote(name, builder, label=""):
    os.makedirs(GODOT, exist_ok=True)
    p = recenter(builder())
    vis = {k: v for k, v in p.P.items() if "colonly" not in k}
    chk = cc.check(vis, n_samp=400)
    gp = os.path.join(GODOT, f"{name}.glb")
    tris, geo = export_final(p.P, [gp]); finish_glb(gp); finish_scissor(gp)
    g = pg.GLTF2().load(gp); dirty = False
    for m in g.materials or []:
        if m.name in ("TT_GlassScissor", "TT_NetScissor"):
            bc = m.pbrMetallicRoughness.baseColorFactor or [0.72, 0.86, 0.93, 1.0]
            if abs(bc[3] - 1.0) > 1e-6:
                m.pbrMetallicRoughness.baseColorFactor = [bc[0], bc[1], bc[2], 1.0]; dirty = True
            if m.alphaMode != "MASK" or abs((m.alphaCutoff or 0) - .5) > 1e-6:
                m.alphaMode = "MASK"; m.alphaCutoff = .5; dirty = True
    if dirty: g.save_binary(gp)
    nchk = _check_normals(gp); schk = _check_scissor_mats(gp)
    try:
        ok_v = vm.validate_file(gp, check_tri_range=(1, 5999), require_textures=False, require_blend_glass=False)
    except AssertionError as e:
        print("VALIDATE FAIL", e); ok_v = False
    has_col = any("colonly" in k for k in p.P)
    V = np.vstack([m.vertices for k, (_, m) in p.P.items() if "colonly" not in k])
    lo, hi = V.min(0), V.max(0)
    glass_names = [k for k in p.P if "glass" in k.lower()]
    r = dict(asset=name, label=label, tris=int(tris), clip_pass=chk["pass"], worst_overlap=chk["worst_overlap"],
             coplanar=len(chk.get("coplanar") or []), pivot=chk["pivot"], size=chk["size"],
             names_ok=name_rule(p), validate=bool(ok_v), colliders=has_col,
             aabb={"min": lo.tolist(), "max": hi.tolist()}, glass_name_violations=glass_names, **nchk, **schk)
    r["passed"] = bool(ok_v and chk["pass"] and tris <= 5999 and name_rule(p) and nchk["normals_ok"]
                       and schk["scissor_ok"] and has_col and abs(float(chk["pivot"]["min_y"])) < 1e-6
                       and not glass_names)
    print(json.dumps(r, default=str)); return r, p, geo

def render_views(name, geo):
    os.makedirs(RENDER_DIR, exist_ok=True)
    g = {k: v for k, v in geo.items() if "colonly" not in k}
    a = np.radians(4)
    eye = np.array([[1, 0, 0], [0, np.cos(a), -np.sin(a)], [0, np.sin(a), np.cos(a)]])
    top = np.array([[1, 0, 0], [0, 0, -1], [0, 1, 0]], float)
    for tag, R in (("iso", views()[3]), ("player", eye), ("top", top)):
        path = os.path.join(RENDER_DIR, f"{name}_{tag}.png")
        if os.path.exists(path) and "tt_bb_" not in name:
            continue
        im = crop(render_view(g, R, size=640, shadow=True, glass_alpha=.35))
        plt.imsave(path, np.clip(im, 0, 1)); print("render", path)

if __name__ == "__main__":
    do_render = "--render" in sys.argv
    jobs = [
        ("tt_bb_court", court, "F3 28x15 court + decals"),
        ("tt_bb_hoop", hoop, "hoop unit, scissor board"),
        ("tt_bb_scorer_table", scorer, "scorer table"),
        ("tt_bb_scoreboard", scoreboard, "mid-hall scoreboard"),
    ]
    reps = []
    for name, fn, lab in jobs:
        r, p, geo = promote(name, fn, lab); reps.append(r)
        if do_render and r["passed"]:
            render_views(name, geo)
    summary = dict(all_passed=all(x["passed"] for x in reps),
                   tris={x["asset"]: x["tris"] for x in reps},
                   fails=[x["asset"] for x in reps if not x["passed"]])
    print(json.dumps(summary, indent=1))
    if not summary["all_passed"]:
        sys.exit(1)
