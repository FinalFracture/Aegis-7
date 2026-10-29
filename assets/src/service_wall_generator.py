#!/usr/bin/env python3
"""Sprocket-first service wall (#25 redirect) - 5 iterations. 3.0 W (X) x 2.0 H x <=0.5 D (floor pad may project),
back on the wall, front +Z, pivot bottom-center. Each has: a small latched human kit (<=0.6 m: hand tools + fuse /
first-aid box), and for Sprocket (~0.78 x 1.03 x 0.77, ports @0.45 m): an auto-reach parts dispenser at Sprocket height,
a charge coupler, a diagnostic port, a tool/battery swap bay, and the floor pad + coupler arm (group-3 items) folded in.
Outputs design/assets/service_wall/."""
import os, sys, numpy as np, trimesh
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dining_chair_generator as dc
from dining_chair_generator import xf, torus_ring, FMAT, export_final, render_view
from bath_pod_generator import blk, cyl, Pod, views
from kitchen_counter_generator import bev, box, crop, tonemap
from washer_dryer_generator import zdisc
from tool_wall_generator import plate_rails, tool
import coat_closet_generator as cc
import wardrobe_generator as wg
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = os.path.join(dc.ROOT, "design/assets/service_wall")
W, D, H = 3.0, 0.5, 2.0; ZB = -D / 2; WZ = ZB + .02; ZMAX = ZB + D

def human_kit(p, x, y0=1.3):   # <=0.6 m latched kit: hand tools + fuse/first-aid box
    p.add("Kit_Panel", "slate", bev(.56, .015, y0, y0 + .55, .01, .004, 1, x, WZ + .0375))
    for dx, k in ((-.19, "driver"), (-.11, "wrench"), (-.03, "pliers")): tool(p, k, x + dx, y0 + .5, WZ + .05)
    p.add("Kit_Box", "white", bev(.2, .14, y0 + .1, y0 + .45, .03, .01, 2, x + .16, WZ + .11))
    p.add("Kit_Box_Cross", "green", box(x + .15, x + .17, y0 + .22, y0 + .33, WZ + .18, WZ + .184), box(x + .105, x + .215, y0 + .265, y0 + .285, WZ + .18, WZ + .184))
    p.add("Kit_Box_Latch", "amber", box(x + .2, x + .24, y0 + .4, y0 + .415, WZ + .18, WZ + .186))

def coupler_diag(p, x):   # charge coupler + diagnostic port at 0.45 m
    p.add("Charge_Coupler", "gunmetal", bev(.22, .05, .35, .55, .02, .006, 2, x, WZ + .025))
    p.add("Charge_Port", "amber", box(x - .03, x + .03, .42, .48, WZ + .05, WZ + .055))
    p.add("Diag_Port", "gunmetal", bev(.1, .03, .4, .5, .01, .004, 1, x + .2, WZ + .015))
    p.add("Diag_Port_Light", "green", box(x + .18, x + .22, .44, .46, WZ + .03, WZ + .034))
    p.add("Status_Bar", "green", box(x - .1, x + .1, .62, .632, WZ + .02, WZ + .024))

def pad_arm(p, x, folded=True):   # floor pad (projects) + coupler arm folded flat on the plate
    p.add("Floor_Pad", "gunmetal", bev(.9, .8, 0, .015, .06, .006, 3, x, WZ + .4))
    p.add("Floor_Pad_Ring", "amber", xf(torus_ring(.22, .006, 20, 3), t=(x, .016, WZ + .42)))
    p.add("Pad_Clamps", "gunmetal", *[box(xx - .03, xx + .03, 0, .03, WZ + .74, WZ + .78) for xx in (x - .38, x + .38)])
    p.add("Coupler_Arm_Base", "gunmetal", bev(.12, .05, .9, 1.02, .02, .006, 2, x - .3, WZ + .025))
    p.add("Coupler_Arm", "alloy", box(x - .3, x + .25, .94, .98, WZ + .05, WZ + .08))     # stowed flat, latched
    p.add("Coupler_Arm_Head", "white", bev(.1, .05, .92, 1.0, .015, .006, 2, x + .28, WZ + .075))
    p.add("Coupler_Arm_Latch", "amber", box(x + .1, x + .14, .985, 1.0, WZ + .07, WZ + .08))

def swap_bay(p, x, n=4, y0=.15, w=.5):   # latched battery / tool-head swap slots
    p.add("Swap_Bay", "gunmetal", bev(w, .3, y0, y0 + .6, .02, .008, 2, x, WZ + .15))
    for i in range(n):
        xx = x - w / 2 + w / n * (i + .5)
        p.add("Swap_Packs", "white", bev(w / n - .03, .26, y0 + .05, y0 + .45, .015, .006, 2, xx, WZ + .15))
        p.add("Swap_Latches", "amber" if i % 2 else "green", box(xx - .02, xx + .02, y0 + .5, y0 + .52, WZ + .3, WZ + .306))

def iter1():  # rotary carousel
    p = Pod("Rotary Carousel"); plate_rails(p, (1.15, 1.95))
    cx = -.55
    p.add("Carousel_Housing", "white", bev(.7, .46, .1, 1.05, .1, .02, 3, cx, WZ + .23))
    p.add("Carousel_Drum", "gunmetal", cyl(cx, WZ + .24, .2, .15, 1.0, 18))
    for y in (.3, .5, .7, .9): p.add("Carousel_Bins", "white", xf(torus_ring(.21, .02, 18, 4), t=(cx, y, WZ + .24)))
    p.add("Carousel_Window", "slate", bev(.36, .01, .2, .95, .02, .004, 1, cx, WZ + .465))
    p.add("Carousel_Gate", "amber", box(cx - .12, cx + .12, .44, .46, WZ + .468, WZ + .474))
    human_kit(p, -1.15); coupler_diag(p, .35); pad_arm(p, .35); swap_bay(p, 1.15)
    return p

def iter2():  # vertical lift dispenser
    p = Pod("Vertical Lift Dispenser"); plate_rails(p, (1.15, 1.95))
    cx = -.55
    p.add("Lift_Column", "alloy", *[bev(.04, .3, .1, 1.95, .01, .004, 1, cx + s * .24, WZ + .15) for s in (-1, 1)])
    p.add("Lift_Back", "slate", box(cx - .22, cx + .22, .1, 1.95, WZ, WZ + .01))
    for y in np.arange(.75, 1.85, .2): p.add("Lift_Bins", "white", bev(.42, .26, y, y + .16, .02, .008, 2, cx, WZ + .15))
    p.add("Lift_Carriage", "gunmetal", bev(.46, .3, .4, .5, .02, .008, 2, cx, WZ + .15))
    p.add("Lift_Delivery_Tray", "alloy", box(cx - .2, cx + .2, .5, .52, WZ + .02, WZ + .3), box(cx - .2, cx + .2, .52, .56, WZ + .28, WZ + .3))
    p.add("Lift_Gates", "amber", *[box(cx - .2, cx + .2, y + .075, y + .085, WZ + .28, WZ + .29) for y in np.arange(.75, 1.85, .2)])
    human_kit(p, -1.15); coupler_diag(p, .35); pad_arm(p, .35); swap_bay(p, 1.15)
    return p

def iter3():  # linear rail shuttle at Sprocket height
    p = Pod("Linear Rail Shuttle"); plate_rails(p, (1.15, 1.95))
    p.add("Shuttle_Rail", "alloy", blk(-1.45, 1.45, .72, .76, WZ, WZ + .05, .01, 1), blk(-1.45, 1.45, .98, 1.02, WZ, WZ + .05, .01, 1))
    for x in np.linspace(-1.3, -.3, 6):
        p.add("Shuttle_Bins", "white", bev(.14, .2, .78, .96, .02, .008, 2, x, WZ + .15))
        p.add("Shuttle_Bin_Latches", "amber", box(x - .02, x + .02, .92, .935, WZ + .25, WZ + .256))
    p.add("Shuttle_Carriage", "gunmetal", bev(.2, .26, .66, 1.06, .02, .008, 2, .05, WZ + .15))
    p.add("Shuttle_Light", "violet", box(-.03, .13, 1.0, 1.01, WZ + .28, WZ + .284))
    p.add("Shuttle_Drop_Tray", "alloy", box(-.05, .15, .55, .57, WZ + .05, WZ + .3))
    human_kit(p, -1.1, 1.3); coupler_diag(p, .55); pad_arm(p, .55); swap_bay(p, 1.25, 3, .1, .4)
    return p

def iter4():  # drawer-matrix auto-feed
    p = Pod("Drawer-Matrix Auto-Feed"); plate_rails(p, (1.15, 1.95))
    cx, nx, ny = -.55, 5, 5; w, h = .7, .8
    p.add("Matrix_Frame", "white", bev(w + .04, .4, .12, .12 + h + .04, .02, .008, 2, cx, WZ + .2))
    for i in range(nx):
        for j in range(ny):
            x = cx - w / 2 + w / nx * (i + .5); y = .14 + h / ny * (j + .5)
            p.add("Matrix_Drawers", "gunmetal", box(x - w / nx / 2 + .006, x + w / nx / 2 - .006, y - h / ny / 2 + .006, y + h / ny / 2 - .006, WZ + .4, WZ + .41))
            p.add("Matrix_Latches", "amber" if (i + j) % 3 else "green", box(x - .012, x + .012, y - .006, y + .006, WZ + .41, WZ + .414))
    p.add("Feed_Chute", "alloy", box(cx + w / 2 + .03, cx + w / 2 + .1, .3, .6, WZ + .2, WZ + .4))
    p.add("Feed_Tray", "alloy", box(cx + w / 2 + .03, cx + w / 2 + .2, .44, .46, WZ + .2, WZ + .42))
    human_kit(p, -1.15, 1.3); coupler_diag(p, .45); pad_arm(p, .45); swap_bay(p, 1.2, 3, .15, .45)
    return p

def iter5():  # compact alcove pod: everything inside one moulded Sprocket alcove (+ kit beside)
    p = Pod("Compact Alcove Pod"); plate_rails(p, (1.15, 1.95))
    cx, aw = .2, 1.1
    p.add("Alcove_Shell", "white", bev(.06, D - .02, 0, 1.4, .02, .008, 2, cx - aw / 2, WZ + (D - .02) / 2),
          bev(.06, D - .02, 0, 1.4, .02, .008, 2, cx + aw / 2, WZ + (D - .02) / 2), bev(aw + .06, D - .02, 1.32, 1.42, .03, .01, 3, cx, WZ + (D - .02) / 2))
    p.add("Alcove_Edge", "violet", box(cx - aw / 2 - .03, cx + aw / 2 + .03, 1.32, 1.33, ZMAX - .03, ZMAX - .026))
    for s in (-1, 1):   # side-wall dispensers (rotary cartridges) at Sprocket height, gated
        x = cx + s * (aw / 2 - .06)
        p.add("Side_Dispensers", "gunmetal", bev(.06, .3, .55, 1.15, .015, .006, 2, x, WZ + .2))
        p.add("Side_Dispenser_Gates", "amber", *[box(x - .03, x + .03, y, y + .012, WZ + .35, WZ + .356) for y in (.65, .85, 1.05)])
    p.add("Alcove_Swap_Shelf", "gunmetal", bev(aw - .2, .3, 1.15, 1.18, .01, .004, 1, cx, WZ + .15))
    p.add("Swap_Packs", "white", *[bev(.18, .24, 1.18, 1.3, .015, .006, 2, x, WZ + .15) for x in (cx - .3, cx - .1, cx + .1, cx + .3)])
    p.add("Swap_Latches", "green", *[box(x - .02, x + .02, 1.27, 1.285, WZ + .27, WZ + .276) for x in (cx - .3, cx - .1, cx + .1, cx + .3)])
    coupler_diag(p, cx - .1); pad_arm(p, cx, True)
    human_kit(p, -1.05, 1.0)
    p.add("Spare_Bins", "white", *[bev(.5, .3, y, y + .18, .03, .01, 2, 1.15, WZ + .15) for y in (.3, .55, .8)])
    p.add("Spare_Bin_Latches", "amber", *[box(1.33, 1.37, y + .14, y + .155, WZ + .3, WZ + .306) for y in (.3, .55, .8)])
    return p

def main():
    os.makedirs(OUT, exist_ok=True); isos = []
    for i, fn in enumerate([iter1, iter2, iter3, iter4, iter5], 1):
        p = fn(); tris, iso, lo, hi, bad = wg.sheet(p, os.path.join(OUT, f"iter_0{i}_sheet.png"), f"iter_0{i}  {p.name}")
        print(i, p.name, tris, lo, hi, "non-watertight:", bad)
        if i == 5:   # render-only: Sprocket docked
            _, geo = export_final(p.P, [os.path.join(OUT, "iter_05.glb")]); g = dict(geo); sg, _ = cc.sprocket_geo(.2); g.update(sg)
            saved = tonemap(); R = views()[3]; im = render_view(g, R, size=760, shadow=True); ns = render_view(g, R, size=760, shadow=False)
            fg = np.abs(ns - ns[0, 0]).sum(2) > .03; im[fg] = np.clip(im[fg] * 1.12 + .02, 0, 1); FMAT.update(saved); iso = crop(im)
        isos.append((p.name + (" (Sprocket docked, render only)" if i == 5 else ""), iso))
    fig, axs = plt.subplots(3, 2, figsize=(16, 14), facecolor="#F4F2EC")
    for ax in axs.flat: ax.axis("off")
    for ax, (i, (n, im)) in zip(axs.flat, enumerate(isos, 1)): ax.imshow(im); ax.set_title(f"{i}. {n}", fontsize=12, color="#555")
    plt.tight_layout(rect=(0, 0, 1, .97)); fig.savefig(os.path.join(OUT, "overview.png"), dpi=80, facecolor="#F4F2EC"); plt.close(fig)

# =====================================================================================================
# final: polished Linear Rail Shuttle (iter_03) with node hierarchy + glTF animation clips
# =====================================================================================================
FPS = 30
BIN_X = list(np.linspace(-1.4, -.4, 6)); FETCH = 2          # Bin_03 is fetched
PARK_X = -.05; CAR_Y = 1.03; CAR_Z = WZ + .18
ARM_PIV = np.array([.2, .45, WZ + .03]); ARM_ANG = -4.7      # deg about Y: head moves +Z to meet the docked port
SP_DOCK = np.array([.55, .015, -.13 + .385]); SP_START = np.array([.55, .015, 1.8])
BIN_Y0 = .78; TRAY_TOP = .57; BIN_PULL = .22; BIN_LIFT = .02

def _rot(axis, deg):
    a = np.radians(deg) / 2; ax = np.asarray(axis, float); ax /= np.linalg.norm(ax)
    return np.r_[ax * np.sin(a), np.cos(a)]          # glTF [x,y,z,w]
QI = np.array([0, 0, 0, 1.])
def ss(t, a, b):   # smoothstep 0..1 over [a,b]
    u = np.clip((t - a) / max(b - a, 1e-9), 0, 1); return u * u * (3 - 2 * u)

def build_nodes():
    """Returns {node: dict(parent, T(rest local), parts={part:(mat, mesh in LOCAL coords)})}."""
    N = {}
    def node(name, T, parent=None): N[name] = dict(parent=parent, T=np.array(T, float), parts={}); return N[name]
    def put(nd, part, mat, *ms):
        o = -np.asarray(nd["Tw"] if "Tw" in nd else nd["T"])
        m = ms[0] if len(ms) == 1 else dc.merge(list(ms)); m = xf(m, t=tuple(o))
        if part in nd["parts"]: m = dc.merge([nd["parts"][part][1], m])
        nd["parts"][part] = (mat, m)
    # ---- static wall (one node, several named parts) ----
    st = Pod("static"); plate_rails(st, (1.15, 1.95))
    st.add("Shuttle_Rails", "alloy", blk(-1.48, 1.0, .72, .76, WZ, WZ + .05, .012, 2), blk(-1.48, 1.0, .98, 1.02, WZ, WZ + .05, .012, 2))
    st.add("Rail_Brackets", "gunmetal", *[box(x - .02, x + .02, .7, 1.04, WZ, WZ + .03) for x in (-1.45, -.75, .0, .95)])
    st.add("Rail_End_Stops", "gunmetal", box(-1.5 + .02, -1.48 + .04, .96, 1.2, WZ, WZ + .3), box(.96, 1.0, .96, 1.2, WZ, WZ + .3))
    st.add("Bin_Shelf", "gunmetal", bev(1.1, .22, .76, .78, .006, .004, 1, -.9, WZ + .13))
    st.add("Handoff_Tray", "alloy", bev(.22, .25, .55, .57, .008, .004, 1, PARK_X, WZ + .365), box(PARK_X - .11, PARK_X + .11, .57, .6, WZ + .47, WZ + .48))
    st.add("Handoff_Tray_Bracket", "gunmetal", box(PARK_X - .015, PARK_X + .015, .45, .55, WZ, WZ + .4))
    human_kit(st, -1.1, 1.3)
    st.add("Coupler_Base", "gunmetal", bev(.1, .05, .37, .53, .02, .006, 2, ARM_PIV[0], WZ + .025))
    st.add("Diag_Port", "gunmetal", bev(.1, .03, .4, .5, .01, .004, 1, 1.0 - .0, WZ + .015))
    st.add("Diag_Port_Light", "green", box(.98, 1.02, .44, .46, WZ + .03, WZ + .034))
    st.add("Status_Bar", "green", box(.45, .65, 1.08, 1.092, WZ + .02, WZ + .024))
    st.add("Floor_Pad", "gunmetal", bev(.9, .8, 0, .015, .06, .006, 3, .55, WZ + .4))
    st.add("Floor_Pad_Ring", "amber", xf(torus_ring(.22, .006, 20, 3), t=(.55, .016, WZ + .42)))
    st.add("Pad_Clamps", "gunmetal", *[box(xx - .03, xx + .03, 0, .03, WZ + .74, WZ + .78) for xx in (.17, .93)])
    swap_bay(st, 1.28, 2, .1, .3)
    ws = node("Wall_Static", (0, 0, 0))
    for k, (mk, m) in st.P.items(): ws["parts"][k] = (mk, m)
    # ---- bins + gates + latches ----
    for i, x in enumerate(BIN_X, 1):
        b = node(f"Bin_{i:02d}", (x, BIN_Y0, WZ + .15))
        put(b, "Bin", "white", bev(.14, .2, BIN_Y0, BIN_Y0 + .18, .02, .008, 2, x, WZ + .15))
        put(b, "Bin_Lip", "alloy", box(x - .07, x + .07, BIN_Y0 + .17, BIN_Y0 + .18, WZ + .23, WZ + .25))
        g = node(f"Gate_{i:02d}", (x - .07, .86, WZ + .255))
        put(g, "Gate", "gunmetal", box(x - .07, x + .07, .855, .865, WZ + .25, WZ + .26))
        l = node(f"Latch_{i:02d}", (x + .07, .86, WZ + .255))
        put(l, "Latch", "amber", box(x + .05, x + .08, .852, .868, WZ + .26, WZ + .266))
    # ---- shuttle carriage (+ child gripper) + park latch ----
    c = node("Shuttle_Carriage", (PARK_X, CAR_Y, CAR_Z)); c["Tw"] = c["T"]
    put(c, "Carriage_Body", "gunmetal", bev(.22, .26, CAR_Y + .005, CAR_Y + .15, .03, .01, 3, PARK_X, CAR_Z + .02))
    put(c, "Carriage_Wheels", "alloy", *[zdisc(PARK_X + dx, CAR_Y + .005, WZ + .045, WZ + .06, .022, 10) for dx in (-.07, .07)])
    put(c, "Carriage_Light", "violet", box(PARK_X - .08, PARK_X + .08, CAR_Y + .13, CAR_Y + .14, CAR_Z + .15, CAR_Z + .154))
    gp = node("Shuttle_Gripper", (0, .24, 0), "Shuttle_Carriage"); gp["Tw"] = np.array([PARK_X, CAR_Y, CAR_Z])   # local mesh about carriage pivot
    for dx in (-.1, .1):
        put(gp, "Gripper_Arms", "alloy", box(PARK_X + dx - .006, PARK_X + dx + .006, CAR_Y - .22, CAR_Y, CAR_Z - .08, CAR_Z + .02))
        put(gp, "Gripper_Pads", "slatefab", box(PARK_X + dx - (.012 if dx > 0 else -.0) - .0, PARK_X + dx + (.0 if dx > 0 else .012), CAR_Y - .2, CAR_Y - .12, CAR_Z - .07, CAR_Z + .01))
    put(gp, "Gripper_Bridge", "gunmetal", box(PARK_X - .11, PARK_X + .11, CAR_Y - .02, CAR_Y, CAR_Z - .08, CAR_Z + .02))
    lp = node("Latch_Park", (PARK_X - .14, CAR_Y + .05, CAR_Z))
    put(lp, "Park_Latch", "amber", box(PARK_X - .16, PARK_X - .11, CAR_Y + .02, CAR_Y + .08, CAR_Z - .03, CAR_Z + .03))
    # ---- coupler arm (swings about Y at its wall base) ----
    a = node("Coupler_Arm", ARM_PIV)
    put(a, "Arm", "alloy", bev(.35, .03, .43, .47, .01, .004, 1, ARM_PIV[0] + .175, ARM_PIV[2]))
    put(a, "Arm_Head", "white", bev(.08, .05, .41, .49, .015, .006, 2, ARM_PIV[0] + .34, ARM_PIV[2] + .01))
    put(a, "Arm_Head_Port", "amber", box(ARM_PIV[0] + .32, ARM_PIV[0] + .36, .435, .465, ARM_PIV[2] + .035, ARM_PIV[2] + .04))
    # ---- Sprocket stand-in (own top-level node; pivot bottom-centre; port on back @0.45) ----
    sp = node("Sprocket_Standin", SP_DOCK); x0, z0 = SP_DOCK[0], SP_DOCK[2]
    put(sp, "Standin_Chassis", "gunmetal", bev(.7, .7, .08, .32, .05, .015, 2, x0, z0))
    put(sp, "Standin_Wheels", "slatefab", *[xf(xf(loft_x(.075, .05), np.eye(4)), t=(x0 + sx * .36, .09, z0 + sz * .24)) for sx in (-1, 1) for sz in (-1, 1)])
    put(sp, "Standin_Torso", "white", bev(.6, .55, .32, .84, .08, .02, 3, x0, z0 + .02))
    put(sp, "Standin_Head", "white", bev(.42, .3, .86, 1.03, .06, .015, 3, x0, z0 + .1))
    put(sp, "Standin_Neck", "alloy", cyl(x0, z0 + .05, .04, .84, .87, 10))
    put(sp, "Standin_Eyes", "slate", *[xf(zdisc(0, .93, 0, .03, .045, 12), t=(x0 + dx, 0, z0 + .25)) for dx in (-.1, .1)])
    put(sp, "Standin_Back_Port", "amber", box(x0 - .03, x0 + .03, .43, .47, z0 - .385, z0 - .375))
    put(sp, "Standin_Back_Plate", "gunmetal", bev(.14, .02, .38, .52, .02, .005, 1, x0, z0 - .375 + .01))
    return N

def loft_x(r, w):   # wheel: cylinder along X centred at origin
    m = dc.loft(dc.circle(r, 12), [(-w / 2, 1, 1), (w / 2, 1, 1)])
    return xf(m, trimesh.transformations.rotation_matrix(np.pi / 2, [0, 0, 1]))

# ---------- clips: f(t) -> {node: (T, R, S)} overrides (local TRS) ----------
def rest(N): return {n: (nd["T"].copy(), QI.copy(), np.ones(3)) for n, nd in N.items()}

def clip_arrive(t, N):
    o = {}; u = ss(t, 0, 2.2); T = SP_START + (SP_DOCK - SP_START) * u
    o["Sprocket_Standin"] = (T, QI, np.ones(3))
    o["Coupler_Arm"] = (N["Coupler_Arm"]["T"], _rot([0, 1, 0], ARM_ANG * ss(t, 2.2, 3.0)), np.ones(3))
    return o
def bin_T(N): return N[f"Bin_{FETCH + 1:02d}"]["T"]
def clip_fetch(t, N):
    o = {}; bx = BIN_X[FETCH]
    o["Latch_Park"] = (N["Latch_Park"]["T"] + [-.04 * ss(t, 0, .2), 0, 0], QI, np.ones(3))
    cx = PARK_X + (bx - PARK_X) * ss(t, .2, 1.2) + (PARK_X - bx) * ss(t, 2.9, 4.0)
    o["Shuttle_Carriage"] = (np.array([cx, CAR_Y, CAR_Z]), QI, np.ones(3))
    li = f"Latch_{FETCH + 1:02d}"; gi = f"Gate_{FETCH + 1:02d}"
    o[li] = (N[li]["T"] + [.03 * (ss(t, 1.2, 1.5) - ss(t, 2.9, 3.1)), 0, 0], QI, np.ones(3))
    o[gi] = (N[gi]["T"], _rot([0, 0, 1], 80 * (ss(t, 1.5, 1.9) - ss(t, 2.7, 2.9))), np.ones(3))
    gy = .24 * (1 - ss(t, 1.9, 2.3)); gz = BIN_PULL * ss(t, 2.3, 2.7)
    o["Shuttle_Gripper"] = (np.array([0, gy, gz]), QI, np.ones(3))
    bt = bin_T(N); bxw = bt[0] + (cx - bx) * (t >= 2.9)
    o[f"Bin_{FETCH + 1:02d}"] = (np.array([bxw if t >= 2.9 else bt[0], bt[1] + BIN_LIFT * ss(t, 2.3, 2.7), bt[2] + gz]), QI, np.ones(3))
    return o
def clip_handoff(t, N):
    o = {}; bt = bin_T(N); dy = (TRAY_TOP - BIN_Y0 - BIN_LIFT) * ss(t, 0, .8)
    o["Shuttle_Carriage"] = (np.array([PARK_X, CAR_Y, CAR_Z]), QI, np.ones(3))
    o["Shuttle_Gripper"] = (np.array([0, dy * (1 - ss(t, .9, 1.3)) + 0 * t, BIN_PULL]), QI, np.ones(3))
    start = np.array([PARK_X, bt[1] + BIN_LIFT + dy, bt[2] + BIN_PULL]); take = np.array([.3, .62, .25])
    u = ss(t, 1.3, 2.5); P = start + (take - start) * u
    o[f"Bin_{FETCH + 1:02d}"] = (P, QI, np.ones(3) * max(1 - ss(t, 1.8, 2.5), 1e-3))
    return o
def clip_return(t, N):
    o = {}; bt = bin_T(N)
    gz = BIN_PULL * (1 - ss(t, 0, .6)); gy = .24 * ss(t, .6, 1.2)
    o["Shuttle_Gripper"] = (np.array([0, gy, gz]), QI, np.ones(3))
    o["Shuttle_Carriage"] = (np.array([PARK_X, CAR_Y, CAR_Z]), QI, np.ones(3))
    o["Coupler_Arm"] = (N["Coupler_Arm"]["T"], _rot([0, 1, 0], ARM_ANG * (1 - ss(t, 0, 1.0))), np.ones(3))
    o["Latch_Park"] = (N["Latch_Park"]["T"] + [-.04 * (1 - ss(t, 1.5, 2.0)), 0, 0], QI, np.ones(3))
    o[f"Bin_{FETCH + 1:02d}"] = (bt, QI, np.ones(3) * max(ss(t, 1.0, 2.0), 1e-3))   # restocked into its slot
    o["Sprocket_Standin"] = (SP_DOCK, QI, np.ones(3))
    return o
CLIPS = [("sprocket_arrive", clip_arrive, 3.0), ("shuttle_fetch", clip_fetch, 4.0), ("handoff", clip_handoff, 2.5), ("return_idle", clip_return, 2.0)]

def qmat(q):
    x, y, z, w = q; return np.array([[1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w)],
                                     [2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w)],
                                     [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y)]])
def world_geo(N, pose, skip=()):
    """pose: {node:(T,R,S)} local. Returns render geo with world-space verts."""
    from dining_chair_generator import shade_split
    def M(n):
        T, R, S = pose[n]; m = np.eye(4); m[:3, :3] = qmat(R) * S; m[:3, 3] = T
        par = N[n]["parent"]; return (M(par) @ m) if par else m
    geo = {}
    for n, nd in N.items():
        if n in skip: continue
        Mw = M(n)
        for part, (mk, m) in nd["parts"].items():
            V, Nn, UV, F = shade_split(m); Vw = V @ Mw[:3, :3].T + Mw[:3, 3]
            Nw = Nn @ Mw[:3, :3].T; Nw /= np.linalg.norm(Nw, axis=1, keepdims=True) + 1e-12
            geo[f"{n}/{part}"] = (mk, Vw, Nw, F)
    return geo

def export_anim_glb(N, path):
    from dining_chair_generator import shade_split, _col
    from pygltflib import (GLTF2, Scene, Node, Mesh, Primitive, Attributes, Buffer, BufferView, Accessor, Material,
                           PbrMetallicRoughness, Animation, AnimationSampler, AnimationChannel, AnimationChannelTarget)
    g = GLTF2(); blob = bytearray(); mats = {}; idx = {}; tris = {}
    def add(arr, target, ctype, typ, mm=False):
        arr = np.ascontiguousarray(arr); off = len(blob); blob.extend(arr.tobytes())
        while len(blob) % 4: blob.append(0)
        g.bufferViews.append(BufferView(buffer=0, byteOffset=off, byteLength=arr.nbytes, target=target))
        acc = Accessor(bufferView=len(g.bufferViews) - 1, componentType=ctype, count=len(arr), type=typ)
        if mm: a2 = arr.reshape(len(arr), -1); acc.min = a2.min(0).tolist(); acc.max = a2.max(0).tolist()
        g.accessors.append(acc); return len(g.accessors) - 1
    for n, nd in N.items():
        prims = []; tris[n] = 0
        bymat = {}
        for part, (mk, m) in nd["parts"].items(): bymat.setdefault(mk, []).append(shade_split(m))
        for mk, lst in bymat.items():
            if mk not in mats:
                pm = FMAT[mk]; mats[mk] = len(g.materials)
                g.materials.append(Material(name=pm.name, emissiveFactor=_col(pm.emissiveFactor if pm.emissiveFactor is not None else [0, 0, 0]),
                    pbrMetallicRoughness=PbrMetallicRoughness(baseColorFactor=_col(pm.baseColorFactor), metallicFactor=float(pm.metallicFactor), roughnessFactor=float(pm.roughnessFactor))))
            V = []; Nn = []; UV = []; F = []; o = 0
            for (v, nn, uv, f) in lst: V.append(v); Nn.append(nn); UV.append(uv); F.append(f + o); o += len(v)
            V, Nn, UV, F = map(np.vstack, (V, Nn, UV, F)); tris[n] += len(F)
            a = Attributes(POSITION=add(V.astype(np.float32), 34962, 5126, "VEC3", True), NORMAL=add(Nn.astype(np.float32), 34962, 5126, "VEC3"),
                           TEXCOORD_0=add(UV.astype(np.float32), 34962, 5126, "VEC2"))
            prims.append(Primitive(attributes=a, indices=add(F.astype(np.uint32).ravel(), 34963, 5125, "SCALAR"), material=mats[mk]))
        g.meshes.append(Mesh(name=n, primitives=prims))
        g.nodes.append(Node(name=n, mesh=len(g.meshes) - 1, translation=[float(x) for x in nd["T"]])); idx[n] = len(g.nodes) - 1
    roots = []
    for n, nd in N.items():
        if nd["parent"]: g.nodes[idx[nd["parent"]]].children.append(idx[n])
        else: roots.append(idx[n])
    g.scenes = [Scene(name="ServiceWall", nodes=roots)]; g.scene = 0
    R0 = rest(N)
    for cname, fn, dur in CLIPS:
        ts = np.round(np.arange(0, dur + 1e-6, 1 / FPS), 5).astype(np.float32); poses = [fn(float(t), N) for t in ts]
        anim = Animation(name=cname, samplers=[], channels=[]); tin = add(ts, None, 5126, "SCALAR", True)
        for n in poses[0].keys():
            for k, (path_, typ) in enumerate((("translation", "VEC3"), ("rotation", "VEC4"), ("scale", "VEC3"))):
                vals = np.array([p[n][k] for p in poses], np.float32)
                if np.allclose(vals, vals[0]) and np.allclose(vals[0], R0[n][k]): continue
                out = add(vals, None, 5126, typ)
                anim.samplers.append(AnimationSampler(input=tin, output=out, interpolation="LINEAR"))
                anim.channels.append(AnimationChannel(sampler=len(anim.samplers) - 1, target=AnimationChannelTarget(node=idx[n], path=path_)))
        g.animations.append(anim)
    g.buffers = [Buffer(byteLength=len(blob))]; g.set_binary_blob(bytes(blob)); g.save_binary(path)
    return tris

def clearance_checks(N):
    """Stowed arm vs docked stand-in; carriage vs stand-in; engaged arm head vs stand-in back port."""
    def wb(pose, n):
        g = world_geo(N, pose); V = np.vstack([v for k, (mk, v, nn, f) in g.items() if k.startswith(n + "/")]); return V.min(0), V.max(0)
    P = rest(N); sp_lo, sp_hi = wb(P, "Sprocket_Standin"); arm_lo, arm_hi = wb(P, "Coupler_Arm"); car_lo, car_hi = wb(P, "Shuttle_Carriage")
    P2 = rest(N); P2.update(clip_arrive(3.0, N)); a2_lo, a2_hi = wb(P2, "Coupler_Arm")
    worst = 9.0
    for cname, fn, dur in CLIPS:   # bins / carriage / gripper vs stand-in over every frame
        for t in np.arange(0, dur + 1e-6, .1):
            P3 = rest(N); P3.update(fn(t, N)); s_lo, s_hi = wb(P3, "Sprocket_Standin")
            for n in ("Shuttle_Carriage",):
                c_lo, c_hi = wb(P3, n); gap = max(s_lo[0] - c_hi[0], c_lo[0] - s_hi[0], s_lo[2] - c_hi[2], c_lo[2] - s_hi[2], s_lo[1] - c_hi[1], c_lo[1] - s_hi[1]); worst = min(worst, gap)
    return {"stowed_arm_to_standin_back_z": round(float(sp_lo[2] - arm_hi[2]), 3),
            "engaged_arm_head_to_standin_back_z": round(float(sp_lo[2] - a2_hi[2]), 3),
            "carriage_to_standin_min_gap_all_clips": round(float(worst), 3),
            "standin_size": (sp_hi - sp_lo).round(3).tolist()}

def final_main():
    from PIL import Image, ImageDraw, ImageFont
    import pygltflib
    N = build_nodes(); gp = os.path.join(dc.ROOT, "godot/assets/models/service_wall_rail_shuttle.glb")
    tris = export_anim_glb(N, gp)
    static = sum(v for k, v in tris.items() if k != "Sprocket_Standin")
    print("tris per node", tris); print("STATIC+moving wall tris", static, "| standin tris", tris["Sprocket_Standin"], "| static-only", tris["Wall_Static"])
    bad = [f"{n}/{p}" for n, nd in N.items() for p, (mk, m) in nd["parts"].items() if not all(c.is_watertight for c in m.split(only_watertight=False))]
    print("non-watertight", bad); print("clearance", clearance_checks(N))
    g = pygltflib.GLTF2().load(gp)
    print("RELOAD nodes:", [n.name for n in g.nodes])
    print("RELOAD anims:", [(a.name, len(a.channels), round(float(g.accessors[a.samplers[0].input].max[0]), 2)) for a in g.animations])
    sc = trimesh.load(gp); print("trimesh reload geometry count", len(sc.geometry))
    # ---- sheet at rest (stand-in hidden) ----
    saved = tonemap(); top, front, side, iso = views()
    def rv(geo, R, s, sh):
        im = render_view(geo, R, size=s, shadow=sh); ns = render_view(geo, R, size=s, shadow=False) if sh else im
        fg = np.abs(ns - ns[0, 0]).sum(2) > .03; im[fg] = np.clip(im[fg] * 1.12 + .02, 0, 1); return crop(im)
    G0 = world_geo(N, rest(N), skip=("Sprocket_Standin",))
    ims = [rv(G0, top, 700, False), rv(G0, front, 700, True), rv(G0, side, 500, True), rv(G0, iso, 760, True)]
    bg = "#F4F2EC"; fig = plt.figure(figsize=(14, 9), facecolor=bg); gs = fig.add_gridspec(2, 3, width_ratios=[1, 1, .5])
    for ax, im, t in ((fig.add_subplot(gs[0, :2]), ims[0], "Top"), (fig.add_subplot(gs[0, 2]), ims[2], "Side"),
                      (fig.add_subplot(gs[1, 0]), ims[1], "Front"), (fig.add_subplot(gs[1, 1:]), ims[3], "Iso")):
        ax.imshow(im); ax.axis("off"); ax.set_title(t, fontsize=11, color="#555")
    fig.suptitle("Final  Linear Rail Shuttle service wall (rest, stand-in hidden)", fontsize=12, color="#444"); plt.tight_layout(rect=(0, 0, 1, .95))
    fig.savefig(os.path.join(OUT, "final_rail_shuttle_sheet.png"), dpi=100, facecolor=bg); plt.close(fig)
    # ---- frame strip + gif ----
    a, b = np.radians(28), np.radians(24)
    Rv = np.array([[1, 0, 0], [0, np.cos(b), -np.sin(b)], [0, np.sin(b), np.cos(b)]]) @ np.array([[np.cos(a), 0, np.sin(a)], [0, 1, 0], [-np.sin(a), 0, np.cos(a)]])
    frames = [("sprocket_arrive", 0.0), ("sprocket_arrive", 1.6), ("sprocket_arrive", 3.0), ("shuttle_fetch", 1.2), ("shuttle_fetch", 1.9),
              ("shuttle_fetch", 2.7), ("shuttle_fetch", 4.0), ("handoff", .8), ("handoff", 1.9), ("handoff", 2.5), ("return_idle", 1.2), ("return_idle", 2.0)]
    fn_of = {c: f for c, f, d in CLIPS}; font = ImageFont.truetype("DejaVuSans.ttf", 18); tiles = []
    # fixed framing: include a far bbox marker by rendering a common geo extent (stand-in start pose)
    for cname, t in frames:
        P = rest(N)
        if cname != "sprocket_arrive": P.update(clip_arrive(3.0, N))
        if cname in ("handoff",): P.update(clip_fetch(4.0, N))
        if cname == "return_idle": P.update(clip_fetch(4.0, N)); P.update(clip_handoff(2.5, N))
        P.update(fn_of[cname](t, N)); G = world_geo(N, P)
        anchor = trimesh.creation.box((.001, .001, .001)); anchor.apply_translation((0, 0, 1.85))
        G["_anchor"] = ("gunmetal", np.array([[-1.5, 0, 1.85], [1.5, 2.0, -.25], [0, 1.0, .8]]), np.array([[0, 0, 1.]] * 3), np.array([[0, 1, 2]]))
        im = render_view(G, Rv, size=520, shadow=True)
        tiles.append((f"{cname} t={t:.1f}s", Image.fromarray((np.clip(im, 0, 1) * 255).astype(np.uint8))))
    FMAT.update(saved)
    tw, th = tiles[0][1].size; cols = 4; rows = (len(tiles) + cols - 1) // cols
    strip = Image.new("RGB", (cols * tw, rows * (th + 30)), (244, 242, 236)); d = ImageDraw.Draw(strip)
    for k, (lab, im) in enumerate(tiles):
        x, y = (k % cols) * tw, (k // cols) * (th + 30); strip.paste(im, (x, y + 30)); d.text((x + 10, y + 5), f"{k + 1}. {lab}", fill=(70, 70, 70), font=font)
    strip.save(os.path.join(OUT, "final_rail_shuttle_sequence.png"))
    gif = [im.resize((tw // 2 * 2 // 1, th)) for _, im in tiles]
    gif[0].save(os.path.join(OUT, "final_rail_shuttle_sequence.gif"), save_all=True, append_images=gif[1:], duration=600, loop=0)

if __name__ == "__main__":
    final_main() if len(sys.argv) > 1 and sys.argv[1] == "final" else main()
