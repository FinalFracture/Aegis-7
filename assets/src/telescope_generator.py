"""Rev C #30 telescope (room 104; qty 1; 0.6 x 0.6 x 1.5 m). Five iterations, family language.
A resident's hobby telescope aimed at the window. Pivot at the bottom-centre of the footprint, +Z front (toward the view).
Spin-down: the feet clamp to floor rail sockets with amber latches, and the tube locks into its cradle; no loose parts."""
import os, sys, numpy as np, trimesh
sys.path.insert(0, os.path.dirname(__file__))
from hydro_planter_generator import cyl, box, bev, blk, Pod, dc, wg, plt
from dining_chair_generator import export_final
from bath_pod_generator import set_glass_blend
OUT = os.path.join(dc.ROOT, "design/assets/telescope")

def rod(a, b, r, n=8):
    a, b = np.asarray(a, float), np.asarray(b, float)
    m = trimesh.creation.cylinder(radius=r, segment=[a, b], sections=n); m.metadata["uv"] = m.vertices[:, [0, 1]]; return m
def tilt(base, ang, L):  # point L along a tube pitched ang (rad) up from +Z, starting at base
    return np.asarray(base, float) + L * np.array([0, np.sin(ang), np.cos(ang)])
def feet(p, pts):
    p.add("Floor_Clamps", "gunmetal", *[blk(x - .04, x + .04, 0, .025, z - .04, z + .04, .004, 1) for x, z in pts])
    p.add("Clamp_Latches", "amber", *[box(x - .012, x + .012, .025, .035, z - .03, z - .01) for x, z in pts])
def tripod(p, top, spread=.26, r=.014):
    pts = [(spread * np.sin(a), spread * np.cos(a)) for a in np.radians((0, 120, 240))]
    p.add("Tripod_Legs", "alloy", *[rod((x, .025, z), top, r, 6) for x, z in pts]); feet(p, pts)
    p.add("Leg_Spreader", "gunmetal", *[rod((x * .4, top[1] * .45, z * .4), (0, top[1] * .45, 0), .008, 6) for x, z in pts])
def tube(p, base, ang, L, r, mat="white", glass=True):
    c = np.asarray(base, float); f = tilt(c, ang, L * .62); b = tilt(c, ang, -L * .38)
    p.add("Tube", mat, rod(b, f, r, 12)); p.add("Dew_Shield", "gunmetal", rod(f, tilt(f, ang, .08), r * 1.12, 12))
    p.add("Focuser", "alloy", rod(b, tilt(b, ang, -.06), r * .35, 8)); p.add("Eyepiece", "gunmetal", rod(tilt(b, ang, -.04), tilt(b, ang, -.04) + np.array([0, .07, 0]), r * .25, 8))
    p.add("Finder", "alloy", rod(tilt(c, ang, .05) + np.array([0, r + .025, 0]), tilt(c, ang, .25) + np.array([0, r + .025, 0]), .015, 8))
    p.add("Tube_Rings", "gunmetal", *[rod(tilt(c, ang, s - .015), tilt(c, ang, s + .015), r * 1.08, 12) for s in (-.12, .12)])
    if glass: p.add("Objective_Glass", "glass", rod(tilt(f, ang, .07), tilt(f, ang, .075), r * .98, 12))
def mount(p, at):
    x, y, z = at; p.add("Mount_Head", "gunmetal", blk(x - .06, x + .06, y - .1, y, z - .06, z + .06, .006, 1))
    p.add("Lock_Knobs", "amber", *[rod((x + s * .06, y - .05, z), (x + s * .085, y - .05, z), .015, 8) for s in (-1, 1)])

A, L, R = .87, .7, .055
def iter1():  # tripod refractor: classic white refractor on an alloy tripod with clamped feet
    p = Pod("Tripod_Refractor"); tripod(p, (0, .93, 0)); mount(p, (0, 1.03, 0)); tube(p, (0, 1.05, 0), A, L, R); return p
def iter2():  # pier dobsonian: square gunmetal pier box with a rocker cradle, short fat slate tube
    p = Pod("Pier_Dobsonian"); feet(p, [(-.22, -.22), (.22, -.22), (-.22, .22), (.22, .22)])
    p.add("Pier_Base", "gunmetal", blk(-.25, .25, .025, .07, -.25, .25, .006, 1)); p.add("Pier_Column", "white", bev(.24, .24, .07, .8, .03, .006, 2, 0, 0))
    p.add("Rocker_Box", "slate", *[box(s * .13 - .015, s * .13 + .015, .8, 1.05, -.12, .12) for s in (-1, 1)]); p.add("Rocker_Floor", "slate", box(-.145, .145, .8, .83, -.12, .12))
    tube(p, (0, 1.0, 0), A, .62, .1, "slate"); return p
def iter3():  # truss reflector: open alloy truss tube on a white pier, mirror cell at the bottom
    p = Pod("Truss_Reflector"); feet(p, [(-.2, -.2), (.2, -.2), (-.2, .2), (.2, .2)])
    p.add("Pier_Base", "gunmetal", blk(-.23, .23, .025, .06, -.23, .23, .006, 1)); p.add("Pier_Column", "white", cyl(0, 0, .07, .06, .95, 10)); mount(p, (0, 1.03, 0))
    c = np.array([0, 1.08, 0]); b, f = tilt(c, A, -.25), tilt(c, A, .4)
    p.add("Mirror_Cell", "gunmetal", rod(tilt(b, A, -.06), b, .1, 12)); p.add("Top_Ring", "white", rod(f, tilt(f, A, .06), .1, 12))
    p.add("Truss_Poles", "alloy", *[rod(b + .085 * np.array([np.cos(t), np.sin(t) * np.cos(A), -np.sin(t) * np.sin(A)]), f + .085 * np.array([np.cos(t), np.sin(t) * np.cos(A), -np.sin(t) * np.sin(A)]), .008, 6) for t in np.radians((45, 135, 225, 315))])
    p.add("Eyepiece", "gunmetal", rod(tilt(f, A, .03) + np.array([.1, 0, 0]), tilt(f, A, .03) + np.array([.16, 0, 0]), .015, 8)); return p
def iter4():  # rail column: telescope on a floor-rail column with a counter-rotation ring (amber) to hold aim against the spin
    p = Pod("Rail_Column"); p.add("Floor_Rail", "gunmetal", blk(-.3, .3, 0, .03, -.06, .06, .004, 1)); p.add("Rail_Latches", "amber", *[box(x - .02, x + .02, .03, .04, .03, .06) for x in (-.24, .24)])
    p.add("Column_Foot", "alloy", blk(-.1, .1, .03, .08, -.1, .1, .006, 1)); p.add("Column", "white", cyl(0, 0, .045, .08, .9, 10))
    p.add("Counter_Ring", "amber", rod((0, .9, 0), (0, .94, 0), .09, 14)); mount(p, (0, 1.03, 0)); tube(p, (0, 1.05, 0), A, L, R); return p
def iter5():  # stow tripod: tripod with a side cradle; tube shown parked vertical, locked by a strap
    p = Pod("Stow_Tripod"); tripod(p, (0, .8, 0)); mount(p, (0, .9, 0))
    p.add("Stow_Cradle", "gunmetal", box(-.04, .04, .9, 1.4, -.1, -.07)); p.add("Cradle_Strap", "amber", rod((0, 1.2, -.07), (0, 1.22, -.07), .07, 10))
    tube(p, (0, 1.04, 0), 1.45, .62, R); return p

def main():
    os.makedirs(OUT, exist_ok=True); isos = []
    for i, fn in enumerate([iter1, iter2, iter3, iter4, iter5], 1):
        p = fn(); full = dict(p.P); p.P = {k: v for k, v in full.items() if v[0] != "glass"}  # glass hidden in sheet renders (BLEND in glb)
        tris, iso, lo, hi, bad = wg.sheet(p, os.path.join(OUT, f"iter_0{i}_sheet.png"), f"iter_0{i}  {p.name}  (#30 telescope)")
        p.P = full; gp = os.path.join(OUT, f"iter_0{i}.glb"); tris, _ = export_final(p.P, [gp]); set_glass_blend(gp)
        isos.append((p.name, iso)); print(i, p.name, tris, (hi - lo).round(3), "bad", bad)
    fig, axs = plt.subplots(3, 2, figsize=(16, 12), facecolor="#F4F2EC")
    for ax in axs.flat: ax.axis("off")
    for ax, (i, (n, im)) in zip(axs.flat, enumerate(isos, 1)): ax.imshow(im); ax.set_title(f"{i}. {n}", fontsize=11, color="#555")
    plt.tight_layout(rect=(0, 0, 1, .97)); fig.savefig(os.path.join(OUT, "overview.png"), dpi=90, facecolor="#F4F2EC"); plt.close(fig)
def final_dob(ang=.98, L=.58):
    p = Pod("Telescope_Pier_Dobsonian"); feet(p, [(-.22, -.22), (.22, -.22), (-.22, .22), (.22, .22)])
    p.add("Pier_Base", "gunmetal", blk(-.25, .25, .025, .07, -.25, .25, .006, 1)); p.add("Pier_Column", "white", bev(.24, .24, .07, .8, .03, .006, 2, 0, 0))
    p.add("Rocker_Box", "slate", *[box(s * .13 - .015, s * .13 + .015, .8, 1.05, -.12, .12) for s in (-1, 1)]); p.add("Rocker_Floor", "slate", box(-.145, .145, .8, .83, -.12, .12))
    tube(p, (0, 1.0, 0), ang, L, .1, "slate")
    p.add("Altitude_Bearings", "alloy", *[rod((s * .115, 1.0, 0), (s * .16, 1.0, 0), .045, 12) for s in (-1, 1)]); p.add("Altitude_Locks", "amber", *[rod((s * .16, 1.0, 0), (s * .175, 1.0, 0), .02, 8) for s in (-1, 1)])
    p.add("Azimuth_Ring", "alloy", cyl(0, 0, .16, .8, .812, 14)); p.add("Pier_Door_Seam", "gunmetal", box(-.07, .07, .3, .6, .12, .123)); p.add("Pier_Status_Light", "green", box(-.02, .02, .65, .66, .12, .124))
    p.add("Base_Bolts", "alloy", *[cyl(x, z, .01, .07, .08, 6) for x in (-.2, .2) for z in (-.2, .2)])
    return p
def final_main():
    p = final_dob(); gp = os.path.join(dc.ROOT, "godot/assets/models/telescope_pier_dobsonian.glb"); tris, geo = export_final(p.P, [gp]); set_glass_blend(gp)
    V = np.vstack([g[1] for g in geo.values()]); bad = [n for n, (mk, m) in p.P.items() if not all(c.is_watertight for c in m.split(only_watertight=False))]
    print("tris", tris, "lo", V.min(0).round(3), "hi", V.max(0).round(3), "size", (V.max(0) - V.min(0)).round(3), "bad", bad)
    p.P.pop("Objective_Glass", None); sp = os.path.join(OUT, "final_pier_dobsonian_sheet.png"); wg.sheet(p, sp, "Final  #30 telescope, Pier Dobsonian (glass hidden)"); os.remove(sp.replace("_sheet.png", ".glb"))
if __name__ == "__main__":
    final_main() if len(sys.argv) > 1 and sys.argv[1] == "final" else main()
