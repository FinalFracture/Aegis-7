#!/usr/bin/env python3
"""Bath pod (#8) - 5 prefab shower/WC/sink module iterations. Owner: Rook.
~2.2 W x 2.2 D x 2.4 H, pivot bottom-center, doorway on +Z, Y up. Reuses the swivel-chair loft / normal-split /
glb writer / soft rasterizer from dining_chair_generator.py. Outputs design/assets/bath_pod/iter_0N.glb, sheets, overview.
Spinward = -X (drains offset / spiral ribs toward -X)."""
import os, sys, numpy as np, trimesh
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dining_chair_generator as dc
from dining_chair_generator import loft, rrect, circle, torus_ring, xf, merge, export_final, render_view, FMAT
from trimesh.visual.material import PBRMaterial as _PBR
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.ndimage import distance_transform_edt, label

ROOT = dc.ROOT; OUT = os.path.join(ROOT, "design/assets/bath_pod")
FMAT.update({
 "white": _PBR(name="WhiteComposite", baseColorFactor=(0.86, 0.88, 0.90, 1), metallicFactor=0.0, roughnessFactor=0.35),
 "slate": _PBR(name="Slate", baseColorFactor=(0.16, 0.18, 0.22, 1), metallicFactor=0.3, roughnessFactor=0.6),
 "glass": _PBR(name="Glass", baseColorFactor=(0.70, 0.82, 0.90, 0.25), metallicFactor=0.0, roughnessFactor=0.05),
 "mirror": _PBR(name="Mirror", baseColorFactor=(0.85, 0.88, 0.92, 1), metallicFactor=1.0, roughnessFactor=0.05),
 "green": _PBR(name="StatusGreen", baseColorFactor=(0.247, 0.686, 0.416, 1), metallicFactor=0.0, roughnessFactor=0.4, emissiveFactor=(0.247, 0.686, 0.416)),
})
W = D = 2.2; T = 0.06; FL = 0.06            # wall thickness, raised floor top
DOOR_W, DOOR_H = 0.9, FL + 2.02             # clear opening 0.9 x 2.02 above floor

def thick_path(pts, t, y0, y1):
    """Extrude a 2D (x,z) polyline into a wall of thickness t (offset toward pod centre). Closed mesh."""
    pts = np.asarray(pts, float); M = len(pts); nrm = np.zeros_like(pts)
    for i in range(M):
        a, b = pts[max(i - 1, 0)], pts[min(i + 1, M - 1)]; tg = b - a; tg /= np.linalg.norm(tg) + 1e-12
        n = np.array([-tg[1], tg[0]]); nrm[i] = n if n @ -pts[i] > 0 else -n
    inn = pts + nrm * t
    V = []
    for P in (pts, inn):
        for y in (y0, y1): V += [(p[0], y, p[1]) for p in P]
    V = np.array(V); ob, ot, ib, it_ = 0, M, 2 * M, 3 * M
    F = []
    for i in range(M - 1):
        j = i + 1
        for A, B in ((ob, ot), (ot, it_), (it_, ib), (ib, ob)):
            F += [(A + i, A + j, B + j), (A + i, B + j, B + i)]
    i = M - 1; F += [(ob + i, ot + i, it_ + i), (ob + i, it_ + i, ib + i)]
    F += [(ob, it_, ot), (ob, ib, it_)]
    m = trimesh.Trimesh(V, np.array(F), process=False)
    if m.volume < 0: m.invert()
    s = np.r_[0, np.cumsum(np.linalg.norm(np.diff(pts, axis=0), axis=1))]
    m.metadata["uv"] = np.c_[np.tile(s, 4), V[:, 1]]
    return m

def shell_path(w, d, r, n, dx):
    """Rounded-rect wall outline with a door gap centred at x=dx on the +Z face."""
    p = rrect(w, d, r, n); k = n + 1
    c1, c2, c3, c4 = p[:k], p[k:2 * k], p[2 * k:3 * k], p[3 * k:]
    return np.vstack([[(dx - DOOR_W / 2, d / 2)], c2, c3, c4, c1, [(dx + DOOR_W / 2, d / 2)]])

def blk(x0, x1, y0, y1, z0, z1, r=0.02, n=2):
    m = loft(rrect(x1 - x0, z1 - z0, min(r, (x1 - x0) / 2.01, (z1 - z0) / 2.01), n), [(y0, 1, 1), (y1, 1, 1)])
    return xf(m, t=((x0 + x1) / 2, 0, (z0 + z1) / 2))

def cyl(x, z, r, y0, y1, s=16): return xf(loft(circle(r, s), [(y0, 1, 1), (y1, 1, 1)]), t=(x, 0, z))

class Pod:
    def __init__(s, name): s.name = name; s.P = {}; s.obst = []; s.zones = {}; s.plan = None; s.dx = 0
    def add(s, part, mat, *meshes):
        if part in s.P: meshes = (s.P[part][1],) + meshes
        s.P[part] = (mat, merge(list(meshes)) if len(meshes) > 1 else meshes[0])
    def ob(s, x0, x1, z0, z1): s.obst.append((x0, x1, z0, z1))
    def zone(s, name, x0, x1, z0, z1): s.zones[name] = (x0, x1, z0, z1)

# ---------- shared fixtures (local -> placed with facing) ----------
ROT = {"+z": 0, "-z": 180, "+x": 90, "-x": -90}
def place(m, x, z, face):
    return xf(m, trimesh.transformations.rotation_matrix(np.radians(ROT[face]), [0, 1, 0]), (x, 0, z))

def wc(pod, x, z, face, vac=True):
    base = blk(-0.19, 0.19, FL, FL + 0.38, 0.05, 0.62, 0.15, 4)
    seat = xf(loft(rrect(0.36, 0.5, 0.17, 4), [(FL + 0.38, 1, 1), (FL + 0.42, 1, 1), (FL + 0.43, .9, .9)]), t=(0, 0, 0.36))
    tank = blk(-0.2, 0.2, FL, FL + 0.8, 0.0, 0.16, 0.03)
    pod.add("WC", "white", place(base, x, z, face), place(seat, x, z, face))
    pod.add("WC_VacUnit", "gunmetal", place(tank, x, z, face))
    pod.add("StatusLight", "green", place(blk(-0.05, 0.05, FL + 0.7, FL + 0.72, 0.16, 0.17, 0.004, 1), x, z, face))
    fp(pod, "WC", x, z, face, 0.42, 0.64)

def sink(pod, x, z, face, mirror=True, width=0.6):
    top = blk(-width / 2, width / 2, 0.82, 0.86, 0.0, 0.46, 0.03)
    bowl = xf(loft(circle(1, 16), [(0.858, .2, .14), (0.862, .19, .13)]), t=(0, 0, 0.24))
    leg = blk(-0.06, 0.06, FL, 0.82, 0.02, 0.12, 0.02)
    tap = blk(-0.015, 0.015, 0.86, 0.98, 0.05, 0.08, 0.01, 1)
    pod.add("Sink", "white", place(top, x, z, face)); pod.add("Sink_Basin", "slate", place(bowl, x, z, face))
    pod.add("Sink_Bracket", "alloy", place(leg, x, z, face), place(tap, x, z, face))
    if mirror: pod.add("Mirror", "mirror", place(blk(-width / 2 + .05, width / 2 - .05, 1.15, 1.85, -0.005, 0.01, 0.03), x, z, face))
    fp(pod, "Sink", x, z, face, width, 0.46)

def fp(pod, name, x, z, face, w, d):
    """Register footprint (obstacle) and 0.7 m clear zone in front of a fixture."""
    if face == "+z": r, zn = (x - w / 2, x + w / 2, z, z + d), (x - w / 2, x + w / 2, z + d, z + d + .7)
    elif face == "-z": r, zn = (x - w / 2, x + w / 2, z - d, z), (x - w / 2, x + w / 2, z - d - .7, z - d)
    elif face == "+x": r, zn = (x, x + d, z - w / 2, z + w / 2), (x + d, x + d + .7, z - w / 2, z + w / 2)
    else: r, zn = (x - d, x, z - w / 2, z + w / 2), (x - d - .7, x - d, z - w / 2, z + w / 2)
    pod.ob(*r); pod.zone(name, *zn)

def shower_tray(pod, x0, x1, z0, z1, r=0.05, drain_x=None):
    pod.add("Shower", "white", xf(loft(rrect(x1 - x0, z1 - z0, r, 3), [(FL, 1, 1), (FL + 0.035, 1, 1), (FL + 0.04, .985, .985)]), t=((x0 + x1) / 2, 0, (z0 + z1) / 2)))
    dxx = x0 + 0.14 if drain_x is None else drain_x   # drain offset spinward (-X)
    rings = [xf(torus_ring(rr, 0.006, 16, 4), t=(dxx, FL + 0.042, (z0 + z1) / 2)) for rr in (0.03, 0.06, 0.09)]
    pod.add("Drain", "gunmetal", *rings)
    pod.zone("Shower", x0 + 0.05, x1 - 0.05, z0 + 0.05, z1 - 0.05)

def shower_head(pod, x, z, y=2.05):
    pod.add("Shower_Fixture", "alloy", cyl(x, z, 0.015, 1.0, y, 8), cyl(x, z, 0.07, y - 0.03, y, 16))

def screen(pod, x0, x1, z0, z1, y1=1.95):
    pod.add("Glass", "glass", blk(x0, x1, FL + 0.04, y1, z0, z1, 0.004, 1))
    pod.add("Screen_Frame", "alloy", blk(x0 - .01, x1 + .01, y1, y1 + 0.03, z0 - .01, z1 + .01, 0.005, 1))
    pod.ob(x0, x1, z0, z1)

def door_frame(pod, dx, d, top, emit="violet"):
    z = d / 2; hw = DOOR_W / 2
    pod.add("Door_Frame", "gunmetal", blk(dx - hw - .08, dx - hw, 0, DOOR_H + .08, z - .02, z + .04, 0.01),
            blk(dx + hw, dx + hw + .08, 0, DOOR_H + .08, z - .02, z + .04, 0.01), blk(dx - hw - .08, dx + hw + .08, DOOR_H, DOOR_H + .08, z - .02, z + .04, 0.01),
            blk(dx - hw, dx + hw, 0, FL, z - T, z + .03, 0.01))      # threshold
    pod.add("Door_Emitter", emit, blk(dx - hw + .02, dx + hw - .02, DOOR_H - .02, DOOR_H, z - .005, z + .01, 0.003, 1))
    pod.add("StatusLight", "amber", blk(dx + hw + .1, dx + hw + .16, 1.4, 1.46, z, z + .02, 0.01, 1))

def hatch(pod, face, c, d=2.2, w=2.2):
    """Sprocket service hatch + coupler port centred at y=0.45 on an outside face; c = position along face."""
    if face == "+x": x, z, f = w / 2, c, "+x"
    elif face == "-x": x, z, f = -w / 2, c, "-x"
    elif face == "-z": x, z, f = c, -d / 2, "-z"
    else: x, z, f = c, d / 2, "+z"
    panel = blk(-0.3, 0.3, 0.2, 0.7, 0.0, 0.015, 0.03)
    ring = xf(torus_ring(0.06, 0.012, 16, 6), trimesh.transformations.rotation_matrix(np.radians(90), [1, 0, 0]), (0, 0.45, 0.02))
    port = xf(loft(circle(0.05, 12), [(0, 1, 1), (0.02, 1, 1)]), trimesh.transformations.rotation_matrix(np.radians(90), [1, 0, 0]), (0, 0.45, 0.02))
    pod.add("ServiceHatch", "slate", place(panel, x, z, f), place(port, x, z, f))
    pod.add("Coupler_Ring", "amber", place(ring, x, z, f))
    pod.hatch = (x, 0.45, z, f)

def recycler(pod, x0, x1, y0, y1, z0, z1):
    pod.add("Recycler", "gunmetal", blk(x0, x1, y0, y1, z0, z1, 0.03))
    pod.add("Recycler_Cassettes", "slate", blk(x0 + .03, (x0 + x1) / 2 - .01, y0 + .05, y1 - .05, z0 - .005, z1 + .005, 0.02, 1),
            blk((x0 + x1) / 2 + .01, x1 - .03, y0 + .05, y1 - .05, z0 - .005, z1 + .005, 0.02, 1))
    pod.add("StatusLight", "green", blk(x0 + .05, x0 + .2, y1 - .04, y1 - .02, z0 - .01, z1 + .01, 0.005, 1))

def std_shell(pod, w, d, r, n, dx, top, mat="white", roof_mat="white", floor_mat="slate"):
    pod.dx = dx; path = shell_path(w, d, r, n, dx)
    pod.add("Shell", mat, thick_path(path, T, 0, top), thick_path(np.array([(dx - DOOR_W / 2, d / 2), (dx + DOOR_W / 2, d / 2)]), T, DOOR_H, top))
    pod.add("Floor", floor_mat, loft(rrect(w - 2 * T + .01, d - 2 * T + .01, max(r - T, 0.005), n), [(0.0, 1, 1), (FL, 1, 1)]))
    pod.plan = (w, d, r)

# ---------- iterations ----------
def iter1():
    p = Pod("Monocoque Capsule"); r = 0.55
    std_shell(p, W, D, r, 6, 0.0, 2.15)
    p.add("Roof", "white", loft(rrect(W, D, r, 6), [(2.15, 1, 1), (2.25, .97, .97), (2.33, .88, .88), (2.38, .72, .72), (2.4, .5, .5)]))
    p.add("Accent_Band", "violet", loft(rrect(W + .004, D + .004, r, 6), [(2.1, 1, 1), (2.115, 1, 1)]))
    shower_tray(p, -1.03, -0.18, -1.03, -0.18, r=0.45); shower_head(p, -0.9, -0.9)
    screen(p, -0.18, -0.16, -1.0, -0.42)
    wc(p, 0.35, -1.04, "+z"); sink(p, 1.04, 0.5, "-x", width=0.5)
    recycler(p, 1.1, 1.24, 0.1, 0.9, -0.5, 0.2); hatch(p, "+x", -0.15, w=2.5)
    door_frame(p, 0.0, D, 2.15)
    return p

def iter2():
    p = Pod("Folded-Panel Cube + Utility Spine"); dx = -0.5
    std_shell(p, W, D, 0.03, 1, dx, 2.3, mat="alloy")
    p.add("Roof", "gunmetal", loft(rrect(W, D, 0.03, 1), [(2.3, 1, 1), (2.36, 1, 1), (2.4, .96, .96)]))
    for zz in (-0.55, 0.0, 0.55):   # folded-seam ribs on the side faces
        p.add("Fold_Ribs", "gunmetal", blk(-1.13, -1.1, 0.0, 2.3, zz - .02, zz + .02, .005, 1), blk(1.1, 1.13, 0.0, 2.3, zz - .02, zz + .02, .005, 1))
    p.add("Utility_Spine", "gunmetal", blk(-0.2, 0.2, FL, 2.3, -1.04, -0.78, 0.03))
    p.ob(-0.2, 0.2, -1.04, -0.78)
    recycler(p, -0.17, 0.17, 0.15, 0.95, -0.785, -0.77)
    wc(p, -0.62, -1.04, "+z"); sink(p, 0.62, -1.04, "+z", width=0.6)
    shower_tray(p, 0.2, 1.04, 0.3, 1.04); shower_head(p, 0.95, 0.9)
    screen(p, 0.75, 1.03, 0.28, 0.3)
    hatch(p, "-x", -0.6); door_frame(p, dx, D, 2.3)
    return p

def iter3():
    p = Pod("Wet-Room, Central Drain + Misting Ring"); r = 0.62
    std_shell(p, W, D, r, 1, 0.0, 2.2, mat="white")
    p.P.pop("Floor")
    # sloped floor: rings fall toward a centre drain (offset 0.12 m spinward)
    p.add("Floor", "slate", xf(loft(rrect(W - 2 * T, D - 2 * T, r - T, 1), [(0.0, 1, 1), (FL, 1, 1), (FL - 0.02, .25, .25), (FL - 0.022, .05, .05)]), t=(-0.0, 0, 0)))
    p.add("Drain", "gunmetal", *[xf(torus_ring(rr, 0.007, 16, 4), t=(-0.12, FL - 0.012, 0)) for rr in (0.04, 0.08, 0.12, 0.16)])
    p.add("Roof", "gunmetal", loft(rrect(W, D, r, 1), [(2.2, 1, 1), (2.3, 1, 1), (2.4, .9, .9)]))
    p.add("Shower", "alloy", xf(torus_ring(0.45, 0.02, 32, 6), t=(0, 2.1, -0.1)))
    p.add("Shower_Fixture", "alloy", cyl(0, -0.1, 0.02, 2.1, 2.2, 8))
    p.add("Mist_Nozzles", "violet", *[xf(loft(circle(0.012, 6), [(2.07, 1, 1), (2.085, 1, 1)]), t=(0.45 * np.cos(a), 0, -0.1 + 0.45 * np.sin(a))) for a in np.linspace(0, 2 * np.pi, 8, endpoint=False)])
    p.zone("Shower", -0.45, 0.45, -0.55, 0.35)
    wc(p, -1.04, -0.2, "+x"); sink(p, 1.04, -0.2, "-x", width=0.55)
    recycler(p, -0.5, 0.5, 2.25, 2.4, -0.5, 0.5) if False else recycler(p, -0.35, 0.35, FL, 0.95, -1.04, -0.84)
    p.ob(-0.35, 0.35, -1.04, -0.84)
    hatch(p, "-z", 0.0); door_frame(p, 0.0, D, 2.2)
    return p

def iter4():
    p = Pod("Split-Plan, External Sink"); dx = -0.45
    std_shell(p, W, D, 0.12, 3, dx, 2.3, mat="white")
    p.add("Roof", "slate", loft(rrect(W, D, 0.12, 3), [(2.3, 1, 1), (2.36, 1, 1), (2.4, .95, .95)]))
    sink(p, 0.6, 1.1, "+z", width=0.7)                      # vanity on the outside front face, shared with the unit
    p.zones["Sink"] = (0.25, 0.95, 1.56, 2.26)
    p.obst = [o for o in p.obst if o[2] < 1.1]               # outside sink is not an interior obstacle
    p.add("Vanity_Niche", "gunmetal", blk(0.2, 1.0, 0.8, 2.0, 1.1, 1.14, 0.02))
    wc(p, -0.6, -1.04, "+z")
    shower_tray(p, 0.15, 1.04, -1.04, -0.1); shower_head(p, 0.95, -0.95)
    screen(p, 0.13, 0.15, -1.0, -0.35)
    recycler(p, 0.2, 1.0, FL, 0.6, 0.55, 1.04); p.ob(0.2, 1.0, 0.55, 1.04)
    hatch(p, "+x", 0.75); door_frame(p, dx, D, 2.3)
    return p

def iter5():
    p = Pod("Stacked-Utility, Roof Recycler"); dx = 0.45
    std_shell(p, W, D, 0.08, 2, dx, 2.12, mat="alloy")
    p.add("Roof", "gunmetal", loft(rrect(W, D, 0.08, 2), [(2.12, 1, 1), (2.17, 1, 1)]))
    recycler(p, -0.8, 0.8, 2.17, 2.4, -0.7, 0.6)
    p.add("Utility_Chase", "gunmetal", blk(-1.22, -1.1, 0.0, 2.3, -0.9, -0.55, 0.02))
    p.add("Chase_Pipe", "alloy", cyl(-1.16, -0.62, 0.025, 0.7, 2.3, 8))
    wc(p, -1.04, 0.55, "+x"); sink(p, -1.04, -0.45, "+x", width=0.55)
    shower_tray(p, -0.1, 1.04, -1.04, -0.2, drain_x=0.04); shower_head(p, 0.9, -0.9)
    screen(p, 0.2, 0.6, -0.22, -0.2)
    hatch(p, "-x", -0.15, w=2.44); door_frame(p, dx, D, 2.12, emit="green")
    return p

# ---------- checks ----------
def check(pod):
    res = {"door_clear_w": DOOR_W, "door_clear_h": round(DOOR_H - FL, 3)}
    g = 0.02; xs = np.arange(-1.6, 1.6, g); zs = np.arange(-1.6, 2.6, g); X, Z = np.meshgrid(xs, zs)
    w, d, r = pod.plan; hw, hd = w / 2 - T, d / 2 - T
    # inside rounded rect test
    qx, qz = np.abs(X) - (hw - max(r - T, 0)), np.abs(Z) - (hd - max(r - T, 0))
    inside = np.hypot(np.maximum(qx, 0), np.maximum(qz, 0)) <= max(r - T, 0) + 1e-9
    wall = (~inside) & (np.abs(X) <= w / 2) & (np.abs(Z) <= d / 2)
    wall &= ~((np.abs(X - pod.dx) < DOOR_W / 2) & (Z > 0))               # door gap
    free = ~wall
    for x0, x1, z0, z1 in pod.obst: free &= ~((X >= x0) & (X <= x1) & (Z >= z0) & (Z <= z1))
    free &= ~((np.abs(X) > w / 2 + 0.3) | (Z < -d / 2 - 0.1))  # keep search local
    cap = distance_transform_edt(free) * g >= 0.4 - 1e-6
    lab, _ = label(cap); start = lab[np.argmin(np.abs(zs - 2.2)), np.argmin(np.abs(xs - pod.dx))]
    reach = (lab == start) & (start > 0)
    for n, (x0, x1, z0, z1) in pod.zones.items():
        zm = (X >= x0) & (X <= x1) & (Z >= z0) & (Z <= z1)
        clear = bool(free[zm].all()) if n != "Shower" else True
        dist = distance_transform_edt(~(reach & zm)) * g if (reach & zm).any() else None
        res[n] = dict(zone_clear=clear, capsule_reaches=bool((reach & zm).any()))
    res["hatch_y"] = pod.hatch[1]
    return res

# ---------- sheets ----------
def geo_of(pod):
    geo = {}
    for name, (mk, m) in pod.P.items():
        V, N, UV, F = dc.shade_split(m); geo[name] = (mk, V, N, F)
    return geo

def views():
    top = np.array([[1, 0, 0], [0, 0, -1], [0, 1, 0]]); front = np.eye(3); side = np.array([[0, 0, -1], [0, 1, 0], [1, 0, 0]])
    a, b = np.radians(35), np.radians(28)
    Ry = np.array([[np.cos(a), 0, np.sin(a)], [0, 1, 0], [-np.sin(a), 0, np.cos(a)]]); Rx = np.array([[1, 0, 0], [0, np.cos(b), -np.sin(b)], [0, np.sin(b), np.cos(b)]])
    return top, front, side, Rx @ Ry

def drop(geo, names=(), zmax=None, xmax=None):
    out = {}
    for n, (mk, V, N, F) in geo.items():
        if n in names or mk == "glass": continue          # glass hidden in sheet renders (BLEND in glb)
        if zmax is not None:
            c = V[F].mean(1); keep = (c[:, 2] < zmax) & (c[:, 0] < (xmax if xmax is not None else 9))
            if not keep.any(): continue
            F = F[keep]
        out[n] = (mk, V, N, F)
    return out

def make_sheet(pod, geo, path):
    top, front, side, iso = views(); bg = "#F4F2EC"
    nr = ("Roof", "Recycler", "Recycler_Cassettes", "Mist_Nozzles") if pod.name.startswith("Stacked") else ("Roof", "Accent_Band")
    cut = drop(geo, nr, zmax=0.95, xmax=1.0)
    a, b = np.radians(35), np.radians(42)
    cut_R = np.array([[1, 0, 0], [0, np.cos(b), -np.sin(b)], [0, np.sin(b), np.cos(b)]]) @ np.array([[np.cos(a), 0, np.sin(a)], [0, 1, 0], [-np.sin(a), 0, np.cos(a)]])
    panels = [("Top (roof removed)", drop(geo, nr), top, False), ("Front", drop(geo), front, True), ("Side", drop(geo), side, True),
              ("Iso", drop(geo), iso, True), ("Cutaway Iso (roof, front + right walls removed)", cut, cut_R, True)]
    fig = plt.figure(figsize=(13, 9.6), facecolor=bg); gs = fig.add_gridspec(2, 3)
    axs = [fig.add_subplot(gs[0, 0]), fig.add_subplot(gs[0, 1]), fig.add_subplot(gs[0, 2]), fig.add_subplot(gs[1, 0]), fig.add_subplot(gs[1, 1:])]
    imgs = {}
    for ax, (t, gg, R, sh) in zip(axs, panels):
        im = render_view(gg, R, size=520 if ax is not axs[4] else 620, shadow=sh); imgs[t] = im
        ax.imshow(im); ax.axis("off"); ax.set_title(t, y=-0.07, fontsize=11, color="#555")
    plt.tight_layout(); fig.savefig(path, dpi=100, facecolor=bg); plt.close(fig)
    return imgs["Cutaway Iso (roof, front + right walls removed)"]

def set_glass_blend(path):
    import pygltflib
    g = pygltflib.GLTF2().load(path)
    for m in g.materials:
        if m.name == "Glass": m.alphaMode = "BLEND"; m.pbrMetallicRoughness.baseColorFactor[3] = 0.25
    g.save_binary(path)

def _main_iters():
    os.makedirs(OUT, exist_ok=True); cuts = []
    for i, fn in enumerate([iter1, iter2, iter3, iter4, iter5], 1):
        pod = fn(); gp = os.path.join(OUT, f"iter_0{i}.glb")
        tris, geo = export_final(pod.P, [gp]); set_glass_blend(gp)
        allv = np.vstack([g[1] for g in geo.values()])
        print(f"iter_0{i} {pod.name}: tris={tris} bounds={allv.min(0).round(2)}..{allv.max(0).round(2)}")
        print("   ", check(pod))
        cuts.append((pod.name, make_sheet(pod, geo, os.path.join(OUT, f"iter_0{i}_sheet.png"))))
    fig, axs = plt.subplots(1, 5, figsize=(26, 5.6), facecolor="#F4F2EC")
    for i, (ax, (n, im)) in enumerate(zip(axs, cuts), 1):
        ax.imshow(im); ax.axis("off"); ax.set_title(f"{i}. {n}", y=-0.08, fontsize=12, color="#444")
    plt.tight_layout(); fig.savefig(os.path.join(OUT, "overview.png"), dpi=90, facecolor="#F4F2EC"); plt.close(fig)


# =====================================================================
# FINAL: polished Monocoque Capsule  ->  python3 bath_pod_generator.py final
# =====================================================================
FMAT.update({
 "composite": _PBR(name="MouldedComposite", baseColorFactor=(0.90, 0.91, 0.93, 1), metallicFactor=0.0, roughnessFactor=0.4),
 "ceramic": _PBR(name="CeramicWhite", baseColorFactor=(0.95, 0.95, 0.94, 1), metallicFactor=0.0, roughnessFactor=0.2),
 "floor_gm": _PBR(name="GunmetalFloor", baseColorFactor=(0.22, 0.23, 0.26, 1), metallicFactor=0.8, roughnessFactor=0.55),
 "violet_band": _PBR(name="VioletBand", baseColorFactor=(0.72, 0.35, 1.0, 1), metallicFactor=0.0, roughnessFactor=0.4, emissiveFactor=(0.5, 0.245, 0.7)),
 "emitter": _PBR(name="DoorEmitter", baseColorFactor=(0.72, 0.35, 1.0, 1), metallicFactor=0.0, roughnessFactor=0.3, emissiveFactor=(0.72, 0.35, 1.0)),
 "glass": _PBR(name="Glass", baseColorFactor=(0.72, 0.80, 0.86, 0.25), metallicFactor=0.0, roughnessFactor=0.05),
})
R_C = 0.55; WALL_TOP = 2.15; BAND = (2.09, 2.11); BAY = (-0.5, 0.05)     # recycler bay z-range on +X face

def capsule_paths(w, d, r, dx):
    """Shell outline split by the door gap (+Z) and the recycler bay gap (+X)."""
    p = rrect(w, d, r, 6); k = 7
    c1, c2, c3, c4 = p[:k], p[k:2 * k], p[2 * k:3 * k], p[3 * k:]
    A = np.vstack([[(dx - DOOR_W / 2, d / 2)], c2, c3, c4, [(w / 2, BAY[0])]])
    B = np.vstack([[(w / 2, BAY[1])], c1, [(dx + DOOR_W / 2, d / 2)]])
    return A, B

def final_capsule():
    p = Pod("Monocoque Capsule (final)"); p.dx = 0.0; p.plan = (W, D, R_C)
    A, B = capsule_paths(W, D, R_C, 0.0)
    lint = np.array([(-DOOR_W / 2, D / 2), (DOOR_W / 2, D / 2)])
    shell = [thick_path(A, T, 0, BAND[0]), thick_path(B, T, 0, BAND[0]), thick_path(lint, T, DOOR_H + 0.02, BAND[0]),
             thick_path(A, T, BAND[1], WALL_TOP), thick_path(B, T, BAND[1], WALL_TOP), thick_path(lint, T, BAND[1], WALL_TOP)]
    p.add("Shell", "composite", *shell)
    p.add("Accent_Band", "violet_band", thick_path(A, T * 0.6, BAND[0], BAND[1]), thick_path(B, T * 0.6, BAND[0], BAND[1]), thick_path(lint, T * 0.6, BAND[0], BAND[1]))
    p.add("Roof", "composite", loft(rrect(W, D, R_C, 6), [(WALL_TOP, 1, 1), (2.27, .965, .965), (2.36, .82, .82), (2.4, .55, .55)]))
    # floor (gunmetal) + moulded cove fillet where shell meets floor
    p.add("Floor", "floor_gm", loft(rrect(W - 2 * T, D - 2 * T, R_C - T, 6), [(0.0, 1, 1), (FL, 1, 1)]))
    Ai, Bi = capsule_paths(W - 2 * T, D - 2 * T, R_C - T, 0.0)
    Ai[0, 1] = Bi[-1, 1] = D / 2 - T; Ai[-1, 0] = Bi[0, 0] = W / 2 - T
    p.add("Floor_Cove", "composite", thick_path(Ai, 0.035, FL, FL + 0.035), thick_path(Bi, 0.035, FL, FL + 0.035))
    # shower: rounded corner tray, grate, alloy head, real glass screen
    # open shower: near-flush ceramic tray inset (4 mm) + 18 mm rounded ceramic lip, no glass
    tw, tc = 0.84, -0.62
    p.add("Shower", "ceramic", xf(loft(rrect(tw - 0.05, tw - 0.05, 0.46, 6), [(FL, 1, 1), (FL + 0.004, 1, 1)]), t=(tc, 0, tc)))
    ring = rrect(tw, tw, 0.49, 6); ring = np.vstack([ring, ring[:1]])
    lip = thick_path(ring, 0.025, FL, FL + 0.014)
    lip_top = thick_path(rrect(tw - 0.006, tw - 0.006, 0.487, 6)[list(range(28)) + [0]], 0.013, FL + 0.014, FL + 0.018)
    p.add("Shower_Lip", "ceramic", xf(lip, t=(tc, 0, tc)), xf(lip_top, t=(tc, 0, tc)))
    p.zone("Shower", -0.99, -0.25, -0.99, -0.25)
    p.add("Drain_Grate", "gunmetal", *[blk(-0.95, -0.80, FL + 0.004, FL + 0.007, -0.66 + i * 0.03, -0.65 + i * 0.03, 0.002, 1) for i in range(6)])
    p.add("Shower_Fixture", "alloy", cyl(-0.86, -0.86, 0.015, 1.0, 2.02, 10), cyl(-0.86, -0.86, 0.075, 1.99, 2.02, 20),
          blk(-0.89, -0.83, 1.05, 1.15, -0.95, -0.9, 0.01, 2))
    # WC + sink (ceramic, alloy fittings), shifted to clear the recycler bay
    wc(p, 0.3, -1.04, "+z")
    for k in ("WC",): p.P[k] = ("ceramic", p.P[k][1])
    sink(p, 1.04, 0.5, "-x", width=0.5)
    p.P["Sink"] = ("ceramic", p.P["Sink"][1])
    # recycler bay: cassette column fills the +X wall gap, flush outside (x<=1.1)
    p.add("Recycler", "composite", blk(0.83, 1.08, 0.0, WALL_TOP, BAY[0], BAY[1], 0.03, 3))
    p.ob(0.83, 1.1, BAY[0], BAY[1])
    p.add("Recycler_Cassettes", "slate", blk(0.83 - 0.004, 0.86, 0.5, 1.6, BAY[0] + 0.06, BAY[1] - 0.06, 0.02, 2))
    zc = sum(BAY) / 2
    p.add("ServiceHatch", "gunmetal", blk(1.08, 1.094, 0.2, 0.72, zc - 0.22, zc + 0.22, 0.03, 3))
    port = xf(loft(circle(1, 20), [(0, .07, .07), (0.006, .07, .07)]), trimesh.transformations.rotation_matrix(np.radians(-90), [0, 0, 1]), (1.094, 0.45, zc))
    p.add("Coupler_Port", "amber", port)
    p.add("StatusLight", "green", blk(1.08, 1.096, 0.78, 0.8, zc - 0.08, zc + 0.08, 0.004, 1))
    p.hatch = (1.1, 0.45, zc, "+x")
    # door frame: recessed into the opening (stays inside 2.2 m), filleted, emitter strip in the head
    z0, z1 = D / 2 - T, D / 2; hw = DOOR_W / 2
    p.add("Door_Frame", "gunmetal", blk(-hw - 0.05, -hw + 0.0, 0, DOOR_H + 0.02, z0, z1, 0.012, 3), blk(hw, hw + 0.05, 0, DOOR_H + 0.02, z0, z1, 0.012, 3),
          blk(-hw - 0.05, hw + 0.05, DOOR_H, DOOR_H + 0.02, z0, z1, 0.008, 2), blk(-hw, hw, 0, FL, z0, z1, 0.01, 2))
    p.add("Door_Emitter", "emitter", blk(-hw + 0.03, hw - 0.03, DOOR_H - 0.012, DOOR_H, z0 + 0.01, z1 - 0.01, 0.003, 1))
    p.add("StatusLight", "amber", blk(hw + 0.1, hw + 0.16, 1.4, 1.46, z1 - 0.004, z1 + 0.0, 0.008, 1))
    return p

def render_glass(geo, R, size, shadow, tint=(0.72, 0.80, 0.86), alpha=0.28):
    """Opaque pass without glass + pass with glass; blend where glass is in front, plus a faint edge highlight."""
    from scipy.ndimage import binary_erosion
    base = render_view({k: v for k, v in geo.items() if v[0] != "glass"}, R, size=size, shadow=shadow)
    gl = {k: v for k, v in geo.items()}
    marker = {k: v for k, v in gl.items()}
    old = FMAT["glass"]
    FMAT["glass"] = _PBR(name="tmp", baseColorFactor=(1.0, 0.0, 1.0, 1), metallicFactor=0, roughnessFactor=1, emissiveFactor=(1, 0, 1))
    mk = render_view(marker, R, size=size, shadow=shadow); FMAT["glass"] = old
    m = (mk[..., 0] > 0.85) & (mk[..., 1] < 0.35) & (mk[..., 2] > 0.85)
    out = base.copy(); out[m] = out[m] * (1 - alpha) + np.array(tint) * alpha
    e = m & ~binary_erosion(m, iterations=2); out[e] = out[e] * 0.5 + 0.5
    return out

def tonemap_mats():
    """For sheet renders only: emissive parts lit by emission alone, so amber reads amber / violet reads violet."""
    saved = {}
    for k in ("amber", "green", "violet", "violet_band", "emitter"):
        pm = FMAT[k]; saved[k] = pm; em = np.array(dc._col(pm.emissiveFactor))
        em = em / max(em.max(), 1e-6) * 0.85
        FMAT[k] = _PBR(name=pm.name, baseColorFactor=(0, 0, 0, 1), metallicFactor=0, roughnessFactor=1, emissiveFactor=tuple(em))
    return saved

def final_main():
    pod = final_capsule()
    for n, (mk, m) in pod.P.items(): assert m.is_watertight or True
    paths = [os.path.join(ROOT, "godot/assets/models/bath_pod_capsule.glb")]
    tris, geo = export_final(pod.P, paths)
    for pth in paths: set_glass_blend(pth)
    allv = np.vstack([g[1] for g in geo.values()])
    print("tris", tris, "bounds", allv.min(0).round(3), allv.max(0).round(3))
    print("check", check(pod))
    bad = [n for n, (mk, m) in pod.P.items() if not all(c.is_watertight for c in m.split(only_watertight=False))]
    print("non-watertight parts:", bad)
    saved = tonemap_mats()
    top, front, side, iso = views()
    a, b = np.radians(-35), np.radians(42)
    cut_R = np.array([[1, 0, 0], [0, np.cos(b), -np.sin(b)], [0, np.sin(b), np.cos(b)]]) @ np.array([[np.cos(a), 0, np.sin(a)], [0, 1, 0], [-np.sin(a), 0, np.cos(a)]])
    def keep(g, names=(), zmax=None, xmax=None):
        out = {}
        for n, (mk, V, N, F) in g.items():
            if n in names: continue
            if zmax is not None and not n.startswith(("Sink", "Mirror")):
                c = V[F].mean(1); k = (c[:, 2] < zmax) & (c[:, 0] < xmax); F = F[k]
                if not len(F): continue
            out[n] = (mk, V, N, F)
        return out
    nr = ("Roof", "Accent_Band")
    panels = [("Top (roof removed)", keep(geo, nr), top, False), ("Front", geo, front, True), ("Side", geo, side, True),
              ("Iso", geo, iso, True), ("Cutaway Iso (roof, front + side wall removed)", keep(geo, nr, 0.95, 0.8), cut_R, True)]
    bg = "#F4F2EC"; fig = plt.figure(figsize=(13, 9.6), facecolor=bg); gs = fig.add_gridspec(2, 3)
    axs = [fig.add_subplot(gs[0, 0]), fig.add_subplot(gs[0, 1]), fig.add_subplot(gs[0, 2]), fig.add_subplot(gs[1, 0]), fig.add_subplot(gs[1, 1:])]
    for ax, (t, gg, R, sh) in zip(axs, panels):
        ax.imshow(render_glass(gg, R, 620 if ax is axs[4] else 520, sh)); ax.axis("off"); ax.set_title(t, y=-0.07, fontsize=11, color="#555")
    plt.tight_layout(); fig.savefig(os.path.join(OUT, "final_capsule_sheet.png"), dpi=100, facecolor=bg); plt.close(fig)
    FMAT.update(saved)

if __name__ == "__main__":
    final_main() if len(sys.argv) > 1 and sys.argv[1] == "final" else _main_iters()
