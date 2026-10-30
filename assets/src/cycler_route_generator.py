"""Rev C #32 cycler route model (room 203, wall; qty 1; 0.9 W x 0.2 D x 1.0 H). Five iterations, family language.
A wall display of the Earth-Mars cycler's looping route. Pivot at the bottom-centre of the back plate, +Z out from the wall (wall at -Z).
Spin-down: every part is bolted to a gunmetal back plate that hooks and latches onto the wall rail; no loose parts."""
import os, sys, numpy as np, trimesh
sys.path.insert(0, os.path.dirname(__file__))
from hydro_planter_generator import cyl, box, bev, blk, Pod, dc, wg, plt
from dining_chair_generator import export_final
from bath_pod_generator import set_glass_blend
OUT = os.path.join(dc.ROOT, "design/assets/cycler_route")
W, D, H = .9, .2, 1.0; ZB = -D / 2

def seg(a, b, t=.008, d=.008):
    a, b = np.asarray(a, float), np.asarray(b, float); v = b - a; L = np.linalg.norm(v)
    m = trimesh.creation.box((L, t, d)); ang = np.arctan2(v[1], v[0])
    m.apply_transform(trimesh.transformations.rotation_matrix(ang, (0, 0, 1))); m.apply_translation((a + b) / 2)
    m.metadata["uv"] = m.vertices[:, [0, 1]]; return m
def ellipse(cx, cy, rx, ry, z, rot=0.0, n=24, t=.008):
    a = np.linspace(0, 2 * np.pi, n + 1); c, s = np.cos(rot), np.sin(rot)
    P = [(cx + rx * np.cos(u) * c - ry * np.sin(u) * s, cy + rx * np.cos(u) * s + ry * np.sin(u) * c, z) for u in a]
    return [seg(P[i], P[i + 1], t, t) for i in range(n)]
def bead(x, y, z, r):
    m = trimesh.creation.icosphere(1, r); m.apply_translation((x, y, z)); m.metadata["uv"] = m.vertices[:, [0, 1]]; return m
def back_plate(p, z0=ZB, depth=.02):
    p.add("Back_Plate", "gunmetal", bev(W, depth, 0, H, .03, .006, 2, 0, z0 + depth / 2))
    p.add("Rail_Hooks", "gunmetal", *[box(x - .05, x + .05, H - .1, H, z0 - .02, z0) for x in (-.3, .3)])
    p.add("Hook_Latches", "amber", *[box(x - .015, x + .015, H - .05, H - .02, z0 + depth, z0 + depth + .006) for x in (-.3, .3)])
    p.add("Plate_Bolts", "alloy", *[cyl(x, z0, .01, y, y + .01, 6) for x in (-.4, .4) for y in (.05, H - .1)])
def bodies(p, z, cx=0.0, cy=.5):
    p.add("Sun", "amber", bead(cx, cy, z, .05)); p.add("Earth", "green", bead(cx + .17, cy + .05, z, .025)); p.add("Mars", "violet", bead(cx - .26, cy - .12, z, .022))
    p.add("Earth_Orbit", "alloy", *ellipse(cx, cy, .18, .18, z, n=20, t=.005)); p.add("Mars_Orbit", "alloy", *ellipse(cx, cy, .3, .29, z, n=24, t=.005))

def route(p, z, t=.009, mat="violet"):
    p.add("Cycler_Route", mat, *ellipse(-.04, .48, .25, .2, z, rot=.5, n=28, t=t))
    p.add("Cycler_Marker", "white", box(.16, .2, .58, .6, z - .01, z + .01))
def iter1():  # etched panel: white composite face on the back plate, violet route inlaid, alloy orbits, small planet beads
    p = Pod("Etched_Panel"); back_plate(p)
    p.add("Face_Panel", "white", bev(W - .06, .015, .03, H - .03, .02, .004, 1, 0, ZB + .0275)); bodies(p, ZB + .04); route(p, ZB + .042); return p
def iter2():  # wire orrery: open gunmetal frame, orbits and route in alloy and violet wire stood off the plate on pins
    p = Pod("Wire_Orrery"); back_plate(p, depth=.015)
    p.add("Standoff_Pins", "alloy", *[box(x - .006, x + .006, y - .006, y + .006, ZB + .015, ZB + .1) for x, y in ((-.3, .2), (.3, .2), (-.3, .8), (.3, .8))])
    bodies(p, ZB + .1); route(p, ZB + .1, .007); return p
def iter3():  # lightbox: slate box with a glass front; the route glows violet, Sun amber, Earth green
    p = Pod("Lightbox"); back_plate(p)
    p.add("Box_Frame", "slate", *[box(x0, x1, y0, y1, ZB + .02, ZB + .09) for x0, x1, y0, y1 in ((-W / 2, W / 2, 0, .03), (-W / 2, W / 2, H - .03, H), (-W / 2, -W / 2 + .03, 0, H), (W / 2 - .03, W / 2, 0, H))])
    p.add("Box_Back", "slate", box(-W / 2 + .03, W / 2 - .03, .03, H - .03, ZB + .02, ZB + .03)); bodies(p, ZB + .05); route(p, ZB + .05, .012)
    p.add("Front_Glass", "glass", box(-W / 2 + .03, W / 2 - .03, .03, H - .03, ZB + .085, ZB + .09)); return p
def iter4():  # shadow box: three stepped layers (orbits at the back, route in the middle, labels and marker in front)
    p = Pod("Shadow_Box"); back_plate(p)
    p.add("Layer_Back", "white", box(-W / 2 + .05, W / 2 - .05, .05, H - .05, ZB + .02, ZB + .03)); bodies(p, ZB + .035)
    p.add("Layer_Mid", "slate", *[box(x0, x1, .05, H - .05, ZB + .07, ZB + .08) for x0, x1 in ((-W / 2 + .05, -W / 2 + .1), (W / 2 - .1, W / 2 - .05))]); route(p, ZB + .085)
    p.add("Label_Strips", "alloy", *[box(-.35 + i * .25, -.17 + i * .25, .1, .13, ZB + .12, ZB + .125) for i in range(3)]); p.add("Label_Glyphs", "amber", *[box(-.3 + i * .25, -.22 + i * .25, .11, .12, ZB + .125, ZB + .128) for i in range(3)]); return p
def iter5():  # tracker slider: etched panel plus a gunmetal slider track below where the family moves a marker to show today's leg
    p = Pod("Tracker_Slider"); back_plate(p)
    p.add("Face_Panel", "white", bev(W - .06, .015, .2, H - .03, .02, .004, 1, 0, ZB + .0275)); bodies(p, ZB + .04, cy=.58); p.add("Cycler_Route", "violet", *ellipse(-.04, .56, .25, .2, ZB + .042, rot=.5, n=28, t=.009))
    p.add("Slider_Track", "alloy", blk(-.38, .38, .08, .12, ZB + .02, ZB + .05, .004, 1)); p.add("Slider_Marker", "amber", box(.05, .11, .06, .14, ZB + .05, ZB + .07))
    p.add("Leg_Ticks", "gunmetal", *[box(x - .004, x + .004, .13, .17, ZB + .02, ZB + .03) for x in np.linspace(-.36, .36, 7)]); return p

def main():
    os.makedirs(OUT, exist_ok=True); isos = []
    for i, fn in enumerate([iter1, iter2, iter3, iter4, iter5], 1):
        p = fn(); full = dict(p.P); p.P = {k: v for k, v in full.items() if v[0] != "glass"}  # glass hidden in sheet renders (BLEND in glb)
        tris, iso, lo, hi, bad = wg.sheet(p, os.path.join(OUT, f"iter_0{i}_sheet.png"), f"iter_0{i}  {p.name}  (#32 cycler route model)")
        p.P = full; gp = os.path.join(OUT, f"iter_0{i}.glb"); tris, _ = export_final(p.P, [gp]); set_glass_blend(gp)
        isos.append((p.name, iso)); print(i, p.name, tris, (hi - lo).round(3), "bad", bad)
    fig, axs = plt.subplots(3, 2, figsize=(16, 12), facecolor="#F4F2EC")
    for ax in axs.flat: ax.axis("off")
    for ax, (i, (n, im)) in zip(axs.flat, enumerate(isos, 1)): ax.imshow(im); ax.set_title(f"{i}. {n}", fontsize=11, color="#555")
    plt.tight_layout(rect=(0, 0, 1, .97)); fig.savefig(os.path.join(OUT, "overview.png"), dpi=90, facecolor="#F4F2EC"); plt.close(fig)
def final_lightbox():
    p = iter3(); p.name = "Cycler_Route_Lightbox"; z1 = ZB + .09
    p.add("Bezel_Trim", "alloy", *[box(x0, x1, y0, y1, z1, z1 + .006) for x0, x1, y0, y1 in ((-W / 2, W / 2, 0, .02), (-W / 2, W / 2, H - .02, H), (-W / 2, -W / 2 + .02, 0, H), (W / 2 - .02, W / 2, 0, H))])
    p.add("Glass_Retainer_Clips", "amber", *[box(x - .02, x + .02, y - .006, y + .006, z1, z1 + .01) for x in (-.25, .25) for y in (.025, H - .025)])
    p.add("Corner_Bolts", "gunmetal", *[box(x - .007, x + .007, y - .007, y + .007, z1 + .006, z1 + .01) for x in (-W / 2 + .01, W / 2 - .01) for y in (.01, H - .01)])
    p.add("Backlight_Diffuser", "white", box(-W / 2 + .05, W / 2 - .05, .08, H - .05, ZB + .03, ZB + .034))
    p.add("Star_Field", "white", *[box(x - .004, x + .004, y - .004, y + .004, ZB + .034, ZB + .037) for x, y in ((-.33, .85), (-.2, .9), (.28, .88), (.34, .72), (-.36, .3), (.32, .2), (-.1, .14), (.15, .86))])
    p.add("Route_Label", "slate", box(-.2, .2, .035, .065, ZB + .03, ZB + .04)); p.add("Label_Glyphs", "violet", *[box(-.17 + i * .07, -.13 + i * .07, .043, .057, ZB + .04, ZB + .043) for i in range(5)])
    p.add("Power_Conduit", "gunmetal", box(W / 2 - .07, W / 2 - .04, -.0, .03, ZB - .0, ZB + .02))
    return p
def final_main():
    p = final_lightbox(); gp = os.path.join(dc.ROOT, "godot/assets/models/cycler_route_lightbox.glb"); tris, geo = export_final(p.P, [gp]); set_glass_blend(gp)
    V = np.vstack([g[1] for g in geo.values()]); bad = [n for n, (mk, m) in p.P.items() if not all(c.is_watertight for c in m.split(only_watertight=False))]
    print("tris", tris, "lo", V.min(0).round(3), "hi", V.max(0).round(3), "bad", bad)
    p.P.pop("Front_Glass", None); sp = os.path.join(OUT, "final_lightbox_sheet.png"); wg.sheet(p, sp, "Final  #32 cycler route model, Lightbox (glass hidden)"); os.remove(sp.replace("_sheet.png", ".glb"))
if __name__ == "__main__":
    final_main() if len(sys.argv) > 1 and sys.argv[1] == "final" else main()
