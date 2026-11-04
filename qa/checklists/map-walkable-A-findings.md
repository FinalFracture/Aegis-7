# Doc A — Map walkability playtest findings (round 1, main 42ceab7)

Rules: APPEND ONLY to the end of this file. Do NOT read the existing entries before appending; write your own findings blind.
Each finding: `- [tester] [ID] location (x,y,z) | what happened | repro | severity`.
When you're done appending, open Doc B (`map-walkable-B-signoff.md`) and sign it.

---

## MAP-QA-2 — Collision edges & falls (2026-11-03)

Tested commit: `e9fad26` (round 1 pin). Godot 4.7.2 headless, `--fixed-fps 60`. Untracked harness outside the repo (`/tmp/qa2/walk.gd`): loads `preface_playable_area.tscn`, teleports `PlayerBody` to a start point and yaw, then holds `move_forward` (plus `sprint`/`jump` where noted) with `Input.action_press`, recording the path, min Y, and slide collisions. A downward ray grid at 0.5 m on L1 (y 0) and L2 (y 4.2) checked for floor holes. 92 walk probes in all: L2 wing edges, stairwell glass, L2 perimeter on N/S/E/W, four L2 corners, ±10 m column cells, and L1 radials from (0,0,2), (-9,0,0), (9,0,0).

**Counts:** fall-through / unguarded drop 1 (High) · invisible wall over continuous floor 1 (Medium) · holes in floor 0 · walk-through solids 0 · wedge/stuck spots 0 (all four L2 corners and both diagonal wall slides along x=±2.45 slid cleanly to the end) · info 1.

1. **[HIGH] A sprint-jump clears the L2 stairwell glass guard and drops the player about 4 m.** Nodes: `Guard_Glass_14-convcolonly`, `Guard_Glass_16-convcolonly` (guard line z -4.83, top y 5.255, which is 1.05 m above the 4.2 slab). JUMP_VELOCITY 4.8 gives about 1.18 m of apex, so the capsule clears the guard.
   Repro: put the player at (0.0, 4.3, -3.0) facing yaw 0 (-Z). Hold W and Shift, and tap Space. The player clears the guard at about z -4.8, drops into the well, and lands at y 0.06 (out through the sector-4 doorway to (0.0, 0.06, -16.7)). The same move from (-1.2, 4.3, -3.0) clears `Guard_Glass_14` and lands on the flight or mid landing at y 2.46.
   Walking into the glass without jumping holds every time: x -1.2, 0.0, 0.30, 0.38 and 0.45 all stop at z -4.47. The 0.37–0.40 seam before flight 2 is sealed too. Fix: guard at least 1.3 m tall, or an invisible cap collider above the glass.
2. **[MEDIUM] Invisible wall on open L2 floor in the west wing.** `SectorSafetyFloorColliders/L2WestWingSouthGuardrail` (box 6.5×1.25×0.18 at (-10.65, 4.82, -6.55); x -13.9..-7.4) stands in the middle of floor: the ray scan and walk probes show L2 slab out to z -8.55 here.
   Repro: from (-12, 4.3, -6.5) or (-8, 4.3, -6.5), walk -Z. The player stops dead at z -6.11 with nothing visible there. From (-10, 4.3, -8.0), walk +Z and the player stops at z -6.99. The area behind it can be reached by walking around the east end: start at (-6, 4.3, -8) and walk -X along z -8 or -7.2 freely to x -13.55.
   This looks like a leftover from the pre-Rev C gallery (PATH-06). Remove it, or move it to the real edge if one exists.
3. **[INFO] Player hangs mid-air when placed inside a prop collider.** A teleport to (-11.0, 4.4, -4.8) lands inside `Alcove2C_Battery_Expansion_Support/Shelf_Shape`. The player stays at y 4.40 with `is_on_floor()=false`, never falls, and can't walk -X. Only the harness can reach this; normal walking can't. I couldn't test the Seam03 1.1 m rail from this start because of it.

No problems on: L2 east/west wing inner edges (x ±2.45, z -8.5..-1.2: solid wall `RevC_Shell_L2_col`), L2 outer walls (x ±13.55, z +8.55, z -8.55), the ±10 m "hole" cells at z -0.5..0.5 (they are solid columns, blocked at z ±1.35), the whole L1 floor (no ray holes and no falls on any radial), or the walk down flight 2 from (1.2, 4.3, -2.5), which steps smoothly to y 2.46.
