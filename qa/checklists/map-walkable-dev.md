# Map solid & walkable — dev stage checklist

Jared, 2026-11-03: make the whole playable map solid and walkable. The starting area, the observation-window glass section and the green stay as they are.
Rules: collider-only edits inside the starting area and the green, so visuals don't change. Don't touch the observation window (`_cut_observation_window` / `Mat_ObservationWindowGlass`). Don't delete the buried x 10.65 ramp collider. Each fix must pass a real-input walk; never move tests, thresholds or waypoints.
When the last box is checked, message QA-01 (navigation) and QA-02 (geometry) once, with priority false.

## Fix tasks (Gage, via Grok CLI)
- [ ] T1 M-46: tram shelter glass collider leaves a clear lane to (12.8, -16.6)
- [ ] T2 NAV-09: tram platform south edge (~8, -18) can be walked off
- [ ] T3 M-59/NAV-10: TramRoofNoStand + rail tops (y 0.66, z ~-19) can't be stood on
- [ ] T4 M-59: stuck spots on L2/L1 corridor rows z ~ +/-1 (collider-only)
- [ ] T5 M-73: L1 NW corner wedge at (-12.97, -8.55) on RevC_Shell_L1_col (collider-only)
- [ ] T6 M-70: real-input stair-core climb verified (x 10.65 buried ramp NOT deleted)
- [ ] T7 GEO-14: collider-only part of the sunk promenade paving (_533/_537/_556), if any
- [ ] T8 GEO-16: collider-only part of the planter float at x -16.6, if any
- [ ] T9 GEO-15: ts4_dead_foliage_1004 gets a collider (collider-only)
- [ ] T10 Add a real --qa-stairs mode (plus M-28 egress Y bands)

## Sign-off
- [ ] Gage
