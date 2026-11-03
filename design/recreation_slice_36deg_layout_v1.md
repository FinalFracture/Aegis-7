# Strip 5 — "The Green" (Recreation, 36° slice) — Layout Plan v1

**Status:** DRAFT v1, 2026-11-02 (Vance). Task from Jared via Atlas (6:38 PM CT). Planning only: markdown, no assets, no code, no builds.
**Rule for this doc:** every number marked *(doc)* comes from a cited repo doc. Everything marked **Vance proposal** is my own design call and is **not** a constraint.

## 1. Sources and constraints
| Fact | Value | Source |
|---|---|---|
| Drum | O'Neill cylinder R = 200 m, static, 10 strips × 36° | `design/cylinder_master_plan.md` §1 |
| Recreation strip | **Strip 5, θ = 180° (162°–198°), "The Green", D-02 Civic**; sports fields, trails, parks, the river; currently a curved grass slab placeholder | master plan §1, §3 |
| Neighbours | Strip 4 Spin Street Residential (S4\|5, 162°) and strip 6 Lantern Row Residential (S5\|6, 198°); the Window (strip 0) directly opposite/overhead | master plan §3 |
| Arc width | 125.66 m at the floor; sagitta 9.7 m; flat-footprint limit ≈ 12.6 m across the curve (10 cm gap), no limit axially | master plan §2 |
| Length / area | 800 m usable axial length; ≈ 10.1 ha per strip | master plan §2 |
| Floor radius | R = 200 m everywhere (Jared Q1) | `design/strip4_plan.md` §1.1 |
| Local frame | x = axial 0 (Fore Ring) … 800 (Aft Ring); z = arc distance ±62.83 m; down = local −y | master plan §6, strip4_plan §1 |
| Maglev | Strip 5 is served by **S4\|5 only** (shared with strip 4). **S5\|6 has a rib but no line.** Elevated T-beam, rail top +5.26, deck +5.40, car roof +8.50 | master plan §4; strip4_plan §5 |
| Stops on S4\|5 | Locals every 100 m at x 100…700 (7). Transfers: **Fore Hub** x 0 (Fore Ring × S4\|5, passenger dock "nearest the preface and the Green") and Aft Ring × S4\|5 x 800 (minor) | master plan §4; strip4_plan §5 |
| Stations | 30 m straight platform, 3.5 m wide local / 5 m at transfers, 2 stair+lift towers, piers on the seam rib every 10 m under platforms; 4 m station forecourts | strip4_plan §5.2, §9 |
| Ring lines | Fore/Aft Rings at x 0 / 800, rail top +10.2, two-level transfers; 12 m ring cross-walks underneath | master plan §4; strip4_plan §5, §9 |
| Seams | Physical rib 2–3 m raised hull frame with utility trench; only **2–4 gated rib crossings per border** (force-field door style), neighbour streams in at the crossing | master plan §6 |
| River | Strip 4 canal exits under the S4\|5 rib by culvert at **x 530** and feeds the River in strip 5; River recirculates to strip 2 | strip4_plan §7; master plan §3 |
| Canal geometry precedent | 2.5 m wide, 1.2 m deep, flat along x (gradient pumped / weired, not built into the floor) | strip4_plan §7 |
| No roads | Maglev is the only vehicle; walkways, promenades, stairs only | master plan §1 |
| Walkway widths (strip 4 precedent) | Spine 12 m, promenades 9.5 m (≥2.7 m clear through-walk), ring cross-walks 12 m, cross walks 6 m, service 4 m, forecourts 4 m, **0.9 m clear minimum anywhere** | strip4_plan §9 |
| Exits rule | Every building has **2 exits**: one onto a promenade/Spine, one onto a service walkway; all doors force-field | strip4_plan §6 |
| Curvature | Buildings level to local up at their centre (rule P3); wide decks need plinths/terraces; cross walks rise with the curve with 1:12 ramps or steps | strip4_plan §6, §9, §11; master plan §2 |
| Height | No building height cap (Jared Q6) | strip4_plan §6 |
| Aegis-7 Standard (assets) | <1.2% micro-noise PBR, alphaMode BLEND glass, <6,000 tris per asset, bottom-centre pivot, +Z facing, 5 iterations per asset, post-render votes in VOTE_LOG.md | `context/vance-handoff-v3.md` §2; `PROJECT.md` |
| Loading | One strip = one scene; neighbours as low-detail proxies; rest as far-wall impostor | master plan §6 |
| Existing rec assets | `bldg_17` Coriolis Recreation Arena (locked #02, 4,996 tris); `bldg_05` Celestial Promenade / Zero-G Observation & Recreation Dome (locked #02); `prop_04` civic planter bench pod (1,976 tris); exterior kit #21/#22/#32/#33/#34/#38/#20, TS-4 planter, #46 canal edge | `PROJECT.md`; `design/residential_exterior_asset_list_v1.md` |
| Overhaul spec landmarks | Arena (bldg_17) and Dome (bldg_05) were placed on a "Recreation Ridge" bluff in Valley A | `design/cylinder_interior_overhaul_spec.md` Zone 3 (pre-strip canon; Vance proposal to move both into strip 5) |

**Not documented (so not constraints):** a numeric egress travel distance, an occupancy load, or a park-specific exit count. §5 uses Vance proposals for these and flags them.

## 2. Frame for this strip
- Same convention as strip 4: **z = −62.83 is S4|5** (the maglev side, toward strip 4) and **z = +62.83 is S5|6** (rib only, toward strip 6). *(Vance proposal: mirror strip 4's convention so S4|5 is −z here; confirm.)*
- Station positions on the S4|5 seam (z −62.83): x 0 (Fore Hub), 100, 200, 300, 400, 500, 600, 700, 800 (Aft transfer). Platforms span x ±15 of each stop *(doc)*.
- River inlet: culvert under S4|5 at x 530 *(doc)*.

## 3. Zones (base plan, shared by all options) — Vance proposal unless marked
| Zone | x | z | Area | Notes |
|---|---|---|---|---|
| F — Fore Gateway Plaza | 0..60 | −62.8..62.8 | ~0.75 ha | Fore Hub forecourt, ring cross-walk (12 m, doc) at x 0, wayfinding |
| S4 — S4\|5 Station Edge band | 0..800 | −56..−50 | 0.48 ha | 4 m forecourts *(doc)* + 2 m buffer off the rib; tower feet at each stop |
| P — Rim Promenade (S4\|5 side) | 0..800 | −50..−40.5 | 0.76 ha | 9.5 m *(doc width)*; pairs with strip 4's Canal Promenade across the rib |
| SP — Spine Walk | 0..800 | −6..6 | 0.96 ha | 12 m *(doc width)*, axial, amber poles every 10 m (strip 4 precedent) |
| RT — Rim Trail (S5\|6 side) | 0..800 | 50..56 | 0.48 ha | 6 m loop trail; master plan landmark "Rim Trail" |
| RV — River corridor | 530..800 (+ return) | −40..−30 then along z +20..+30 | see options | Fed at x 530 *(doc)*; flat along x, pumped/weired *(doc rule)* |
| Program blocks | 60..740 | −40..50 | ~8.2 ha | Varies per option (§8) |
| A — Aft Plaza | 740..800 | −62.8..62.8 | ~0.75 ha | Aft Ring transfer forecourt, 12 m ring cross-walk |
- Rib buffer: keep **1.5 m off each rib** (strip4_plan review fix, applied here).
- Rib crossings to strip 4: x 530 (doc: gated walkway over the culvert) plus **x 100 and x 300** (Vance proposal; the station towers already sit on that rib). To strip 6: **x 200 and x 600** (Vance proposal), max 4 per border *(doc)*.

## 4. Circulation
- **Axial:** Spine Walk (z 0) + Rim Promenade (z −45) + Rim Trail (z +53) = three parallel axial routes, joined by **6 m cross walks every 50 m** (doc precedent) and **12 m "Station Walks" at every stop x** (Vance proposal), so every stop has a straight cross-strip route.
- **Cross-strip rise:** z runs up the curve; ±62.8 m edge sits 9.7 m sagitta *(doc)* above the centre in the curved frame, so cross walks use 1:12 ramps or steps at plinth steps *(doc rule)*. Fields and pools use terraced plinths, each piece ≤ 12.6 m across the curve or stepped *(doc limit)*.
- **Transit:** all arrivals by S4|5 elevated stations (+5.40 deck) via 2 towers each (stairs + lift) *(doc)*. Peak flows: Fore Hub (passenger dock) → Fore Gateway; x 500/600 stops → River district.
- **Service:** 4 m service walkway at z +40..+44 (Vance proposal) for Sprocket/carts; bollard gaps 0.9–1.5 m at junctions *(doc)*.
- **No vehicles** on the floor *(doc)*.

## 5. Egress (per the documented standard)
- **Documented:** every building has 2 exits (promenade/Spine + service walkway), force-field doors; 0.9 m clear minimum on all paths; promenades keep ≥ 2.7 m clear through-walk *(strip4_plan §6, §9)*.
- **Vance proposal (not documented; please confirm or supply the real rule):**
  - Open-air rec zones: from any point, ≤ 60 m walk to an axial route (Spine, Promenade or Trail). The 50 m cross-walk grid gives a worst case ≈ 25 m axial + 25 m cross ≈ 50 m.
  - ≤ 100 m to a station tower or a rib crossing: stops are 100 m apart, so worst case is 50 m axial + ~60 m across ≈ 110 m from the S5|6 edge. I propose the S5|6 rib crossings at x 200/600 count as exits to strip 6, which brings the worst case under 100 m.
  - Enclosed venues (arena, pool hall): 2 exits minimum *(doc)*, plus a 3rd if the hall is over 40 m long (Vance proposal).
  - Flare/emergency: venues double as shelter points for the Chapter 1 flare (Vance proposal; ties to the Shutter Ribs hook in master plan §3).

## 6. Prop list (base set; per-option extras in §8)
| # | Name | Size (m) | Zone | Placement rule | Asset |
|---|---|---|---|---|---|
| 1 | bldg_17 Coriolis Recreation Arena | per locked GLB | Program block | Level to local up at centre (P3); 2 exits min | **Existing** (locked #02) |
| 2 | bldg_05 Zero-G Observation & Rec Dome | per locked GLB | Program block, sightline to Window overhead | P3; 2 exits | **Existing** (locked #02) |
| 3 | prop_04 civic planter bench pod | per locked GLB | Spine, Promenade | every 25 m, outside the 2.7 m clear lane | **Existing** |
| 4 | Bench #32 | per asset list | All walks | back to planter or edge, 0.9 m clear kept | **Existing** (ext kit) |
| 5 | Street light pole #21 (amber) | per asset list | Spine (every 10 m), Promenade | strip 4 precedent | **Existing** |
| 6 | Bollard light #22 / bollard #34 | per asset list | Trail, service junctions | gaps 0.9–1.5 m | **Existing** |
| 7 | Bin/recycler #33 | per asset list | Plazas, stops | by forecourts | **Existing** |
| 8 | Wayfinding totem #38, stop totem #20 | per asset list | Each stop foot, cross-walk junctions | facing the walk | **Existing** |
| 9 | Tiered Steps TS-4 planter | 4.0 × 0.41 × 0.70 | Edges of fields/plazas | 0.2–0.4 m gaps (doc precedent) | **Existing** |
| 10 | Canal edge module #46 | per asset list | River corridor | continuous coping, rail on walk side | **Existing** |
| 11 | Elevated station + towers | 30 × 3.5 deck, towers per strip4_plan | S4 band | shared S4\|5 assets, authored once *(doc)* | **Existing design** (shared with strip 4) |
| 12 | Curved turf / ground tile kit | 10 × 10 (Vance proposal) | Fields, lawns | bend to R 200 | **New** |
| 13 | Terraced plinth module | 12 × 12 × 0.25 step (Vance proposal) | Fields, pools | ≤ 12.6 m across curve (doc limit) | **New** |
| 14 | River weir / footbridge | 6 m span (matches 6 m cross walks) | River | at each cross walk over the River | **New** |
| 15 | Rib crossing gate | per rib crossing | Each rib crossing | force-field door style *(doc)* | **New** (shared kit with strip 4 Civic Gate) |
| 16 | Field markings / goal / net set | per sport | Sports fields | on terraced plinth | **New** |
| 17 | Shade canopy (BLEND glass) | 8 × 8 (Vance proposal) | Plazas, pools | 3.0 m clear (station canopy precedent) | **New** |
All new assets: Aegis-7 Standard (<6,000 tris, bottom-centre pivot, +Z facing, BLEND glass, 5 iterations, VOTE_LOG vote).

## 7. Ties to adjacent slices and the tram
- **Strip 4 (S4|5):** shares the maglev line and all 9 stations; the Rim Promenade mirrors strip 4's Canal Promenade (z 45..54.5 there) across the rib. The **preface x 100 station** is the nearest stop to the Green from the Chapter 1 start; I propose the x 100 rib crossing so a player can walk preface → Green without riding (Vance proposal).
- **River:** enters at x 530 under the rib *(doc)*; options route it toward the Aft end and return; final exit back to strip 2 by pumped main under the floor (master plan says it recirculates to strip 2; route not documented → Vance proposal: utility trench of S4|5 rib).
- **Strip 6 (S5|6):** no line *(doc)*; up to 4 gated rib crossings. Proposed x 200 and x 600 (Vance proposal). Lantern Row's market/galleys suggest a food-stall edge near the x 600 crossing (Vance proposal).
- **Window (strip 0):** directly overhead *(doc)*; the Dome (bldg_05) is the natural view anchor.
- **End caps:** Fore Hub (x 0) is the main arrival from the passenger dock; Aft transfer (x 800) is minor *(doc)*.

## 8. Five candidate layouts (Jared to pick)
All share §3 edges, §4 circulation and §7 ties. The program block (x 60..740, z −40..50) differs.

### C1 — Park-Centric "Long Meadow"
Rolling lawns and groves the full length, River meanders z −30..+30 from x 530 to 740 and back along z +25 to x 300; Dome at x 400 (central, under the Window); Arena small at x 650.
```
x: 0    100   200   300   400   500   600   700  800
S4|5 [F]=st===st====st====st====st====st====st===[A]
     | meadow   grove   | DOME |  meadow ~~~RIVER~~~ |
     |======== SPINE ==============================  |
     | groves    lawn  ~~~~~~~~~~~ river return ~~~~ |
S5|6 ------- Rim Trail ---------------------------------
```
+ Biggest "sky-land" read, cheapest props, best breather. − Little gameplay; large empty areas to fill with foliage tris.

### C2 — Sports "Long Field"
Terraced fields x 120..520 (four 100 m-ish pitches on stepped plinths), Arena at x 550..620 next to the x 600 stop, River along the S4|5 side x 530..740 as a rowing channel.
```
S4|5 [F]=st===st====st====st====st====st====st===[A]
     | FIELD1 | FIELD2 | FIELD3 | FIELD4 |ARENA| ~row~ |
     |======== SPINE ==============================  |
     | courts / track ring  ............  | stands     |
S5|6 ------- Rim Trail (running loop) -------------------
```
+ Matches master plan's "Long Field", clear side-activities. − Curvature: pitches must be terraced (9.7 m sagitta); heavy plinth work.

### C3 — Aquatic / Thermal "River Baths"
River widened into lagoons and terraced pools x 530..760; thermal bath hall near x 500; lawns fore.
```
S4|5 [F]=st===st====st====st====st====st====st===[A]
     | lawns     picnic   | BATH HALL | LAGOON ~~~ POOLS |
     |======== SPINE ==============================  |
     | gardens         | DOME |  ~~~~ terraced pools ~~~ |
S5|6 ------- Rim Trail ---------------------------------
```
+ Strong use of the documented River inlet; unique set. − Water volume on a curved floor = most plinth/weir work; water shader cost; pool depth/mass not documented.

### C4 — Arcade / Social "Lantern Commons"
Pavilions, game halls, food court near the strip 6 crossings, amphitheatre at x 300; Arena x 650; small parks between.
```
S4|5 [F]=st===st====st====st====st====st====st===[A]
     | pavilions | AMPHI |  arcade halls | ARENA | river |
     |======== SPINE ==============================  |
     | food court(x200 gate) |  lawns  | stalls(x600 gate) |
S5|6 ------- Rim Trail ---------------------------------
```
+ Most NPC/mission hooks; ties to Lantern Row. − Feels like another town, weakens "brightest open strip"; most new buildings.

### C5 — Mixed Terraces "Green Steps" (**recommended**)
Three bands: Fore third (x 60..280) parks + Dome; middle third (x 258..568) **the Multi-Sport Tower complex** (`design/strip5_tennis_tower_v1.md`, Rev 2.3: building x 306..458, z −40..39, 152 × 79 m, Glass Box top +26.3) with the **West Arrival Plaza** (x 258..306) and **East Plaza** (x 458..488) as raised terraces at +4.0 HD, reached by 1:20 Spine ramps (x 178..258, 488..568); the Spine Walk loops the building (S arm = Rim Promenade, N arm z 39..50); x 300 and x 400 Station Walks link the S4|5 stops. **The C5 Arena block is deferred (Jared will revisit)**; the rest of the Long Field third stays open lawn/fields. Aft third (x 568..740) River with pools/weirs. Terraced plinth tiers step up toward both ribs to absorb the curve.
```
S4|5 [F]=st===st=300=st=400=st====st====st====st===[A]
     | PARK + DOME |W PLZ|  SPORTS TOWER  |E PLZ| lawn |~~RIVER/POOLS~~|
     |== SPINE ===/ramp+-- loop S arm ----+ramp\== SPINE ============== |
     | groves/lawns|     +-- loop N arm ----+     | lawn | ~ weirs ~     |
S5|6 ------- Rim Trail (full loop) ---------------------
```
+ Covers all four master-plan landmarks (River, Long Field, Rim Trail, parks); reuses both locked rec buildings; River placed where the doc puts the inlet; the Spine now ends at a destination building. − Each band is smaller than in the pure options; the tower and terraces take ~2.1 ha of the middle third.

**Recommendation (Vance proposal): C5 Mixed Terraces.** It is the only option that hits every documented landmark, keeps the open sky-land mood, and sits the River on its documented x 530 inlet.

## 9. Open questions for Jared
1. Pick a candidate (C1–C5); Vance recommends C5.
2. Egress: confirm or give the real Aegis-7 egress travel distance / exit count for open-air zones (my 60 m / 100 m numbers are proposals).
3. z convention: S4|5 at z −62.83 in strip 5 (mirror of strip 4)?
4. Rib crossings: x 100 / 300 / 530 to strip 4 and x 200 / 600 to strip 6 OK?
5. Move bldg_17 Arena and bldg_05 Dome from the old Valley A "Recreation Ridge" into strip 5?
6. River return route to strip 2 (via S4|5 rib utility trench?) and River width/depth (strip 4 canal is 2.5 × 1.2 m).
7. Depends on strip 4 Q5 (canal length, on hold): the x 530 inlet stays unless Q5 changes it.
