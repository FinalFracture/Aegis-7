# Reticle, Rotating Outer Starfield & RFID Sliding Doors QA ([t38u])

display=X11  failures=0

PASS | reticle_project_stretch_settings | mode=canvas_items aspect=expand
PASS | reticle_centered_1920x1080 | vp=(1920.0, 1080.0) reticle_center=(960.0, 540.0) expected=(960.0, 540.0) err=0.0000 px ray_dot=1.00000000
PASS | reticle_centered_1600x900 | vp=(1920.0, 1080.0) reticle_center=(960.0, 540.0) expected=(960.0, 540.0) err=0.0000 px ray_dot=1.00000000
PASS | reticle_centered_1280x800 | vp=(1920.0, 1080.0) reticle_center=(960.0, 540.0) expected=(960.0, 540.0) err=0.0000 px ray_dot=1.00000000
PASS | reticle_centered_1920x1080 | vp=(1920.0, 1080.0) reticle_center=(960.0, 540.0) expected=(960.0, 540.0) err=0.0000 px ray_dot=1.00000000
PASS | starfield_outer_cylinder_geometry | exists=true R=2200.0 m L=4800.0 m camera_far=6500.0 m
PASS | starfield_rotates_while_vessel_stationary | star_drot=0.0713 rad (4.09 deg) hab_dpos=0.000000 hab_drot=0.000000
PASS | starfield_pixels_visible_and_moving | changed_sky_sample_pixels=741
PASS | rfid_doors_count_6 | door_count=6
PASS | door_apt201_blocks_when_closed | door_z=2.75 player_stopped_at_z=2.33 open=false
PASS | door_apt201_opens_on_F_rfid_scan | open=true blend=1.000
PASS | door_apt201_walk_through_when_open | door_z=2.75 player_crossed_to_z=6.66
PASS | door_alcove2c_blocks_when_closed | door_z=-3.55 player_stopped_at_z=-3.13 open=false
PASS | door_alcove2c_opens_on_F_rfid_scan | open=true blend=1.000
PASS | door_alcove2c_walk_through_when_open | door_z=-3.55 player_crossed_to_z=-4.37
PASS | door_apt202_blocks_when_closed | door_z=2.75 player_stopped_at_z=2.34 open=false
PASS | door_apt202_opens_on_F_rfid_scan | open=true blend=1.000
PASS | door_apt202_walk_through_when_open | door_z=2.75 player_crossed_to_z=6.02
PASS | door_rm1a_blocks_when_closed | door_z=2.85 player_stopped_at_z=2.43 open=false
PASS | door_rm1a_opens_on_F_rfid_scan | open=true blend=1.000
PASS | door_rm1a_walk_through_when_open | door_z=2.85 player_crossed_to_z=6.15
PASS | door_rm1b_blocks_when_closed | door_z=2.85 player_stopped_at_z=2.43 open=false
PASS | door_rm1b_opens_on_F_rfid_scan | open=true blend=1.000
PASS | door_rm1b_walk_through_when_open | door_z=2.85 player_crossed_to_z=6.15
PASS | door_sector4_exit_blocks_when_closed | door_z=-8.90 player_stopped_at_z=-8.48 open=false
PASS | door_sector4_exit_opens_on_F_rfid_scan | open=true blend=1.000
PASS | door_sector4_exit_walk_through_when_open | door_z=-8.90 player_crossed_to_z=-12.20
