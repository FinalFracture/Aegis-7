"""temp-Courts: write godot/assets/models/rooms/temp-Courts_placements.json (Rev 3.0).
Covers court kit, stands (incl. F3 seats + cut bays), basketball, track.
Default court doors are CLOSED. Open-door frame sits at local z=-0.432 after recenter;
shift +0.432 m along local +Z to align with panels if the open leaf is used.
Run: python3 placements.py"""
import json, os, sys, math
HERE = os.path.dirname(os.path.abspath(__file__))
TT = os.path.abspath(os.path.join(HERE, "..", ".."))
if os.path.basename(os.path.normpath(TT)) != "tennis_tower":
    TT = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, TT)
from modlib import ROOT

OUT = os.path.join(ROOT, "godot/assets/models/rooms/temp-Courts_placements.json")
Y1, Y2, Y3 = 0.0, 6.1, 12.2
COURTS = [(48.5, 68.5, 27.5, 37.5), (74.5, 94.5, 27.5, 37.5),
          (48.5, 68.5, 41.5, 51.5), (74.5, 94.5, 41.5, 51.5)]
OPEN_DOOR_SHIFT = 0.432  # along local +Z; documented, not applied (default = closed)
HOOP_BASELINE_Z = -0.430  # local z of court baseline after hoop recenter

def item(asset, p, yaw, tag, room, note=None):
    d = dict(glb=f"res://assets/models/{asset}.glb", asset=asset,
             p=[round(float(p[0]), 4), round(float(p[1]), 4), round(float(p[2]), 4)],
             yaw=int(yaw) if float(yaw) == int(yaw) else float(yaw), tag=tag, room=room)
    if note: d["note"] = note
    return d

def rot_offset(yaw, lx, lz):
    r = math.radians(yaw)
    return lx * math.cos(r) + lz * math.sin(r), -lx * math.sin(r) + lz * math.cos(r)

def courts():
    out = []
    for i, (x0, x1, z0, z1) in enumerate(COURTS):
        mid = (x0 + x1) / 2.0
        room = "F1-CRT"
        # long sides: 10 x 2 m panels; door (closed) at box centre
        for z, yaw in ((z0, 180), (z1, 0)):
            for k in range(10):
                x = x0 + 1 + 2 * k
                # mid slot k=4 (x0+9) is the 2 m cell nearest box centre; a door
                # exactly at mid would leave 1 m remainders (no 1 m panel).
                if k == 4:
                    out.append(item("tt_court_partition_door_closed", (x, Y1, z), yaw, "f1", room,
                                    "default closed; mid long-side 2m slot (1 m west of box centre; no 1 m filler)"))
                else:
                    out.append(item("tt_court_partition", (x, Y1, z), yaw, "f1", room))
                out.append(item("tt_court_net", (x, 3.0, z), yaw, "f1", room, "net band +3.0..+5.0"))
        # short sides: 5 panels, no doors
        for x, yaw in ((x0, -90), (x1, 90)):
            for k in range(5):
                z = z0 + 1 + 2 * k
                out.append(item("tt_court_partition", (x, Y1, z), yaw, "f1", room))
                out.append(item("tt_court_net", (x, 3.0, z), yaw, "f1", room, "net band +3.0..+5.0"))
    return out

def stands():
    out = []
    # long runs: 3x7.5 + 3.8 cut at the corner-stair end (Vance Rev 2.7)
    long_west = [(42.1, "tt_stand_module_3p8"), (47.75, "tt_stand_module"),
                 (55.25, "tt_stand_module"), (62.75, "tt_stand_module")]
    long_east = [(80.25, "tt_stand_module"), (87.75, "tt_stand_module"),
                 (95.25, "tt_stand_module"), (100.9, "tt_stand_module_3p8")]
    # short runs: 7.5 at corner-stair end, 6.5 at lift-gap end
    short_s = [(24.25, "tt_stand_module"), (31.25, "tt_stand_module_6p5")]
    short_n = [(47.75, "tt_stand_module_6p5"), (54.75, "tt_stand_module")]
    def f3_name(a):
        return a.replace("tt_stand_module", "tt_stand_module_f3") if a != "tt_stand_module" else "tt_stand_module_f3"
    # F1 / F2
    for y, tag, room in ((Y1, "f1", "F1-CON"), (Y2, "f2", "F2-CON")):
        for x, a in long_west + long_east:
            out.append(item(a, (x, y, 17.6), 0, tag, room, "S long; put z 17.6 keeps preview back-face convention"))
            out.append(item(a, (x, y, 61.4), 180, tag, room, "N long"))
        for z, a in short_s + short_n:
            out.append(item(a, (32.6, y, z), 90, tag, room, "W short; 6.5 m at lift-gap end"))
            out.append(item(a, (110.4, y, z), -90, tag, room, "E short; 6.5 m at lift-gap end"))
    # F3: rake + seats co-placed
    for x, a in long_west + long_east:
        af, seat = f3_name(a), f3_name(a) + "_seats"
        for z, yaw, side in ((14.8, 0, "S"), (64.2, 180, "N")):
            out.append(item(af, (x, Y3, z), yaw, "f3", "F3-STAND", f"{side} long rake; seats co-placed"))
            out.append(item(seat, (x, Y3, z), yaw, "f3", "F3-STAND", "co-placed with rake, same transform"))
    for z, a in short_s + short_n:
        af, seat = f3_name(a), f3_name(a) + "_seats"
        for x, yaw, side in ((29.8, 90, "W"), (113.2, -90, "E")):
            out.append(item(af, (x, Y3, z), yaw, "f3", "F3-STAND", f"{side} short rake; 6.5 at lift-gap end"))
            out.append(item(seat, (x, Y3, z), yaw, "f3", "F3-STAND", "co-placed with rake, same transform"))
    return out

def basketball():
    out = []; room = "F3-BB"
    # courts: W X 41.5..69.5, E X 73.5..101.5, Z 32..47
    out.append(item("tt_bb_court", (55.5, Y3, 39.5), 0, "f3", room, "W court 28x15, end-to-end along X"))
    out.append(item("tt_bb_court", (87.5, Y3, 39.5), 0, "f3", room, "E court 28x15"))
    # hoops: baseline at court ends; local baseline z=-0.430, +Z into court
    def hoop_at(baseline_x, yaw):
        dx, dz = rot_offset(yaw, 0.0, -HOOP_BASELINE_Z)
        return (baseline_x + dx, Y3, 39.5 + dz)
    out.append(item("tt_bb_hoop", hoop_at(41.5, 90), 90, "f3", room, "W court W hoop; baseline X 41.5"))
    out.append(item("tt_bb_hoop", hoop_at(69.5, -90), -90, "f3", room, "W court E hoop; baseline X 69.5"))
    out.append(item("tt_bb_hoop", hoop_at(73.5, 90), 90, "f3", room, "E court W hoop; baseline X 73.5"))
    out.append(item("tt_bb_hoop", hoop_at(101.5, -90), -90, "f3", room, "E court E hoop; baseline X 101.5"))
    out.append(item("tt_bb_scorer_table", (71.5, Y3, 39.5), 90, "f3", room, "mid-gap 4 m, long axis along Z"))
    out.append(item("tt_bb_scoreboard", (71.5, Y3 + 7.5, 39.5), 90, "f3", room,
                    "hung on hall centre line Z 39.5, faces ±X; y=19.7 under ball net +21.5"))
    return out

def track():
    out = []; room = "F3-TRK"; y = Y3
    # corners: built +X+Z from circle centre; AABB 3x3, pivot is footprint centre (offset 1.5,1.5 in local)
    # SW / SE / NE / NW centres and yaws (quarter toward the outer glass corner)
    corners = [
        ((3.7, 3.7), 180, "SW"),
        ((124.6, 3.7), 90, "SE"),
        ((124.6, 75.4), 0, "NE"),
        ((3.7, 75.4), -90, "NW"),
    ]
    for (cx, cz), yaw, name in corners:
        dx, dz = rot_offset(yaw, 1.5, 1.5)
        out.append(item("tt_trk_corner", (cx + dx, y, cz + dz), yaw, "f3", room,
                        f"{name} corner; outer E stays 127.6; r_in=1.2 r_out=3.0"))
    # full straights (crossings not co-located — see note)
    out.append(item("tt_trk_straight_sn", (64.15, y, 1.6), 0, "f3", room, "S straight X 3.7..124.6, outer Z 0.7"))
    out.append(item("tt_trk_straight_sn", (64.15, y, 77.5), 180, "f3", room, "N straight, outer Z 78.4"))
    out.append(item("tt_trk_straight_ew", (1.6, y, 39.55), 90, "f3", room, "W straight Z 3.7..75.4, outer X 0.7"))
    out.append(item("tt_trk_straight_ew", (126.7, y, 39.55), -90, "f3", room, "E straight, outer X 127.6 FIXED"))
    return out

def main():
    rooms = {
        "F1-CRT": courts(),
        "F1-CON": [p for p in stands() if p["room"] == "F1-CON"],
        "F2-CON": [p for p in stands() if p["room"] == "F2-CON"],
        "F3-STAND": [p for p in stands() if p["room"] == "F3-STAND"],
        "F3-BB": basketball(),
        "F3-TRK": track(),
    }
    items = [p for v in rooms.values() for p in v]
    counts = {}
    for p in items:
        counts[p["asset"]] = counts.get(p["asset"], 0) + 1
    doc = dict(
        owner="temp-Courts",
        spec="design/strip5_tennis_tower_v1.md Rev 3.0",
        axes="Y up, X axial, Z across; yaw deg about +Y; p = building coords of GLB pivot (bottom centre)",
        note=(
            "Court doors default CLOSED at mid of each long side (Vance). "
            "Open-door asset (tt_court_partition_door) frame line is local z=-0.432 after recenter; "
            "apply +0.432 m along local +Z to align with panels if that variant is used. "
            "F3 rake + seats are co-placed at the same transform. "
            "3.8 m cut bays sit at the corner-stair end of each long run; 6.5 m cut bays sit at the lift-gap end of each short run "
            "(preview had only the 7.5 m short bays, at the lift end — this file follows Vance Rev 2.7). "
            "Stand put-z 17.6 / 61.4 / 14.8 / 64.2 / 32.6 / 110.4 / 29.8 / 113.2 matches assemble_preview; "
            "do not 'correct' the back face to nominal Z 15. "
            "Track E outer edge is 127.6 and is not moved; playground perches X 128.3..128.6 and path X 128.6..129.8 stay clear. "
            "tt_trk_crossing is promoted but not co-located on the full straights (a second bed would clash); "
            "Rook may split straights and drop it in at ST+S1/S2 (X 57..64 / 86..92), ST+N1/N2, ST+E (Z 50..60.6), ST-AQS/AQN. "
            "Void-edge rail: reuse tt_struct_void_guard (structure / F3-SLNG); not re-placed here. "
            "F1-CON / F2-CON floor finish and vomitory portal kit are a later batch if usage allows. "
            "WC interiors under the stands are temp-Services'; stand fronts stay lip-only so access stays open."
        ),
        stats=dict(counts=counts, n=len(items),
                   basketball_courts=["W X 41.5..69.5 Z 32..47", "E X 73.5..101.5 Z 32..47"],
                   open_door_shift_m=OPEN_DOOR_SHIFT,
                   skipped=["concourse floor/vomitory (budget)", "track crossing co-location (clash)",
                            "void guard (reuse structure)"]),
        open_conflicts=[
            "Short-run 7.5 m bays moved to the corner-stair end vs assemble_preview z=30.75/48.25 (lift-gap end). Follows Vance.",
            "Concourse vomitory / floor kit not in this commit.",
        ],
        rooms=rooms,
    )
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump(doc, open(OUT, "w"), indent=1)
    print(json.dumps({"wrote": OUT, "n": len(items), "counts": counts}, indent=1))

if __name__ == "__main__":
    main()
