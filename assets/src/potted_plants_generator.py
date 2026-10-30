"""Rev C #34 potted plants set (102, 203; qty 2 sets; 0.4-0.7 m each). Five iterations, family language.
Bottom-centre pivot, front +Z. Spin-down: every pot is latched or clipped to a clamped base or rail; soil sealed under slate grow lids.
Foliage reuses the hydro planter's matte leaf greens (not emissive)."""
import os, sys, numpy as np, trimesh
sys.path.insert(0, os.path.dirname(__file__))
import hydro_planter_generator as hp
from hydro_planter_generator import bush, cyl, box, bev, blk, Pod, dc, wg, plt
OUT = os.path.join(dc.ROOT, "design/assets/potted_plants")

def pot(p, x, z, r, h, y0=0.0, mat="white", seg=12):
    p.add("Pots", mat, cyl(x, z, r, y0, y0 + h, seg))
    p.add("Grow_Lids", "slate", cyl(x, z, r * .9, y0 + h, y0 + h + .008, seg))
    p.add("Pot_Latches", "amber", box(x - .015, x + .015, y0 + h - .03, y0 + h - .01, z + r - .002, z + r + .006))
def plant(p, x, z, y, size, tall=False, mat="leaf"):
    if tall:
        p.add("Stems", "gunmetal", cyl(x, z, .012, y, y + size * 1.0, 6))
        p.add("Foliage", "leaf", bush(x, y + size * .85, z, size * .5), bush(x + .03, y + size * .45, z - .02, size * .45))
    else:
        p.add("Foliage" if mat == "leaf" else "Foliage_Light", mat, bush(x, y, z, size * .5, mat))
def clamp_ring(p, x, z, r):
    p.add("Clamp_Rings", "gunmetal", cyl(x, z, r + .03, 0, .02, 12))
    p.add("Clamp_Bolts", "alloy", *[cyl(x + (r + .015) * np.cos(a), z + (r + .015) * np.sin(a), .007, .02, .028, 6) for a in (0, 2.1, 4.2)])

def iter1():  # moulded trio: three white round pots on bolted clamp rings
    p = Pod("Moulded_Trio")
    for x, r, h, s, t in ((-.32, .13, .26, .26, False), (0, .15, .3, .2, True), (.34, .11, .22, .3, False)):
        clamp_ring(p, x, 0, r); pot(p, x, 0, r, h, .02); plant(p, x, 0, h + .03, s, t, "leaf" if x <= 0 else "leaf2")
    return p
def iter2():  # rail cradles: four pots in gunmetal cradles hooked on a bolted alloy wall rail at 0.30 m, floor clear
    p = Pod("Rail_Cradles")
    p.add("Wall_Rail", "alloy", blk(-.6, .6, .28, .32, -.12, -.09, .006, 1))
    p.add("Wall_Plates", "gunmetal", *[box(x - .05, x + .05, .24, .36, -.125, -.12) for x in (-.55, .55)])
    for i, x in enumerate((-.45, -.15, .15, .45)):
        p.add("Cradles", "gunmetal", box(x - .1, x + .1, .2, .23, -.09, .1)); p.add("Cradle_Hooks", "gunmetal", box(x - .03, x + .03, .23, .34, -.09, -.07))
        pot(p, x, 0, .09, .16, .23); plant(p, x, 0, .4, .22, i % 2 == 1, "leaf" if i % 2 == 0 else "leaf2")
    return p
def iter3():  # shared tray: four pots latched into one slate tray with a violet water gauge, floor-clamped
    p = Pod("Shared_Tray")
    p.add("Tray", "slate", bev(1.1, .4, 0, .06, .03, .01, 2, 0, 0)); p.add("Water_Gauge", "violet", box(.3, .45, .02, .045, .2, .204))
    p.add("Floor_Clamps", "gunmetal", *[box(x - .05, x + .05, 0, .02, z - .04, z + .04) for x in (-.5, .5) for z in (-.15, .15)])
    for i, (x, r, h) in enumerate(((-.38, .1, .2), (-.12, .12, .28), (.14, .11, .24), (.39, .09, .18))):
        pot(p, x, 0, r, h, .06); plant(p, x, 0, h + .07, .2 + .05 * (i % 2), i == 1, "leaf" if i % 2 == 0 else "leaf2")
    return p
def iter4():  # pocket column: one 0.65 m banded column with three side pockets, plus two small clamped pots
    p = Pod("Pocket_Column")
    clamp_ring(p, -.15, 0, .14); p.add("Column", "white", cyl(-.15, 0, .14, .02, .46, 12)); p.add("Column_Bands", "alloy", *[cyl(-.15, 0, .145, y, y + .02, 12) for y in (.16, .32)])
    for y, a in ((.14, .5), (.28, 2.6), (.42, 4.6)):
        x, z = -.15 + .17 * np.cos(a), .17 * np.sin(a); p.add("Pockets", "white", box(x - .05, x + .05, y - .06, y, z - .05, z + .05)); plant(p, x, z, y, .14, False, "leaf2")
    p.add("Grow_Lids", "slate", cyl(-.15, 0, .12, .46, .468, 12)); plant(p, -.15, 0, .47, .2, True)
    for x in (.2, .42): clamp_ring(p, x, .05, .08); pot(p, x, .05, .08, .16, .02); plant(p, x, .05, .19, .18)
    return p
def iter5():  # Sprocket wick base: three pots on a reservoir plinth; Sprocket tops it up through a port at 0.45 m
    p = Pod("Sprocket_Wick")
    p.add("Plinth", "white", bev(1.0, .36, 0, .14, .03, .01, 3, 0, 0)); p.add("Plinth_Clamps", "gunmetal", *[box(x - .05, x + .05, 0, .02, -.2, .2) for x in (-.45, .45)])
    p.add("Port_Post", "gunmetal", bev(.16, .16, .14, .55, .02, .006, 2, .4, .08)); p.add("Sprocket_Port", "alloy", box(.35, .45, .4, .5, .16, .17))
    p.add("Port_Ring", "amber", box(.38, .42, .43, .47, .17, .174)); p.add("Wick_Status", "green", box(.36, .44, .52, .53, .16, .164))
    for i, (x, r, h) in enumerate(((-.3, .12, .26), (-.02, .1, .2), (.18, .08, .16))):
        pot(p, x, -.02, r, h, .14); plant(p, x, -.02, .14 + h + .01, .22, i == 0, "leaf" if i != 1 else "leaf2")
    return p

def main():
    os.makedirs(OUT, exist_ok=True); isos = []
    for i, fn in enumerate([iter1, iter2, iter3, iter4, iter5], 1):
        p = fn(); tris, iso, lo, hi, bad = wg.sheet(p, os.path.join(OUT, f"iter_0{i}_sheet.png"), f"iter_0{i}  {p.name}  (#34 potted plants set)")
        isos.append((p.name, iso)); print(i, p.name, tris, (hi - lo).round(3), "bad", bad)
    fig, axs = plt.subplots(3, 2, figsize=(16, 12), facecolor="#F4F2EC")
    for ax in axs.flat: ax.axis("off")
    for ax, (i, (n, im)) in zip(axs.flat, enumerate(isos, 1)): ax.imshow(im); ax.set_title(f"{i}. {n}", fontsize=11, color="#555")
    plt.tight_layout(rect=(0, 0, 1, .97)); fig.savefig(os.path.join(OUT, "overview.png"), dpi=90, facecolor="#F4F2EC"); plt.close(fig)

# ---------- finals (Jared picked both #1 Moulded_Trio and #4 Pocket_Column; default one set per room, 102 and 203) ----------
def final_trio():
    p = iter1(); p.name = "Potted_Moulded_Trio"; return p
def final_column():
    p = iter4(); p.name = "Potted_Pocket_Column"
    for y, a in ((.14, .5), (.28, 2.6), (.42, 4.6)):
        x, z = -.15 + .17 * np.cos(a), .17 * np.sin(a)
        p.add("Pocket_Lids", "slate", box(x - .045, x + .045, y, y + .006, z - .045, z + .045))
        p.add("Pocket_Latches", "amber", box(x - .012, x + .012, y - .03, y - .01, z + .05, z + .056))
    for n, (mk, m) in p.P.items(): m.apply_translation((-.0825, 0, .0335))  # recentre to bottom-centre pivot
    return p
def final_main():
    from dining_chair_generator import export_final
    for fn, gname, sname, title in ((final_trio, "potted_plants_moulded_trio.glb", "final_moulded_trio_sheet.png", "Final  #34 potted plants, Moulded Trio"),
                                    (final_column, "potted_plants_pocket_column.glb", "final_pocket_column_sheet.png", "Final  #34 potted plants, Pocket Column")):
        p = fn(); tris, geo = export_final(p.P, [os.path.join(dc.ROOT, "godot/assets/models", gname)])
        V = np.vstack([g[1] for g in geo.values()]); bad = [n for n, (mk, m) in p.P.items() if not all(c.is_watertight for c in m.split(only_watertight=False))]
        print(gname, "tris", tris, "lo", V.min(0).round(3), "hi", V.max(0).round(3), "bad", bad)
        sp = os.path.join(OUT, sname); wg.sheet(p, sp, title); os.remove(sp.replace("_sheet.png", ".glb"))
if __name__ == "__main__":
    final_main() if len(sys.argv) > 1 and sys.argv[1] == "final" else main()
