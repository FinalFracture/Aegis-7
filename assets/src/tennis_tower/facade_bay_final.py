"""Rook: #75 generic F1-F2 façade bay, final (Jared pick V1 Branch Glass, thickened). 4.0 m x 12.2 m + 2.0 m half bay.
Layers (out from the glass line z 0): recessed TT_GlassScissor panes with deep gunmetal reveal frames (z to +0.15) | slate spandrel band + gunmetal
soffit/header with cyan downlight at +6.1 | stepped slate plinth ledge + slate sill | free-standing Branch Fin trunk (z +0.55) with
sculpted Y-forks onto the reveal frames, leaf clusters seated on the fork nodes, Leaf Capital. Inside: heavy fin + light fin (-Z, #52).
Colliders: Wall-colonly (glass/frame plane) + Plinth-colonly + Trunk-convcolonly. Run: python3 facade_bay_final.py"""
from modlib import *
from restroom_extras import crest
from structure.struct_lib import SCR, finish_scissor
H = 12.2; ROWS = [(.7, 3.05), (3.05, 5.42), (6.62, 9.15), (9.15, 12.05)]
def _fin(x, y0, y1, depth, t, z0=0.0, belly=0.0):
    # Closed box for belly=0 (facade fins). Avoids loft end-cap zero-area faces that become zero-length normals.
    if belly > 0:
        m = fin(x, y0, y1, depth, t, z0=z0, belly=belly); uv = np.array(m.metadata["uv"], copy=True)
        m.update_faces(m.nondegenerate_faces()); m.remove_unreferenced_vertices(); m.metadata["uv"] = m.vertices[:, [0, 1]]; return m
    return box(x - t/2, x + t/2, y0, y1, z0 - depth, z0)
def build(q):
    w = q.get("width", 4.0); h = w/2; X0, X1 = -h + .001, h - .001; p = Part(); F = []
    PZ = -.525 if q.get("pool") else None   # r7c (Aquatics 667f3cc): S bays X 2..26 behind the lap-tank wall (Z 0.500): ledge / edge fin to raw z >= -0.525 (world Z <= 0.496)
    F += [box(X0, X1, H - .15, H, -.65, .1), _fin(-h + .06, .6 - E, H - .15 + E, .555 if PZ else .6, .05, z0=.03), box(h - .045, h - .01, .6 - E, H - .15 + E, -.04, .04)]
    cols = [(-h + .085, -.0125), (.0125, h - .045)] if w > 3 else [(-h + .085, h - .045)]
    if w > 3: F.append(_fin(0, .6 - E, H - .15 + E, .45, .025, z0=.03))
    # recessed alpha-scissor panes + deep reveal frames (4 bars per cell, standing proud to z +0.15)
    R = []
    for r, (y0, y1) in enumerate(ROWS):
        for c, (a, b) in enumerate(cols):
            p.add(f"Pane_Scissor_{r}{c}", SCR, pane(a + .002, b - .002, y0 + .008, y1 - .008, -.045, t=.02))
            R += [box(a + .004, a + .07, y0 + .004, y1 - .004, -.04, .15), box(b - .07, b - .004, y0 + .004, y1 - .004, -.04, .15),
                  box(a + .07 - E, b - .07 + E, y0 + .004, y0 + .07, -.04, .15), box(a + .07 - E, b - .07 + E, y1 - .07, y1 - .004, -.04, .12)]
    F += R
    # plinth ledge (stepped) + slate sill
    p.add("Plinth_Ledge", SL, box(X0, X1, 0, .45, -.1, .42), box(X0, X1, .45 - E, .6, PZ if PZ else -.65, .3))
    p.add("Slate_Sill", SSL, box(X0, X1, .596, .702, .045, .26))
    p.add("Plinth_Court_Line", AM, box(X0, -h + .047, .2, .24, .42 - E, .427), box(-h + .453, X1, .2, .24, .42 - E, .427))
    # spandrel band between F1 and F2 (5.6..6.52) with soffit/header
    p.add("Spandrel_Band", SL, box(X0, X1, 5.6 + .002, 6.52 - .002, .042, .2))
    F += [box(X0, X1, 5.42 - .004, 5.6 + .004, -.04, .34), box(X0, X1, 6.52 - .004, 6.62 + .004, -.04, .3)]; p.add("Frame", G, *F)
    p.add("Soffit_Downlight", CY, box(X0 + .1, X1 - .1, 5.41, 5.416 + E, .2, .3))
    p.add("Spandrel_Court_Line", AM, box(X0, X1, 6.0, 6.05, .2 - E, .207))
    # Branch Fin trunk(s), free-standing in front of the frames
    xs = [-h + .25] if w < 3 else [-h + .25, .02 + .0]
    xs = xs[:1] if w < 3 else [-h + .25]
    T = []; Lc = []; zt = .62
    for x0 in xs:
        p.add("Trunk_Pedestal", SL, box(x0 - .2, x0 + .2, 0, .45, .42 - E, .84))
        T += [node((x0, .45 + .11 - E, zt), .11, 0), tube((x0, .55, zt), (x0, 11.4, zt), .085, 10)]
        for y in (3.05, 9.15):
            n = (x0, y, zt); T += [node(n, .13, 0)]
            for (dx, dy, rr) in ((.85, .55, .05), (.55, 1.0, .04), (.9, -.45, .04)):
                e = (x0 + dx, y + dy, .15 + .03 - E); m = (x0 + dx*.45, y + dy*.55, zt - .12)
                T += [tube(n, m, rr + .012, 8), node(m, rr + .02, 0), tube(m, e, rr, 6), node((e[0], e[1], .15 + .02), rr*.9, 0)]
            Lc += [clump((x0, y + .16, zt + .249), .17, int(y))]
        T += [node((x0, 11.4, zt), .12, 0)]
        for a in (0, np.pi/3, -np.pi/3, np.pi): Lc.append(xf(crest((0, 0, 0)), R=trimesh.transformations.rotation_matrix(a, [0, 1, 0]), t=(x0, 11.4 + .12 - .01, zt)))
        p.add("Trunk-convcolonly", G, box(x0 - .2, x0 + .2, 0, 11.5, zt - .2, zt + .2))
    p.add("Branch_Trunk", G, *T); p.add("Fork_Leaves", LF, *Lc[:-4] if False else Lc)
    p.add("Wall-colonly", G, box(X0, X1, .6, H, -.08, .02)); p.add("Plinth-colonly", SL, box(X0, X1, 0, .7, -.1, .42))
    return p
VARIANTS = [dict(label="Branch Glass final: 4.0 m bay", width=4.0), dict(label="Branch Glass final: 2.0 m half bay", width=2.0)]
from entrance_bay_final import run_layout as _rl
import entrance_bay_final as _ebf
def run_layout(widths):
    _ebf.build, b0 = build, _ebf.build
    try: return _rl(widths)
    finally: _ebf.build = b0
def seam_check(widths):
    A = {k: v for k, v in run_layout(widths).items() if "colonly" not in k}; edge = widths[0]
    near = {k: v for k, v in A.items() if v[1].bounds[1][0] > edge - .6 and v[1].bounds[0][0] < edge + .6}
    chk = cc.check(near, n_samp=300); bad = [o for o in chk["overlap"] if not o[3] and o[0][:2] != o[1][:2]]; cop = [c for c in chk["coplanar"] if c[0][:2] != c[1][:2]]
    return dict(bad=bad[:3], coplanar=cop[:3], pass_=not bad and not cop)
def promote_pool():   # r7c: tt_facade_bay_pool (header keeps -0.65, so bbox / pivot match tt_facade_bay)
    p = recenter(build(dict(VARIANTS[0], pool=True))); gp = os.path.join(ROOT, "godot/assets/models", "tt_facade_bay_pool.glb")
    chk = cc.check({k: v for k, v in p.P.items() if "colonly" not in k}, n_samp=300)
    tris, _ = export_final(p.P, [gp]); finish_glb(gp); finish_scissor(gp)
    ok = vm.validate_file(gp, check_tri_range=(1, TRI_MAX), require_textures=False, require_blend_glass=False)
    V = np.vstack([m.vertices for _, m in p.P.values()])
    print("tt_facade_bay_pool.glb", int(tris), chk["pass"], chk["worst_overlap"], [o for o in chk["overlap"] if not o[3]][:3], chk["coplanar"][:3], ok, V.min(0).round(4).tolist(), V.max(0).round(4).tolist())
def promote():
    for prm, fn in ((VARIANTS[0], "tt_facade_bay.glb"), (VARIANTS[1], "tt_facade_bay_half.glb")):
        p = recenter(build(prm)); gp = os.path.join(ROOT, "godot/assets/models", fn)
        tris, _ = export_final(p.P, [gp]); finish_glb(gp); finish_scissor(gp)
        V = np.vstack([m.vertices for _, m in p.P.values()]); lo, hi = V.min(0), V.max(0)
        print(fn, "tris", int(tris), "bbox", lo.round(4).tolist(), hi.round(4).tolist())
if __name__ == "__main__" and sys.argv[1:] == ["pool"]:
    promote_pool()
elif __name__ == "__main__":
    rep = run("facade_bay_final", build, VARIANTS, title="F1-F2 facade bay final", sheet="facade_bay_final_run_sheet.png", post=finish_scissor)
    seams = {str(w): seam_check(w) for w in ([4, 4], [4, 2], [2, 4])}; print("SEAMS", seams)
    rdir = os.path.join(RENDER_OUT, "facade_bay_final"); os.makedirs(rdir, exist_ok=True)
    Ry = lambda el, az: (lambda a, b: np.array([[1, 0, 0], [0, np.cos(b), -np.sin(b)], [0, np.sin(b), np.cos(b)]]) @ np.array([[np.cos(a), 0, np.sin(a)], [0, 1, 0], [-np.sin(a), 0, np.cos(a)]]))(np.radians(az), np.radians(el))
    fig = plt.figure(figsize=(26, 17), facecolor="#F4F2EC"); gs = fig.add_gridspec(2, 4)
    shots = [(0, (6, 40), "4.0 m bay, low 3/4"), (0, (20, -75), "4.0 m bay, raking side (depth)"), (0, (-10, 60), "4.0 m bay, from below (soffit, forks)"), (1, (6, 40), "2.0 m half bay")]
    for j, (vi, (el, az), t) in enumerate(shots):
        p = recenter(build(VARIANTS[vi])); gp = f"/tmp/fbf_{j}.glb"; _, geo = export_final(p.P, [gp]); finish_scissor(gp)
        geo = {k: v for k, v in geo.items() if "colonly" not in k}
        im = crop(render_view(geo, Ry(el, az), size=800, shadow=False, glass_alpha=.35))
        ax = fig.add_subplot(gs[0, j]); ax.imshow(np.clip(im, 0, 1)); ax.axis("off"); ax.set_title(f"{t}\n{rep[vi]['tris']} tris | {'PASS' if rep[vi]['passed'] else 'FAIL'}", fontsize=11)
    Pt = Part()
    for n, (mk, m) in run_layout([4, 4, 2, 4, 4]).items():
        if "colonly" not in n: Pt.add(n, mk, m)
    _, g2 = export_final(Pt.P, ["/tmp/fbf_run.glb"]); finish_scissor("/tmp/fbf_run.glb"); im = crop(render_view(g2, Ry(10, 28), size=1400, shadow=False, glass_alpha=.35))
    ax = fig.add_subplot(gs[1, :]); ax.imshow(np.clip(im, 0, 1)); ax.axis("off"); ax.set_title(f"run 4+4+2+4+4 m | seams 4|4, 4|2, 2|4: {'PASS' if all(s['pass_'] for s in seams.values()) else 'FAIL'}", fontsize=12)
    fig.suptitle("Rook | #75 tt_facade_bay (V1 Branch Glass, thickened) + tt_facade_bay_half | FINAL", fontsize=15)
    plt.tight_layout(rect=(0, 0, 1, .95)); sp = os.path.join(rdir, "facade_bay_final_sheet.png"); fig.savefig(sp, dpi=85, facecolor="#F4F2EC"); print("SHEET", sp)
    promote()
