# #3 Switchback stair set (stair core v1.1, approved 818f136)
Generator: `assets/src/stair_set_generator.py` (it asserts the riser check). glb: `godot/assets/models/stair_set_switchback.glb`, 2,480 tris, closed meshes, not placed anywhere.

**Origin:** the stair-core plan coordinates from `design/residential_stair_core_v1.py`, unchanged, so the glb drops in at identity.
- (0,0,0) is the building plan origin on the L1 finished floor; the core centreline is X = 0.
- X is axial, Y is up, and +Z is spinward.
- The core is clear over X −1.9..1.9 and Z −8.9 (shell face) .. −0.8 (corridor opening). The glb bounds are X ±1.9, Z −8.9..−0.8, Y 0..4.2 (the wall handrail brackets reach 4.47).

## Verified numerically against the plan
| | Plan | Model |
|---|---|---|
| Risers | 26 × 0.1615 = 4.20 | 26 risers, each 0.1615 (min = max), sum 4.200 |
| Flight 1 (west, X −1.9..−0.4, rises south) | 16 R, 15 T, run 4.20 | 16 R, 15 T × 0.28, run 4.20 (Z −3.2 → −7.4) |
| Flight 2 (east, X 0.4..1.9, rises north) | 10 R, 9 T, run 2.52 | 10 R, 9 T × 0.28, run 2.52 (Z −7.4 → −4.88) |
| Mid-landing | Z −8.9..−7.4, Y 2.585, soffit 2.335 | the same; top 2.5846, soffit 2.3346 |
| L2 landing | 4.08 deep, Y 4.20, slab 0.30 | Z −4.88..−0.8 (4.08), top 4.20, underside 3.90 |
| L1 bottom landing | 2.4 | Z −3.2..−0.8 = 2.40. This is the L1 floor slab, so it isn't modeled. |
| Z fit | 1.5 + 4.2 + 2.4 = 8.1 | 8.100 |

## Build
- **Flight 1:** cast white composite, closed below. This is the under-stair store, with a gunmetal door and an amber latch on the well side.
- **Flight 2:** bolted modular white steps with gunmetal stringer plates, open below for the L1 walk. The step soffit sits at or above the plan's soffit line, so headroom is at least the plan's.
- **Treads and lighting:** slate tread and landing finishes (15 mm), amber emergency nosing strips, and violet stringer LEDs (the plan's cyan, mapped to the family emissive).
- **Spin-down anchoring:** bolted gunmetal anchor plates on both core walls and the shell face, plus a floor shoe at the flight 1 base.
- **#4 interface:** alloy guard sockets on the well edges, the mid-landing edge and the L2 landing edge, plus alloy handrail wall brackets at 0.9 m above the nosings on both walls.
- **Manufacture and service:** the flights can be cast or bolted modules made in the cylinder. Sprocket uses lift #51, so the stair is human-first and needs no Sprocket features.

# #4 Stair glass guards + handrails
Generator: `assets/src/stair_guard_generator.py` (it imports `stair_set_generator` for the geometry). glb: `godot/assets/models/stair_guard_handrail.glb`, 2,816 tris, closed meshes, not placed anywhere. It uses the same origin as `stair_set_switchback.glb`, so the two overlay at identity. Sheet: `final_stair_guard_sheet.png`, which shows #3 and #4 together.

- **Guards:** 1.1 m laminated glass, 12 mm, in alloy clamps on alloy posts with a cap rail and a gunmetal shoe channel, plus an amber latch light on every panel. The panels are latched for spin-down and lift out for service. The glass material is `alphaMode BLEND`, double-sided.
  - Guard runs: the flight 1 well edge (X −0.37), the flight 2 well edge (X 0.37), the mid-landing well edge (Z −7.43, X −0.37..0.37) and the L2 landing edge (Z −4.83, X −1.89..0.37).
  - The corridor opening at Z −0.8 has no guard, because the plan shows none there.
- **Handrails:** rail top at 0.9 m, Ø40 alloy.
  - Wall side: continuous from the flight 1 foot, around the mid-landing walls (west wall, shell face, east wall) and up flight 2. It sits on saddles over the #3 wall brackets, plus 5 new landing-turn wall brackets.
  - Well side: on standoffs from the guard posts, continuous around the mid-landing turn.

## Checks
- **Guard height:** the guard top is 1.100 m above the nosing line on the flights and above the landing finish at every break point. The cap-rail top measures 1.097–1.100 m everywhere except where flight 2 starts, where the nosing line steps up one riser (0.1615 m) from the mid-landing.
- **Posts:** 14 posts on the 14 #3 Guard_Sockets, 0.000 m XZ offset. Each post base is the socket top; on flight 2 it is 6 mm higher, on the stringer plate.
- **Clashes:** I sampled 4,000 points per #4 part against every #3 solid (all of which are convex). There are no clashes, except the glass edge and shoe seating into the #3 Guard_Sockets, which is the bolt-in engagement by design.
