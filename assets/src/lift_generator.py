"""Rev C asset #51: Sprocket bot lift (stair core v1.1 lift option 1, SW stack). Building plan origin like #3-#7
(X axial, Y up from L1 finished floor, +Z spinward). Shaft X 0.6..2.2, Z 0.8..2.4, Y -0.15 (pit) .. 6.6 (cap); car 1.2 x 1.2 x 1.4
at X 0.8..2.0, Z 1.0..2.2; landing doors 1.0 x 1.3 at X 0.9..1.9 in the south (corridor) wall Z 0.8..0.9 on L1 (Y 0) and L2 (Y 4.2);
call panels on the west jamb (X 0.45..0.85, corridor face); MRL rack drive + controller cabinet in the 202 slot X 0.1..0.6 (L2)."""
import os, sys, inspect, numpy as np, trimesh
sys.path.insert(0, os.path.dirname(__file__))
import service_wall_generator as sw
import dining_chair_generator as dc
from dining_chair_generator import xf, FMAT, render_view
from bath_pod_generator import cyl, views
from kitchen_counter_generator import bev, box, crop, tonemap
from service_wall_generator import rest, ss, _rot, QI, world_geo
OUT = os.path.join(dc.ROOT, "design/assets/lift")
SX0, SX1, SZ0, SZ1 = .6, 2.2, .8, 2.4; WT = .1; PIT = -.15; CAP = 6.6; L2 = 4.2; SLAB = (3.9, 4.2)
CX0, CX1, CZ0, CZ1, CH = .8, 2.0, 1.0, 2.2, 1.4; DX0, DX1, DH = .9, 1.9, 1.3
CARP = np.array([1.4, 0, 1.6]); SP_DOCK = np.array([1.4, 0, 1.75]); SP_OUT = np.array([1.4, 0, -.02])
PW = .25; TRK = {"W1": .839, "W2": .861, "E1": .839, "E2": .861}          # telescoping 2-speed panels in the wall cavity
DOPEN = {"W1": -.5, "W2": -.25, "E1": .5, "E2": .25}; CLAMP_IN = .11

def nodes():
    N = {}
    def node(n, T, parent=None, Wp=None): N[n] = dict(parent=parent, T=np.array(T, float), parts={}, W=np.array(Wp if Wp is not None else T, float)); return N[n]
    def put(nd, part, mk, *ms):
        m = ms[0] if len(ms) == 1 else dc.merge(list(ms)); m = xf(m, t=tuple(-nd["W"]))
        if part in nd["parts"]: m = dc.merge([nd["parts"][part][1], m])
        nd["parts"][part] = (mk, m)
    s = node("Shaft_Static", (0, 0, 0))
    put(s, "Shaft_Wall_W", "white", box(SX0, SX0 + WT, PIT, CAP, SZ0 + WT, SZ1)); put(s, "Shaft_Wall_E", "white", box(SX1 - WT, SX1, PIT, CAP, SZ0 + WT, SZ1))
    put(s, "Shaft_Wall_N", "white", box(SX0 + WT, SX1 - WT, PIT, CAP, SZ1 - WT, SZ1))
    sw_ = []                                                     # south wall: two skins (cavity Z .825..0.875 for the door stacks), door openings
    for z0, z1 in ((SZ0, .825), (.875, SZ0 + WT)):
        ys = [PIT, 0, DH, L2, L2 + DH, CAP]
        for a, b in ((ys[0], ys[1]), (ys[2], ys[3]), (ys[4], ys[5])): sw_.append(box(SX0, SX1, a, b, z0, z1))
        for y in (0, L2): sw_ += [box(SX0, DX0, y, y + DH, z0, z1), box(DX1, SX1, y, y + DH, z0, z1)]
    put(s, "Shaft_Wall_S", "white", *sw_)
    put(s, "Door_Jambs", "gunmetal", *[box(DX0 - .02, DX0, y, y + DH, SZ0 - .01, SZ0) for y in (0, L2)], *[box(DX1, DX1 + .02, y, y + DH, SZ0 - .01, SZ0) for y in (0, L2)],
        *[box(DX0 - .02, DX1 + .02, y + DH, y + DH + .02, SZ0 - .01, SZ0) for y in (0, L2)])
    put(s, "Shaft_Wall_S", "white", box(SX0, SX0 + .02, PIT, CAP, .825, .875), box(SX1 - .02, SX1, PIT, CAP, .825, .875))
    put(s, "Pit_Floor", "gunmetal", box(SX0 + WT, SX1 - WT, PIT, PIT + .03, SZ0 + WT, SZ1 - WT)); put(s, "Shaft_Cap", "gunmetal", box(SX0, SX1, CAP - .1, CAP, SZ0, SZ1))
    put(s, "Fire_Separation", "gunmetal", box(SX0 - .02, SX0, *SLAB, SZ0, SZ1), box(SX1, SX1 + .02, *SLAB, SZ0, SZ1), box(SX0, SX1, *SLAB, SZ0 - .02, SZ0))
    put(s, "Sills", "alloy", *[box(DX0, DX1, y - .01, y, SZ0 - .03, SZ0 + WT) for y in (0, L2)])
    put(s, "Guide_Rails", "alloy", box(.7, .74, PIT + .03, CAP - .1, 1.58, 1.62), box(2.06, 2.1, PIT + .03, CAP - .1, 1.58, 1.62))
    put(s, "Drive_Rack", "gunmetal", box(2.06, 2.1, PIT + .03, CAP - .1, 1.7, 1.74))
    put(s, "Controller_Cabinet", "gunmetal", bev(.4, 1.3, L2 + .05, L2 + 2.0, .02, .006, 2, .35, 1.65))
    put(s, "Controller_Status", "green", box(.54, .552, L2 + 1.7, L2 + 1.76, 1.5, 1.8))
    for y, lv in ((0, "L1"), (L2, "L2")):
        put(s, "Call_Panels", "gunmetal", bev(.4, .02, y + .9, y + 1.4, .02, .006, 2, .65, SZ0 - .01))
        put(s, "Call_Panel_Glyph", "amber", box(.6, .7, y + 1.1, y + 1.22, SZ0 - .024, SZ0 - .02))
        put(s, "Status_Green", "green", box(1.25, 1.35, y + DH + .05, y + DH + .09, SZ0 - .012, SZ0))
        put(s, "Status_Amber", "amber", box(1.45, 1.55, y + DH + .05, y + DH + .09, SZ0 - .012, SZ0))
    # landing doors (each panel a node; pivot at panel centre)
    order = {"W2": DX0, "W1": DX0 + PW, "E1": DX0 + 2 * PW, "E2": DX0 + 3 * PW}
    for y, lv in ((0, "L1"), (L2, "L2")):
        for k, x0 in order.items():
            c = (x0 + PW / 2, y + DH / 2, TRK[k]); d = node(f"Door_{lv}_{k}", c)
            put(d, "Door_Panel", "gunmetal", box(x0, x0 + PW, y + .005, y + DH - .005, TRK[k] - .01, TRK[k] + .01))
            put(d, "Door_Latch", "amber", box(x0 + PW / 2 - .02, x0 + PW / 2 + .02, y + .62, y + .7, TRK[k] - .013, TRK[k] - .01) if k in ("W1", "E1") else
                box(x0 + .1, x0 + .15, y + 1.2, y + 1.23, TRK[k] - .013, TRK[k] - .01))
    # car (pivot: car floor top centre) + children
    c = node("Lift_Car", CARP)
    put(c, "Car_Floor", "gunmetal", box(CX0, CX1, -.08, 0, CZ0, CZ1)); put(c, "Car_Roof", "gunmetal", box(CX0, CX1, CH, CH + .05, CZ0, CZ1))
    put(c, "Car_Walls", "white", box(CX0, CX0 + .03, 0, CH, CZ0, CZ1), box(CX1 - .03, CX1, 0, CH, CZ0, CZ1), box(CX0 + .03, CX1 - .03, 0, CH, CZ1 - .03, CZ1))
    put(c, "Dock_Pad", "amber", box(1.0, 1.8, 0, .006, 1.3, 2.1))
    put(c, "Charge_Contact", "gunmetal", bev(.14, .02, .38, .52, .02, .005, 1, 1.4, CZ1 - .04)); put(c, "Charge_Contact_Pin", "amber", box(1.37, 1.43, .43, .47, CZ1 - .065, CZ1 - .05))
    put(c, "Rear_Bumper", "slatefab", box(1.05, 1.75, .08, .3, CZ1 - .05, CZ1 - .03))
    put(c, "Guide_Shoes", "alloy", box(.744, CX0, .1, .3, 1.55, 1.65), box(.744, CX0, 1.1, 1.3, 1.55, 1.65), box(CX1, 2.056, .1, .3, 1.55, 1.65), box(CX1, 2.056, 1.1, 1.3, 1.55, 1.65))
    put(c, "Drive_Pinion", "gunmetal", box(CX1, 2.056, .5, .72, 1.68, 1.76)); put(c, "Car_Light", "violet", box(1.1, 1.7, CH - .01, CH, 1.3, 1.9))
    for k, x0 in (("W", CX0 + .03), ("E", CX1 - .03 - .1)):
        cl = node(f"Car_Clamp_{k}", (x0 + .05, .24, 1.75), "Lift_Car", Wp=(x0 + .05, .24, 1.75)); cl["T"] = cl["W"] - CARP
        put(cl, "Clamp_Jaw", "gunmetal", box(x0, x0 + .1, .18, .3, 1.65, 1.85)); put(cl, "Clamp_Latch", "amber", box(x0 + .03, x0 + .07, .3, .306, 1.715, 1.785))
    # stand-in (top level; built like the service-wall one, yawed 180 deg so its back port meets the car's charge contact)
    sp = node("Sprocket_Standin", SP_DOCK - CARP, "Lift_Car", Wp=SP_DOCK)
    R180 = trimesh.transformations.rotation_matrix(np.pi, [0, 1, 0], point=SP_DOCK)
    x0, z0 = SP_DOCK[0], SP_DOCK[2]
    parts = [("Standin_Chassis", "gunmetal", bev(.7, .7, .08, .32, .05, .015, 2, x0, z0)),
             ("Standin_Wheels", "slatefab", dc.merge([xf(sw.loft_x(.075, .05), t=(x0 + a * .36, .09, z0 + b * .24)) for a in (-1, 1) for b in (-1, 1)])),
             ("Standin_Torso", "white", bev(.6, .55, .32, .84, .08, .02, 3, x0, z0 + .02)), ("Standin_Head", "white", bev(.42, .3, .86, 1.03, .06, .015, 3, x0, z0 + .1)),
             ("Standin_Neck", "alloy", cyl(x0, z0 + .05, .04, .84, .87, 10)),
             ("Standin_Eyes", "slate", dc.merge([xf(sw.zdisc(0, .93, 0, .03, .045, 12), t=(x0 + dx, 0, z0 + .25)) for dx in (-.1, .1)])),
             ("Standin_Back_Port", "amber", box(x0 - .03, x0 + .03, .43, .47, z0 - .385, z0 - .375)),
             ("Standin_Back_Plate", "gunmetal", bev(.14, .02, .38, .52, .02, .005, 1, x0, z0 - .375 + .01))]
    for n, mk, m in parts: put(sp, n, mk, xf(m, R180))
    return N

# ---------------- clips ----------------
def doors(lv, u, N):  # u: 0 closed .. 1 open
    return {f"Door_{lv}_{k}": (N[f"Door_{lv}_{k}"]["T"] + [DOPEN[k] * u, 0, 0], QI, np.ones(3)) for k in DOPEN}
SP_LOC = SP_DOCK - CARP; EXIT_Z = -.1      # stand-in is a child of Lift_Car (local z); exits to world Z -0.1 on the landing
def car(y, N, clamp_u, spz_world=None):
    o = {"Lift_Car": (CARP + [0, y, 0], QI, np.ones(3))}
    for k, s_ in (("W", 1), ("E", -1)): o[f"Car_Clamp_{k}"] = (N[f"Car_Clamp_{k}"]["T"] + [s_ * CLAMP_IN * clamp_u, 0, 0], QI, np.ones(3))
    z = SP_DOCK[2] if spz_world is None else spz_world
    o["Sprocket_Standin"] = (np.array([0, 0, z - CARP[2]]), QI, np.ones(3)); return o
def lerp(a, b, u): return a + (b - a) * u
def st(lv1, lv2, y, cl, spz=None): o = doors("L1", lv1, N_); o.update(doors("L2", lv2, N_)); o.update(car(y, N_, cl, spz)); return o
# clip timings (s)
def clip_call(t, N):   return st(ss(t, .3, 1.7), 0, 0, 0)
def clip_board(t, N):  return st(1, 0, 0, ss(t, 2.7, 3.3), lerp(EXIT_Z, SP_DOCK[2], ss(t, .2, 2.6)))
def clip_up(t, N):     return st(1 - ss(t, 0, 1.5), 0, L2 * ss(t, 2.6, 6.0), ss(t, 1.7, 2.3))
def clip_arr2(t, N):   return st(0, ss(t, .2, 1.8), L2, 1)
def clip_exit2(t, N):  return st(0, 1, L2, 1 - ss(t, 0, .6), lerp(SP_DOCK[2], EXIT_Z, ss(t, .8, 3.2)))
def clip_down(t, N):   return st(0, 1 - ss(t, 0, 1.5), L2 * (1 - ss(t, 2.6, 6.0)), ss(t, 1.7, 2.3))
def clip_arr1(t, N):   return st(ss(t, .2, 1.8), 0, 0, 1)
def clip_exit1(t, N):  return st(1, 0, 0, 1 - ss(t, 0, .6), lerp(SP_DOCK[2], EXIT_Z, ss(t, .8, 3.2)))
def clip_idle(t, N):   return st(0, 0, 0, 0)
CLIPS = [("call_open_L1", clip_call, 2.0), ("sprocket_board", clip_board, 3.5), ("ride_up", clip_up, 6.5), ("arrive_open_L2", clip_arr2, 2.0),
         ("sprocket_exit_L2", clip_exit2, 3.5), ("ride_down", clip_down, 6.5), ("arrive_open_L1", clip_arr1, 2.0), ("sprocket_exit_L1", clip_exit1, 3.5), ("idle", clip_idle, 2.0)]
N_ = None

def exporter():
    src = inspect.getsource(sw.export_anim_glb).replace("if np.allclose(vals, vals[0]) and np.allclose(vals[0], R0[n][k]): continue",
        "if np.allclose(vals, vals[0]) and np.allclose(vals[0], R0[n][k]) and not (cname == 'idle' and k == 0 and n == 'Lift_Car'): continue")
    ns = dict(sw.__dict__); ns["CLIPS"] = CLIPS; exec(src, ns); return ns["export_anim_glb"]

# ---------- glb-driven sampler + real clash check ----------
def glb_poses(gp):
    """Reload the glb; return {clip: (times, {node: {path: values}})} sampled straight from the accessors."""
    import pygltflib
    g = pygltflib.GLTF2().load(gp); blob = g.binary_blob()
    def acc(i):
        a = g.accessors[i]; bv = g.bufferViews[a.bufferView]; n = {"SCALAR": 1, "VEC3": 3, "VEC4": 4}[a.type]
        return np.frombuffer(blob, np.float32, a.count * n, bv.byteOffset + (a.byteOffset or 0)).reshape(a.count, n)
    out = {}
    for an in g.animations:
        ch = {}; ts = None
        for c in an.channels:
            smp = an.samplers[c.sampler]; ts = acc(smp.input)[:, 0]; ch.setdefault(g.nodes[c.target.node].name, {})[c.target.path] = acc(smp.output)
        out[an.name] = (ts, ch)
    return g, out
def pose_from_glb(N, ch, i):
    P = rest(N)
    for n, d in ch.items():
        T, R, S = P[n]
        if "translation" in d: T = d["translation"][i].astype(float)
        if "rotation" in d: R = d["rotation"][i].astype(float)
        if "scale" in d: S = d["scale"][i].astype(float)
        P[n] = (T, R, S)
    return P
def comps(G, pred):
    out = []
    for k, (mk, V, Nn, F) in G.items():
        if not pred(k): continue
        m = trimesh.Trimesh(V, F, process=True)
        for c in m.split(only_watertight=False): out.append((k, c.bounds[0], c.bounds[1]))
    return out
def gap(a, b):   # AABB separation (negative = penetration depth along the least-overlap axis)
    d = np.maximum(a[1] - b[2], b[1] - a[2]); return float(d.max())
CAR_P = lambda k: k.startswith(("Lift_Car/", "Car_Clamp_", "Sprocket_Standin/"))
def clash_table(N, gp):
    g, clips = glb_poses(gp); best = {}; frames = 0
    stat0 = None
    for cname, (ts, ch) in clips.items():
        for i in range(len(ts)):
            P = pose_from_glb(N, ch, i); G = world_geo(N, P); frames += 1
            if stat0 is None: stat0 = comps(G, lambda k: k.startswith("Shaft_Static/"))
            car = comps(G, CAR_P); drs = comps(G, lambda k: k.startswith("Door_"))
            cr = [c for c in car if not c[0].startswith("Sprocket_Standin/")]; sp = [c for c in car if c[0].startswith("Sprocket_Standin/")]
            def upd(key, A, B, allow=()):
                m = min(gap(a, b) for a in A for b in B) if A and B else 9
                if key not in best or m < best[key][0]: best[key] = (round(m, 4), cname, round(float(ts[i]), 3))
            for part in sorted({c[0] for c in stat0}):
                upd(("car+clamps", part.split("/")[1]), cr, [c for c in stat0 if c[0] == part])
                upd(("standin", part.split("/")[1]), [c for c in sp], [c for c in stat0 if c[0] == part])
            for dn in sorted({c[0].split("/")[0] for c in drs}):
                upd(("car+clamps", dn), cr, [c for c in drs if c[0].startswith(dn)])
                ins = sp[0][1][2] > CZ0 - .01 if sp else True
                upd(("standin", dn), sp, [c for c in drs if c[0].startswith(dn)])
            # stand-in vs car (charge pin contact allowed at 0.000)
            upd(("standin", "car body"), sp, [c for c in cr if "Charge_Contact_Pin" not in c[0] and "Dock_Pad" not in c[0]])
            upd(("standin", "charge pin (contact)"), sp, [c for c in cr if "Charge_Contact_Pin" in c[0]])
    return frames, best, [a.name for a in g.animations]

def main():
    global N_
    import pygltflib
    from PIL import Image, ImageDraw, ImageFont
    os.makedirs(OUT, exist_ok=True); N = nodes(); N_ = N; gp = os.path.join(dc.ROOT, "godot/assets/models/sprocket_lift.glb")
    tris = exporter()(N, gp)
    stt = tris["Shaft_Static"]; spt = tris["Sprocket_Standin"]; mv = sum(tris.values()) - stt - spt
    print("tris static", stt, "moving", mv, "standin", spt, "total", sum(tris.values()))
    bad = [f"{n}/{p}" for n, nd in N.items() for p, (mk, m) in nd["parts"].items() if not all(c.is_watertight for c in m.split(only_watertight=False))]
    print("non-watertight", bad)
    g = pygltflib.GLTF2().load(gp)
    print("nodes", [(n.name, [g.nodes[c].name for c in n.children]) for n in g.nodes])
    print("anims", [(a.name, len(a.channels), round(float(g.accessors[a.samplers[0].input].max[0]), 2)) for a in g.animations])
    frames, best, names = clash_table(N, gp); print("frames sampled", frames)
    fails = {k: v for k, v in best.items() if v[0] < -1e-4 and not (k[1].startswith("Standin_Back") or "pin" in k[1])}
    for k, v in sorted(best.items(), key=lambda kv: kv[1][0]): print("CLR", k, v)
    print("FAILS", fails)
    import json; json.dump({f"{a} | {b}": v for (a, b), v in best.items()}, open("/tmp/lift_clearance.json", "w"), indent=0)
    # ----- renders -----
    saved = tonemap(); top, front, side, iso = views(); a = np.pi; Ry = np.array([[np.cos(a), 0, np.sin(a)], [0, 1, 0], [-np.sin(a), 0, np.cos(a)]])
    def rv(G, R, s, sh=True):
        im = render_view(G, R, size=s, shadow=sh); ns = render_view(G, R, size=s, shadow=False) if sh else im
        fg = np.abs(ns - ns[0, 0]).sum(2) > .03; im[fg] = np.clip(im[fg] * 1.12 + .02, 0, 1); return crop(im)
    G0 = world_geo(N, rest(N), skip=("Sprocket_Standin",))
    FRONT = ("Shaft_Static/Shaft_Wall_S", "Shaft_Static/Shaft_Wall_E", "Shaft_Static/Door_Jambs", "Shaft_Static/Call_Panel", "Shaft_Static/Status_", "Shaft_Static/Sills", "Shaft_Static/Fire_Separation")
    def cut(G): return {k: v for k, v in G.items() if not k.startswith(FRONT)}
    def ghost(G):   # doors as tinted glass so they read but never hide the car
        return {k: (("glass",) + v[1:]) if k.startswith("Door_") else v for k, v in G.items()}
    from bath_pod_generator import render_glass
    ims = [rv(G0, top, 500, False), rv(G0, front @ Ry, 650), rv(G0, side, 650), rv(G0, iso @ Ry, 700), crop(render_glass(ghost(cut(world_geo(N, rest(N)))), iso @ Ry, 700, True))]
    import matplotlib.pyplot as plt
    bg = "#F4F2EC"; fig, axs = plt.subplots(1, 5, figsize=(20, 8), facecolor=bg)
    for ax, im, t in zip(axs, ims, ("Top", "Front (corridor face)", "Side", "Iso", "Iso cutaway (front + east walls hidden, doors ghosted), Sprocket docked")):
        ax.imshow(im); ax.axis("off"); ax.set_title(t, fontsize=10, color="#555")
    fig.suptitle("Final  #51 Sprocket bot lift (v1.1 option 1, SW stack)", fontsize=12, color="#444"); plt.tight_layout(rect=(0, 0, 1, .94))
    fig.savefig(os.path.join(OUT, "final_lift_sheet.png"), dpi=90, facecolor=bg); plt.close(fig)
    _, clips = glb_poses(gp)
    fr = [("call_open_L1", 0), ("call_open_L1", 2.0), ("sprocket_board", 1.4), ("sprocket_board", 3.5), ("ride_up", .8), ("ride_up", 1.6), ("ride_up", 2.4),
          ("ride_up", 4.3), ("ride_up", 6.5), ("arrive_open_L2", 2.0), ("sprocket_exit_L2", 2.0), ("sprocket_exit_L2", 3.5),
          ("ride_down", 4.3), ("arrive_open_L1", 2.0), ("sprocket_exit_L1", 3.5), ("idle", 0)]
    def anchor(G):  # zero-area (collinear) framing triangle: fixes the camera across frames, draws nothing
        p0, p1 = np.array([SX0 - .1, PIT, EXIT_Z - .45]), np.array([SX1 + .1, CAP, SZ1])
        G["_anchor"] = ("gunmetal", np.array([p0, p1, (p0 + p1) / 2]), np.array([[0, 0, 1.]] * 3), np.array([[0, 1, 2]])); return G
    def frame(c, t, big):
        ts, ch = clips[c]; i = int(np.argmin(np.abs(ts - t))); P = pose_from_glb(N, ch, i); G = world_geo(N, P)
        if big: return render_glass(anchor(ghost(cut(G))), iso @ Ry, 900, True)
        return render_view(anchor(G), iso @ Ry, size=320, shadow=True)
    for big, name, cols, fs in ((False, "final_lift_sequence", 8, 13), (True, "final_lift_cutaway_sequence", 4, 20)):
        font = ImageFont.truetype("DejaVuSans.ttf", fs); tiles = []
        for c, t in fr:
            im = frame(c, t, big); tiles.append((f"{c} t={t:.1f}s", Image.fromarray((np.clip(im, 0, 1) * 255).astype(np.uint8))))
        tw, th = tiles[0][1].size; rows = (len(tiles) + cols - 1) // cols; S = Image.new("RGB", (cols * tw, rows * (th + fs + 12)), (244, 242, 236)); d = ImageDraw.Draw(S)
        for k, (lab, im) in enumerate(tiles):
            x, y = (k % cols) * tw, (k // cols) * (th + fs + 12); S.paste(im, (x, y + fs + 12)); d.text((x + 8, y + 4), f"{k + 1}. {lab}", fill=(60, 60, 60), font=font)
        S.save(os.path.join(OUT, name + ".png"))
        gif = []
        for lab, im in tiles:
            im = im.copy(); ImageDraw.Draw(im).text((8, 6), lab, fill=(60, 60, 60), font=font); gif.append(im)
        gif[0].save(os.path.join(OUT, name + ".gif"), save_all=True, append_images=gif[1:], duration=700, loop=0)
    FMAT.update(saved)
if __name__ == "__main__": main()
