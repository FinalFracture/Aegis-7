"""Rev C #28 window desk + data slates (104, 204; qty 2; 4.0 W x 0.4 D x 0.75 H). Five iterations, family language.
Bottom-centre pivot, front +Z (window/wall at -Z). Data slates are mag-docked in latched cradles (spin-down); amber glyph screens
(104 story: every slate shows the same solar glyph). No loose stored contents."""
import os, sys, numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import dining_chair_generator as dc
from bath_pod_generator import blk, cyl, Pod
from kitchen_counter_generator import bev, box
from sofa_generator import tilt
import wardrobe_generator as wg
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
OUT = os.path.join(dc.ROOT, "design/assets/window_desk")
W, D, H = 4.0, .4, .75; ZB, ZF = -.2, .2; TOP = .75

def slates(p, xs, y=TOP, z=-.05):
    for x in xs:
        p.add("Slate_Cradles", "gunmetal", box(x - .14, x + .14, y, y + .02, z - .05, z + .03))
        p.add("Cradle_Latches", "amber", box(x + .12, x + .135, y + .02, y + .03, z + .02, z + .03))
        s = tilt(box(x - .125, x + .125, y + .02, y + .2, z - .03, z - .018), -18, [x, y + .02, z - .018])
        g = tilt(box(x - .05, x + .05, y + .07, y + .15, z - .0175, z - .016), -18, [x, y + .02, z - .018])
        p.add("Data_Slates", "slate", s); p.add("Slate_Glyphs", "amber", g)
def wall_rail(p, y=.62):
    p.add("Wall_Rail", "alloy", blk(-W / 2, W / 2, y - .02, y + .02, ZB - .03, ZB, .006, 1))
    p.add("Rail_Bolts", "gunmetal", *[box(x - .015, x + .015, y - .01, y + .01, ZB - .036, ZB - .03) for x in np.linspace(-1.8, 1.8, 7)])

def iter1():  # cantilever slab off a wall rail, recessed slate docks, violet under-light
    p = Pod("Cantilever_Slab"); wall_rail(p)
    p.add("Desk_Slab", "white", bev(W, D, TOP - .05, TOP, .02, .008, 2, 0, 0))
    p.add("Brackets", "gunmetal", *[blk(x - .02, x + .02, .5, TOP - .05, ZB, ZB + .3, .006, 1) for x in (-1.6, -.55, .55, 1.6)])
    p.add("Under_Light", "violet", box(-1.8, 1.8, TOP - .055, TOP - .05, ZF - .04, ZF - .03))
    slates(p, (-1.2, -.4, .4, 1.2)); return p
def iter2():  # alloy trestles, gunmetal top, floor-latched feet
    p = Pod("Alloy_Trestle")
    p.add("Desk_Top", "gunmetal", bev(W, D, TOP - .04, TOP, .015, .006, 2, 0, 0))
    for x in (-1.7, 0, 1.7):
        p.add("Trestles", "alloy", blk(x - .02, x + .02, .03, TOP - .04, ZB + .03, ZB + .07, .006, 1), blk(x - .02, x + .02, .03, TOP - .04, ZF - .07, ZF - .03, .006, 1),
              blk(x - .02, x + .02, .3, .34, ZB + .07, ZF - .07, .006, 1))
        p.add("Foot_Latches", "amber", box(x - .04, x + .04, 0, .03, ZB + .02, ZF - .02))
    slates(p, (-1.4, -.5, .5, 1.4)); return p
def iter3():  # moulded plinth with empty latched cubbies + knee bays
    p = Pod("Plinth_Cubbies")
    p.add("Desk_Top", "white", bev(W, D, TOP - .04, TOP, .02, .008, 2, 0, 0))
    for x in (-1.6, 0, 1.6):
        p.add("Cubby_Towers", "white", bev(.6, D - .02, 0, TOP - .04, .02, .006, 2, x, 0))
        p.add("Cubby_Doors", "slate", *[box(x - .27, x + .27, y, y + .3, ZF - .01, ZF) for y in (.04, .36)])
        p.add("Cubby_Latches", "amber", *[box(x + .2, x + .24, y + .13, y + .17, ZF, ZF + .004) for y in (.04, .36)])
    slates(p, (-.8, .8)); return p
def iter4():  # four fold-down leaves on a wall rail (two down/latched in use, two stowed up)
    p = Pod("Fold_Down_Leaves"); wall_rail(p, .7)
    for i, x in enumerate((-1.5, -.5, .5, 1.5)):
        if i in (1, 2):
            p.add("Leaves", "white", bev(.96, D - .02, TOP - .035, TOP, .015, .006, 2, x, .01))
            p.add("Leaf_Stays", "alloy", blk(x - .45, x - .43, .45, TOP - .035, ZB, ZB + .3, .004, 1), blk(x + .43, x + .45, .45, TOP - .035, ZB, ZB + .3, .004, 1))
            slates(p, (x,))
        else:
            p.add("Leaves", "white", bev(.96, .035, .32, .7, .015, .006, 2, x, ZB + .0175))
            p.add("Leaf_Latches", "amber", box(x - .03, x + .03, .66, .69, ZB + .035, ZB + .04))
    return p
def iter5():  # Sprocket service: desk (X -2..0.9) + open-topped Sprocket dock bay at the east end (no top over it), port at 0.45
    p = Pod("Sprocket_Bay")
    p.add("Desk_Top", "white", bev(2.9, D, TOP - .04, TOP, .02, .008, 2, -.55, 0))
    p.add("End_Panels", "white", bev(.04, D, 0, TOP - .04, .01, .004, 1, -W / 2 + .02, 0), bev(.04, D, 0, TOP, .01, .004, 1, .92, 0))
    p.add("Bay_Back", "gunmetal", bev(1.06, .03, 0, 1.1, .015, .005, 2, 1.47, ZB + .015))
    p.add("Bay_Side", "white", bev(.04, D, 0, 1.1, .01, .004, 1, W / 2 - .02, 0))
    p.add("Bay_Floor_Pad", "amber", box(1.1, 1.85, 0, .006, ZB + .05, ZF))
    p.add("Sprocket_Port", "gunmetal", bev(.14, .02, .38, .52, .01, .004, 1, 1.47, ZB + .04)); p.add("Port_Ring", "amber", box(1.44, 1.5, .43, .47, ZB + .05, ZB + .054))
    p.add("Status", "green", box(1.42, 1.52, .9, .92, ZB + .03, ZB + .034))
    p.add("Wall_Rail", "alloy", blk(-W / 2 + .04, .9, .05, .09, ZB, ZB + .03, .006, 1))
    slates(p, (-1.3, -.4, .4)); return p

def main():
    os.makedirs(OUT, exist_ok=True); isos = []
    for i, fn in enumerate([iter1, iter2, iter3, iter4, iter5], 1):
        p = fn(); tris, iso, lo, hi, bad = wg.sheet(p, os.path.join(OUT, f"iter_0{i}_sheet.png"), f"iter_0{i}  {p.name}  (#28 window desk + data slates)")
        isos.append((p.name, iso)); print(i, p.name, tris, (hi - lo).round(3), "bad", bad)
    fig, axs = plt.subplots(3, 2, figsize=(16, 12), facecolor="#F4F2EC")
    for ax in axs.flat: ax.axis("off")
    for ax, (i, (n, im)) in zip(axs.flat, enumerate(isos, 1)): ax.imshow(im); ax.set_title(f"{i}. {n}", fontsize=11, color="#555")
    plt.tight_layout(rect=(0, 0, 1, .97)); fig.savefig(os.path.join(OUT, "overview.png"), dpi=90, facecolor="#F4F2EC"); plt.close(fig)
if __name__ == "__main__": main()
