"""Rev C #53 Lab crate (104, 204; qty 2; 1.0 W x 0.6 D x 0.5 H and 0.9 W x 0.7 D x 0.5 H). Five iterations, no final picked yet.
No exterior #48 crate mesh exists, so this is a fresh design. Each sheet shows both: the 104 crate closed (left) and the 204 crate with its
lid ajar, showing emitter parts (right). A violet D-03 lab glyph area sits on the front and lid; it is wordless (geometric marks only).
Pivot at the bottom-centre of each crate, +Z front. Spin-down: lids latch (amber) and crates sit on gunmetal skids with floor clamps."""
import os, sys, numpy as np, trimesh
sys.path.insert(0, os.path.dirname(__file__))
from hydro_planter_generator import cyl, box, bev, blk, Pod, dc, wg, plt
from dining_chair_generator import export_final
from bath_pod_generator import set_glass_blend
from cycler_route_generator import cyl_z
from folding_counter_generator import xcyl
OUT = os.path.join(dc.ROOT, "design/assets/lab_crate")
SIZES = ((1.0, .6, .5), (.9, .7, .5)); GAP = .7  # sheet layout: 104 crate at x=-GAP, 204 crate at x=+GAP
def mv(m, dx): m = m.copy(); m.apply_translation((dx, 0, 0)); m.metadata["uv"] = m.metadata.get("uv", m.vertices[:, [0, 2]]); return m
def rot_lid(ms, hinge_y, hinge_z, deg):  # rotate lid parts about the back hinge line (X axis)
    T = trimesh.transformations.rotation_matrix(np.radians(-deg), (1, 0, 0), (0, hinge_y, hinge_z)); out = []
    for m in ms: m = m.copy(); uv = m.metadata.get("uv"); m.apply_transform(T); m.metadata["uv"] = uv if uv is not None else m.vertices[:, [0, 2]]; out.append(m)
    return out
def glyph(cx, cy, z, s=.07, axis="front"):  # D-03 lab glyph: a hex ring with three bars (wordless); front face (z) or lid top (y)
    a = np.linspace(0, 2 * np.pi, 7)[:-1]; P = []
    for k, t in enumerate(a):
        x, v = cx + s * np.cos(t), s * np.sin(t)
        P.append(box(x - .012, x + .012, cy + v - .012, cy + v + .012, z, z + .006) if axis == "front" else box(x - .012, x + .012, cy, cy + .006, z + v - .012, z + v + .012))
    for k in range(3):
        dx = (k - 1) * s * .45
        P.append(box(cx + dx - .006, cx + dx + .006, cy - s * .4, cy + s * .4, z, z + .006) if axis == "front" else box(cx + dx - .006, cx + dx + .006, cy, cy + .006, z - s * .4, z + s * .4))
    return P
def emitter(W, D, y0):  # emitter parts nested in a foam tray: two coil cans, ceramic insulators, a glass lens and a cable loop
    P = {"slate": [box(-W / 2 + .05, W / 2 - .05, y0, y0 + .06, -D / 2 + .05, D / 2 - .05)], "alloy": [], "ceramic": [], "glass": [], "green": [], "violet": []}
    for x in (-W * .25, W * .05):
        P["alloy"].append(cyl(x, 0, .08, y0 + .06, y0 + .26, 14)); P["violet"].append(cyl(x, 0, .082, y0 + .18, y0 + .2, 14))
        P["ceramic"] += [cyl(x + s * .05, 0, .015, y0 + .26, y0 + .32, 8) for s in (-1, 1)]
    P["glass"].append(cyl(W * .3, 0, .07, y0 + .06, y0 + .1, 16)); P["alloy"].append(cyl(W * .3, 0, .078, y0 + .1, y0 + .115, 16))
    P["green"].append(xcyl(-W * .25, W * .05, y0 + .1, -D * .3, .012, 6)); return P
def crate(p, dx, W, D, H, ajar, style):
    tag = "_204" if ajar else "_104"; D = D - .03; W = W - (.09 if style == 4 else 0)  # inset so front latches / side handles stay inside the envelope
    z0, z1 = -D / 2 + .015, D / 2 - .0; LT = .04; bodyH = H - LT
    def A(name, mat, *ms): p.add(name + tag, mat, *[mv(m, dx) for m in ms])
    # skids + clamps
    A("Skids", "gunmetal", *[box(-W / 2 + .05, W / 2 - .05, 0, .04, z - .03, z + .03) for z in (z0 + .08, z1 - .08)])
    A("Floor_Clamps", "amber", *[box(x - .04, x + .04, 0, .015, z - .045, z + .045) for x in (-W / 2 + .08, W / 2 - .08) for z in (z0 + .08, z1 - .08)])
    shell = "white" if style in (1, 4) else "slate"; trim = "gunmetal" if style != 3 else "alloy"
    if ajar:  # open-top tub so the emitter parts read
        th = .025; A("Body", shell, box(-W / 2, W / 2, .04, .07, z0, z1), box(-W / 2, -W / 2 + th, .04, bodyH, z0, z1), box(W / 2 - th, W / 2, .04, bodyH, z0, z1),
                    box(-W / 2 + th, W / 2 - th, .04, bodyH, z0, z0 + th), box(-W / 2 + th, W / 2 - th, .04, bodyH, z1 - th, z1))
        for mat, L in emitter(W, D, .07).items():
            if L: A("Emitter_" + mat, mat, *L)
    else: A("Body", shell, blk(-W / 2, W / 2, .04, bodyH, z0, z1, .015, 1))
    # style details
    if style == 1:  # ribbed shell: horizontal gunmetal ribs
        A("Ribs", trim, *[b for y in (.12, .34) for b in (box(-W / 2 - .008, W / 2 + .008, y, y + .025, z0 - .008, z0), box(-W / 2 - .008, W / 2 + .008, y, y + .025, z1, z1 + .008),
                                                   box(-W / 2 - .008, -W / 2, y, y + .025, z0, z1), box(W / 2, W / 2 + .008, y, y + .025, z0, z1))])  # hollow ring bands
    elif style == 2:  # corner-armoured: alloy corner guards
        A("Corner_Guards", "alloy", *[box(x - .035, x + .035, .04, bodyH, z - .035, z + .035) for x in (-W / 2 + .025, W / 2 - .025) for z in (z0 + .025, z1 - .025)])
    elif style == 3:  # frame crate: open alloy frame edges around slate panels
        A("Frame", trim, *[box(-W / 2 - .01, W / 2 + .01, y, y + .03, z - .01, z + .01) for y in (.04, bodyH - .03) for z in (z0, z1)] + [box(x - .01, x + .01, .04, bodyH, z - .01, z + .01) for x in (-W / 2, W / 2) for z in (z0, z1)])
    elif style == 4:  # soft-carry: side handles + strap bands
        A("Handles", "gunmetal", *[box(s * (W / 2 + .03) - .015, s * (W / 2 + .03) + .015, .28, .31, -.12, .12) for s in (-1, 1)], *[box(s * (W / 2) - (.03 if s > 0 else 0), s * (W / 2) + (.0 if s > 0 else .03), .26, .33, z - .015, z + .015) for s in (-1, 1) for z in (-.12, .12)])
        A("Straps", "violet", *[box(x - .025, x + .025, .04, bodyH + .005, z, z + .006) for x in (-W * .3, W * .3) for z in (z0 - .006, z1)])  # face straps only (tub stays open)
    elif style == 5:  # stacking crate: corner stacking lugs on lid and recessed feet, green seal-status lamp
        A("Stack_Lugs", "alloy", *[box(x - .03, x + .03, H, H + .025, z - .03, z + .03) for x in (-W / 2 + .05, W / 2 - .05) for z in (z0 + .05, z1 - .05)] if not ajar else [box(x - .03, x + .03, .04, .07, z - .03, z + .03) for x in (-W / 2 + .05, W / 2 - .05) for z in (z0 + .05, z1 - .05)])
        A("Seal_Lamp", "green", box(W / 2 - .12, W / 2 - .06, bodyH - .07, bodyH - .05, z1, z1 + .006))
    # front glyph area (violet plate + white glyph marks)
    gx = -W * .18; gy = bodyH * .55
    A("Glyph_Plate", "violet", box(gx - .12, gx + .12, gy - .1, gy + .1, z1, z1 + .006)); A("Glyph_Marks", "white", *glyph(gx, gy, z1 + .006))
    # latches
    A("Latches", "amber", *[box(x - .03, x + .03, bodyH - .06, bodyH + .01, z1, z1 + .015) for x in (W * .15, W * .35)])
    # lid (hinged at back top edge)
    lid = [blk(-W / 2, W / 2, bodyH, H, z0, z1, .01, 1)]; lidg = [box(-.1, .1, H, H + .006, -.1, .1)]; marks = glyph(0, H + .006, 0, .06, "top")
    hinge = [cyl_z(x, bodyH, .015, z0 - .015, z0 + .03, 8) for x in (-W * .3, W * .3)]
    if ajar: lid, lidg, marks = (rot_lid(L, bodyH, z0, 28) for L in (lid, lidg, marks)); A("Lid_Prop", "alloy", box(W / 2 - .06, W / 2 - .045, bodyH - .1, bodyH + .17, z0 + .1, z0 + .115))
    A("Lid", "slate" if shell == "white" else "white", *lid); A("Lid_Glyph", "violet", *lidg); A("Lid_Glyph_Marks", "white" if shell == "slate" else "gunmetal", *marks); A("Hinges", "alloy", *hinge)
def make(style, name):
    p = Pod(name)
    for (W, D, H), dx, aj in zip(SIZES, (-GAP, GAP), (False, True)): crate(p, dx, W, D, H, aj, style)
    return p
ITERS = [(1, "Ribbed_Shell"), (2, "Corner_Armoured"), (3, "Frame_Crate"), (4, "Strapped_Carry"), (5, "Stacking_Seal")]
def main():
    os.makedirs(OUT, exist_ok=True); isos = []
    for i, (st, nm) in enumerate(ITERS, 1):
        p = make(st, nm); full = dict(p.P); p.P = {k: v for k, v in full.items() if v[0] != "glass"}
        tris, iso, lo, hi, bad = wg.sheet(p, os.path.join(OUT, f"iter_0{i}_sheet.png"), f"iter_0{i}  {nm}  (#53 lab crate: 104 closed 1.0x0.6x0.5 | 204 ajar 0.9x0.7x0.5)")
        tmp = os.path.join(OUT, f"iter_0{i}.glb")
        if os.path.exists(tmp): os.remove(tmp)
        p.P = full; T = {}
        for s in ("_104", "_204"):
            q = Pod(nm + s); W, D, H = SIZES[s == "_204"]; crate(q, 0, W, D, H, s == "_204", st)  # export each crate on its own bottom-centre pivot
            gp = os.path.join(OUT, f"iter_0{i}{s}.glb"); t, geo = export_final(q.P, [gp]); set_glass_blend(gp)
            V = np.vstack([g[1] for g in geo.values()]); T[s] = (t, (V.max(0) - V.min(0)).round(3), V.min(0).round(3), V.max(0).round(3))
        isos.append((nm, iso)); print(i, nm, T, "bad", bad)
    fig, axs = plt.subplots(3, 2, figsize=(16, 12), facecolor="#F4F2EC")
    for ax in axs.flat: ax.axis("off")
    for ax, (i, (n, im)) in zip(axs.flat, enumerate(isos, 1)): ax.imshow(im); ax.set_title(f"{i}. {n}", fontsize=11, color="#555")
    plt.tight_layout(rect=(0, 0, 1, .97)); fig.savefig(os.path.join(OUT, "overview.png"), dpi=90, facecolor="#F4F2EC"); plt.close(fig)
if __name__ == "__main__" and len(sys.argv) == 1: main()

# ---------------- final: Frame_Crate (iter 3), picked by Jared Oct 30 ----------------
# Polish: frame edges brought flush to the rev C width, lid glyph decals kept inside the 0.5 m height, depth restored to the full envelope.
def final_main():
    import pygltflib
    sheet = Pod("Frame_Crate_Final"); res = {}
    for (W, D, H), dx, aj, nm in zip(SIZES, (-GAP, GAP), (False, True), ("lab_crate_frame_104", "lab_crate_frame_204")):
        q = Pod(nm); crate(q, 0, W - .02, D + .015, H - .012, aj, 3); crate(sheet, dx, W - .02, D + .015, H - .012, aj, 3)
        nouv = [k for k, (mk, m) in q.P.items() if "uv" not in m.metadata]; bad = [k for k, (mk, m) in q.P.items() if not all(c.is_watertight for c in m.split(only_watertight=False))]
        gp = os.path.join(dc.ROOT, "godot/assets/models", nm + ".glb"); t, geo = export_final(q.P, [gp]); set_glass_blend(gp)
        V = np.vstack([g[1] for g in geo.values()]); g = pygltflib.GLTF2().load(gp)
        print(nm, "tris", t, "size", (V.max(0) - V.min(0)).round(3), "lo", V.min(0).round(3), "hi", V.max(0).round(3), "bad", bad, "nouv", nouv, "alpha", [m.alphaMode for m in g.materials if m.alphaMode])
    sheet.P = {k: v for k, v in sheet.P.items() if v[0] != "glass"}
    sp = os.path.join(OUT, "final_frame_crate_sheet.png"); wg.sheet(sheet, sp, "Final  #53 lab crate, Frame Crate: 104 closed 1.0x0.6x0.5 | 204 lid ajar 0.9x0.7x0.5 (glass hidden)"); os.remove(sp.replace("_sheet.png", ".glb"))
if __name__ == "__main__" and len(sys.argv) > 1 and sys.argv[1] == "final": final_main()
