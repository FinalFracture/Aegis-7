"""Rev C #23 suit hook + storage (room 102; qty 1; listed 0.5 x 2.5 x 2.1, read as 2.5 W x 0.5 D x 2.1 H wall unit). Five iterations, family language.
EMPTY storage: no clothes and no suit modeled (Jared's no-clothes rule); the pressure suit is a separate prop if wanted. Pivot at the bottom-centre, +Z front, wall at -Z.
Spin-down: the unit bolts to the wall rail and floor; doors and drawers latch with amber catches; the suit hook arm locks."""
import os, sys, numpy as np, trimesh
sys.path.insert(0, os.path.dirname(__file__))
from hydro_planter_generator import cyl, box, bev, blk, Pod, dc, wg, plt
from dining_chair_generator import export_final
from bath_pod_generator import set_glass_blend
OUT = os.path.join(dc.ROOT, "design/assets/suit_storage")
W, D, H = 2.5, .5, 2.1; ZB, ZF = -D / 2, D / 2; BW = .8  # central suit bay width
def carcass(p, mat="white"):
    p.add("Side_Panels", mat, *[box(x0, x1, 0, H, ZB, ZF) for x0, x1 in ((-W / 2, -W / 2 + .03), (W / 2 - .03, W / 2))])
    p.add("Bay_Walls", mat, *[box(s * BW / 2 - .015, s * BW / 2 + .015, 0, H, ZB, ZF) for s in (-1, 1)])
    p.add("Top_Panel", mat, box(-W / 2, W / 2, H - .03, H, ZB, ZF)); p.add("Back_Panel", "slate", box(-W / 2, W / 2, 0, H, ZB, ZB + .015))
    p.add("Plinth", "gunmetal", box(-W / 2, W / 2, 0, .06, ZB, ZF - .03)); p.add("Wall_Rail_Bolts", "alloy", *[cyl(x, ZB + .015, .012, 1.8, 1.82, 6) for x in (-1.1, -.5, .5, 1.1)])
def doors(p, x0, x1, mat="white", n=1):
    w = (x1 - x0) / n; p.add("Doors", mat, *[box(x0 + i * w + .005, x0 + (i + 1) * w - .005, .065, H - .035, ZF - .032, ZF - .012) for i in range(n)])
    p.add("Door_Catches", "amber", *[box(x0 + (i + .5) * w - .015, x0 + (i + .5) * w + .015, 1.0, 1.12, ZF - .012, ZF) for i in range(n)])
def hook(p, y=1.75):
    p.add("Hook_Mount", "gunmetal", blk(-.1, .1, y - .08, y + .08, ZB + .015, ZB + .05, .004, 1)); p.add("Hook_Arm", "alloy", box(-.02, .02, y - .02, y + .02, ZB + .05, ZB + .32))
    p.add("Hook_Tip", "alloy", box(-.02, .02, y - .02, y + .08, ZB + .29, ZB + .33)); p.add("Hook_Lock", "amber", box(-.025, .025, y - .035, y - .02, ZB + .05, ZB + .1))
def bay_floor(p): p.add("Boot_Tray", "gunmetal", blk(-BW / 2 + .02, BW / 2 - .02, .06, .1, ZB + .02, ZF - .02, .004, 1)); p.add("Tray_Grip_Ribs", "slate", *[box(-BW / 2 + .05, BW / 2 - .05, .1, .106, z - .006, z + .006) for z in np.linspace(ZB + .08, ZF - .08, 4)])
def helmet_shelf(p, y=1.95): p.add("Helmet_Shelf", "alloy", box(-BW / 2 + .015, BW / 2 - .015, y, y + .025, ZB + .015, ZF - .03)); p.add("Helmet_Collar_Dock", "gunmetal", cyl(0, 0, .13, y + .025, y + .04, 14)); p.add("Collar_Latch", "amber", box(-.02, .02, y + .025, y + .045, .13, .15))

SX = (-W / 2 + .03, -BW / 2 - .015); SXR = (BW / 2 + .015, W / 2 - .03)
def iter1():  # open hook bay: open central bay with locking hook arm and boot tray, closed white lockers each side
    p = Pod("Open_Hook_Bay"); carcass(p); doors(p, *SX); doors(p, *SXR); hook(p, 1.65); bay_floor(p); helmet_shelf(p, 1.84); return p
def iter2():  # glass suit locker: the bay gets a full glass door with an alloy frame; side doors slate
    p = Pod("Glass_Suit_Locker"); carcass(p); doors(p, *SX, "slate"); doors(p, *SXR, "slate"); hook(p, 1.65); bay_floor(p); helmet_shelf(p, 1.84)
    p.add("Bay_Glass", "glass", box(-BW / 2 + .02, BW / 2 - .02, .08, H - .05, ZF - .027, ZF - .02))
    p.add("Glass_Frame", "alloy", *[box(x0, x1, y0, y1, ZF - .032, ZF - .012) for x0, x1, y0, y1 in ((-BW / 2 + .015, BW / 2 - .015, .065, .09), (-BW / 2 + .015, BW / 2 - .015, H - .06, H - .035), (-BW / 2 + .015, -BW / 2 + .04, .065, H - .035), (BW / 2 - .04, BW / 2 - .015, .065, H - .035))])
    p.add("Glass_Catch", "amber", box(BW / 2 - .04, BW / 2 - .025, 1.0, 1.12, ZF - .012, ZF)); return p
def iter3():  # rail rack: no side doors; open alloy shelves left, drawer stack right, suit hanger slides on a top rail
    p = Pod("Rail_Rack"); carcass(p, "alloy"); bay_floor(p)
    p.add("Open_Shelves", "white", *[box(SX[0], SX[1], y, y + .025, ZB + .015, ZF - .02) for y in (.5, .95, 1.4, 1.85)]); p.add("Shelf_Lips", "gunmetal", *[box(SX[0], SX[1], y + .025, y + .06, ZF - .03, ZF - .02) for y in (.5, .95, 1.4, 1.85)])
    ys = np.linspace(.07, H - .04, 6); p.add("Drawers", "white", *[box(SXR[0] + .005, SXR[1] - .005, ys[i] + .005, ys[i + 1] - .005, ZF - .032, ZF - .012) for i in range(5)])
    p.add("Drawer_Pulls", "amber", *[box(sum(SXR) / 2 - .1, sum(SXR) / 2 + .1, ys[i + 1] - .06, ys[i + 1] - .04, ZF - .012, ZF) for i in range(5)])
    p.add("Top_Rail", "gunmetal", box(-BW / 2 + .015, BW / 2 - .015, 1.85, 1.9, -.03, .03)); p.add("Slide_Hanger", "alloy", box(-.06, .06, 1.7, 1.85, -.02, .02)); p.add("Hanger_Lock", "amber", box(-.07, -.05, 1.85, 1.9, .03, .04)); return p
def iter4():  # service wall: bay backed by a suit service panel (green charge and O2 status lights, umbilical port), tool cabinets
    p = Pod("Service_Wall"); carcass(p, "white"); doors(p, *SX, n=2); doors(p, *SXR, n=2); hook(p, 1.65); bay_floor(p); helmet_shelf(p, 1.84)
    p.add("Service_Panel", "gunmetal", blk(-.3, .3, .9, 1.4, ZB + .015, ZB + .05, .006, 1)); p.add("Umbilical_Port", "alloy", cyl(0, ZB + .05, .05, 1.05, 1.05, 12) if False else box(-.06, .06, 1.0, 1.12, ZB + .05, ZB + .08))
    p.add("Status_Lights", "green", *[box(x - .02, x + .02, 1.28, 1.31, ZB + .05, ZB + .056) for x in (-.18, -.1, .1, .18)]); p.add("Port_Cap_Latch", "amber", box(-.03, .03, .97, .99, ZB + .05, ZB + .085)); return p
def iter5():  # pod alcove: arched bay opening (stepped frame), slate interior, violet edge light, doors either side
    p = Pod("Pod_Alcove"); carcass(p); p.add("Bay_Interior", "slate", box(-BW / 2 + .015, BW / 2 - .015, .06, H - .03, ZB + .015, ZB + .03)); doors(p, *SX, "white"); doors(p, *SXR, "white")
    p.add("Arch_Steps", "white", *[box(-BW / 2 + .015, BW / 2 - .015 - 0, H - .03 - .06 * (i + 1), H - .03 - .06 * i, ZF - .02, ZF) for i in range(1)] + [box(s * (BW / 2 - .015 - .05 * (i + 1)) - (0 if s > 0 else 0), s * (BW / 2 - .015 - .05 * i), H - .09 - .06 * (i + 1), H - .09 - .06 * i, ZF - .02, ZF) for s in (-1, 1) for i in range(3)])
    p.add("Edge_Light", "violet", *[box(s * (BW / 2 - .03) - .006, s * (BW / 2 - .03) + .006, .1, H - .3, ZF - .03, ZF - .02) for s in (-1, 1)]); hook(p, 1.6); bay_floor(p); return p

def main():
    os.makedirs(OUT, exist_ok=True); isos = []
    for i, fn in enumerate([iter1, iter2, iter3, iter4, iter5], 1):
        p = fn(); full = dict(p.P); p.P = {k: v for k, v in full.items() if v[0] != "glass"}  # glass hidden in sheet renders (BLEND in glb)
        tris, iso, lo, hi, bad = wg.sheet(p, os.path.join(OUT, f"iter_0{i}_sheet.png"), f"iter_0{i}  {p.name}  (#23 suit storage (empty))")
        p.P = full; gp = os.path.join(OUT, f"iter_0{i}.glb"); tris, _ = export_final(p.P, [gp]); set_glass_blend(gp)
        isos.append((p.name, iso)); print(i, p.name, tris, (hi - lo).round(3), "bad", bad)
    fig, axs = plt.subplots(3, 2, figsize=(16, 12), facecolor="#F4F2EC")
    for ax in axs.flat: ax.axis("off")
    for ax, (i, (n, im)) in zip(axs.flat, enumerate(isos, 1)): ax.imshow(im); ax.set_title(f"{i}. {n}", fontsize=11, color="#555")
    plt.tight_layout(rect=(0, 0, 1, .97)); fig.savefig(os.path.join(OUT, "overview.png"), dpi=90, facecolor="#F4F2EC"); plt.close(fig)
if __name__ == "__main__": main()
