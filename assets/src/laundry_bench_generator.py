"""Rev C #39 Laundry bench (Laundry; qty 1; 1.2 W x 0.4 D x 0.45 H). Five iterations in the family language.
Empty: no laundry, clothes or shoes modeled. Pivot at the bottom-centre, +Z front, wall at -Z.
Spin-down: the bench bolts to the floor or wall rail; every lid, bin and flap latches with amber catches."""
import os, sys, numpy as np, trimesh
sys.path.insert(0, os.path.dirname(__file__))
from hydro_planter_generator import cyl, box, bev, blk, Pod, dc, wg, plt
from dining_chair_generator import export_final
from bath_pod_generator import set_glass_blend
OUT = os.path.join(dc.ROOT, "design/assets/laundry_bench")
W, D, H = 1.2, .4, .45; X0, X1, ZB, ZF = -W / 2, W / 2, -D / 2, D / 2; ST = .04
def feet(p, xs=(-W / 2 + .06, W / 2 - .06), zs=(ZB + .05, ZF - .05)):
    p.add("Floor_Bolts", "amber", *[cyl(x, z, .012, 0, .008, 6) for x in xs for z in zs])
def iter1():  # slatted rail bench: gunmetal sled-leg frames, white seat slats, a low alloy stretcher
    p = Pod("Slatted_Rail_Bench"); n = 5; zs = np.linspace(ZB, ZF, n + 1)
    p.add("Seat_Slats", "white", *[blk(X0, X1, H - ST, H, zs[i] + .006, zs[i + 1] - .006, .005, 1) for i in range(n)])
    for x in (X0 + .08, X1 - .08):
        p.add("Sled_Legs", "gunmetal", box(x - .02, x + .02, .02, H - ST, ZB + .03, ZB + .07), box(x - .02, x + .02, .02, H - ST, ZF - .07, ZF - .03),
              box(x - .02, x + .02, 0, .03, ZB + .02, ZF - .02), box(x - .02, x + .02, H - ST - .03, H - ST, ZB + .02, ZF - .02))
    p.add("Stretcher", "alloy", box(X0 + .1, X1 - .1, .14, .17, -.015, .015)); p.add("Floor_Bolts", "amber", *[cyl(x, z, .01, 0, .034, 6) for x in (X0 + .08, X1 - .08) for z in (ZB + .045, ZF - .045)])
    return p
def iter2():  # storage box bench: closed white carcass, slate padded lift lid, two amber lid latches and a gunmetal plinth
    p = Pod("Storage_Box_Bench"); p.add("Plinth", "gunmetal", box(X0 + .02, X1 - .02, 0, .05, ZB + .02, ZF - .03))
    p.add("Carcass", "white", blk(X0, X1, .05, H - .06, ZB, ZF, .006, 1)); p.add("Lid_Pad", "slate", blk(X0 + .005, X1 - .005, H - .06, H, ZB + .005, ZF - .005, .015, 2))
    p.add("Lid_Hinge_Bar", "alloy", box(X0 + .05, X1 - .05, H - .07, H - .055, ZB - .006, ZB)); p.add("Lid_Latches", "amber", *[box(x - .035, x + .035, H - .09, H - .065, ZF, ZF + .006) for x in (-W / 4, W / 4)])
    p.add("Front_Panel_Lines", "alloy", *[box(x - .003, x + .003, .07, H - .1, ZF, ZF + .003) for x in (-W / 6, W / 6)]); feet(p); return p
def iter3():  # wall-hung flip seat: seat on a gunmetal wall rail with two diagonal stays, open floor below, seat flips up to the rail
    p = Pod("Wall_Flip_Seat"); p.add("Wall_Rail", "gunmetal", blk(X0, X1, 0, H + .25, ZB, ZB + .03, .004, 1))
    p.add("Seat", "white", blk(X0 + .02, X1 - .02, H - ST, H, ZB + .045, ZF, .008, 1)); p.add("Seat_Hinge", "alloy", box(X0 + .02, X1 - .02, H - ST - .02, H - ST, ZB + .03, ZB + .05))
    St = []
    for x in (X0 + .12, X1 - .12):
        for k in range(6): t0, t1 = k / 6, (k + 1) / 6; St.append(box(x - .012, x + .012, .12 + (H - ST - .12) * t0, .12 + (H - ST - .12) * t1, ZB + .03, ZB + .03 + (ZF - .06 - ZB - .03) * t1))
    p.add("Diagonal_Stays", "gunmetal", *St); p.add("Flip_Catches", "amber", *[box(x - .03, x + .03, H + .17, H + .2, ZB + .03, ZB + .045) for x in (-W / 4, W / 4)])
    p.add("Rail_Bolts", "alloy", *[cyl(x, ZB + .03, .01, y, y + .012, 6) for x in (X0 + .1, 0, X1 - .1) for y in (.08, H + .18)]); return p
def iter4():  # shoe cubby bench: seat over three open cubbies with a slate back and alloy-lipped floor shelf (empty)
    p = Pod("Cubby_Bench"); xs = np.linspace(X0, X1, 4)
    p.add("Seat_Top", "white", blk(X0, X1, H - ST, H, ZB, ZF, .008, 1)); p.add("Plinth", "gunmetal", box(X0 + .02, X1 - .02, 0, .04, ZB + .02, ZF - .04))
    p.add("Uprights", "white", *[box(max(x - .012, X0), min(x + .012, X1), .04, H - ST, ZB, ZF - .01) for x in xs]); p.add("Back_Panel", "slate", box(X0, X1, .04, H - ST, ZB, ZB + .015))
    p.add("Cubby_Floor", "white", box(X0, X1, .04, .06, ZB, ZF - .01)); p.add("Mid_Shelf", "alloy", *[box(xs[i] + .012, xs[i + 1] - .012, .22, .235, ZB + .015, ZF - .03) for i in range(3)])
    p.add("Shelf_Lips", "alloy", *[box(xs[i] + .012, xs[i + 1] - .012, .06, .09, ZF - .03, ZF - .015) for i in range(3)]); feet(p); return p
def iter5():  # padded bench with basket shelf: violet cushion on an alloy tray, gunmetal four-leg frame, lower lipped shelf with amber tie-down cleats
    p = Pod("Padded_Shelf_Bench"); lx, lz = (X0 + .04, X1 - .04), (ZB + .04, ZF - .04)
    p.add("Legs", "gunmetal", *[box(x - .02, x + .02, 0, H - .07, z - .02, z + .02) for x in lx for z in lz]); p.add("Seat_Tray", "alloy", box(X0, X1, H - .08, H - .06, ZB, ZF))
    p.add("Cushion", "violet", blk(X0 + .01, X1 - .01, H - .06, H, ZB + .01, ZF - .01, .02, 2)); p.add("Lower_Shelf", "alloy", box(X0 + .02, X1 - .02, .1, .12, ZB + .02, ZF - .02))
    p.add("Shelf_Lip", "alloy", box(X0 + .02, X1 - .02, .12, .15, ZF - .03, ZF - .02), box(X0 + .02, X1 - .02, .12, .15, ZB + .02, ZB + .03))
    p.add("Tie_Down_Cleats", "amber", *[box(x - .02, x + .02, .12, .135, -.015, .015) for x in (-W / 4, W / 4)]); feet(p, lx, lz); return p
def main():
    os.makedirs(OUT, exist_ok=True); isos = []
    for i, fn in enumerate([iter1, iter2, iter3, iter4, iter5], 1):
        p = fn(); full = dict(p.P); p.P = {k: v for k, v in full.items() if v[0] != "glass"}  # glass hidden in sheet renders (BLEND in glb)
        tris, iso, lo, hi, bad = wg.sheet(p, os.path.join(OUT, f"iter_0{i}_sheet.png"), f"iter_0{i}  {p.name}  (#39 laundry bench)")
        p.P = full; gp = os.path.join(OUT, f"iter_0{i}.glb"); tris, _ = export_final(p.P, [gp]); set_glass_blend(gp)
        isos.append((p.name, iso)); print(i, p.name, tris, (hi - lo).round(3), "bad", bad)
    fig, axs = plt.subplots(3, 2, figsize=(16, 12), facecolor="#F4F2EC")
    for ax in axs.flat: ax.axis("off")
    for ax, (i, (n, im)) in zip(axs.flat, enumerate(isos, 1)): ax.imshow(im); ax.set_title(f"{i}. {n}", fontsize=11, color="#555")
    plt.tight_layout(rect=(0, 0, 1, .97)); fig.savefig(os.path.join(OUT, "overview.png"), dpi=90, facecolor="#F4F2EC"); plt.close(fig)

# ---------------- final: polished Wall Flip Seat (iter 3), with flip clips ----------------
# Seat hinges on a knuckle in front of the wall rail; two gunmetal swing arms under the seat carry it and swing back flat
# along the wall before the seat flips up. Nodes: Bench_Static, Seat (pivot = hinge axis), Swing_Arm_1..2 (pivot = arm pin).
from folding_counter_generator import xcyl, qx, qy, ease
FPS = 30; ZR = ZB + .03; YH, ZH = H - ST, ZB + .085; SD = ZF - ZH; RT = .8; ARMX = (-.5, .1); ARML = .3; ZP = -.1
def final_flip():
    S = Pod("Bench_Static")
    S.add("Wall_Rail", "gunmetal", blk(X0, X1, 0, RT, ZB, ZR, .004, 1)); S.add("Floor_Shoe", "gunmetal", box(X0, X1, 0, .03, ZR, ZR + .03))
    S.add("Rail_Bolts", "alloy", *[cyl(x, ZR, .01, y, y + .012, 6) for x in (X0 + .1, -.2, .2, X1 - .1) for y in (.1, RT - .08)])
    S.add("Hinge_Mounts", "alloy", *[box(x - .04, x + .04, YH - .03, YH - .006, ZR, ZH - .02) for x in (X0 + .08, 0, X1 - .08)])
    S.add("Arm_Mounts", "gunmetal", *[box(x - .025, x + .025, YH - .08, YH - .028, ZR, ZP + .02) for x in ARMX])
    S.add("Arm_Pins", "amber", *[cyl(x, ZP, .01, YH - .03, YH - .026, 8) for x in ARMX])
    S.add("Stow_Catches", "amber", *[box(x - .035, x + .035, YH + SD + .012, YH + SD + .03, ZR, ZH - .015) for x in (-W / 4, W / 4)])
    Se = Pod("Seat")   # local frame: origin on the hinge axis, seat runs +Z when down
    Se.add("Seat_Board", "white", blk(X0 + .02, X1 - .02, -.004, ST - .004, .012, SD - .006, .008, 1)); Se.add("Hinge_Knuckle", "alloy", xcyl(X0 + .1, X1 - .1, .008, 0, .012))
    Se.add("Front_Edge_Strip", "alloy", box(X0 + .02, X1 - .02, .0, ST - .008, SD - .006, SD))
    Se.add("Lift_Grip", "amber", box(-.06, .06, -.012, -.004, SD - .06, SD - .02))
    A = []
    for i, x in enumerate(ARMX):  # local frame: origin on the pin top; stowed the arm points +X along the wall
        a = Pod(f"Swing_Arm_{i + 1}"); a.add("Arm", "gunmetal", box(-.012, ARML, -.022, 0, -.01, .01)); a.add("Arm_Pad", "slate", box(ARML - .07, ARML - .01, 0, .003, -.008, .008))
        A.append((a, np.array([x, YH - .026 + .022 - .004, ZP])))
    return S, Se, A
def fpose(t, up):  # up: seat 0-1.4 s then arms in 1.4-2.0 s; down: arms out 0-0.6 s then seat 0.6-2.0 s
    if up: s, a = ease(t, 0, 1.4), 1 - ease(t, 1.4, 2.0)
    else: a, s = ease(t, 0, .6), 1 - ease(t, .6, 2.0)
    return -np.pi / 2 * s, -np.pi / 2 * a
FCLIPS = [("Seat_Flip_Up", True, 2.0), ("Seat_Flip_Down", False, 2.0)]
def fworld(S, Se, A, s, a):
    Wp = Pod("World"); R = trimesh.transformations.rotation_matrix; Tm = trimesh.transformations.translation_matrix
    for k, (mk, m) in S.P.items(): Wp.add(k, mk, m.copy())
    for k, (mk, m) in Se.P.items(): mm = m.copy(); mm.apply_transform(Tm([0, YH, ZH]) @ R(s, [1, 0, 0])); Wp.add(k, mk, mm)
    for ap, piv in A:
        for k, (mk, m) in ap.P.items(): mm = m.copy(); mm.apply_transform(Tm(piv) @ R(a, [0, 1, 0])); Wp.add("Swing_" + k, mk, mm)
    return Wp
def export_flip(S, Se, A, path):
    from dining_chair_generator import shade_split, _col, FMAT
    from pygltflib import (GLTF2, Scene, Node, Mesh, Primitive, Attributes, Buffer, BufferView, Accessor, Material,
                           PbrMetallicRoughness, Animation, AnimationSampler, AnimationChannel, AnimationChannelTarget)
    g = GLTF2(); blob = bytearray(); mats = {}; tris = [0]
    def add(arr, target, ctype, typ, mm=False):
        arr = np.ascontiguousarray(arr); off = len(blob); blob.extend(arr.tobytes())
        while len(blob) % 4: blob.append(0)
        g.bufferViews.append(BufferView(buffer=0, byteOffset=off, byteLength=arr.nbytes, target=target))
        acc = Accessor(bufferView=len(g.bufferViews) - 1, componentType=ctype, count=len(arr), type=typ)
        if mm: a2 = arr.reshape(len(arr), -1); acc.min = a2.min(0).tolist(); acc.max = a2.max(0).tolist()
        g.accessors.append(acc); return len(g.accessors) - 1
    def node(pod, T):
        bym = {}; prims = []
        for k, (mk, m) in pod.P.items(): bym.setdefault(mk, []).append(shade_split(m))
        for mk, lst in bym.items():
            if mk not in mats:
                pm = FMAT[mk]; mats[mk] = len(g.materials)
                g.materials.append(Material(name=pm.name, emissiveFactor=_col(pm.emissiveFactor if pm.emissiveFactor is not None else [0, 0, 0]),
                    pbrMetallicRoughness=PbrMetallicRoughness(baseColorFactor=_col(pm.baseColorFactor), metallicFactor=float(pm.metallicFactor), roughnessFactor=float(pm.roughnessFactor))))
            o = 0; V, N, U, F = [], [], [], []
            for v, n, u, f in lst: V.append(v); N.append(n); U.append(u); F.append(f + o); o += len(v)
            V, N, U, F = map(np.vstack, (V, N, U, F)); tris[0] += len(F)
            at = Attributes(POSITION=add(V.astype(np.float32), 34962, 5126, "VEC3", True), NORMAL=add(N.astype(np.float32), 34962, 5126, "VEC3"), TEXCOORD_0=add(U.astype(np.float32), 34962, 5126, "VEC2"))
            prims.append(Primitive(attributes=at, indices=add(F.astype(np.uint32).ravel(), 34963, 5125, "SCALAR"), material=mats[mk]))
        g.meshes.append(Mesh(name=pod.name, primitives=prims)); g.nodes.append(Node(name=pod.name, mesh=len(g.meshes) - 1, translation=[float(c) for c in T])); return len(g.nodes) - 1
    root = node(S, [0, 0, 0]); seat = node(Se, [0, YH, ZH]); arms = [node(a, p) for a, p in A]
    for n in arms: g.nodes[n].rotation = [float(c) for c in qy(-np.pi / 2)]  # rest pose = seat down, arms out
    g.nodes[root].children = [seat] + arms; g.scenes = [Scene(name="LaundryBench", nodes=[root])]; g.scene = 0
    for name, up, dur in FCLIPS:
        ts = np.round(np.arange(0, dur + 1e-6, 1 / FPS), 5).astype(np.float32); P = [fpose(float(t), up) for t in ts]
        an = Animation(name=name, samplers=[], channels=[]); tin = add(ts, None, 5126, "SCALAR", True)
        for nid, q in [(seat, np.array([qx(p[0]) for p in P]))] + [(n, np.array([qy(p[1]) for p in P])) for n in arms]:
            an.samplers.append(AnimationSampler(input=tin, output=add(q.astype(np.float32), None, 5126, "VEC4"), interpolation="LINEAR"))
            an.channels.append(AnimationChannel(sampler=len(an.samplers) - 1, target=AnimationChannelTarget(node=nid, path="rotation")))
        g.animations.append(an)
    g.buffers = [Buffer(byteLength=len(blob))]; g.set_binary_blob(bytes(blob)); g.save_binary(path); return tris[0]
def final_main():
    import pygltflib
    S, Se, A = final_flip(); gp = os.path.join(dc.ROOT, "godot/assets/models/laundry_bench_wall_flip_seat.glb"); tris = export_flip(S, Se, A, gp)
    bad = [k for pod in [S, Se] + [a for a, _ in A] for k, (mk, m) in pod.P.items() if not all(c.is_watertight for c in m.split(only_watertight=False))]
    # swept-clearance check: every frame of both clips, arms vs seat (AABB overlap volume) and seat vs rail face
    worst = []
    for name, up, dur in FCLIPS:
        for t in np.arange(0, dur + 1e-6, 1 / 15):
            s, a = fpose(t, up); Wp = fworld(S, Se, A, s, a)
            seatV = np.vstack([m.vertices for k, (mk, m) in Wp.P.items() if k in Se.P]); worst.append(seatV[:, 2].min() - ZR)
            for k, (mk, m) in Wp.P.items():
                if k.startswith("Swing_Arm") and not k.endswith("Pad"):
                    if Wp.P["Seat_Board"][1].contains(m.vertices).any() or m.contains(Wp.P["Seat_Board"][1].vertices).any(): print("COLLIDE", name, round(t, 2))
    print("seat-to-rail min gap", round(min(worst), 4))
    for st, (s, a) in (("down", (0, -np.pi / 2)), ("stowed", (-np.pi / 2, 0))):
        Wp = fworld(S, Se, A, s, a); V = np.vstack([m.vertices for mk, m in Wp.P.values()]); print(st, "size", (V.max(0) - V.min(0)).round(3), "min", V.min(0).round(3), "max", V.max(0).round(3))
        sp = os.path.join(OUT, f"final_wall_flip_seat_{st}_sheet.png"); wg.sheet(Wp, sp, f"Final  #39 laundry bench, Wall Flip Seat, {st}"); os.remove(sp.replace("_sheet.png", ".glb"))
    g = pygltflib.GLTF2().load(gp); print("tris", tris, "nodes", [n.name for n in g.nodes], "anims", [(an.name, len(an.channels)) for an in g.animations], "bad", bad)
if __name__ == "__main__": final_main() if len(sys.argv) > 1 and sys.argv[1] == "final" else main()
