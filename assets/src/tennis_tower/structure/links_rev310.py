"""Rook (2026-11-20): spec Rev 3.8 #1 TTQA-050 bowling entrances (Jared approved 8 -> 6 lanes, 2026-11-20; Vance N-side layout),
building coords (X axial, Z across, Y up, F1 = 0).
- Divider rail (Rev 3.10 8c23d43 restates Rev 3.8 #1): 1.07 m Court Line guard (kerb + colonly) at Z 11.06..11.16, X 37.0..56.9, 0.01 m off lane pair 1148's bed (Z 11.05),
  keeping players in the freed N aisle (X 30.0..56.9, Z 11.16..14.70) off the lanes past the foul line (X 37.0).
- Stand-end cheeks (Rev 3.8 #3 cheek(): 0.1 m solid, 1.07 m over every tier): X 43.91..44.01 (W end of the 6p5 at X 44.01..50.48, gap A)
  and X 50.48..50.58 / 52.41..52.51 (gap B, 1.83 m clear).
The Walls_F1 Z 15 door openings (X 40.35..42.15 new, X 50.6..52.4 from 50..53) are in build_structure.py, the stand removal / swaps
in rooms/temp-Courts/placements.py and the lane-pair / settee removal in rooms/temp-Leisure/bowling.py.  Run: python3 links_rev310.py"""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from struct_lib import *
from ramps import Kit
from access_rev37 import export_kit
from links_rev38 import TIERS

S_FRONT, S_BACK = 17.6 + 2.147, 17.6 - 2.103
DIV_Z = 11.11                     # kerb / collider +-0.05 -> Z 11.06..11.16
def bowl_links():
    k = Kit(); y = 0.0
    # E end at X 56.86: end post (r 0.035) and kerb stay 0.04 m off the acoustic Panel_Base face X 56.90 (was coplanar / 35 mm clip); < 100 mm gap
    k.guard(37.0, 56.86, DIV_Z, "x", lambda t: y, lambda t: y + 1.07, (True, True), kerb=True)
    # Rev 3.10 cheeks: Z 15.00..19.76 (back to the Walls_F1 face, closing the 0.45 m dead slot behind the stand backs). Faces kept
    # 3 mm off the 6p5 end faces (X 44.01 / 50.48 / 52.51) and the slab top / wall face are lapped 5 mm (no coplanar contact).
    for x0, x1 in ((43.91, 44.007), (50.483, 50.58), (52.41, 52.507)):
        cheek_r310(k, x0, x1)
    return k

def cheek_r310(k, s0, s1, y0=-0.005, front=19.76, back=S_BACK, wall=14.995):
    """links_rev38.cheek() profile (floor to tier + 1.07 over each 0.4 m tier), heights from F1 = 0, base lapped into the slab; plus
    the back segment Z 14.995..S_BACK at the top tier + 1.07 (3.07 m)."""
    ms = []
    for z0, z1, hgt in TIERS:
        f = lambda zl: front + (back - front) * (2.147 - zl) / 4.25
        a, b = sorted((f(z1), f(z0))); ms.append(box(s0, s1, y0, hgt + 1.07, a, b))
    ms.append(box(s0, s1, y0, 3.07, wall, back))
    k.add("Cheek_Wall", SL, *ms); k.col(*[m.copy() for m in ms])

if __name__ == "__main__":
    REP = []; LAY = json.load(open(LAYOUT))
    export_kit("tt_struct_bowl_links_r310", bowl_links(), REP, LAY, "Rev 3.8 #1 TTQA-050 bowling divider rail Z 11.06..11.16 X 37.0..56.9 + stand-end cheeks X 43.91..44.01 / 50.48..50.58 / 52.41..52.51, Z 15.00..19.76 (Rev 3.10)")
    json.dump(LAY, open(LAYOUT, "w"), indent=1)
    print("ASSETS", len(REP), "FAILED", [x["asset"] for x in REP if not x["passed"]], [(x["asset"], x["tris"], x["world_offset"]) for x in REP])
