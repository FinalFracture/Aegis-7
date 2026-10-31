# #19 maglev vehicle — placement & clearances (Rook, Oct 30)
Car frame: x along track (car 1 cab at +X), z from track centre (world Z -19.90), world y.
- `ext_maglev_car_body_0N.glb` pivot = car-frame (x -0.069, y 0.06, z 0). `ext_maglev_magnet_module_0N.glb` pivot = car-frame (x -0.30 [01,03,05] / -0.20 [02] / -0.25 [04], y 0.06, z 0).
- Car 1 centre Xc: body at (Xc-0.069, 0.06, -19.90), magnets at (Xc+off, 0.06, -19.90), rot 0. Car 2 = rot 180 about Y at Xc2 = Xc - 12.306 (body Xc2+0.069, magnets Xc2-off); couplers 6 mm apart. Set length 24.31 m.
- Floor y 0.30 (= kerb top). Underframe y 0.25-0.30 (61 mm over the T-flange glow 0.163, >= 0.19 rule met over |z|<=0.60).
- Magnet_Arms |z| 0.575-0.70, y 0.064-0.254; Lev_Magnets hooks |z| 0.31-0.575, y 0.060-0.076 -> 12 mm under Stator_Lev (0.088), 13 mm outside Stator_Guide (0.562), 16 mm over bed (0.044 lines).
- Skirts |z| 1.17-1.23, y 0.06-0.254. Body widest |z| 1.33 (door sills) -> 70 mm to kerb face (Z -18.5); nothing over the kerb.
- Gage nodes: Door_L_01/02 (+Z), Door_R_01/02 (-Z) slide along X; Headlights, Tail_Lights, Destination_Screen, Lev_Magnets, Lev_Glow, Seats, Grab_Poles.
- Checks: each GLB clip + validate PASS; assembled 2 cars + 3x promoted T-Beam guideway + 6x kerb 02 at world placement: no overlaps/coplanar/open.
