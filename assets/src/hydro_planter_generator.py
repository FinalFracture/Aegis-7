"""Rev C #33 hydro planter (window/balcony; 103, 202; qty 2; 4.0 W x 0.4 D x 0.6 H). Five iterations, family language.
Bottom-centre pivot, front +Z (window/wall at -Z). Spin-down: sealed reservoirs, latched grow lids, plants held in clipped net cups.
Foliage is low-poly closed clusters in a matte leaf green (not emissive)."""
import os, sys, numpy as np, trimesh
sys.path.insert(0, os.path.dirname(__file__))
import dining_chair_generator as dc
from dining_chair_generator import FMAT
from bath_pod_generator import blk, cyl, Pod
from kitchen_counter_generator import bev, box
from trimesh.visual.material import PBRMaterial as _PBR
import wardrobe_generator as wg
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
FMAT["leaf"] = _PBR(name="LeafGreen", baseColorFactor=(0.30, 0.52, 0.32, 1), metallicFactor=0.0, roughnessFactor=0.8)
FMAT["leaf2"] = _PBR(name="LeafGreenLight", baseColorFactor=(0.45, 0.66, 0.38, 1), metallicFactor=0.0, roughnessFactor=0.8)
OUT = os.path.join(dc.ROOT, "design/assets/hydro_planter")
W, D, H = 4.0, .4, .6; ZB, ZF = -.2, .2
rng = np.random.default_rng(7)

def bush(x, y, z, r, mat="leaf"):
    m = trimesh.creation.icosphere(1, r); m.vertices *= [1, .8, 1]; m.vertices += rng.normal(0, r * .08, m.vertices.shape) * [1, 1, 1]
    m.apply_translation((x, y + r * .7, z)); m.metadata["uv"] = m.vertices[:, [0, 2]]; return m
def plants(p, xs, y, z=0.0, r=.1):
    a = [bush(x, y, z, r * (0.8 + .4 * rng.random()), "leaf") for i, x in enumerate(xs) if i % 2 == 0]
    b = [bush(x, y, z, r * (0.8 + .4 * rng.random()), "leaf2") for i, x in enumerate(xs) if i % 2 == 1]
    p.add("Foliage", "leaf", *a); p.add("Foliage_Light", "leaf2", *b)
    p.add("Net_Cups", "gunmetal", *[cyl(x, z, .035, y - .02, y + .01, 10) for x in xs])
def lid(p, x0, x1, y, z0=ZB + .03, z1=ZF - .03, name="Grow_Lid"):
    p.add(name, "slate", box(x0, x1, y - .01, y + .006, z0, z1))
    p.add("Lid_Latches", "amber", *[box(x - .02, x + .02, y - .012, y - .004, z1, z1 + .006) for x in np.linspace(x0 + .15, x1 - .15, max(2, int((x1 - x0) / .9)))])
def clamps(p, xs):
    p.add("Floor_Clamps", "gunmetal", *[box(x - .06, x + .06, 0, .02, z - .05, z + .05) for x in xs for z in (ZB + .06, ZF - .06)])

def iter1():  # moulded white trough, sealed reservoir, latched slate grow lid, floor-clamped
    p = Pod("Moulded_Trough")
    p.add("Trough", "white", bev(W, D, .03, .36, .04, .012, 3, 0, 0)); p.add("Plinth", "gunmetal", bev(W - .1, D - .1, 0, .03, .02, .006, 1, 0, 0))
    lid(p, -W / 2 + .04, W / 2 - .04, .36); p.add("Level_Window", "violet", box(1.6, 1.85, .1, .2, ZF, ZF + .004))
    plants(p, np.linspace(-1.8, 1.8, 12), .36); clamps(p, (-1.7, 0, 1.7)); return p
def iter2():  # wall-rail-hung cassettes (4 x 1.0 m), latched to the rail, clear floor
    p = Pod("Rail_Cassettes")
    p.add("Wall_Rail", "alloy", blk(-W / 2, W / 2, .5, .54, ZB, ZB + .03, .006, 1))
    for x in (-1.5, -.5, .5, 1.5):
        p.add("Cassettes", "white", bev(.96, .34, .2, .44, .03, .01, 2, x, .0)); p.add("Cassette_Hooks", "gunmetal", box(x - .3, x + .3, .44, .54, ZB + .03, ZB + .05))
        p.add("Rail_Latches", "amber", box(x - .02, x + .02, .5, .53, ZB + .05, ZB + .055))
        lid(p, x - .46, x + .46, .44, ZB + .06, ZF - .06); plants(p, np.linspace(x - .36, x + .36, 3), .44, 0, .09)
    return p
def iter3():  # tiered steps: three stepped troughs rising toward the window
    p = Pod("Tiered_Steps")
    for i, (y, z) in enumerate(((.2, .12), (.36, 0), (.52, -.12))):
        p.add("Tiers", "white", bev(W, .16, 0, y, .03, .01, 2, 0, z)); lid(p, -W / 2 + .04, W / 2 - .04, y, z - .07, z + .07, "Tier_Lids")
        plants(p, np.linspace(-1.8, 1.8, 10 - i * 2), y, z, .07)
    clamps(p, (-1.7, 1.7)); return p
def iter4():  # NFT channels: three alloy channels on gunmetal frames + sealed pump box
    p = Pod("NFT_Channels")
    for x in (-1.9, -.65, .65, 1.9): p.add("Frames", "gunmetal", blk(x - .02, x + .02, 0, .58, ZB + .02, ZF - .02, .006, 1))
    for y, z in ((.18, .1), (.34, -.02), (.5, -.12)):
        p.add("Channels", "alloy", blk(-1.92, 1.92, y - .05, y, z - .045, z + .045, .015, 2)); plants(p, np.linspace(-1.75, 1.75, 9), y, z, .065)
    p.add("Pump_Box", "white", bev(.3, .3, 0, .14, .02, .006, 2, 0, 0)); p.add("Pump_Status", "green", box(-.04, .04, .1, .11, .15, .154))
    clamps(p, (-1.9, 1.9)); return p
def iter5():  # Sprocket service: trough + front reservoir drawer, dosing panel and Sprocket port at 0.45 at one end
    p = Pod("Sprocket_Service")
    p.add("Trough", "white", bev(3.4, D, .03, .38, .04, .012, 3, -.3, 0)); p.add("Plinth", "gunmetal", bev(3.3, D - .1, 0, .03, .02, .006, 1, -.3, 0))
    p.add("Reservoir_Drawer", "slate", box(-1.8, -.6, .06, .26, ZF, ZF + .01)); p.add("Drawer_Latch", "amber", box(-1.24, -1.16, .2, .23, ZF + .01, ZF + .014))
    p.add("Service_Tower", "gunmetal", bev(.56, D, 0, H, .03, .01, 3, W / 2 - .28, 0))
    p.add("Sprocket_Port", "alloy", bev(.14, .02, .38, .52, .01, .004, 1, W / 2 - .28, ZF + .01)); p.add("Port_Ring", "amber", box(W / 2 - .31, W / 2 - .25, .43, .47, ZF + .02, ZF + .024))
    p.add("Dosing_Status", "green", box(W / 2 - .4, W / 2 - .16, .54, .56, ZF, ZF + .004))
    lid(p, -1.96, 1.36, .38); plants(p, np.linspace(-1.85, 1.25, 10), .38); clamps(p, (-1.8, 0, 1.2)); return p

def main():
    os.makedirs(OUT, exist_ok=True); isos = []
    for i, fn in enumerate([iter1, iter2, iter3, iter4, iter5], 1):
        p = fn(); tris, iso, lo, hi, bad = wg.sheet(p, os.path.join(OUT, f"iter_0{i}_sheet.png"), f"iter_0{i}  {p.name}  (#33 hydro planter)")
        isos.append((p.name, iso)); print(i, p.name, tris, (hi - lo).round(3), "bad", bad)
    fig, axs = plt.subplots(3, 2, figsize=(16, 12), facecolor="#F4F2EC")
    for ax in axs.flat: ax.axis("off")
    for ax, (i, (n, im)) in zip(axs.flat, enumerate(isos, 1)): ax.imshow(im); ax.set_title(f"{i}. {n}", fontsize=11, color="#555")
    plt.tight_layout(rect=(0, 0, 1, .97)); fig.savefig(os.path.join(OUT, "overview.png"), dpi=90, facecolor="#F4F2EC"); plt.close(fig)
# ---------- final: polished iter_03 Tiered_Steps as an EXTERIOR asset (hydro co-op beds / sidewalk planters) ----------
# Interior #33 dropped from 103/202 (Jared, Oct 29). Levelling clamp feet: each foot is a threaded alloy jack in a
# gunmetal clamp shoe; jacks take up curved-floor sag (+/-25 mm) so the tiers stay level on the cylinder floor.
def lean_plants(p, xs, y, z, r):
    a = [bush(x, y, z, r * (0.85 + .3 * rng.random())) for i, x in enumerate(xs) if i % 2 == 0]
    b = [bush(x, y, z, r * (0.85 + .3 * rng.random()), "leaf2") for i, x in enumerate(xs) if i % 2 == 1]
    p.add("Foliage", "leaf", *a); p.add("Foliage_Light", "leaf2", *b)
    p.add("Net_Cup_Clips", "gunmetal", *[cyl(x, z, .035, y - .02, y + .012, 6) for x in xs])
def final_tiered():
    p = Pod("Tiered_Steps_Exterior"); FT = .06
    p.add("Base_Frame", "gunmetal", blk(-W / 2 + .05, W / 2 - .05, FT - .03, FT, -.19, .19, .006, 1))
    for i, (y, z) in enumerate(((.2, .12), (.36, 0), (.52, -.12))):
        p.add("Tiers", "white", bev(W, .16, FT, y + FT, .03, .01, 2, 0, z))
        x0, x1 = -W / 2 + .04, W / 2 - .04; yy = y + FT
        p.add("Tier_Lids", "slate", box(x0, x1, yy - .01, yy + .006, z - .07, z + .07))
        p.add("Tier_Latches", "amber", *[box(x - .02, x + .02, yy - .012, yy - .004, z + .07, z + .076) for x in (-1.5, 0, 1.5)])
        lean_plants(p, np.linspace(-1.75, 1.75, (7, 5, 4)[i]), yy, z, .075)
    p.add("Reservoir", "slate", box(-1.9, 1.9, FT + .02, FT + .14, .2, .206))
    p.add("Reservoir_Seal", "alloy", box(-1.9, 1.9, FT + .14, FT + .15, .2, .206))
    feet = [(x, z) for x in (-1.75, 0, 1.75) for z in (-.14, .14)]
    p.add("Levelling_Jacks", "alloy", *[cyl(x, z, .018, .02, FT - .03, 8) for x, z in feet])
    p.add("Clamp_Shoes", "gunmetal", *[box(x - .06, x + .06, 0, .02, z - .045, z + .045) for x, z in feet])
    p.add("Shoe_Bolts", "alloy", *[cyl(x + dx, z, .008, .02, .03, 6) for x, z in feet for dx in (-.04, .04)])
    return p
def final_main():
    from dining_chair_generator import export_final
    p = final_tiered(); gp = os.path.join(dc.ROOT, "godot/assets/models/hydro_planter_tiered_exterior.glb"); tris, geo = export_final(p.P, [gp])
    V = np.vstack([g[1] for g in geo.values()]); bad = [n for n, (mk, m) in p.P.items() if not all(c.is_watertight for c in m.split(only_watertight=False))]
    print("tris", tris, "lo", V.min(0).round(3), "hi", V.max(0).round(3), "bad", bad)
    sp = os.path.join(OUT, "final_tiered_exterior_sheet.png"); wg.sheet(p, sp, "Final  hydro planter, Tiered Steps (EXTERIOR: hydro co-op / sidewalk)"); os.remove(sp.replace("_sheet.png", ".glb"))
if __name__ == "__main__":
    final_main() if len(sys.argv) > 1 and sys.argv[1] == "final" else main()
