"""Rook r9 (2026-11-15): spec Rev 3.8 (Vance 73fac5b) pieces, building coords (X axial, Z across, Y up, F1 = 0).
#3 TTQA-053 zone links: tt_door_pair_18 (1.8 m pair door for the Walls_F1/F2 Z 64 and X 113 openings; leaves grouped as Leaf_L /
Leaf_R parent nodes with their own *-colonly child, origin on each hinge, like TTQA-049) + stand-end cheeks (1.07 m over every tier).
#4 TTQA-011 remainder: NE plant-opening guards at F2 / F3 + slab infill under the staff-door gap.  Run: python3 links_rev38.py"""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from struct_lib import *
import pygltflib as pg
from ramps import Kit
from access_rev37 import export_kit, gd

# ------------------------------------------------------------------ #3 pair door (local: X across the 1.8 m opening, Z through a 0.3 m wall, Y up)
DW, DH, WT = 1.8, 2.4, .3
def door_pair():
    h = DW / 2; zc = 0.0; P = []; C = []
    cas = [box(-h - .08, -h + E, 0, DH + .08, zs - .025, zs) for zs in (-WT/2, WT/2 + .025)] + \
          [box(h - E, h + .08, 0, DH + .08, zs - .025, zs) for zs in (-WT/2, WT/2 + .025)] + \
          [box(-h - .08 + E, h + .08 - E, DH - E, DH + .08, zs - .025, zs) for zs in (-WT/2, WT/2 + .025)]
    P.append(("Door_Casing", ALY, cas)); C.append(("Frame-colonly", cas))
    P.append(("Head_Court_Line", AM, [box(-h + .05, h - .05, DH - .045, DH - .005, WT/2 - .02, WT/2 + .002), box(-h + .05, h - .05, DH - .045, DH - .005, -WT/2 - .002, -WT/2 + .02)]))
    for tag, a, b in (("L", -h + .005, -.004), ("R", .004, h - .005)):
        P.append((f"Leaf_{tag}_Panel", WH, [box(a, b, .01, 1.0, -.025, .025), box(a, b, 2.0, DH - .01, -.025, .025),
                                             box(a, a + .2, 1.0 - E, 2.0 + E, -.025, .025), box(b - .2, b, 1.0 - E, 2.0 + E, -.025, .025)]))
        P.append((f"Leaf_{tag}_Vision_Scissor", SCR, [box(a + .2 - E, b - .2 + E, 1.0 - E, 2.0 + E, -.006, .006)]))
        P.append((f"Leaf_{tag}_Kick_Plate", ALY, [box(a + .03, b - .03, .03, .25, *((.023, .029) if sz > 0 else (-.029, -.023))) for sz in (-1, 1)]))
        hx = (b - .1, b - .07) if tag == "L" else (a + .07, a + .1)
        P.append((f"Leaf_{tag}_Push_Bar", AM, [box(*hx, .95, 1.15, *((.023, .055) if sz > 0 else (-.055, -.023))) for sz in (-1, 1)]))
        C.append((f"Leaf_{tag}-colonly", [box(a, b, .01, DH - .01, -.025, .025)]))
    return P, C

def group_leaves(gp):
    """reparent Leaf_<T>_* + Leaf_<T>-colonly under a 'Leaf_<T>' node whose origin is the leaf's hinge (outer jamb, wall centre)."""
    g = pg.GLTF2().load(gp); sc = g.scenes[g.scene or 0]; piv = {}
    for tag, hx in (("L", -DW / 2), ("R", DW / 2)):
        P = [hx, 0.0, 0.0]; piv[f"Leaf_{tag}"] = P
        kids = [j for j, n in enumerate(g.nodes) if n.name and (n.name.startswith(f"Leaf_{tag}_") or n.name == f"Leaf_{tag}-colonly")]
        assert kids
        for j in kids:
            t = g.nodes[j].translation or [0, 0, 0]; g.nodes[j].translation = [t[0] - P[0], t[1] - P[1], t[2] - P[2]]
        g.nodes.append(pg.Node(name=f"Leaf_{tag}", translation=P, children=kids)); sc.nodes = [j for j in sc.nodes if j not in kids] + [len(g.nodes) - 1]
    g.save_binary(gp); return piv

# placements (centre of the opening on the wall centre line, yaw 0 = leaves across X)
DOORS = [(91.5, 0.0, 64.15, 0), (91.5, 6.1, 64.15, 0), (113.15, 0.0, 33.3, 90), (113.15, 6.1, 33.3, 90)]

# ------------------------------------------------------------------ #3 stand-end cheeks: 0.1 m solid, 1.07 m over each 0.4 m tier of the
# stand module (tiers 0.4/0.8/1.2/1.6/2.0 over local z +2.147..-2.103, front at +z), floor to tier + 1.07
TIERS = [(1.3, 2.147, .4), (.5, 1.3, .8), (-.4, .5, 1.2), (-1.2, -.4, 1.6), (-2.103, -1.2, 2.0)]
def cheek(k, y, s0, s1, line, axis, front, back, extra=None):
    """s0..s1 = cheek thickness across, front/back = world coords of the module's local z +2.147 / -2.103 along the other axis."""
    ms = []
    def seg(u0, u1, top):
        a, b = sorted((u0, u1))
        return box(s0, s1, y, y + top, a, b) if axis == "z" else box(a, b, y, y + top, s0, s1)
    for z0, z1, hgt in TIERS:
        f = lambda zl: front + (back - front) * (2.147 - zl) / 4.25
        ms.append(seg(f(z1) , f(z0), hgt + 1.07))
    if extra: ms.append(seg(extra[0], extra[1], 3.07))
    k.add("Cheek_Wall", SL, *ms); k.col(*[m.copy() for m in ms])

def cheeks():
    k = Kit()
    for y in (0.0, 6.1):
        # L1-N / L2-N: X 90.48..90.58 and 92.41..92.51 over the N stand depth Z 59.25..63.50 (yaw 180: front Z 59.253)
        for x0, x1 in ((90.48, 90.58), (92.41, 92.51)):
            cheek(k, y, x0, x1, None, "z", 59.253, 63.503)
        # L1-E / L2-E: Z 31.78..31.88 over X 108.25..113.0 (3p8 yaw -90: front X 108.253, back X 112.503, then the dead pocket to the wall)
        cheek(k, y, 31.78, 31.88, None, "x", 108.253, 112.503, extra=(112.503, 113.0 - .002))
    return k

# ------------------------------------------------------------------ #4 TTQA-011 NE plant opening guards (F2 / F3) + slab infill under the staff-door gap
def guards_ne():
    k = Kit()
    for y, d in ((6.1, .40), (12.2, .50)):
        gd(k, 69.04, 78.38, 127.95, "z", y, (False, True))            # W guard X 127.90..128.00, ends on the facade-bay inner face
        gd(k, 127.90, 131.25, 68.95, "x", y, (True, True))            # S guard Z 68.90..69.00, gap X 131.25..133.24 at the staff door
        gd(k, 133.24, 134.00, 68.95, "x", y, (True, False))
        # Rev 3.8 says Z 69.00..69.19, but the stack's visible Stack_Gratings start at Z 69.15 (y-0.25..y), so the infill stops 2 mm short
        # of them (69.19 would clip the grating by 40 mm); the stack's own Struct-colonly floor plate already runs out to Z 69.025.
        inf = box(131.25, 133.24, y - d, y, 69.00, 69.148)
        k.add("Slab_Infill", CON, inf); k.add("Infill_Court_Line", AM, box(131.3, 133.19, y - E, y + .003, 69.06, 69.10)); k.col(inf.copy())
    return k

if __name__ == "__main__":
    REP = []; LAY = json.load(open(LAYOUT))
    P, C = door_pair()
    r, _ = export_chunk("tt_door_pair_18", P, C, REP, layout=None, note="Rev 3.8 #3 1.8 m pair door, leaves Leaf_L / Leaf_R")
    piv = group_leaves(os.path.join(GODOT_MODELS, "tt_door_pair_18.glb")); print("LEAF_PIVOTS", piv)
    export_kit("tt_struct_stand_cheeks_r38", cheeks(), REP, LAY, "Rev 3.8 #3 TTQA-053 stand-end cheeks (L1/L2-N X 90.48..90.58 / 92.41..92.51, L1/L2-E Z 31.78..31.88)")
    export_kit("tt_struct_guards_ne_plant", guards_ne(), REP, LAY, "Rev 3.8 #4 TTQA-011 NE plant opening guards F2/F3 + slab infill Z 69.00..69.19")
    json.dump(LAY, open(LAYOUT, "w"), indent=1)
    print("ASSETS", len(REP), "FAILED", [x["asset"] for x in REP if not x["passed"]])
