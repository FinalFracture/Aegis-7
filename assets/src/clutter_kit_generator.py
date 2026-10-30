"""Rev C #36 small clutter kit (meal tray, cups, cables, photo frames with decal faces; rooms 101, 102, 104, 202; 1 kit). Five iterations, family language.
Each iteration is one kit: separate named pieces laid out in a row (split per piece in Godot). Each piece's pivot is its own bottom-centre (offsets below are layout only).
Spin-down: every piece has a docking base (magnet ring, clip or tacky pad) so tabletop clutter stays put; photo faces are decal panels for Sloane."""
import os, sys, numpy as np, trimesh
sys.path.insert(0, os.path.dirname(__file__))
from hydro_planter_generator import cyl, box, bev, blk, Pod, dc, wg, plt
from dining_chair_generator import export_final
from bath_pod_generator import set_glass_blend
from telescope_generator import rod
from cycler_route_generator import ellipse
OUT = os.path.join(dc.ROOT, "design/assets/clutter_kit")
def tray(p, x, mat, acc, ribs=2, base="gunmetal"):
    p.add("Meal_Tray", mat, blk(x - .18, x + .18, .006, .03, -.12, .12, .006, 1)); p.add("Tray_Dividers", acc, *[box(x - .17 + .12 * (i + 1) - .005, x - .17 + .12 * (i + 1) + .005, .03, .045, -.11, .11) for i in range(ribs)])
    p.add("Tray_Dock_Pad", base, box(x - .15, x + .15, 0, .006, -.09, .09))
def cups(p, x, mat, lid, n=2):
    for i in range(n):
        cx = x + (i - (n - 1) / 2) * .08; p.add(f"Cup_{i}", mat, cyl(cx, 0, .03, .006, .1, 10)); p.add(f"Cup_{i}_Lid", lid, cyl(cx, 0, .032, .1, .11, 10)); p.add(f"Cup_{i}_Base", "gunmetal", cyl(cx, 0, .034, 0, .006, 10))
def cable(p, x, mat, clip="amber"):
    p.add("Cable_Coil", mat, *ellipse(x, .06, .05, .05, 0, n=12, t=.01), *ellipse(x, .06, .04, .04, .012, n=12, t=.01))
    p.add("Cable_Tail", mat, rod((x + .05, .06, 0), (x + .12, .01, 0), .005, 6)); p.add("Cable_Plug", "alloy", box(x + .115, x + .14, 0, .02, -.008, .008)); p.add("Coil_Clip", clip, box(x - .015, x + .015, .1, .12, -.015, .015)); p.add("Coil_Hook_Base", "gunmetal", box(x - .03, x + .03, 0, .01, -.03, .03))
def frame(p, x, mat, w=.16, h=.2, lean=True, name="Photo_Frame"):
    t = .015; p.add(name, mat, *[box(x - w / 2, x + w / 2, y0, y1, -.01, .01) for y0, y1 in ((.01, .01 + t), (h - t + .01, h + .01))] + [box(x0, x1, .01, h + .01, -.01, .01) for x0, x1 in ((x - w / 2, x - w / 2 + t), (x + w / 2 - t, x + w / 2))])
    p.add(name + "_Decal_Face", "white", box(x - w / 2 + t, x + w / 2 - t, .01 + t, h + .01 - t, -.004, .004)); p.add(name + "_Stand", "gunmetal", box(x - .03, x + .03, 0, .01, -.04, .06))
X = (-.55, -.25, -.02, .2, .42)
def iter1():  # soft white: white tray with violet dividers, white cups with violet lids, white cable, alloy frames
    p = Pod("Soft_White"); tray(p, X[0], "white", "violet"); cups(p, X[1], "white", "violet"); cable(p, X[2], "white"); frame(p, X[3], "alloy"); frame(p, X[4], "alloy", .12, .15, name="Photo_Frame_Small"); return p
def iter2():  # magnet dock: slate pieces on visible gunmetal magnet rings with amber dock dots
    p = Pod("Magnet_Dock"); tray(p, X[0], "slate", "alloy", 3); cups(p, X[1], "slate", "alloy"); cable(p, X[2], "slate"); frame(p, X[3], "gunmetal"); frame(p, X[4], "gunmetal", .12, .15, name="Photo_Frame_Small")
    p.add("Dock_Dots", "amber", *[box(x - .008, x + .008, .006, .01, .08, .095) for x in X[:3]]); return p
def iter3():  # clip rail: everything parks on a short alloy rail strip; frames clip on top
    p = Pod("Clip_Rail"); p.add("Rail_Strip", "alloy", box(-.75, .55, 0, .012, -.14, .14)); p.add("Rail_Clips", "amber", *[box(x - .02, x + .02, .012, .02, .13, .14) for x in X])
    tray(p, X[0], "white", "slate"); cups(p, X[1], "alloy", "white"); cable(p, X[2], "gunmetal"); frame(p, X[3], "white"); frame(p, X[4], "white", .12, .15, name="Photo_Frame_Small"); return p
def iter4():  # family colour: mixed accent colours per resident (violet, green, amber), white bodies
    p = Pod("Family_Colour"); tray(p, X[0], "white", "green"); cups(p, X[1], "white", "amber", 3); cable(p, X[2], "violet", "green"); frame(p, X[3], "violet"); frame(p, X[4], "green", .12, .15, name="Photo_Frame_Small"); return p
def iter5():  # utility: gunmetal tray with tall walls and a lid clip, insulated alloy cups, cable on a reel, a digital photo slate
    p = Pod("Utility"); tray(p, X[0], "gunmetal", "alloy"); p.add("Tray_Walls", "gunmetal", box(X[0] - .18, X[0] + .18, .03, .06, .11, .12)); p.add("Tray_Lid_Clip", "amber", box(X[0] - .02, X[0] + .02, .03, .07, .12, .13))
    cups(p, X[1], "alloy", "gunmetal"); p.add("Cable_Reel", "slate", cyl(X[2], 0, .06, 0, .03, 12)); cable(p, X[2], "gunmetal")
    p.add("Photo_Slate", "gunmetal", blk(X[3] - .1, X[3] + .1, .01, .16, -.008, .008, .004, 1)); p.add("Photo_Slate_Decal_Face", "white", box(X[3] - .09, X[3] + .09, .02, .15, .008, .01)); p.add("Photo_Slate_Stand", "gunmetal", box(X[3] - .04, X[3] + .04, 0, .01, -.05, .05))
    p.add("Slate_Status_Light", "green", box(X[3] + .07, X[3] + .085, .012, .018, .008, .011)); frame(p, X[4], "alloy", .12, .15, name="Photo_Frame_Small"); return p

def main():
    os.makedirs(OUT, exist_ok=True); isos = []
    for i, fn in enumerate([iter1, iter2, iter3, iter4, iter5], 1):
        p = fn(); full = dict(p.P); p.P = {k: v for k, v in full.items() if v[0] != "glass"}  # glass hidden in sheet renders (BLEND in glb)
        tris, iso, lo, hi, bad = wg.sheet(p, os.path.join(OUT, f"iter_0{i}_sheet.png"), f"iter_0{i}  {p.name}  (#36 clutter kit)")
        p.P = full; gp = os.path.join(OUT, f"iter_0{i}.glb"); tris, _ = export_final(p.P, [gp]); set_glass_blend(gp)
        isos.append((p.name, iso)); print(i, p.name, tris, (hi - lo).round(3), "bad", bad)
    fig, axs = plt.subplots(3, 2, figsize=(16, 12), facecolor="#F4F2EC")
    for ax in axs.flat: ax.axis("off")
    for ax, (i, (n, im)) in zip(axs.flat, enumerate(isos, 1)): ax.imshow(im); ax.set_title(f"{i}. {n}", fontsize=11, color="#555")
    plt.tight_layout(rect=(0, 0, 1, .97)); fig.savefig(os.path.join(OUT, "overview.png"), dpi=90, facecolor="#F4F2EC"); plt.close(fig)
if __name__ == "__main__": main()
