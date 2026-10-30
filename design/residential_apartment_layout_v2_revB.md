# Residential Building Layout v2: Apartments on Both Floors + Open Stair Core (Vance, Oct 29 2026, rev B)
Rev B: all 18 doors use Bulkhead Hubs (Threshold Spine and Halo Panel deleted); all apartments enterable with full interiors; Patch Realism Audit REAL-01..05 folded in. Status: plan only, awaiting Jared's approval before any build.
Replaces the open-atrium layout in `preface_playable_residential_sector_spec.md` §1. Plan only (no models/code).
Shell unchanged: 28.0 m (X, -14..+14) × 18.0 m (Z, -9..+9) × 8.8 m; L1 at Y 0.00, L2 at Y +4.20. South wall (Z -9) faces the Valley A Promenade.
Jared's ask: no senseless open space; fill both floors with apartments; open up the area around the stairs.

## Grid rules
- Structural grid 5.5 m (X) with a 6.0 m central stair bay: X -14 | -8.5 | -3 | +3 | +8.5 | +14.
- One straight east–west double-loaded corridor per floor, **2.4 m clear** (Z -1.2..+1.2), ending in the stair hall at the center. Realistic for a dense habitat, wide enough for 2 people plus a passing Sprocket (0.78 m).
- Standard apartment: **5.5 × 7.8 m = 42.9 m² gross (~40 m² net)**, studio/1-bed: entry + kitchenette along the corridor wall, living/sleep zone at the window wall, wet pod (bath) 2.0 × 2.4 m beside the entry.
- **Open stair core (both floors):** stair hall X -3..+3, Z -5..+5 (6 × 10 m), **double height** (open void through L2 with a glass-and-rail gallery edge). Two side-by-side switchback flights, each 2.4 m wide, 24 risers at 0.175 m (4.2 m) with a mid-landing at Z +3.8. Ground-floor lobby continues south to the Sector-4 exit (X -3..+3, Z -9..-5). No atrium lightwell anymore; light comes from the stair void and a skylight strip above it.

## Level 1 (Y 0.00): 6 apartments + 3 service rooms + lobby
| Unit | Position (X, Z) | Size | Notes |
|---|---|---|---|
| 1A Laundry & Lockers | -14..-8.5, +1.2..+9 | 42.9 m² | kept (west side as before) |
| 101 | -8.5..-3, +1.2..+9 | 42.9 m² | apartment |
| 1C Mail/Parcel & Riser | -3..+3, +5..+9 | 24 m² | building services, behind the stair |
| 102 | +3..+8.5, +1.2..+9 | 42.9 m² | apartment |
| 1B Substation & Bot Dock | +8.5..+14, +1.2..+9 | 42.9 m² | kept (NE); houses the Sprocket floor pads |
| 103 | -14..-8.5, -9..-1.2 | 42.9 m² | apartment, promenade window |
| 104 | -8.5..-3, -9..-1.2 | 42.9 m² | apartment, promenade window |
| Lobby + Sector-4 exit | -3..+3, -9..-5 | 24 m² | entry vestibule; exit stays at Z -9.0, 2.6 m W |
| 105 | +3..+8.5, -9..-1.2 | 42.9 m² | apartment, promenade window |
| 106 | +8.5..+14, -9..-1.2 | 42.9 m² | apartment, promenade window |

```
LEVEL 1 (north = +Z, top)                                    X -14 ........................ +14
+-----------+-----------+-------------+-----------+-----------+  Z +9
| 1A LAUNDRY|   101     | 1C MAIL/RSR |   102     | 1B SUBSTN |
|  & LOCKER |   apt     +------[ ]----+   apt     | BOT PADS  |
|           |           |  STAIR HALL |           |  [P][P]   |  Z +5
+---[=]-----+---[=]-----+  (open,     +---[=]-----+---[B]-----+  Z +1.2
|<======== CORRIDOR 2.4 m =====  2-story  ===== CORRIDOR 2.4 m ========>|
+---[=]-----+---[=]-----+  void) /\/\ +---[=]-----+---[=]-----+  Z -1.2
|   103     |   104     |  switchback |   105     |   106     |
|   apt     |   apt     +-------------+   apt     |   apt     |  Z -5
|  window   |  window   |   LOBBY     |  window   |  window   |
+-----------+-----------+====[B]======+-----------+-----------+  Z -9
                          SECTOR-4 EXIT (2.6 m) -> Promenade
[=] [ ] [B] force-field door + Bulkhead Hub (all doors)   [P] Sprocket open floor pad + coupler arm
```

## Level 2 (Y +4.20): 8 apartments + 1 service alcove + overlook
| Unit | Position (X, Z) | Size | Notes |
|---|---|---|---|
| **201 Player apt** | -14..-8.5, +1.2..+9 | 42.9 m² | kept NW; spawn + workbench unchanged |
| 202 | -8.5..-3, +1.2..+9 | 42.9 m² | neighbor (keep balcony-suite story beat as a window bay) |
| 2C Vent/Cable Alcove | -3..+3, +5..+9 | 24 m² | kept; above 1C, shares the riser |
| 203 | +3..+8.5, +1.2..+9 | 42.9 m² | apartment |
| 204 | +8.5..+14, +1.2..+9 | 42.9 m² | apartment |
| 205 | -14..-8.5, -9..-1.2 | 42.9 m² | apartment, promenade window |
| 206 | -8.5..-3, -9..-1.2 | 42.9 m² | apartment, promenade window |
| Overlook landing | -3..+3, -9..-5 | 24 m² | open floor over the lobby, window to the promenade, bench |
| 207 | +3..+8.5, -9..-1.2 | 42.9 m² | apartment, promenade window |
| 208 | +8.5..+14, -9..-1.2 | 42.9 m² | apartment, promenade window |

```
LEVEL 2 (north = +Z, top)
+-----------+-----------+-------------+-----------+-----------+  Z +9
| 201 PLAYER|   202     | 2C VENT/CBL |   203     |   204     |
|  (spawn)  |   apt     +-----[B]-----+   apt     |   apt     |
|           |           | gallery rail|           |           |  Z +5
+---[=]-----+---[=]-----+.............+---[=]-----+---[=]-----+  Z +1.2
|<======== CORRIDOR 2.4 m ==== OPEN VOID ==== CORRIDOR 2.4 m ===========>|
+---[=]-----+---[=]-----+ over stairs +---[=]-----+---[=]-----+  Z -1.2
|   205     |   206     |.............|   207     |   208     |
|   apt     |   apt     |  OVERLOOK   |   apt     |   apt     |  Z -5
|  window   |  window   | (window)    |  window   |  window   |
+-----------+-----------+-------------+-----------+-----------+  Z -9
.... = glass-and-rail gallery edge around the stair void
```

## Doors and hubs (rev B: Bulkhead Hub only)
- **All 18 doors** (101–106, 201–208, 1A, 1B, 1C, 2C) are force-field doors in the v2 frame with a **Bulkhead Hub** on the latch-side jamb (corridor side). Apartment, 1A and 1C doors: 1.4 m clear × 2.3 m; 1B: 2.0 m (Sprocket fits); 2C: 1.4 m. **Sector-4 exit:** 2.6 m dual retracting leaves + field, with the same Bulkhead Hub.
- Hub panel 0.40 W × 0.80 H × 0.20 D at 1.0–1.8 m. The hub's flapped dock is **deleted**; the only Sprocket hardware on a hub is a small coupler socket at 0.9 m for emitter servicing.
- **Sprocket (≈0.78 × 1.03 × 0.77 m):** three open 1.2 × 1.2 m floor pads with coupler arms, two in 1B and one in the lobby beside the exit. No docks in walls.

## Realism Audit fixes (Patch, `context/playtest_bug_report.md`)
- **REAL-01 (hub with no collider behind it):** every Bulkhead Hub mounts on a jamb pier that has its own StaticBody, with the hub back face within 30 mm of the pier. One shared mounting rule in `_mount_door_hub`, no per-door offsets.
- **REAL-02 (balustrade without its own collider):** the stair-void glass and rail get a collider built from the same mesh/node, not separate loose boxes, so thrown props and bots are blocked reliably.
- **REAL-03 (L1 zone labels don't match walls):** each unit gets an Area3D zone box that matches its real partitions exactly (from the grid tables above); the same box drives the HUD zone name and the interior streaming below. Every unit shell must pass the 72-ray ring-cast closed check.
- **REAL-04 (stairs):** the current east stair passes and is replaced by the central switchback; recheck width (2.4 m per flight) and headroom (≥2.1 m) after the rebuild.
- **REAL-05 (wasted space):** the current 101 m², 73.5 m² and 60 m² empty areas are all absorbed by units 101–106 and 202–208. Note that 201 shrinks from 49.8 m² to 42.9 m²; if Jared wants it larger, 201 can take the 2C footprint and 2C moves to L1 1C.

## Interiors: every unit enterable (rev B)
Interiors are built from 4 modular kits that share one shell kit (walls, wet pod, kitchenette, window bay) and one texture atlas per kit. Each unit = kit + layout mirror/variant + story set (3–5 unique props) so no two read alike.

**Kits**
- **K1 Shift Tech Studio** (Engineering, amber D-01 accents): fold-down bunk, tool pegboard wall, work mat with half-repaired part, boot rack, single dining stool.
- **K2 Family 1-Bed** (Agri, emerald D-04 accents): sleeping partition with child bunk alcove, hydroponic window planter, small table for 3, toy bin, drawings on the wall as textures.
- **K3 Researcher Loft** (Science, violet D-03 accents): desk with data slates, specimen shelf, small telescope at the window, cable clutter, cot.
- **K4 Civic Elder** (Civic, teal D-02 accents): reading chair, potted plants, Earth photo frames (textures), tea set, a pressure suit hung by the door.

**Per-unit assignment** (Chapter 1 "Solar Flare" storytelling: residents evacuated or sheltering; loose items show the spin-gravity events)
| Unit | Kit | Variation and story beat |
|---|---|---|
| 101 | K1 | Night-shift tech; bunk still down, half-eaten meal; Sprocket-sized charger cable left out (Sprocket's owner). |
| 102 | K4 | Elder sheltering in place; suit missing from its hook; plants knocked over by the 0.35G drop. |
| 103 | K2 | Family left in a hurry; toys scattered toward the window (Coriolis drift tell). |
| 104 | K3 | Researcher's flare-monitor desk; slates all showing the same red solar glyph. |
| 105 | K1 (mirrored) | Tidy apprentice; tools sorted by color; a Super Wire spool pickup. |
| 106 | K4 (mirrored) | Couple's apartment; two chairs at the window, tea cups floated off the table at 0.12G and stuck to the ceiling hooks. |
| 201 | Bespoke (existing) | Player's apartment, unchanged (spawn, workbench, sleeve, headband, spool). |
| 202 | K2 (mirrored) | Neighbor family; window-bay balcony nook with planter; a note-free drawing of the player taped up. |
| 203 | K3 | Botanist; seed trays labelled by texture glyphs; Thermal Jelly pickup. |
| 204 | K1 | Engineer's repair bench with a dismantled field emitter (teaches the door system). |
| 205 | K4 | Retired pilot; Aldrin Cycler route model on the wall; Battery Charge pickup. |
| 206 | K2 | Empty move-in unit; crates still sealed (cheap variant, ~60% of kit). |
| 207 | K3 (mirrored) | Med-tech; first-aid cabinet open, emptied; trail of dropped supplies to the door. |
| 208 | K1 (mirrored) | Hoarder tinkerer; overfilled shelves; a stuck Sweep bot to free (Mechanic B co-op beat). |

## Interior streaming (despawn bands) and budgets
- **Bands per unit, driven by the REAL-03 unit Area3D and the player's floor:**
  - *Live:* player inside the unit, or on the same floor within 12 m of its door → full interior, props physics-active.
  - *Warm:* same floor, 12–20 m from the door, or the door field is closed → meshes visible but props frozen (no physics), lights baked only.
  - *Cold:* other floor or more than 24 m away → interior unloaded; the window bay shows a lit interior card (one quad) from outside. Hysteresis: reload at 20 m, unload at 24 m, so walking the corridor never pops.
  - The stair void sees both floors, so units facing the void (101, 102, 202, 203) stay Warm while the player is on the stairs.
- **Budget per unit:** shell ≤ 2,000 tris, kit furniture ≤ 10,000, story set ≤ 3,000 (**≤ 15,000 tris total**); ≤ 6 materials (one kit atlas + shared shell); ≤ 2 dynamic lights, 1 shadowed; ≤ 25 physics props. 201 bespoke ≤ 25,000. With the bands, at most ~4 units are Live/Warm at once (≈ 60k tris for interiors).

## Rook: what to model (rev B)
1. Rebuild `preface_residential_sector.glb`: new partitions on the grid, 2.4 m corridors, central stair hall with double-height void, two 2.4 m switchback flights + mid-landing, gallery glass and rail **with its own collider** (REAL-02), skylight strip; remove the atrium lightwell and old mezzanine.
2. Jamb piers with colliders (REAL-01) and 19 force-field frames (18 doors + Sector-4 exit) from one frame kit.
3. Bulkhead Hub, one asset instanced 19 times, with the 0.9 m coupler socket; no dock flap.
4. 3 Sprocket floor pads + coupler arms.
5. Interior shell kit + kits K1–K4 + the 13 story sets in the table, within the budgets above; one lit window card per unit for the Cold band.

## Gage: what to change (rev B)
1. Replace the building scene; rebuild collision and navmesh; per-unit Area3D zones that match the partitions (REAL-03) for HUD zone names and streaming.
2. Keep the player spawn in 201; re-check coordinates after the rebuild.
3. Force-field door logic on all 18 doors: wrist [F] at the Bulkhead Hub plays amber standby → scanning → `#3FAF6A` granted and drops the violet field. All apartments are enterable (per Jared); decide per unit in the door table whether it starts open or needs a story trigger.
4. Interior streaming bands (Live/Warm/Cold with 20/24 m hysteresis) per unit.
5. Sprocket pathing to the floor pads and the door coupler sockets.
6. Light probes and occlusion for the stair void and skylight.

## Open items
- Jared's approval of this plan (no build until then).
- Whether 201 keeps 42.9 m² or takes the 2C footprint (REAL-05 note).
