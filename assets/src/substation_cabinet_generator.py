"""Rev C #42 Substation cabinet (Maintenance, RM 1B Bot Substation; qty 1; 2.5 W x 0.6 D x 2.2 H; level blockout Room1B_Substation_*).
Five iterations in the family language. Pivot at the bottom-centre, +Z front, wall at -Z.
Spin-down: the cabinet bolts to the floor and wall rail; every door, drawer and cell latches with amber catches. Green = live/OK lamps."""
import os, sys, numpy as np, trimesh
sys.path.insert(0, os.path.dirname(__file__))
from hydro_planter_generator import cyl, box, bev, blk, Pod, dc, wg, plt
from dining_chair_generator import export_final
from bath_pod_generator import set_glass_blend
from cycler_route_generator import cyl_z
OUT = os.path.join(dc.ROOT, "design/assets/substation_cabinet")
W, D, H = 2.5, .6, 2.2; X0, X1, ZB, ZF = -W / 2, W / 2, -D / 2, D / 2; PL = .08
def shell(p, mat="white", top=H):
    p.add("Plinth", "gunmetal", box(X0 + .02, X1 - .02, 0, PL, ZB, ZF - .05)); p.add("Carcass", mat, blk(X0, X1, PL, top, ZB, ZF - .03, .006, 1))
    p.add("Floor_Bolts", "amber", *[cyl(x, ZF - .05 + .0, .012, 0, PL + .004, 6) for x in (X0 + .06, X1 - .06)])
def doors(p, xs, y0, y1, mat="slate", name="Doors", latch=True):
    p.add(name, mat, *[box(xs[i] + .01, xs[i + 1] - .01, y0, y1, ZF - .03, ZF - .012) for i in range(len(xs) - 1)])
    if latch: p.add(name + "_Latches", "amber", *[box(xs[i + 1] - .06, xs[i + 1] - .03, (y0 + y1) / 2 - .06, (y0 + y1) / 2 + .06, ZF - .012, ZF) for i in range(len(xs) - 1)])
def louvres(p, x0, x1, y0, y1, n, name="Louvres"):
    p.add(name, "gunmetal", *[box(x0, x1, y, y + .012, ZF - .012, ZF - .004) for y in np.linspace(y0, y1 - .012, n)])
def lamps(p, xs, y, mat="green", name="Status_Lamps"):
    p.add(name, mat, *[cyl(x, ZF - .012, .012, y, y + .01, 8) for x in xs])
def iter1():  # breaker bank: three tall slate doors with louvred vents, a green status lamp each, gunmetal header with a cable gland row
    p = Pod("Breaker_Bank"); shell(p, top=H - .2); xs = np.linspace(X0, X1, 4); doors(p, xs, PL + .02, H - .22)
    p.add("Header", "gunmetal", box(X0, X1, H - .2, H, ZB, ZF - .02)); p.add("Cable_Glands", "alloy", *[cyl(x, -.05, .03, H, H + 0.0001 + .0, 10) for x in []] or [box(X0 + .1, X1 - .1, H - .14, H - .06, ZF - .02, ZF - .012)])
    for i in range(3): c = (xs[i] + xs[i + 1]) / 2; louvres(p, c - .25, c + .25, H - .6, H - .3, 6, f"Louvres_{i}"); louvres(p, c - .25, c + .25, .25, .5, 6, f"Low_Louvres_{i}")
    lamps(p, [(xs[i] + xs[i + 1]) / 2 for i in range(3)], H - .17 + .0); return p
def iter2():  # open busbar rack: gunmetal frame, BLEND glass doors over alloy busbars and amber breaker rows, slate back
    p = Pod("Busbar_Glass_Rack"); p.add("Plinth", "gunmetal", box(X0 + .02, X1 - .02, 0, PL, ZB, ZF - .05)); xs = np.linspace(X0, X1, 4)
    p.add("Frame", "gunmetal", *[box(max(x - .03, X0), min(x + .03, X1), PL, H, ZB, ZF - .03) for x in xs], box(X0, X1, H - .06, H, ZB, ZF - .03), box(X0, X1, PL, PL + .05, ZB, ZF - .03))
    p.add("Back_Panel", "slate", box(X0, X1, PL, H - .06, ZB, ZB + .02)); p.add("Busbars", "alloy", *[box(X0 + .05, X1 - .05, y, y + .03, ZB + .08, ZB + .095) for y in (1.7, 1.78, 1.86)])
    p.add("Breakers", "white", *[box(x - .025, x + .025, y, y + .14, ZB + .02, ZB + .12) for y in (.4, .75, 1.1, 1.45) for x in np.linspace(X0 + .15, X1 - .15, 14)])
    p.add("Breaker_Toggles", "amber", *[box(x - .008, x + .008, y + .06, y + .09, ZB + .12, ZB + .14) for y in (.4, .75, 1.1, 1.45) for x in np.linspace(X0 + .15, X1 - .15, 14)])
    p.add("Glass_Doors", "glass", *[box(xs[i] + .03, xs[i + 1] - .03, PL + .05, H - .06, ZF - .045, ZF - .035) for i in range(3)])
    p.add("Door_Latches", "amber", *[box(xs[i + 1] - .07, xs[i + 1] - .04, 1.0, 1.15, ZF - .035, ZF - .02) for i in range(3)]); lamps(p, np.linspace(X0 + .3, X1 - .3, 5), H - .045); return p
def iter3():  # battery cell wall: 4 x 8 grid of slide-in cell bays, some cells docked (white with green charge bands), amber cell latches
    p = Pod("Battery_Cell_Wall"); shell(p, top=H - .22); xs = np.linspace(X0 + .05, X1 - .05, 9); ys = np.linspace(PL + .1, H - .25, 5)
    p.add("Bay_Dividers", "gunmetal", *[box(x - .008, x + .008, ys[0], ys[-1], ZF - .2, ZF - .03) for x in xs], *[box(xs[0], xs[-1], y - .008, y + .008, ZF - .2, ZF - .03) for y in ys])
    p.add("Bay_Backs", "slate", box(xs[0], xs[-1], ys[0], ys[-1], ZF - .21, ZF - .2)); full = [(i, j) for i in range(8) for j in range(4) if (i * 3 + j) % 4 != 1]
    p.add("Cells", "white", *[blk(xs[i] + .03, xs[i + 1] - .03, ys[j] + .04, ys[j + 1] - .04, ZF - .2, ZF - .04, .01, 1) for i, j in full])
    p.add("Charge_Bands", "green", *[box(xs[i] + .05, xs[i + 1] - .05, ys[j + 1] - .08, ys[j + 1] - .065, ZF - .04, ZF - .034) for i, j in full])
    p.add("Cell_Latches", "amber", *[box(xs[i] + .1, xs[i + 1] - .1, ys[j] + .05, ys[j] + .07, ZF - .04, ZF - .034) for i, j in full])
    p.add("Header", "gunmetal", box(X0, X1, H - .22, H, ZB, ZF - .02)); lamps(p, np.linspace(X0 + .2, X1 - .2, 8), H - .12); return p
def iter4():  # bot dock cabinet: lower central docking alcove with alloy charge contacts and amber guide rails, slate breaker doors either side and above
    p = Pod("Bot_Dock_Cabinet"); shell(p); ax0, ax1, ah = -.5, .5, 1.1
    p.add("Alcove_Liner", "gunmetal", box(ax0, ax1, PL, ah, ZB + .1, ZF - .025), box(ax0 - .02, ax0, PL, ah, ZB + .1, ZF - .02), box(ax1, ax1 + .02, PL, ah, ZB + .1, ZF - .02))
    p.add("Alcove_Floor", "slate", box(ax0, ax1, PL, PL + .02, ZB + .12, ZF - .02)); p.add("Charge_Contacts", "alloy", *[box(x - .05, x + .05, .45, .6, ZB + .1, ZB + .14) for x in (-.15, .15)])
    p.add("Guide_Rails", "amber", *[box(x - .015, x + .015, PL + .02, PL + .04, ZB + .14, ZF - .03) for x in (ax0 + .1, ax1 - .1)]); p.add("Dock_Lamp", "green", box(-.2, .2, ah - .05, ah - .03, ZB + .1, ZB + .12))
    doors(p, [X0, ax0 - .02], PL + .02, H - .05, name="Side_Doors_L"); doors(p, [ax1 + .02, X1], PL + .02, H - .05, name="Side_Doors_R"); doors(p, [ax0 - .02, 0, ax1 + .02], ah + .02, H - .05, name="Upper_Doors")
    lamps(p, (X0 + .2, X1 - .2), H - .1); return p
def iter5():  # conduit spine: compact cabinet with a central maintenance panel and amber handwheel disconnect, conduits rising from the top, side cable trays
    p = Pod("Conduit_Spine"); shell(p, top=H - .35); doors(p, np.linspace(X0, X1, 5), PL + .02, H - .4)
    p.add("Conduits", "alloy", *[cyl(x, z, .035, H - .35, H, 10) for x in np.linspace(X0 + .2, X1 - .2, 6) for z in (ZB + .08,)], *[cyl(x, ZB + .2, .025, H - .35, H, 8) for x in np.linspace(X0 + .4, X1 - .4, 4)])
    p.add("Conduit_Clamps", "gunmetal", box(X0 + .1, X1 - .1, H - .12, H - .08, ZB + .02, ZB + .25))
    p.add("Cable_Trays", "gunmetal", *[box(s * W / 2 - (.12 if s > 0 else 0), s * W / 2 + (0 if s > 0 else .12), PL, H - .35, ZB, ZB + .12) for s in (-1, 1)])
    p.add("Handwheel", "amber", cyl_z(0, 1.15, .1, ZF - .012, ZF - .004, 16)); p.add("Handwheel_Hub", "alloy", cyl_z(0, 1.15, .03, ZF - .004, ZF, 10))
    lamps(p, np.linspace(-.3, .3, 3), H - .45); return p
def main():
    os.makedirs(OUT, exist_ok=True); isos = []
    for i, fn in enumerate([iter1, iter2, iter3, iter4, iter5], 1):
        p = fn(); full = dict(p.P); p.P = {k: v for k, v in full.items() if v[0] != "glass"}  # glass hidden in sheet renders (BLEND in glb)
        tris, iso, lo, hi, bad = wg.sheet(p, os.path.join(OUT, f"iter_0{i}_sheet.png"), f"iter_0{i}  {p.name}  (#42 substation cabinet)")
        p.P = full; gp = os.path.join(OUT, f"iter_0{i}.glb"); tris, _ = export_final(p.P, [gp]); set_glass_blend(gp)
        isos.append((p.name, iso)); print(i, p.name, tris, (hi - lo).round(3), "bad", bad)
    fig, axs = plt.subplots(3, 2, figsize=(16, 12), facecolor="#F4F2EC")
    for ax in axs.flat: ax.axis("off")
    for ax, (i, (n, im)) in zip(axs.flat, enumerate(isos, 1)): ax.imshow(im); ax.set_title(f"{i}. {n}", fontsize=11, color="#555")
    plt.tight_layout(rect=(0, 0, 1, .97)); fig.savefig(os.path.join(OUT, "overview.png"), dpi=90, facecolor="#F4F2EC"); plt.close(fig)
if __name__ == "__main__": main()
