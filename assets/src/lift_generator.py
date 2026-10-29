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
    put(c, "Guide_Shoes", "alloy", box(.74, CX0, .1, .3, 1.55, 1.65), box(.74, CX0, 1.1, 1.3, 1.55, 1.65), box(CX1, 2.06, .1, .3, 1.55, 1.65), box(CX1, 2.06, 1.1, 1.3, 1.55, 1.65))
    put(c, "Drive_Pinion", "gunmetal", box(CX1, 2.06, .5, .72, 1.68, 1.76)); put(c, "Car_Light", "violet", box(1.1, 1.7, CH - .01, CH, 1.3, 1.9))
    for k, x0 in (("W", CX0 + .03), ("E", CX1 - .03 - .1)):
        cl = node(f"Car_Clamp_{k}", (x0 + .05, .24, 1.75), "Lift_Car", Wp=(x0 + .05, .24, 1.75)); cl["T"] = cl["W"] - CARP
        put(cl, "Clamp_Jaw", "gunmetal", box(x0, x0 + .1, .18, .3, 1.65, 1.85)); put(cl, "Clamp_Latch", "amber", box(x0 + .03, x0 + .07, .3, .306, 1.715, 1.785))
    # stand-in (top level; built like the service-wall one, yawed 180 deg so its back port meets the car's charge contact)
    sp = node("Sprocket_Standin", SP_DOCK)
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
def car(y, N, clamp_u, sp_on=True, spz=None):
    o = {"Lift_Car": (CARP + [0, y, 0], QI, np.ones(3))}
    for k, s in (("W", 1), ("E", -1)): o[f"Car_Clamp_{k}"] = (N[f"Car_Clamp_{k}"]["T"] + [s * CLAMP_IN * clamp_u, 0, 0], QI, np.ones(3))
    o["Sprocket_Standin"] = (np.array([SP_DOCK[0], y, SP_DOCK[2] if spz is None else spz]), QI, np.ones(3)); return o
def clip_call(t, N): o = doors("L1", ss(t, .3, 1.7), N); o.update(car(0, N, 0)); o.update(doors("L2", 0, N)); return o
def clip_board(t, N):
    o = doors("L1", 1, N); z = SP_OUT[2] + (SP_DOCK[2] - SP_OUT[2]) * ss(t, .2, 2.6); o.update(car(0, N, ss(t, 2.7, 3.3), spz=z)); return o
def clip_up(t, N):
    o = doors("L1", 1 - ss(t, 0, 1.2), N); o.update(doors("L2", ss(t, 5.1, 6.5), N)); o.update(car(L2 * ss(t, 1.8, 5.0), N, ss(t, 1.2, 1.7))); return o
def clip_down(t, N):
    o = doors("L2", 1 - ss(t, 0, 1.2), N); o.update(doors("L1", ss(t, 5.1, 6.5), N)); o.update(car(L2 * (1 - ss(t, 1.8, 5.0)), N, 1 - ss(t, 4.6, 5.0))); return o
def clip_idle(t, N): o = doors("L1", 0, N); o.update(doors("L2", 0, N)); o.update(car(0, N, 0)); return o
CLIPS = [("call_open_L1", clip_call, 2.0), ("sprocket_board", clip_board, 3.5), ("ride_up", clip_up, 6.5), ("ride_down", clip_down, 6.5), ("idle", clip_idle, 2.0)]

def exporter():
    src = inspect.getsource(sw.export_anim_glb).replace("if np.allclose(vals, vals[0]) and np.allclose(vals[0], R0[n][k]): continue",
        "if np.allclose(vals, vals[0]) and np.allclose(vals[0], R0[n][k]) and not (cname == 'idle' and k == 0 and n == 'Lift_Car'): continue")
    ns = dict(sw.__dict__); ns["CLIPS"] = CLIPS; exec(src, ns); return ns["export_anim_glb"]

def bounds(G, pre):
    V = [v for k, (mk, v, n, f) in G.items() if k.startswith(pre)]; V = np.vstack(V); return V.min(0), V.max(0)
def checks(N):
    worst = dict(car_vs_shaft=9.0, standin_vs_car=9.0, car_vs_riser=9.0); door_ok = True
    for cname, fn, dur in CLIPS:
        for t in np.arange(0, dur + 1e-6, 1 / 15):
            P = rest(N); P.update(fn(t, N)); G = world_geo(N, P)
            lo, hi = bounds({k: v for k, v in G.items() if k.startswith(("Lift_Car", "Car_Clamp"))}, "")
            worst["car_vs_shaft"] = min(worst["car_vs_shaft"], lo[0] - (SX0 + WT), (SX1 - WT) - hi[0], lo[2] - (.875), (SZ1 - WT) - hi[2], lo[1] - (PIT + .03), (CAP - .1) - hi[1])
            worst["car_vs_riser"] = min(worst["car_vs_riser"], 2.4 - hi[2])
            slo, shi = bounds(G, "Sprocket_Standin")
            if slo[2] > CZ0:   # fully inside the car
                cy = P["Lift_Car"][0][1]; clo, chi = bounds(G, "Sprocket_Standin/Standin_Chassis")
                worst["standin_vs_car"] = min(worst["standin_vs_car"], clo[0] - (CX0 + .03 + .1 + CLAMP_IN * P["Car_Clamp_W"][0][0].__sub__(N["Car_Clamp_W"]["T"][0]) / CLAMP_IN), (CX1 - .03 - .1 - (N["Car_Clamp_E"]["T"][0] - P["Car_Clamp_E"][0][0])) - chi[0], (CZ1 - .065) - shi[2], (cy + CH) - shi[1])
            for lv in ("L1", "L2"):
                dl, dh = bounds(G, f"Door_{lv}_"); door_ok &= dl[0] >= SX0 + .02 - 1e-6 and dh[0] <= SX1 - .02 + 1e-6 and dl[2] >= .825 - 1e-6 and dh[2] <= .875 + 1e-6
    worst = {k: round(float(v), 3) for k, v in worst.items()}; worst["doors_inside_wall_cavity"] = bool(door_ok); return worst

def main():
    import pygltflib
    from PIL import Image, ImageDraw, ImageFont
    os.makedirs(OUT, exist_ok=True); N = nodes(); gp = os.path.join(dc.ROOT, "godot/assets/models/sprocket_lift.glb")
    tris = exporter()(N, gp)
    st = tris["Shaft_Static"]; sp = tris["Sprocket_Standin"]; mv = sum(tris.values()) - st - sp
    print("tris static", st, "moving", mv, "standin", sp, "total", sum(tris.values()))
    bad = [f"{n}/{p}" for n, nd in N.items() for p, (mk, m) in nd["parts"].items() if not all(c.is_watertight for c in m.split(only_watertight=False))]
    print("non-watertight", bad); print("checks", checks(N))
    g = pygltflib.GLTF2().load(gp); print("nodes", [n.name for n in g.nodes])
    print("anims", [(a.name, len(a.channels), round(float(g.accessors[a.samplers[0].input].max[0]), 2)) for a in g.animations])
    saved = tonemap(); top, front, side, iso = views(); a = np.pi; Ry = np.array([[np.cos(a), 0, np.sin(a)], [0, 1, 0], [-np.sin(a), 0, np.cos(a)]])
    def rv(G, R, s, sh=True):
        im = render_view(G, R, size=s, shadow=sh); ns = render_view(G, R, size=s, shadow=False) if sh else im
        fg = np.abs(ns - ns[0, 0]).sum(2) > .03; im[fg] = np.clip(im[fg] * 1.12 + .02, 0, 1); return crop(im)
    G0 = world_geo(N, rest(N), skip=("Sprocket_Standin",))
    cut = lambda G: {k: v for k, v in G.items() if not k.startswith("Shaft_Static/Shaft_Wall_") or k.endswith("_W") or k.endswith("_N")}
    ims = [rv(G0, top, 500, False), rv(G0, front @ Ry, 650), rv(G0, side, 650), rv(G0, iso @ Ry, 700), rv(cut(world_geo(N, rest(N))), iso @ Ry, 700)]
    import matplotlib.pyplot as plt
    bg = "#F4F2EC"; fig, axs = plt.subplots(1, 5, figsize=(20, 8), facecolor=bg)
    for ax, im, t in zip(axs, ims, ("Top", "Front (corridor face)", "Side", "Iso", "Iso cutaway (S + E walls hidden), Sprocket docked")):
        ax.imshow(im); ax.axis("off"); ax.set_title(t, fontsize=10, color="#555")
    fig.suptitle("Final  #51 Sprocket bot lift (v1.1 option 1, SW stack)", fontsize=12, color="#444"); plt.tight_layout(rect=(0, 0, 1, .94))
    fig.savefig(os.path.join(OUT, "final_lift_sheet.png"), dpi=90, facecolor=bg); plt.close(fig)
    fr = [("call_open_L1", 0), ("call_open_L1", 2.0), ("sprocket_board", 1.2), ("sprocket_board", 3.5), ("ride_up", 1.0), ("ride_up", 2.6),
          ("ride_up", 4.0), ("ride_up", 6.5), ("ride_down", 1.2), ("ride_down", 3.4), ("ride_down", 6.5), ("idle", 0)]
    fn = {c: f for c, f, d in CLIPS}; font = ImageFont.truetype("DejaVuSans.ttf", 16); tiles = []
    Rv = iso @ Ry
    for c, t in fr:
        P = rest(N); P.update(fn[c](t, N)); G = cut(world_geo(N, P))
        G["_a"] = ("gunmetal", np.array([[SX0, PIT, SZ0 - .6], [SX1, CAP, SZ1], [(SX0 + SX1) / 2, 3, 1.5]]), np.array([[0, 0, 1.]] * 3), np.array([[0, 1, 2]]))
        im = render_view(G, Rv, size=440, shadow=True); tiles.append((f"{c} t={t:.1f}s", Image.fromarray((np.clip(im, 0, 1) * 255).astype(np.uint8))))
    FMAT.update(saved)
    tw, th = tiles[0][1].size; cols = 6; S = Image.new("RGB", (cols * tw, 2 * (th + 26)), (244, 242, 236)); d = ImageDraw.Draw(S)
    for k, (lab, im) in enumerate(tiles):
        x, y = (k % cols) * tw, (k // cols) * (th + 26); S.paste(im, (x, y + 26)); d.text((x + 8, y + 4), f"{k + 1}. {lab}", fill=(70, 70, 70), font=font)
    S.save(os.path.join(OUT, "final_lift_sequence.png"))
    tiles[0][1].save(os.path.join(OUT, "final_lift_sequence.gif"), save_all=True, append_images=[im for _, im in tiles[1:]], duration=600, loop=0)
if __name__ == "__main__": main()
