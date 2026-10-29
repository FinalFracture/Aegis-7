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
