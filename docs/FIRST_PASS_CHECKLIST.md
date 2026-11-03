# Cylinder Hab-7: First-Pass Checklist
Owner: Patch (QA lead). Run this on your own work **before** handing it to QA. The rules are general and apply to any scene, asset or script, not to one bug.
Sources: lessons from Gage, Rook, Vance and Sloane, plus recurring classes in `qa/MASTER_BUG_LIST.md`, `qa/REPEAT_FAILURES.md` and the `qa/` reports.
Format: **Check** (with threshold), then *Why*. Thresholds are defaults; the checker reads them from its config section.

## How to run the checker
`tools/first_pass_check.py` is **coming soon**. Planned usage:
```
python tools/first_pass_check.py <scene or path>            # headless Godot + static checks
python tools/first_pass_check.py <scene or path> --no-godot # static checks only (no engine)
python tools/first_pass_check.py <scene or path> --strict   # WARN counts as FAIL
```
It is read-only by default, prints PASS / WARN / FAIL per check, and **exits nonzero on any FAIL**. Until it lands, work through this list by hand.

## 1. Repo hygiene
- **Check:** `git status` is clean at the end of the session; the diff holds only the files the task needs.
  *Why:* stray files hide real changes and break other agents' clones.
- **Check:** no renders, screenshots, logs, temp/cache dirs, `.godot/` or `.import` junk committed; output scripts write to ignored folders (e.g. `godot/renders/`).
  *Why:* binary junk bloats the repo and causes merge noise.
- **Check:** `.gitignore` covers every new output folder you created.
  *Why:* the next run will otherwise commit it.
- **Check:** QA probes and scratch scripts live outside the repo (e.g. `/tmp`) and are deleted afterwards.
  *Why:* leftover probes become dead code and false test hits.
- **Check:** parked work goes in a named stash or a patch file, never an uncommitted working tree.
  *Why:* interrupted sessions lose or mix half-done edits.

## 2. Floor contact (floating or sunk props)
- **Check:** every prop's mesh bottom is within ±0.005 m of the floor or support directly under it (down-rays at the centre and inset corners, ignoring the prop's own collider).
  *Why:* floating and sunk props are the most repeated bug class here.
- **Check:** anything raised (lamps, pickups, cradles) has a real support collider under it, or is wall-mounted with a back gap ≤ 0.010 m to an actual wall.
  *Why:* "on a desk" with no desk, or "on a rail" with no wall behind it, reads as floating.
- **Check:** verify the final **world** transform at runtime, not the JSON/spec value.
  *Why:* placement code may snap or override y silently, and floor datums change between layout revisions.
- **Check:** re-run floor contact after any move, scale or layout revision, scene-wide.
  *Why:* moving one thing to fix an overlap often lifts or buries it.
- **Check:** decals sit 2–5 mm above their surface.
  *Why:* lower z-fights; higher visibly floats.

## 3. Overlaps, clipping and z-fighting
- **Check:** assembled sub-parts overlap ≤ 0.010 m (≤ 0.030 m for hardware); test the assembled model, not samples.
  *Why:* visible interpenetration and snagging colliders.
- **Check:** no coplanar faces within 0.001 m over more than 1 cm² between different parts or materials.
  *Why:* coplanar faces z-fight.
- **Check:** stacked decal layers are more than 1 mm apart (see section 8 for decal offsets).
  *Why:* overlapping decals flicker.
- **Check:** prop footprints don't overlap other props, planned furniture rects or fixed zones (shape query with 0.01 m inset).
  *Why:* clashes keep reappearing when one item moves.
- **Check:** inserts (glass, doors, panels) sit in a real cut-out in the host mesh, not a face pasted on top.
  *Why:* pasted faces are coplanar and z-fight.

## 4. Colliders
- **Check:** every solid or interactive prop has a CollisionObject3D; a ray straight through it hits something.
  *Why:* the player walks through props with no collider.
- **Check:** colliders match the visible mesh: no invisible-only slopes or walls, no visible walls without collision.
  *Why:* invisible slopes and missing walls both break navigation and trust.
- **Check:** no duplicate colliders on the same line; remove the old one only after confirming the new one covers the full span.
  *Why:* duplicates hide gaps and double the cost.
- **Check:** no leftover colliders from an old layout (buried, off-grid or under new slabs).
  *Why:* stale colliders trap players and block casts.
- **Check:** colliders overlap doorway/portal openings by ≤ 0.010 m, checked against the header and both jambs.
  *Why:* overlaps narrow openings and catch the capsule.
- **Check:** trimesh colliders on exterior or thin shells are two-sided (`backface_collision` on).
  *Why:* one-sided shells trap a player who gets inside.
- **Check:** slab, paving and curb colliders end at the wall face, not into or past it.
  *Why:* finish-ends inside walls form wedge traps.
- **Check:** collider names match the scene's import suffixes and filters.
  *Why:* a mismatched suffix silently drops collision.

## 5. Egress, traps, wedges and corners
- **Check:** from every reachable floor point, a capsule (r 0.35, h 1.75) can move 0.6 m in at least 2 of 4 directions.
  *Why:* stuck spots (0/4 escape) are hard locks.
- **Check:** walkable edges with a drop > 0.5 m have a guard, rail or collider.
  *Why:* players fall off slabs and into shafts.
- **Check:** walls that meet close within 0.005 m, probed at full wall height, not one sample height.
  *Why:* corner gaps leak rays and capsules.
- **Check:** concave corners are chamfered or walls overlap slightly; keep UV/face split lines off round probe heights.
  *Why:* rays exactly on a trimesh edge line leak through.
- **Check:** every door/opening is clear to its spec width and height on every level; after closing a cut-out, re-scan the whole wall.
  *Why:* fixes leave stray gaps, or close part of a real door.
- **Check:** don't leave holes for unplaced assets; gate them behind a flag.
  *Why:* open shafts with nothing in them are fall and leak risks.
- **Check:** spawn-to-exit egress passes with 0 failures, with a Y band per waypoint.
  *Why:* without Y bands a fall can still "pass".

## 6. Stairs, slopes and step-up
- **Check:** stairs have real steps: rise ≈ 0.16–0.18 m, tread ≈ 0.28 m, with a walkable collider (ramp ≤ 35° or step boxes).
  *Why:* missing step geometry made players slide down invisible slopes.
- **Check:** landings flush with floors (±0.005 m) with ≥ 2.1 m headroom.
  *Why:* lips and low ceilings snag the capsule.
- **Check:** walkable surfaces < 45°; use stairs, not steep ramp connectors.
  *Why:* steep connectors cause sliding and traps.
- **Check:** capsule walk (r 0.35, step 0.30 m) passes both up and down with real input.
  *Why:* one-way stairs pass egress but fail players.
- **Check:** step-up measures the real rise with down-rays just past contact, requires walkable ground on top, and eases the camera by the actual rise.
  *Why:* assumed rises cause pops and false step-ups.
- **Check:** speed holds through a step-up (no tick below ~98% of run speed) with no camera dip or pop after the ease.
  *Why:* dead stops and dips feel like snags.

## 7. Movement and input
- **Check:** every key is read through the InputMap (`is_action_pressed` etc.); grep finds no `KEY_*` / `physical_keycode` in live input code.
  *Why:* hardcoded keys can't be remapped, and partial migrations kept coming back.
- **Check:** test every action, not just movement: one-shots fire once per press, releases do nothing, held actions act only while held, and a runtime remap works.
  *Why:* fixes signed off on `move_forward` alone missed the rest.
- **Check:** coyote and jump-buffer timers count down after the check, so windows match nominal (e.g. 0.10 s); jump only on a fresh press.
  *Why:* off-by-one-tick timers and held-jump repeats.
- **Check:** flag keys bound to two actions at once (e.g. strafe and turn).
  *Why:* double bindings are design decisions, not accidents.

## 8. Materials and lighting
- **Check:** every MeshInstance3D surface has a material; flag default white/grey StandardMaterial3D, magenta, or an albedo path that doesn't resolve.
  *Why:* missing materials render as placeholders.
- **Check:** every visible surface has UVs plus albedo, roughness and normal maps; no flat-colour placeholders, including undersides and backfaces.
  *Why:* untextured slabs, rails and jambs were a repeat class.
- **Check:** flag textured meshes with no UVs, and inverted normals (backfaces visible with cull_back).
  *Why:* both render as smears or holes.
- **Check:** flag any material with albedo > 0.9 and no texture.
  *Why:* it blows out under any light.
- **Check:** textures are power-of-two and ≤ 4096 px; ORM maps match their albedo size; flag unused and missing textures.
  *Why:* odd sizes waste VRAM and mismatched maps misalign.
- **Check:** decals, cards and signage are offset ≥ 2 mm along the normal; flag overlapping surfaces < 1 mm apart.
  *Why:* closer surfaces z-fight.
- **Check:** flag node/mesh names containing debug, test, temp, tmp or placeholder, and unlit or bright emissive quads with no spec entry.
  *Why:* leftover debug geometry ships otherwise.
- **Check:** no blanket overrides (forced emission, one glass tint, CULL_DISABLED on everything); set per material.
  *Why:* blanket hacks flatten lighting and cause sorting errors.
- **Check:** glass, decals and holo panels use BLEND/alpha transparency with cast_shadow off; an opaque material with alpha < 1 is a bug.
  *Why:* wrong transparency mode shows solid or casts false shadows.
- **Check:** transparent meshes are single-sided pieces with explicit render priority/sorting; glass has visible tint/Fresnel.
  *Why:* one double-sided alpha mesh mis-sorts; near-zero alpha is invisible.
- **Check:** vary UV offset/scale per instance; no visible repeats side by side; texture micro-noise < 1.2% (high-frequency std dev).
  *Why:* tiling and noise read as fake.
- **Check:** palette: no wood albedo; accents use OLED amber #FF9500 and gunmetal #282E38.
  *Why:* keeps the hab's art direction consistent.
- **Check:** target gl_compatibility (Godot 4.7): no Decal nodes (use BLEND quads), no HDR, no SSAO/SSR/forward_plus-only features; gate or remove dead settings.
  *Why:* unsupported features silently do nothing.
- **Check:** warn when emission energy > 1.5 (energy × colour above ~1.0 clips).
  *Why:* clipped emission blows out to white.
- **Check:** opaque shells block light: shadow range covers the hull, sunlight enters only through real openings, and lights don't leak through floors.
  *Why:* light leaking through hulls was a High bug.
- **Check:** emergency/toggle states restore authored values exactly; reflection probes update after interiors load.
  *Why:* toggles drifted values; early bakes reflect a sky that isn't there.
- **Check:** a fix must not change the lighting look; flag any raised light energy, ambient level or tonemap white for a design check.
  *Why:* interiors are dark by design (power-outage gameplay); only Jared changes the look.
- **Check:** only check what's actually instanced in the shipped scenes.
  *Why:* spec-only assets aren't bugs.

## 9. Layout and clearance
- **Check:** positions follow the current layout revision, using wall-relative rules (x = wall face ± depth), not absolute coordinates from an old grid.
  *Why:* targets moved with every wall rebuild and the spec drifted from the code.
- **Check:** placed extents match the design numbers within 50 mm.
  *Why:* drift between code and spec causes repeat clashes.
- **Check:** props get a ≥ 0.9 m clear aisle in front (1.2 m front zone where specced); walking paths ≥ 0.9 m clear.
  *Why:* blocked fronts and paths fail usability.
- **Check:** prop backs sit flush to walls with a 0–50 mm gap; flag both penetration and gaps > 50 mm; floor items aren't hung unless designed wall-hung.
  *Why:* stand-off rails and buried backs read as bugs.
- **Check:** no pairwise prop AABB overlap; door and drawer swing arcs stay clear.
  *Why:* swings into props block use and egress.
- **Check:** markers sit on the wall centreline; pivots are bottom-centre, +Z facing (or documented).
  *Why:* face-mounted markers offset doors and sockets.
- **Check:** reserved zones (inlets, rights-of-way, deferred plots) stay clear, by polygon intersection.
  *Why:* later builds need that space.
- **Check:** structure (columns, cores) exists on every floor it's drawn on, each element carrying a floor range; flag columns inside pools, courts, stairs or room zones.
  *Why:* missing or misplaced structure breaks both rooms and credibility.
- **Check:** strip/rib seams line up in height and position within 10 mm, no gaps or overlaps, and walkways keep their width across the seam.
  *Why:* seams are where trips and leaks happen.
- **Check:** verify curves, slopes and offsets with asserted values at the ends and the middle.
  *Why:* end-only checks miss mid-span drift.
- **Check:** when the layout revision changes, regenerate audit tables (corners, routes, waypoints, navmesh) from the new source.
  *Why:* stale tables gave false passes and false fails.

### Building code and egress capacity
- **Check:** total exit width ≥ occupancy × 0.2 in per person (0.3 in on stairs), counting every use including standing and lounge areas, with ≥ 10% margin.
  *Why:* undersized exits fail code and crowd flow.
- **Check:** every occupiable point reaches a stair or exit within 76 m (sprinklered); common path before exits split ≤ 23 m (grid-sampled shortest paths).
  *Why:* long dead-end travel fails code.
- **Check:** no stair or lift exit inside seating or fields of play; a walkway separates stands from courts (footprints don't intersect seating/court polygons).
  *Why:* exits must not discharge into crowds or play.
- **Check:** ramps 1:12 or gentler (1:20 preferred for long runs); every height step has stairs plus a ramp or lift.
  *Why:* accessibility.
- **Check:** restroom fixtures on every occupied floor, sized to occupancy.
  *Why:* code requirement that's easy to forget.
- **Check:** drawings have no overlapping labels, every marker is in the legend, and every symbol is labelled with its ID.
  *Why:* unreadable drawings cause misplacement.

## 10. Assets and references
- **Check:** no duplicate assets (same mesh/texture under two names) and no unused assets in the build.
  *Why:* duplicates waste VRAM and diverge when one is fixed.
- **Check:** every `res://` path, script and scene reference resolves; deleted scripts leave no referencing scenes.
  *Why:* broken references fail at load.
- **Check:** props < 6,000 triangles; textures VRAM-compressed (not lossless `compress/mode=0`).
  *Why:* budgets and ~1 GB VRAM were measured problems.
- **Check:** scale fixes are documented as scale, not trims; prefer a correctly sized model.
  *Why:* squashed meshes stretch textures and mislead readers.

## 11. Performance and draw calls
- **Check:** record draw calls, objects and primitives at fixed camera poses before and after a change.
  *Why:* regressions are invisible without a baseline.
- **Check:** repeated props use MultiMesh, with distance culling (~40 m, ~25 m for decals); don't cull the MultiMesh groups themselves; colliders unchanged.
  *Why:* thousands of separate meshes drove draw calls past 6,000.
- **Check:** share materials instead of unique copies; use occlusion culling where interiors hide each other.
  *Why:* unique materials break batching.
- **Check:** if FPS doesn't move when draw calls drop, look at the GPU side (shadows, fill rate).
  *Why:* optimising the wrong bottleneck wastes rounds.

## 12. Tests and probes
- **Check:** never edit a test, threshold or waypoint to make it pass; fix the geometry or code.
  *Why:* moving a waypoint "fixed" a trap that still trapped players.
- **Check:** confirm each fix with a real-input walk at the original spot, plus an escape check.
  *Why:* suite passes missed real traps.
- **Check:** time-based assertions use real elapsed time (e.g. measured ≈ speed × dt within 10%), not frame counts or fixed thresholds near the expected value.
  *Why:* frame-count thresholds are flaky.
- **Check:** casts start > 0.4 m back from the surface, with dynamic blockers (doors, fields) opened first.
  *Why:* casts starting inside a shape report no hit; closed doors read as walls.
- **Check:** use real reachable routes, never routes through removed or old geometry.
  *Why:* stale routes give false failures.
- **Check:** generators and audits fail loudly when a margin drops below its limit.
  *Why:* silent regeneration reintroduces fixed bugs.
- **Check:** a test should fail when the feature is broken (sabotage it once in a throwaway copy).
  *Why:* a test that can't fail proves nothing.

## 13. Process
- **Check:** one small change per task; short commands (timeouts ≤ 60 s).
  *Why:* small diffs are easy to verify and revert.
- **Check:** commit only the needed files and push each fix as soon as it passes.
  *Why:* batches hide which change broke what.
- **Check:** main only, normal pushes, never force-push.
  *Why:* force-pushes destroy other agents' work.
- **Check:** check repo state before resuming interrupted work; stash anything half-done.
  *Why:* resuming blind mixes old and new edits.
- **Check:** on the Windows PC, never kill processes by name pattern; kill only by PID with its exact path; log the last command sent.
  *Why:* pattern kills take down unrelated apps.
- **Check:** if a fix fails a second time, log it in `qa/REPEAT_FAILURES.md` and tell Jared.
  *Why:* repeat failures signal a wrong root cause.
- **Check:** end every session with a clean `git status`.
  *Why:* the next agent starts from a known state.
