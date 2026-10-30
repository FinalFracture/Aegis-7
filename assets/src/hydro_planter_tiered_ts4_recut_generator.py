"""Rook (Oct 30, Jared 1:32 PM CT): clip-clean re-cut of the approved TS-4 Tiered Steps exterior planter
(godot/assets/models/hydro_planter_tiered_exterior.glb, same file name). Same 4.0 x 0.40 footprint, 3 stepped tiers, 7/5/4 plants,
6 levelling feet with 2 bolts each, front reservoir. TS-2 construction: the troughs are contiguous depth bands with 2 mm reveals (no overlap),
lids embedded 4 mm and kept inside their own band (clear of the next tier), amber latches on each trough front, net cups on the lids,
foliage in the cups, reservoir embedded into the front trough and its seal offset 1.5 mm.
Original backed up to design/assets/hydro_planter_tiered_ts4/hydro_planter_tiered_exterior_pre_recut.glb.
Run: python3 hydro_planter_tiered_ts4_recut_generator.py"""
import os, sys, json, numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import ext_street_furniture_generator as sf, ext_memorial_hydro_generator as mh, hydro_planter_generator as hp, ext_clip_check as cc
from ext_street_furniture_generator import E, box, blk, Pod, export_final, set_glass_blend, views, render_view, crop, plt
from hydro_planter_generator import bev
ROOT = sf.ROOT; OUT = os.path.join(ROOT, "design/assets/hydro_planter_tiered_ts4"); GP = os.path.join(ROOT, "godot/assets/models/hydro_planter_tiered_exterior.glb")
def recut():
    p = Pod("Tiered_Steps_Exterior"); FT = .06; W = 4.0; rng = np.random.default_rng(404)
    p.add("Base_Frame", "gunmetal", blk(-W / 2 + .05, W / 2 - .05, FT - .03, FT, -.19, .19, .006, 1))
    bands = ((.2, .061, .2), (.36, -.059, .059), (.52, -.2, -.061))
    for i, (y, z0, z1) in enumerate(bands):
        yy = y + FT; z = (z0 + z1) / 2; d = z1 - z0
        p.add("Tiers", "white", bev(W, d, FT - E, yy, .03, .01, 2, 0, z))
        p.add("Tier_Lids", "slate", box(-W / 2 + .04, W / 2 - .04, yy - E, yy + .012, z - d / 2 + .01, z + d / 2 - .01))
        p.add("Tier_Latches", "amber", *[box(x - .02, x + .02, yy - .035, yy - .02, z1 - E, z1 + .006) for x in (-1.5, 0, 1.5)])
        xs = np.linspace(-1.75, 1.75, (7, 5, 4)[i])
        p.add("Net_Cup_Clips", "gunmetal", *[hp.cyl(x, z, .035, yy + .012 - E, yy + .03, 6) for x in xs])
        for k, x in enumerate(xs): p.add("Foliage" if k % 2 == 0 else "Foliage_Light", "leaf" if k % 2 == 0 else "leaf2", mh._bush(x, yy + .03 - .0012, z, .065 * (.9 + .2 * rng.random()), rng))
    p.add("Reservoir", "slate", box(-1.9, 1.9, FT + .02, FT + .14, .2 - E, .206))
    p.add("Reservoir_Seal", "alloy", box(-1.895, 1.895, FT + .14 - E, FT + .15, .2 - E + .0015, .2045))
    feet = [(x, z) for x in (-1.75, 0, 1.75) for z in (-.14, .14)]
    p.add("Levelling_Jacks", "alloy", *[hp.cyl(x, z, .018, .02 - E, FT - .03 + E, 8) for x, z in feet])
    p.add("Clamp_Shoes", "gunmetal", *[box(x - .06, x + .06, 0, .02, z - .045, z + .045) for x, z in feet])
    p.add("Shoe_Bolts_Hardware", "alloy", *[hp.cyl(x + dx, z, .008, .02 - E, .028, 6) for x, z in feet for dx in (-.04, .04)])
    return p
def summ(c): return dict(pass_=c["pass"], worst=c["worst_overlap"], over=len([o for o in c["overlap"] if not o[3]]), coplanar=len(c["coplanar"]), open=len(c["open"]), size=c["size"], pivot=c["pivot"])
if __name__ == "__main__":
    old = hp.final_tiered(); c_old = cc.check(old.P); t_old, g_old = export_final(old.P, ["/tmp/_ts4_old.glb"])
    new = recut(); c_new = cc.check(new.P); t_new, g_new = export_final(new.P, [GP]); set_glass_blend(GP)
    rep = dict(before=dict(tris=t_old, **summ(c_old), overlaps=[o[:3] for o in c_old["overlap"] if not o[3]][:20], coplanar_pairs=c_old["coplanar"][:20]),
               after=dict(tris=t_new, **summ(c_new), overlaps=[o[:3] for o in c_new["overlap"] if not o[3]], coplanar_pairs=c_new["coplanar"], open_parts=c_new["open"]))
    print(json.dumps(rep, default=str)); json.dump(rep, open(os.path.join(OUT, "ts4_recut_report.json"), "w"), indent=1, default=str)
    top, front, side, iso = views()
    def sub(g, x0): return {k: v for k, v in g.items()} if x0 is None else sf.headgeo({k: (mk, V * [-1, 1, 1], N * [-1, 1, 1], F[:, ::-1]) for k, (mk, V, N, F) in g.items()}, -9) if False else {k: (mk, V[u], N[u], inv.reshape(-1, 3)) for k, (mk, V, N, F) in g.items() for keep in [F[(V[F][:, :, 0] >= x0).all(1)]] if len(keep) for u, inv in [np.unique(keep, return_inverse=True)]}
    import trimesh
    def cutgeo(pod):
        q = Pod("cut")
        for k, (mk, m) in pod.P.items():
            if m.bounds[1][0] < 1.2: continue
            c = m.copy(); c.vertices[:, 0] = np.maximum(c.vertices[:, 0], 1.2)  # clamp = planar section cap at x 1.2
            if len(c.faces): c.metadata["uv"] = np.zeros((len(c.vertices), 2)); q.P[k] = (mk, c)
        return export_final(q.P, ["/tmp/_ts4_cut.glb"])[1]
    def Ry(a): a = np.radians(a); return np.array([[np.cos(a), 0, np.sin(a)], [0, 1, 0], [-np.sin(a), 0, np.cos(a)]])
    def Rx(b): b = np.radians(b); return np.array([[1, 0, 0], [0, np.cos(b), -np.sin(b)], [0, np.sin(b), np.cos(b)]])
    lab = lambda t, r: f"{t}: {r['tris']} tris | clip {'PASS' if r['pass_'] else 'FAIL'} | worst overlap {r['worst']:.3f} m | {r['over']} overlaps > tol | {r['coplanar']} coplanar"
    fig, axs = plt.subplots(2, 3, figsize=(24, 11), facecolor="#F4F2EC")
    for row, (t, g, r) in enumerate((("BEFORE (approved TS-4)", g_old, rep["before"]), ("AFTER (re-cut)", g_new, rep["after"]))):
        for ax, (st, gg, Rm) in zip(axs[row], (("iso", g, iso), ("trough/lid joints, right end (side 3/4)", cutgeo(old if g is g_old else new), Rx(15) @ Ry(70)), ("lid + latch close-up (front, x > 1.2 section)", cutgeo(old if g is g_old else new), Rx(12) @ Ry(12)))):
            ax.imshow(crop(render_view(gg, Rm, size=600, shadow=gg is g))); ax.axis("off"); ax.set_title(f"{t} - {st}", fontsize=11, color="#333")
        axs[row][0].text(0, -.08, lab(t, r), transform=axs[row][0].transAxes, fontsize=11, color="#a00" if not r["pass_"] else "#060")
    fig.suptitle("Rook  hydro_planter_tiered_exterior (TS-4) re-cut  |  before vs after, TS-2 construction, same 4.0 x 0.40 footprint", fontsize=14, color="#444")
    plt.tight_layout(rect=(0, .02, 1, .95)); sp = os.path.join(OUT, "ts4_recut_before_after_sheet.png"); fig.savefig(sp, dpi=90, facecolor="#F4F2EC"); print("sheet", sp)
