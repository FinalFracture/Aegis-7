"""Rev C #14 tea set (pot + cups; rooms 102, 203; qty 2; 0.4 W x 0.3 D x 0.2 H). Five iterations, family language.
Tabletop set. Pivot at the bottom-centre, +Z front. Spin-down: every piece docks in a recess or clip with an amber latch, so nothing slides off the table."""
import os, sys, numpy as np, trimesh
sys.path.insert(0, os.path.dirname(__file__))
from hydro_planter_generator import cyl, box, bev, blk, Pod, dc, wg, plt
from dining_chair_generator import export_final
from bath_pod_generator import set_glass_blend
from telescope_generator import rod
OUT = os.path.join(dc.ROOT, "design/assets/tea_set")
N = 12
def pot(p, x, y, z, r=.06, h=.11, mat="white", lid="alloy"):
    p.add("Pot_Body", mat, cyl(x, z, r, y, y + h, N)); p.add("Pot_Lid", lid, cyl(x, z, r * .8, y + h, y + h + .012, N)); p.add("Lid_Knob", "amber", cyl(x, z, .012, y + h + .012, y + h + .025, 8))
    p.add("Spout", mat, rod((x + r * .8, y + h * .3, z), (x + r + .05, y + h * .8, z), .011, 8)); p.add("Pot_Handle", lid, box(x - r - .03, x - r + .005, y + h * .25, y + h * .8, z - .008, z + .008))
def cup(p, x, y, z, r=.028, h=.06, mat="white", tag=""):
    p.add("Cups" + tag, mat, cyl(x, z, r, y, y + h, 10)); p.add("Cup_Handles" + tag, mat, box(x + r - .002, x + r + .014, y + .015, y + .045, z - .005, z + .005))
def latch(p, pts, y):
    p.add("Dock_Latches", "amber", *[box(x - .01, x + .01, y, y + .008, z - .004, z + .004) for x, z in pts])

CUPS = [(.08, -.07), (.15, -.07), (.08, .07), (.15, .07)]
def iter1():  # pocket tray: white tray with recessed docks; pot left, four cups right, amber latch tabs at each dock
    p = Pod("Pocket_Tray"); p.add("Tray", "slate", blk(-.2, .2, 0, .02, -.15, .15, .006, 1)); p.add("Tray_Rim", "gunmetal", *[box(-.2, .2, .02, .03, s * .15 - .006, s * .15 + .006) for s in (-1, 1)])
    pot(p, -.08, .012, 0); [cup(p, x, .012, z) for x, z in CUPS]; latch(p, [(x, z + .032) for x, z in CUPS] + [(-.08, .066)], .02); return p
def iter2():  # rail caddy: alloy caddy with a carry handle arch; cups hang mouth-down on pegs beside the pot
    p = Pod("Rail_Caddy"); p.add("Caddy_Base", "alloy", blk(-.19, .19, 0, .015, -.1, .1, .004, 1)); p.add("Handle_Posts", "alloy", *[box(s * .17 - .008, s * .17 + .008, .015, .19, -.008, .008) for s in (-1, 1)])
    p.add("Handle_Bar", "gunmetal", box(-.178, .178, .18, .195, -.01, .01)); pot(p, -.07, .015, 0, h=.1)
    p.add("Cup_Pegs", "gunmetal", *[box(x - .006, x + .006, .015, .05, z - .006, z + .006) for x, z in ((.06, -.05), (.13, -.05), (.06, .05), (.13, .05))])
    [cup(p, x, .015, z, h=.055) for x, z in ((.06, -.05), (.13, -.05), (.06, .05), (.13, .05))]; latch(p, [(-.17, 0), (.17, 0)], .15); return p
def iter3():  # stacking tower: four nested cups stack under the pot, one compact column on a small dock
    p = Pod("Stacking_Tower"); p.add("Dock", "gunmetal", cyl(0, 0, .07, 0, .015, N)); p.add("Cup_Stack", "white", *[cyl(0, 0, .045 - i * .002, .015 + i * .018, .033 + i * .018, N) for i in range(4)])
    p.add("Stack_Bands", "violet", *[cyl(0, 0, .046 - i * .002, .03 + i * .018, .033 + i * .018, N) for i in range(4)]); pot(p, 0, .087, 0, r=.05, h=.08)
    p.add("Lock_Arm", "alloy", box(.06, .072, .015, .17, -.008, .008)); latch(p, [(.066, 0)], .17); return p
def iter4():  # magnetic plate: slate plate with gunmetal ring docks; pot centre, cups at the corners, green dock lights
    p = Pod("Magnetic_Plate"); p.add("Plate", "slate", bev(.4, .3, 0, .012, .04, .004, 2, 0, 0))
    pts = [(-.15, -.1), (.15, -.1), (-.15, .1), (.15, .1)]; p.add("Dock_Rings", "gunmetal", *[cyl(x, z, .034, .012, .016, 10) for x, z in pts] + [cyl(0, 0, .068, .012, .016, N)])
    p.add("Dock_Lights", "green", *[box(x - .006, x + .006, .012, .016, z + .034, z + .04) for x, z in pts]); pot(p, 0, .016, 0, h=.1, mat="alloy", lid="white"); [cup(p, x, .016, z, mat="alloy") for x, z in pts]; return p
def iter5():  # spin-lock lids: fenced tray, pot with screw lid, cups with sip lids, a gate bar latching across the front
    p = Pod("Spin_Lock_Lids"); p.add("Tray", "white", blk(-.2, .2, 0, .015, -.15, .15, .006, 1))
    p.add("Fence", "alloy", *[box(-.2, .2, .015, .045, -.15, -.142), box(-.2, -.192, .015, .045, -.15, .15), box(.192, .2, .015, .045, -.15, .15)])
    p.add("Gate_Bar", "gunmetal", box(-.19, .19, .03, .045, .135, .145)); latch(p, [(.17, .14)], .045); pot(p, -.08, .015, 0); p.add("Lid_Thread", "gunmetal", cyl(-.08, 0, .05, .125, .13, N))
    [cup(p, x, .015, z) for x, z in CUPS]; p.add("Sip_Lids", "violet", *[cyl(x, z, .03, .075, .083, 10) for x, z in CUPS]); return p

def main():
    os.makedirs(OUT, exist_ok=True); isos = []
    for i, fn in enumerate([iter1, iter2, iter3, iter4, iter5], 1):
        p = fn(); full = dict(p.P); p.P = {k: v for k, v in full.items() if v[0] != "glass"}  # glass hidden in sheet renders (BLEND in glb)
        tris, iso, lo, hi, bad = wg.sheet(p, os.path.join(OUT, f"iter_0{i}_sheet.png"), f"iter_0{i}  {p.name}  (#14 tea set)")
        p.P = full; gp = os.path.join(OUT, f"iter_0{i}.glb"); tris, _ = export_final(p.P, [gp]); set_glass_blend(gp)
        isos.append((p.name, iso)); print(i, p.name, tris, (hi - lo).round(3), "bad", bad)
    fig, axs = plt.subplots(3, 2, figsize=(16, 12), facecolor="#F4F2EC")
    for ax in axs.flat: ax.axis("off")
    for ax, (i, (n, im)) in zip(axs.flat, enumerate(isos, 1)): ax.imshow(im); ax.set_title(f"{i}. {n}", fontsize=11, color="#555")
    plt.tight_layout(rect=(0, 0, 1, .97)); fig.savefig(os.path.join(OUT, "overview.png"), dpi=90, facecolor="#F4F2EC"); plt.close(fig)
if __name__ == "__main__": main()
