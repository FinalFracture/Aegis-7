"""temp-Courts: F3-TRK running-track kit — straight, corner, stair-landing crossing.
Loop outer X 0.7..127.6, Z 0.7..78.4; 1.8 m wide, 2 lanes 0.9 m. E outer edge stays 127.6.
Inner corner radius 1.2 m (outer 3.0). +Z = infield. No wood, no planters, no BLEND.
Void-edge rail: reuse tt_struct_void_guard (structure / F3-SLNG), not rebuilt here.
Run: python3 track.py [--render]"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
TT = os.path.abspath(os.path.join(HERE, "..", ".."))
if os.path.basename(os.path.normpath(TT)) != "tennis_tower":
    TT = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, TT)
from modlib import *
import pygltflib as pg

GODOT = os.path.join(ROOT, "godot/assets/models")
RENDER_DIR = "/workspace/renders/tennis_tower/rooms/temp-Courts"
# rubber-like slate + white/cyan lane paint
W, LANE, TH, GAP, LW = 1.8, 0.9, .04, .008, .04
R_IN, R_OUT = 1.2, 3.0

def straight(q=None):
    """Default 8 m straight; q['L'] overrides length. Width 1.8 m along Z, length along X, +Z infield."""
    q = {} if q is None else dict(q)
    L = float(q.get("L", 8.0))
    p = Part(); x0, x1, z0, z1 = -L / 2, L / 2, -W / 2, W / 2
    p.add("Track_Bed", SL, box(x0, x1, 0, TH, z0, z1))
    p.add("Track-colonly", SL, box(x0, x1, 0, TH, z0, z1))
    y0, y1 = TH + GAP, TH + GAP + .003
    # outer kerb (thin, -Z), mid lane line, inner kerb tick
    p.add("Lane_Paint", WH,
          box(x0 + .02, x1 - .02, y0, y1, -LANE / 2 - LW / 2, -LANE / 2 + LW / 2),  # mid split
          box(x0 + .02, x1 - .02, y0, y1, z0 + .015, z0 + .015 + LW),
          box(x0 + .02, x1 - .02, y0, y1, z1 - .015 - LW, z1 - .015))
    p.add("Cyan_Ticks", CY,
          *[box(x, x + .08, y1 + GAP, y1 + GAP + .003, .12, .22)
            for x in np.arange(x0 + .5, x1 - .4, 4.0)])
    p.add("Moss_Tufts", LF2, clump((x0 + .15, TH + .01, z0 + .12), .03, seed=2),
          clump((x1 - .15, TH + .01, z1 - .12), .03, seed=3))
    return p

def _prism_xz(outline, y0, y1):
    """prism()/loft caps fan from (0,y,0); centroid-centre the outline so caps stay non-degenerate."""
    o = np.asarray(outline, float)
    c = o.mean(axis=0)
    return xf(prism(o - c, y0, y1), t=(float(c[0]), 0.0, float(c[1])))

def corner(q=None):
    """Quarter-annulus, built in +X+Z from circle centre, then recentered. r 1.2..3.0, 1.8 m band."""
    p = Part(); n = 12
    an = np.linspace(0, np.pi / 2, n + 1)
    slabs, cols = [], []
    for a, b in zip(an[:-1], an[1:]):
        c0, c1, s0, s1 = np.cos(a), np.cos(b), np.sin(a), np.sin(b)
        outline = [(R_OUT * c0, R_OUT * s0), (R_OUT * c1, R_OUT * s1),
                   (R_IN * c1, R_IN * s1), (R_IN * c0, R_IN * s0)]
        slabs.append(_prism_xz(outline, 0, TH))
        cols.append(_prism_xz(outline, 0, TH))
    p.add("Track_Bed", SL, *slabs)
    p.add("Track-colonly", SL, *cols)
    # paint arcs at mid-lane r=2.1, outer 2.96, inner 1.24
    y0, y1 = TH + GAP, TH + GAP + .003
    def _ring(r, w=LW):
        ms = []
        for a, b in zip(an[:-1], an[1:]):
            c0, c1, s0, s1 = np.cos(a), np.cos(b), np.sin(a), np.sin(b)
            r0, r1 = r - w / 2, r + w / 2
            outline = [(r1 * c0, r1 * s0), (r1 * c1, r1 * s1), (r0 * c1, r0 * s1), (r0 * c0, r0 * s0)]
            ms.append(_prism_xz(outline, y0, y1))
        return ms
    p.add("Lane_Paint", WH, *(_ring(R_IN + LANE) + _ring(R_IN + .06) + _ring(R_OUT - .06)))
    mid_a = np.pi / 4
    p.add("Cyan_Ticks", CY, box(2.08, 2.16, y0, y1 + .001, 2.08, 2.16))
    p.add("Moss_Tufts", LF2, clump(((R_OUT - .12) * np.cos(.2), TH + .01, (R_OUT - .12) * np.sin(.2)), .03, seed=4))
    return p

def crossing(q=None):
    """6 m stair-landing crossing (same envelope as a short straight). Zebra + lane continuity."""
    q = {} if q is None else dict(q)
    L = float(q.get("L", 6.0))
    p = Part(); x0, x1, z0, z1 = -L / 2, L / 2, -W / 2, W / 2
    p.add("Track_Bed", SL, box(x0, x1, 0, TH, z0, z1))
    p.add("Track-colonly", SL, box(x0, x1, 0, TH, z0, z1))
    y0, y1 = TH + GAP, TH + GAP + .003
    p.add("Lane_Paint", WH,
          box(x0 + .02, x1 - .02, y0, y1, -LANE / 2 - LW / 2, -LANE / 2 + LW / 2),
          box(x0 + .02, x1 - .02, y0, y1, z0 + .015, z0 + .015 + LW),
          box(x0 + .02, x1 - .02, y0, y1, z1 - .015 - LW, z1 - .015))
    # zebra bars across both lanes, 8 mm above paint, inset from kerbs
    bars = []
    for i, x in enumerate(np.arange(x0 + .25, x1 - .25, .35)):
        bars.append(box(x, x + .16, y1 + GAP, y1 + GAP + .003, z0 + .08, z1 - .08))
    p.add("Zebra", WH, *bars)
    p.add("Amber_Hold", AM, box(-L / 2 + .08, -L / 2 + .22, y1 + GAP, y1 + GAP + .003, .10, .22))
    p.add("Moss_Tufts", LF2, clump((x0 + .12, TH + .01, z1 - .12), .03, seed=7))
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
    g = pg.GLTF2().load(path); blend = [m.name for m in (g.materials or []) if m.alphaMode == "BLEND"]
    return dict(scissor_ok=(not blend), scissor_bad=[], blend=blend)

def promote(name, builder, label=""):
    os.makedirs(GODOT, exist_ok=True)
    p = recenter(builder())
    vis = {k: v for k, v in p.P.items() if "colonly" not in k}
    chk = cc.check(vis, n_samp=400)
    gp = os.path.join(GODOT, f"{name}.glb")
    tris, geo = export_final(p.P, [gp]); finish_glb(gp)
    nchk = _check_normals(gp); schk = _check_scissor_mats(gp)
    try:
        ok_v = vm.validate_file(gp, check_tri_range=(1, 5999), require_textures=False, require_blend_glass=False)
    except AssertionError as e:
        print("VALIDATE FAIL", e); ok_v = False
    has_col = any("colonly" in k for k in p.P)
    V = np.vstack([m.vertices for k, (_, m) in p.P.items() if "colonly" not in k])
    lo, hi = V.min(0), V.max(0)
    r = dict(asset=name, label=label, tris=int(tris), clip_pass=chk["pass"], worst_overlap=chk["worst_overlap"],
             coplanar=len(chk.get("coplanar") or []), pivot=chk["pivot"], size=chk["size"],
             names_ok=name_rule(p), validate=bool(ok_v), colliders=has_col,
             aabb={"min": lo.tolist(), "max": hi.tolist(), "size": (hi - lo).tolist()}, **nchk, **schk)
    r["passed"] = bool(ok_v and chk["pass"] and tris <= 5999 and name_rule(p) and nchk["normals_ok"]
                       and schk["scissor_ok"] and has_col and abs(float(chk["pivot"]["min_y"])) < 1e-6)
    print(json.dumps(r, default=str)); return r, p, geo

def render_views(name, geo):
    os.makedirs(RENDER_DIR, exist_ok=True)
    g = {k: v for k, v in geo.items() if "colonly" not in k}
    a = np.radians(4)
    eye = np.array([[1, 0, 0], [0, np.cos(a), -np.sin(a)], [0, np.sin(a), np.cos(a)]])
    top = np.array([[1, 0, 0], [0, 0, -1], [0, 1, 0]], float)
    for tag, R in (("iso", views()[3]), ("player", eye), ("top", top)):
        path = os.path.join(RENDER_DIR, f"{name}_{tag}.png")
        im = crop(render_view(g, R, size=640, shadow=True, glass_alpha=.35))
        plt.imsave(path, np.clip(im, 0, 1)); print("render", path)

if __name__ == "__main__":
    do_render = "--render" in sys.argv
    # full-run straights as dedicated assets so tiling is exact (no leftover gaps)
    jobs = [
        ("tt_trk_straight", lambda: straight({"L": 8.0}), "8 m straight module"),
        ("tt_trk_straight_sn", lambda: straight({"L": 120.9}), "S/N full straight 120.9 m"),
        ("tt_trk_straight_ew", lambda: straight({"L": 71.7}), "E/W full straight 71.7 m"),
        ("tt_trk_corner", corner, "quarter corner r 1.2-3.0"),
        ("tt_trk_crossing", crossing, "6 m stair-landing crossing"),
    ]
    reps = []
    for name, fn, lab in jobs:
        r, p, geo = promote(name, fn, lab); reps.append(r)
        if do_render and r["passed"]:
            render_views(name, geo)
    summary = dict(all_passed=all(x["passed"] for x in reps),
                   tris={x["asset"]: x["tris"] for x in reps},
                   fails=[x["asset"] for x in reps if not x["passed"]],
                   aabb={x["asset"]: x.get("aabb") for x in reps})
    print(json.dumps(summary, indent=1))
    if not summary["all_passed"]:
        sys.exit(1)
