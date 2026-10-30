"""Rev C #35 toy bin + scattered toys (room 103; 1 set; bin 1.2 x 0.6 x 0.5). Five iterations, family language.
Bottom-centre pivot, front +Z. Toys ship as a loose kit beside the bin; how they are scattered is left to the room layout.
Spin-down: bin lids latch, and every toy has a magnetic gunmetal foot pad that snaps into the bin's clamp rack or onto the floor plates."""
import os, sys, numpy as np, trimesh
sys.path.insert(0, os.path.dirname(__file__))
from hydro_planter_generator import cyl, box, bev, blk, Pod, dc, wg, plt
OUT = os.path.join(dc.ROOT, "design/assets/toy_bin")
W, D, H = 1.2, .6, .5

def toys(p, x0, z0):
    """Small kit: 3 stacking blocks, a ball, a toy rocket and a mini Sprocket figure, each on a magnetic foot pad."""
    for i, (dx, c) in enumerate(((0, "violet"), (.09, "amber"), (.045, "green"))):
        y = 0 if i < 2 else .08
        p.add("Toy_Blocks", c, box(x0 + dx - .04, x0 + dx + .04, y, y + .08, z0 - .04, z0 + .04))
    ball = trimesh.creation.icosphere(1, .07); ball.apply_translation((x0 + .26, .07, z0)); ball.metadata["uv"] = ball.vertices[:, [0, 2]]
    p.add("Toy_Ball", "amber", ball)
    p.add("Toy_Rocket", "white", cyl(x0 + .42, z0, .035, .03, .22, 8)); p.add("Toy_Rocket_Fins", "violet", box(x0 + .37, x0 + .47, .02, .07, z0 - .008, z0 + .008))
    p.add("Toy_Sprocket", "gunmetal", bev(.08, .08, .02, .12, .015, .005, 1, x0 + .58, z0)); p.add("Toy_Sprocket_Eye", "green", box(x0 + .56, x0 + .60, .09, .1, z0 + .04, z0 + .044))
    p.add("Mag_Pads", "gunmetal", *[box(x0 + x - .045, x0 + x + .045, 0, .006, z0 - .045, z0 + .045) for x in (.42, .58)])
def clamps(p, xs, zs=(-D / 2 + .06, D / 2 - .06)):
    p.add("Floor_Clamps", "gunmetal", *[box(x - .05, x + .05, 0, .02, z - .04, z + .04) for x in xs for z in zs])

TZ = D / 2 + .22  # loose toy kit sits in front of the bin on the sheet
def iter1():  # moulded chest: white chest, slate lid with two amber latches, floor-clamped
    p = Pod("Moulded_Chest")
    p.add("Bin_Body", "white", bev(W, D, 0, H - .03, .04, .012, 3, 0, 0)); p.add("Bin_Lid", "slate", bev(W + .02, D + .02, H - .03, H, .04, .008, 2, 0, 0))
    p.add("Lid_Latches", "amber", *[box(x - .03, x + .03, H - .07, H - .035, D / 2, D / 2 + .008) for x in (-.35, .35)])
    p.add("Grip_Slot", "gunmetal", box(-.15, .15, H - .12, H - .09, D / 2, D / 2 + .004)); clamps(p, (-.5, .5)); toys(p, -.35, TZ); return p
def iter2():  # cubby bench: three cubbies with latched slate doors and a padded seat top a child can sit on
    p = Pod("Cubby_Bench")
    p.add("Bench_Body", "white", bev(W, D, 0, H - .05, .03, .01, 3, 0, 0)); p.add("Seat_Pad", "slate", bev(W - .04, D - .04, H - .05, H, .04, .015, 3, 0, 0))
    for x in (-.4, 0, .4):
        p.add("Cubby_Doors", "slate", box(x - .17, x + .17, .06, .38, D / 2, D / 2 + .012)); p.add("Door_Latches", "amber", box(x - .025, x + .025, .3, .34, D / 2 + .012, D / 2 + .02))
    p.add("Plinth", "gunmetal", bev(W - .06, D - .06, 0, .03, .02, .006, 1, 0, 0)); clamps(p, (-.5, .5)); toys(p, -.35, TZ); return p
def iter3():  # rail bins: three gunmetal-hooked bins on the 0.30 m wall rail, floor clear underneath
    p = Pod("Rail_Bins")
    p.add("Wall_Rail", "alloy", blk(-W / 2, W / 2, .28, .32, -D / 2, -D / 2 + .03, .006, 1))
    p.add("Wall_Plates", "gunmetal", *[box(x - .05, x + .05, .22, .38, -D / 2 - .005, -D / 2) for x in (-.55, .55)])
    for x in (-.4, 0, .4):
        p.add("Bins", "white", bev(.38, D - .08, .12, H, .03, .01, 2, x, .04)); p.add("Bin_Hooks", "gunmetal", box(x - .1, x + .1, .3, .36, -D / 2 + .03, -D / 2 + .05))
        p.add("Bin_Lids", "slate", bev(.38, D - .08, H, H + .012, .03, .004, 1, x, .04)); p.add("Lid_Latches", "amber", box(x - .025, x + .025, H - .04, H - .01, D / 2, D / 2 + .008))
    toys(p, -.35, TZ); return p
def iter4():  # rolling tub: open tub on four caster pods; amber brake clamps lock the casters to floor plates
    p = Pod("Rolling_Tub")
    p.add("Tub", "white", bev(W, D, .08, H, .1, .015, 3, 0, 0)); p.add("Tub_Rim", "alloy", bev(W + .02, D + .02, H - .02, H, .1, .006, 1, 0, 0))
    p.add("Soft_Net_Lid", "slate", bev(W - .06, D - .06, H - .015, H - .005, .08, .003, 1, 0, 0))
    pods = [(x, z) for x in (-.48, .48) for z in (-.22, .22)]
    p.add("Casters", "gunmetal", *[cyl(x, z, .04, .0, .08, 10) for x, z in pods])
    p.add("Brake_Clamps", "amber", *[box(x - .015, x + .015, .03, .07, z + (.04 if z > 0 else -.046), z + (.046 if z > 0 else -.04)) for x, z in pods])
    p.add("Floor_Plates", "gunmetal", *[box(x - .06, x + .06, 0, .006, z - .06, z + .06) for x, z in pods]); toys(p, -.35, TZ); return p
def iter5():  # Sprocket tidy: chest with a front intake flap at 0.45 m; Sprocket drops toys in, green status shows it is tidy
    p = Pod("Sprocket_Tidy")
    p.add("Bin_Body", "white", bev(W, D, 0, H - .03, .04, .012, 3, 0, 0)); p.add("Bin_Lid", "slate", bev(W + .02, D + .02, H - .03, H, .04, .008, 2, 0, 0))
    p.add("Lid_Latches", "amber", *[box(x - .03, x + .03, H - .07, H - .035, D / 2, D / 2 + .008) for x in (-.45, -.05)])
    p.add("Intake_Flap", "gunmetal", box(.2, .5, .38, .46, D / 2, D / 2 + .012)); p.add("Sprocket_Port", "alloy", box(.3, .4, .42, .45, D / 2 + .012, D / 2 + .02))
    p.add("Tidy_Status", "green", box(.22, .48, .35, .36, D / 2, D / 2 + .006)); clamps(p, (-.5, .5)); toys(p, -.35, TZ); return p

def main():
    os.makedirs(OUT, exist_ok=True); isos = []
    for i, fn in enumerate([iter1, iter2, iter3, iter4, iter5], 1):
        p = fn(); tris, iso, lo, hi, bad = wg.sheet(p, os.path.join(OUT, f"iter_0{i}_sheet.png"), f"iter_0{i}  {p.name}  (#35 toy bin + toys)")
        isos.append((p.name, iso)); print(i, p.name, tris, (hi - lo).round(3), "bad", bad)
    fig, axs = plt.subplots(3, 2, figsize=(16, 12), facecolor="#F4F2EC")
    for ax in axs.flat: ax.axis("off")
    for ax, (i, (n, im)) in zip(axs.flat, enumerate(isos, 1)): ax.imshow(im); ax.set_title(f"{i}. {n}", fontsize=11, color="#555")
    plt.tight_layout(rect=(0, 0, 1, .97)); fig.savefig(os.path.join(OUT, "overview.png"), dpi=90, facecolor="#F4F2EC"); plt.close(fig)

# ---------- final (Jared, Oct 29): combine #1 Moulded_Chest (floor) + #3 Rail_Bins (wall, above), same toy kit ----------
# The bins hang on a local bolted alloy rail at 0.90 m (top of bins 1.20 m, within a child's reach) and are only 0.30 m deep,
# so the chest lid can still swing up to about 75 degrees under them.
def final_combo():
    p = iter1(); p.name = "Toy_Chest_Rail_Bins"; RY = .9; BD = .3; zb0 = -D / 2; zb1 = zb0 + BD
    p.add("Wall_Rail", "alloy", blk(-W / 2, W / 2, RY - .02, RY + .02, zb0 - .03, zb0, .006, 1))
    p.add("Wall_Plates", "gunmetal", *[box(x - .05, x + .05, RY - .08, RY + .08, zb0 - .035, zb0 - .03) for x in (-.55, .55)])
    p.add("Rail_Bolts", "alloy", *[cyl(x, zb0 - .03, .008, RY + dy - .005, RY + dy + .005, 6) for x in (-.55, .55) for dy in (-.06, .06)])
    for x in (-.4, 0, .4):
        p.add("Bins", "white", bev(.38, BD - .02, RY - .16, RY + .3, .03, .01, 2, x, zb0 + BD / 2 + .01))
        p.add("Bin_Hooks", "gunmetal", box(x - .1, x + .1, RY - .02, RY + .05, zb0, zb0 + .02))
        p.add("Bin_Lids", "slate", bev(.38, BD - .02, RY + .3, RY + .312, .03, .004, 1, x, zb0 + BD / 2 + .01))
        p.add("Bin_Latches", "amber", box(x - .025, x + .025, RY + .26, RY + .29, zb1, zb1 + .008))
    p.add("Chest_Bolts", "alloy", *[cyl(x, z, .008, .02, .03, 6) for x in (-.5, .5) for z in (-D / 2 + .06, D / 2 - .06)])
    return p
def final_main():
    from dining_chair_generator import export_final
    p = final_combo(); gp = os.path.join(dc.ROOT, "godot/assets/models/toy_chest_rail_bins.glb"); tris, geo = export_final(p.P, [gp])
    V = np.vstack([g[1] for g in geo.values()]); bad = [n for n, (mk, m) in p.P.items() if not all(c.is_watertight for c in m.split(only_watertight=False))]
    print("tris", tris, "lo", V.min(0).round(3), "hi", V.max(0).round(3), "bad", bad)
    sp = os.path.join(OUT, "final_chest_rail_bins_sheet.png"); wg.sheet(p, sp, "Final  #35 toy chest + rail bins + toy kit (103)"); os.remove(sp.replace("_sheet.png", ".glb"))
if __name__ == "__main__":
    final_main() if len(sys.argv) > 1 and sys.argv[1] == "final" else main()
