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

# TTQA-023 3a / 3b: slide-link slot screens (court-partition scissor panes like the tower enclosures, 16 mm, colonly = the full spec
# band). 3a sits on the link's own cap rails (top 8.12) up to the enclosure head; 3b closes the slot ends between the corner columns
# (T1 / T2 tubes r 0.10 at Z 55.90 / 57.10), from the ground-entry heads (+3.50) up; the entries below stay open.
HEAD = 9.148   # 2 mm under the tower roofs (+9.15)
def slot_screens():
    k = Kit()
    for xc, (c0, c1) in ((23.64, (23.60, 23.68)), (24.66, (24.62, 24.70))):     # 3a link sides
        k.add("Slot_Screen_Scissor", SCR, box(xc - .008, xc + .008, 8.122, HEAD, 55.912, 57.088))
        k.col(box(c0, c1, 7.00, HEAD, 55.905, 57.095))
    for xc, (c0, c1) in ((20.06, (20.03, 20.09)), (24.94, (24.91, 24.97))):     # 3b slot ends
        k.add("Slot_Screen_Scissor", SCR, box(xc - .008, xc + .008, 3.50, HEAD, 56.002, 56.998))
        k.col(box(c0, c1, 3.50, HEAD, 55.905, 57.095))
    return k

if __name__ == "__main__":
    REP = []; LAY = json.load(open(LAYOUT))
    export_kit("tt_struct_stand_cheeks_r39", cheeks_s(), REP, LAY, "Rev 3.9 TTQA-056/057 stand-end cheeks (L1-S/L2-S1 X 62.78..62.88, L2-S2 X 90.48..90.58 / 92.41..92.51)")
    export_kit("tt_struct_slide_slot_screens_r39", slot_screens(), REP, LAY, "Rev 3.9 TTQA-023 3a link screens (X 23.60..23.68 / 24.62..24.70, Y 7.00..9.15) + 3b slot end screens (X 20.03..20.09 / 24.91..24.97, Y 3.50..9.15)")
    json.dump(LAY, open(LAYOUT, "w"), indent=1)
    print("ASSETS", len(REP), "FAILED", [x["asset"] for x in REP if not x["passed"]], [(x["asset"], x["tris"]) for x in REP])
