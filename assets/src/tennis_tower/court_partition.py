"""temp-Courts: Tennis Tower F1 court partition kit (scissor glass/net, no planters, colliders, open+closed doors).
Former BLEND glass -> TT_GlassScissor (MASK, cutoff 0.5, baseColor alpha 1.0). Net -> TT_NetScissor.
GAGE_NOTES #56 glass-line offsets changed after planter removal: see GLASS_LINE_* printed at export.
Y-up, +Z = court side, bottom-centre pivot. Run: python3 court_partition.py [--render]"""
from modlib import *
import tempfile, pygltflib as pg

# ---- scissor helpers (prefer shared struct_lib) ----
def _fallback_scissor():
    global SCR, NET, finish_scissor
    _m("tt_scr", "TT_GlassScissor", (.72, .86, .93), 0, .08, a=1.0)
    _m("tt_net", "TT_NetScissor", (.10, .12, .15), .3, .7, a=1.0)
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
        im = Image.new("RGBA", (n, n), rgb + (0,)); im.putalpha(Image.fromarray(a)); b = io.BytesIO(); im.save(b, "PNG"); return b.getvalue()
    def finish_scissor(path):
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
            bc = m.pbrMetallicRoughness.baseColorFactor
            if bc is None: m.pbrMetallicRoughness.baseColorFactor = [0.72, 0.86, 0.93, 1.0]
            else: m.pbrMetallicRoughness.baseColorFactor = [bc[0], bc[1], bc[2], 1.0]
            m.pbrMetallicRoughness.baseColorTexture = pg.TextureInfo(index=len(g.textures) - 1)
        if hit:
            while len(blob) % 4: blob.append(0)
            g.buffers[0].byteLength = len(blob); g.set_binary_blob(bytes(blob)); g.save_binary(path)
try:
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "structure"))
    from struct_lib import SCR, NET, finish_scissor  # noqa: E402
except Exception:
    _fallback_scissor()

GH, NH, PW = 3.0, 2.0, .08
GODOT = os.path.join(ROOT, "godot/assets/models")
RENDER_DIR = "/workspace/renders/tennis_tower/rooms/temp-Courts"
GLASS_LINE_PANEL = None
GLASS_LINE_DOOR = None

def _moss_on_post(xp, y0=0.12):
    # sit just outside the post face (half-width ~0.04); keep overlap <= 10 mm
    return [clump((xp + .055, y0 + .06, s * .07), .035, seed=2 + i) for i, s in enumerate((-1, 1))]

def _leaf_crest(xp, y):
    # crest above the post top / around the finial — no post body intersection
    return [leaf_dir((xp + np.cos(a) * .07, y, np.sin(a) * .07), (np.cos(a) * .35, 1.1, np.sin(a) * .35), .18, .07, t=.008)
            for a in (np.pi / 4, 3 * np.pi / 4, 5 * np.pi / 4, 7 * np.pi / 4)]

def build(q=None):
    """2.0 m panel: floor channel, scissor pane, steel post to 5.0 m, leaf/moss nature, colliders."""
    q = q or {}; p = Part(); xp = -1 + PW / 2
    # solids
    p.add("Floor_Channel", G, box(-.999, .999, 0, .08, -.04, .04))
    p.add("Post_Steel", ST, box(-.997, -1 + PW, .08 - E, GH + NH, -.045, .045))
    clampx = (-1 + PW + .004, -1 + PW + .1)
    for y in (.6, 2.4):
        for s in (-1, 1):
            z0, z1 = sorted((s * (.006 - E), s * .026))
            p.add("Pane_Clamps", G, box(clampx[0] - .006, clampx[1], y - .05, y + .05, z0, z1))
    p.add("Court_Line_LED", AM, box(-1 + PW + .004, .995, .08 - E, .11, .04 - E, .046))
    p.add("Ball_Finial", BA, node((xp, GH + NH + .065 - E, 0), .065, 1))
    p.add("Leaf_Capital", LF, *_leaf_crest(xp, GH + NH + .02))
    p.add("Moss_Tufts", LF2, *_moss_on_post(xp))
    # scissor pane (no 'glass' in name)
    p.add("Court_Pane_Scissor", SCR, box(-1 + PW + .004, .995, .08 - E, GH, -.006, .006))
    # colliders (solids only; match visible; no scissor)
    p.add("Post-colonly", G, box(-.997, -1 + PW, .08 - E, GH + NH, -.045, .045))
    p.add("Channel-colonly", G, box(-.999, .999, 0, .08, -.04, .04))
    return p

def net(q=None):
    """Ball net 2.0 x 2.0 m (own asset, place at y=+3.0)."""
    q = q or {}; p = Part(); m = q.get("mesh", .12); ms = []
    ms += [box(-.999, .999, 0, .03, -.01, .01), box(-.999, .999, NH - .03, NH, -.01, .01)]
    ms += [box(x - .003, x + .003, .03 - E, NH - .03 + E, -.003, .003) for x in np.arange(-.95, .96, m)]
    ms += [box(-.999, .999, y - .003, y + .003, -.004, .004) for y in np.arange(.1, NH - .05, m)]
    p.add("Ball_Net_Scissor", NET, *ms)
    p.add("Net_Rails-colonly", G, box(-.999, .999, 0, .03, -.01, .01), box(-.999, .999, NH - .03, NH, -.01, .01))
    return p

def _door_frame(p, closed):
    """Shared door bay: sidelight + 1.0 m clear opening. Leaf open (+Z) or closed in opening."""
    xp = -1 + PW / 2; jx = (-.14, -.06); oh = 2.2; open_x0, open_x1 = jx[1], .999
    p.add("Floor_Channel", G, box(-.999, jx[0] + E, 0, .08, -.04, .04))
    p.add("Sidelight_Scissor", SCR, box(-1 + PW + .004, jx[0] + E, .08 - E, GH, -.006, .006))
    # frame posts as non-degenerate boxes (avoid zero-area / zero normals)
    p.add("Post_Steel", ST,
          box(-.997, -1 + PW, .08 - E, GH + NH, -.045, .045),
          box(jx[0], jx[1], 0, GH, -.045, .045))
    p.add("Door_Header", G, box(jx[1] - E, .999, oh, oh + .1, -.04, .04))
    p.add("Transom_Scissor", SCR, box(jx[1] + .004, .995, oh + .1 - E, GH, -.006, .006))
    p.add("Leaf_Capital", LF, *_leaf_crest(xp, GH + NH + .02))
    p.add("Moss_Tufts", LF2, *_moss_on_post(xp))
    if closed:
        # leaf in opening; scissor inset by E from frame so no coplanar faces
        p.add("Door_Leaf_Frame", G,
              box(open_x0 + .02, open_x0 + .06, 0.02, oh - .02, -.02, .02),
              box(open_x1 - .06, open_x1 - .02, 0.02, oh - .02, -.02, .02),
              box(open_x0 + .02, open_x1 - .02, oh - .06, oh - .02, -.02, .02),
              box(open_x0 + .02, open_x1 - .02, 0.02, 0.06, -.02, .02))
        p.add("Door_Leaf_Scissor", SCR, box(open_x0 + .06 + E, open_x1 - .06 - E, 0.06 + E, oh - .06 - E, -.004, .004))
        p.add("Pull_Handle", ST, box(open_x1 - .08, open_x1 - .05, .9, 1.2, .02 + E, .05))
    else:
        # parked open 90° on court side (+Z); pane starts past frame face (+E)
        p.add("Door_Leaf_Frame", G, box(.93, .97, 0.02, oh - .02, .05, .1))
        p.add("Door_Leaf_Scissor", SCR, box(.944, .956, .1 + E, oh - .1, .1 + E, .96))
        p.add("Pull_Handle", ST, box(.97 + E, 1.0, .9, 1.2, .85, .89))
    # colliders: left pier / hinge pier / header; opening clear; leaf when present
    p.add("Frame-colonly", G,
          box(-.997, -1 + PW, 0, GH + NH, -.045, .045),
          box(jx[0], jx[1], 0, GH, -.045, .045),
          box(jx[1] - E, .999, oh, oh + .1, -.04, .04),
          box(-.999, jx[0] + E, 0, .08, -.04, .04))
    if closed:
        p.add("DoorLeaf-colonly", G, box(open_x0 + .02, open_x1 - .02, 0.02, oh - .02, -.02, .02))
    else:
        p.add("DoorLeaf-colonly", G, box(.93, .97, 0.02, oh - .02, .05, .96))
    return p

def door_open(q=None):
    return _door_frame(Part(), closed=False)

def door_closed(q=None):
    return _door_frame(Part(), closed=True)

def _pane_z(p, key_substr="Scissor"):
    zs = []
    for k, (mk, m) in p.P.items():
        if "colonly" in k: continue
        if key_substr in k and mk in (SCR, NET):
            zs.append(float(m.bounds.mean(0)[2]))
    return round(float(np.mean(zs)), 4) if zs else None

def _check_normals(path):
    """Fail if any mesh normal has near-zero length."""
    tm = trimesh.load(path, force="scene")
    geoms = list(tm.geometry.values()) if hasattr(tm, "geometry") else [tm]
    bad = 0; total = 0
    for g in geoms:
        if g is None or not hasattr(g, "faces") or len(g.faces) == 0: continue
        try: n = g.face_normals
        except Exception: g.rezero(); n = g.face_normals
        lens = np.linalg.norm(n, axis=1); total += len(lens); bad += int(np.sum(lens < 1e-8))
        if hasattr(g, "vertex_normals") and g.vertex_normals is not None and len(g.vertex_normals):
            vl = np.linalg.norm(g.vertex_normals, axis=1); total += len(vl); bad += int(np.sum(vl < 1e-8))
    return dict(normals_ok=(bad == 0), normals_bad=bad, normals_checked=total)

def _check_scissor_mats(path):
    g = pg.GLTF2().load(path); bad = []
    for m in g.materials or []:
        if m.name not in ("TT_GlassScissor", "TT_NetScissor"): continue
        if m.alphaMode != "MASK" or abs((m.alphaCutoff or 0) - .5) > 1e-6: bad.append(f"{m.name}:mode")
        bc = (m.pbrMetallicRoughness.baseColorFactor or [1, 1, 1, 1])
        if abs(bc[3] - 1.0) > 1e-6: bad.append(f"{m.name}:alpha")
    blend = [m.name for m in (g.materials or []) if m.alphaMode == "BLEND"]
    return dict(scissor_ok=(not bad and not blend), scissor_bad=bad, blend=blend)

def promote(name, builder, label=""):
    os.makedirs(GODOT, exist_ok=True)
    p = recenter(builder({})); glass_z = _pane_z(p)
    vis = {k: v for k, v in p.P.items() if "colonly" not in k}
    chk = cc.check(vis, n_samp=400)
    gp = os.path.join(GODOT, f"{name}.glb")
    tris, geo = export_final(p.P, [gp]); finish_glb(gp); finish_scissor(gp)
    # ensure GlassScissor alpha factor 1.0 even if shared finish_scissor skipped factor rewrite
    g = pg.GLTF2().load(gp); dirty = False
    for m in g.materials or []:
        if m.name == "TT_GlassScissor":
            bc = m.pbrMetallicRoughness.baseColorFactor or [0.72, 0.86, 0.93, 1.0]
            if abs(bc[3] - 1.0) > 1e-6:
                m.pbrMetallicRoughness.baseColorFactor = [bc[0], bc[1], bc[2], 1.0]; dirty = True
            if m.alphaMode != "MASK" or abs((m.alphaCutoff or 0) - .5) > 1e-6:
                m.alphaMode = "MASK"; m.alphaCutoff = .5; dirty = True
    if dirty: g.save_binary(gp)
    nchk = _check_normals(gp); schk = _check_scissor_mats(gp)
    try:
        ok_v = vm.validate_file(gp, check_tri_range=(1, TRI_MAX), require_textures=False, require_blend_glass=False)
    except AssertionError as e:
        print("VALIDATE FAIL", e); ok_v = False
    has_col = any("colonly" in k for k in p.P)
    r = dict(asset=name, label=label, tris=int(tris), glass_line_z=glass_z, clip_pass=chk["pass"],
             worst_overlap=chk["worst_overlap"], pivot=chk["pivot"], size=chk["size"],
             names_ok=name_rule(p), validate=bool(ok_v), colliders=has_col, **nchk, **schk)
    r["passed"] = bool(ok_v and chk["pass"] and tris <= TRI_MAX and name_rule(p) and nchk["normals_ok"]
                       and schk["scissor_ok"] and has_col and abs(float(chk["pivot"]["min_y"])) < 1e-6)
    print(json.dumps(r, default=str)); return r, p, geo

def render_views(name, geo):
    os.makedirs(RENDER_DIR, exist_ok=True)
    g = {k: v for k, v in geo.items() if "colonly" not in k}
    a = np.radians(4)
    eye = np.array([[1, 0, 0], [0, np.cos(a), -np.sin(a)], [0, np.sin(a), np.cos(a)]])
    top = np.array([[1, 0, 0], [0, 0, -1], [0, 1, 0]], float)
    for tag, R in (("iso", views()[3]), ("player", eye), ("top", top)):
        im = crop(render_view(g, R, size=640, shadow=True, glass_alpha=.35))
        plt.imsave(os.path.join(RENDER_DIR, f"{name}_{tag}.png"), np.clip(im, 0, 1))
        print("render", os.path.join(RENDER_DIR, f"{name}_{tag}.png"))

if __name__ == "__main__":
    do_render = "--render" in sys.argv
    jobs = [
        ("tt_court_partition", build, "panel leaf/moss scissor"),
        ("tt_court_net", net, "ball net scissor"),
        ("tt_court_partition_door", door_open, "door open 90deg"),
        ("tt_court_partition_door_closed", door_closed, "door closed"),
    ]
    reps = []
    g_panel = g_door = None
    for name, fn, lab in jobs:
        r, p, geo = promote(name, fn, lab); reps.append(r)
        if name == "tt_court_partition":
            g_panel = r["glass_line_z"]
        if name == "tt_court_partition_door":
            g_door = r["glass_line_z"]
        if do_render and r["passed"]:
            render_views(name, geo)
    print(json.dumps({"GLASS_LINE_PANEL": g_panel, "GLASS_LINE_DOOR": g_door,
                      "all_passed": all(x["passed"] for x in reps)}, indent=1))
    if not all(x["passed"] for x in reps):
        sys.exit(1)
