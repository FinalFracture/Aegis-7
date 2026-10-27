# AEGIS-1 / CYLINDER HAB-7 — VISUAL STORYTELLING CONTINUITY LEDGER

**Owner:** Sloane (Texture & Environment Artist) / Vance (Lead Designer) / Scribe (Continuity)  
**Directive Reference:** Jared (`[t4u]`, `[t6u]`, `[t8u]`)  
**Purpose:** Canonical production record tracking every environmental and texture-baked visual cue across Aegis-1 / Cylinder Hab-7. The visual storytelling across the station is engineered to tell a cohesive, forensically verifiable **hidden narrative** that contrasts sharply with the surface story presented to the player. By the end of production, every visual mark, wear pattern, tampered stencil, and telemetry anomaly must link into this ledger with zero random/orphan decoration.

---

## 1. Dual-Layer Narrative Architecture

### Layer A — Surface Player Experience (The Official Story)
* **What the player is told:** You are Lead Technician Kaelen Rostov (`TECH-2`) waking for a routine morning maintenance shift in Residential Sector-04 aboard Cylinder Hab-7.
* **Official explanation of events:** A minor, routine breaker trip occurred overnight on **Sub-Bus B-14**, temporarily dropping the Sector-04 service bulkhead to 40% travel. The four municipal `#05` Hammerhead drones (`Sprocket #0419`, `Sweep #0812`, `Kelvin #0204`, and `Clover #0631`) are executing ordinary daily duties: sweeping the mezzanine, tending the atrium planters, and running routine `D-03 // SCIENCE` thermal calibration in Room 1B (`BOT SUBSTATION`). Your objective is simply to gather spare `+5A` cells, Super-Wire, and Thermal Jelly to reset the door relay.

### Layer B — The Hidden Visual Story (What Actually Happened on Aegis-1)
* **What the physical environment & textures actually reveal:** Eight days ago, at **`2026-10-19 // 03:14 UTC`**, an unlogged **48.2 kW / 13.56 MHz / 412 Hz harmonic power spike** was covertly routed along **Sub-Bus B-14** from the restricted **Room 1B / Bay 102 Telemetry Relay** through **Rostov's Workbench (Apt 201 / Apt 101)** and across the upper mezzanine into **Quartermaster Suite Apt 202**.
* **The Cover-Up & Unit `#0204` Re-Designation:**
  1. Following an unlogged biological/cryo containment incident on the upper gallery (`Apt 202`), **Unit `#0204` ("Puddle")** — originally an Agri/Hydro-Cryo unit (`D-04` / `D-03 HYDRO`) — suffered a left-tread actuator lockup while hauling a sealed containment load down the East Stairwell.
  2. Unit `#0204` was dragged across the East Atrium floor into **Room 1B** (leaving a single-locked-tread rubber skid mark and glossy violet/cyan cryo-coolant drips leading straight to Sub-Bus B-14 Hatch 04).
  3. Inside Room 1B — whose doorway placard still shows ghost stenciling for **`SEC-04 // TELEMETRY RELAY [RESTRICTED // CLR-4 ONLY]`** underneath fresh `RM 1B // BOT SUBSTATION` paint and a torn security seal stamped **`2026-10-19 // 03:14`** — Unit `#0204` had its old identity purged and overwritten as **`D-03 // SCIENCE` ("Kelvin #0204")**.
  4. Before his **`CLR-4` security clearance was revoked** and downgraded to `TECH-2` (scratched out on the `APT 201` placard), Rostov pried open the left edge of his apartment's 13.56 MHz RFID door bezel, tapped `PIN_RESET -> BUS B-14`, and extracted a raw memory dump (**`A7-0204-MEM`**) from `#0204` on his workbench — blowing the **3rd neural capacitor coil (`COIL C3 [BLOWN]`)** and scorching the butcher-block wood right beside his taped `03:14 UTC` oscilloscope calibration note.

---

## 2. Master Visual Cue Registry (`Preface Residential Sector`)

| Cue ID | Title / Visual Detail | Sector & World Pos `(x, y, z)` | Asset / Material / UV Region | Surface Cover (Layer A) | Hidden Truth (Layer B) | Connected Cues |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **`CUE-001`** | **Blown Coil `C3` Scorch Ring, `A7-0204-MEM` Tally & `03:14 UTC` Oscilloscope Note** | Apt 201 Workbench `(-8.45, 5.12, 7.75)` | `preface_residential_sector.glb` / `Apartment_Workbench` / `UV_WORKBENCH_TOP` `(0.755..0.995, 0.505..0.635)` | Routine soldering burns and calibration notes from repairing PCBA door boards. | Taped oscilloscope waveform shows a **13.56 MHz / 412 Hz spike at `03:14 UTC` on `BUS B-14`** with `#0204: PUDDLE -> KELVIN` and a red arrow pointing to the **blown `C3` capacitor scorch mark** from an unauthorized `A7-0204-MEM` dump. | Links to `CUE-002`, `CUE-003`, `CUE-004`, `CUE-006`, `CUE-007` |
| **`CUE-002`** | **Single-Locked-Tread Skid Mark & Cryo-Coolant Drip Trail** | East Stairwell Base `(8.80, 0.12, -3.40)` to Room 1B Hatch `(5.60, 0.12, 6.20)` | `preface_residential_sector.glb` / `Residential_Hallway_Atrium` / `UV_FLOOR_SKID_TRAIL` `(0.755..0.995, 0.640..0.720)` | Ordinary utility bot tire wear and floor cleaning fluid along the east walkway. | **Asymmetric single-track rubber cleat skid** + metallic score line + glossy (`roughness 0.16`) violet/cyan cryo-coolant drips where `#0204`'s jammed left tread was dragged from the East Stairs into Room 1B over `SUB-BUS B-14 // HATCH 04`. | Links from `CUE-005` (Upper Gallery) to `CUE-003` & `CUE-006` (Room 1B) |
| **`CUE-003`** | **Over-Painted `RM 1B` Placard Ghost Stencil & Torn `03:14 UTC` Seal** | Room 1B Exterior Jamb `(2.96, 1.60, 2.74)` & Rack `(4.70, 1.15, 7.85)` | `preface_residential_sector.glb` / `Open_Portal_1B` / `UV_PLACARD_1B` `(0.758..0.984, 0.883..0.988)` | Standard municipal bot charging bay placard (`RM 1B // BOT SUBSTATION`). | Faint ghost stencil bleeding through underneath reads **`SEC-04 // TELEMETRY RELAY [RESTRICTED // CLR-4 ONLY]`**, and the red security seal on the bottom right is torn across **`SEAL: 2026-10-19 // 03:14`**. | Matches `03:14 UTC` timestamp in `CUE-001` & `CUE-006` |
| **`CUE-004`** | **Pried `APT 201` RFID Bezel & Scratched-Out `CLR-4 [REVOKED]` Code** | Apt 201 Exterior Jamb `(-12.66, 5.80, 2.64)` | `preface_residential_sector.glb` / `Open_Portal_201` / `UV_PLACARD_201` `(0.516..0.742, 0.762..0.867)` | Standard Lead Tech residential nameplate (`APT 201 // TECH-2`). | Left metallic bezel edge has 4 bright **screwdriver pry gouges** (`roughness 0.18, metallic 0.92`) where Rostov tapped the 13.56 MHz door bus; sub-line shows **`CLR-4 [REVOKED]`** struck through in red and re-stamped `-> TECH-2 // 13.56MHz`. | Explains `CLR-4` access in `CUE-003` & RFID bus tap in `CUE-007` |
| **`CUE-005`** | **Apt 202 Quartermaster `BUS B-14` Tag & Reserve Cell Staging** | Apt 202 Exterior Jamb `(9.36, 5.80, 2.64)` & Desk `(10.70, 5.10, 7.20)` | `preface_residential_sector.glb` / `Open_Portal_202` / `UV_PLACARD_202` `(0.758..0.984, 0.762..0.867)` | Neighboring Quartermaster suite (`APT 202 // QUARTERMASTER`) with a spare battery on the desk. | Placard sub-line explicitly tags **`SEC-04 // BUS B-14`**—the upper-level termination of the 48.2 kW `03:14 UTC` load spike before `#0204` was hauled down the adjacent East Stairwell (`X = +10.65m`). | Connects `CUE-001` (Bus B-14 spike) to `CUE-002` (East Stairwell drag trail) |
| **`CUE-006`** | **Unit `#0204` ("Kelvin" / "Puddle") Re-Designation & Actuator Fault** | Room 1B Substation Bay `(5.60, 0.06, 6.00)` | `char_bot_r2_05_livery_03_kelvin.glb` + `preface_playable_area.gd` `[E]` / `[R]` telemetry | Science department drone `Kelvin #0204` (`D-03 // SCIENCE`) running thermal diagnostics in Room 1B. | Parked directly over `SUB-BUS B-14 // HATCH 04` at the end of the `CUE-002` skid trail; 13.56 MHz RFID scan & `[E]` query report **`-18% left tread actuator drag since 2026-10-19 03:14 UTC`** and **`[WARN: ID PUDDLE_0204 OVERWRITTEN]`**. | Central subject of `CUE-001`, `CUE-002`, `CUE-003`, `CUE-007` |
| **`CUE-007`** | **Pegboard `D-03 HYDRO [REMOVED]` Ghost Mark, `RFID BUS TAP` Card & Thermal Jelly** | Apt 201 Workbench Pegboard `(-8.45, 5.64, 8.13)` & Bench `(-7.64, 5.12, 7.58)` | `preface_residential_sector.glb` / `UV_WORKBENCH_PEGBOARD` `(0.512..0.748, 0.638..0.720)` + `prop_jelly_01.glb` | Missing tool rack outline on pegboard, pinout diagram, and standard thermal paste canister. | Clean oxidation ghost rectangle labeled **`D-03 HYDRO [REMOVED]`** where `#0204`'s original hydro/cryo service cradle hung; pinned schematic shows **`RFID BUS TAP: PIN_RESET -> B14 / 03:14 MEM LOG / UNIT #0204`** alongside cryo-grade Thermal Jelly salvaged from the breach. | Links `CUE-004` (bezel tap) to `CUE-001` (bench dump) & `CUE-006` (`#0204`) |

---

## 3. Detailed Forensic Breakdown & Cross-Verification

### `CUE-001` — Apt 201 Workbench Surface (`UV_WORKBENCH_TOP`)
* **Exact Location:** `Tech_Apartment_Upper/Apartment_Workbench` at World `(-8.45, 5.12, 7.75)`.
* **Visual Elements Baked in `residential_atrium_and_apartment_atlas_*.png` (`x: 768..1024, y: 512..652`):**
  1. **Wear-Polished Forearm Rest:** Along the front `-Z` edge (`y: 620..650`), the honey-teak wood is worn lighter (`RGB 162, 130, 98`) and smoother (`ORM roughness = 0.26`) where Rostov leans while working.
  2. **Blown 3rd Capacitor Coil (`C3 [BLOWN]`):** Two intact copper SMD footprints (`C1`, `C2`) sit beside a third pad obliterated by a circular carbonized plasma-arc scorch mark (`#14100E` center, `#4E3420` flux ring, `ORM roughness = 0.84`).
  3. **Scratched Serial & Tally:** `A7-0204-MEM // III` etched into the upper-left wood grain above the scorch ring, representing three failed attempts to dump `#0204`'s protected memory sector before the capacitor blew.
  4. **Taped Oscilloscope Calibration Note:** Held by diagonal amber Kapton tape strips (`x: 892..1016, y: 520..636`), displaying a cyan 13.56 MHz / 412 Hz spike waveform (`03:14 UTC B-14`), `#0204: PUDDLE -> KELVIN`, `COIL C3 DUMP!`, and a hand-drawn red arrow pointing directly at the `C3` scorch ring.
* **Diegetic `[E]` Verification (`Workbench_DiagnosticTerminal`):**
  > `OSCILLOSCOPE [2026-10-19 03:14 UTC] // 13.56MHz / 412Hz spike on BUS B-14 (48.2 kW). Unit #0204 re-keyed [PUDDLE -> KELVIN]; Coil C3 blown during A7-0204-MEM dump.`

### `CUE-002` — East Stairwell to Room 1B Skid & Coolant Trail (`UV_FLOOR_SKID_TRAIL`)
* **Exact Location:** Flush floor forensic geometry (`y = 0.123m..0.125m`) running in three connected segments from `(8.80, -3.40)` -> `(5.20, 0.85)` -> `(4.65, 3.85)` -> `(5.60, 6.20)`.
* **Visual Elements Baked in `residential_atrium_and_apartment_atlas_*.png` (`x: 768..1024, y: 652..740`):**
  1. **Single-Locked-Tread Cleat Marks:** Only the left track lane leaves dark vulcanized rubber skid cleats (`#22262C`) accompanied by a bright metallic score line (`ORM roughness = 0.22, metallic = 0.75`), proving the bot was dragged or limped with a seized left actuator rather than rolling normally.
  2. **Cryo-Coolant Drip Trail:** Alternating violet-indigo (`RGB 92, 82, 168`) and cyan (`RGB 74, 134, 162`) fluid spots with low specular roughness (`ORM roughness = 0.16`) and subtle luminescence, matching the thermal jelly/cryo-fluid signature.
  3. **Sub-Bus Floor Stencil:** `SUB-BUS B-14 // HATCH 04 [DRAG TRACE #0204]` stamped at the termination under `Kelvin #0204`.
* **Diegetic `[E]` Verification (`Sweep #0812` & `Kelvin #0204`):**
  * `Sweep #0812`: `"Mezzanine patrol 72% complete. Logged single-tread rubber skid & cryo-coolant trace from East Stairwell into RM 1B."`
  * `Kelvin #0204`: `"Left tread actuator drag (-18% since 2026-10-19 03:14 UTC). Sub-Bus B-14 Hatch 04 sealed. [WARN: ID PUDDLE_0204 OVERWRITTEN]."`

### `CUE-003` & `CUE-004` — Tampered Doorway Placards (`UV_PLACARD_1B` & `UV_PLACARD_201`)
* **Exact Locations:**
  * `Open_Portal_1B` placard at `(2.96, 1.60, 2.74)` (`x: 776..1008, y: 904..1012` in atlas)
  * `Open_Portal_201` placard at `(-12.66, 5.80, 2.64)` (`x: 528..760, y: 780..888` in atlas)
* **Forensic Details:**
  * On `RM 1B`, warm-amber ghost lettering (`#7E6448` / `#8A543E`) bleeds through the dark over-paint: **`SEC-04 // TELEMETRY RELAY`** and **`[RESTRICTED // CLR-4 ONLY]`**, while the bottom-right red security seal is physically torn in half across **`SEAL: 2026-10-19 // 03:14`**.
  * On `APT 201`, four bright diagonal screwdriver gouges scar the left bezel edge, and the clearance line **`CLR-4 [REVOKED]`** is crossed out with a red slash and replaced by **`-> TECH-2 // 13.56MHz`**.

---

## 4. Continuity Verification Checklist (Rules for All Future Sectors)

To preserve the integrity of Aegis-1's hidden visual narrative through the end of production, every artist and designer must enforce these rules before committing any texture or scene update:

1. **Zero Decorative/Random Grime on Tiled UVs:**
   * World-tiled architectural regions (`UV_WALL_APT`, `UV_WALL_ATRIUM`, `UV_FLOOR_SLATE`, `UV_WOOD_WALNUT`, `UV_STEEL_TRIM`) must **never** contain text stamps, room numbers, scorch marks, or unique decals that would repeat across multiple walls or floor bays.
2. **Every Visual Clue Must Have a `CUE-###` Entry:**
   * Any non-repeating visual anomaly (scorch mark, pried panel, ghost stencil, fluid trail, sticky note, cable splice) must be placed on a dedicated non-tiled UV sub-rect and logged in this file with exact world coordinates `(x, y, z)`.
3. **Two-Way Causal Linking (No Orphan Clues):**
   * Every new `CUE-###` entry must link to at least one **upstream physical cause** and one **downstream physical or telemetry effect** (e.g., `03:14 UTC` timestamp -> Bus B-14 load spike -> blown `C3` coil -> `#0204` left-tread drag -> torn Room 1B seal).
4. **Layer A vs. Layer B Separation:**
   * Surface UI prompts and standard NPC/bot greetings must maintain the plausible mundane cover story (Layer A), while close visual inspection of textures, physical placement, and raw diagnostic readouts reveal the true Aegis-1 timeline (Layer B).

---

## 5. Reserved Registry Block for Upcoming Sectors

| Cue ID (Reserved) | Target Sector | Planned Forensic Link to `2026-10-19 // 03:14 UTC` Timeline |
| :--- | :--- | :--- |
| `CUE-008` | Sector-04 Service Bulkhead (`prop_service_door.glb` / `prop_door_pcba_terminal.glb`) | Loose Super-Wire jumper on `J4_HEADER` (`Pin_RESET`) & `supply_amperage = 7` drop caused by the 48.2 kW Bus B-14 shunt into Room 1B. |
| `CUE-009` | District-04 Hydroponics / Agri-Biosphere Bay | Empty docking cradle `#0204` (`PUDDLE`) with ground-off `D-04` serial plate and matching `2026-10-19` transfer manifest. |
| `CUE-010` | District-03 Cryo / Science Lab | Secondary containment canister matching the `A7-0204-MEM` dump checksum and `CLR-4` revocation order signed at `03:22 UTC`. |
