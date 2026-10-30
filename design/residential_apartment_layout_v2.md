# Residential Building Layout v2, rev C: 10 Generous Units, Minimal Public Space (Vance, Oct 29 2026)
Rev C (Jared): 10 units total = 8 apartments + 1 Laundry + 1 Maintenance; generous rooms; minimal public space (tight corridor + stair core, no lobby/atrium); 201 absorbs the old 2C alcove; Maintenance holds Sprocket pads, the substation role and the risers; all doors Bulkhead Hub; all apartments enterable; 4 interior kits re-mapped; doors seated on the real wall face (QA-BK-01). Rev B kept as `residential_apartment_layout_v2_revB.md`. **Plan only, no build until Jared approves.**
Shell unchanged: 28.0 m (X -14..+14) × 18.0 m (Z -9..+9) × 8.8 m; L1 Y 0.00, L2 Y +4.20. South wall (Z -9) faces the Valley A Promenade; Sector-4 exit stays at Z -9, X 0.
- **Exterior v1 (approved 2026-10-29):** Maintenance gains a **2.0 m north service door** (Z +9 wall, X 3.2, force-field + Bulkhead Hub, rev C door spec) for Sprocket access and as the 2nd fire exit. See `residential_exterior_plan_v1.md`.

## Circulation (public space ≈ 65 m² per floor, 13% of the floor)
- **Corridor:** one east–west corridor per floor, **1.6 m clear** between wall faces (Z -0.8..+0.8), running only **X -10..+10** (the end strips go to the corner units). Fits 2 people passing, or 1 person + Sprocket (0.78 m).
- **Stair core (approved 2026-10-29, see `residential_stair_core_v1.md`):** X -2..+2, Z -9..-0.8 (4.0 × 8.2 m; 3.8 × 8.1 m clear), opening straight off the corridor with no door.
  - **Flights:** two 1.5 m switchback flights, **26 risers × 0.1615 m, treads 0.28 m**, split unequally: **flight 1 (west) 16 R** climbs south from the L1 bottom landing (2.4 m deep, by the corridor) to a **south mid-landing at Y 2.585** (Z -8.9..-7.4, 1.5 m deep, soffit 2.335 m, above the exit vestibule and clear of the 2.3 m exit door head). **Flight 2 (east) 10 R** climbs north to a **4.1 m L2 landing** that opens onto the L2 corridor.
  - **L1:** residents walk from the corridor under flight 2 (≥ 2.33 m headroom) to the vestibule and the Sector-4 door. The space under flight 1 is closed (store + strap locker).
  - **Window and light:** the promenade window is a tall slot on Z -9 at the mid-landing (Y 3.0–7.0). The skylight strip (3.8 × 4.0 m) sits over the stair void only.
  - Glass guards 1.1 m, handrails 0.9 m both sides. No lobby, no atrium, no double-height public void.
- **Partitions:** 0.20 m thick; all dimensions below are to partition centerlines.

## Level 1 (Y 0.00): 4 apartments + Laundry + Maintenance
| Unit | X, Z | Size | Door (on corridor wall face) |
|---|---|---|---|
| 101 apt | -14..-4.5, +0.8..+9 | 77.9 m² | Z +0.8 face, X -6.5, 1.4 m |
| Laundry (1A) | -4.5..+0.5, +0.8..+9 | 41.0 m² | Z +0.8 face, X -2.0, 1.4 m |
| Maintenance (was 1B) | +0.5..+6, +0.8..+9 | 45.1 m² gross, **42.5 m² net** (bot-lift shaft 1.6 × 1.6 in the SW corner, v1.1) | Z +0.8 face, X +3.2, **2.0 m** (Sprocket); north service door Z +9, X 3.2 |
| 102 apt | +6..+14, +0.8..+9 | 65.6 m² | Z +0.8 face, X +8.0, 1.4 m |
| 103 apt | -14..-2, -9..-0.8 (+ end strip -14..-10, -0.8..+0.8) | 104.8 m² | Z -0.8 face, X -4.5, 1.4 m |
| Stair core + vestibule | -2..+2, -9..-0.8 | 32.8 m² | Sector-4 exit: Z -9 face, X 0, 2.6 m |
| 104 apt | +2..+14, -9..-0.8 (+ end strip +10..+14) | 104.8 m² | Z -0.8 face, X +4.5, 1.4 m |

```
LEVEL 1  (north = +Z at top)
X -14            -4.5      +0.5    +6              +14
+----------------+---------+-------+----------------+  Z +9
|                | LAUNDRY | MAINT |                |
|      101       |  41 m²  |[P] [P]|      102       |
|    77.9 m²     |         |LF R[P]|    65.6 m²     |
+------[B]-------+---[B]---+--[B]--+------[B]-------+  Z +0.8
|    |<========== CORRIDOR 1.6 m ==========>|      |
+------------[B]-----+ STAIR  +-----[B]-------------+  Z -0.8
|                    |F1^ walk|                    |
|        103         |16R |F2 |        104         |
|      104.8 m²       | ^  |und|      104.8 m²      |
|   (promenade wdw)  |-midlnd-|  (promenade wdw)   |
|                    | VESTIB.|                    |
+--------------------+==[B]===+--------------------+  Z -9
X -14               -2  exit +2                  +14
[B] force-field door + Bulkhead Hub, frame seated in the wall   [P] Sprocket floor pad   R riser shaft   LF Sprocket bot lift (v1.1)
```

## Level 2 (Y +4.20): 4 apartments
| Unit | X, Z | Size | Door |
|---|---|---|---|
| **201 player apt** | -14..0, +0.8..+9 | **114.8 m²** (absorbs the old 2C alcove as a workshop nook) | Z +0.8 face, X -3.0, 1.4 m |
| 202 apt | 0..+14, +0.8..+9 | 114.8 m² gross, **109.7 m² net** (SW corner, v1.1: bot-lift shaft 1.6 × 1.6, riser chase 1.0 × 1.0 re-aligned to X 0.6..1.6, Z 2.4..3.4 so it stacks with L1, and a sealed 0.5 m slot for the lift controller) | Z +0.8 face, X +3.0, 1.4 m |
| 203 apt | -14..-2, -9..-0.8 (+ end strip) | 104.8 m² | Z -0.8 face, X -4.5, 1.4 m |
| Stair core + L2 landing | -2..+2, -9..-0.8 | 32.8 m² | open to corridor (4.1 m L2 landing at the north); promenade window on Z -9 at the mid-landing |
| 204 apt | +2..+14, -9..-0.8 (+ end strip) | 104.8 m² | Z -0.8 face, X +4.5, 1.4 m |

```
LEVEL 2  (north = +Z at top)
X -14                     0                       +14
+-------------------------+-------------------------+  Z +9
|          201            |          202            |
|   PLAYER  114.8 m²      |        114.8 m²         |
| (workbench + ex-2C nook)|LF R                     |
+----------[B]------------+-----------[B]-----------+  Z +0.8
|    |<========== CORRIDOR 1.6 m ==========>|      |
+------------[B]-----+ STAIR  +-----[B]-------------+  Z -0.8
|        203         |L2 LAND.|        204         |
|      104.8 m²       |--guard-|      104.8 m²      |
|   (promenade wdw)  |void|F2^|  (promenade wdw)   |
|                    |mid+wdw |                    |
+--------------------+--------+--------------------+  Z -9
```

## Doors (11 Bulkhead Hubs) and QA-BK-01
- 10 unit doors + the Sector-4 exit, all force-field in the v2 frame with a **Bulkhead Hub** (0.40 × 0.80 × 0.20 m panel at 1.0–1.8 m, 0.9 m Sprocket coupler socket, no dock flap) on the latch-side jamb, corridor side.
- **QA-BK-01 fix:** each door is defined by its partition (the wall line in the tables), never by a free coordinate. The frame is centered in the 0.20 m partition; the hub's back face sits on the corridor-side wall face (Z ±0.8 or Z -9 for the exit), within 30 mm, on a jamb pier with its own StaticBody (also covers REAL-01).
- **Sprocket:** 3 open 1.2 × 1.2 m floor pads with coupler arms, all in Maintenance; no wall docks anywhere. Maintenance also holds the substation cabinet and the riser shaft base (R), which rises through the sealed chase in 202.
- **v1.1 Sprocket bot lift (pending Jared review):**
  - **Shaft:** 1.6 × 1.6 m gross at X 0.6..2.2, Z 0.8..2.4 (Maintenance SW corner at L1, 202 SW corner at L2). It holds a 1.2 × 1.2 m car and serves L1 and L2.
  - **Doors:** 1.0 × 1.3 m doors open onto the **corridor** at both levels, each with a 1.2 × 1.2 m landing and a Bulkhead Hub style call panel.
  - **Services stacking:** the riser now sits directly north of the shaft at the same XZ on both levels. The old L1 and L2 risers were 0.7 m out of line.
  - **Maintenance re-plan:** the pads move out of a straight 2.0 m fire-egress lane (X 2.2..4.2) between the corridor door and the north service door, to X 0.8..2.0 / Z 6.6..7.8 and X 4.4..5.6 / Z 4.0..5.2 and 6.6..7.8. The tool wall moves to Z 3.6..6.4 and the spares shelf to X 4.3..5.9. The substation stays.

## Other audit items (carried from rev B)
- REAL-02: the stair rail and any glass get their own colliders from the same mesh.
- REAL-03: one Area3D per unit matching its partitions, used for both HUD zone names and interior streaming; each shell must pass the 72-ray closed check.
- REAL-04: recheck stair width and headroom (≥2.1 m) after the rebuild.
- REAL-05: no leftover open areas; public space is only the corridor and stair core.

## Interiors: 4 kits mapped to the 7 non-player apartments
Kits: **K1** Shift Tech Studio (Engineering amber), **K2** Family home (Agri emerald), **K3** Researcher (Science violet), **K4** Civic Elder (Civic teal). Larger units get an extra room zone (bedroom/study) from the same kit.
| Unit | Kit | Story beat (Chapter 1, Solar Flare) |
|---|---|---|
| 101 | K1 | Night-shift tech: bunk still down, half-eaten meal, Sprocket's spare charge cable. |
| 102 | K4 | Elder sheltering in place: suit missing from its hook, plants knocked over by the 0.35G drop. |
| 103 | K2 | Family left in a hurry; toys drifted toward the window (Coriolis tell). |
| 104 | K3 | Researcher's flare-monitor desk; every slate shows the same red solar glyph. |
| 201 | Bespoke | Player apartment; existing workbench, sleeve, headband, spool; ex-2C becomes a tool and cable nook. |
| 202 | K2 (mirrored) | Neighbor family; a wordless drawing of the player taped up; riser chase as a boxed-in corner. |
| 203 | K4 (mirrored) | Retired pilot; Aldrin Cycler route model on the wall; Battery Charge pickup. |
| 204 | K1 (mirrored) | Engineer's bench with a dismantled field emitter (teaches the door system); a stuck Sweep bot to free (Mechanic B). |
Laundry: lockers, 4 washer/dryer stacks, folding counter. Maintenance: substation cabinet, 3 pads, riser base, tool wall.

## Budgets and streaming
| Unit type | Tris | Materials | Dynamic lights | Physics props |
|---|---|---|---|---|
| 201 (player) | ≤ 28,000 | ≤ 8 | 3 (1 shadowed) | ≤ 35 |
| 103, 104, 202, 203, 204 (~105–115 m²) | ≤ 20,000 | ≤ 6 | 2 (1 shadowed) | ≤ 30 |
| 101, 102 (~66–78 m²) | ≤ 16,000 | ≤ 6 | 2 (1 shadowed) | ≤ 25 |
| Maintenance | ≤ 14,000 | ≤ 5 | 2 | ≤ 15 |
| Laundry | ≤ 10,000 | ≤ 4 | 1 | ≤ 10 |
Shell, corridor and stair core: ≤ 12,000 tris per floor.
- **Live:** player inside the unit, or on the same floor within 10 m of its door → full interior, physics on.
- **Warm:** same floor 10–16 m, or door field closed → visible, props frozen, baked light only.
- **Cold:** other floor, or more than 20 m → unloaded; window shows a lit interior card. Hysteresis: reload at 16 m, unload at 20 m.
- At most about 3 units are Live/Warm at once (≈ 60k tris for interiors).

## Rook: what to model
1. Rebuild `preface_residential_sector.glb` to this grid: 0.20 m partitions, the 1.6 m corridors (X -10..+10), the 4.0 m stair core with switchback and its colliders; remove the atrium, mezzanine and old open areas.
2. One door frame kit + one Bulkhead Hub, instanced 11 times, seated per the QA-BK-01 rule.
3. 3 floor pads with coupler arms, substation cabinet and riser shaft (Maintenance) plus the 202 chase.
4. Interior kits K1–K4 (with the extra room zone for big units), 7 story sets, the Laundry and Maintenance fit-outs, the 201 extension into the ex-2C nook, and one window card per unit.

## Gage: what to change
1. Replace the building scene; rebuild collision and navmesh; one Area3D per unit for zone names and streaming.
2. Re-place the player spawn in 201 and check it after the rebuild.
3. Door logic for all 11 doors: wrist [F] at the hub → amber standby, scanning, `#3FAF6A` granted, violet field drops. All apartments are enterable.
4. Live/Warm/Cold streaming with 16/20 m hysteresis.
5. Sprocket pathing to the Maintenance pads and to door coupler sockets.
6. Light probes and occlusion for the smaller core (no atrium light; add a skylight over the stair core).

## 2D floor plans
- `design/residential_floorplan_rev_c_L1.png`
- `design/residential_floorplan_rev_c_L2.png`
(generated by `design/residential_floorplan_rev_c.py`)
- Room layouts: `design/residential_roomlayout_rev_c_L1.png`, `design/residential_roomlayout_rev_c_L2.png` (generated by `design/residential_roomlayout_rev_c.py`)

## Rev C.1 changes, pending Jared approval (Oct 29 2026)
Plans: `residential_roomlayout_rev_c_v2_L1.png` / `_v2_L2.png`. The main `residential_roomlayout_rev_c_L1/L2.png` are overwritten with the same images. The assert QC passes: no overlaps, door zones / lift landing / egress lane clear, 0.9 m paths.
- **Out of the building** (kept as assets, not deleted): #17 lab bench (104), #29 specimen shelf (104), #31 emitter repair bench (204) and #26 workbench (201) go to the future lab/workshop building. Hydro planter #33 (103, 202) goes outdoors as Rook's Tiered Steps (exterior #23/#25/#26).
- **104 (K3 Researcher):** the lab bench footprint is left open as a dust outline. A wall-anchor "shelf ghost" marks where the shelf stood, and a lab crate sits between the window desk and the telescope. The flare-monitor desk beat is unchanged.
- **201 (player):** the 2.0 m fold-down wall desk + task lamp on the N wall is the stand-in. It keeps the Stage 1 pickups, the terminal and the CUE-001 decals. The old 3.7 × 2.5 nook is left open as an "ex-bench outline", with a 0.9 m path to the desk.
- **204 (K1 Shift Tech, mirrored):** an "emitter wall" (tool wall #25 + one loose door emitter strip + rail task lamp) on the E wall keeps the door-system teaching beat. A lab crate with its lid ajar (emitter parts) sits in the old bench slot beside the stuck Sweep.
- **103 (K2):** the window strip is left open: planter clamp-bolt marks plus the toy drift against the glass (the Coriolis tell, now unobstructed).
- **202 (K2 mirrored):** the planter clamp marks remain; two dining chairs are pulled to the window (the family watched the flare). The taped drawing of the player is on the glass.
