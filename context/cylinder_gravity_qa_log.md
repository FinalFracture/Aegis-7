# Cylinder radial spin-gravity QA log ([t34u])

display=X11  failures=0  ring: R=10.0 m, L=20.0 m, center=(150.0, 30.0, 0.0), axis=(0.0, 0.0, 1.0), g(rho)=9.8*rho/R, orient rate=3.5 rad/s

PASS | step1_spawn_on_floor_theta0 | on_floor=true rho=10.121 theta=0.0
PASS | step1_full_360_traversed | travelled=366.5 deg (64.0 m) in 466 physics frames, sprint W
PASS | step1_stays_on_local_floor | on_floor 466/466 frames, max |rho - 10.121| = 0.0133 m
PASS | step1_basis_tracks_radial_up | min dot(basis.y, -radial_outward) = 0.99991 over the loop
PASS | step1_back_at_start_on_floor | theta=23.5 on_floor=true
PASS | step2_8_boxes_planted_0_to_315 | 8/8 boxes flat on local floor (rho 9.60 +/- 0.06, speed < 0.05, face-aligned > 0.995, drift < 3 deg) after a 1.6 m/s axis-ward kick
PASS | step3_box_transit_started | from theta=0.0 rho=9.606
PASS | step3_box_crossed_core_rho0 | min_rho=0.000 flipped=true
PASS | step3_box_gravity_flipped_planted_opposite | gravity dir before=(0.00, -1.00, 0.00) after=(0.00, 1.00, 0.00) theta=180.0 rho=9.596 speed=0.0001 face_align=1.0000
PASS | step3_player_E_starts_core_transit | transit_active=true
PASS | step3_player_crossed_core_rho0 | min_rho=0.000 flipped=true
PASS | step3_player_smooth_reorient | max basis rotation per physics frame = 0.0583 rad (limit 0.0593, 180 deg in ~0.90 s)
PASS | step3_player_on_opposite_floor_flipped | on_floor=true theta=180.0 rho=10.120 body_up=(-0.00, -1.00, 0.00) dot(up_before)=-1.000 body_align=1.0000 camera_pivot_x_align=1.0000
PASS | step3_walk_on_flipped_floor | walked 66.7 deg (11.64 m) along the new floor, on_floor=true

## Step 1 - 360 deg sprint walk milestones

| milestone | frame | theta_deg | rho_m | on_floor | basis_y . local_up | basis_y world |
|---|---|---|---|---|---|---|
| 90 deg | 118 | 102.8 | 10.126 | true | 0.99991 | (-0.98, -0.21, 0.00) |
| 180 deg | 232 | 192.5 | 10.128 | true | 0.99991 | (0.20, -0.98, 0.00) |
| 270 deg | 343 | 283.0 | 10.128 | true | 0.99991 | (0.98, 0.21, 0.00) |
| 360 deg | 458 | 12.6 | 10.128 | true | 0.99991 | (-0.21, 0.98, 0.00) |

## Step 2 - ring boxes after settle + 1.6 m/s axis-ward kick (300 physics frames)

| box | home_theta | theta_now | rho_center | speed_m_s | face_align | drift_deg |
|---|---|---|---|---|---|---|
| RingBox_000 | 0 | 0.00 | 9.610 | 0.0001 | 1.00000 | 0.00 |
| RingBox_045 | 45 | 45.00 | 9.610 | 0.0001 | 1.00000 | 0.00 |
| RingBox_090 | 90 | 90.00 | 9.610 | 0.0000 | 1.00000 | 0.00 |
| RingBox_135 | 135 | 135.00 | 9.610 | 0.0001 | 1.00000 | 0.00 |
| RingBox_180 | 180 | 180.00 | 9.610 | 0.0000 | 1.00000 | 0.00 |
| RingBox_225 | 225 | 225.00 | 9.610 | 0.0000 | 1.00000 | 0.00 |
| RingBox_270 | 270 | 270.00 | 9.610 | 0.0000 | 1.00000 | 0.00 |
| RingBox_315 | 315 | 315.00 | 9.610 | 0.0001 | 1.00000 | 0.00 |
