"""Rev C #20 kids' bunk (103, 202; qty 2; 0.9 W x 1.9 D x 1.7 H). Five iterations, family language.
Long axis along Z (D 1.9), front/foot end +Z, bottom-centre pivot. Spin-down: mattresses strapped/latched, guard rails, ladder latched.
No clothes or soft storage contents anywhere (drawers/cubbies are empty)."""
import os, sys, numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import dining_chair_generator as dc
from bath_pod_generator import blk, cyl, Pod
from kitchen_counter_generator import bev, box
from double_bed_generator import soft
import wardrobe_generator as wg
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
OUT = os.path.join(dc.ROOT, "design/assets/kids_bunk")
W, D, H = .9, 1.9, 1.7; X0, X1, Z0, Z1 = -.45, .45, -.95, .95
YLO, YUP = .3, 1.12     # deck tops

def mattress(p, y, tag):
    p.add(f"Mattress_{tag}", "slatefab", soft(.8, 1.8, y, y + .12, .04))
    p.add("Mattress_Straps", "amber", *[box(-.405, .405, y + .12, y + .126, z - .02, z + .02) for z in (-.6, .6)])
def guard(p, y, z0=Z0, z1=.45, mat="alloy"):   # upper guard both long sides, open at the foot ladder side
    for x in (X0, X1 - .03):
        p.add("Guard_Rails", mat, box(x, x + .03, y + .12, y + .42, z0, z1) if mat == "white" else blk(x, x + .03, y + .38, y + .42, z0, z1, .008, 1),
              *([] if mat == "white" else [box(x + .005, x + .025, y, y + .38, zz - .015, zz + .015) for zz in np.linspace(z0 + .05, z1 - .05, 4)]))
def ladder(p, x0=-.2, x1=.2, z=Z1 - .04, top=YUP + .1, mat="alloy"):
    p.add("Ladder", mat, box(x0, x0 + .03, 0, top + .3, z - .02, z + .02), box(x1 - .03, x1, 0, top + .3, z - .02, z + .02),
          *[box(x0 + .03, x1 - .03, y - .015, y + .015, z - .02, z + .02) for y in np.arange(.4, top, .27)])
    p.add("Ladder_Latch", "amber", box(x1, x1 + .015, top + .2, top + .26, z - .015, z + .015))
def floor_anchors(p, pts):
    p.add("Floor_Anchors", "gunmetal", *[box(x - .05, x + .05, 0, .015, z - .05, z + .05) for x, z in pts])

def iter1():  # moulded shell end panels
    p = Pod("Moulded_Shell")
    for z in (Z0, Z1 - .05): p.add("End_Panels", "white", bev(W, .05, 0, H, .04, .01, 2, 0, z + .025))
    p.add("Head_Cutouts_Trim", "violet", box(-.3, .3, H - .12, H - .1, Z0 + .05, Z0 + .052))
    for y in (YLO, YUP):
        p.add("Decks", "gunmetal", bev(.86, 1.8, y - .05, y, .02, .006, 1, 0, 0)); mattress(p, y, "Lo" if y < 1 else "Up")
    p.add("Side_Rails", "white", box(X0, X0 + .04, YLO - .12, YLO, Z0 + .05, Z1 - .05), box(X1 - .04, X1, YLO - .12, YLO, Z0 + .05, Z1 - .05),
          box(X0, X0 + .04, YUP - .12, YUP, Z0 + .05, Z1 - .05), box(X1 - .04, X1, YUP - .12, YUP, Z0 + .05, Z1 - .05))
    guard(p, YUP, mat="white"); ladder(p, z=Z1 + .03); floor_anchors(p, [(x, z) for x in (-.35, .35) for z in (-.9, .9)]); return p
def iter2():  # wall-rail clamped (wall on -X), cantilevered decks, no floor posts on the room side
    p = Pod("Wall_Clamped")
    p.add("Wall_Plate", "gunmetal", bev(.04, 1.9, 0, H, .01, .004, 1, X0 + .02, 0))
    p.add("Wall_Rails", "alloy", *[box(X0 + .04, X0 + .07, y - .02, y + .02, Z0, Z1) for y in (.25, 1.05, 1.6)])
    for y in (YLO, YUP):
        p.add("Decks", "white", bev(.83, 1.86, y - .06, y, .02, .006, 1, .035, 0)); mattress(p, y, "Lo" if y < 1 else "Up")
        p.add("Rail_Clamps", "amber", *[box(X0 + .07, X0 + .1, y - .1, y - .06, z - .04, z + .04) for z in (-.7, 0, .7)])
    p.add("Front_Post", "alloy", cyl(X1 - .03, Z1 - .04, .025, 0, YUP, 12))
    guard(p, YUP, X0 if False else Z0); ladder(p, .05, .4); floor_anchors(p, [(X0 + .05, -.9), (X0 + .05, .9), (X1 - .03, Z1 - .04)]); return p
def iter3():  # capsule upper with hood + latched net-free guard panels, open lower
    p = Pod("Upper_Capsule")
    p.add("Posts", "gunmetal", *[blk(x - .03, x + .03, 0, YUP, z - .03, z + .03, .01, 1) for x in (X0 + .03, X1 - .03) for z in (Z0 + .03, Z1 - .03)])
    p.add("Lower_Deck", "gunmetal", bev(.86, 1.86, YLO - .05, YLO, .02, .006, 1, 0, 0)); mattress(p, YLO, "Lo")
    p.add("Capsule_Shell", "white", bev(W, D, YUP - .08, YUP, .05, .01, 2), box(X0, X0 + .04, YUP, H, Z0, Z1), box(X0, X1, H - .04, H, Z0, Z1),
          box(X0, X1, YUP, H, Z0, Z0 + .04), box(X1 - .04, X1, YUP, YUP + .3, Z0 + .04, Z1))
    p.add("Capsule_Light", "violet", box(X0 + .04, X0 + .045, H - .15, H - .12, Z0 + .1, Z1 - .1))
    mattress(p, YUP, "Up"); ladder(p, .02, .38, top=YUP); floor_anchors(p, [(x, z) for x in (-.4, .4) for z in (-.9, .9)]); return p
def iter4():  # lower bunk on empty storage plinth (latched drawers), step-stair at the foot
    p = Pod("Plinth_Steps")
    p.add("Plinth", "white", bev(W, 1.5, 0, YLO - .03, .03, .008, 2, 0, -.2))
    p.add("Drawer_Fronts", "slate", *[box(X1 - .002 if False else -.4, .4, .05, YLO - .07, z - .3, z + .3) if False else box(X1, X1 + .012, .05, YLO - .07, z - .3, z + .3) for z in (-.6, .1)])
    p.add("Drawer_Latches", "amber", *[box(X1 + .012, X1 + .018, .15, .2, z - .03, z + .03) for z in (-.6, .1)])
    p.add("Mattress_Lo", "slatefab", soft(.8, 1.4, YLO - .03, YLO + .09, .04, 0, -.2)); p.add("Mattress_Straps", "amber", *[box(-.405, .405, YLO + .09, YLO + .096, z - .02, z + .02) for z in (-.7, .3)])
    p.add("Upper_Frame", "gunmetal", bev(.9, 1.5, YUP - .06, YUP, .02, .006, 1, 0, -.2), *[box(x - .03, x + .03, YLO - .03, YUP, Z0 + .0, Z0 + .06) for x in (X0 + .03, X1 - .03)], *[box(x - .03, x + .03, YLO - .03, YUP, .49, .55) for x in (X0 + .03, X1 - .03)])
    p.add("Upper_Mattress", "slatefab", soft(.8, 1.4, YUP, YUP + .12, .04, 0, -.2))
    guard(p, YUP, Z0, .55)
    steps = [(.55, 1.0, .0), (.55, 1.0, .3), (.55, 1.0, .6), (.55, 1.0, .9)]
    for i, y in enumerate((YUP - .02, .74, .37)):
        p.add("Step_Stair", "white", box(-.45, .45, 0 if i == 0 else 0, y, .55 + .13 * i, .55 + .13 * (i + 1)) if False else box(-.45, .45, 0, y, .55 + .133 * i, .55 + .133 * (i + 1)))
        p.add("Step_Nosing", "amber", box(-.4, .4, y - .004, y + .002, .55 + .133 * i, .55 + .133 * i + .02))
    p.add("Step_Stair", "white", box(-.45, .45, 0, YUP, .949, .95)) if False else None
    floor_anchors(p, [(x, z) for x in (-.35, .35) for z in (-.9, .9)]); return p
def iter5():  # Sprocket-serviced: lower deck lifts on latched gas struts for under-bed service port at 0.45; integrated night light
    p = Pod("Sprocket_Service")
    for z in (Z0, Z1 - .05): p.add("End_Frames", "gunmetal", bev(W, .05, 0, H - .1, .03, .008, 2, 0, z + .025))
    p.add("Side_Rails", "alloy", *[box(x, x + .03, y - .1, y, Z0 + .05, Z1 - .05) for x in (X0, X1 - .03) for y in (YLO + .1, YUP)])
    p.add("Decks", "white", bev(.84, 1.8, YLO + .05, YLO + .1, .02, .006, 1, 0, 0), bev(.84, 1.8, YUP - .05, YUP, .02, .006, 1, 0, 0))
    mattress(p, YLO + .1, "Lo"); mattress(p, YUP, "Up"); guard(p, YUP)
    p.add("Service_Port", "gunmetal", bev(.14, .02, .38, .52, .01, .004, 1, 0, Z1 - .05 + .01 + .02)); p.add("Service_Port_Ring", "amber", box(-.03, .03, .43, .47, Z1 + .02, Z1 + .025))
    p.add("Status_Light", "green", box(-.06, .06, .58, .6, Z1, Z1 + .004))
    p.add("Night_Light", "violet", box(X0 + .03, X1 - .03, YUP - .06, YUP - .052, Z0 + .1, Z1 - .1))
    ladder(p, X0 + .05, X0 + .4, z=Z1 + .03, mat="alloy"); floor_anchors(p, [(x, z) for x in (-.35, .35) for z in (-.9, .9)]); return p

def main():
    os.makedirs(OUT, exist_ok=True); isos = []
    for i, fn in enumerate([iter1, iter2, iter3, iter4, iter5], 1):
        p = fn(); tris, iso, lo, hi, bad = wg.sheet(p, os.path.join(OUT, f"iter_0{i}_sheet.png"), f"iter_0{i}  {p.name}  (#20 kids' bunk)")
        isos.append((p.name, iso)); print(i, p.name, tris, (hi - lo).round(3), lo.round(3), "bad", bad)
    fig, axs = plt.subplots(2, 3, figsize=(15, 10), facecolor="#F4F2EC")
    for ax in axs.flat: ax.axis("off")
    for ax, (i, (n, im)) in zip(axs.flat, enumerate(isos, 1)): ax.imshow(im); ax.set_title(f"{i}. {n}", fontsize=11, color="#555")
    plt.tight_layout(rect=(0, 0, 1, .97)); fig.savefig(os.path.join(OUT, "overview.png"), dpi=90, facecolor="#F4F2EC"); plt.close(fig)
if __name__ == "__main__": main()
