"""Rev C #38 folding counter (Laundry; qty 2: a 3.5 m run and a 3.0 m run (C.2a, N wall); 0.6 D x 0.9 H). Five iterations, family language, shown at 3.5 m.
The run length is a parameter, so the final exports both lengths. Empty: no laundry or clothes modeled. Pivot at the bottom-centre, +Z front, wall at -Z.
Spin-down: the counter bolts to the wall rail and floor; every door, drawer, basket and bin latches with amber catches."""
import os, sys, numpy as np, trimesh
sys.path.insert(0, os.path.dirname(__file__))
from hydro_planter_generator import cyl, box, bev, blk, Pod, dc, wg, plt
from dining_chair_generator import export_final
from bath_pod_generator import set_glass_blend
OUT = os.path.join(dc.ROOT, "design/assets/folding_counter")
D, H = .6, .9; ZB, ZF = -D / 2, D / 2; TOP = .04
def top(p, L, mat="white"):
    p.add("Worktop", mat, blk(-L / 2, L / 2, H - TOP, H, ZB, ZF, .008, 1)); p.add("Worktop_Nosing", "alloy", box(-L / 2, L / 2, H - TOP - .005, H - .005, ZF - .008, ZF))
    p.add("Wall_Rail", "gunmetal", blk(-L / 2, L / 2, H - .14, H - TOP, ZB, ZB + .02, .004, 1)); p.add("Rail_Bolts", "alloy", *[cyl(x, ZB + .02, .01, H - .1, H - .09, 6) for x in np.linspace(-L / 2 + .2, L / 2 - .2, int(L / .7) + 1)])
def bays(L, w=.6):
    n = max(1, int(round(L / w))); return np.linspace(-L / 2, L / 2, n + 1)
def carcass(p, L, xs, mat="white"):
    p.add("Uprights", mat, *[box(max(x - .012, -L / 2), min(x + .012, L / 2), 0, H - TOP, ZB, ZF - .03) for x in xs]); p.add("Plinth", "gunmetal", box(-L / 2, L / 2, 0, .08, ZB, ZF - .06))
    p.add("Bottom_Panel", mat, box(-L / 2, L / 2, .08, .1, ZB, ZF - .03)); p.add("Back_Panel", "slate", box(-L / 2, L / 2, .08, H - TOP, ZB, ZB + .015))
def fronts(p, xs, rows, mat, pull="amber"):
    F, Pl = [], []
    for i in range(len(xs) - 1):
        r = rows[i % len(rows)]; ys = np.linspace(.1, H - TOP - .01, r + 1)
        for j in range(r):
            x0, x1 = xs[i] + .015, xs[i + 1] - .015; F.append(box(x0, x1, ys[j] + .006, ys[j + 1] - .006, ZF - .03, ZF - .012)); c = (x0 + x1) / 2
            Pl.append(box(c - .08, c + .08, ys[j + 1] - .05, ys[j + 1] - .035, ZF - .012, ZF))
    p.add("Fronts", mat, *F); p.add("Pull_Latches", pull, *Pl)
L0 = 3.5
def iter1(L=L0):  # open base: worktop on gunmetal leg frames, two open alloy shelves with lips (baskets go here later)
    p = Pod("Open_Base"); top(p, L); xs = bays(L, .9)
    p.add("Leg_Frames", "gunmetal", *[box(max(x - .02, -L / 2), min(x + .02, L / 2), 0, H - TOP, z - .02, z + .02) for x in xs for z in (ZB + .04, ZF - .06)])
    p.add("Open_Shelves", "alloy", *[box(-L / 2, L / 2, y, y + .02, ZB + .02, ZF - .06) for y in (.12, .45)]); p.add("Shelf_Lips", "gunmetal", *[box(-L / 2, L / 2, y + .02, y + .05, ZF - .07, ZF - .06) for y in (.12, .45)])
    p.add("Foot_Clamps", "amber", *[box(max(x - .02, -L / 2), min(x + .02, L / 2), 0, .02, ZF - .04, ZF - .02) for x in xs]); return p
def iter2(L=L0):  # cabinet base: closed white bays, alternating door and three-drawer columns, slate fronts
    p = Pod("Cabinet_Base"); top(p, L); xs = bays(L); carcass(p, L, xs); fronts(p, xs, [1, 3], "slate"); return p
def iter3(L=L0):  # fold-down leaf: wall-hung counter with a front leaf that folds up to widen the folding surface; open floor below
    p = Pod("Fold_Down_Leaf"); p.add("Worktop", "white", blk(-L / 2, L / 2, H - TOP, H, ZB, ZF - .2, .008, 1)); p.add("Wall_Rail", "gunmetal", blk(-L / 2, L / 2, 0, H - TOP, ZB, ZB + .03, .004, 1))
    p.add("Fold_Leaf", "white", box(-L / 2 + .01, L / 2 - .01, H - TOP - .4, H - TOP - .01, ZF - .23, ZF - .2)); p.add("Leaf_Hinge_Bar", "alloy", box(-L / 2, L / 2, H - TOP - .02, H - TOP, ZF - .22, ZF - .19))
    p.add("Cantilever_Brackets", "gunmetal", *[box(x - .015, x + .015, H - .22, H - TOP, ZB + .03, ZF - .25) for x in np.linspace(-L / 2 + .2, L / 2 - .2, 5)]); p.add("Leaf_Latches", "amber", *[box(x - .03, x + .03, H - TOP - .41, H - TOP - .39, ZF - .2, ZF - .19) for x in (-L / 4, L / 4)])
    p.add("Support_Struts_Stowed", "alloy", *[box(x - .01, x + .01, H - TOP - .38, H - TOP - .05, ZF - .25, ZF - .235) for x in (-L / 3, 0, L / 3)]); return p
def iter4(L=L0):  # basket bays: open bays with pull-out alloy wire baskets (empty) on runners, amber basket latches
    p = Pod("Basket_Bays"); top(p, L); xs = bays(L); carcass(p, L, xs); B, R, Lt = [], [], []
    for i in range(len(xs) - 1):
        x0, x1 = xs[i] + .03, xs[i + 1] - .03
        for y in (.12, .45):
            B += [box(x0, x1, y, y + .012, ZB + .04, ZF - .05), box(x0, x1, y, y + .25, ZF - .062, ZF - .05), box(x0, x1, y, y + .25, ZB + .04, ZB + .052), box(x0, x0 + .012, y, y + .25, ZB + .04, ZF - .05), box(x1 - .012, x1, y, y + .25, ZB + .04, ZF - .05)]
            R += [box(x0 - .018, x0, y + .1, y + .115, ZB + .04, ZF - .05), box(x1, x1 + .018, y + .1, y + .115, ZB + .04, ZF - .05)]; Lt.append(box((x0 + x1) / 2 - .05, (x0 + x1) / 2 + .05, y + .2, y + .23, ZF - .05, ZF - .04))
    p.add("Wire_Baskets", "alloy", *B); p.add("Basket_Runners", "gunmetal", *R); p.add("Basket_Latches", "amber", *Lt); return p
def iter5(L=L0):  # sorting bins: tilt-out sorting bins (violet, green, amber tags) across the run, a drawer row above them
    p = Pod("Sorting_Bins"); top(p, L); xs = bays(L); carcass(p, L, xs)
    F, T, Pl = [], [], []; cols = ("violet", "green", "amber")
    for i in range(len(xs) - 1):
        x0, x1 = xs[i] + .015, xs[i + 1] - .015; c = (x0 + x1) / 2
        F.append(box(x0, x1, .1, .62, ZF - .03, ZF - .012)); F.append(box(x0, x1, .63, H - TOP - .01, ZF - .03, ZF - .012))
        T.append((cols[i % 3], box(c - .06, c + .06, .52, .56, ZF - .012, ZF - .006))); Pl += [box(c - .1, c + .1, .58, .6, ZF - .012, ZF), box(c - .08, c + .08, H - TOP - .06, H - TOP - .045, ZF - .012, ZF)]
    p.add("Bin_Fronts", "white", *F); p.add("Pull_Latches", "amber", *Pl)
    for k in cols: p.add(f"Sort_Tag_{k}", k, *[m for c, m in T if c == k])
    return p

def main():
    os.makedirs(OUT, exist_ok=True); isos = []
    for i, fn in enumerate([iter1, iter2, iter3, iter4, iter5], 1):
        p = fn(); full = dict(p.P); p.P = {k: v for k, v in full.items() if v[0] != "glass"}  # glass hidden in sheet renders (BLEND in glb)
        tris, iso, lo, hi, bad = wg.sheet(p, os.path.join(OUT, f"iter_0{i}_sheet.png"), f"iter_0{i}  {p.name}  (#38 folding counter (3.5 m run shown))")
        p.P = full; gp = os.path.join(OUT, f"iter_0{i}.glb"); tris, _ = export_final(p.P, [gp]); set_glass_blend(gp)
        isos.append((p.name, iso)); print(i, p.name, tris, (hi - lo).round(3), "bad", bad)
    fig, axs = plt.subplots(3, 2, figsize=(16, 12), facecolor="#F4F2EC")
    for ax in axs.flat: ax.axis("off")
    for ax, (i, (n, im)) in zip(axs.flat, enumerate(isos, 1)): ax.imshow(im); ax.set_title(f"{i}. {n}", fontsize=11, color="#555")
    plt.tight_layout(rect=(0, 0, 1, .97)); fig.savefig(os.path.join(OUT, "overview.png"), dpi=90, facecolor="#F4F2EC"); plt.close(fig)
if __name__ == "__main__": main()
