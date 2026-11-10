"""Rook: Tennis Tower plan data (spec Rev 2.9 §3-§4.6), building coordinates. Single source for the structure generators,
the preview assembly and ROOM_OWNERSHIP.md. Rects are (x0, x1, z0, z1)."""
FOOT = (-12, 140, 0, 79)
# stair cores (§4.6): id, type, rect
CORES = [("C-SW", "A", (30, 40.2, 15, 20.5)), ("C-SE", "A", (102.8, 113, 15, 20.5)), ("C-NW", "A", (30, 40.2, 58.5, 64)), ("C-NE", "A", (102.8, 113, 58.5, 64)),
         ("LS", "A", (71, 76.5, 9.5, 19.7)), ("LN", "A", (71, 76.5, 59.3, 69.5)), ("LW", "A", (24.5, 34.7, 39, 44.5)), ("LE", "A", (108.3, 118.5, 39, 44.5)),
         ("ST+S1", "B", (57, 64, 2.6, 13.2)), ("ST+S2", "B", (86, 92, 2.6, 13.2)), ("ST+N1", "B", (58, 64, 65.8, 76.4)), ("ST+N2", "B", (86, 92, 65.8, 76.4)),
         ("ST+E", "B", (119.5, 125.5, 50, 60.6)), ("ST-AQS", "B", (-6, 0, 10, 20.6)), ("ST-AQN", "B", (-6, 0, 58.4, 69)),
         ("ST-ARS", "B", (134, 140, 10, 20.6)), ("ST-ARN", "B", (134, 140, 58.4, 69))]
# r1: per-core asset overrides. ST-AQN / ST-ARN take tt_stair_core_b_m (Type B mirrored in Z), so like ST-AQS / ST-ARS their
# portals and F3 arrival face the foyer / arcade (S face Z 58.4, X -5.52..-3.38 / 134.48..136.62), not the N face that sits
# 0.02 m off the NW / NE plant-stack S walls (Z 69.025). A plain 180 deg turn would put the NE portal against the E facade.
CORE_ASSET = {"ST-AQN": "tt_stair_core_b_m", "ST-ARN": "tt_stair_core_b_m"}
# r1: F3 under-stand WC shells (tt_restroom_6, 5.4 x 2.4 m) centred in the 6.31 m clear bays between the Courts Aisle_Solid walls
# of the 7.5 m stand modules at X 47.75 / 95.25; backs 0.08 m inside the stand back line (S Z 9.072 / N Z 69.928), stalls face the rear concourse
RESTROOMS_F3 = [((47.75, 10.35), 180), ((95.25, 10.35), 180), ((47.75, 68.65), 0), ((95.25, 68.65), 0)]
# lift stacks: id, rect, door facing
LIFTS = [("Lift S", (66.5, 70.5, 11, 15), "+z"), ("Lift N", (66.5, 70.5, 64, 68), "-z"), ("Lift W", (26, 30, 34.5, 38.5), "+x"), ("Lift E", (113, 117, 34.5, 38.5), "-x")]
TREES = [(x, 8.5) for x in (57.5, 65.5, 84.5, 101.5)] + [(x, 70.5) for x in (57.5, 65.5, 84.5, 101.5)] + [(119.5, 30.5), (119.5, 48.5)]
TREES_W = [(23.5, 30.5), (23.5, 48.5)]
PLANT = [("SW", (-12, 0, 0, 10)), ("NW", (-12, 0, 69, 79)), ("SE", (128, 140, 0, 10)), ("NE", (128, 140, 69, 79))]
PT_X = [39.5 + 8*k for k in range(9)]; PT_Z = (24.5, 54.5)
AQ_Z = [3.5 + 9*k for k in range(9)]           # X 0 / X 30 column + transfer-truss lines
COURTS = [(48.5, 68.5, 27.5, 37.5), (74.5, 94.5, 27.5, 37.5), (48.5, 68.5, 41.5, 51.5), (74.5, 94.5, 41.5, 51.5)]
V_CL = (35, 57, 3, 8); COFFER = (0, 30, 21.5, 30.5)
WATER = dict(lap=(2.5, 27.5, .5, 21.5, 2.0), diving=(15, 28, 22, 34, 4.5), splash=(5, 17, 51, 62, .6), runout=(5, 23, 64, 71, 1.0))
RIVER_OUT, RIVER_IN = (1, 29, 47, 75), (4, 26, 50, 72)
RIVER = [(1, 29, 47, 50), (1, 29, 72, 75), (1, 4, 50, 72), (26, 29, 50, 72)]

# Rooms / zones (floor, id, name, rect, programme, spec §)
ROOMS = [
 # F1
 ("F1", "F1-FOY", "W foyer / main entrance hall", (-12, 0, 10, 69), "44 m doors Z 17.5..61.5, 2 desks, 8 kiosks, 6 m passage X -12..-6", "§3.6, §3.12.3-4"),
 ("F1", "F1-AQC", "Lobby / aquarium corridor", (0, 30, 34.5, 44.5), "tank X 1..23 acrylic Z 42.5, terrazzo, benches, plinths", "§3.12.1"),
 ("F1", "F1-POOL", "Lap pool + diving well hall (S deck +2.0)", (0, 30, 0, 34.5), "8-lane 25 m lap pool, 4.5 m diving well, 3 m + 1 m boards", "§3.6"),
 ("F1", "F1-LEIS", "Leisure water (N deck +1.0)", (0, 30, 44.5, 79), "lazy river, splash pool, slide towers T1/T2, runout pool", "§3.6, §3.12.6"),
 ("F1", "F1-CRT", "Spin Court hall (play area)", (39.5, 103.5, 24.5, 54.5), "4 glass court boxes 10 x 20 m, 3.0 m glass + net", "§3.11.5"),
 ("F1", "F1-CON", "F1 concourse ring + 5-row stands", (30, 113, 15, 64), "4 m concourse, stands 5 rows, 10 m lift gaps", "§3.1-3.2"),
 ("F1", "F1-BOWL", "Bowling (S band)", (30, 57, 0, 15), "8 lanes along X, acoustic wall X 57..58", "§3.7"),
 ("F1", "F1-SENT", "S entrance + lift lobby, free bay", (57, 77, 0, 15), "secondary entrance X 68..76, ST+S1, lift S, LS", "§3.7, §3.12.3"),
 ("F1", "F1-AXE", "Axe throwing (S band)", (77, 102, 0, 15), "2 rows x 4 bays, target walls X 84..85 / 101..102, ST+S2", "§3.7"),
 ("F1", "F1-WC-S", "WC R1-S", (102, 113, 0, 15), "restroom block", "§3.10"),
 ("F1", "F1-FOOD", "Food court (N band)", (44, 102, 64, 79), "counters + seating, ST+N1/N2, lift N, LN, N entrance X 68..76", "§3.7"),
 ("F1", "F1-WC-N", "WC R1-NW / R1-NE", (30, 44, 64, 79), "restroom blocks (NE = X 102..113)", "§3.10"),
 ("F1", "F1-ARC", "Arcade L1 (E band)", (113, 140, 0, 79), "arcade, ST-ARS/ARN, ST+E, LE, E entrance Z 33.5..41.5", "§3.7"),
 ("F1", "F1-PLANT", "Plant stacks (4 corners)", (-12, 140, 0, 79), "SW/NW pool plant, SE substation, NE AHU", "§3.7"),
 # F2
 ("F2", "F2-GAL", "Aquatic gallery (changing, lockers, viewing)", (-12, 0, 10, 69), "changing / lockers / showers, viewing walk, slide bridge", "§3.6"),
 ("F2", "F2-BRG", "Slide bridge + view bridge", (0, 24.5, 34.5, 60.4), "slide bridge Z 58..60.4 X 0..20, view bridge over corridor", "§3.6, §3.12.6"),
 ("F2", "F2-RINK", "Box-lacrosse / arena-soccer rink", (39.5, 103.5, 24.5, 54.5), "61 x 26 rink, boards, glass, gates, goals", "§4.1"),
 ("F2", "F2-CON", "F2 concourse ring + 5-row stands", (30, 113, 15, 64), "as F1", "§3.1-3.2"),
 ("F2", "F2-CLIMB", "Climbing & bouldering gym (S band)", (30, 113, 0, 15), "lead hall, 20 x 11.5 m wall, kids wall, bouldering, desk", "§3.7.1"),
 ("F2", "F2-GYM", "Gym (N band)", (44, 102, 64, 79), "gym floor, R2-NW/NE at the ends", "§3.7"),
 ("F2", "F2-WC", "WC R2-NW / R2-NE", (30, 44, 64, 79), "restroom blocks", "§3.10"),
 ("F2", "F2-ARC", "Arcade L2 (E band)", (113, 140, 0, 79), "arcade upper level", "§3.7"),
 # F3
 ("F3", "F3-BB", "Basketball hall", (39.5, 103.5, 24.5, 54.5), "2 courts 28 x 15 end to end, ball net overhead", "§4.1, §3.11.10"),
 ("F3", "F3-STAND", "F3 12-row stands + concourse", (24.1, 118.9, 9.1, 69.9), "12 rows all 4 sides, WC under stands", "§3.2, §3.10"),
 ("F3", "F3-TRK", "Running track loop", (0.7, 127.6, 0.7, 78.4), "1.8 m 2-lane ~400 m loop", "§3.9"),
 ("F3", "F3-DINE", "W dining terrace + bar", (-0.7, 24.1, 4, 75), "2 x 565 m2 dining, bar X 8..20 Z 35..44", "§3.9"),
 ("F3", "F3-CAB", "Cabanas + lounge view walk", (-12, -0.7, 18, 62), "8 cabanas X -11..-7, lounge X -7..-0.7", "§3.9"),
 ("F3", "F3-PLAY", "Kids' playground (E terrace)", (128.3, 140, 20.6, 58.4), "Rev 2.9 plan, benches X 127.2..127.7", "§3.12.6"),
 ("F3", "F3-SLNG", "S / N rear concourse lounges + climbing void", (3, 125, 2.5, 9.1), "lounges (N = Z 69.9..76.5), void guard X 35..57 Z 3..8", "§3.9"),
 ("F3", "F3-ROOF", "Glass Box envelope + roof", (-12, 140, 0, 79), "curtain wall, space frame, ridge, plant caps", "§3.5, §3.11"),
 # site
 ("SITE", "S-WT", "West Arrival Terrace", (-60, -12, 16, 64), "deck +4.0 HD, Fore cap portal level", "§3.8"),
 ("SITE", "S-EP", "East Plaza + Spine ramp", (140, 170, 16, 64), "deck +4.0 HD, E entrance, 1:20 ramp", "§3.8"),
]
