"""temp-Active batch 5 (scratch, outside repo): lead-wall route overlays.
Owned tt_climb_lead_routes_* hold-set GLBs. Do NOT edit shared tt_climbing_panel.

FACE_PLANE: wall face at local z=0; holds and tape toward +Z; hold backs embed 8 mm (z=-0.008).
Width 2.50 m (two 1.25 m panel columns), height 11.50 m, max hold proud 0.35 m.
Place yaw 180 so local +Z maps to world -Z (into the lead hall). Pass raw Z = 8.0 (the face);
put() applies raw_pivot so the face lands on world Z 8, backs at Z 8.008 (8 mm embed).
8 colour-coded vertical routes (4 layouts, 4 mirrored) with panel-grid variation and route tape
that spans both columns and all 5 courses. No wood. No planter boxes. Alpha-scissor / opaque only.
"""
import os, sys, json
sys.dont_write_bytecode = True
sys.path.insert(0, "/workspace/game-project/assets/src/tennis_tower")
sys.path.insert(0, "/workspace/game-project/assets/src/tennis_tower/structure")
import modlib as ML
from modlib import *
import struct_lib as SLB
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
ML.GLB_OUT = str(HERE / "glb")
ML.RENDER_OUT = "/workspace/renders/tennis_tower/rooms/temp-Active"
ML._m("tt_hold_yellow", "TT_HoldYellow", (.78, .70, .16), 0, .72)
ML._m("tt_hold_cyan",   "TT_HoldCyan",   (.12, .55, .62), 0, .72)
ML._m("tt_hold_amber",  "TT_HoldAmber",  (.78, .46, .10), 0, .72)
ML._m("tt_hold_green",  "TT_HoldGreen",  (.22, .52, .28), 0, .72)
ML._m("tt_hold_violet", "TT_HoldViolet", (.42, .24, .62), 0, .72)
ML._m("tt_hold_teal",   "TT_HoldTeal",   (.08, .42, .44), 0, .72)
ML._m("tt_hold_red",    "TT_HoldRed",    (.66, .18, .16), 0, .72)
ML._m("tt_hold_blue",   "TT_HoldBlue",   (.18, .30, .62), 0, .72)
ML._m("tt_panel_a", "TT_LeadPanelA", (.26, .30, .36), 0, .68)
ML._m("tt_panel_b", "TT_LeadPanelB", (.22, .24, .28), 0, .70)
ML._m("tt_panel_c", "TT_LeadPanelC", (.30, .32, .30), 0, .66)
ML._m("tt_panel_d", "TT_LeadPanelD", (.24, .28, .34), 0, .70)
HY, HC, HA, HG = "tt_hold_yellow", "tt_hold_cyan", "tt_hold_amber", "tt_hold_green"
HV, HT, HR, HB = "tt_hold_violet", "tt_hold_teal", "tt_hold_red", "tt_hold_blue"
PA, PB, PC, PD = "tt_panel_a", "tt_panel_b", "tt_panel_c", "tt_panel_d"

def U(m):
    m.metadata["uv"] = np.zeros((len(m.vertices), 2)); return m

def hull(pts):
    return U(trimesh.convex.convex_hull(np.asarray(pts, float)))

def col(p, name, lo, hi):
    p.add(name + "-convcolonly", G, U(trimesh.creation.box(bounds=[lo, hi])))

W, H = 2.50, 11.50
Z_BACK, Z_MAX = -0.008, 0.350
COURSES = (0.0, 2.3, 4.6, 6.9, 9.2, 11.5)


def hold_mesh(x, y, kind, s, seed):
    """Organic convex hold, characteristic size s (m), back at Z_BACK, proud toward +Z."""
    rng = np.random.default_rng(seed)
    pts = [(x, y, Z_BACK)]
    if kind == "volume":
        # Faceted composite volume: s is width; height 0.72 s; proud locked to Z_MAX.
        hw, hh, hz = s * 0.50, s * 0.36, Z_MAX
        bevel = 0.06 * s
        for sx in (-1, 1):
            for sy in (-1, 1):
                pts += [
                    (x + sx * (hw - bevel), y + sy * hh, Z_BACK + 0.01),
                    (x + sx * hw, y + sy * (hh - bevel), Z_BACK + 0.01),
                    (x + sx * (hw - bevel), y + sy * (hh - bevel), hz),
                    (x + sx * hw * 0.70, y + sy * hh * 0.70, hz),
                ]
        # slight top rake so it reads as a volume, not a box
        pts.append((x, y + hh * 0.15, hz * 0.92))
        return hull(pts)
    if kind == "jug":
        rx, ry, rz = s * 0.50, s * 0.42, min(Z_MAX, s * 0.70)
        n = 10
        for i in range(n):
            a = 2 * np.pi * i / n
            jx, jy = float(rng.uniform(0.86, 1.08)), float(rng.uniform(0.78, 1.00))
            pts.append((x + np.cos(a) * rx * jx, y + np.sin(a) * ry * jy, Z_BACK + 0.012))
            # mid lip (fatter) then front (slightly tighter = incut read on a convex hull)
            pts.append((x + np.cos(a) * rx * 1.08 * jx, y + np.sin(a) * ry * 0.95 * jy, rz * 0.55))
            pts.append((x + np.cos(a) * rx * 0.88 * jx, y + np.sin(a) * ry * 0.80 * jy, rz))
        return hull(pts)
    if kind == "crimp":
        rx, ry, rz = s * 0.50, s * 0.22, min(Z_MAX, s * 0.45)
        n = 8
        for i in range(n):
            a = 2 * np.pi * i / n
            j = float(rng.uniform(0.90, 1.06))
            pts.append((x + np.cos(a) * rx * j, y + np.sin(a) * ry * j, Z_BACK + 0.006))
            pts.append((x + np.cos(a) * rx * 0.95 * j, y + np.sin(a) * ry * 0.85, rz))
        return hull(pts)
    if kind == "sloper":
        rx, ry, rz = s * 0.52, s * 0.48, min(Z_MAX, s * 0.48)
        n = 10
        for i in range(n):
            a = 2 * np.pi * i / n
            j = float(rng.uniform(0.88, 1.06))
            pts.append((x + np.cos(a) * rx * j, y + np.sin(a) * ry * j, Z_BACK + 0.008))
            pts.append((x + np.cos(a) * rx * 0.70 * j, y + np.sin(a) * ry * 0.70 * j, rz))
        pts.append((x, y + ry * 0.15, rz * 0.85))
        return hull(pts)
    if kind == "pinch":
        rx, ry, rz = s * 0.26, s * 0.60, min(Z_MAX, s * 0.62)
        n = 8
        for i in range(n):
            a = 2 * np.pi * i / n
            j = float(rng.uniform(0.90, 1.08))
            pts.append((x + np.cos(a) * rx * j, y + np.sin(a) * ry * j, Z_BACK + 0.010))
            pts.append((x + np.cos(a) * rx * 0.85 * j, y + np.sin(a) * ry * 0.90 * j, rz))
        return hull(pts)
    raise ValueError(kind)


def hold_front_z(kind, s):
    if kind == "volume":
        return Z_MAX
    if kind == "jug":
        return min(Z_MAX, s * 0.70)
    if kind == "crimp":
        return min(Z_MAX, s * 0.45)
    if kind == "sloper":
        return min(Z_MAX, s * 0.48)
    if kind == "pinch":
        return min(Z_MAX, s * 0.62)
    return 0.12


# Four authored layouts: (x, y, kind, size). x in a 2.5 m bay, inset from the 1.25 m mullions.
# One volume per layout, proud to Z_MAX so every GLB shares the same z envelope after recenter.
LAYOUTS = {
    "a": [  # left-leaning jug line, volume low-mid left
        (-0.58, 0.42, "jug", 0.18), (0.52, 0.62, "crimp", 0.09),
        (-0.22, 1.00, "pinch", 0.13), (0.62, 1.38, "jug", 0.16),
        (-0.68, 1.78, "sloper", 0.24), (0.28, 2.18, "crimp", 0.08),
        (-0.40, 2.62, "jug", 0.20), (0.70, 3.05, "pinch", 0.14),
        (-0.62, 3.70, "volume", 0.70), (0.48, 4.20, "crimp", 0.10),
        (-0.18, 4.62, "jug", 0.17), (0.66, 5.05, "sloper", 0.22),
        (-0.72, 5.48, "pinch", 0.15), (0.22, 5.95, "jug", 0.18),
        (-0.48, 6.42, "crimp", 0.09), (0.58, 6.88, "jug", 0.16),
        (-0.28, 7.35, "sloper", 0.26), (0.70, 7.82, "pinch", 0.12),
        (-0.64, 8.28, "jug", 0.19), (0.32, 8.75, "crimp", 0.08),
        (-0.16, 9.22, "pinch", 0.13), (0.60, 9.68, "jug", 0.17),
        (-0.70, 10.12, "sloper", 0.22), (0.24, 10.55, "crimp", 0.09),
        (-0.42, 11.02, "jug", 0.16),
    ],
    "b": [  # right-leaning crimpy line, volume mid right
        (0.58, 0.40, "crimp", 0.09), (-0.50, 0.68, "jug", 0.16),
        (0.22, 1.08, "pinch", 0.12), (-0.66, 1.48, "crimp", 0.08),
        (0.70, 1.90, "sloper", 0.22), (-0.28, 2.32, "jug", 0.18),
        (0.44, 2.78, "crimp", 0.10), (-0.70, 3.22, "pinch", 0.14),
        (0.18, 3.68, "jug", 0.17), (-0.42, 4.15, "sloper", 0.24),
        (0.66, 4.62, "crimp", 0.09), (-0.20, 5.08, "jug", 0.16),
        (0.62, 5.70, "volume", 0.64), (-0.60, 6.28, "pinch", 0.13),
        (0.30, 6.72, "crimp", 0.08), (-0.48, 7.18, "jug", 0.19),
        (0.70, 7.64, "sloper", 0.26), (-0.22, 8.10, "crimp", 0.09),
        (0.50, 8.56, "pinch", 0.14), (-0.68, 9.02, "jug", 0.17),
        (0.18, 9.48, "sloper", 0.22), (-0.40, 9.95, "crimp", 0.10),
        (0.62, 10.40, "jug", 0.16), (-0.28, 10.88, "pinch", 0.12),
        (0.42, 11.08, "crimp", 0.08),
    ],
    "c": [  # central juggy line, volume mid-left
        (0.08, 0.44, "jug", 0.20), (-0.62, 0.72, "crimp", 0.09),
        (0.66, 1.10, "sloper", 0.22), (-0.30, 1.52, "jug", 0.17),
        (0.48, 1.98, "pinch", 0.13), (-0.70, 2.42, "jug", 0.18),
        (0.22, 2.88, "crimp", 0.08), (-0.48, 3.35, "sloper", 0.24),
        (0.70, 3.82, "jug", 0.16), (-0.16, 4.28, "pinch", 0.14),
        (0.52, 4.75, "crimp", 0.09), (-0.66, 5.35, "volume", 0.78),
        (0.30, 5.95, "jug", 0.19), (-0.42, 6.42, "crimp", 0.10),
        (0.68, 6.88, "sloper", 0.26), (-0.22, 7.35, "jug", 0.17),
        (0.48, 7.82, "pinch", 0.13), (-0.68, 8.28, "crimp", 0.09),
        (0.18, 8.75, "jug", 0.18), (-0.50, 9.22, "sloper", 0.22),
        (0.66, 9.68, "pinch", 0.12), (-0.28, 10.12, "jug", 0.16),
        (0.42, 10.58, "crimp", 0.08), (-0.62, 11.00, "jug", 0.17),
    ],
    "d": [  # wide-move line, volume high right
        (-0.70, 0.42, "sloper", 0.26), (0.66, 0.70, "jug", 0.16),
        (-0.22, 1.15, "crimp", 0.09), (0.48, 1.60, "pinch", 0.14),
        (-0.62, 2.08, "jug", 0.19), (0.22, 2.55, "sloper", 0.24),
        (-0.40, 3.02, "crimp", 0.08), (0.70, 3.50, "jug", 0.17),
        (-0.18, 3.98, "pinch", 0.13), (0.52, 4.46, "crimp", 0.10),
        (-0.68, 4.95, "jug", 0.18), (0.28, 5.42, "sloper", 0.22),
        (-0.50, 5.90, "pinch", 0.15), (0.68, 6.38, "jug", 0.16),
        (-0.26, 6.86, "crimp", 0.09), (0.44, 7.35, "sloper", 0.26),
        (-0.70, 7.84, "jug", 0.19), (0.18, 8.32, "pinch", 0.12),
        (0.62, 8.95, "volume", 0.66), (-0.48, 9.55, "crimp", 0.08),
        (0.30, 10.00, "jug", 0.17), (-0.66, 10.45, "sloper", 0.22),
        (0.55, 10.90, "pinch", 0.13), (-0.20, 11.08, "jug", 0.16),
    ],
}


def tape_segments(holds, gap=0.10, w=0.028, z0=0.008, z1=0.012):
    """Route tape between consecutive holds, gapped so it does not meet the hold bodies."""
    segs = []
    for (x0, y0, k0, s0), (x1, y1, k1, s1) in zip(holds, holds[1:]):
        dx, dy = x1 - x0, y1 - y0
        L = float(np.hypot(dx, dy))
        if L < 0.20:
            continue
        ux, uy = dx / L, dy / L
        g0 = s0 * 0.55 + gap
        g1 = s1 * 0.55 + gap
        if g0 + g1 >= L - 0.08:
            continue
        ax, ay = x0 + ux * g0, y0 + uy * g0
        bx, by = x1 - ux * g1, y1 - uy * g1
        # thin box in XY along the segment, extruded in Z
        mx, my = (ax + bx) / 2, (ay + by) / 2
        length = float(np.hypot(bx - ax, by - ay))
        ang = float(np.arctan2(uy, ux))
        m = box(-length / 2, length / 2, -w / 2, w / 2, z0, z1)
        R = trimesh.transformations.rotation_matrix(ang, [0, 0, 1])
        m = xf(m, R=R, t=(mx, my, 0))
        segs.append(U(m))
    return segs


def panel_grid(mat_l, mat_r):
    """Perimeter/course mullions for the two 1.25 m columns (tile-repeat breakup). 4 mm proud of the face."""
    t, z0, z1 = 0.036, 0.002, 0.006
    verts = []  # shared gunmetal verticals, flush to the 2.50 m envelope
    left, right = [], []
    # outer verticals sit inside the 2.50 m bay so adjacent route GLBs do not overlap
    verts.append(box(-W / 2, -W / 2 + t, 0.02, H - 0.02, z0, z1))
    verts.append(box(-t / 2, t / 2, 0.02, H - 0.02, z0, z1))
    verts.append(box(W / 2 - t, W / 2, 0.02, H - 0.02, z0, z1))
    # horizontals per course, split left/right of the mid mullion (2 mm gap from verticals)
    g = 0.002
    for y in COURSES:
        y0, y1 = y - t / 2, y + t / 2
        if y == 0.0:
            y0, y1 = 0.0, t
        if y == H:
            y0, y1 = H - t, H
        left.append(box(-W / 2 + t + g, -t / 2 - g, y0, y1, z0, z1))
        right.append(box(t / 2 + g, W / 2 - t - g, y0, y1, z0, z1))
    return verts, left, right, mat_l, mat_r


def hold_half(kind, s):
    if kind == "volume":
        return s * 0.50 + 0.01, s * 0.36 + 0.01
    if kind == "jug":
        return s * 0.54, s * 0.42
    if kind == "crimp":
        return s * 0.52, s * 0.24
    if kind == "sloper":
        return s * 0.54, s * 0.50
    if kind == "pinch":
        return s * 0.28, s * 0.62
    return s * 0.50, s * 0.50


def clear_grid(x, y, kind, s, margin=0.014):
    """Nudge a hold off the 1.25 m mullions and 2.3 m course rails (A1)."""
    hx, hy = hold_half(kind, s)
    t = 0.036
    for mx in (-W / 2, 0.0, W / 2):
        # distance from hold to mullion centre-line
        if abs(x - mx) < hx + t / 2 + margin:
            side = 1.0 if x >= mx else -1.0
            # if exactly on the line, push toward bay centre
            if abs(x - mx) < 1e-6:
                side = -1.0 if mx > 0 else 1.0
            x = mx + side * (hx + t / 2 + margin)
    for c in COURSES:
        band = hy + t / 2 + margin
        if abs(y - c) < band:
            side = 1.0 if y >= c else -1.0
            if abs(y - c) < 1e-6:
                side = 1.0 if c < H / 2 else -1.0
            y = c + side * band
    # keep inside the bay and above the floor / below the cap
    hx, hy = hold_half(kind, s)
    x = float(np.clip(x, -W / 2 + hx + t + 0.01, W / 2 - hx - t - 0.01))
    y = float(np.clip(y, hy + 0.02, H - hy - 0.02))
    return x, y


def routes(q):
    layout = LAYOUTS[q["layout"]]
    if q.get("mirror"):
        layout = [(-x, y, k, s) for (x, y, k, s) in layout]
    layout = [(*clear_grid(x, y, k, s), k, s) for (x, y, k, s) in layout]
    seed0 = int(q.get("seed", 1))
    p = Part()
    holds = []
    bolts = []
    for i, (x, y, k, s) in enumerate(layout):
        holds.append(hold_mesh(x, y, k, s, seed0 * 40 + i))
        fz = hold_front_z(k, s)
        bolts.append(tube((x, y, fz - 0.014), (x, y, fz + 0.006), 0.007, 6))
    p.add("Holds_PU", q["hold"], *holds)
    tape = tape_segments(layout)
    if tape:
        p.add("Route_Tape", q["hold"], *tape)
    verts, left, right, mat_l, mat_r = panel_grid(q["frame_l"], q["frame_r"])
    p.add("Grid_Mullion", G, *verts)
    p.add("Grid_Course_L", mat_l, *left)
    p.add("Grid_Course_R", mat_r, *right)
    p.add("Bolts_Hardware", ST, *bolts)
    # Thin face-plane collider only (the shared panel already owns the wall). Do not fill the 0.35 m hold depth.
    col(p, "LeadRoutes", (-W / 2, 0.0, Z_BACK), (W / 2, H, 0.012))
    return p


# 8 routes, 4 layouts x 2 (mirrored). Distinct hold colours. Alternating panel-grid tints.
SETS = {
    "tt_climb_lead_routes_a": (routes, [dict(label="Route A yellow, layout a", layout="a", hold=HY, frame_l=PA, frame_r=PB, seed=11)]),
    "tt_climb_lead_routes_b": (routes, [dict(label="Route B cyan, layout b", layout="b", hold=HC, frame_l=PC, frame_r=PD, seed=21)]),
    "tt_climb_lead_routes_c": (routes, [dict(label="Route C amber, layout c", layout="c", hold=HA, frame_l=PB, frame_r=PC, seed=31)]),
    "tt_climb_lead_routes_d": (routes, [dict(label="Route D green, layout d", layout="d", hold=HG, frame_l=PD, frame_r=PA, seed=41)]),
    "tt_climb_lead_routes_e": (routes, [dict(label="Route E violet, layout a mirrored", layout="a", hold=HV, frame_l=PC, frame_r=PA, seed=12, mirror=True)]),
    "tt_climb_lead_routes_f": (routes, [dict(label="Route F teal, layout b mirrored", layout="b", hold=HT, frame_l=PD, frame_r=PB, seed=22, mirror=True)]),
    "tt_climb_lead_routes_g": (routes, [dict(label="Route G red, layout c mirrored", layout="c", hold=HR, frame_l=PA, frame_r=PD, seed=32, mirror=True)]),
    "tt_climb_lead_routes_h": (routes, [dict(label="Route H blue, layout d mirrored", layout="d", hold=HB, frame_l=PB, frame_r=PC, seed=42, mirror=True)]),
}

if __name__ == "__main__":
    for mod in (sys.argv[1:] or list(SETS)):
        b, prm = SETS[mod]
        ML.run(mod, b, prm, title="temp-Active batch 5 lead routes", names=[mod])
