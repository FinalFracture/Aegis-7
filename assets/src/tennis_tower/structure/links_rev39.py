"""Rook (2026-11-16): spec Rev 3.9 (Vance 67e9105) pieces, building coords (X axial, Z across, Y up, F1 = 0).
TTQA-056 / 057: stand-end cheeks for the L1-S / L2-S1 cuts (X 62.78..62.88, F1 + F2) and the L2-S2 pair door (X 90.48..90.58 /
92.41..92.51, F2), Rev 3.8 #3 cheek(): 0.1 m solid, 1.07 m over every tier of the S long stand (yaw 0, front Z 19.747, back Z 15.497).
The Walls_F1/F2 Z 15 openings are in build_structure.py, the stand swaps in rooms/temp-Courts/placements.py and the F2 door
placement in assemble_preview.py.  Run: python3 links_rev39.py"""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from struct_lib import *
from ramps import Kit
from access_rev37 import export_kit
from links_rev38 import cheek

S_FRONT, S_BACK = 17.6 + 2.147, 17.6 - 2.103
def cheeks_s():
    k = Kit()
    for y in (0.0, 6.1):
        cheek(k, y, 62.78, 62.88, None, "z", S_FRONT, S_BACK)                 # L1-S / L2-S1: end of the 3p8 at X 59.01..62.78
    for x0, x1 in ((90.48, 90.58), (92.41, 92.51)):
        cheek(k, 6.1, x0, x1, None, "z", S_FRONT, S_BACK)                     # L2-S2: ends of the 6p5 pair at X 84.01..90.48 / 92.51..98.98
    return k

if __name__ == "__main__":
    REP = []; LAY = json.load(open(LAYOUT))
    export_kit("tt_struct_stand_cheeks_r39", cheeks_s(), REP, LAY, "Rev 3.9 TTQA-056/057 stand-end cheeks (L1-S/L2-S1 X 62.78..62.88, L2-S2 X 90.48..90.58 / 92.41..92.51)")
    json.dump(LAY, open(LAYOUT, "w"), indent=1)
    print("ASSETS", len(REP), "FAILED", [x["asset"] for x in REP if not x["passed"]], [(x["asset"], x["tris"]) for x in REP])
