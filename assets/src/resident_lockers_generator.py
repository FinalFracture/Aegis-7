"""Rev C #24 resident lockers (laundry; one run; 4.8 W x 0.5 D x 2.0 H). Five iterations, family language. Empty (no clothes).
Pivot at the bottom-centre, +Z front, wall at -Z. Spin-down: the run bolts to the wall rail and floor; every door has an amber latch and a green or amber lock light."""
import os, sys, numpy as np, trimesh
sys.path.insert(0, os.path.dirname(__file__))
from hydro_planter_generator import cyl, box, bev, blk, Pod, dc, wg, plt
from dining_chair_generator import export_final
from bath_pod_generator import set_glass_blend
OUT = os.path.join(dc.ROOT, "design/assets/resident_lockers")
W, D, H = 4.8, .5, 2.0; ZB, ZF = -D / 2, D / 2; Y0, Y1 = .08, H - .04
def carcass(p, mat="white", cols=8):
    xs = np.linspace(-W / 2, W / 2, cols + 1)
    p.add("Uprights", mat, *[box(max(x - .012, -W / 2), min(x + .012, W / 2), 0, H, ZB, ZF - .012) for x in xs]); p.add("Top_Panel", mat, box(-W / 2, W / 2, H - .04, H, ZB, ZF - .012))
    p.add("Back_Panel", "slate", box(-W / 2, W / 2, 0, H, ZB, ZB + .015)); p.add("Plinth", "gunmetal", box(-W / 2, W / 2, 0, Y0, ZB, ZF - .04))
    p.add("Wall_Bolts", "alloy", *[cyl(x, ZB + .015, .012, 1.8, 1.82, 6) for x in np.linspace(-2.2, 2.2, 5)]); return xs
def doorgrid(p, xs, rows, mat="white", light=True, vent=False):
    D_, L_, P_, V_ = [], [], [], []
    for i in range(len(xs) - 1):
        r = rows[i] if isinstance(rows, (list, tuple)) else rows; ys = np.linspace(Y0, Y1, r + 1)
        for j in range(r):
            x0, x1, y0, y1 = xs[i] + .015, xs[i + 1] - .015, ys[j] + .008, ys[j + 1] - .008; cx = (x0 + x1) / 2
            D_.append(box(x0, x1, y0, y1, ZF - .03, ZF - .012)); L_.append(box(x1 - .05, x1 - .03, (y0 + y1) / 2 - .05, (y0 + y1) / 2 + .05, ZF - .012, ZF))
            P_.append(box(cx - .05, cx + .05, y1 - .07, y1 - .045, ZF - .012, ZF - .008))
            if vent: V_ += [box(x0 + .06, x1 - .06, y1 - .2 - k * .04, y1 - .185 - k * .04, ZF - .012, ZF - .009) for k in range(3)]
    p.add("Locker_Doors", mat, *D_); p.add("Door_Latches", "amber", *L_); p.add("Number_Plates", "alloy" if not light else "green", *P_)
    if V_: p.add("Vent_Slots", "slate", *V_)

def iter1():  # full height: eight tall white lockers, green lock-light number plates
    p = Pod("Full_Height"); xs = carcass(p); doorgrid(p, xs, 1); return p
def iter2():  # two-tier: sixteen half-height slate doors in a white frame, alloy number plates
    p = Pod("Two_Tier"); xs = carcass(p); doorgrid(p, xs, 2, "slate", light=False); return p
def iter3():  # mixed grid: tall lockers alternate with three-tier cubby columns
    p = Pod("Mixed_Grid"); xs = carcass(p); doorgrid(p, xs, [1, 3, 1, 3, 1, 3, 1, 3]); return p
def iter4():  # vent doors: six wide gunmetal-framed white doors with vent slot bands and green lights
    p = Pod("Vent_Doors"); xs = carcass(p, "alloy", 6); doorgrid(p, xs, 1, vent=True); return p
def iter5():  # bench niche: lockers left and right of an open niche with a latched fold-down seat and hook rail
    p = Pod("Bench_Niche"); xs = carcass(p); p.P.pop("Uprights"); p.add("Uprights", "white", *[box(max(x - .012, -W / 2), min(x + .012, W / 2), 0, H, ZB, ZF - .012) for k, x in enumerate(xs) if k != 4]); doorgrid(p, np.r_[xs[:4]], 2); doorgrid_r = doorgrid; P2 = Pod("tmp"); doorgrid(P2, np.r_[xs[5:]], 2)
    for k, (mk, m) in P2.P.items(): p.P[k + "_R"] = (mk, m)
    n0, n1 = xs[3] + .012, xs[5] - .012; p.add("Niche_Back", "slate", box(n0, n1, Y0, Y1, ZB + .015, ZB + .03))
    p.add("Fold_Seat", "white", blk(n0 + .02, n1 - .02, .42, .46, ZB + .03, ZB + .38, .006, 1)); p.add("Seat_Hinges", "gunmetal", *[box(x - .03, x + .03, .4, .46, ZB + .03, ZB + .06) for x in (n0 + .15, n1 - .15)])
    p.add("Seat_Latch", "amber", box(-.04, .04, .44, .47, ZB + .36, ZB + .38)); p.add("Hook_Rail", "alloy", box(n0 + .05, n1 - .05, 1.55, 1.58, ZB + .03, ZB + .06))
    p.add("Rail_Hooks", "gunmetal", *[box(x - .012, x + .012, 1.5, 1.58, ZB + .06, ZB + .12) for x in np.linspace(n0 + .15, n1 - .15, 4)]); return p

def main():
    os.makedirs(OUT, exist_ok=True); isos = []
    for i, fn in enumerate([iter1, iter2, iter3, iter4, iter5], 1):
        p = fn(); full = dict(p.P); p.P = {k: v for k, v in full.items() if v[0] != "glass"}  # glass hidden in sheet renders (BLEND in glb)
        tris, iso, lo, hi, bad = wg.sheet(p, os.path.join(OUT, f"iter_0{i}_sheet.png"), f"iter_0{i}  {p.name}  (#24 resident lockers (empty))")
        p.P = full; gp = os.path.join(OUT, f"iter_0{i}.glb"); tris, _ = export_final(p.P, [gp]); set_glass_blend(gp)
        isos.append((p.name, iso)); print(i, p.name, tris, (hi - lo).round(3), "bad", bad)
    fig, axs = plt.subplots(3, 2, figsize=(16, 12), facecolor="#F4F2EC")
    for ax in axs.flat: ax.axis("off")
    for ax, (i, (n, im)) in zip(axs.flat, enumerate(isos, 1)): ax.imshow(im); ax.set_title(f"{i}. {n}", fontsize=11, color="#555")
    plt.tight_layout(rect=(0, 0, 1, .97)); fig.savefig(os.path.join(OUT, "overview.png"), dpi=90, facecolor="#F4F2EC"); plt.close(fig)
def final_niche():
    """Standalone locker run (Jared, Oct 29): not in the apartment building or tied to laundry; building TBD."""
    p = iter5(); p.name = "Locker_Run_Bench_Niche"; xs = np.linspace(-W / 2, W / 2, 9); n0, n1 = xs[3] + .012, xs[5] - .012
    p.add("End_Panels", "alloy", *[box(x0, x1, 0, H, ZB, ZF - .006) for x0, x1 in ((-W / 2, -W / 2 + .02), (W / 2 - .02, W / 2))])
    p.add("Top_Trim", "alloy", box(-W / 2, W / 2, H - .045, H - .035, ZF - .02, ZF - .006))
    p.add("Niche_Light", "amber", box(n0 + .05, n1 - .05, Y1 - .03, Y1 - .02, ZB + .03, ZB + .2))
    p.add("Seat_Pad", "slate", bev(n1 - n0 - .08, .3, .46, .48, .03, .006, 1, (n0 + n1) / 2, ZB + .2))
    p.add("Niche_Floor_Tray", "gunmetal", box(n0, n1, Y0 - .01, Y0, ZB + .015, ZF - .04))
    p.add("Floor_Bolts", "alloy", *[cyl(x, ZF - .07, .01, Y0, Y0 + .008, 6) for x in (-2.1, -1.0, 1.0, 2.1)])
    return p
def final_main():
    p = final_niche(); gp = os.path.join(dc.ROOT, "godot/assets/models/locker_run_bench_niche.glb"); tris, geo = export_final(p.P, [gp])
    V = np.vstack([g[1] for g in geo.values()]); bad = [n for n, (mk, m) in p.P.items() if not all(c.is_watertight for c in m.split(only_watertight=False))]
    print("tris", tris, "size", (V.max(0) - V.min(0)).round(3), "bad", bad)
    sp = os.path.join(OUT, "final_bench_niche_sheet.png"); wg.sheet(p, sp, "Final  locker run, Bench Niche (standalone, building TBD; empty)"); os.remove(sp.replace("_sheet.png", ".glb"))
if __name__ == "__main__":
    final_main() if len(sys.argv) > 1 and sys.argv[1] == "final" else main()
