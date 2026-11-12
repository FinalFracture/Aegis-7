"""Rook r7 (2026-11-11): writes the cylinder-drop manifest godot/assets/models/tt_tower_manifest.json for
godot/scenes/tennis_tower/tennis_tower.tscn (loader godot/scripts/tennis_tower/tennis_tower_loader.gd).
Same placement list as assemble_complex.assemble() (structure + committed temp-*_placements.json, Services included
since r7e with 0 world placements), minus the box-only preview_hull: the drum floor is the cylinder's own. Building coords, F1 = 0, origin SW corner.
Also prints the Strip 5 drop transform from preface_playable_area.gd constants (read-only copy below)."""
import json, math, os, sys, collections
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import assemble_complex as AC
GODOT = os.path.join(AC.ROOT, "godot"); OUT = os.path.join(GODOT, "assets/models/tt_tower_manifest.json")
# preface_playable_area.gd (read-only): DRUM_FLOOR_R 200, DRUM_AXIS_Z -1.25, DRUM_AXIS_Y = EXT_GROUND_TOP_Y (0.12) + R,
# strip k centred at alpha = (k - 4) * 36 deg, outward(a) = (0, -cos a, sin a), tangent(a) = (0, sin a, cos a).
R, AXIS_Y, AXIS_Z, STRIP = 200.0, 0.12 + 200.0, -1.25, 5
F1_HD = R - math.sqrt(R*R - 40.0**2)   # 4.0408: true-circle F1 so the S threshold (Z 0, z -40) is flush; spec parabola says 4.0
def drop(axial_offset=-100.0, strip_x0=60.0, strip_z0=-40.0, f1_hd=F1_HD):
    a = math.radians((STRIP - 4) * 36.0); c, s = math.cos(a), math.sin(a)
    U, T = (0.0, c, -s), (0.0, s, c)                       # building +Y (drum up at the strip centreline), +Z (increasing alpha)
    C = (strip_x0 + axial_offset, AXIS_Y - R*c, AXIS_Z + R*s)
    o = [C[i] + T[i]*strip_z0 + U[i]*f1_hd for i in range(3)]
    return dict(alpha_deg=math.degrees(a), rotation_deg=[-math.degrees(a), 0, 0], f1_hd=round(f1_hd, 4), origin=[round(v, 4) for v in o],
                basis_x=[1, 0, 0], basis_y=[round(v, 6) for v in U], basis_z=[round(v, 6) for v in T])
def main():
    pl, log = AC.assemble()
    out, skipped = [], []
    for p in pl:
        g = os.path.realpath(p["glb"])
        if not g.startswith(GODOT + "/"): skipped.append(p["asset"]); continue
        out.append(dict(glb="res://" + os.path.relpath(g, GODOT), p=p["p"], yaw=p["yaw"], tag=p["tag"], owner=p["owner"], asset=p["asset"]))
    man = dict(note="Rook r7 Tennis Tower cylinder drop. Building coords (X axial, Z across, Y up, F1 = 0, SW corner). See design/tennis_tower_handoff/CYLINDER_DROP.md",
               count=len(out), by_owner=dict(collections.Counter(q["owner"] for q in out)), skipped=skipped,
               services="temp-Services_placements.json included (r7e): %d world placements; fountains/family rooms proposed_unplaced" % sum(q["owner"] == "Services" for q in out), drop=drop(), placements=out)
    json.dump(man, open(OUT, "w"), indent=0)
    print("manifest", len(out), "skipped", skipped, man["by_owner"]); print("drop", json.dumps(man["drop"]))
if __name__ == "__main__": main()
