"""Rev C #42 Substation, round 2 (Jared, Oct 29: build from option 3 Battery Cell Wall, read as industrial power equipment, not furniture).
RM 1B Bot Substation; envelope ~2.5 W x <=0.8 D x 2.2 H. Sprocket-first: every option has a Sprocket service port at 0.45 m with floor guide rails;
humans get only a small status panel + amber disconnect handle. Open frames, exposed cells, busbars/cables into wall (-Z) and floor, standoff insulators,
drums, fins and ducts. Pivot at the bottom-centre, +Z front. Spin-down: cells latch (amber), racks clamp to floor and wall."""
import os, sys, numpy as np, trimesh
sys.path.insert(0, os.path.dirname(__file__))
from hydro_planter_generator import cyl, box, bev, blk, Pod, dc, wg, plt
from dining_chair_generator import export_final
from bath_pod_generator import set_glass_blend
from cycler_route_generator import cyl_z
from folding_counter_generator import xcyl
OUT = os.path.join(dc.ROOT, "design/assets/substation_r2")
W, D, H = 2.5, .8, 2.2; X0, X1, ZB, ZF = -W / 2, W / 2, -D / 2, D / 2; PY = .45
def cells(p, xs, ys, z0, z1, skip=(), tag=""):
    C, B, L = [], [], []
    for i, x in enumerate(xs):
        for j, y in enumerate(ys):
            if (i, j) in skip: continue
            C.append(blk(x - .1, x + .1, y, y + .26, z0, z1, .01, 1)); B.append(box(x - .08, x + .08, y + .2, y + .215, z1, z1 + .006)); L.append(box(x - .03, x + .03, y + .03, y + .05, z1, z1 + .006))
    p.add("Cells" + tag, "white", *C); p.add("Charge_Bands" + tag, "green", *B); p.add("Cell_Latches" + tag, "amber", *L)
def rack(p, x0, x1, ys, z0, z1, tag=""):  # open frame: 4 posts + shelf rails per tier, no panels
    x0, x1 = x0 + .045, x1 - .045
    p.add("Rack_Posts" + tag, "gunmetal", *[box(x - .025, x + .025, 0, ys[-1] + .32, z - .025, z + .025) for x in (x0, x1) for z in (z0, z1)])
    p.add("Tier_Rails" + tag, "alloy", *[box(x0, x1, y - .025, y, z - .02, z + .02) for y in ys for z in (z0, z1)])
    p.add("Floor_Clamps" + tag, "amber", *[box(x - .045, x + .045, 0, .025, z - .045, z + .045) for x in (x0, x1) for z in (z0, z1)])
def insulators(p, pts, h=.08, tag=""):  # standoff insulators along -Z from the wall: stacked discs
    p.add("Standoffs" + tag, "ceramic", *[cyl_z(x, y, r, ZB + k * h / 3, ZB + (k + 1) * h / 3 - .006, 8) for x, y in pts for k, r in enumerate((.03, .024, .03))])
def busbar_runs(p, x, y0, y1, n=3, dx=.06, tag=""):  # vertical copper-alloy busbars on standoffs, entering the floor
    p.add("Busbars" + tag, "alloy", *[box(x + k * dx - .012, x + k * dx + .012, 0, y1, ZB + .08, ZB + .1) for k in range(n)])
    insulators(p, [(x + k * dx, y) for k in range(n) for y in np.linspace(y0, y1 - .1, 3)], tag=tag)
def port(p, x, z, tag=""):  # Sprocket service port at 0.45 m: slate socket, alloy pins, amber funnel, green ready lamp, floor guide rails forward
    p.add("Port_Plate" + tag, "slate", box(x - .16, x + .16, PY - .12, PY + .12, z - .03, z)); p.add("Port_Pins" + tag, "alloy", *[cyl_z(x + dx, PY, .012, z, z + .025, 6) for dx in (-.06, 0, .06)])
    p.add("Port_Funnel" + tag, "amber", box(x - .18, x + .18, PY + .12, PY + .14, z - .03, z + .02), box(x - .18, x + .18, PY - .14, PY - .12, z - .03, z + .02), box(x - .18, x - .16, PY - .12, PY + .12, z - .03, z + .02), box(x + .16, x + .18, PY - .12, PY + .12, z - .03, z + .02))
    p.add("Port_Ready_Lamp" + tag, "green", box(x - .05, x + .05, PY + .16, PY + .18, z - .02, z)); p.add("Guide_Rails" + tag, "amber", *[box(x + s * .3 - .02, x + s * .3 + .02, 0, .03, z, ZF) for s in (-1, 1)])
def human(p, x, z, tag=""):  # small status panel + amber disconnect handle; the only human interactable
    p.add("Status_Panel" + tag, "slate", box(x - .14, x + .14, 1.35, 1.6, z - .04, z)); p.add("Panel_Lamps" + tag, "green", *[box(x - .1 + k * .07, x - .06 + k * .07, 1.52, 1.56, z, z + .006) for k in range(3)])
    p.add("Panel_Post" + tag, "gunmetal", box(x - .02, x + .02, 0, 1.6, z - .07, z - .04), box(x - .06, x + .06, 0, .02, z - .1, z - .01))
    p.add("Disconnect_Housing" + tag, "gunmetal", box(x - .06, x + .06, 1.1, 1.3, z - .05, z)); p.add("Disconnect_Handle" + tag, "amber", box(x - .015, x + .015, 1.12, 1.3, z, z + .05), box(x - .05, x + .05, 1.12, 1.15, z + .05, z + .07))
def fins(p, x0, x1, y0, y1, z0, z1, n, tag="", axis="x"):
    if axis == "x": p.add("Heat_Sink_Fins" + tag, "gunmetal", *[box(x - .004, x + .004, y0, y1, z0, z1) for x in np.linspace(x0, x1, n)])
    else: p.add("Heat_Sink_Fins" + tag, "gunmetal", *[box(x0, x1, y - .004, y + .004, z0, z1) for y in np.linspace(y0, y1, n)])
def iter1():  # open cell rack + inverter drum: two open 3-tier racks of exposed cells, a finned horizontal inverter drum bridging them over the Sprocket bay
    p = Pod("Open_Rack_Inverter_Drum"); ys = [.9, 1.3, 1.7]
    for s, tag in ((-1, "_L"), (1, "_R")):
        xa, xb = (X0, -.45) if s < 0 else (.45, X1); rack(p, xa, xb, ys, ZB + .08, ZF - .2, tag); cells(p, np.linspace(xa + .17, xb - .17, 3), ys, ZB + .12, ZF - .22, tag=tag)
    p.add("Inverter_Drum", "slate", xcyl(-.45, .45, 1.55, -.05, .28, 16)); p.add("Drum_End_Caps", "alloy", xcyl(-.47, -.45, 1.55, -.05, .3, 16), xcyl(.45, .47, 1.55, -.05, .3, 16))
    p.add("Drum_Fins", "gunmetal", *[xcyl(x - .008, x + .008, 1.55, -.05, .34, 16) for x in np.linspace(-.38, .38, 9)])
    p.add("Drum_Saddles", "gunmetal", *[box(x - .03, x + .03, 1.2, 1.3, -.2, .1) for x in (-.4, .4)]); p.add("Saddle_Straps", "amber", *[box(x - .02, x + .02, 1.3, 1.9, .27, .3) for x in (-.3, .3)])
    p.add("Port_Pedestal", "gunmetal", box(-.22, .22, 0, PY - .14, ZB + .1, -.1)); p.add("Port_Column", "gunmetal", box(-.22, .22, PY - .14, PY + .2, ZB + .1, -.13)); port(p, 0, -.1)
    busbar_runs(p, -.25, .9, 2.2, tag="_L"); busbar_runs(p, .13, .9, 2.2, tag="_R"); human(p, X1 - .2, ZF - .07); return p
def iter2():  # swap carriage tower: a single cell column on a vertical rail with a gunmetal carriage that lowers cells to the 0.45 m port; wall-side cell magazine racks
    p = Pod("Swap_Carriage_Tower"); ys = [.15, .5, .85, 1.2, 1.55]
    for s, tag in ((-1, "_L"), (1, "_R")):
        xa, xb = (X0, -.55) if s < 0 else (.55, X1); rack(p, xa, xb, ys, ZB + .05, ZB + .4, tag); cells(p, np.linspace(xa + .17, xb - .17, 3), ys, ZB + .08, ZB + .37, skip={(1, 2), (2, 0)}, tag=tag)
    p.add("Swap_Mast", "gunmetal", *[box(x - .03, x + .03, 0, H, ZB + .05, ZB + .14) for x in (-.4, .4)], box(-.43, .43, H - .08, H, ZB + .05, ZB + .14))
    p.add("Mast_Rails", "alloy", *[box(x - .012, x + .012, .05, H - .1, ZB + .14, ZB + .16) for x in (-.37, .37)])
    p.add("Swap_Carriage", "slate", box(-.36, .36, 1.25, 1.33, ZB + .16, ZF - .15), box(-.36, .36, 1.33, 1.37, ZF - .2, ZF - .15)); cells(p, [0], [1.33], ZB + .2, ZF - .22, tag="_Carried")
    p.add("Carriage_Clamps", "amber", *[box(x - .02, x + .02, 1.33, 1.42, ZF - .2, ZF - .17) for x in (-.15, .15)])
    p.add("Cable_Chain", "gunmetal", *[box(.3, .36, y, y + .05, ZB + .16, ZB + .22) for y in np.arange(.6, 1.25, .07)])
    p.add("Port_Bridge", "gunmetal", box(-.4, .4, PY - .16, PY + .2, ZB + .14, ZB + .3)); port(p, 0, ZB + .3)
    p.add("Overhead_Busway", "alloy", box(X0, X1, 2.0, 2.06, ZB, ZB + .08)); insulators(p, [(x, 2.03) for x in np.linspace(X0 + .2, X1 - .2, 6)]); human(p, X0 + .35, ZB + .55); return p
def iter3():  # transformer drum spine: tall finned transformer drum at the centre, open cell racks either side, heavy busbars bridging overhead into the wall
    p = Pod("Transformer_Drum_Spine"); ys = [.75, 1.15, 1.55]
    for s, tag in ((-1, "_L"), (1, "_R")):
        xa, xb = (X0 + .05, -.55) if s < 0 else (.55, X1 - .05); rack(p, xa, xb, ys, ZB + .1, ZF - .25, tag); cells(p, np.linspace(xa + .17, xb - .17, 3), ys, ZB + .14, ZF - .27, skip={(0, 2)} if s < 0 else {(2, 1)}, tag=tag)
    p.add("Drum_Plinth", "gunmetal", box(-.38, .38, .7, .78, -.33, .33)); p.add("Transformer_Drum", "slate", cyl(0, 0, .3, .78, 1.95, 16)); p.add("Drum_Cap", "alloy", cyl(0, 0, .26, 1.95, 2.0, 16))
    p.add("Radiator_Fins", "gunmetal", *[box(-.006, .006, .85, 1.85, .3, .38) if False else trimesh.Trimesh() for _ in []] or [xf for xf in [box(x - .006, x + .006, .85, 1.85, -.38, .38) for x in (-.33, -.3, .3, .33)]] + [box(-.38, .38, .85, 1.85, z - .006, z + .006) for z in (.3, .33)])
    p.add("Drum_Legs", "gunmetal", *[box(x - .03, x + .03, 0, .7, z - .03, z + .03) for x in (-.33, .33) for z in (-.3, .3)]); p.add("Leg_Clamps", "amber", *[box(x - .05, x + .05, 0, .02, z - .05, z + .05) for x in (-.33, .33) for z in (-.3, .3)])
    p.add("Bushings", "ceramic", *[cyl(x, 0, .035, 2.0, 2.12, 8) for x in (-.15, 0, .15)])
    p.add("Overhead_Busbars", "alloy", *[box(min(x, x * 6), max(x, x * 6) if x else .012, 2.12, 2.15, -.012, .012) if False else box(-1.0, 1.0, 2.12 + k * .0, 2.15, -.012 + z, .012 + z) for k, z in enumerate((-.15, -.08, -.01))], *[box(-.012 + x, .012 + x, 2.12, 2.15, ZB, 0) for x in (-1.0, 1.0)])
    insulators(p, [(x, 2.13) for x in (-1.0, 1.0)]); p.add("Port_Pod", "gunmetal", box(-.25, .25, 0, PY + .22, -.3, .1)); port(p, 0, .1); human(p, X1 - .25, ZF - .07); return p
def iter4():  # stepped cell terrace: cells step down toward the front in three open terraces, a cooling duct along the top into the wall, Sprocket bay cut through the middle
    p = Pod("Stepped_Cell_Terrace"); steps = [(ZB + .05, ZB + .3, 1.85), (ZB + .3, ZB + .55, 1.3), (ZB + .55, ZF - .05, .75)]
    for k, (z0, z1, top) in enumerate(steps):
        for s, tag in ((-1, "_L"), (1, "_R")):
            xa, xb = (X0, -.45) if s < 0 else (.45, X1); t = f"{tag}{k}"
            p.add("Terrace_Frame" + t, "gunmetal", *[box(x - .02, x + .02, 0, top, z - .02, z + .02) for x in (xa + .02, xb - .02) for z in (z0 + .02, z1 - .02)], box(xa, xb, top - .03, top, z0, z1))
            cells(p, np.linspace(xa + .17, xb - .17, 3), [top - .32 - .05], z0 + .03, z1 - .03, tag=t)
    p.add("Cooling_Duct", "alloy", box(X0 + .1, X1 - .1, 1.9, 2.15, ZB, ZB + .22)); p.add("Duct_Bands", "gunmetal", *[box(x - .02, x + .02, 1.88, 2.17, ZB, ZB + .24) for x in np.linspace(X0 + .2, X1 - .2, 6)])
    p.add("Fan_Grilles", "slate", *[cyl_z(x, 2.02, .09, ZB + .22, ZB + .235, 12) for x in (-.7, 0, .7)]); fins(p, -.4, .4, 1.0, 1.75, ZB + .02, ZB + .12, 9)
    p.add("Bay_Back", "gunmetal", box(-.45, .45, 0, .95, ZB, ZB + .2)); port(p, 0, ZB + .2); busbar_runs(p, -.38, .2, 1.85, n=2, tag="_L"); busbar_runs(p, .32, .2, 1.85, n=2, tag="_R")
    human(p, .3, ZB + .2 + .0); return p
def iter5():  # wall-hung cell ladder + floor busway: cells hang on two wall ladders, open below for Sprocket; a floor busway trench with cables up into a finned inverter block
    p = Pod("Wall_Ladder_Floor_Busway"); ys = [1.0, 1.4, 1.8]
    for s, tag in ((-1, "_L"), (1, "_R")):
        xa, xb = (X0, -.15) if s < 0 else (.15, X1)
        p.add("Ladder_Rails" + tag, "gunmetal", *[box(x - .03, x + .03, .8, H, ZB, ZB + .06) for x in (xa + .03, xb - .03)], *[box(xa, xb, y - .03, y, ZB, ZB + .35) for y in ys])
        p.add("Cantilever_Arms" + tag, "gunmetal", *[box(x - .02, x + .02, .82, .98, ZB + .06, ZB + .3) for x in (xa + .08, xb - .08)])
        cells(p, np.linspace(xa + .17, xb - .17, 4), ys, ZB + .06, ZB + .33, skip={(3, 2)} if s < 0 else {(0, 0)}, tag=tag)
    p.add("Wall_Bolts", "amber", *[cyl_z(x, y, .015, ZB + .06, ZB + .07, 6) for x in (X0 + .03, -.18, .18, X1 - .03) for y in (.9, 2.1)])
    p.add("Busway_Trench_Cover", "slate", box(X0, X1, 0, .03, ZB + .4, ZB + .7)); p.add("Trench_Grate_Bars", "gunmetal", *[box(x - .01, x + .01, .03, .04, ZB + .42, ZB + .68) for x in np.linspace(X0 + .1, X1 - .1, 16)])
    p.add("Riser_Cables", "alloy", *[cyl(x, ZB + .55, .025, 0, .7, 8) for x in (-.9, -.8, .8, .9)]); p.add("Inverter_Block", "slate", box(-.15, .15, .7, .78, ZB, ZB + .3))
    p.add("Cable_Saddles", "amber", *[box(x - .06, x + .06, .5, .53, ZB + .5, ZB + .6) for x in (-.85, .85)])
    p.add("Port_Stand", "gunmetal", box(-.2, .2, 0, PY - .14, ZB, ZB + .3), box(-.2, .2, PY - .14, PY + .2, ZB, ZB + .2)); port(p, 0, ZB + .2)
    fins(p, X0 + .1, X1 - .1, .2, .65, ZB, ZB + .1, 7, axis="y") if False else fins(p, -.9, -.3, .1, .62, ZB, ZB + .12, 8); fins(p, .3, .9, .1, .62, ZB, ZB + .12, 8, tag="_R")
    human(p, 0, ZB + .2); return p
def main():
    os.makedirs(OUT, exist_ok=True); isos = []
    for i, fn in enumerate([iter1, iter2, iter3, iter4, iter5], 1):
        p = fn(); full = dict(p.P); p.P = {k: v for k, v in full.items() if v[0] != "glass"}  # glass hidden in sheet renders (BLEND in glb)
        tris, iso, lo, hi, bad = wg.sheet(p, os.path.join(OUT, f"iter_0{i}_sheet.png"), f"iter_0{i}  {p.name}  (#42 substation, round 2)")
        p.P = full; gp = os.path.join(OUT, f"iter_0{i}.glb"); tris, _ = export_final(p.P, [gp]); set_glass_blend(gp)
        isos.append((p.name, iso)); print(i, p.name, tris, (hi - lo).round(3), "bad", bad)
    fig, axs = plt.subplots(3, 2, figsize=(16, 12), facecolor="#F4F2EC")
    for ax in axs.flat: ax.axis("off")
    for ax, (i, (n, im)) in zip(axs.flat, enumerate(isos, 1)): ax.imshow(im); ax.set_title(f"{i}. {n}", fontsize=11, color="#555")
    plt.tight_layout(rect=(0, 0, 1, .97)); fig.savefig(os.path.join(OUT, "overview.png"), dpi=90, facecolor="#F4F2EC"); plt.close(fig)
if __name__ == "__main__": main()
