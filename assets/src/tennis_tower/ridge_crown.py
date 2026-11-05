"""Rook: Tennis Tower Glass Box roof ridge crown (spec §3.11.10: faceted crown = two flat planes meeting at a ridge along X at Z 39.5,
one bay each side, peak +26.3; roof modelled flat at top-chord +25.5). Tiles along X with the promoted #55 tt_roof_bay (V4 Branch Diagonals):
20.0 m long, owns the posts/rafters on its -X grid lines (x = 0, 4, 8, 12, 16 in roof-tile coords); ridge / eave members stop 1-3 mm short
of the tile end. Seats on the roof tile's TOP-CHORD NODES at ridge +/- 2.0 m (a roof grid line each side of a mid-bay ridge), so the ridge
must lie on a mid-bay Z of the roof grid (e.g. roof-tile local z 10). Facets: ridge +0.80 over the top chords (+26.3), eave beams at
ridge +/- 4.0 m kept 40 mm above the roof glazing bars (no clipping), slope 6.1°.
REUSE: #55 roof tile node/chord language + Branch Diagonals Y-forks, #70/#65 leaf crests, #55 V1 slate leaf-relief panels, #71 Court Line
(ball finials, amber line), #68/#69 greenery, modlib vine(). No wood, no planter boxes. Glass = BLEND, named Glass. Run: python3 ridge_crown.py"""
from modlib import *
import roof_bay as rb
B, L, YT, RN = rb.B, rb.L, rb.RN + rb.D, rb.RN
PK = YT + .8; EV = 4.0; SLP = (PK - (YT + RN + .2))/EV       # peak local y 3.975 (= +26.3), facet top at eave 3.55
yt = lambda z: PK - SLP*abs(z)                                 # facet top surface
yr = lambda z: yt(z) - .1                                      # rafter centre line
XS = [i*B for i in range(rb.N)]
def huv(P):
    m = trimesh.convex.convex_hull(np.asarray(P, float))
    m.metadata["uv"] = m.vertices[:, [0, 2]] / 2.0 + m.vertices[:, [1, 1]] * [0, .5]; return m
def fhull(xa, xb, z0, z1, s, o0, o1):
    return huv([(x, yt(z) + o, s*z) for x in (xa, xb) for z in (z0, z1) for o in (o0, o1)])
def frame(q):
    F = []; RR = .07
    for x in XS:
        for s in (-1, 1):
            F.append(tube((x, yr(0), 0), (x, yr(EV), s*EV), RR, 8))
            if q.get("branch"):   # Y-fork from the roof node: stem, fork node, two branches up to the rafter (Branch Diagonals echo)
                c = (x, YT + RN + .16, s*2.0); F += [tube((x, YT + RN - E, s*2.0), c, .07, 8), node(c, .09, 0), tube(c, (x, yr(1.0), s*1.0), .055, 6), tube(c, (x, yr(3.0), s*3.0), .055, 6)]
            else: F.append(tube((x, YT + RN - E, s*2.0), (x, yr(2.0), s*2.0), .084, 8))
            F.append(node((x, YT + RN + .1 - E, s*2.0), .1, 0))                 # shoe ball on the roof top-chord node
        F.append(node((x, PK - .13, 0), .09, 0))
    F.append(tube((.001, PK - .13, 0), (L - .093, PK - .13, 0), .08, 10))            # ridge beam (stops short of the next tile's ridge node)
    F += [tube((.001, yr(EV), s*EV), (L - .075, yr(EV), s*EV), RR, 8) for s in (-1, 1)]
    return F
def cover(p, q):
    c = q["cover"]
    if c in ("glass", "slate"):
        panes = [fhull(x + .06, x + B - .06, .16, EV - .08, s, -.03, -.01 if c == "glass" else .0) for x in XS for s in (-1, 1)]
        if c == "glass": p.add("Crown_Glass_Panes", GL, *panes)
        else: p.add("Crown_Slate_Panels", SL, *panes)
        p.add("Crown_Glazing_Caps", G, *[fhull(x - .05, x + .05, .12, EV - .04, s, -.034, .01) for x in XS for s in (-1, 1)])
        p.add("Ridge_Cap", G, huv([(x, y, z) for x in (.001, L - .003) for y, z in ((PK - .034, -.12), (PK - .034, .12), (PK + .03, 0))]))
        return panes
    if c == "louvre":   # open alloy louvres on the rafters, parallel to the ridge (shade, no glass layer)
        p.add("Crown_Louvres", ALY, *[fhull(.001, L - .003, z, z + .18, s, -.034, -.004) for s in (-1, 1) for z in np.arange(.25, EV - .2, .42)])
        return []
def leaf_on(c, n, L_, W, t=.02):  # leaf lying in a facet (normal n), long axis along +X
    Yc = np.array([1., 0, 0]); Zc = n/np.linalg.norm(n); Xc = np.cross(Yc, Zc); R = np.eye(4); R[:3, :3] = np.c_[Xc, Yc, Zc]
    m = leaf((0, 0, 0), L_, W, t=t); m.apply_transform(R); m.apply_translation(np.asarray(c) + Zc*(t - .006)); return m
def build(q):
    p = Part(); p.add("Crown_Frame", q.get("frame", SGM), *frame(q)); panels = cover(p, q); d = q.get("dress")
    top = PK + .03 if q["cover"] != "louvre" else yr(0) + .11
    if d == "crest": p.add("Ridge_Leaf_Crests", LF, *[crest_at((x + B/2, top - .004, 0)) for x in XS])
    if d == "relief":
        Ls = []
        for x in XS:
            for s in (-1, 1):
                z = 2.0; Ls.append(leaf_on((x + .6, yt(z), s*z), np.array([0, 1, s*SLP]), 2.8, 1.1, t=.07))
        p.add("Leaf_Relief", LF, *Ls)
    if d == "court":
        p.add("Ridge_Ball_Finials", BA, *[node((x, top + .07 - E, 0), .07, 0) for x in XS])
        p.add("Ridge_LED_Line", AM, *[fhull(x + .07, x + B - .07, .13, .17, s, -E, .006) for x in XS for s in (-1, 1)])
    if d == "vine":
        st, lv = vine([(.05, top + .012 - E*.5, 0), (5, top + .012 - E*.5, 0), (10, top + .012 - E*.5, 0), (15, top + .012 - E*.5, 0), (L - .05, top + .012 - E*.5, 0)], r=.012, leaf_every=.5, leaf_len=.3, seed=2, outward=True)
        p.add("Ridge_Vine", LF, st); p.add("Ridge_Vine_Leaves", LF2, lv)
    return p
from restroom_extras import crest
def crest_at(c): return xf(crest((0, 0, 0)), R=trimesh.transformations.rotation_matrix(np.pi/2, [0, 1, 0]), t=c)
VARIANTS = [
    dict(label="Leaf Crest Glass: BLEND glass facets, leaf crests along the ridge", cover="glass", dress="crest"),
    dict(label="Branch Ridge: Y-fork branch supports (roof V4 echo), glass facets, vine ridge", cover="glass", dress="vine", branch=True),
    dict(label="Leaf Relief Slate: opaque slate facets with leaf relief (no 2nd BLEND layer)", cover="slate", dress="relief"),
    dict(label="Court Line: slate facets, ball finials, amber ridge lines, alloy frame", cover="slate", dress="court", frame=ALY),
    dict(label="Leaf Louvre: open alloy louvres, leaf crests, branch supports", cover="louvre", dress="crest", branch=True),
]
# ---------- seating check on the promoted roof tile (raw roof coords, ridge on mid-bay z = 10) ----------
ZR = 10.0
def seated(prm, tiles=3, roof_tiles=None):
    roof = rb.build(dict(branch=True)); A = {}
    for k in range(roof_tiles or tiles):
        for n, (mk, m) in roof.P.items():
            if "colonly" in n: continue
            m2 = m.copy(); m2.apply_translation((k*L, 0, 0)); A[f"ROOF{k}_{n}"] = (mk, m2)
    for k in range(tiles):
        c = build(prm)
        for n, (mk, m) in c.P.items():
            if "colonly" in n: continue
            m2 = m.copy(); m2.apply_translation((k*L, 0, ZR)); A[f"CROWN{k}_{n}"] = (mk, m2)
    return A
def seat_check(prm):
    A = seated(prm, 2, 2)
    S = {k: v for k, v in A.items() if k.startswith("CROWN")}
    near = {k: v for k, v in A.items() if k.startswith("ROOF") and v[1].bounds[1][1] > YT - .3}
    chk = cc.check({**S, **near}, n_samp=300)
    bad = [o for o in chk["overlap"] if not o[3] and (o[0].startswith("CROWN") != o[1].startswith("CROWN") or o[0][:6] != o[1][:6])]
    cop = [c for c in chk["coplanar"] if c[0].startswith("CROWN") != c[1].startswith("CROWN") or c[0][:6] != c[1][:6]]
    worst = max([o[2] for o in chk["overlap"] if (o[0].startswith("CROWN") != o[1].startswith("CROWN") or o[0][:6] != o[1][:6])] + [0])
    return dict(worst_cross=round(worst, 4), bad=bad[:4], coplanar=cop[:4], pass_=not bad and not cop)
def sheet(rep):
    rdir = os.path.join(RENDER_OUT, "ridge_crown"); fig, axs = plt.subplots(3, 5, figsize=(28, 15), facecolor="#F4F2EC")
    Ry = lambda el, az: (lambda a, b: np.array([[1, 0, 0], [0, np.cos(b), -np.sin(b)], [0, np.sin(b), np.cos(b)]]) @ np.array([[np.cos(a), 0, np.sin(a)], [0, 1, 0], [-np.sin(a), 0, np.cos(a)]]))(np.radians(az), np.radians(el))
    for i, (prm, r) in enumerate(zip(VARIANTS, rep)):
        p = recenter(build(prm)); _, geo = export_final(p.P, [f"/tmp/rc_{i}.glb"]); geo = {k: v for k, v in geo.items() if "colonly" not in k}
        for row, (el, az) in enumerate(((14, 30), (40, 70))):
            im = crop(render_view(geo, Ry(el, az), size=760, shadow=False, glass_alpha=.35)); axs[row, i].imshow(np.clip(im, 0, 1)); axs[row, i].axis("off")
            plt.imsave(os.path.join(rdir, f"v{i+1}_{['low', 'end'][row]}.png"), np.clip(im, 0, 1))
        A = Part()
        for n, (mk, m) in seated(prm, 3).items():
            if n.startswith("ROOF") and m.bounds[1][1] < 0: continue
            m.metadata["uv"] = np.zeros((len(m.vertices), 2)); A.add(n, mk, m)
        _, g2 = export_final(A.P, [f"/tmp/rcs_{i}.glb"]); im = crop(render_view(g2, Ry(22, 35), size=900, shadow=False, glass_alpha=.35))
        plt.imsave(os.path.join(rdir, f"v{i+1}_seated_3bays.png"), np.clip(im, 0, 1)); axs[2, i].imshow(np.clip(im, 0, 1)); axs[2, i].axis("off")
        sc = r.get("seat", {})
        axs[0, i].set_title(f"v{i+1}  {prm['label'].split(': ')[0]}\n{prm['label'].split(': ')[1]}\n{r['tris']} tris | {'PASS' if r['passed'] else 'FAIL'} | seat {'PASS' if sc.get('pass_') else 'FAIL'} (worst {sc.get('worst_cross')})", fontsize=10, color="#222")
    for row, t in enumerate(("low 3/4 along the ridge", "high 3/4 (facets)", "seated on 3 x tt_roof_bay (V4), 60 m run")): axs[row, 0].text(-.02, .5, t, transform=axs[row, 0].transAxes, rotation=90, va="center", ha="right", fontsize=12)
    fig.suptitle("Rook | Tennis Tower ridge crown V1-V5 | 20 m tile along X, ridge +26.3, eaves +/-4.0 m | candidates (not promoted)", fontsize=15, color="#333")
    plt.tight_layout(rect=(0, 0, 1, .95)); sp = os.path.join(rdir, "ridge_crown_contact_sheet.png"); fig.savefig(sp, dpi=90, facecolor="#F4F2EC"); plt.close(fig); print("SHEET", sp)
def pair_check(prm):  # crown tile + its +X neighbour: no overlap / coplanar across the seam
    A = {}
    for k in range(2):
        for n, (mk, m) in build(prm).P.items():
            m2 = m.copy(); m2.apply_translation((k*L, 0, 0)); A[f"T{k}_{n}"] = (mk, m2)
    near = {k: v for k, v in A.items() if v[1].bounds[1][0] > L - 1 and v[1].bounds[0][0] < L + 1}
    chk = cc.check(near, n_samp=300); bad = [o for o in chk["overlap"] if not o[3] and o[0][:2] != o[1][:2]]; cop = [c for c in chk["coplanar"] if c[0][:2] != c[1][:2]]
    return dict(bad=bad[:3], coplanar=cop[:3], pass_=not bad and not cop)
if __name__ == "__main__":
    rep = run("ridge_crown", build, VARIANTS, title="ridge crown 20 m", view=views()[3], sheet="ridge_crown_run_sheet.png")
    for r, prm in zip(rep, VARIANTS): r["seat"] = seat_check(prm); r["pair"] = pair_check(prm); print("SEAT", r["v"], r["seat"], "PAIR", r["pair"])
    json.dump(rep, open(os.path.join(RENDER_OUT, "ridge_crown", "report.json"), "w"), indent=1, default=str); sheet(rep)
