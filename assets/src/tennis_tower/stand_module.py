"""temp-Courts: Tennis Tower hollow-rake stand kit (V6 hybrid sports+nature, scissor guards, colliders).
F12: 5 rows riser 0.40 tread 0.85. F3: 12 rows riser 0.45 tread 0.95.
Bay widths: 7.5 m (12 seats + 1.2 m aisle), cut-bay 3.8 m (corner-stair), 6.5 m (lift-gap).
Hollow: tread slabs + risers + side stringers only — under-stand WC volume from y=0 stays empty (no solid fill).
Guards: TT_GlassScissor MASK@0.5 alpha 1.0 (*_Scissor names, never 'glass'). No BLEND, no wood, no planters.
Colliders are simplified proxies matching the hollow solids (not a tri-doubling of every seat).
Front +Z = concourse, tiers rise toward -Z, bottom-centre pivot. Preserve existing depth so stand-back stays Z14.7 in placement.
F3 splits into tt_stand_module_f3 (rake/rail) + tt_stand_module_f3_seats (seats/canopy) when full >6k.
Run: python3 stand_module.py [--render] [--split-f3]"""
from modlib import *
import pygltflib as pg

def _fallback_scissor():
    global SCR, finish_scissor
    import modlib as _ML
    _ML._m("tt_scr", "TT_GlassScissor", (.72, .86, .93), 0, .08, a=1.0)
    SCR = "tt_scr"
    def _tex_png():
        from PIL import Image
        n = 64; bay = np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]) / 16.0
        a = ((np.tile(bay, (n // 4, n // 4))) < .30).astype(np.uint8) * 255
        a[:4, :] = a[-4:, :] = a[:, :4] = a[:, -4:] = 255
        im = Image.new("RGBA", (n, n), (184, 219, 237, 0)); im.putalpha(Image.fromarray(a))
        b = io.BytesIO(); im.save(b, "PNG"); return b.getvalue()
    def finish_scissor(path):
        g = pg.GLTF2().load(path); blob = bytearray(g.binary_blob()); hit = False
        for m in g.materials:
            if m.name != "TT_GlassScissor": continue
            hit = True; data = _tex_png()
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
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "structure"))
    from struct_lib import SCR, finish_scissor  # noqa: E402
except Exception:
    _fallback_scissor()

GODOT = os.path.join(ROOT, "godot/assets/models")
RENDER_DIR = "/workspace/renders/tennis_tower/rooms/temp-Courts"
CFG = {"F12": (5, .40, .85), "F3": (12, .45, .95)}
SLAB, FASCIA, STR_W, SEAT_PITCH = .14, .28, .10, .525
HA = .6  # half-aisle each side -> 1.2 m aisle when bays tile

def _seats_for(W):
    clear = max(.4, W - 2 * HA)
    ns = max(1, int(round(clear / SEAT_PITCH)))
    return ns, clear / ns

def _hollow_rake(p, W, n, R, T, seats_only=False, structure_only=False):
    x0, x1 = -W / 2, W / 2
    NS, sp = _seats_for(W)
    meta = dict(W=W, n=n, R=R, T=T, NS=NS, sp=sp, depth=T * n, height=R * n,
                back_z_local_before_recenter=-T * n, front_z_local_before_recenter=0.0)
    GAP = .008

    if not seats_only:
        seat_treads, seat_risers, aisle_solids, beams = [], [], [], []
        col_seat, col_aisle, col_beam = [], [], []
        for i in range(n):
            y_top = R * (i + 1); y_bot = y_top - SLAB
            z0, z1 = -T * (i + 1), -T * i + (E if i else 0)
            sx0, sx1 = x0 + HA + E, x1 - HA - E
            # hollow seating bay: slab + riser only
            seat_treads.append(box(sx0, sx1, y_bot, y_top, z0, z1))
            col_seat.append(box(sx0, sx1, y_bot, y_top, z0, z1))
            if i == 0:
                seat_risers.append(box(sx0, sx1, max(0.0, y_bot - FASCIA), y_bot - GAP, z1 - .045, z1 - GAP))
            else:
                seat_risers.append(box(sx0, sx1, R * i + GAP, y_bot - GAP, z1 - .05, z1 - GAP))
            # solid aisle stairs (supports the rake; WC stays in centre bay)
            for s in (-1, 1):
                xa, xb = sorted((s * (W / 2 - .015), s * (W / 2 - HA + E)))
                aisle_solids.append(box(xa, xb, 0.0, y_top, z0, z1))
                col_aisle.append(box(xa, xb, 0.0, y_top, z0, z1))
        # short beam stubs from each aisle into the bay (centre WC volume stays clear — no full-span beams)
        stub = min(.55, max(.25, (W - 2 * HA) * .12))
        for i in range(1, n):  # skip lowest row (insufficient hang depth)
            y_top = R * (i + 1); y_bot = y_top - SLAB
            y_hang = y_bot - 0.50
            if y_hang < 0.45: continue
            zc0 = -T * i - T * .58; zc1 = -T * i - T * .38
            for xa, xb in ((x0 + HA + E, x0 + HA + E + stub), (x1 - HA - E - stub, x1 - HA - E)):
                beams.append(box(xa, xb, y_hang, y_bot - GAP, zc0, zc1))
                col_beam.append(box(xa, xb, y_hang, y_bot - GAP, zc0, zc1))
        # rear head beam above top tread (not under)
        yt, zb = R * n, -T * n
        beams.append(box(x0 + HA + .1, x1 - HA - .1, yt + GAP, yt + .05, zb - .05, zb - GAP))
        p.add("Tier_Slabs", SL, *seat_treads)
        p.add("Risers", SL, *seat_risers)
        p.add("Aisle_Solid", SL, *aisle_solids)
        p.add("Beams", G, *beams)
        p.add("Tiers-colonly", SL, *col_seat)
        p.add("Aisle-colonly", SL, *col_aisle)
        p.add("Beams-colonly", G, *col_beam)
        xs = np.linspace(x0 + HA + .15, x1 - HA - .15, max(3, int(W // 2.4) + 1))
        panes = [box(a + .05, b - .05, R + .15, R + .85, -.091, -.089) for a, b in zip(xs[:-1], xs[1:])]
        posts = [box(xp - .022, xp + .022, R + GAP, R + .96, -.108, -.072) for xp in xs]
        caps = [node((xp, R + 1.02, -.09), .05, 0) for xp in xs]
        p.add("Guard_Scissor", SCR, *panes)
        p.add("Rail_Posts", ST, *posts)
        p.add("Ball_Caps", BA, *caps)
        p.add("Row_LED", AM, *[box(x0 + HA + .08, x0 + HA + .36, R * i + .14, R * i + .17, -T * i + 3 * E, -T * i + 3 * E + .005) for i in range(1, n)])
        p.add("Rail-colonly", ST, *posts)
        p.add("Cyan_Edge", CY, box(x0 + HA + .1, x1 - HA - .1, R + GAP, R + .02, -.016, .006))
        moss = [clump((xs[0] + .05, R + .22, -.125), .026, seed=3), clump((xs[-1] - .05, R + .52, -.125), .024, seed=5)]
        p.add("Moss_Tufts", LF2, *moss)
        meta["probe_pts"] = [(0.0, min(1.1, R * n * .35), -T * n * f) for f in (.55, .75, .92)]
        meta["probe_pts"].append((0.0, R * (n // 2 + 1) - SLAB - .06, -T * (n // 2) - T * .5))
        meta["clear_origin"] = (0.0, 0.05, -T * n + .45)
        meta["wc_note"] = "centre seating bay hollow; aisle strips solid; cross-beams under mid-tread only"

    if not structure_only:
        seats, backs, peds = [], [], []
        col_rows = []
        for i in range(n):
            y, zc = R * (i + 1), -T * i - T * .45
            peds.append(box(x0 + HA + .14, x1 - HA - .14, y + GAP, y + .36, zc - .035, zc + .035))
            seats.append(box(x0 + HA + .16, x1 - HA - .16, y + .36 + GAP, y + .43, zc - .17, zc + .19))
            backs.append(box(x0 + HA + .16, x1 - HA - .16, y + .43 + GAP, y + .80, zc - .195, zc - .175))
            col_rows.append(box(x0 + HA + .14, x1 - HA - .14, y + GAP, y + .80, zc - .17, zc + .19))
        p.add("Seat_Beams", G, *peds)
        p.add("Seat_Pans", WH, *seats)
        p.add("Seat_Backs", WH, *backs)
        p.add("Seats-colonly", WH, *col_rows)
        yt, zb = R * n, -T * n + .12
        for xp in (x0 + min(1.15, W * .22), x1 - min(1.15, W * .22)):
            top = np.array([xp, yt + 2.6, zb])
            p.add("Canopy_Steel", ST,
                  tube((xp, yt + GAP, zb), top, .07, 5),
                  node(top, .09, 0),
                  tube(top, top + np.array([.55, .55, 1.25]), .045, 4),
                  tube(top, top + np.array([-.55, .55, 1.25]), .045, 4))
            p.add("Canopy_Leaves", LF,
                  leaf_dir(top + np.array([.55, .55, 1.3]), (0, .2, 1), 1.2, .5, t=.025),
                  leaf_dir(top + np.array([-.55, .55, 1.3]), (0, .2, 1), 1.2, .5, t=.025))
            p.add("Canopy-colonly", ST, tube((xp, yt + GAP, zb), top, .07, 5))
        if "probe_pts" not in meta:
            meta["probe_pts"] = [(0.0, min(1.1, R * n * .35), -T * n * f) for f in (.55, .75, .92)]
            meta["clear_origin"] = (0.0, 0.05, -T * n + .45)
    return p, meta

def build(q=None):
    if q is None: q = {}
    q = dict(q)
    W = float(q.get("W", 7.5)); n, R, T = CFG[q.get("cfg", "F12")]
    mode = q.get("mode", "full")
    p = Part()
    p, meta = _hollow_rake(p, W, n, R, T, seats_only=(mode == "seats"), structure_only=(mode == "structure"))
    p._stand_meta = meta
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
        if m.name != "TT_GlassScissor": continue
        if m.alphaMode != "MASK" or abs((m.alphaCutoff or 0) - .5) > 1e-6: bad.append(f"{m.name}:mode")
        bc = (m.pbrMetallicRoughness.baseColorFactor or [1, 1, 1, 1])
        if abs(bc[3] - 1.0) > 1e-6: bad.append(f"{m.name}:alpha")
    return dict(scissor_ok=(not bad and not blend), scissor_bad=bad, blend=blend)

def _hollow_probe(p, meta, recentered=False):
    """Probe under-volume emptiness. Prefer PRE-recenter Part + meta probe_pts."""
    vis = [m for k, (_, m) in p.P.items() if "colonly" not in k]
    if not vis: return dict(hollow_ok=False, reason="no_vis")
    solid = trimesh.util.concatenate(vis)
    probes = list(meta.get("probe_pts") or [])
    if recentered or not probes:
        # fallback: use AABB centre band
        V = np.vstack([m.vertices for m in vis]); lo, hi = V.min(0), V.max(0)
        probes = [(0.0, lo[1] + .5, lo[2] * f + hi[2] * (1 - f)) for f in (.2, .35, .5)]
    inside = 0
    for pt in probes:
        try:
            if solid.contains([pt])[0]: inside += 1
        except Exception:
            try:
                if solid.nearest.signed_distance([pt])[0] > 0: inside += 1
            except Exception:
                pass
    clear_h = None
    origin = meta.get("clear_origin")
    if origin is None and recentered:
        V = np.vstack([m.vertices for m in vis]); lo, hi = V.min(0), V.max(0)
        origin = (0.0, 0.05, lo[2] + .4)
    if origin is not None:
        try:
            locs, _, _ = solid.ray.intersects_location([list(origin)], [[0.0, 1.0, 0.0]], multiple_hits=False)
            if len(locs): clear_h = float(locs[0][1] - origin[1])
        except Exception:
            clear_h = None
    return dict(hollow_ok=(inside == 0), hollow_inside=inside, probes=probes,
                under_stand_clear_h_rear=clear_h, access_front_open=True,
                access_note="front fascia is lip-only; centre bay has no y=0 solid fill; side stringers only")

def promote(name, builder, label=""):
    os.makedirs(GODOT, exist_ok=True)
    raw = builder()
    meta = getattr(raw, "_stand_meta", {})
    # hollow check in pre-recenter frame (probe coords match builder)
    hchk = _hollow_probe(raw, meta, recentered=False)
    p = recenter(raw)
    vis = {k: v for k, v in p.P.items() if "colonly" not in k}
    chk = cc.check(vis, n_samp=400)
    gp = os.path.join(GODOT, f"{name}.glb")
    tris, geo = export_final(p.P, [gp]); finish_glb(gp); finish_scissor(gp)
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
    V = np.vstack([m.vertices for k, (_, m) in p.P.items() if "colonly" not in k])
    lo, hi = V.min(0), V.max(0)
    aabb = dict(min=lo.tolist(), max=hi.tolist(), size=(hi - lo).tolist(),
                back_face_z=float(lo[2]), front_face_z=float(hi[2]), min_y=float(lo[1]))
    # world stand-back note for S F1/F2 placement z=17.6 and F3 z=14.8 (assemble_preview)
    place = {}
    if meta.get("cfg") == "F3" or "f3" in name:
        place = dict(preview_put_z=14.8, implied_back_world_z=round(14.8 + float(lo[2]), 3))
    else:
        place = dict(preview_put_z=17.6, implied_back_world_z=round(17.6 + float(lo[2]), 3))
    glass_names = [k for k in p.P if "glass" in k.lower()]
    r = dict(asset=name, label=label, tris=int(tris), clip_pass=chk["pass"], worst_overlap=chk["worst_overlap"],
             pivot=chk["pivot"], size=chk["size"], names_ok=name_rule(p), validate=bool(ok_v),
             colliders=has_col, aabb=aabb, place_hint=place, meta=meta, glass_name_violations=glass_names,
             **nchk, **schk, **hchk)
    r["passed"] = bool(ok_v and chk["pass"] and tris <= TRI_MAX and name_rule(p) and nchk["normals_ok"]
                       and schk["scissor_ok"] and has_col and abs(float(chk["pivot"]["min_y"])) < 1e-6
                       and hchk["hollow_ok"] and not glass_names and abs(float(lo[1])) < 1e-6)
    if tris > TRI_MAX:
        try: os.remove(gp)
        except OSError: pass
        r["removed_over_budget"] = True
    print(json.dumps(r, default=str)); return r, p, geo

def render_views(name, geo):
    os.makedirs(RENDER_DIR, exist_ok=True)
    g = {k: v for k, v in geo.items() if "colonly" not in k}
    a = np.radians(4)
    eye = np.array([[1, 0, 0], [0, np.cos(a), -np.sin(a)], [0, np.sin(a), np.cos(a)]])
    top = np.array([[1, 0, 0], [0, 0, -1], [0, 1, 0]], float)
    under = np.array([[1, 0, 0], [0, np.cos(np.radians(28)), -np.sin(np.radians(28))],
                      [0, np.sin(np.radians(28)), np.cos(np.radians(28))]])
    for tag, R in (("iso", views()[3]), ("player", eye), ("top", top), ("under", under)):
        im = crop(render_view(g, R, size=640, shadow=True, glass_alpha=.35))
        path = os.path.join(RENDER_DIR, f"{name}_{tag}.png")
        plt.imsave(path, np.clip(im, 0, 1)); print("render", path)

def _f12_jobs():
    return [
        ("tt_stand_module", dict(cfg="F12", W=7.5, mode="full"), "F12 7.5m hollow V6"),
        ("tt_stand_module_3p8", dict(cfg="F12", W=3.8, mode="full"), "F12 3.8m cut bay"),
        ("tt_stand_module_6p5", dict(cfg="F12", W=6.5, mode="full"), "F12 6.5m cut bay"),
    ]

def _f3_split_jobs():
    out = []
    for W, tag in ((7.5, ""), (3.8, "_3p8"), (6.5, "_6p5")):
        out += [
            (f"tt_stand_module_f3{tag}", dict(cfg="F3", W=W, mode="structure"), f"F3{tag} rake/rail"),
            (f"tt_stand_module_f3{tag}_seats", dict(cfg="F3", W=W, mode="seats"), f"F3{tag} seats/canopy"),
        ]
    return out

if __name__ == "__main__":
    do_render = "--render" in sys.argv
    # F3 always split (full visual+seats exceeds 6k once colliders are honest proxies + detail)
    jobs = _f12_jobs() + _f3_split_jobs()
    reps = []
    for name, prm, lab in jobs:
        def _b(prm=prm):
            p = build(dict(prm)); p._stand_meta["cfg"] = prm.get("cfg"); return p
        r, p, geo = promote(name, _b, lab); reps.append(r)
        if do_render and r["passed"]:
            render_views(name, geo)
    summary = dict(all_passed=all(x["passed"] for x in reps),
                   assets=[x["asset"] for x in reps],
                   tris={x["asset"]: x["tris"] for x in reps},
                   fails=[x["asset"] for x in reps if not x["passed"]])
    print(json.dumps(summary, indent=1))
    if not summary["all_passed"]:
        sys.exit(1)
