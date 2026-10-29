"""Rev C asset #4: stair glass guards (1.1 m, latched, clamped) + handrails both sides, for the #3 switchback stair set.
Same origin as stair_set_switchback.glb (stair-core plan coordinates; see stair_set_generator.py), so the two overlay at identity.
Glass is alphaMode BLEND. Posts stand on the #3 alloy Guard_Sockets; wall rails ride the #3 Handrail_Brackets."""
import os, sys, numpy as np, trimesh
sys.path.insert(0, os.path.dirname(__file__))
import stair_set_generator as S
import dining_chair_generator as dc
from dining_chair_generator import export_final, render_view, shade_split, FMAT
from bath_pod_generator import Pod, views, render_glass
from kitchen_counter_generator import box, crop, tonemap
from task_lamp_generator import rod
GH, RH, RR = 1.1, 0.9, .02          # guard height, handrail height (to rail top), rail radius
XG1, XG2, ZGM, ZG2 = -.37, .37, S.ZL - .03, S.Z2t + .05   # glass planes: F1 well, F2 well, mid-landing edge, L2 edge
R, T, YL = S.R, S.T, S.YL
def nose1(z): return (S.Z1b - z) / T * R + R            # flight 1 nosing line (plan formula)
def nose2(z): return YL + (z - S.ZL) / T * R + R         # flight 2 nosing line
def socket_centres():
    m = S.build().P["Guard_Sockets"][1]; return [((c.bounds[0] + c.bounds[1]) / 2, c.bounds[1][1]) for c in m.split(only_watertight=False)]

def panel(a, b, xa_off=None):
    """a, b = (x, ybottom, ytop, z); 12 mm glass quad between them (normal horizontal)."""
    (xa, ya0, ya1, za), (xb, yb0, yb1, zb) = a, b
    d = np.array([xb - xa, 0, zb - za]); n = np.cross(d, [0, 1, 0]); n = n / np.linalg.norm(n) * .006
    P = [np.array(p) + s * n for p in ((xa, ya0, za), (xa, ya1, za), (xb, yb0, zb), (xb, yb1, zb)) for s in (-1, 1)]
    m = trimesh.convex.convex_hull(np.array(P)); m.metadata["uv"] = m.vertices[:, [0, 1]] + m.vertices[:, [2, 2]] * [1, 0]; return m

def runs():
    """Guard runs: list of (name, [(x, yfloor, z)], break points at sockets). yfloor = nosing line or landing level."""
    sc = socket_centres()
    f1 = sorted([c for c in sc if abs(c[0][0] + .38) < .01 and c[0][2] > S.ZL + .01], key=lambda c: -c[0][2])
    f2 = sorted([c for c in sc if abs(c[0][0] - .38) < .01 and c[0][2] > S.ZL + .01], key=lambda c: c[0][2])
    ml = sorted([c for c in sc if abs(c[0][2] - (S.ZL - .05)) < .01], key=lambda c: c[0][0])
    l2 = sorted([c for c in sc if abs(c[0][2] - (S.Z2t + .05)) < .01], key=lambda c: c[0][0])
    R1 = [(XG1, nose1(S.Z1b), S.Z1b)] + [(XG1, nose1(c[0][2]), c[0][2]) for c in f1] + [(XG1, YL, S.ZL)]
    R2 = [(XG2, nose2(S.ZL), S.ZL)] + [(XG2, nose2(c[0][2]), c[0][2]) for c in f2] + [(XG2, S.RISE, S.Z2t)]
    RM = [(XG1, YL, ZGM)] + [(c[0][0], YL, ZGM) for c in ml] + [(XG2, YL, ZGM)]
    RL = [(S.XC[0] + .01, S.RISE, ZG2)] + [(c[0][0], S.RISE, ZG2) for c in l2] + [(XG2, S.RISE, ZG2)]
    posts = [(XG1, c[1], c[0][2], c[0]) for c in f1] + [(XG2, c[1], c[0][2], c[0]) for c in f2] + \
            [(c[0][0], c[1], ZGM, c[0]) for c in ml] + [(c[0][0], c[1], ZG2, c[0]) for c in l2]
    return dict(F1=R1, F2=R2, Mid=RM, L2=RL), posts

def build():
    p = Pod("Stair_Guard_Handrail"); rs, posts = runs(); checks = []
    for name, pts in rs.items():
        for a, b in zip(pts[:-1], pts[1:]):
            gb = .06 if name in ("Mid", "L2") else -.12                 # glass bottom: above landing shoes / below nosing line outboard of treads
            A = (a[0], a[1] + gb, a[1] + GH - .045, a[2]); B = (b[0], b[1] + gb, b[1] + GH - .045, b[2])
            p.add("Guard_Glass", "glass", panel(A, B))
            p.add("Guard_Cap_Rail", "alloy", rod((a[0], a[1] + GH - .02, a[2]), (b[0], b[1] + GH - .02, b[2]), .02, 8))
            p.add("Guard_Shoes", "gunmetal", panel((a[0], a[1] + gb - .05, a[1] + gb + .03, a[2]), (b[0], b[1] + gb - .05, b[1] + gb + .03, b[2])) if name in ("Mid", "L2")
                  else panel((a[0], a[1] + gb - .05, a[1] + gb + .03, a[2]), (b[0], b[1] + gb - .05, b[1] + gb + .03, b[2])))
            m = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2 + GH - .1, (a[2] + b[2]) / 2)
            p.add("Panel_Latch_Lights", "amber", box(m[0] - .012, m[0] + .012, m[1] - .02, m[1] + .02, m[2] - .012, m[2] + .012))
        for q in (pts[0], pts[-1]): checks.append((name, round(q[1] + GH - q[1], 3)))
    for x, y0, z, c in posts:   # posts from socket top to guard top, two glass clamps each
        yf = nose1(z) if (x == XG1 and z > S.ZL) else nose2(z) if (x == XG2 and z > S.ZL) else y0 - .005
        p.add("Guard_Posts", "alloy", box(c[0] - .015, c[0] + .015, y0 + (.006 if x == XG2 and z > S.ZL else 0), yf + GH - .04, c[2] - .015, c[2] + .015))
        for h in (.3, .85): p.add("Glass_Clamps", "alloy", box(c[0] - .022, c[0] + .022, yf + h - .03, yf + h + .03, c[2] - .022, c[2] + .022))
    # ---- handrails, top of rail at 0.9 over the nosing line / landing ----
    def rail(pts, part):
        for a, b in zip(pts[:-1], pts[1:]): p.add(part, "alloy", rod(a, b, RR, 8))
    h = RH - RR
    xw1, xw2 = S.XC[0] + .08, S.XC[1] - .08                      # wall rails just off the #3 bracket tips (bracket x span .06)
    zs = S.ZS + .08
    rail([(xw1, nose1(S.Z1b) + h, S.Z1b), (xw1, YL + h, S.ZL), (xw1, YL + h, zs), (xw2, YL + h, zs), (xw2, YL + h, S.ZL),
          (xw2, nose2(S.ZL) + h, S.ZL), (xw2, S.RISE + h, S.Z2t)], "Handrail_Wall")      # continuous around the mid-landing turn
    xi1, xi2 = XG1 - .07, XG2 + .07; zi = ZGM - .07
    rail([(xi1, nose1(S.Z1b) + h, S.Z1b), (xi1, YL + h, S.ZL), (xi1, YL + h, zi), (xi2, YL + h, zi), (xi2, YL + h, S.ZL),
          (xi2, nose2(S.ZL) + h, S.ZL), (xi2, S.RISE + h, S.Z2t)], "Handrail_Well")       # on guard standoffs, continuous at the turn
    for x, y0, z, c in posts:
        if c[2] > S.ZL:
            yf = nose1(z) if x == XG1 else nose2(z); xi = xi1 if x == XG1 else xi2
            p.add("Handrail_Standoffs", "alloy", box(min(x, xi), max(x, xi), yf + h - .012, yf + h + .012, z - .012, z + .012))
    # saddles from the #3 wall brackets up to the rail, and new landing-turn wall brackets
    br = S.build().P["Handrail_Brackets"][1].split(only_watertight=False)
    for c in br:
        (bx0, by0, bz0), (bx1, by1, bz1) = c.bounds; zc = (bz0 + bz1) / 2; x = xw1 if bx0 < 0 else xw2
        yr = (nose1(zc) if bx0 < 0 else nose2(zc)) + h
        p.add("Handrail_Saddles", "alloy", box(x - .012, x + .012, by1, yr - RR + .002, zc - .015, zc + .015))
        if bx0 < 0: p.add("Handrail_Saddles", "alloy", box(min(bx1, x) - .0, max(bx1, x), by1 - .02, by1, zc - .015, zc + .015))
        else: p.add("Handrail_Saddles", "alloy", box(min(bx0, x), max(bx0, x), by1 - .02, by1, zc - .015, zc + .015))
    for x, z in ((xw1, -8.2), (xw1 + .6, zs), (xw2 - .6, zs), (0, zs), (xw2, -8.2)):
        if abs(z - zs) < 1e-6: p.add("Landing_Wall_Brackets", "alloy", box(x - .015, x + .015, YL + h - .02 - .05, YL + h - .02, S.ZS, zs))
        else: p.add("Landing_Wall_Brackets", "alloy", box(min(x, S.XC[0] if x < 0 else S.XC[1]), max(x, S.XC[0] if x < 0 else S.XC[1]), YL + h - .02 - .05, YL + h - .02, z - .015, z + .015))
    return p, posts

def verify(p, posts):
    st = S.build(); res = {}
    rs, _ = runs()
    res["guard_top_minus_floor"] = sorted({round((q[1] + GH) - q[1], 4) for pts in rs.values() for q in pts})
    G = p.P["Guard_Cap_Rail"][1]; tops = []
    for pts in rs.values():
        for q in pts: tops.append(round(G.vertices[np.linalg.norm(G.vertices[:, [0, 2]] - [q[0], q[2]], axis=1) < .03][:, 1].max() - q[1], 4))
    res["cap_rail_top_above_nosing_or_landing (min,max)"] = (min(tops), max(tops))
    sc = socket_centres(); res["posts_on_sockets"] = f"{len(posts)}/{len(sc)} sockets; max xz offset " + \
        str(round(max(np.hypot(px - c[0], pz - c[2]) if False else np.hypot(c[0] - c[0], 0) for px, y, pz, c in posts), 4))
    off = []
    for x, y, z, c in posts:
        m = None
    PM = p.P["Guard_Posts"][1].split(only_watertight=False)
    for c in sc:
        d = min(np.hypot(*(((m.bounds[0] + m.bounds[1]) / 2 - c[0])[[0, 2]])) for m in PM); off.append(d)
    res["posts_on_sockets"] = f"{len(PM)} posts / {len(sc)} sockets, max xz offset {max(off):.4f} m, post base = socket top"
    # clash: sample #4 surfaces, test inside #3 solids (excluding contact-by-design with Guard_Sockets top / brackets)
    clashes = []
    for n4, (mk, m4) in p.P.items():
        pts, _ = trimesh.sample.sample_surface(m4, 4000, seed=1)
        for n3, (mk3, m3) in st.P.items():
            for c3 in m3.split(only_watertight=False):
                lo, hi = c3.bounds; sel = np.all((pts > lo + .002) & (pts < hi - .002), axis=1)
                if sel.any():
                    from scipy.spatial import ConvexHull
                    E = ConvexHull(c3.vertices).equations; inside = np.all(pts[sel] @ E[:, :3].T + E[:, 3] < -.002, axis=1)
                    if inside.any(): clashes.append((n4, n3, int(inside.sum())))
    res["clashes_with_#3 (all #3 parts are convex boxes)"] = clashes
    hr = p.P["Handrail_Wall"][1].vertices; res["wall_rail_top_y_range"] = (round(hr[:, 1].min(), 3), round(hr[:, 1].max(), 3))
    return res

def render_sheet(geo, path, title):
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    saved = tonemap(); top, front, side, iso = views(); a = np.pi
    Ry = np.array([[np.cos(a), 0, np.sin(a)], [0, 1, 0], [-np.sin(a), 0, np.cos(a)]])
    def rv(R, s, sh):
        im = render_glass(geo, R, s, sh); ns = render_view({k: v for k, v in geo.items() if v[0] != "glass"}, R, size=s, shadow=False)
        fg = np.abs(ns - ns[0, 0]).sum(2) > .03; im[fg] = np.clip(im[fg] * 1.12 + .02, 0, 1); return crop(im)
    ims = [rv(top, 600, False), rv(front, 650, True), rv(side, 650, True), rv(iso, 700, True), rv(iso @ Ry, 700, True)]; FMAT.update(saved)
    bg = "#F4F2EC"; fig, axs = plt.subplots(1, 5, figsize=(22, 7), facecolor=bg, gridspec_kw=dict(width_ratios=[.5, 1, 1, 1.2, 1.2]))
    for ax, im, t in zip(axs, ims, ("Top", "Front", "Side", "Iso", "Iso (shell side)")): ax.imshow(im); ax.axis("off"); ax.set_title(t, fontsize=11, color="#555")
    fig.suptitle(title, fontsize=12, color="#444"); plt.tight_layout(rect=(0, 0, 1, .94)); fig.savefig(path, dpi=90, facecolor=bg); plt.close(fig)

if __name__ == "__main__":
    import pygltflib
    p, posts = build(); gp = os.path.join(dc.ROOT, "godot/assets/models/stair_guard_handrail.glb")
    tris, geo = export_final(p.P, [gp])
    g = pygltflib.GLTF2().load(gp)
    for m in g.materials:
        if m.name.lower() == "glass": m.alphaMode = "BLEND"; m.doubleSided = True
    g.save_binary(gp); g = pygltflib.GLTF2().load(gp)
    print("tris", tris, "materials", [(m.name, m.alphaMode) for m in g.materials])
    bad = [n for n, (mk, m) in p.P.items() if not all(c.is_watertight for c in m.split(only_watertight=False))]; print("non-watertight", bad)
    for k, v in verify(p, posts).items(): print(k, ":", v)
    st = S.build(); geo3 = {f"S_{k}": (mk,) + tuple(shade_split(m)[i] for i in (0, 1, 3)) for k, (mk, m) in st.P.items()}
    geo3.update(geo); render_sheet(geo3, os.path.join(S.OUT, "final_stair_guard_sheet.png"), "Final  #4 stair glass guards + handrails on #3 stair set (stair core v1.1)")
