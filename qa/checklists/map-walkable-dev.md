# Map solid & walkable — dev stage checklist

Jared, 2026-11-03: make the whole playable map solid and walkable. The starting area, the observation-window glass section and the green stay as they are.
Rules: collider-only edits inside the starting area and the green, so visuals don't change. Don't touch the observation window (`_cut_observation_window` / `Mat_ObservationWindowGlass`). Don't delete the buried x 10.65 ramp collider. Each fix must pass a real-input walk; never move tests, thresholds or waypoints.
When the last box is checked, message QA-01 (navigation) and QA-02 (geometry) once, with priority false.

## Fix tasks (Gage, via Grok CLI)
- [x] T1 M-46: no code change needed on 370bc40. Real-input check: the old trap spot (10.2,-16.97) escapes 4/4, and a walk along the platform south of the shelter reaches (12.72,-16.88), 0.29 m from (12.8,-16.6). The direct route from (10.2,-16.3) stops on the shelter west wall at x 12.07, which is correct.
- [x] T2 NAV-09: no code change. (8.0,-18.22) escapes N/W/E (3/3). South is the docked maglev car body, a real obstacle.
- [x] T3 NAV-10: no code change. Jump plus forward from the platform at x 7..10 never mounts the car (y stays 0.2-0.36). The roof and the 1.6 m skirt can only be reached by spawning or dropping onto them.
- [x] T4 M-59: L1 corridor (-9.7..9.7, z -0.2) walks clean. The z +/-1 grid points sit inside the Rev C walls (sweep artifact). The tram shelter row is walkable (13..17, -16.9). One new finding is split out as T11.
- [x] T5 M-73: no code change. From (-13.55,-8.55), real input escapes E and N. The old target (-14.3,-9.3) is outside the shell, so stopping there is correct.
- [x] T6 M-70: real-input climb L1 (-1.15,-2) -> F2 -> landing y 2.46 -> F1 -> L2 y 4.08 passes; --qa-stairs 12/12 (4f39d99). The x 10.65 ramp was not touched.
- [x] T7 GEO-14: skipped, visual only. The walk surface over _533/_537/_556 is flat at y 0.170; the curb step is 0.15 m by design.
- [x] T8 GEO-16: skipped, visual only (the mesh floats 0.051 m). No collider fix applies.
- [x] T9 GEO-15: 370bc40. ext_ts4_dead_foliage is now solid; walking across it at z 1 is blocked at x -16.8. You can step up onto its low tier, like the neighbouring planters 1006/1007.
- [x] T10: 4f39d99 adds --qa-stairs, 12/12 pass. Egress itself was not edited (M-28 left open, since that would change an existing test).
- [ ] T11 NEW (needs Jared's OK, it removes a collider): M58_L2GalleryWestEdge (invisible box at x 5.50, y 4.75, z 0, 0.1x1.1x1.7) cuts the L2 gallery. The Rev C L2 slab is continuous across it (floor rays y 4.20 at x 4..9, z -0.6..0.7). Real input from (-9.7,4.08,0.3) heading +X stops at x 5.10, so the east L2 gallery can't be reached from the west.

## Sign-off
- [ ] Gage
