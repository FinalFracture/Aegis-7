"""Rev C #43 Spares shelf (Maintenance, RM 1B Bot Substation; qty 1; 1.9 W x 0.5 D x 1.8 H). Five iterations.
Jared (Oct 29): not a plain closet. Sprocket-first: each option delivers parts to a Sprocket pick point at 0.45 m with amber floor guide rails;
humans get only a small request panel and an amber release lever. Open frames, no full-height doors. Pivot at the bottom-centre, +Z front, wall at -Z.
Spin-down: every bin, spool and cartridge latches or clamps (amber)."""
import os, sys, numpy as np, trimesh
sys.path.insert(0, os.path.dirname(__file__))
from hydro_planter_generator import cyl, box, bev, blk, Pod, dc, wg, plt
from dining_chair_generator import export_final
from bath_pod_generator import set_glass_blend
from cycler_route_generator import cyl_z
from folding_counter_generator import xcyl
OUT = os.path.join(dc.ROOT, "design/assets/spares_shelf")
W, D, H = 1.9, .5, 1.8; X0, X1, ZB, ZF = -W / 2, W / 2, -D / 2, D / 2; PY = .45
def bin_(x, y, z0, w=.16, h=.1, d=.2): return blk(x - w / 2, x + w / 2, y, y + h, z0, z0 + d, .008, 1)
def bins(p, xs, ys, z0, tag="", mats=("slate", "green", "violet"), w=.16, h=.1, d=.2):
    B = {m: [] for m in mats}; T = []
    for i, x in enumerate(xs):
        for j, y in enumerate(ys): B[mats[(i + j) % len(mats)]].append(bin_(x, y, z0, w, h, d)); T.append(box(x - .03, x + .03, y + h - .03, y + h - .015, z0 + d, z0 + d + .006))
    for m, L in B.items():
        if L: p.add(f"Bins_{m}{tag}", m, *L)
    p.add("Bin_Latches" + tag, "amber", *T)
def pick(p, x, z, tag=""):  # Sprocket pick tray at 0.45 m with lipped alloy tray, green ready lamp and floor guide rails
    p.add("Pick_Tray" + tag, "alloy", box(x - .2, x + .2, PY - .02, PY, z - .2, z), box(x - .2, x + .2, PY, PY + .05, z - .015, z), box(x - .2, x - .185, PY, PY + .05, z - .2, z), box(x + .185, x + .2, PY, PY + .05, z - .2, z))
    p.add("Pick_Lamp" + tag, "green", box(x - .05, x + .05, PY + .1, PY + .12, z - .21, z - .2)); p.add("Guide_Rails" + tag, "amber", *[box(x + s * .3 - .02, x + s * .3 + .02, 0, .03, z - .1, ZF) for s in (-1, 1)])
def human(p, x, z, tag=""):  # request panel + amber release lever
    p.add("Request_Panel" + tag, "slate", box(x - .1, x + .1, 1.3, 1.48, z - .03, z)); p.add("Request_Keys" + tag, "green", *[box(x - .07 + k * .05, x - .04 + k * .05, 1.4, 1.43, z, z + .005) for k in range(3)])
    p.add("Release_Lever" + tag, "amber", box(x - .012, x + .012, 1.12, 1.27, z - .02, z + .02), box(x - .04, x + .04, 1.12, 1.15, z + .02, z + .05))
def frame(p, x0, x1, z0, z1, h=H, tag=""):
    p.add("Posts" + tag, "gunmetal", *[box(x - .02, x + .02, 0, h, z - .02, z + .02) for x in (x0 + .02, x1 - .02) for z in (z0 + .02, z1 - .02)])
    p.add("Floor_Clamps" + tag, "amber", *[box(x - .04, x + .04, 0, .02, z - .04, z + .04) for x in (x0 + .04, x1 - .04) for z in (z0 + .04, z1 - .04)])
def iter1():  # paternoster carousel: a vertical loop of bins on a chain inside an open frame; the bottom bin passes the 0.45 m pick window
    p = Pod("Bin_Paternoster"); frame(p, -.55, .55, ZB, ZF - .05); p.add("Sprockets", "alloy", xcyl(-.5, .5, .55, -.02, .2, 12), xcyl(-.5, .5, 1.6, -.02, .2, 12))
    p.add("Chain_Guides", "gunmetal", *[box(x - .015, x + .015, .55, 1.6, z - .015, z + .015) for x in (-.5, .5) for z in (-.22, .18)])
    ys = np.linspace(.62, 1.5, 5); B = []
    for y in ys:
        for z0 in (ZB + .04, .1):
            B.append((y, z0))
    for k, (y, z0) in enumerate(B): p.add("Carrier_Bins" + ("A" if k % 2 else "B"), "slate" if k % 2 else "violet", blk(-.45, .45, y - .06, y + .06, z0, z0 + .1, .01, 1))
    p.add("Carrier_Latches", "amber", *[box(-.05, .05, y + .03, y + .05, .2, .206) for y in ys]); p.add("Header_Motor", "slate", box(-.55, .55, 1.65, 1.8, ZB, ZF - .05))
    p.add("Side_Bins_Rails", "alloy", *[box(x0, x1, y - .02, y, ZB, ZB + .25) for x0, x1 in ((X0, -.57), (.57, X1)) for y in (.3, .8, 1.3)])
    bins(p, (-.85, -.67), (.3, .8, 1.3), ZB + .02, "_L", w=.15); bins(p, (.67, .85), (.3, .8, 1.3), ZB + .02, "_R", w=.15)
    p.add("Side_Posts", "gunmetal", *[box(x - .015, x + .015, 0, 1.45, ZB, ZB + .03) for x in (X0 + .015, X1 - .015)]); pick(p, 0, ZF - .05); human(p, .7, ZB + .3); return p
def iter2():  # magnetic bin rail wall: open perforated back plate, bins hang on four magnetic rails, a low Sprocket pick tray and a sliding step-bin shuttle
    p = Pod("Magnet_Bin_Rails"); p.add("Back_Plate", "slate", box(X0, X1, .2, H, ZB, ZB + .02)); p.add("Perforation_Dots", "gunmetal", *[box(x - .01, x + .01, y - .01, y + .01, ZB + .02, ZB + .024) for x in np.linspace(X0 + .1, X1 - .1, 10) for y in np.linspace(1.68, 1.68, 1)])
    ys = [.7, 1.0, 1.3, 1.6]; p.add("Magnet_Rails", "alloy", *[box(X0 + .05, X1 - .05, y - .03, y, ZB + .02, ZB + .05) for y in ys])
    bins(p, np.linspace(X0 + .15, X1 - .15, 9), [y - .12 for y in ys], ZB + .05, w=.15, h=.11, d=.18)
    p.add("Feet", "gunmetal", *[box(x - .03, x + .03, 0, .2, ZB, ZB + .3) for x in (X0 + .05, X1 - .05)]); p.add("Floor_Clamps", "amber", *[box(x - .05, x + .05, 0, .02, ZB + .2, ZB + .3) for x in (X0 + .05, X1 - .05)])
    p.add("Shuttle_Rail", "gunmetal", box(X0 + .05, X1 - .05, .52, .56, ZB + .02, ZB + .08)); p.add("Bin_Shuttle", "alloy", box(-.25, .25, .4, .52, ZB + .03, ZB + .2)); pick(p, 0, ZB + .4); human(p, X1 - .2, ZB + .05); return p
def iter3():  # gravity dispenser tubes: glass (BLEND) tubes feed parts capsules down to a 0.45 m pick tray; open gunmetal ladder frame
    p = Pod("Gravity_Dispenser_Tubes"); frame(p, X0, X1, ZB, ZB + .3); xs = np.linspace(X0 + .2, X1 - .2, 7)
    p.add("Tubes", "glass", *[cyl(x, ZB + .15, .07, .6, 1.7, 12) for x in xs]); p.add("Tube_Collars", "alloy", *[cyl(x, ZB + .15, .08, y, y + .03, 12) for x in xs for y in (.58, 1.1, 1.68)])
    p.add("Capsules", "white", *[cyl(x, ZB + .15, .055, y, y + .09, 10) for i, x in enumerate(xs) for y in np.arange(.62, 1.62 - .12 * (i % 3), .1)])
    p.add("Capsule_Bands", "green", *[cyl(x, ZB + .15, .057, .66, .67, 10) for x in xs]); p.add("Gate_Valves", "amber", *[box(x - .05, x + .05, .58, .6, ZB + .15, ZB + .26) for x in xs])
    p.add("Feed_Chute", "gunmetal", box(X0 + .1, X1 - .1, .5, .56, ZB + .02, ZB + .32)); p.add("Top_Cap", "slate", box(X0, X1, 1.72, 1.8, ZB, ZB + .3)); pick(p, 0, ZB + .5); human(p, X1 - .15, ZB + .32); return p
def iter4():  # gantry picker rack: open bin racks, an overhead gantry with a hoisting pick head that drops a bin into the 0.45 m tray
    p = Pod("Gantry_Picker_Rack"); frame(p, X0, X1, ZB, ZB + .3, h=1.55)
    p.add("Rack_Shelves", "alloy", *[box(X0 + .02, X1 - .02, y - .02, y, ZB, ZB + .3) for y in (.9, 1.2, 1.5)]); bins(p, np.linspace(X0 + .15, X1 - .15, 10), (.9, 1.2), ZB + .05, w=.15, h=.11, d=.22)
    p.add("Gantry_Uprights", "gunmetal", *[box(x - .025, x + .025, 0, H, ZF - .07, ZF - .02) for x in (X0 + .025, X1 - .025)]); p.add("Gantry_Beam", "gunmetal", box(X0, X1, 1.72, 1.8, ZB, ZF - .02))
    p.add("Trolley", "slate", box(-.55, -.35, 1.62, 1.72, ZB + .1, ZF - .05)); p.add("Hoist_Cable", "alloy", box(-.455, -.445, 1.3, 1.62, .08, .09)); p.add("Pick_Head", "amber", box(-.52, -.38, 1.24, 1.3, .0, .17))
    p.add("Gripped_Bin", "violet", bin_(-.45, 1.1, .0, .15, .12, .17)); p.add("Drop_Funnel", "gunmetal", box(-.25, .25, .6, .64, ZB + .3, ZF - .08)); pick(p, 0, ZF - .08)
    p.add("Funnel_Beam", "gunmetal", box(X0 + .04, X1 - .04, .58, .64, ZB + .28, ZB + .32)); p.add("Tray_Hangers", "alloy", *[box(x - .01, x + .01, PY, .6, ZF - .2, ZF - .18) for x in (-.21, .21)])
    human(p, X1 - .15, ZF - .05); return p
def iter5():  # spool + cartridge rack: cable and sealant spools on clamped axles, slide-in cartridges in clip rails, a Sprocket refill port at 0.45 m
    p = Pod("Spool_Cartridge_Rack"); frame(p, X0, X1, ZB, ZB + .45, h=1.7)
    p.add("Axles", "alloy", *[xcyl(X0 + .04, X1 - .04, y, ZB + .22, .02, 8) for y in (1.0, 1.42)])
    p.add("Spools", "slate", *[xcyl(x - .1, x + .1, y, ZB + .22, .17, 14) for x in np.linspace(X0 + .25, X1 - .25, 4) for y in (1.0, 1.42)])
    p.add("Spool_Wraps", "violet", *[xcyl(x - .085, x + .085, y, ZB + .22, .18, 14) for x in np.linspace(X0 + .25, X1 - .25, 4)[::2] for y in (1.0,)], *[xcyl(x - .085, x + .085, 1.42, ZB + .22, .18, 14) for x in np.linspace(X0 + .25, X1 - .25, 4)[1::2]])
    p.add("Axle_Clamps", "amber", *[box(x - .02, x + .02, y - .05, y + .05, ZB + .17, ZB + .27) for x in (X0 + .05, X1 - .05) for y in (1.0, 1.42)])
    p.add("Cartridge_Rails", "gunmetal", box(X0 + .04, X1 - .04, .66, .7, ZB, ZB + .45)); p.add("Cartridges", "white", *[cyl(x, z, .035, .7, .8, 10) for x in np.linspace(X0 + .12, X1 - .12, 10) for z in (ZB + .12, ZB + .3) if abs(x) > .3])
    p.add("Cartridge_Clips", "amber", *[box(x - .04, x + .04, .74, .755, z - .04, z + .04) for x in np.linspace(X0 + .12, X1 - .12, 10) for z in (ZB + .12, ZB + .3) if abs(x) > .3])
    p.add("Top_Shelf", "alloy", box(X0 + .02, X1 - .02, 1.68, 1.7, ZB, ZB + .45)); p.add("Refill_Port", "slate", box(-.16, .16, PY - .12, PY + .12, ZB + .3, ZB + .33)); p.add("Port_Nozzles", "alloy", *[cyl_z(x, PY, .015, ZB + .33, ZB + .36, 8) for x in (-.06, .06)])
    p.add("Port_Stand", "gunmetal", box(-.2, .2, 0, PY + .2, ZB, ZB + .3)); p.add("Port_Lamp", "green", box(-.05, .05, PY + .15, PY + .17, ZB + .3, ZB + .31)); p.add("Guide_Rails", "amber", *[box(s * .3 - .02, s * .3 + .02, 0, .03, ZB + .3, ZF) for s in (-1, 1)])
    human(p, X1 - .15, ZB + .45); return p
def main():
    os.makedirs(OUT, exist_ok=True); isos = []
    for i, fn in enumerate([iter1, iter2, iter3, iter4, iter5], 1):
        p = fn(); full = dict(p.P); p.P = {k: v for k, v in full.items() if v[0] != "glass"}  # glass hidden in sheet renders (BLEND in glb)
        tris, iso, lo, hi, bad = wg.sheet(p, os.path.join(OUT, f"iter_0{i}_sheet.png"), f"iter_0{i}  {p.name}  (#43 spares shelf)")
        p.P = full; gp = os.path.join(OUT, f"iter_0{i}.glb"); tris, _ = export_final(p.P, [gp]); set_glass_blend(gp)
        isos.append((p.name, iso)); print(i, p.name, tris, (hi - lo).round(3), "bad", bad)
    fig, axs = plt.subplots(3, 2, figsize=(16, 12), facecolor="#F4F2EC")
    for ax in axs.flat: ax.axis("off")
    for ax, (i, (n, im)) in zip(axs.flat, enumerate(isos, 1)): ax.imshow(im); ax.set_title(f"{i}. {n}", fontsize=11, color="#555")
    plt.tight_layout(rect=(0, 0, 1, .97)); fig.savefig(os.path.join(OUT, "overview.png"), dpi=90, facecolor="#F4F2EC"); plt.close(fig)

# ---------------- final: polished Gravity Dispenser Tubes (iter 3), with Capsule_Drop and Pick_Ready_Blink clips ----------------
# Polish: alloy hangers carry the pick tray from the feed chute, the chute gets a forward lip and amber side guards, the request panel
# hangs on a bracket off the right front post, the tubes get top caps, and the centre tube's gate and one capsule are animated nodes.
# Nodes: Spares_Static, Centre_Gate (slides +Z to open), Drop_Capsule, Pick_Ready_Lamp.
from substation_r2_generator import export_nodes
GATE0 = np.array([0, .58, ZB + .15]); CAP0 = np.array([0, .62, ZB + .15]); TRAY = (ZB + .3, ZB + .5)
def final_tubes():
    p = iter3(); p.name = "Spares_Static"; xs = np.linspace(X0 + .2, X1 - .2, 7)
    g = p.P.pop("Gate_Valves"); p.add("Gate_Valves", "amber", *[box(x - .05, x + .05, .58, .6, ZB + .15, ZB + .26) for x in xs if abs(x) > 1e-6])
    p.add("Gate_Guides", "gunmetal", *[box(x - .065, x - .055, .575, .605, ZB + .1, ZB + .3) for x in xs] + [box(x + .055, x + .065, .575, .605, ZB + .1, ZB + .3) for x in xs])
    p.P.pop("Capsules"); p.add("Capsules", "white", *[cyl(x, ZB + .15, .055, y, y + .09, 10) for i, x in enumerate(xs) for y in np.arange(.62, 1.62 - .12 * (i % 3), .1) if not (abs(x) < 1e-6 and y < .63)])
    p.add("Tube_Caps", "slate", *[cyl(x, ZB + .15, .075, 1.7, 1.72, 12) for x in xs]); p.add("Chute_Lip", "alloy", box(X0 + .1, X1 - .1, .56, .6, ZB + .31, ZB + .32))
    p.add("Chute_Guards", "amber", *[box(x - .005, x + .005, .56, .6, ZB + .02, ZB + .32) for x in (X0 + .1, X1 - .1)])
    p.add("Tray_Hangers", "alloy", *[box(x - .01, x + .01, .45, .5, z - .01, z + .01) for x in (-.19, .19) for z in (TRAY[0] + .01,)], *[box(x - .01, x + .01, .45, .5, ZB + .31, ZB + .33) for x in (-.19, .19)])
    p.add("Panel_Bracket", "gunmetal", box(X1 - .25, X1 - .02, 1.25, 1.3, ZB + .26, ZB + .29))
    p.P.pop("Pick_Lamp")
    gate = Pod("Centre_Gate"); gate.add("Gate", "amber", box(-.05, .05, 0, .02, 0, .11))
    cap = Pod("Drop_Capsule"); cap.add("Capsule", "white", cyl(0, 0, .055, 0, .09, 10)); cap.add("Capsule_Band", "green", cyl(0, 0, .057, .04, .05, 10))
    lamp = Pod("Pick_Ready_Lamp"); lamp.add("Lamp", "green", box(-.05, .05, -.01, .01, -.01, 0))
    return [(p, [0, 0, 0]), (gate, GATE0.tolist()), (cap, CAP0.tolist()), (lamp, [0, PY + .11, TRAY[0]])]
def sm(t, a, b): u = np.clip((t - a) / (b - a), 0, 1); return u * u * (3 - 2 * u)
def capsule_pos(t):  # 2.4 s: gate opens 0-0.3, capsule falls to the chute 0.3-0.6, gate closes 0.6-0.9, capsule rolls forward 0.6-1.6, drops into the tray 1.6-1.9
    y = CAP0[1] + (.56 - CAP0[1] - .0) * sm(t, .3, .6) + (.45 - .56) * sm(t, 1.6, 1.9); z = CAP0[2] + (ZB + .36 - CAP0[2]) * sm(t, .6, 1.6) + (ZB + .4 - ZB - .36) * sm(t, 1.6, 1.9)
    return np.array([0, y - (0 if t < .3 else 0), z])
def clip_drop(t): return {"Centre_Gate": ("translation", GATE0 + [0, 0, .12 * (sm(t, 0, .3) - sm(t, .6, .9))]), "Drop_Capsule": ("translation", capsule_pos(t)) if t < 2.39 else ("translation", CAP0)}
def clip_blink(t): return {"Pick_Ready_Lamp": ("scale", np.ones(3) if (t % 1.0) < .5 else np.full(3, .001))}
SCLIPS = [("Capsule_Drop", clip_drop, 2.4), ("Pick_Ready_Blink", clip_blink, 1.0)]
def final_main():
    import pygltflib
    nodes = final_tubes(); gp = os.path.join(dc.ROOT, "godot/assets/models/spares_gravity_dispenser.glb"); tris = export_nodes(nodes, SCLIPS, gp); set_glass_blend(gp)
    bad = [f"{pod.name}/{k}" for pod, _ in nodes for k, (mk, m) in pod.P.items() if not all(c.is_watertight for c in m.split(only_watertight=False))]
    for st, t in (("rest", 0.0), ("capsule_in_tray", 2.2)):
        Wp = Pod("World"); P = clip_drop(t)
        for pod, T in nodes:
            off = P[pod.name][1] if pod.name in P else np.array(T)
            for k, (mk, m) in pod.P.items():
                if mk == "glass": continue
                mm = m.copy(); mm.apply_translation(off); Wp.add(pod.name + "/" + k, mk, mm)
        V = np.vstack([m.vertices for mk, m in Wp.P.values()]); print(st, "size", (V.max(0) - V.min(0)).round(3), "min", V.min(0).round(3), "max", V.max(0).round(3))
        sp = os.path.join(OUT, f"final_gravity_dispenser_{st}_sheet.png"); wg.sheet(Wp, sp, f"Final  #43 spares shelf, Gravity Dispenser Tubes ({st.replace('_', ' ')}; glass hidden)"); os.remove(sp.replace("_sheet.png", ".glb"))
    g = pygltflib.GLTF2().load(gp); print("tris", tris, "nodes", [n.name for n in g.nodes], "anims", [(a.name, len(a.channels)) for a in g.animations], "alpha", [m.alphaMode for m in g.materials if m.alphaMode], "bad", bad)
if __name__ == "__main__": final_main() if len(sys.argv) > 1 and sys.argv[1] == "final" else main()
