"""Rev C #39 Laundry bench (Laundry; qty 1; 1.2 W x 0.4 D x 0.45 H). Five iterations in the family language.
Empty: no laundry, clothes or shoes modeled. Pivot at the bottom-centre, +Z front, wall at -Z.
Spin-down: the bench bolts to the floor or wall rail; every lid, bin and flap latches with amber catches."""
import os, sys, numpy as np, trimesh
sys.path.insert(0, os.path.dirname(__file__))
from hydro_planter_generator import cyl, box, bev, blk, Pod, dc, wg, plt
from dining_chair_generator import export_final
from bath_pod_generator import set_glass_blend
OUT = os.path.join(dc.ROOT, "design/assets/laundry_bench")
W, D, H = 1.2, .4, .45; X0, X1, ZB, ZF = -W / 2, W / 2, -D / 2, D / 2; ST = .04
def feet(p, xs=(-W / 2 + .06, W / 2 - .06), zs=(ZB + .05, ZF - .05)):
    p.add("Floor_Bolts", "amber", *[cyl(x, z, .012, 0, .008, 6) for x in xs for z in zs])
def iter1():  # slatted rail bench: gunmetal sled-leg frames, white seat slats, a low alloy stretcher
    p = Pod("Slatted_Rail_Bench"); n = 5; zs = np.linspace(ZB, ZF, n + 1)
    p.add("Seat_Slats", "white", *[blk(X0, X1, H - ST, H, zs[i] + .006, zs[i + 1] - .006, .005, 1) for i in range(n)])
    for x in (X0 + .08, X1 - .08):
        p.add("Sled_Legs", "gunmetal", box(x - .02, x + .02, .02, H - ST, ZB + .03, ZB + .07), box(x - .02, x + .02, .02, H - ST, ZF - .07, ZF - .03),
              box(x - .02, x + .02, 0, .03, ZB + .02, ZF - .02), box(x - .02, x + .02, H - ST - .03, H - ST, ZB + .02, ZF - .02))
    p.add("Stretcher", "alloy", box(X0 + .1, X1 - .1, .14, .17, -.015, .015)); p.add("Floor_Bolts", "amber", *[cyl(x, z, .01, 0, .034, 6) for x in (X0 + .08, X1 - .08) for z in (ZB + .045, ZF - .045)])
    return p
def iter2():  # storage box bench: closed white carcass, slate padded lift lid, two amber lid latches and a gunmetal plinth
    p = Pod("Storage_Box_Bench"); p.add("Plinth", "gunmetal", box(X0 + .02, X1 - .02, 0, .05, ZB + .02, ZF - .03))
    p.add("Carcass", "white", blk(X0, X1, .05, H - .06, ZB, ZF, .006, 1)); p.add("Lid_Pad", "slate", blk(X0 + .005, X1 - .005, H - .06, H, ZB + .005, ZF - .005, .015, 2))
    p.add("Lid_Hinge_Bar", "alloy", box(X0 + .05, X1 - .05, H - .07, H - .055, ZB - .006, ZB)); p.add("Lid_Latches", "amber", *[box(x - .035, x + .035, H - .09, H - .065, ZF, ZF + .006) for x in (-W / 4, W / 4)])
    p.add("Front_Panel_Lines", "alloy", *[box(x - .003, x + .003, .07, H - .1, ZF, ZF + .003) for x in (-W / 6, W / 6)]); feet(p); return p
def iter3():  # wall-hung flip seat: seat on a gunmetal wall rail with two diagonal stays, open floor below, seat flips up to the rail
    p = Pod("Wall_Flip_Seat"); p.add("Wall_Rail", "gunmetal", blk(X0, X1, 0, H + .25, ZB, ZB + .03, .004, 1))
    p.add("Seat", "white", blk(X0 + .02, X1 - .02, H - ST, H, ZB + .045, ZF, .008, 1)); p.add("Seat_Hinge", "alloy", box(X0 + .02, X1 - .02, H - ST - .02, H - ST, ZB + .03, ZB + .05))
    St = []
    for x in (X0 + .12, X1 - .12):
        for k in range(6): t0, t1 = k / 6, (k + 1) / 6; St.append(box(x - .012, x + .012, .12 + (H - ST - .12) * t0, .12 + (H - ST - .12) * t1, ZB + .03, ZB + .03 + (ZF - .06 - ZB - .03) * t1))
    p.add("Diagonal_Stays", "gunmetal", *St); p.add("Flip_Catches", "amber", *[box(x - .03, x + .03, H + .17, H + .2, ZB + .03, ZB + .045) for x in (-W / 4, W / 4)])
    p.add("Rail_Bolts", "alloy", *[cyl(x, ZB + .03, .01, y, y + .012, 6) for x in (X0 + .1, 0, X1 - .1) for y in (.08, H + .18)]); return p
def iter4():  # shoe cubby bench: seat over three open cubbies with a slate back and alloy-lipped floor shelf (empty)
    p = Pod("Cubby_Bench"); xs = np.linspace(X0, X1, 4)
    p.add("Seat_Top", "white", blk(X0, X1, H - ST, H, ZB, ZF, .008, 1)); p.add("Plinth", "gunmetal", box(X0 + .02, X1 - .02, 0, .04, ZB + .02, ZF - .04))
    p.add("Uprights", "white", *[box(max(x - .012, X0), min(x + .012, X1), .04, H - ST, ZB, ZF - .01) for x in xs]); p.add("Back_Panel", "slate", box(X0, X1, .04, H - ST, ZB, ZB + .015))
    p.add("Cubby_Floor", "white", box(X0, X1, .04, .06, ZB, ZF - .01)); p.add("Mid_Shelf", "alloy", *[box(xs[i] + .012, xs[i + 1] - .012, .22, .235, ZB + .015, ZF - .03) for i in range(3)])
    p.add("Shelf_Lips", "alloy", *[box(xs[i] + .012, xs[i + 1] - .012, .06, .09, ZF - .03, ZF - .015) for i in range(3)]); feet(p); return p
def iter5():  # padded bench with basket shelf: violet cushion on an alloy tray, gunmetal four-leg frame, lower lipped shelf with amber tie-down cleats
    p = Pod("Padded_Shelf_Bench"); lx, lz = (X0 + .04, X1 - .04), (ZB + .04, ZF - .04)
    p.add("Legs", "gunmetal", *[box(x - .02, x + .02, 0, H - .07, z - .02, z + .02) for x in lx for z in lz]); p.add("Seat_Tray", "alloy", box(X0, X1, H - .08, H - .06, ZB, ZF))
    p.add("Cushion", "violet", blk(X0 + .01, X1 - .01, H - .06, H, ZB + .01, ZF - .01, .02, 2)); p.add("Lower_Shelf", "alloy", box(X0 + .02, X1 - .02, .1, .12, ZB + .02, ZF - .02))
    p.add("Shelf_Lip", "alloy", box(X0 + .02, X1 - .02, .12, .15, ZF - .03, ZF - .02), box(X0 + .02, X1 - .02, .12, .15, ZB + .02, ZB + .03))
    p.add("Tie_Down_Cleats", "amber", *[box(x - .02, x + .02, .12, .135, -.015, .015) for x in (-W / 4, W / 4)]); feet(p, lx, lz); return p
def main():
    os.makedirs(OUT, exist_ok=True); isos = []
    for i, fn in enumerate([iter1, iter2, iter3, iter4, iter5], 1):
        p = fn(); full = dict(p.P); p.P = {k: v for k, v in full.items() if v[0] != "glass"}  # glass hidden in sheet renders (BLEND in glb)
        tris, iso, lo, hi, bad = wg.sheet(p, os.path.join(OUT, f"iter_0{i}_sheet.png"), f"iter_0{i}  {p.name}  (#39 laundry bench)")
        p.P = full; gp = os.path.join(OUT, f"iter_0{i}.glb"); tris, _ = export_final(p.P, [gp]); set_glass_blend(gp)
        isos.append((p.name, iso)); print(i, p.name, tris, (hi - lo).round(3), "bad", bad)
    fig, axs = plt.subplots(3, 2, figsize=(16, 12), facecolor="#F4F2EC")
    for ax in axs.flat: ax.axis("off")
    for ax, (i, (n, im)) in zip(axs.flat, enumerate(isos, 1)): ax.imshow(im); ax.set_title(f"{i}. {n}", fontsize=11, color="#555")
    plt.tight_layout(rect=(0, 0, 1, .97)); fig.savefig(os.path.join(OUT, "overview.png"), dpi=90, facecolor="#F4F2EC"); plt.close(fig)
if __name__ == "__main__": main()
