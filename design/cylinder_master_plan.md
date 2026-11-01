# Cylinder Hab-7 — Master Plan: 10 Radial Strips (planning only)

**Status:** draft v3, 2026-10-31 (v3: 5 lines on every other seam, end-cap rings only, per Jared via Atlas). v2 was (Atlas for Jared [t118u], revised for [t119u]: seam lines, elevated guideway, 5 rings, end-cap maps, preface move approved). This doc covers districts, maglev routes and landmarks only. No assets and no code.
**Sources:** `story_and_narrative_bible.md`, `cylinder_interior_overhaul_spec.md`, `city_district_zoning_and_emblems_spec.md` (D-01..D-04), `residential_exterior_plan_v1.md`, `godot/scripts/preface_playable_area.gd`, and context/STATUS.md design notes.

## 1. Fixed facts
- **O'Neill cylinder, R = 200 m.** The bible gives 800 m × 400 m dia, and the code agrees with R ≈ 200 for the Valley A arc.
- **Static cylinder.** It never rotates in-engine; the starfield, sun and planets orbit outside it. Spin gravity is still lore: the floor is "down" and the Coriolis/Mechanic C lore stays.
- **10 strips × 36°.** Each strip is its own map. Strip *k* is centred at θ = 36·k°.
- **Strip 0** = the full-length observation window. **Strip 5** (180°, opposite) = Recreation, currently a curved grass-slab placeholder.
- **No roads.** The maglev (T-beam guideway, Civic Pearl Classic cars, shelters, cyan tactile kerb) is the only vehicle transport. Buildings are joined by walkways, promenades and stairs.

## 2. Strip geometry
| Quantity | Value | Note |
|---|---|---|
| Arc width per strip at the floor | 2π·200/10 = **125.66 m** | Measured on the hull floor. Buildings built at R 185.5 m (the overhaul spec's R_HULL_FLOOR) get 116.6 m. |
| Sagitta of a full strip (chord 123.6 m) | 9.7 m | A strip is visibly curved, so big decks need plinths or terracing (see Jared [t112u]). |
| Flat-footprint limit across the curve | ≈12.6 m for a 10 cm gap | Along the axis there is no limit. |
| Usable axial length | **800 m (resolved)** | Jared chose the canonical 800 m. **TODO (Gage):** the authored cylinder mesh spans about x −368..+354 (~722 m) and must be extended to 800 m. |
| Floor area per strip | ~125.7 × 800 ≈ 10.1 ha | The current preface deck (66 m × ~94 m) uses about 7% of one strip. |

Long, narrow strips (about 5.6:1) mean each map plays as an **axial boulevard**: one spine of walkways and a maglev line, with buildings either side. The spine runs straight along the flat axis, and the cross-section curves up to the strip borders.

## 3. The ten strips
Ordering logic: heavy industry sits two or more strips away from residential. Science and Engineering flank the window, because the window is a structural and observational asset. Agri is spread around the ring so air and water loops are distributed. Residential flanks Recreation. Each department's emblem/accent from the zoning spec marks its strips.

| # | θ centre | Name | Dept | Purpose |
|---|---|---|---|---|
| 0 | 0° | **The Long Window** | D-03 / D-02 | An 800 m glazed observation strip: viewing galleries and catwalks over glass. |
| 1 | 36° | **Meridian Science Quarter** | D-03 Science | Labs, astrometry, new-tech testing. |
| 2 | 72° | **Cascade Biosphere** (Valley B) | D-04 Agri | Atmosphere and hydro cycle, the waterfall dam, biodome, TS-4 terraforming beds. |
| 3 | 108° | **Civic Commons** | D-02 Civic | Government, hospital/medbay, life support, sanitation. |
| 4 | 144° | **Spin Street Residential** (Valley A) | D-02 Civic | Housing. **Home of the preface playable area.** |
| 5 | 180° | **The Green** (Recreation) | D-02 Civic | Sports fields, trails, parks, the river. Placeholder. |
| 6 | 216° | **Lantern Row Residential** | D-02 Civic | Housing plus markets and galleys. |
| 7 | 252° | **Terrace Farms** | D-04 Agri | Food production, hydroponics, animal/pest control, veterinary. |
| 8 | 288° | **Foundry Reach** (Valley C) | D-01 Engineering | The fusion core, coolant, power, heavy fabrication. |
| 9 | 324° | **Signal & Cargo Yards** | D-01 Engineering | Comms array, cargo/rail hub, plumbing mains, the meteor-defence control. |

### Strip details
**0 · The Long Window.** *Mood:* hushed, dark, cathedral-like; the light comes from outside and slides as the sky orbits. *Landmarks:* (1) the Keel Catwalk, an axial truss walkway over the glass with the stars below your feet; (2) the Prism Bridge, where the mid-drum maglev crosses on a glazed truss (v3 2026-10-31: the Mid Ring is removed, so its role is open); (3) the Shutter Ribs, armoured louvres that close for a flare (a Chapter 1 hook). *Gameplay:* a vista hub, navigation landmark and flare-event set. There is almost no ground, so walking is on catwalks only. *Adjacency:* flanked by Science (observation) and Engineering (window structure and shutters).

**1 · Meridian Science Quarter.** *Mood:* clean, violet-indigo accents, quiet labs and telescope domes leaning toward the glass. *Landmarks:* the Astrometry Observatory (bldg_08 lineage) at the window edge; the Zero-G Materials Lab (bldg_18) lift to the spine; the Coriolis test range (the [t34u] spin-ring lineage). *Gameplay:* puzzle labs and tech unlocks. *Adjacency:* window on one side for sightlines, Biosphere on the other for shared experiments; no heavy industry next door.

**2 · Cascade Biosphere (Valley B).** *Mood:* humid, green, mist and white noise from the falls. *Landmarks:* the Waterfall Hydro-Dam (setpiece_02); the Geodesic Bio-Dome (bldg_04/06); the Atmo Plant scrubber stacks (bldg_07). *TS-4 terraforming beds originate here, and its nurseries supply the TS-4 planters in Spin Street.* *Gameplay:* Sato's hydro and scrubber work, and water-routing puzzles. *Adjacency:* upstream of the river in strip 5 via an aqueduct along the strip 3–4 border; it buffers Science from Civic.

**3 · Civic Commons.** *Mood:* busy, formal, municipal white with civic accents; plazas and arcades. *Landmarks:* the Council Rotunda; Hab-7 General Hospital (medbay); the Life-Support Nexus (bldg_11 / the AEGIS-7 node room). *Gameplay:* quest hub, AI-node overrides, NPC density. *Adjacency:* between Biosphere and Residential, a short walk for citizens.

**4 · Spin Street Residential (Valley A).** *Mood:* lived-in, warm, cyan tactile kerbs, TS-4 planters, the canal promenade. *Landmarks:* **the preface building and its tram stop** (existing); the Memorial (ext #29); the Canal Promenade, which feeds the river into strip 5. *Gameplay:* the preface and start of Chapter 1, the D-204 hatch and force-field doors, the first tram ride. *Adjacency:* next to Recreation and Civic, and three strips from Foundry Reach.

**5 · The Green (Recreation, placeholder).** *Mood:* open sky-land, the brightest strip, sitting directly "overhead" of the window view. *Landmarks (TBD):* the River (canal outflow from strip 4 that recirculates to strip 2); the Long Field sports grounds; the Rim Trail. *Gameplay:* downtime, side activities, a breather between missions. *For now* it is one long curved grass slab. *Adjacency:* residential on both sides, the window directly opposite.

**6 · Lantern Row Residential.** *Mood:* denser and older housing, night-market lanterns, galleys and food stalls. *Landmarks:* the Lantern Market; the stacked Galley Towers; the Pneumatic Mail Exchange (the preface Zone 5 mail tube lineage). *Gameplay:* trade/economy, NPC errands. *Adjacency:* Recreation on one side, Farms on the other (fresh food to the market).

**7 · Terrace Farms.** *Mood:* stepped green terraces under grow-light amber, agricultural bots (Clover). *Landmarks:* the stepped hydroponic terraces; the Aquifer Pump (bldg_09); the Cryo Seed Vault (bldg_10). *Gameplay:* bot-command and logistics puzzles. *Adjacency:* a deliberate buffer between Residential (6) and Industry (8); it absorbs noise and heat.

**8 · Foundry Reach (Valley C).** *Mood:* heavy, amber floodlights, steam and hum, caterpillar-amber workwear. *Landmarks:* the D-He3 Fusion Core (bldg_12); the Coolant Towers; the Spin-Trim Flywheel Hall (Mechanic C). *Gameplay:* Mensah's heavy-industry missions and the Chapter 1 flare crisis core. *Adjacency:* well away from housing (two strips from 6, four from 4), next to Cargo.

**9 · Signal & Cargo Yards.** *Mood:* busy logistics, gantries, cargo pods, comms masts aimed at the window. *Landmarks:* the Deep-Space Comms Array (bldg_08 comms); the Cargo/Rail Hub (bldg_13); the Window Shutter Control. *Gameplay:* Vance-Lin's transit and loader missions, and freight maglev. *Adjacency:* the cargo route to the aft dock, the window edge for comms sightlines, Industry next door.

### Why the preface lives in strip 4
- The existing area is already residential (D-02), with tram, canal, promenade and memorial. Strip 4 is the residential strip.
- It sits next to **Recreation (5)**, so the existing canal edge becomes the river's headwater, which gives the canal a purpose with no redesign.
- It is next to **Civic (3)**, where Chapter 1 heads first (hospital, AEGIS node).
- It is far from industry, which keeps the quiet opening mood.
- Canon placed the preface in Valley A at 180°. Strip 5 now takes 180°, so Valley A shifts to 144°. Gage's current backdrop roll (−43°) will need retargeting so the deck sits under strip 4's arc. That is a one-number change. **Approved [t119u]:** Valley A and the preface move to strip 4 (144°). Gage's backdrop roll is retargeted from −43° to strip 4's arc (TODO for Gage).

## 4. Maglev network (v3, 2026-10-31, per Jared via Atlas; supersedes v2)
- **Axial lines run on every other seam: 5 lines in total, S0|1, S2|3, S4|5, S6|7 and S8|9.** Each is shared by the two strips it divides, so every strip is served by exactly one line:
  - S0|1 serves strips 0 and 1.
  - S2|3 serves strips 2 and 3.
  - S4|5 serves strips 4 and 5.
  - S6|7 serves strips 6 and 7.
  - S8|9 serves strips 8 and 9.
  - Seams S1|2, S3|4, S5|6, S7|8 and S9|0 keep their physical ribs (§6) but carry no line.
- **Window strip:** S0|1 frames the 18° glass edge, and its guideway is the edge beam on that side. The S9|0 edge has no line, so its glazing edge beam is structural only (a Vance note; Atlas/Jared to confirm the look).
- **Elevated guideway:** the T-beam guideway runs elevated, and its height may rise or fall as needed (Jared, 2026-10-31; there is no fixed band). Boarding stations are elevated to match, with stair and lift access at grade.
  - **TODO (Gage, not now):** raise the preface tram per `strip4_plan.md` v2.2 (rail top +5.26, deck +5.40).
- **Two circumferential rings only (2026-10-31):** the **Fore Ring (0 m)** and the **Aft Ring (800 m)**, on the end-cap seams. Ring 25, the Mid Ring and Ring 75 are removed, and with them the Prism Bridge maglev crossing (§3 strip 0 landmark 2 needs a new role; open). Both rings cross the window on glazed bridges.
- **Crossings:** option A, two-level (ring rail top +10.2 over the seam line), **only at the end caps**.
- **Transfer stations:** ring × line = **2 × 5 = 10 nodes**, all at the end caps.
- **Local stops:** every 100 m on each line, at x 100..700, so 7 per line and **35 local stops**. That makes **45 stops in total** (10 transfers + 35 locals).
- **Hubs:**
  1. **Fore Hub**, Fore Ring × S4|5 (passenger dock, nearest the preface and the Green)
  2. **Aft Hub**, Aft Ring × S8|9 (cargo, starport, freight interchange)
  - The other 8 transfers are minor: Fore/Aft × S0|1, S2|3 and S6|7, plus Aft × S4|5 and Fore × S8|9.
  - Prism West/East, Commons Central, Green Central, Cascade Junction and Foundry Junction are **removed**.
- **Freight:** a separate freight track runs parallel to **S8|9 only** to the Aft Hub (S7|8 has no line now). Passengers never share it.
- **Service:** one direction per track at walking-scale speeds (≤ 60 km/h inside the drum).
- **Guideway quantity:** 400 seam modules + 240 ring modules ≈ 640 × ~600 tris ≈ 384k before instancing.

```mermaid
graph LR
  FH((Fore Hub<br/>passenger dock)) --- R0[Fore Ring 0 m]
  AH((Aft Hub<br/>cargo + starport)) --- R4[Aft Ring 800 m]
  subgraph Seam lines elevated, every other seam
    S01[S0-1 window edge]
    S23[S2-3]
    S45[S4-5]
    S67[S6-7]
    S89[S8-9 + freight]
  end
  R0 --- S01 & S23 & S45 & S67 & S89
  R4 --- S01 & S23 & S45 & S67 & S89
  W0[Strip 0 Window<br/>glazed ring bridges x2] -. framed by .- S01
  S89 == freight ==> AH
  FH -. spine lift / funicular .- SP((Axial Spine<br/>zero-G))
  AH -. spine lift .- SP
  FC[[Fore Cap map]] --- FH
  AC[[Aft Cap map]] --- AH
```

## 5. End caps and spine
- **Each cap** is stepped concentric terraces (setpiece_04 lineage) from R 185 m up to the R ≈ 45 m docking collar. The terrace tiers hold each strip's end station and the Ring stations.
- **Fore cap:** the passenger dock (bldg_14 Pinnacle), customs, and the Fore Hub. Earth/Mars shuttles berth at the axis.
- **Aft cap:** the Zero-G Starport, cargo berths, and the Aft Hub with the freight interchange.
- **Spine (R = 0):** the Axial Sun-Core (setpiece_03) plus a zero-G transfer tube from fore to aft, reached by the radial funicular and lifts. This is where Kade works (EVA/rigging). Gravity falls off with radius, which is the lore of Mechanic A/C.
- **Glass:** both caps have a glazed band in line with strip 0 (Patch confirmed stars show through both end caps at 797fc94).
- **Resolved [t119u]:** each end cap is **its own map** (Fore Cap, Aft Cap), so there are **12 maps in total**. The Fore and Aft Rings run along the cap seams, and their stations are the load points into the cap maps.

## 6. How the maps connect
- **Unit of loading:** one strip = one scene. The active strip is fully loaded. Its two neighbours are loaded as **low-detail proxies** (a curved slab, building silhouettes, lights), and the remaining 7 strips are a baked "far-wall" impostor that also tilts up overhead. This keeps the O'Neill look of land overhead without loading 10 maps.
- **Seams sit on strip borders and are always physical:** a structural rib (a 2–3 m raised hull frame carrying a utility trench and walkway bridges). There are only 2–4 rib crossings per border; a crossing is a short gated walkway (force-field door style) where the neighbour streams in and becomes the active map.
- **Seam lines and strip ownership:** a seam line belongs to both neighbouring maps. Its elevated guideway and stations are authored once and shared, appearing in each neighbour's proxy.
- **Maglev transfers** are the main way to move between strips. Boarding a Ring car hides a load behind the ride (~20–40 s). Axial travel stays inside one map.
- **Window border (0|1 and 9|0):** the rib is a catwalk gate. Strip 0 is small enough to stay always-loaded as a light scene.
- **Coordinates:** each strip map is authored flat-ish in local space (x = axial, z = arc length ±62.8 m) with a fixed rotation θ_k = 36·k° about the drum axis. The Godot pivot (as already set up in `preface_playable_area.gd`) rolls the shared cylinder backdrop by −θ_k, so "down" is always local −y. No runtime spinning.

## 7. Open questions for Jared
**Resolved [t119u]:**
- ~~Moving Valley A~~: approved. The preface goes to strip 4 (144°), and the backdrop roll is retargeted (Gage TODO).
- ~~Ring count~~: ~~five rings~~ → **two end-cap rings (0/800 m), 2026-10-31.**
- ~~End caps as maps~~: yes, 12 maps.
- ~~Station density~~: **v3, 2026-10-31:** 5 lines, 10 transfers + 35 locals = 45 stops, 100 m spacing (see §4).
- ~~Usable length~~: the canonical **800 m**; rings at 0/800 m (inner rings removed 2026-10-31). TODO for Gage: extend the ~722 m cylinder mesh to 800 m.
- Axial line placement: on the 10 seams, elevated 15–20 ft.

**Still open:**
1. **Strip order:** OK with Science and Cargo flanking the window, and Farms as the buffer between housing and industry?
2. **Valley names:** keep "Valley A/B/C" as lore names for strips 4/2/8, or retire them?
3. **The Green:** should the river run along the axis or as a loop? Should sports fields be gameplay or scenery?
4. **Window walking:** are catwalks over the glass enough, or should there be a solid floor path?
5. **Build order:** strip 4 (exists) → 3 → 5 → 0 → the rest. OK?
6. **Hub picks:** OK with the 8 suggested major hubs in §4?


## Change log
- **2026-10-31 (v3, Jared via Atlas):**
  - Inner rings at 200/400/600 m removed; only the Fore/Aft end-cap rings remain.
  - Axial lines only on S0|1, S2|3, S4|5, S6|7 and S8|9 (5 lines).
  - 10 end-cap transfers (option A, two-level) + 35 locals = 45 stops.
  - Hubs: Fore Hub (S4|5) and Aft Hub (S8|9) only.
  - Freight on S8|9 only.
  - Maglev height is no longer a fixed band.
  - Open items: the Prism Bridge's role, and the S9|0 window edge beam.
