"""Rev C #18 window reading nook bench (room 203; qty 1; 4.0 W x 0.4 D x 0.5 H). Five iterations, family language.
Runs under the 203 window. Pivot at the bottom-centre, +Z front, wall at -Z. Spin-down: the bench bolts to the wall rail and floor; cushions snap to amber clip strips and the drawers latch."""
import os, sys, numpy as np, trimesh
sys.path.insert(0, os.path.dirname(__file__))
from hydro_planter_generator import cyl, box, bev, blk, Pod, dc, wg, plt
from dining_chair_generator import export_final
from bath_pod_generator import set_glass_blend
OUT = os.path.join(dc.ROOT, "design/assets/reading_bench")
W, D, H = 4.0, .4, .5; ZB, ZF = -D / 2, D / 2; SEAT = .42
def seat(p, mat="white", t=.04, y=SEAT):
    p.add("Seat_Slab", mat, blk(-W / 2, W / 2, y - t, y, ZB, ZF, .008, 1))
def cushions(p, n=3, mat="slate"):
    w = (W - .1) / n; p.add("Cushions", mat, *[bev(w - .03, D - .06, SEAT, H - .0, .04, .01, 2, -W / 2 + .05 + w * (i + .5), .01) for i in range(n)])
    p.add("Cushion_Clips", "amber", *[box(-W / 2 + .05 + w * (i + .5) - .05, -W / 2 + .05 + w * (i + .5) + .05, SEAT + .005, SEAT + .02, ZF - .025, ZF - .015) for i in range(n)])
def wall_rail(p):
    p.add("Wall_Rail", "gunmetal", blk(-W / 2, W / 2, .28, .34, ZB, ZB + .02, .004, 1)); p.add("Rail_Bolts", "alloy", *[cyl(x, ZB + .02, .01, .3, .32, 6) for x in np.linspace(-1.8, 1.8, 7)])
def bolster(p, mat="violet"):
    p.add("Back_Bolster", mat, *[bev(1.2, .1, SEAT, H, .04, .008, 2, x, ZB + .06) for x in (-1.3, 0, 1.3)])

def iter1():  # cushion slab: white slab on four gunmetal brackets, slate cushions, violet back bolsters
    p = Pod("Cushion_Slab"); wall_rail(p); seat(p)
    p.add("Brackets", "gunmetal", *[blk(x - .03, x + .03, 0, SEAT - .04, ZB, ZB + .3, .004, 1) for x in (-1.9, -.65, .65, 1.9)]); p.add("Floor_Plates", "alloy", *[box(x - .05, x + .05, 0, .01, ZB, ZB + .32) for x in (-1.9, -.65, .65, 1.9)])
    cushions(p); bolster(p); return p
def iter2():  # storage drawers: closed white plinth with six wide drawers, amber latching pulls
    p = Pod("Storage_Drawers"); wall_rail(p); p.add("Plinth", "white", blk(-W / 2, W / 2, .02, SEAT - .04, ZB, ZF - .01, .008, 1)); p.add("Toe_Kick", "gunmetal", box(-W / 2 + .02, W / 2 - .02, 0, .02, ZB, ZF - .04)); seat(p, "alloy", .03)
    xs = np.linspace(-W / 2, W / 2, 7); p.add("Drawer_Fronts", "slate", *[box(xs[i] + .015, xs[i + 1] - .015, .06, SEAT - .07, ZF - .022, ZF - .012) for i in range(6)])
    p.add("Drawer_Pulls", "amber", *[box((xs[i] + xs[i + 1]) / 2 - .08, (xs[i] + xs[i + 1]) / 2 + .08, .27, .29, ZF - .012, ZF) for i in range(6)]); cushions(p, 2); return p
def iter3():  # book cubbies: open cubby grid under the seat, book blocks held by gunmetal retainer bars
    p = Pod("Book_Cubbies"); wall_rail(p); seat(p); xs = np.linspace(-W / 2, W / 2, 9)
    p.add("Cubby_Dividers", "white", *[box(max(x - .015, -W / 2), min(x + .015, W / 2), 0, SEAT - .04, ZB, ZF) for x in xs]); p.add("Cubby_Floor", "white", box(-W / 2, W / 2, 0, .03, ZB, ZF)); p.add("Cubby_Back", "white", box(-W / 2, W / 2, .03, SEAT - .04, ZB, ZB + .015))
    cols = ("violet", "green", "amber", "slate"); [p.add(f"Books_{k}", cols[k], *[box(xs[i] + .04 + j * .06, xs[i] + .09 + j * .06, .03, .25 + .03 * ((i + j) % 3), ZB + .03, ZB + .25) for i in range(8) for j in range(4) if (i + j) % 4 == k]) for k in range(4)]
    p.add("Retainer_Bars", "gunmetal", *[box(xs[i] + .02, xs[i + 1] - .02, .18, .2, ZF - .02, ZF) for i in range(8)]); cushions(p, 4, "white"); return p
def iter4():  # floating cantilever: wall-hung slab on the rail with a green underglow strip, free floor below
    p = Pod("Floating_Cantilever"); p.add("Wall_Rail", "gunmetal", blk(-W / 2, W / 2, 0, .38, ZB, ZB + .03, .004, 1)); seat(p, "white", .06)
    p.add("Hidden_Brackets", "gunmetal", *[box(x - .02, x + .02, .3, SEAT - .06, ZB, ZB + .3) for x in np.linspace(-1.8, 1.8, 5)]); p.add("Underglow", "green", box(-W / 2 + .05, W / 2 - .05, SEAT - .065, SEAT - .06, ZF - .04, ZF - .02))
    cushions(p, 4); bolster(p, "slate"); return p
def iter5():  # segmented pads with flip tables: three seat pads separated by two flip-up alloy side tables with amber locks
    p = Pod("Flip_Tables"); wall_rail(p); seat(p, "slate"); p.add("Plinth", "white", blk(-W / 2, W / 2, 0, SEAT - .04, ZB, ZF - .03, .008, 1))
    p.add("Seat_Pads", "white", *[bev(1.05, D - .06, SEAT, H, .04, .01, 2, x, .01) for x in (-1.4, 0, 1.4)])
    p.add("Flip_Tables", "alloy", *[box(x - .14, x + .14, SEAT, SEAT + .03, ZB + .02, ZF - .02) for x in (-.7, .7)]); p.add("Table_Hinges", "gunmetal", *[cyl(x, ZB + .03, .012, SEAT, SEAT + .03, 8) for x in (-.8, -.6, .6, .8)])
    p.add("Table_Locks", "amber", *[box(x - .02, x + .02, SEAT + .03, SEAT + .04, ZF - .05, ZF - .03) for x in (-.7, .7)]); return p

def main():
    os.makedirs(OUT, exist_ok=True); isos = []
    for i, fn in enumerate([iter1, iter2, iter3, iter4, iter5], 1):
        p = fn(); full = dict(p.P); p.P = {k: v for k, v in full.items() if v[0] != "glass"}  # glass hidden in sheet renders (BLEND in glb)
        tris, iso, lo, hi, bad = wg.sheet(p, os.path.join(OUT, f"iter_0{i}_sheet.png"), f"iter_0{i}  {p.name}  (#18 window reading nook bench)")
        p.P = full; gp = os.path.join(OUT, f"iter_0{i}.glb"); tris, _ = export_final(p.P, [gp]); set_glass_blend(gp)
        isos.append((p.name, iso)); print(i, p.name, tris, (hi - lo).round(3), "bad", bad)
    fig, axs = plt.subplots(3, 2, figsize=(16, 12), facecolor="#F4F2EC")
    for ax in axs.flat: ax.axis("off")
    for ax, (i, (n, im)) in zip(axs.flat, enumerate(isos, 1)): ax.imshow(im); ax.set_title(f"{i}. {n}", fontsize=11, color="#555")
    plt.tight_layout(rect=(0, 0, 1, .97)); fig.savefig(os.path.join(OUT, "overview.png"), dpi=90, facecolor="#F4F2EC"); plt.close(fig)
if __name__ == "__main__": main()
