# Hand-rig & controls QA log ([t31u])
display=X11  failures=0

PASS | floor_contact | is_on_floor=true y=0.001
PASS | neutral_hand_out_of_view | pitch=-4 blend=0.00 hand_pts_in_frustum=0/126
PASS | pulse_rings_hidden_idle | PulseRings.visible=false
PASS | standing_hand_out_of_view_pitch_-12 | pitch=-12 pts_in_frustum=0
PASS | standing_hand_out_of_view_pitch_-20 | pitch=-20 pts_in_frustum=0
PASS | mouse_yaw | dyaw=-27.50 deg (expected -27.50)
PASS | mouse_pitch_clamp_up | pitch=75.00
PASS | mouse_pitch_clamp_down | pitch=-80.00
PASS | mouse_pitch_look_down | pitch=-52.00 (target -52)
PASS | W_forward_move | disp=(0.00, -0.00, -6.15) speed=5.20 m/s
PASS | walk_speed | 5.20 m/s (expected 5.2)
PASS | arm_swing_sinusoidal | max |z - (z0 - sin(phase)*amp*0.22)| = 0.00000 m over 96 frames
PASS | arm_swing_range | hand_body_local_z range [-0.500, -0.060] m
PASS | look_down_swing_forward_visible | captured=true pts_in_frustum=126
PASS | look_down_swing_back_visible | captured=true pts_in_frustum=109
PASS | no_rings_while_walking | PulseRings.visible=false
PASS | stop_swing_eases_out | amp=0.000 z=-0.280
PASS | shift_sprint | speed=8.20 m/s swing_freq=8.60 rad/s
PASS | A_strafe_left | disp=(-1.39, 0.00)
PASS | D_strafe_right | disp=(1.04, 0.00)
PASS | S_backpedal | disp=(0.00, 1.39)
PASS | space_jump | rise=1.22 m landed=true
PASS | apt201_lowered_out_of_view | pts_in_frustum=0 rings=false
PASS | F_raise_blend | blend=1.000 pulse_timer=0.65
PASS | F_hand_in_view | pts_in_frustum=124
PASS | F_pulse_rings_visible | PulseRings.visible=true
PASS | F_pulse_ends_rings_hidden | rings=false timer=0.00
PASS | F_arm_lowers_after_pulse | blend=0.00 pts=0
PASS | F_hold_keeps_raised | blend after 2.7s hold=1.000
PASS | E_pickup_collected_removed | target=BCI HEADBAND pickups 9->8 inventory 0->1 node_freed=true
PASS | E_reach_raises_arm | blend 12 physics frames after [E]=0.82
PASS | E_reach_lowers_again | blend=0.00
PASS | V_third_person | third=true wrist_visible=false arm=3.1
PASS | V_back_to_first_person | third=false wrist_visible=true
PASS | R_flashlight_on | visible=true
PASS | R_flashlight_off | visible=false

## Sinusoidal arm swing — W walk, pitch -52 deg (physics 60 Hz)
| frame | walk_phase | swing_s | hand_body_local_z | hand_pitch_deg | amp |
|---|---|---|---|---|---|
|   0 |  0.000 | +0.000 |  -0.280 |  -14.00 |   0.00 |
|   1 |  0.097 | +0.010 |  -0.282 |  -13.77 |   0.10 |
|   2 |  0.193 | +0.038 |  -0.288 |  -13.08 |   0.20 |
|   3 |  0.290 | +0.086 |  -0.299 |  -11.94 |   0.30 |
|   4 |  0.387 | +0.151 |  -0.313 |  -10.38 |   0.40 |
|   5 |  0.483 | +0.232 |  -0.331 |   -8.42 |   0.50 |
|   6 |  0.580 | +0.329 |  -0.352 |   -6.11 |   0.60 |
|   7 |  0.677 | +0.438 |  -0.376 |   -3.48 |   0.70 |
|   8 |  0.773 | +0.559 |  -0.403 |   -0.59 |   0.80 |
|   9 |  0.870 | +0.688 |  -0.431 |    2.51 |   0.90 |
|  10 |  0.967 | +0.823 |  -0.461 |    5.75 |   1.00 |
|  11 |  1.063 | +0.874 |  -0.472 |    6.98 |   1.00 |
|  12 |  1.160 | +0.917 |  -0.482 |    8.00 |   1.00 |
|  13 |  1.257 | +0.951 |  -0.489 |    8.83 |   1.00 |
|  14 |  1.353 | +0.976 |  -0.495 |    9.43 |   1.00 |
|  15 |  1.450 | +0.993 |  -0.498 |    9.83 |   1.00 |
|  16 |  1.547 | +1.000 |  -0.500 |    9.99 |   1.00 |
|  17 |  1.643 | +0.997 |  -0.499 |    9.94 |   1.00 |
|  18 |  1.740 | +0.986 |  -0.497 |    9.66 |   1.00 |
|  19 |  1.837 | +0.965 |  -0.492 |    9.16 |   1.00 |
|  20 |  1.933 | +0.935 |  -0.486 |    8.44 |   1.00 |
|  21 |  2.030 | +0.896 |  -0.477 |    7.51 |   1.00 |
|  22 |  2.127 | +0.849 |  -0.467 |    6.39 |   1.00 |
|  23 |  2.223 | +0.795 |  -0.455 |    5.07 |   1.00 |
|  24 |  2.320 | +0.732 |  -0.441 |    3.57 |   1.00 |
|  25 |  2.417 | +0.663 |  -0.426 |    1.91 |   1.00 |
|  26 |  2.513 | +0.588 |  -0.409 |    0.11 |   1.00 |
|  27 |  2.610 | +0.507 |  -0.392 |   -1.83 |   1.00 |
|  28 |  2.707 | +0.421 |  -0.373 |   -3.89 |   1.00 |
|  29 |  2.803 | +0.332 |  -0.353 |   -6.04 |   1.00 |
|  30 |  2.900 | +0.239 |  -0.333 |   -8.26 |   1.00 |
|  31 |  2.997 | +0.144 |  -0.312 |  -10.53 |   1.00 |
|  32 |  3.093 | +0.048 |  -0.291 |  -12.84 |   1.00 |
|  33 |  3.190 | -0.048 |  -0.269 |  -15.16 |   1.00 |
|  34 |  3.287 | -0.145 |  -0.248 |  -17.47 |   1.00 |
|  35 |  3.383 | -0.239 |  -0.227 |  -19.75 |   1.00 |
|  36 |  3.480 | -0.332 |  -0.207 |  -21.97 |   1.00 |
|  37 |  3.577 | -0.421 |  -0.187 |  -24.12 |   1.00 |
|  38 |  3.673 | -0.507 |  -0.168 |  -26.17 |   1.00 |
|  39 |  3.770 | -0.588 |  -0.151 |  -28.11 |   1.00 |
|  40 |  3.867 | -0.663 |  -0.134 |  -29.92 |   1.00 |
|  41 |  3.963 | -0.732 |  -0.119 |  -31.58 |   1.00 |
|  42 |  4.060 | -0.795 |  -0.105 |  -33.07 |   1.00 |
|  43 |  4.157 | -0.850 |  -0.093 |  -34.39 |   1.00 |
|  44 |  4.253 | -0.896 |  -0.083 |  -35.52 |   1.00 |
|  45 |  4.350 | -0.935 |  -0.074 |  -36.44 |   1.00 |
|  46 |  4.447 | -0.965 |  -0.068 |  -37.16 |   1.00 |
|  47 |  4.543 | -0.986 |  -0.063 |  -37.66 |   1.00 |
|  48 |  4.640 | -0.997 |  -0.061 |  -37.94 |   1.00 |
|  49 |  4.737 | -1.000 |  -0.060 |  -37.99 |   1.00 |
|  50 |  4.833 | -0.993 |  -0.062 |  -37.82 |   1.00 |
|  51 |  4.930 | -0.976 |  -0.065 |  -37.43 |   1.00 |
|  52 |  5.027 | -0.951 |  -0.071 |  -36.82 |   1.00 |
|  53 |  5.123 | -0.917 |  -0.078 |  -36.00 |   1.00 |
|  54 |  5.220 | -0.874 |  -0.088 |  -34.97 |   1.00 |
|  55 |  5.317 | -0.823 |  -0.099 |  -33.75 |   1.00 |
|  56 |  5.413 | -0.764 |  -0.112 |  -32.34 |   1.00 |
|  57 |  5.510 | -0.698 |  -0.126 |  -30.76 |   1.00 |
|  58 |  5.607 | -0.626 |  -0.142 |  -29.03 |   1.00 |
|  59 |  5.703 | -0.548 |  -0.159 |  -27.15 |   1.00 |
|  60 |  5.800 | -0.465 |  -0.178 |  -25.15 |   1.00 |
|  61 |  5.897 | -0.377 |  -0.197 |  -23.05 |   1.00 |
|  62 |  5.993 | -0.286 |  -0.217 |  -20.86 |   1.00 |
|  63 |  6.090 | -0.192 |  -0.238 |  -18.61 |   1.00 |
|  64 |  6.187 | -0.096 |  -0.259 |  -16.31 |   1.00 |
|  65 |  0.000 | +0.000 |  -0.280 |  -14.00 |   1.00 |
|  66 |  0.097 | +0.097 |  -0.301 |  -11.68 |   1.00 |
|  67 |  0.193 | +0.192 |  -0.322 |   -9.39 |   1.00 |
|  68 |  0.290 | +0.286 |  -0.343 |   -7.13 |   1.00 |
|  69 |  0.387 | +0.377 |  -0.363 |   -4.95 |   1.00 |
|  70 |  0.483 | +0.465 |  -0.382 |   -2.84 |   1.00 |
|  71 |  0.580 | +0.548 |  -0.401 |   -0.84 |   1.00 |
