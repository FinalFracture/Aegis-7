"""Rev C #29 specimen shelf (room 104, the researcher's room; qty 1; 0.9 W x 0.6 D x 1.9 H). Five iterations, family language.
Bottom-centre pivot, front +Z, wall at -Z. Spin-down: specimens sit in clipped jars or foam-cut trays behind latched glass or slate doors; the frame clamps to the floor and hooks onto the 2.06 m wall rail."""
import os, sys, numpy as np, trimesh
sys.path.insert(0, os.path.dirname(__file__))
from dining_chair_generator import export_final
from bath_pod_generator import set_glass_blend
from hydro_planter_generator import cyl, box, bev, blk, Pod, dc, wg, plt
OUT = os.path.join(dc.ROOT, "design/assets/specimen_shelf")
W, D, H = .9, .6, 1.9; ZB, ZF = -D / 2, D / 2
rng = np.random.default_rng(29)

def rock(x, y, z, r):
    m = trimesh.creation.icosphere(0, r); m.vertices *= [1, .7, 1]; m.vertices += rng.normal(0, r * .1, m.vertices.shape)
    m.apply_translation((x, y + r * .6, z)); m.metadata["uv"] = m.vertices[:, [0, 2]]; return m
def jars(p, y, xs, z=0.0, r=.045, h=.16):
    p.add("Jars", "white", *[cyl(x, z, r, y, y + h, 10) for x in xs])
    p.add("Jar_Caps", "gunmetal", *[cyl(x, z, r + .004, y + h, y + h + .02, 10) for x in xs])
    p.add("Jar_Clips", "amber", *[box(x - .012, x + .012, y + .02, y + .05, z + r, z + r + .006) for x in xs])
def samples(p, y, xs, z=0.0):
    p.add("Foam_Trays", "slate", *[box(x - .09, x + .09, y, y + .03, z - .1, z + .1) for x in xs])
    p.add("Rock_Samples", "alloy", *[rock(x + dx, y + .02, z + dz, .035) for x in xs for dx, dz in ((-.04, -.03), (.04, .03))])
def anchors(p):
    p.add("Floor_Clamps", "gunmetal", *[box(x - .05, x + .05, 0, .02, z - .04, z + .04) for x in (-.36, .36) for z in (ZB + .06, ZF - .06)])
    p.add("Rail_Hooks", "gunmetal", *[box(x - .05, x + .05, 2.0 - .06 if H > 1.95 else H - .06, H, ZB - .03, ZB) for x in (-.3, .3)])

SH = (.06, .48, .9, 1.32)  # shelf levels
def carcass(p, y0=0.0, y1=H, mat="white"):
    p.add("Carcass_Sides", mat, *[box(x - .015, x + .015, y0, y1, ZB, ZF - .02) for x in (-W / 2 + .015, W / 2 - .015)])
    p.add("Carcass_Back", mat, box(-W / 2, W / 2, y0, y1, ZB, ZB + .02)); p.add("Carcass_Top", mat, bev(W, D - .02, y1 - .03, y1, .02, .006, 1, 0, -.01))
def iter1():  # glass cabinet: white carcass, four shelves, two latched glass doors, jars up top and rock trays below
    p = Pod("Glass_Cabinet"); carcass(p)
    p.add("Shelves", "slate", *[box(-W / 2 + .03, W / 2 - .03, y, y + .02, ZB + .02, ZF - .03) for y in SH])
    for y in SH[2:]: jars(p, y + .02, (-.28, -.09, .1, .29))
    for y in SH[:2]: samples(p, y + .02, (-.2, .2))
    p.add("Glass_Doors", "glass", *[box(x0, x1, .04, H - .04, ZF - .02, ZF - .008) for x0, x1 in ((-W / 2 + .02, -.005), (.005, W / 2 - .02))])
    p.add("Door_Latches", "amber", *[box(x - .015, x + .015, .95, 1.05, ZF - .008, ZF) for x in (-.03, .03)]); anchors(p); return p
def iter2():  # open rack: alloy frame, slate shelves, flip-down restraint bars with amber latches
    p = Pod("Open_Rack")
    p.add("Posts", "alloy", *[blk(x - .02, x + .02, 0, H, z - .02, z + .02, .004, 1) for x in (-W / 2 + .02, W / 2 - .02) for z in (ZB + .02, ZF - .02)])
    p.add("Shelves", "slate", *[box(-W / 2 + .03, W / 2 - .03, y, y + .02, ZB + .02, ZF - .02) for y in SH + (1.74,)])
    for y in SH[2:]: jars(p, y + .02, (-.28, -.09, .1, .29))
    for y in SH[:2]: samples(p, y + .02, (-.2, .2))
    p.add("Restraint_Bars", "gunmetal", *[box(-W / 2 + .03, W / 2 - .03, y + .2, y + .22, ZF - .04, ZF - .02) for y in SH])
    p.add("Bar_Latches", "amber", *[box(W / 2 - .06, W / 2 - .03, y + .19, y + .23, ZF - .02, ZF - .012) for y in SH]); anchors(p); return p
def iter3():  # drawer tower: flat specimen drawers below (violet label strips), latched glass case above
    p = Pod("Drawer_Tower"); carcass(p)
    for i in range(6):
        y = .04 + i * .14; p.add("Drawer_Fronts", "slate", box(-W / 2 + .03, W / 2 - .03, y, y + .12, ZF - .03, ZF - .01))
        p.add("Drawer_Labels", "violet", box(-.12, .12, y + .08, y + .095, ZF - .01, ZF - .006)); p.add("Drawer_Latches", "amber", box(-.02, .02, y + .03, y + .06, ZF - .01, ZF - .004))
    p.add("Shelves", "slate", *[box(-W / 2 + .03, W / 2 - .03, y, y + .02, ZB + .02, ZF - .03) for y in (.9, 1.32)])
    for y in (.9, 1.32): jars(p, y + .02, (-.28, -.09, .1, .29))
    p.add("Glass_Doors", "glass", box(-W / 2 + .02, W / 2 - .02, .9, H - .04, ZF - .02, ZF - .008)); p.add("Door_Latches", "amber", box(-.02, .02, 1.3, 1.4, ZF - .008, ZF)); anchors(p); return p
def iter4():  # rail case: a shallow 0.35 m glass case hung from the 2.06 m wall rail, floor clear below 0.6 m
    p = Pod("Rail_Case"); d = .35; z0, z1 = ZB, ZB + d
    p.add("Wall_Rail", "alloy", blk(-W / 2 - .05, W / 2 + .05, 2.04, 2.08, z0 - .03, z0, .006, 1))
    p.add("Rail_Hooks", "gunmetal", *[box(x - .05, x + .05, 1.9, 2.08, z0, z0 + .02) for x in (-.3, .3)])
    p.add("Case_Sides", "white", *[box(x - .015, x + .015, .6, H, z0, z1) for x in (-W / 2 + .015, W / 2 - .015)])
    p.add("Case_Back", "white", box(-W / 2, W / 2, .6, H, z0, z0 + .02)); p.add("Case_Top", "white", box(-W / 2, W / 2, H - .03, H, z0, z1)); p.add("Case_Floor", "white", box(-W / 2, W / 2, .6, .63, z0, z1)); p.add("Case_Base_Light", "violet", box(-.35, .35, .59, .6, z0 + .05, z1 - .05))
    p.add("Shelves", "slate", *[box(-W / 2 + .03, W / 2 - .03, y, y + .02, z0 + .02, z1 - .03) for y in (.66, 1.06, 1.46)])
    for y in (1.06, 1.46): jars(p, y + .02, (-.28, -.09, .1, .29), z0 + d / 2, .04, .14)
    samples(p, .68, (-.2, .2), z0 + d / 2 - .05)
    p.add("Glass_Doors", "glass", box(-W / 2 + .02, W / 2 - .02, .62, H - .04, z1, z1 + .012)); p.add("Door_Latches", "amber", box(-.02, .02, 1.2, 1.3, z1 + .012, z1 + .018))
    return p
def iter5():  # Sprocket sorter: glass cabinet over a sample intake drawer at 0.45 m where Sprocket delivers field samples
    p = Pod("Sprocket_Sorter"); carcass(p)
    p.add("Intake_Drawer", "gunmetal", box(-W / 2 + .03, W / 2 - .03, .3, .6, ZF - .03, ZF - .01)); p.add("Sprocket_Port", "alloy", box(-.06, .06, .42, .48, ZF - .01, ZF))
    p.add("Intake_Status", "green", box(-.2, .2, .55, .56, ZF - .01, ZF - .006)); p.add("Base_Plinth", "slate", box(-W / 2 + .03, W / 2 - .03, .02, .3, ZF - .03, ZF - .01))
    p.add("Shelves", "slate", *[box(-W / 2 + .03, W / 2 - .03, y, y + .02, ZB + .02, ZF - .03) for y in (.64, 1.0, 1.36)])
    jars(p, .66, (-.28, -.09, .1, .29)); samples(p, 1.02, (-.2, .2)); jars(p, 1.38, (-.28, -.09, .1, .29))
    p.add("Glass_Doors", "glass", box(-W / 2 + .02, W / 2 - .02, .62, H - .04, ZF - .02, ZF - .008)); p.add("Door_Latches", "amber", box(-.02, .02, 1.1, 1.2, ZF - .008, ZF)); anchors(p); return p

def main():
    os.makedirs(OUT, exist_ok=True); isos = []
    for i, fn in enumerate([iter1, iter2, iter3, iter4, iter5], 1):
        p = fn(); full = dict(p.P); p.P = {k: v for k, v in full.items() if v[0] != "glass"}  # glass hidden in sheet renders (BLEND in glb)
        tris, iso, lo, hi, bad = wg.sheet(p, os.path.join(OUT, f"iter_0{i}_sheet.png"), f"iter_0{i}  {p.name}  (#29 specimen shelf, glass doors hidden)")
        p.P = full; gp = os.path.join(OUT, f"iter_0{i}.glb"); tris, _ = export_final(p.P, [gp]); set_glass_blend(gp)
        isos.append((p.name, iso)); print(i, p.name, tris, (hi - lo).round(3), "bad", bad)
    fig, axs = plt.subplots(3, 2, figsize=(16, 12), facecolor="#F4F2EC")
    for ax in axs.flat: ax.axis("off")
    for ax, (i, (n, im)) in zip(axs.flat, enumerate(isos, 1)): ax.imshow(im); ax.set_title(f"{i}. {n}", fontsize=11, color="#555")
    plt.tight_layout(rect=(0, 0, 1, .97)); fig.savefig(os.path.join(OUT, "overview.png"), dpi=90, facecolor="#F4F2EC"); plt.close(fig)

# ---------- final (Jared, Oct 29): #2 Open_Rack, moved OUT of residential 104 to a future science/lab building ----------
def final_rack():
    p = iter2(); p.name = "Specimen_Rack_Open_Lab"
    xs = (-W / 2 + .02, W / 2 - .02)
    p.add("Bar_Hinges", "gunmetal", *[cyl(x, ZF - .03, .014, y + .19, y + .23, 8) for x in (-W / 2 + .045,) for y in SH])
    p.add("Post_Bolts", "alloy", *[cyl(x, z, .008, .02, .03, 6) for x in xs for z in (ZB + .02, ZF - .02)])
    p.add("Shelf_Lips", "gunmetal", *[box(-W / 2 + .03, W / 2 - .03, y + .02, y + .04, ZB + .02, ZB + .03) for y in SH + (1.74,)])
    p.add("Tray_Clips", "amber", *[box(x - .012, x + .012, y + .022, y + .052, .1, .106) for y in SH[:2] for x in (-.2, .2)])
    return p
def final_main():
    p = final_rack(); gp = os.path.join(dc.ROOT, "godot/assets/models/specimen_rack_open_lab.glb"); tris, geo = export_final(p.P, [gp])
    V = np.vstack([g[1] for g in geo.values()]); bad = [n for n, (mk, m) in p.P.items() if not all(c.is_watertight for c in m.split(only_watertight=False))]
    print("tris", tris, "lo", V.min(0).round(3), "hi", V.max(0).round(3), "bad", bad)
    sp = os.path.join(OUT, "final_open_rack_lab_sheet.png"); wg.sheet(p, sp, "Final  specimen rack, Open Rack (LAB BUILDING asset, not residential)"); os.remove(sp.replace("_sheet.png", ".glb"))
if __name__ == "__main__":
    final_main() if len(sys.argv) > 1 and sys.argv[1] == "final" else main()
