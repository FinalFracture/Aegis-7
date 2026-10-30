"""Rev C #38 folding counter (Laundry; qty 2: a 3.5 m run and a 3.0 m run (C.2a, N wall); 0.6 D x 0.9 H). Five iterations, family language, shown at 3.5 m.
The run length is a parameter, so the final exports both lengths. Empty: no laundry or clothes modeled. Pivot at the bottom-centre, +Z front, wall at -Z.
Spin-down: the counter bolts to the wall rail and floor; every door, drawer, basket and bin latches with amber catches."""
import os, sys, numpy as np, trimesh
sys.path.insert(0, os.path.dirname(__file__))
from hydro_planter_generator import cyl, box, bev, blk, Pod, dc, wg, plt
from dining_chair_generator import export_final
from bath_pod_generator import set_glass_blend
OUT = os.path.join(dc.ROOT, "design/assets/folding_counter")
D, H = .6, .9; ZB, ZF = -D / 2, D / 2; TOP = .04
def top(p, L, mat="white"):
    p.add("Worktop", mat, blk(-L / 2, L / 2, H - TOP, H, ZB, ZF, .008, 1)); p.add("Worktop_Nosing", "alloy", box(-L / 2, L / 2, H - TOP - .005, H - .005, ZF - .008, ZF))
    p.add("Wall_Rail", "gunmetal", blk(-L / 2, L / 2, H - .14, H - TOP, ZB, ZB + .02, .004, 1)); p.add("Rail_Bolts", "alloy", *[cyl(x, ZB + .02, .01, H - .1, H - .09, 6) for x in np.linspace(-L / 2 + .2, L / 2 - .2, int(L / .7) + 1)])
def bays(L, w=.6):
    n = max(1, int(round(L / w))); return np.linspace(-L / 2, L / 2, n + 1)
def carcass(p, L, xs, mat="white"):
    p.add("Uprights", mat, *[box(max(x - .012, -L / 2), min(x + .012, L / 2), 0, H - TOP, ZB, ZF - .03) for x in xs]); p.add("Plinth", "gunmetal", box(-L / 2, L / 2, 0, .08, ZB, ZF - .06))
    p.add("Bottom_Panel", mat, box(-L / 2, L / 2, .08, .1, ZB, ZF - .03)); p.add("Back_Panel", "slate", box(-L / 2, L / 2, .08, H - TOP, ZB, ZB + .015))
def fronts(p, xs, rows, mat, pull="amber"):
    F, Pl = [], []
    for i in range(len(xs) - 1):
        r = rows[i % len(rows)]; ys = np.linspace(.1, H - TOP - .01, r + 1)
        for j in range(r):
            x0, x1 = xs[i] + .015, xs[i + 1] - .015; F.append(box(x0, x1, ys[j] + .006, ys[j + 1] - .006, ZF - .03, ZF - .012)); c = (x0 + x1) / 2
            Pl.append(box(c - .08, c + .08, ys[j + 1] - .05, ys[j + 1] - .035, ZF - .012, ZF))
    p.add("Fronts", mat, *F); p.add("Pull_Latches", pull, *Pl)
L0 = 3.5
def iter1(L=L0):  # open base: worktop on gunmetal leg frames, two open alloy shelves with lips (baskets go here later)
    p = Pod("Open_Base"); top(p, L); xs = bays(L, .9)
    p.add("Leg_Frames", "gunmetal", *[box(max(x - .02, -L / 2), min(x + .02, L / 2), 0, H - TOP, z - .02, z + .02) for x in xs for z in (ZB + .04, ZF - .06)])
    p.add("Open_Shelves", "alloy", *[box(-L / 2, L / 2, y, y + .02, ZB + .02, ZF - .06) for y in (.12, .45)]); p.add("Shelf_Lips", "gunmetal", *[box(-L / 2, L / 2, y + .02, y + .05, ZF - .07, ZF - .06) for y in (.12, .45)])
    p.add("Foot_Clamps", "amber", *[box(max(x - .02, -L / 2), min(x + .02, L / 2), 0, .02, ZF - .04, ZF - .02) for x in xs]); return p
def iter2(L=L0):  # cabinet base: closed white bays, alternating door and three-drawer columns, slate fronts
    p = Pod("Cabinet_Base"); top(p, L); xs = bays(L); carcass(p, L, xs); fronts(p, xs, [1, 3], "slate"); return p
def iter3(L=L0):  # fold-down leaf: wall-hung counter with a front leaf that folds up to widen the folding surface; open floor below
    p = Pod("Fold_Down_Leaf"); p.add("Worktop", "white", blk(-L / 2, L / 2, H - TOP, H, ZB, ZF - .2, .008, 1)); p.add("Wall_Rail", "gunmetal", blk(-L / 2, L / 2, 0, H - TOP, ZB, ZB + .03, .004, 1))
    p.add("Fold_Leaf", "white", box(-L / 2 + .01, L / 2 - .01, H - TOP - .4, H - TOP - .01, ZF - .23, ZF - .2)); p.add("Leaf_Hinge_Bar", "alloy", box(-L / 2, L / 2, H - TOP - .02, H - TOP, ZF - .22, ZF - .19))
    p.add("Cantilever_Brackets", "gunmetal", *[box(x - .015, x + .015, H - .22, H - TOP, ZB + .03, ZF - .25) for x in np.linspace(-L / 2 + .2, L / 2 - .2, 5)]); p.add("Leaf_Latches", "amber", *[box(x - .03, x + .03, H - TOP - .41, H - TOP - .39, ZF - .2, ZF - .19) for x in (-L / 4, L / 4)])
    p.add("Support_Struts_Stowed", "alloy", *[box(x - .01, x + .01, H - TOP - .38, H - TOP - .05, ZF - .25, ZF - .235) for x in (-L / 3, 0, L / 3)]); return p
def iter4(L=L0):  # basket bays: open bays with pull-out alloy wire baskets (empty) on runners, amber basket latches
    p = Pod("Basket_Bays"); top(p, L); xs = bays(L); carcass(p, L, xs); B, R, Lt = [], [], []
    for i in range(len(xs) - 1):
        x0, x1 = xs[i] + .03, xs[i + 1] - .03
        for y in (.12, .45):
            B += [box(x0, x1, y, y + .012, ZB + .04, ZF - .05), box(x0, x1, y, y + .25, ZF - .062, ZF - .05), box(x0, x1, y, y + .25, ZB + .04, ZB + .052), box(x0, x0 + .012, y, y + .25, ZB + .04, ZF - .05), box(x1 - .012, x1, y, y + .25, ZB + .04, ZF - .05)]
            R += [box(x0 - .018, x0, y + .1, y + .115, ZB + .04, ZF - .05), box(x1, x1 + .018, y + .1, y + .115, ZB + .04, ZF - .05)]; Lt.append(box((x0 + x1) / 2 - .05, (x0 + x1) / 2 + .05, y + .2, y + .23, ZF - .05, ZF - .04))
    p.add("Wire_Baskets", "alloy", *B); p.add("Basket_Runners", "gunmetal", *R); p.add("Basket_Latches", "amber", *Lt); return p
def iter5(L=L0):  # sorting bins: tilt-out sorting bins (violet, green, amber tags) across the run, a drawer row above them
    p = Pod("Sorting_Bins"); top(p, L); xs = bays(L); carcass(p, L, xs)
    F, T, Pl = [], [], []; cols = ("violet", "green", "amber")
    for i in range(len(xs) - 1):
        x0, x1 = xs[i] + .015, xs[i + 1] - .015; c = (x0 + x1) / 2
        F.append(box(x0, x1, .1, .62, ZF - .03, ZF - .012)); F.append(box(x0, x1, .63, H - TOP - .01, ZF - .03, ZF - .012))
        T.append((cols[i % 3], box(c - .06, c + .06, .52, .56, ZF - .012, ZF - .006))); Pl += [box(c - .1, c + .1, .58, .6, ZF - .012, ZF), box(c - .08, c + .08, H - TOP - .06, H - TOP - .045, ZF - .012, ZF)]
    p.add("Bin_Fronts", "white", *F); p.add("Pull_Latches", "amber", *Pl)
    for k in cols: p.add(f"Sort_Tag_{k}", k, *[m for c, m in T if c == k])
    return p

def main():
    os.makedirs(OUT, exist_ok=True); isos = []
    for i, fn in enumerate([iter1, iter2, iter3, iter4, iter5], 1):
        p = fn(); full = dict(p.P); p.P = {k: v for k, v in full.items() if v[0] != "glass"}  # glass hidden in sheet renders (BLEND in glb)
        tris, iso, lo, hi, bad = wg.sheet(p, os.path.join(OUT, f"iter_0{i}_sheet.png"), f"iter_0{i}  {p.name}  (#38 folding counter (3.5 m run shown))")
        p.P = full; gp = os.path.join(OUT, f"iter_0{i}.glb"); tris, _ = export_final(p.P, [gp]); set_glass_blend(gp)
        isos.append((p.name, iso)); print(i, p.name, tris, (hi - lo).round(3), "bad", bad)
    fig, axs = plt.subplots(3, 2, figsize=(16, 12), facecolor="#F4F2EC")
    for ax in axs.flat: ax.axis("off")
    for ax, (i, (n, im)) in zip(axs.flat, enumerate(isos, 1)): ax.imshow(im); ax.set_title(f"{i}. {n}", fontsize=11, color="#555")
    plt.tight_layout(rect=(0, 0, 1, .97)); fig.savefig(os.path.join(OUT, "overview.png"), dpi=90, facecolor="#F4F2EC"); plt.close(fig)

# ---------------- final: polished Fold-Down Leaf (iter 3), both runs, with a fold clip ----------------
# Leaf hinges on a piano-hinge knuckle at the worktop front edge; three swing brackets under the worktop
# rotate out under the raised leaf. Nodes: Counter_Static, Leaf (pivot = hinge axis), Swing_Bracket_1..3 (pivot = bracket pin).
ZH = ZF - .2; ZFB = ZH + .02; YC, ZC = H - .015, ZFB + .015; LEAF = .415; FPS = 30
def xcyl(x0, x1, y, z, r, s=12):
    m = trimesh.creation.cylinder(radius=r, height=x1 - x0, sections=s); m.apply_transform(trimesh.transformations.rotation_matrix(np.pi / 2, [0, 1, 0]))
    m.apply_translation([(x0 + x1) / 2, y, z]); m.metadata["uv"] = np.c_[m.vertices[:, 0], np.arctan2(m.vertices[:, 1] - y, m.vertices[:, 2] - z) * r]; return m
def br_x(L): return [-L / 3 - .2, -.2, L / 3 - .2]
def final_fold(L=L0):
    S = Pod("Counter_Static")
    S.add("Worktop", "white", blk(-L / 2, L / 2, H - TOP, H, ZB, ZH, .008, 1)); S.add("Hinge_Bar", "alloy", box(-L / 2, L / 2, H - .03, H, ZH, ZFB))
    S.add("Wall_Rail", "gunmetal", blk(-L / 2, L / 2, 0, H - TOP, ZB, ZB + .03, .004, 1))
    S.add("Rail_Bolts", "alloy", *[cyl(x, ZB + .03, .01, y, y + .012, 6) for x in np.linspace(-L / 2 + .15, L / 2 - .15, int(L / .7) + 1) for y in (.15, H - .12)])
    S.add("Floor_Shoe", "gunmetal", box(-L / 2, L / 2, 0, .03, ZB, ZB + .06))
    S.add("Cantilever_Brackets", "gunmetal", *[box(x - .015, x + .015, H - .22, H - TOP, ZB + .03, ZH - .05) for x in np.linspace(-L / 2 + .2, L / 2 - .2, 5)])
    S.add("Bracket_Pins", "amber", *[cyl(x, ZH - .025, .012, H - .075, H - TOP, 8) for x in br_x(L)])
    S.add("End_Caps", "slate", *[box(s * L / 2 - (.01 if s > 0 else 0), s * L / 2 + (0 if s > 0 else .01), H - TOP - .002, H, ZB, ZH) for s in (-1, 1)])
    Lf = Pod("Leaf")   # local frame: origin on the hinge axis; stowed it hangs straight down
    Lf.add("Fold_Leaf", "white", blk(-L / 2 + .01, L / 2 - .01, -LEAF, -.004, -.015, .015, .006, 1))
    Lf.add("Hinge_Knuckle", "alloy", xcyl(-L / 2 + .01, L / 2 - .01, 0, 0, .015))
    Lf.add("Leaf_Edge_Strip", "alloy", box(-L / 2 + .01, L / 2 - .01, -LEAF - .006, -LEAF + .004, -.012, .012))
    Lf.add("Leaf_Pull_Latches", "amber", *[box(x - .04, x + .04, -LEAF - .022, -LEAF - .006, -.008, .008) for x in (-L / 4, L / 4)])
    B = []
    for i, x in enumerate(br_x(L)):   # local frame: origin on the pin; stowed the arm points +X under the worktop
        b = Pod(f"Swing_Bracket_{i + 1}"); b.add("Arm", "gunmetal", box(-.012, .4, -.025, 0, -.01, .01)); b.add("Arm_Pad", "slate", box(.33, .39, -.002, .006, -.008, .008))
        B.append((b, np.array([x, H - TOP - .002, ZH - .025])))
    return S, Lf, B
def qx(a): return np.array([np.sin(a / 2), 0, 0, np.cos(a / 2)])
def qy(a): return np.array([0, np.sin(a / 2), 0, np.cos(a / 2)])
def ease(t, t0, t1): u = np.clip((t - t0) / (t1 - t0), 0, 1); return u * u * (3 - 2 * u)
def pose(t, up):   # up=True: fold-up clip (leaf 0-1.2 s, brackets 1.2-2.0 s); False: reverse
    if up: a, b = ease(t, 0, 1.2), ease(t, 1.2, 2.0)
    else: a, b = 1 - ease(t, .8, 2.0), 1 - ease(t, 0, .8)
    return -np.pi / 2 * a, -np.pi / 2 * b
CLIPS = [("Leaf_Fold_Up", True, 2.0), ("Leaf_Fold_Down", False, 2.0)]
def world(S, Lf, B, a, b):
    """World-space Pod for sheets and checks at leaf angle a, bracket angle b."""
    W = Pod("World"); R = trimesh.transformations.rotation_matrix
    for k, (mk, m) in S.P.items(): W.add(k, mk, m.copy())
    T = trimesh.transformations.translation_matrix([0, YC, ZC]) @ R(a, [1, 0, 0])
    for k, (mk, m) in Lf.P.items(): mm = m.copy(); mm.apply_transform(T); W.add(k, mk, mm)
    for bp, piv in B:
        T = trimesh.transformations.translation_matrix(piv) @ R(b, [0, 1, 0])
        for k, (mk, m) in bp.P.items(): mm = m.copy(); mm.apply_transform(T); W.add("Swing_" + k, mk, mm)
    return W
def export_fold(S, Lf, B, path):
    from dining_chair_generator import shade_split, _col, FMAT
    from pygltflib import (GLTF2, Scene, Node, Mesh, Primitive, Attributes, Buffer, BufferView, Accessor, Material,
                           PbrMetallicRoughness, Animation, AnimationSampler, AnimationChannel, AnimationChannelTarget)
    g = GLTF2(); blob = bytearray(); mats = {}; tris = 0
    def add(arr, target, ctype, typ, mm=False):
        arr = np.ascontiguousarray(arr); off = len(blob); blob.extend(arr.tobytes())
        while len(blob) % 4: blob.append(0)
        g.bufferViews.append(BufferView(buffer=0, byteOffset=off, byteLength=arr.nbytes, target=target))
        acc = Accessor(bufferView=len(g.bufferViews) - 1, componentType=ctype, count=len(arr), type=typ)
        if mm: a2 = arr.reshape(len(arr), -1); acc.min = a2.min(0).tolist(); acc.max = a2.max(0).tolist()
        g.accessors.append(acc); return len(g.accessors) - 1
    def node(pod, T):
        nonlocal tris; bym = {}
        for k, (mk, m) in pod.P.items(): bym.setdefault(mk, []).append(shade_split(m))
        prims = []
        for mk, lst in bym.items():
            if mk not in mats:
                pm = FMAT[mk]; mats[mk] = len(g.materials)
                g.materials.append(Material(name=pm.name, emissiveFactor=_col(pm.emissiveFactor if pm.emissiveFactor is not None else [0, 0, 0]),
                    pbrMetallicRoughness=PbrMetallicRoughness(baseColorFactor=_col(pm.baseColorFactor), metallicFactor=float(pm.metallicFactor), roughnessFactor=float(pm.roughnessFactor))))
            o = 0; V, N, U, F = [], [], [], []
            for v, n, u, f in lst: V.append(v); N.append(n); U.append(u); F.append(f + o); o += len(v)
            V, N, U, F = map(np.vstack, (V, N, U, F)); tris += len(F)
            a = Attributes(POSITION=add(V.astype(np.float32), 34962, 5126, "VEC3", True), NORMAL=add(N.astype(np.float32), 34962, 5126, "VEC3"), TEXCOORD_0=add(U.astype(np.float32), 34962, 5126, "VEC2"))
            prims.append(Primitive(attributes=a, indices=add(F.astype(np.uint32).ravel(), 34963, 5125, "SCALAR"), material=mats[mk]))
        g.meshes.append(Mesh(name=pod.name, primitives=prims)); g.nodes.append(Node(name=pod.name, mesh=len(g.meshes) - 1, translation=[float(c) for c in T])); return len(g.nodes) - 1
    root = node(S, [0, 0, 0]); leaf = node(Lf, [0, YC, ZC]); brs = [node(b, piv) for b, piv in B]
    g.nodes[root].children = [leaf] + brs; g.scenes = [Scene(name="FoldingCounter", nodes=[root])]; g.scene = 0
    for name, up, dur in CLIPS:
        ts = np.round(np.arange(0, dur + 1e-6, 1 / FPS), 5).astype(np.float32); P = [pose(float(t), up) for t in ts]
        an = Animation(name=name, samplers=[], channels=[]); tin = add(ts, None, 5126, "SCALAR", True)
        for nid, q in [(leaf, np.array([qx(p[0]) for p in P]))] + [(n, np.array([qy(p[1]) for p in P])) for n in brs]:
            an.samplers.append(AnimationSampler(input=tin, output=add(q.astype(np.float32), None, 5126, "VEC4"), interpolation="LINEAR"))
            an.channels.append(AnimationChannel(sampler=len(an.samplers) - 1, target=AnimationChannelTarget(node=nid, path="rotation")))
        g.animations.append(an)
    g.buffers = [Buffer(byteLength=len(blob))]; g.set_binary_blob(bytes(blob)); g.save_binary(path); return tris
def final_main():
    import pygltflib
    for L, tag in ((3.5, "3p5"), (3.0, "3p0")):
        S, Lf, B = final_fold(L); gp = os.path.join(dc.ROOT, f"godot/assets/models/folding_counter_fold_leaf_{tag}.glb"); tris = export_fold(S, Lf, B, gp)
        bad = [k for pod in [S, Lf] + [b for b, _ in B] for k, (mk, m) in pod.P.items() if not all(c.is_watertight for c in m.split(only_watertight=False))]
        for st, (a, b) in (("stowed", (0, 0)), ("deployed", (-np.pi / 2, -np.pi / 2))):
            W = world(S, Lf, B, a, b); V = np.vstack([m.vertices for mk, m in W.P.values()])
            print(tag, st, "size", (V.max(0) - V.min(0)).round(3), "min", V.min(0).round(3), "max", V.max(0).round(3))
            if tag == "3p5" or st == "stowed":
                sp = os.path.join(OUT, f"final_fold_leaf_{tag}_{st}_sheet.png"); wg.sheet(W, sp, f"Final  #38 folding counter, Fold-Down Leaf, {L} m run, {st}"); os.remove(sp.replace("_sheet.png", ".glb"))
        # leaf vs bracket clearance during the swing: sample bracket arm tips vs raised-leaf underside
        g = pygltflib.GLTF2().load(gp); print(tag, "tris", tris, "nodes", [n.name for n in g.nodes], "anims", [(an.name, len(an.channels)) for an in g.animations], "bad", bad)
if __name__ == "__main__": final_main() if len(sys.argv) > 1 and sys.argv[1] == "final" else main()
