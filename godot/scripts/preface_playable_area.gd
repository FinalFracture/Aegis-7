class_name PrefacePlayableArea
extends Node3D
## Aegis-7 // Cylinder Hab-7 — Playable 2-Story Preface Residential Sector (press F5).
## - Portable `res://` asset resolution (BUG-02), locked #05 Hammerhead department bots (BUG-05),
##   live looping animations (BUG-04), null-mesh guard (BUG-07), static collisions + walkable
##   CharacterBody3D 1st/3rd-person controller (BUG-03), interactive pickups / bot queries /
##   #04 Wrist RFID pulse + diegetic HUD (BUG-06).
## - [t3u] grounded low-key lighting, controlled saturation, single eye-level room placards.
## Command-line flags (after `--`): `--render-all` (4 showcase cams), `--validate-only`, `--capture-f5-hud`, `--qa-exterior-render`, `--qa-nav-reach`, `--qa-player-exit`, `--qa-egress`.

const SECTOR_GLB_PATHS := [
	"res://assets/models/environments/preface_residential_sector.glb",
	"res://assets/models/preface_residential_sector.glb",
	"res://assets/models/environments/preface_residential_two_story_block.glb"
]
# Rev C stair core (M-70). Same building-plan origin as the sector GLB, so both mount at identity.
const STAIR_SET_GLB := "res://assets/models/stair_set_switchback.glb"
const STAIR_GUARD_GLB := "res://assets/models/stair_guard_handrail.glb"
const CYLINDER_MAP_PATHS := [
	"res://assets/models/env_cylinder_hab7_fullscale_map.glb",
	"res://assets/models/environments/env_cylinder_hab7_fullscale_map.glb"
]
const WRIST_04_PATHS := [
	"res://assets/models/props/wrist_rfid/prop_wrist_rfid_winner_01_neural_tendon_sleeve.glb",
	"res://assets/models/prop_wrist_rfid_winner_01_neural_tendon_sleeve.glb",
	"res://assets/models/props/wrist_rfid/prop_wrist_rfid_r1_04.glb"
]
const PICKUP_WIRE_PATHS := [
	"res://assets/models/props/pickups/prop_super_wire_spool.glb",
	"res://assets/models/prop_super_wire_spool.glb"
]
const PICKUP_BATT_PATHS := [
	"res://assets/models/props/pickups/prop_pickup_battery_charge.glb",
	"res://assets/models/prop_pickup_battery_charge.glb"
]
const PICKUP_BCI_PATHS := [
	"res://assets/models/props/pickups/prop_bci_headband.glb",
	"res://assets/models/prop_bci_headband.glb"
]
const PICKUP_JELLY_PATHS := [
	"res://assets/models/prop_jelly_01.glb",
	"res://assets/models/props/pickups/prop_pickup_thermal_jelly.glb"
]
# Locked #05 Hammerhead stereo-scanner winner liveries (first entry = canonical).
const BOT_SPROCKET_PATHS := [
	"res://assets/models/char_bot_r2_05_livery_01_sprocket.glb",
	"res://assets/models/characters/char_bot_r2_05_livery_01_sprocket.glb"
]
const BOT_SWEEP_PATHS := [
	"res://assets/models/char_bot_r2_05_livery_02_sweep.glb",
	"res://assets/models/characters/char_bot_r2_05_livery_02_sweep.glb"
]
const BOT_KELVIN_PATHS := [
	"res://assets/models/char_bot_r2_05_livery_03_kelvin.glb",
	"res://assets/models/characters/char_bot_r2_05_livery_03_kelvin.glb",
	"res://assets/models/characters/char_bot_r2_05_livery_03_quasar.glb"
]
const BOT_PUDDLE_PATHS := BOT_KELVIN_PATHS  # Legacy alias: D-03 is SCIENCE (Kelvin), not Hydro.
const BOT_CLOVER_PATHS := [
	"res://assets/models/char_bot_r2_05_livery_04_clover.glb",
	"res://assets/models/characters/char_bot_r2_05_livery_04_clover.glb"
]
const COMMUTER_PATHS := [
	"res://assets/models/char_citizen_commuter.glb",
	"res://assets/models/characters/char_citizen_commuter.glb"
]
const ROSTOV_PATHS := [
	"res://assets/models/winners/char_crew_winner_01_aegis7_commander.glb",
	"res://assets/models/char_crew_r1_02.glb",
	"res://assets/models/characters/char_crew_r1_02.glb"
]
const TEX_DIRS := [
	"res://assets/textures/preface",
	"res://assets/textures/residential",
	"res://assets/textures/wrist_rfid",
	"res://assets/textures",
	"res://assets/textures/character",
	"res://assets/textures/cylinder_interior",
	"res://assets/textures/buildings"
]
const OUT_DIRS := ["res://renders/preface"]
const QA_DIR := "res://renders/qa"
const EXT_PLACEMENTS_PATH := "res://data/exterior_placements_v1_3.json"
const EXT_RENDER_DIR := "res://renders/queue_2026-10-31"
const EXT_RENDER_SETTLE_FRAMES := 30
const EXT_RENDER_HOLD_FRAMES := 10
const EXT_KIND_GROUND := 0
const EXT_KIND_SOLID := 1
const EXT_KIND_CAR := 2
const EXT_KIND_DECAL := 3
const EXT_SNAP_ABOVE := 0.3
const EXT_SNAP_DEPTH := 12.0
const EXT_CORNER_INSET := 0.05
# Corner samples that only clip a rail (east guardrail top is y 1.245) must not lift the prop.
const EXT_SUPPORT_LIFT := 0.40
const EXT_DECAL_LIFT := 0.005
# Plan is x -47..47, z -26..40.5. Two metres of margin, deck top matching PromenadePlazaDeckSlab.
const EXT_GROUND_X0 := -49.0
const EXT_GROUND_X1 := 49.0
const EXT_GROUND_Z0 := -28.0
const EXT_GROUND_Z1 := 42.5
const EXT_GROUND_TOP_Y := 0.12
const EXT_GROUND_THICK := 0.2

const CAMERAS := [
	{"name": "cam_01_top_floor_apartment_open_portal", "pos": Vector3(-6.55, 5.72, 4.85), "target": Vector3(-10.45, 5.05, 6.35), "fov": 58.0, "fp_wrist": true},
	{"name": "cam_02_two_story_atrium_staircase_and_sweep_bot", "pos": Vector3(-6.20, 5.95, 2.05), "target": Vector3(5.80, 2.55, -3.20), "fov": 58.0, "fp_wrist": false},
	{"name": "cam_03_open_side_rooms_and_puddle_substation", "pos": Vector3(3.65, 1.85, 0.35), "target": Vector3(4.65, 1.25, 6.50), "fov": 56.0, "fp_wrist": false},
	{"name": "cam_04_ground_concourse_open_exit_and_faction_bots", "pos": Vector3(-2.35, 2.05, -1.65), "target": Vector3(0.15, 1.35, -8.85), "fov": 55.0, "fp_wrist": false}
]

# --qa-exterior-render. Eye, then look-at. Saved as item4_<name>.png.
const EXT_RENDER_VIEWS: Array[Dictionary] = [
	{"name": "shelter_platform", "pos": Vector3(15.0, 1.7, -8.0), "at": Vector3(15.0, 1.0, -18.0)},
	{"name": "plaza_ramp", "pos": Vector3(4.0, 1.7, -8.0), "at": Vector3(12.0, 0.5, -18.0)},
	{"name": "canal_edge", "pos": Vector3(0.0, 3.0, -15.0), "at": Vector3(0.0, 0.0, -25.8)},
	{"name": "west_walkway", "pos": Vector3(-20.0, 1.7, 6.0), "at": Vector3(-18.0, 0.5, -6.0)}
]

# Player controller tuning
const SPAWN_POS := Vector3(-9.35, 4.25, 6.20)
const SPAWN_YAW_DEG := 28.0  # Spawn stays. APT 201's door is the Rev C face at (-3.0, 4.2, 0.8).
const WALK_SPEED := 5.2
const SPRINT_SPEED := 8.2
const JUMP_VELOCITY := 4.8
const GRAVITY := 9.8
const STEP_HEIGHT := 0.32
# [QA-05] Accel / friction, coyote + jump buffer, step-up camera ease, landing dip. No head bob.
const GROUND_ACCEL := 45.0
const GROUND_FRICTION := 35.0
const AIR_ACCEL := 8.0
const JUMP_BUFFER_S := 0.10
const COYOTE_S := 0.10
const STEP_EASE_S := 0.10
const LAND_DIP_M := 0.15 # [SYS-20] ~0.07 m visible dip at a typical ~4.4 m/s landing (scaled by fall/8, minus first-tick recovery)
const LAND_DIP_MIN_FALL := 3.0 # m/s
const MOUSE_SENS := 0.0024
const KEY_LOOK_SPEED := 2.2
const INTERACT_RANGE := 2.8
const TP_ARM_LENGTH := 3.1
const COLOR_CYAN := Color("#2E96B2")
const COLOR_AMBER := Color("#C47D2B")

# [t31u] Body-anchored first-person #04 arm: lowered at the player's left side (torso/yaw space, out of view
# when looking ahead), sinusoidal walk swing visible when looking down, raised into camera view on [F] / [E].
const RFID_PULSE_DURATION := 1.8
const INTERACT_REACH_DURATION := 0.65
const ARM_LOWERED_POS := Vector3(-0.26, 0.97, -0.28)       # _player_body local (wrist pivot)
const ARM_LOWERED_ROT_DEG := Vector3(-14.0, -22.0, -10.0)   # forearm extends from left hip forward-down to wrist
const ARM_RAISED_POS := Vector3(-0.20, -0.15, -0.42)       # _camera local (wrist pivot) [HW-02]
const ARM_RAISED_ROT_DEG := Vector3(24.0, -24.0, -10.0)
const ARM_RAISE_SPEED := 4.5
const WALK_SWING_Z := 0.22
const WALK_SWING_LIFT := 0.04
const WALK_SWING_PITCH_DEG := 24.0
const WRIST_PIVOT_IN_MODEL := Vector3(0.0, 0.195, 0.062)
const PITCH_MIN_DEG := -80.0
const PITCH_MAX_DEG := 75.0

# [t34u] Cylinder radial spin-gravity test ring (walk 360 deg, planted boxes, Coriolis core transit).
const RING_CENTER := Vector3(150.0, 30.0, 0.0)
const RING_AXIS := Vector3(0.0, 0.0, 1.0)
const RING_RADIUS := 10.0
const RING_LENGTH := 20.0
const RING_SEGMENTS := 72
const RING_SHAFT_Z := 7.0
const RING_BOX_Z := 3.0
const RING_WALK_Z := -3.0
const RING_BOX_SIZE := 0.8
const RING_ORIENT_RATE := 3.5          # rad/s max basis re-orientation (smooth 180 deg flip ~0.9 s)
const RING_FEET_OFFSET := 0.10         # body origin sits ~0.12 m below capsule bottom
const CORE_TRANSIT_DURATION := 4.0
const CORE_PAD_RADIUS := 1.4

# [t38u] Rotating distant outer starfield cylinder & RFID doors ([t45u] force-field)
const STARFIELD_CYL_RADIUS := 2200.0
const STARFIELD_CYL_LENGTH := 4800.0
const STARFIELD_ROT_SPEED := TAU / 240.0  # rad/s, one revolution per 4 minutes, about the world +X cylinder axis
const SCAN_ZONE_RANGE := 2.0          # [QA-HUB-01] max horizontal (XZ) metres, player body -> doorway centre at body height
const SCAN_FACING_DOT := 0.7          # [QA-HUB-01] min flattened camera-forward . dir-to-ScanZone
const DOOR_DISSOLVE_TIME := 0.8

# [t39u]-[t40u] Dynamic interior model despawn/respawn streaming
# [REAL-03] Interior volumes of the L1 side rooms, from the sector glb shells (Side_Room_East_Lounge =
# x[-12.25,-4.75] z[2.76,7.98]; Side_Room_West_Storage = x[0.75,8.25] z[2.76,8.16]; y[0.2,4.01]) inset by
# 0.15 m walls; the door wall's inner face is z = 2.85 + 0.15.
const ROOM_1A_INTERIOR := AABB(Vector3(-12.10, 0.0, 3.00), Vector3(7.20, 4.0, 4.83))
const ROOM_1B_INTERIOR := AABB(Vector3(0.90, 0.0, 3.00), Vector3(7.20, 4.0, 5.01))
const INTERIOR_DESPAWN_Z := -14.0   # [QA-FF-02] despawn farther out than respawn (hysteresis band 1 m)
const INTERIOR_RESPAWN_Z := -13.0

# [t45u] RFID force-field door (Rook's model + shader; swap paths here)
const FORCEFIELD_DOOR_GLB := "res://assets/models/rfid_forcefield_door.glb"
const FORCEFIELD_DOOR_SHADER := "res://shaders/forcefield_door.gdshader"
const DOORS_ROOT_NAME := "SectorRFIDForceFieldDoors"
const FF_OPEN_W := 1.50
const FF_OPEN_H := 2.45
const FF_FRAME_HALF_W := 0.91
const FF_FRAME_H := 2.61
const FF_DEFAULT_COLOR := Color(0.72, 0.35, 1.0, 1.0)   # in-game violet (shader default stays cyan)
const FF_EMITTER_ENERGY := {"EmitterStrip": 2.5, "EmitterNodes": 3.0, "Conduits": 1.6}
const FF_DEFAULT_OPACITY := 0.45
const FF_LIGHT_GREEN := Color("#3FAF6A")
# [Bulkhead Hub] Rook's door_hub_bulkhead.glb mounted beside every force-field door (door-local frame).
const DOOR_HUB_GLB := "res://assets/models/door_hub_bulkhead.glb"
const HUB_MOUNT_OFFSET := Vector3(1.14, 0.0, 0.15)
# Baked sector walls can't be cut at runtime, and the hub's recessed face (HubPanel z -0.020) would sit behind
# the wall face, so the hub stands off the wall by this much (bezel ~25 mm proud; liner hidden inside the wall).
const HUB_WALL_STANDOFF := 0.022
const HUB_AMBER := Color(1.0, 0.584, 0.0)
const HUB_GLOW_PARTS := ["LightPipe", "DisplayGlyphs", "ScanZone_Ring", "EqualBand", "Meniscus_L", "Meniscus_R", "CouplerHead_Ring", "DockPad_InductionRing"]
const HUB_ARM_PARTS := ["CouplerArm", "CouplerHead", "CouplerHead_Ring"]
const HUB_ARM_PIVOT := Vector3(0.25, 0.45, -0.025)
const HUB_ARM_STOWED_DEG := 90.0
const HUB_DOCK_POS := Vector3(0.25, 0.013, 0.47)
const HUB_DOCK_RADIUS := 0.30
const GLASS_QA_LAYER_BIT := 1 << 19
const HUB_BACKING_MAX_GAP := 0.05                    # [REAL-01] max allowed void behind the hub face
const HUB_BACKING_SAMPLE_X := [-0.15, 0.13, 0.40]   # hub-local bezel sample columns (bezel x -0.20..0.455)
const HUB_BACKING_SAMPLE_Y := [0.50, 1.10, 1.70]    # hub-local bezel sample rows (bezel y 0.40..1.80)
const HUB_SEAT_RAY_DEPTH := 0.30                     # [D670-04] wall search depth for seating the hub
const HUB_SEAT_MIN_HITS := 5                         # below this, a back-normal seat is not applied
const HUB_SEAT_GAP := 0.003                          # back face stands 3 mm off the real wall
const HUB_TANGENT_STEP := 0.01                       # [D670-04] wall-tangent step when a sample column overhangs the opening
const HUB_TANGENT_MAX := 0.35                        # furthest slide along hub local X
const SPROCKET_NODE := "Hammerhead05_Sprocket_0419_Engineering"
# Python UI (tools/door_field_ui.py) writes this file; the game polls it every DOOR_FIELD_POLL_SEC.
# [QA-FF-04/06] every run polls BOTH res://config/door_fields.json (godot/config/, gitignored) and
#            user://door_fields.json and applies whichever has the newer mtime (exports: user:// in practice).
const DOOR_FIELD_JSON_DEV := "res://config/door_fields.json"
const DOOR_FIELD_JSON_USER := "user://door_fields.json"
const DOOR_FIELD_POLL_SEC := 0.5
const FF_OCCUPANCY_DEPTH := 0.35       # [QA-HUB-01] thin box exactly in the opening, centred on the field plane
const FF_CLOSE_RETRY_SEC := 0.5
const FF_TEX_DIR := "res://assets/textures/force_field/"
const FF_STALL_STRENGTH := 0.40
const FF_STALL_TIME := 2.0
const FF_DENY_TIME := 0.3
const NAV_LINK_OFFSET := 0.8          # metres either side of a force-field door plane along its normal
const HATCH_NAV_ID := "HATCH_D204"    # field gate; link stays off until the D-204 field is open
const FF_BASE_STATIC := 0.35
const FF_BASE_JITTER := 0.004
const FF_BASE_ARC := 0.8
const FF_READY_CYAN := Color("#00E5FF")

var _arch_container: Node3D
var _props_container: Node3D
var _actors_container: Node3D
var _lights_container: Node3D
var _camera: Camera3D
var _world_env: WorldEnvironment

var _fp_wrist_holder: Node3D
var _fp_wrist_model: Node3D
var _rostov_root: Node3D

var _tex_cache: Dictionary = {}
var _batch_render: bool = false
var _validate_only: bool = false
var _capture_hud: bool = false
var _frame_counter: int = 0
var _render_step: int = 0
var _render_wait: int = 0

# Player
var _player_body: CharacterBody3D
var _camera_pivot: Node3D
var _spring_arm: SpringArm3D
var _third_person: bool = false
var _preset_active: int = -1
var _pitch: float = -0.08
# [QA-05] Mouse scale, jump buffer / coyote, and FP-camera step ease + landing dip.
var _mouse_sens: float = MOUSE_SENS
var _jump_buffer_t: float = -1.0
var _coyote_t: float = -1.0
var _step_ease_offset: float = 0.0
var _land_dip: float = 0.0
var _fp_cam_base_pos: Vector3 = Vector3.ZERO
var _fp_cam_base_set: bool = false
var _rostov_anim: String = ""

# Interactables & inventory
var _interactables: Array[Dictionary] = []
var _inventory: Dictionary = {"bci": 0, "jelly": 0, "wire": 0, "batt": 0}
var _inventory_max: Dictionary = {"bci": 0, "jelly": 0, "wire": 0, "batt": 0}
var _nearest: Dictionary = {}

# Lighting
var _sun: DirectionalLight3D
var _sun_base_basis: Basis  # [CYL-02] authored sun basis; _process orbits it with the starfield, not the drum
var _fill: DirectionalLight3D
var _task_lights: Array[OmniLight3D] = []
var _task_base: Array[Dictionary] = []
var _spot_lights: Array[SpotLight3D] = []
var _spot_base: Array[Dictionary] = []
var _emissive_mats: Array[Dictionary] = []
var _reflection_probe: ReflectionProbe
var _probe_rebake_frames: int = 0
var _emergency: bool = false
var _light_tween: Tween
var _light_tween_serial: int = 0
var _lighting_tween_active: bool = false
var _sun_energy_authored: float = 1.4
var _fill_energy_authored: float = 0.28
var _ambient_energy_authored: float = 0.30
var _ambient_color_authored: Color = Color(0.62, 0.68, 0.78, 1.0)
# Live values at the moment a restore starts. An interrupted flicker eases from here.
var _restore_sun: float = 1.4
var _restore_fill: float = 0.28
var _restore_amb_color: Color = Color(0.62, 0.68, 0.78, 1.0)
var _restore_amb_energy: float = 0.30
var _restore_task: Array[Dictionary] = []
var _restore_spot_energy: Array[float] = []
var _restore_emissive_energy: Array[float] = []
var _time: float = 0.0
# Grass slab UV domain, set for the duration of _add_recreation_grass_slab.
var _slab_uv_x0: float = 0.0
var _slab_uv_x1: float = 1.0
var _slab_uv_a0: float = 0.0
var _slab_uv_a1: float = 1.0

# RFID pulse rings + body-anchored arm kinematics ([t31u])
var _pulse_rings_root: Node3D
var _pulse_rings: Array[MeshInstance3D] = []
var _rfid_pulse_timer: float = 0.0
var _interact_reach_timer: float = 0.0
var _arm_raise_blend: float = 0.0
var _walk_phase: float = 0.0
var _walk_swing_amp: float = 0.0
var _flashlight: SpotLight3D
var _qa_hand: bool = false
var _qa_placement: bool = false
var _qa_ext_render: bool = false
var _ext_shot: int = 0
var _ext_shot_frames: int = -1
var _ext_scene_cache: Dictionary = {}
var _ext_shape_cache: Dictionary = {}
var _ext_shell_clipped: int = 0
## placement_assert_exterior.gd waits on this signal and the exterior_spawned meta flag.
signal exterior_spawned
var _qa_cyl: bool = false
var _qa_t38: bool = false
var _qa_ff_door: bool = false
var _qa_hub_shot: bool = false
var _qa_ts: bool = false
var _qa_exit: bool = false
var _qa_egress: bool = false
var _qa_last_slide_path: String = ""
var _qa_nav_reach: bool = false
var _qa_drawcalls: bool = false
var _ts_layer: CanvasLayer
var _ts_ui: TroubleshootSimpleUI
var _ff_shader: Shader = null
var _ff_tex_cache: Dictionary = {}
var _glb_cache: Dictionary = {}
var _door_json_mtime: int = -1
var _door_json_src: String = ""
var _door_json_hash: int = 0
var _door_json_poll_t: float = 0.0
var _door_json_recheck_until: float = 0.0
var _interiors_loaded: bool = true
var _interior_managed_count: int = 0
var _interior_detached_records: Array[Dictionary] = []
var _collected_pickup_ids: Dictionary = {}
var _pickup_templates: Dictionary = {}
var _ring_root: Node3D
var _starfield_cylinder: Node3D
var _rfid_doors: Array[Dictionary] = []
var _hatch_link: NavigationLink3D = null
var _hatch_open: bool = false
var _reticle_box: Control
var _reticle_center_px: Vector2 = Vector2(960.0, 540.0)
var _gravity_boxes: Array[Dictionary] = []
var _core_transits: Array[Dictionary] = []
var _player_transit: Dictionary = {}
var _qa_failures: int = 0
var _qa_log: PackedStringArray = PackedStringArray()

# HUD
var _hud: CanvasLayer
var _hud_zone: Label
var _hud_view: Label
var _hud_light: Label
var _hud_inv: Label
var _hud_prompt: Label
var _hud_toast: Label
var _hud_scan: Label
var _toast_t: float = 0.0
var _scan_t: float = 0.0


func _ready() -> void:
	# [QA-05] Project setting, then user://settings.cfg [input] mouse_sensitivity if present.
	_mouse_sens = float(ProjectSettings.get_setting("aegis/input/mouse_sensitivity", MOUSE_SENS))
	var sens_cfg := ConfigFile.new()
	if sens_cfg.load("user://settings.cfg") == OK and sens_cfg.has_section_key("input", "mouse_sensitivity"):
		_mouse_sens = float(sens_cfg.get_value("input", "mouse_sensitivity"))
	_camera = get_node_or_null("SceneCamera") as Camera3D
	_arch_container = _ensure_child("SectorArchitecture")
	_props_container = _ensure_child("InteractivePropsAndPickups")
	_actors_container = _ensure_child("Johnny5BotsAndCitizens")
	_lights_container = _ensure_child("SectorLightingRig")
	_world_env = get_node_or_null("WorldEnvironment") as WorldEnvironment
	# SSR is valid only on Forward+. Scenes leave it off so load does not warn; enable the duplicate here.
	if _world_env != null and _world_env.environment != null:
		var env: Environment = _world_env.environment.duplicate() as Environment
		env.ssr_enabled = RenderingServer.get_current_rendering_method() == "forward_plus"
		# [M-19] Black space. Reflections read the background, not a sky. Ambient is a colour.
		# Sun full-exposure is 1.4, so this ambient is lower than the old 0.42 sky fill.
		env.background_mode = Environment.BG_COLOR
		env.background_color = Color(0, 0, 0, 1)
		env.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
		env.ambient_light_color = Color(0.62, 0.68, 0.78, 1)
		env.ambient_light_energy = 0.30
		env.reflected_light_source = Environment.REFLECTION_SOURCE_BG
		env.tonemap_mode = Environment.TONE_MAPPER_FILMIC
		env.tonemap_exposure = 1.0
		env.tonemap_white = 4.0
		env.glow_enabled = true
		env.glow_intensity = 0.4
		env.glow_bloom = 0.05
		env.glow_hdr_threshold = 1.0
		_world_env.environment = env

	var all_args: PackedStringArray = OS.get_cmdline_args() + OS.get_cmdline_user_args()
	for arg: String in all_args:
		if arg == "--render-all" or arg == "--capture-screenshots" or arg == "--screenshots":
			_batch_render = true
		elif arg == "--validate-only" or arg == "--validate":
			_validate_only = true
		elif arg == "--capture-f5-hud":
			_capture_hud = true
		elif arg == "--qa-hand-controls":
			_qa_hand = true
		elif arg == "--qa-cylinder-gravity":
			_qa_cyl = true
			_qa_hand = true  # reuse the interactive (non-batch, non-validate) QA boot path
		elif arg == "--qa-reticle-stars-doors":
			_qa_t38 = true
			_qa_hand = true
		elif arg == "--qa-forcefield-door":
			_qa_ff_door = true
			_qa_hand = true
		elif arg == "--qa-player-exit":
			_qa_exit = true
			_qa_hand = true
		elif arg == "--qa-egress":
			_qa_egress = true
			_qa_hand = true
		elif arg == "--qa-door-hub-shot":
			_qa_hub_shot = true
			_qa_hand = true
		elif arg == "--qa-troubleshoot-simple":
			_qa_ts = true
			_qa_hand = true
		elif arg == "--qa-placement":
			_qa_placement = true
		elif arg == "--qa-exterior-render":
			_qa_ext_render = true
		elif arg == "--qa-drawcalls":
			_qa_drawcalls = true
			_qa_hand = true
		elif arg == "--qa-nav-reach":
			_qa_nav_reach = true
	if OS.get_environment("RENDER_ALL") == "1" or OS.get_environment("CAPTURE_SCREENSHOTS") == "1":
		_batch_render = true
	if OS.get_environment("VALIDATE_ONLY") == "1":
		_validate_only = true
	if _capture_hud or _qa_hand:
		_batch_render = false
		_validate_only = false
	if _qa_hand:
		_capture_hud = false
	if _qa_placement:
		_batch_render = false
		_validate_only = false
		_capture_hud = false
	if _qa_ext_render:
		_batch_render = false
		_validate_only = false
		_capture_hud = false
		if DisplayServer.get_name() != "headless":
			DisplayServer.window_set_size(Vector2i(1920, 1080))
	if DisplayServer.get_name() == "headless" and not _batch_render and not _qa_hand and not _qa_placement and not _qa_ext_render and not _qa_nav_reach:
		_validate_only = true
		_capture_hud = false
	if _qa_nav_reach:
		_batch_render = false
		_validate_only = false
		_capture_hud = false

	_assemble_open_doorless_sector()
	_populate_pickups_and_wrist_rig()
	_populate_johnny5_bots_and_citizens()
	_setup_sector_lighting()
	apply_camera_preset(0)
	if not _batch_render:
		_setup_player_controller()
		_build_hud()
		_update_hud()
		# Clean startup HUD without banner toast ([t22u] Todo #3)
	if _validate_only:
		print("[PrefacePlayableArea] Validate OK | interactables=", _interactables.size(), " | player=", _player_body != null)
	if _qa_hand:
		if _qa_cyl:
			_run_cylinder_gravity_qa.call_deferred()
		elif _qa_ff_door:
			_run_forcefield_door_qa.call_deferred()
		elif _qa_hub_shot:
			_run_door_hub_shot.call_deferred()
		elif _qa_t38:
			_run_reticle_stars_doors_qa.call_deferred()
		elif _qa_ts:
			_run_troubleshoot_simple_qa.call_deferred()
		elif _qa_exit:
			_run_qa_player_exit.call_deferred()
		elif _qa_egress:
			_run_qa_egress.call_deferred()
		elif _qa_drawcalls:
			_run_qa_drawcalls.call_deferred()
		else:
			_run_hand_controls_qa.call_deferred()
	# --qa-placement stays at the Apt 201 spawn _ready already uses, with interiors loaded.
	if _qa_placement:
		if not _interiors_loaded:
			_respawn_building_interiors()
		if _player_body != null:
			_player_body.global_position = SPAWN_POS
			_player_body.velocity = Vector3.ZERO
			_player_body.rotation_degrees = Vector3(0.0, SPAWN_YAW_DEG, 0.0)
	# D670-05. Baked mesh covers interior + exterior walk: ramp, platform, hatch, walkways.
	# Skip while tools/bake_navmesh.gd is the running script (its path is on OS.get_cmdline_args()).
	var baking_nav := false
	for nav_arg: String in OS.get_cmdline_args():
		if nav_arg.contains("bake_navmesh"):
			baking_nav = true
			break
	if not baking_nav and ResourceLoader.exists("res://assets/nav/preface_navmesh.tres"):
		var nav_region := NavigationRegion3D.new()
		nav_region.name = "PlayableNavRegion"
		nav_region.navigation_mesh = load("res://assets/nav/preface_navmesh.tres") as NavigationMesh
		add_child(nav_region)
		_add_forcefield_nav_links()
	if _qa_nav_reach:
		_run_qa_nav_reach.call_deferred()
	# After sector and prop setup. Both playable scenes use this script.
	_spawn_exterior_placements()


func _add_forcefield_nav_links() -> void:
	for door: Dictionary in _rfid_doors:
		var droot: Node3D = door.get("root") as Node3D
		if droot == null or not is_instance_valid(droot):
			continue
		var link := NavigationLink3D.new()
		link.name = "NavLink_" + String(door["id"])
		var normal := droot.global_transform.basis.z
		if normal.length_squared() < 0.0001:
			normal = Vector3.FORWARD
		else:
			normal = normal.normalized()
		add_child(link)
		link.global_position = droot.global_position
		link.global_rotation = Vector3.ZERO
		link.start_position = -normal * NAV_LINK_OFFSET
		link.end_position = normal * NAV_LINK_OFFSET
		link.bidirectional = true
		link.enabled = _door_field_is_open(door)
		door["nav_link"] = link
	_add_hatch_nav_link()
	# 0.8 m endpoints sit past the carved door gap; snap them onto the mesh within 1 m.
	_apply_nav_link_radius.call_deferred()


func _add_hatch_nav_link() -> void:
	# Same shape as a door link. The emitter is the D-204 field gate; the link stays off while the field is closed.
	if _props_container == null:
		return
	var panel: Node3D = _props_container.get_node_or_null("Hatch_D204_EmitterPanel") as Node3D
	if panel == null or not is_instance_valid(panel):
		return
	var link := NavigationLink3D.new()
	link.name = "NavLink_HATCH_D204"
	var normal := panel.global_transform.basis.z
	if normal.length_squared() < 0.0001:
		normal = Vector3.FORWARD
	else:
		normal = normal.normalized()
	add_child(link)
	link.global_position = panel.global_position
	link.global_rotation = Vector3.ZERO
	link.start_position = -normal * NAV_LINK_OFFSET
	link.end_position = normal * NAV_LINK_OFFSET
	link.bidirectional = true
	link.enabled = _hatch_open
	_hatch_link = link


func _set_hatch_field_open(open_state: bool) -> void:
	_hatch_open = open_state
	if _hatch_link != null and is_instance_valid(_hatch_link):
		_hatch_link.enabled = open_state


func _door_field_is_open(door: Dictionary) -> bool:
	var st := String(door.get("ff_state", ""))
	if st == "stall" or st == "deny":
		return false
	return bool(door.get("open", false))


func _sync_door_nav_link(door: Dictionary) -> void:
	var link := door.get("nav_link") as NavigationLink3D
	if link == null or not is_instance_valid(link):
		return
	link.enabled = _door_field_is_open(door)


func _apply_nav_link_radius() -> void:
	for _i: int in 30:
		var region := get_node_or_null("PlayableNavRegion") as NavigationRegion3D
		if region != null and is_instance_valid(region):
			var map := region.get_navigation_map()
			if map.is_valid() and NavigationServer3D.map_get_iteration_id(map) > 0:
				NavigationServer3D.map_set_link_connection_radius(map, 1.0)
				return
		await get_tree().physics_frame


func _nav_qa_id(it: Dictionary) -> String:
	if it.has("id") and String(it["id"]) != "":
		return String(it["id"])
	if it.has("door_id") and String(it["door_id"]) != "":
		return String(it["door_id"])
	var node := it.get("node") as Node
	if node != null and is_instance_valid(node):
		return String(node.name)
	return String(it.get("label", "interactable"))


## True when p is on the interior side of this door. The door plane itself is outside the volume.
func _nav_point_in_door_room(door_id: String, p: Vector3) -> bool:
	match door_id:
		"DOOR_APT201":
			return p.y > 3.3 and p.y < 8.2 and p.x > -14.6 and p.x < -5.2 and p.z > 2.75 and p.z < 9.6
		"DOOR_APT202":
			return p.y > 3.3 and p.y < 8.2 and p.x > 5.2 and p.x < 14.6 and p.z > 2.75 and p.z < 9.6
		"DOOR_ALCOVE2C":
			return p.y > 3.3 and p.y < 8.2 and p.x > -14.6 and p.x < -7.4 and p.z < -3.55 and p.z > -7.2
		"DOOR_RM1A":
			return ROOM_1A_INTERIOR.has_point(p)
		"DOOR_RM1B":
			return ROOM_1B_INTERIOR.has_point(p)
		"DOOR_SECTOR4_EXIT":
			return p.y < 3.6 and p.z < -8.90 and p.x > -18.5 and p.x < 18.5
		"HATCH_D204":
			# Under the Apt201 slab, inside Room1A. The slab is the field-gated floor between them.
			return p.y < 4.05 and p.x > -13.6 and p.x < -5.4 and ROOM_1A_INTERIOR.has_point(p)
		_:
			return false


## Doors whose interior contains exactly one of the two points. That door is the gate between them.
func _nav_separating_doors(a: Vector3, b: Vector3) -> PackedStringArray:
	var out := PackedStringArray()
	for door: Dictionary in _rfid_doors:
		var id := String(door.get("id", ""))
		if id == "":
			continue
		if _nav_point_in_door_room(id, a) != _nav_point_in_door_room(id, b):
			out.append(id)
	if _nav_point_in_door_room(HATCH_NAV_ID, a) != _nav_point_in_door_room(HATCH_NAV_ID, b):
		out.append(HATCH_NAV_ID)
	return out


## Pass only when the path ends within 1 m horizontally (XZ) of the interactable. No approach point.
func _nav_strict_reach(map: RID, spawn_pt: Vector3, target: Vector3) -> Dictionary:
	var closest := NavigationServer3D.map_get_closest_point(map, target)
	var path := NavigationServer3D.map_get_path(map, spawn_pt, closest, true)
	var end_dist := -1.0
	if not path.is_empty():
		var end: Vector3 = path[path.size() - 1]
		end_dist = Vector2(end.x, end.z).distance_to(Vector2(target.x, target.z))
	return {
		"reached": not path.is_empty() and end_dist <= 1.0,
		"end_dist": end_dist,
		"closest_dist": closest.distance_to(target),
		"pts": path.size(),
		"path": path,
	}


func _nav_qa_await_map(region: NavigationRegion3D) -> RID:
	var map := RID()
	var ready := false
	for _i: int in 180:
		await get_tree().physics_frame
		if region != null and is_instance_valid(region):
			map = region.get_navigation_map()
		if map.is_valid() and NavigationServer3D.map_get_iteration_id(map) > 0:
			ready = true
			break
	if ready:
		for _k: int in 3:
			await get_tree().physics_frame
		if region != null and is_instance_valid(region):
			map = region.get_navigation_map()
	if map.is_valid():
		NavigationServer3D.map_set_link_connection_radius(map, 1.0)
	return map


func _nav_qa_set_fields(open_state: bool) -> void:
	for door: Dictionary in _rfid_doors:
		_set_door_dissolve_immediate(door, 1.0 if open_state else 0.0)
		var link := door.get("nav_link") as NavigationLink3D
		if link != null and is_instance_valid(link):
			link.enabled = open_state and _door_field_is_open(door)
	_set_hatch_field_open(open_state)


## --qa-nav-reach: closed fields must block every gated interactable; open fields must reach all.
## DOOR_* interactables sit on the door plane and are used from outside, so they are left out of the
## closed-phase gated list. They stay in the open-phase reach list below.
func _run_qa_nav_reach() -> void:
	var region := get_node_or_null("PlayableNavRegion") as NavigationRegion3D
	_nav_qa_set_fields(false)
	var map := await _nav_qa_await_map(region)
	_print_nav_qa_stats(region)
	var total := _interactables.size()
	var gated_ids: PackedStringArray = PackedStringArray()
	var gated_doors: Dictionary = {}
	var nodes: Dictionary = {}
	for it: Dictionary in _interactables:
		var id := _nav_qa_id(it)
		var node := it.get("node") as Node3D
		if node == null or not is_instance_valid(node):
			continue
		nodes[id] = node
		if id.begins_with("DOOR_"):
			continue
		var doors := _nav_separating_doors(SPAWN_POS, node.global_position)
		if doors.is_empty():
			continue
		gated_ids.append(id)
		gated_doors[id] = doors
	var gated_n := gated_ids.size()
	if not map.is_valid():
		for it2: Dictionary in _interactables:
			print("[NAV-QA] FAIL %s nav map not ready" % _nav_qa_id(it2))
		print("[NAV-QA] closed: unreachable=0/%d leaks=%d" % [gated_n, gated_n])
		print("[NAV-QA] DONE reachable=0/%d failures=%d" % [total, gated_n + total])
		get_tree().quit(1)
		return
	var spawn_pt := NavigationServer3D.map_get_closest_point(map, SPAWN_POS)
	var unreachable := 0
	var leaks := 0
	for gid: String in gated_ids:
		var gnode := nodes[gid] as Node3D
		var reach: Dictionary = _nav_strict_reach(map, spawn_pt, gnode.global_position)
		if bool(reach["reached"]):
			leaks += 1
			var door_list: PackedStringArray = gated_doors[gid] as PackedStringArray
			print("[NAV-QA] FAIL %s leak doors=%s path_end_dist=%.2f path_pts=%d" % [gid, ",".join(door_list), float(reach["end_dist"]), int(reach["pts"])])
			var leak_path: PackedVector3Array = reach["path"]
			for pi: int in leak_path.size():
				var lp: Vector3 = leak_path[pi]
				print("[NAV-QA] leak_path %s i=%d %.2f,%.2f,%.2f" % [gid, pi, lp.x, lp.y, lp.z])
		else:
			unreachable += 1
	print("[NAV-QA] closed: unreachable=%d/%d leaks=%d" % [unreachable, gated_n, leaks])
	var iter_before := NavigationServer3D.map_get_iteration_id(map)
	_nav_qa_set_fields(true)
	for _i: int in 60:
		await get_tree().physics_frame
		if region != null and is_instance_valid(region):
			map = region.get_navigation_map()
		if map.is_valid() and NavigationServer3D.map_get_iteration_id(map) != iter_before:
			break
	for _k: int in 3:
		await get_tree().physics_frame
	if region != null and is_instance_valid(region):
		map = region.get_navigation_map()
	if map.is_valid():
		NavigationServer3D.map_set_link_connection_radius(map, 1.0)
		spawn_pt = NavigationServer3D.map_get_closest_point(map, SPAWN_POS)
	var reachable := 0
	var phase_b_fails := 0
	if not map.is_valid():
		for it3: Dictionary in _interactables:
			phase_b_fails += 1
			print("[NAV-QA] FAIL %s nav map not ready" % _nav_qa_id(it3))
	else:
		for it4: Dictionary in _interactables:
			var id4 := _nav_qa_id(it4)
			var node4 := it4.get("node") as Node3D
			if node4 == null or not is_instance_valid(node4):
				phase_b_fails += 1
				print("[NAV-QA] FAIL %s missing node" % id4)
				continue
			var reach4: Dictionary = _nav_strict_reach(map, spawn_pt, node4.global_position)
			if bool(reach4["reached"]):
				reachable += 1
			else:
				phase_b_fails += 1
				print("[NAV-QA] FAIL %s closest_dist=%.2f path_end_dist=%.2f path_pts=%d" % [id4, float(reach4["closest_dist"]), float(reach4["end_dist"]), int(reach4["pts"])])
	var failures := leaks + phase_b_fails
	print("[NAV-QA] DONE reachable=%d/%d failures=%d" % [reachable, total, failures])
	get_tree().quit(0 if failures == 0 else 1)


func _print_nav_qa_stats(region: NavigationRegion3D) -> void:
	var polygons := 0
	var vertices := 0
	var islands := 0
	if region != null and is_instance_valid(region) and region.navigation_mesh != null:
		var mesh := region.navigation_mesh
		polygons = mesh.get_polygon_count()
		vertices = mesh.get_vertices().size()
		islands = _nav_island_count(mesh)
	print("[NAV-QA] polygons=%d vertices=%d islands=%d" % [polygons, vertices, islands])


func _nav_island_count(mesh: NavigationMesh) -> int:
	var n := mesh.get_polygon_count()
	if n == 0:
		return 0
	var verts := mesh.get_vertices()
	var parent: Array[int] = []
	parent.resize(n)
	for i: int in n:
		parent[i] = i
	var buckets: Dictionary = {}
	for pi: int in n:
		var poly := mesh.get_polygon(pi)
		for k: int in poly.size():
			var p: Vector3 = verts[poly[k]]
			var key := Vector3i(int(round(p.x / 0.05)), int(round(p.y / 0.05)), int(round(p.z / 0.05)))
			if buckets.has(key):
				_nav_uf_union(parent, pi, int(buckets[key]))
			else:
				buckets[key] = pi
			for ox: int in range(-1, 2):
				for oy: int in range(-1, 2):
					for oz: int in range(-1, 2):
						var nk := Vector3i(key.x + ox, key.y + oy, key.z + oz)
						if buckets.has(nk):
							_nav_uf_union(parent, pi, int(buckets[nk]))
	var roots: Dictionary = {}
	for i2: int in n:
		roots[_nav_uf_find(parent, i2)] = true
	return roots.size()


func _nav_uf_find(parent: Array[int], i: int) -> int:
	var root := i
	while parent[root] != root:
		root = parent[root]
	while parent[i] != root:
		var nxt := parent[i]
		parent[i] = root
		i = nxt
	return root


func _nav_uf_union(parent: Array[int], a: int, b: int) -> void:
	var ra := _nav_uf_find(parent, a)
	var rb := _nav_uf_find(parent, b)
	if ra != rb:
		parent[rb] = ra


func _ensure_child(nm: String) -> Node3D:
	var n: Node3D = get_node_or_null(nm) as Node3D
	if n == null:
		n = Node3D.new()
		n.name = nm
		add_child(n)
	return n


# ------------------------------------------------------------------------------
# Portable path resolution (BUG-02)
# ------------------------------------------------------------------------------
func _resolve_path(p: String) -> String:
	if p.begins_with("res://") or p.begins_with("user://"):
		return ProjectSettings.globalize_path(p)
	return p


func _load_tex(fname: String) -> Texture2D:
	if _tex_cache.has(fname):
		return _tex_cache[fname] as Texture2D
	for d: String in TEX_DIRS:
		var p: String = _resolve_path(d + "/" + fname)
		if FileAccess.file_exists(p):
			var img: Image = Image.new()
			if img.load(p) == OK and not img.is_empty():
				img.generate_mipmaps()
				var tex: ImageTexture = ImageTexture.create_from_image(img)
				_tex_cache[fname] = tex
				return tex
	return null


func _find_first_existing(paths: Array) -> String:
	for p in paths:
		var sp: String = String(p)
		if FileAccess.file_exists(_resolve_path(sp)):
			return sp
	return ""


func _load_glb_scene(path: String, emission_mult: float = 0.65) -> Node3D:
	if path == "":
		return null
	var abs_path: String = _resolve_path(path)
	if not FileAccess.file_exists(abs_path):
		return null
	var doc: GLTFDocument = GLTFDocument.new()
	var state: GLTFState = GLTFState.new()
	if doc.append_from_file(abs_path, state) == OK:
		var root: Node = doc.generate_scene(state)
		if root is Node3D:
			var n3d: Node3D = root as Node3D
			_upgrade_sector_materials(n3d, emission_mult)
			return n3d
		elif root != null:
			root.free()
	return null


# ------------------------------------------------------------------------------
# Sector architecture + collisions (BUG-03)
# ------------------------------------------------------------------------------
func _is_baked_leaf_door_name(nm: String) -> bool:
	var n: String = nm.to_lower()
	return n.contains("door_slide") or n.contains("door_leaf") or n.contains("door_apt")


## Baked slide/leaf/apt meshes are removed in `_remove_baked_leaf_doors_and_grates`. Lookups of those names return null.
func _lookup_sector_node(root: Node, name_exact: String) -> Node:
	if root == null or not is_instance_valid(root):
		return null
	if _is_baked_leaf_door_name(name_exact):
		return null
	var stack: Array[Node] = [root]
	while not stack.is_empty():
		var c: Node = stack.pop_back()
		if not is_instance_valid(c):
			continue
		if _is_baked_leaf_door_name(String(c.name)):
			continue
		if String(c.name) == name_exact:
			return c
		for ch: Node in c.get_children():
			stack.append(ch)
	return null


func _remove_baked_leaf_doors_and_grates(root: Node3D) -> void:
	# Free baked *door_slide* / *door_leaf* / *door_apt* meshes (remove_child + queue_free) so a later
	# trimesh pass cannot see them. Grates and baked pickups stay hidden, matching the previous pass.
	var stack: Array[Node] = [root]
	var free_nodes: Array[Node] = []
	while not stack.is_empty():
		var curr: Node = stack.pop_back()
		if not is_instance_valid(curr):
			continue
		var drop: bool = false
		if curr != root and curr is Node3D:
			var nm: String = String(curr.name).to_lower()
			if _is_baked_leaf_door_name(nm):
				drop = true
			elif nm.contains("maint_grate") or nm.begins_with("pickup_"):
				(curr as Node3D).visible = false
		if drop:
			free_nodes.append(curr)
			continue
		for ch: Node in curr.get_children():
			stack.append(ch)
	for n: Node in free_nodes:
		if not is_instance_valid(n):
			continue
		var p: Node = n.get_parent()
		if p != null:
			p.remove_child(n)
		n.queue_free()


func _is_visible_in_tree_static(n: Node3D) -> bool:
	var c: Node = n
	while c != null:
		if c is Node3D and not (c as Node3D).visible:
			return false
		c = c.get_parent()
	return true


func _add_sector_trimesh_collisions(sector_node: Node3D) -> int:
	var count: int = 0
	var stack: Array[Node] = [sector_node]
	var meshes: Array[MeshInstance3D] = []
	while not stack.is_empty():
		var curr: Node = stack.pop_back()
		if curr is MeshInstance3D:
			meshes.append(curr as MeshInstance3D)
		for ch: Node in curr.get_children():
			stack.append(ch)
	for mi: MeshInstance3D in meshes:
		var nm: String = mi.name.to_lower()
		if nm.contains("glass") or nm.contains("foliage") or nm.contains("holo"):
			continue
		# Stairs use a smooth sloped safety collider so treads never snag the capsule.
		if nm.contains("stair") or (mi.get_parent() != null and String(mi.get_parent().name).to_lower().contains("stair")):
			continue
		if mi.mesh == null or mi.mesh.get_surface_count() <= 0:
			continue
		if not is_instance_valid(mi) or _is_baked_leaf_door_name(nm):
			continue
		if not _is_visible_in_tree_static(mi):
			continue
		var faces: PackedVector3Array = mi.mesh.get_faces()
		if faces.size() < 3:
			continue
		mi.create_trimesh_collision()
		count += 1
	return count


func _add_architectural_shadow_occluders(parent: Node3D) -> void:
	var occ_root: Node3D = Node3D.new()
	occ_root.name = "SectorShadowOccluders"
	parent.add_child(occ_root)
	# Hidden SHADOWS_ONLY solid slabs inside the L2 floor and L2/L1 apartment ceilings so
	# upper-deck characters/props NEVER project shadows onto the L1 atrium floor and
	# exterior skylight sunlight NEVER leaks through enclosed room ceilings.
	# D670-06: material instead of hiding (hidden meshes cast no shadows)
	var occ_mat: StandardMaterial3D = StandardMaterial3D.new()
	occ_mat.resource_name = "Mat_Occluder_Gunmetal"
	occ_mat.albedo_color = Color("#2A2F36")
	occ_mat.roughness = 0.9
	occ_mat.metallic = 0.0
	for cfg: Dictionary in [
		# M-41: Occ_L2_NorthGallerySlab removed. It covered the Rev C L2 apartments.
		{"name": "Occ_L2_WestAlcoveSlab", "size": Vector3(6.5, 0.30, 7.9), "pos": Vector3(-10.65, 4.02, -2.65)},
		{"name": "Occ_L2_EastLandingSlab", "size": Vector3(6.5, 0.30, 3.6), "pos": Vector3(10.65, 4.02, -0.50)},
		{"name": "Occ_L2_EastStairSoffit", "size": Vector3(2.95, 0.28, 6.95), "pos": Vector3(10.65, 2.05, -5.00), "rot_x": -atan2(4.20, 5.60)},
		{"name": "Occ_Roof_NorthApartments", "size": Vector3(28.0, 0.32, 7.9), "pos": Vector3(0.0, 8.20, 5.0)},
		{"name": "Occ_Roof_WestWing", "size": Vector3(6.5, 0.32, 7.8), "pos": Vector3(-10.65, 8.20, -2.65)},
		{"name": "Occ_Roof_EastWing", "size": Vector3(6.5, 0.32, 7.8), "pos": Vector3(10.65, 8.20, -2.65)}
	]:
		var mi: MeshInstance3D = MeshInstance3D.new()
		mi.name = String(cfg["name"])
		var bm: BoxMesh = BoxMesh.new()
		bm.size = cfg["size"] as Vector3
		mi.mesh = bm
		mi.position = cfg["pos"] as Vector3
		if cfg.has("rot_x"):
			mi.rotation = Vector3(float(cfg["rot_x"]), 0.0, 0.0)
		mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_SHADOWS_ONLY
		mi.material_override = occ_mat
		occ_root.add_child(mi)


func _add_safety_floor_colliders(parent: Node3D) -> void:
	var body: StaticBody3D = StaticBody3D.new()
	body.name = "SectorSafetyFloorColliders"
	parent.add_child(body)
	var boxes: Array[Dictionary] = [
		{"name": "GroundFloorDeck", "size": Vector3(32.0, 0.4, 24.0), "pos": Vector3(0.0, -0.2, 0.0), "rot_x": 0.0},
		# M-41: UpperL2NorthDeck, UpperL2WestWing and UpperL2EastStairLanding removed.
		# Those boxes were the pre-Rev C gallery floor (top y=4.20). L2 is the shell trimesh, slab top y=4.2.
		# PATH-06 Fixed: Missing guardrail colliders on L2 West Wing South Edge, East Upper Landing West Edge & East Staircase West Edge
		{"name": "L2WestWingSouthGuardrail", "size": Vector3(6.5, 1.25, 0.18), "pos": Vector3(-10.65, 4.82, -6.55), "rot_x": 0.0},
		{"name": "EastLandingWestGuardrail", "size": Vector3(0.18, 1.25, 3.55), "pos": Vector3(7.55, 4.82, -0.45), "rot_x": 0.0},
		{"name": "EastStairWestGuardrail", "size": Vector3(0.18, 4.80, 4.00), "pos": Vector3(9.16, 2.40, -4.20), "rot_x": 0.0},
		# Walkable Exterior Sector-4 Cylinder Hab-7 Promenade Deck (Z = -9.15m..-45.0m, X = -18.0m..+18.0m) + Guardrails
		{"name": "Sector4PromenadeExteriorDeck", "size": Vector3(36.0, 0.40, 36.0), "pos": Vector3(0.0, -0.08, -27.0), "rot_x": 0.0},
		{"name": "PromenadeWestGuardrail", "size": Vector3(0.24, 1.25, 36.0), "pos": Vector3(-18.0, 0.62, -27.0), "rot_x": 0.0},
		{"name": "PromenadeEastGuardrail", "size": Vector3(0.24, 1.25, 36.0), "pos": Vector3(18.0, 0.62, -27.0), "rot_x": 0.0},
		{"name": "PromenadeSouthGuardrail", "size": Vector3(36.0, 1.25, 0.24), "pos": Vector3(0.0, 0.62, -45.0), "rot_x": 0.0}
	]
	# M-70: 37 deg EastStairRampConnector (x 10.65) removed; Rev C stair_set_switchback.glb colliders replace it.
	for b: Dictionary in boxes:
		var cs: CollisionShape3D = CollisionShape3D.new()
		cs.name = String(b["name"])
		var shape: BoxShape3D = BoxShape3D.new()
		shape.size = b["size"] as Vector3
		cs.shape = shape
		cs.position = b["pos"] as Vector3
		cs.rotation = Vector3(float(b["rot_x"]), 0.0, 0.0)
		body.add_child(cs)
	_add_playtest_seam_blocks(parent)


func _add_seam_static_box(parent: Node3D, nm: String, sz: Vector3, pos: Vector3, mat: Material, margin: float = -1.0) -> void:
	var seam: StaticBody3D = StaticBody3D.new()
	seam.name = nm
	seam.position = pos
	parent.add_child(seam)
	var seam_cs: CollisionShape3D = CollisionShape3D.new()
	seam_cs.name = nm + "_Shape"
	var seam_bs: BoxShape3D = BoxShape3D.new()
	seam_bs.size = sz
	if margin >= 0.0:
		seam_bs.margin = margin
	seam_cs.shape = seam_bs
	seam.add_child(seam_cs)
	if mat != null:
		var mi: MeshInstance3D = MeshInstance3D.new()
		mi.name = nm + "_Mesh"
		var bm: BoxMesh = BoxMesh.new()
		bm.size = sz
		mi.mesh = bm
		mi.material_override = mat
		seam.add_child(mi)


## [SEAM-03] Alcove 2C's east opening is a 1.1 m guardrail, not a wall. The mezzanine edge keeps its rail.
## Rook's *_SeamFix meshes already supply the side-wall trimesh colliders (SEAM-01).
## Safety-floor boxes share one StaticBody, so these are their own StaticBody3D nodes on the same parent.
func _add_playtest_seam_blocks(parent: Node3D) -> void:
	var rail_mat: StandardMaterial3D = StandardMaterial3D.new()
	# [M-36] Brushed titanium. Roughness/metallic scalars are multipliers on the ORM channels.
	rail_mat.albedo_color = Color(1, 1, 1, 1)
	rail_mat.metallic = 1.0
	rail_mat.roughness = 1.0
	var rail_alb: Texture2D = _load_tex("qa03/rail_brushed_titanium_albedo.png")
	var rail_orm: Texture2D = _load_tex("qa03/rail_brushed_titanium_orm.png")
	if rail_alb != null:
		rail_mat.albedo_texture = rail_alb
	if rail_orm != null:
		rail_mat.metallic_texture = rail_orm
		rail_mat.metallic_texture_channel = BaseMaterial3D.TEXTURE_CHANNEL_BLUE
		rail_mat.roughness_texture = rail_orm
		rail_mat.roughness_texture_channel = BaseMaterial3D.TEXTURE_CHANNEL_GREEN
	rail_mat.uv1_triplanar = true
	rail_mat.uv1_scale = Vector3(2.0, 2.0, 2.0)
	var az0: float = -5.69
	var az1: float = -3.94
	var alen: float = az1 - az0
	var azc: float = (az0 + az1) * 0.5
	var afloor: float = 4.32
	# East opening of the alcove. z stops at -3.94, south of DOOR_ALCOVE2C (x -11.5, z -3.55), so the doorway stays clear.
	_add_seam_static_box(parent, "Seam03_Alcove2C_EastRail", Vector3(0.08, 1.1, alen), Vector3(-10.30, afloor + 0.55, azc), rail_mat)
	# Mezzanine-edge rail, on the atrium face of that opening.
	var edge_mat: StandardMaterial3D = rail_mat.duplicate() as StandardMaterial3D
	_add_seam_static_box(parent, "Seam03_Alcove2C_Rail", Vector3(0.08, 1.1, alen), Vector3(-10.18, afloor + 0.55, azc), edge_mat)
	# M-70: QA_BK01_Alcove2C_EastJamb removed (Rook: not part of Rev C).


func _add_glass_balustrade_colliders(parent: Node3D) -> void:
	# [REAL-02] Rev C L2 open edge is the south side of the stair landing (drop into the well).
	# Landing top Y 4.2, edge Z -4.88. Guard plane Z -4.83, X -1.89..0.37, so it stops before
	# flight 2 (X 0.4..1.9) and does not cross the corridor opening at Z -0.8.
	# M-41 keeps this rail. It is not one of the gallery decks.
	var runs: Array[Dictionary] = [
		{"name": "MezzanineGlassBalustrade_L2Edge", "size": Vector3(2.26, 1.04, 0.06), "pos": Vector3(-0.76, 4.78, -4.83)}
	]
	for r: Dictionary in runs:
		var body: StaticBody3D = StaticBody3D.new()
		body.name = String(r["name"])
		body.collision_layer = 1 | GLASS_QA_LAYER_BIT  # default world layer + a dedicated bit for QA rays
		body.position = r["pos"] as Vector3
		parent.add_child(body)
		var cs: CollisionShape3D = CollisionShape3D.new()
		var bs: BoxShape3D = BoxShape3D.new()
		bs.size = r["size"] as Vector3
		cs.shape = bs
		body.add_child(cs)


## [M-58] Invisible 1.1 m edge guards. Floor y=4.2, so the box centre is 4.75.
## Gallery: a 0.6 m move heading -X from (6, 4.2, 0) leaves the L2 slab. The rail is
## the west lip of that slab (east face x=5.55), 10 cm clear of a capsule at x=6,
## and east of DOOR_APT202 (x=3) so the egress waypoints (x<=1.15) do not cross it.
## NE and W sit outside the Rev C wall line (north outer face z=9.1, west outer face x=-14.1).
func _add_m58_edge_guards(parent: Node3D) -> void:
	var runs: Array[Dictionary] = [
		{"name": "M58_L2GalleryWestEdge", "size": Vector3(0.10, 1.1, 1.70), "pos": Vector3(5.50, 4.75, 0.0)},
		{"name": "M58_L2NorthEastEdge", "size": Vector3(2.0, 1.1, 0.10), "pos": Vector3(13.0, 4.75, 9.15)},
		{"name": "M58_L2WestEdge", "size": Vector3(0.10, 1.1, 6.0), "pos": Vector3(-14.15, 4.75, 5.0)},
	]
	for r: Dictionary in runs:
		var body: StaticBody3D = StaticBody3D.new()
		body.name = String(r["name"])
		body.collision_layer = 1
		body.collision_mask = 1
		body.position = r["pos"] as Vector3
		parent.add_child(body)
		var cs: CollisionShape3D = CollisionShape3D.new()
		var bs: BoxShape3D = BoxShape3D.new()
		bs.size = r["size"] as Vector3
		bs.margin = 0.0
		cs.shape = bs
		body.add_child(cs)


func _build_cylinder_hab7_fullscale_world(parent: Node3D) -> void:
	var hab_root: Node3D = Node3D.new()
	hab_root.name = "CylinderHab7_FullScale_World"
	parent.add_child(hab_root)

	# 1. Instantiate the full-scale 800m x 400m (R = 200m) O'Neill Cylinder Hab-7 interior backdrop.
	# Static pose (no spin animation). Valley A is the bottom nadir under the Sector-4 promenade; the map is not moved.
	# Looking along world ±X looks down the 800m spin axis (axial solar rails, Ring-A..Ring-E). Looking up (+Y)
	# sees the opposite valleys overhead; looking south (-Z) looks across the valley, not along the axis.
	var cyl_path: String = _find_first_existing(CYLINDER_MAP_PATHS)
	var cyl_pivot: Node3D = Node3D.new()
	cyl_pivot.name = "CylinderHab7_DrumAxisPivot"
	# Cylinder local X is the spin axis (authored axial span about [-368..+354]). No yaw: local +X stays world +X,
	# the map's long axis (exterior x -47..47). Godot Euler order is YXZ, so a Z component would pitch the axis;
	# the valley roll is a pure X rotation. Child offset y -200 cancels the GLB axis at y 200, so this pivot is the axis.
	# Measured with raycasts against the cylinder mesh: rotation (43, 0, 0) pushes terrain up through the map;
	# (-43, 0, 0) puts the Valley A floor (circular arc, R ~ 200) under the map, with its valley wall at z ~ -26
	# (matching the canal edge at -25.8). Surface height is constant along X (axis parallel to the map's long axis).
	# Axis y 187.2, lowered 0.5 m so the inner surface and glass stay below the deck; surface max y about -0.6.
	# A flat 66 m footprint on an R 200 m arc cannot be fully tangent; the deck floats above the valley floor.
	# The 135 m axial offset is along X, and Z = 0 holds the axis over the map centre line.
	cyl_pivot.position = Vector3(135.0, 187.2, 0.0)
	cyl_pivot.rotation_degrees = Vector3(-43.0, 0.0, 0.0)
	hab_root.add_child(cyl_pivot)

	var cyl_node: Node3D = _load_glb_scene(cyl_path, 0.85)
	if cyl_node != null:
		cyl_node.name = "CylinderHab7_FullScale_Mesh"
		cyl_node.position = Vector3(0.0, -200.0, 0.0)
		cyl_pivot.add_child(cyl_node)
		# Mesh edit only. Pivot pose above is the drum axis; this never rotates CylinderHab7_DrumAxisPivot.
		_cut_observation_window(cyl_node, cyl_pivot)
		# [M-04] Opaque drum hull casts shadows, so the sun reaches the interior only through the cut window.
		_enable_hull_shadows(cyl_node)

	_build_starfield_outer_cylinder(hab_root)

	# 2. Walkable Exterior Sector-4 Promenade Plaza Deck (Z = -9.0m..-45.0m, X = -18.0m..+18.0m, Y = 0.0m)
	var plaza_root: Node3D = Node3D.new()
	plaza_root.name = "Sector4_Promenade_ExteriorPlaza"
	hab_root.add_child(plaza_root)

	var deck_mat: StandardMaterial3D = StandardMaterial3D.new()
	deck_mat.albedo_color = Color(0.34, 0.38, 0.43, 1.0)
	deck_mat.roughness = 0.42
	deck_mat.metallic = 0.22
	var deck_tex: Texture2D = _load_tex("mat_deck_floor_albedo.png")
	if deck_tex != null:
		deck_mat.albedo_texture = deck_tex
		deck_mat.uv1_scale = Vector3(12.0, 12.0, 1.0)

	var rail_mat: StandardMaterial3D = StandardMaterial3D.new()
	rail_mat.albedo_color = Color(0.24, 0.28, 0.33, 1.0)
	rail_mat.metallic = 0.82
	rail_mat.roughness = 0.36

	var amber_mat: StandardMaterial3D = StandardMaterial3D.new()
	amber_mat.albedo_color = COLOR_AMBER
	amber_mat.emission_enabled = true
	amber_mat.emission = COLOR_AMBER
	amber_mat.emission_energy_multiplier = 0.85

	var cyan_mat: StandardMaterial3D = StandardMaterial3D.new()
	cyan_mat.albedo_color = COLOR_CYAN
	cyan_mat.emission_enabled = true
	cyan_mat.emission = COLOR_CYAN
	cyan_mat.emission_energy_multiplier = 0.85

	var deck_mi: MeshInstance3D = MeshInstance3D.new()
	deck_mi.name = "PromenadePlazaDeckSlab"
	var deck_bm: BoxMesh = BoxMesh.new()
	deck_bm.size = Vector3(36.0, 0.24, 36.0)
	deck_mi.mesh = deck_bm
	deck_mi.position = Vector3(0.0, 0.0, -27.0)
	deck_mi.material_override = deck_mat
	plaza_root.add_child(deck_mi)

	# Centerline promenade guideway inlay & side balustrade rails
	for gx: float in [-3.2, 3.2]:
		var guide_mi: MeshInstance3D = MeshInstance3D.new()
		var gbm: BoxMesh = BoxMesh.new()
		gbm.size = Vector3(0.14, 0.02, 34.0)
		guide_mi.mesh = gbm
		guide_mi.position = Vector3(gx, 0.125, -26.5)
		guide_mi.material_override = cyan_mat
		guide_mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
		plaza_root.add_child(guide_mi)

	for rail_cfg: Dictionary in [
		{"pos": Vector3(-18.0, 0.62, -27.0), "sz": Vector3(0.16, 1.10, 36.0)},
		{"pos": Vector3(18.0, 0.62, -27.0), "sz": Vector3(0.16, 1.10, 36.0)},
		{"pos": Vector3(0.0, 0.62, -45.0), "sz": Vector3(36.0, 1.10, 0.16)}
	]:
		var rmi: MeshInstance3D = MeshInstance3D.new()
		var rbm: BoxMesh = BoxMesh.new()
		rbm.size = rail_cfg["sz"] as Vector3
		rmi.mesh = rbm
		rmi.position = rail_cfg["pos"] as Vector3
		rmi.material_override = rail_mat
		plaza_root.add_child(rmi)

	# Exterior promenade bollards & Ring-A..Ring-E architectural arch markers along the plaza
	for bz: float in [-14.0, -22.0, -30.0, -38.0]:
		for bx: float in [-6.5, 6.5]:
			var bol: MeshInstance3D = MeshInstance3D.new()
			var bcm: BoxMesh = BoxMesh.new()
			bcm.size = Vector3(0.36, 1.15, 0.36)
			bol.mesh = bcm
			bol.position = Vector3(bx, 0.65, bz)
			bol.material_override = rail_mat
			plaza_root.add_child(bol)
			var cap: MeshInstance3D = MeshInstance3D.new()
			var cbm: BoxMesh = BoxMesh.new()
			cbm.size = Vector3(0.38, 0.08, 0.38)
			cap.mesh = cbm
			cap.position = Vector3(bx, 1.18, bz)
			cap.material_override = amber_mat
			cap.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
			plaza_root.add_child(cap)




# World triangle against the playable-map AABB.
# (a) any vertex inside the box, (b) any triangle edge meets the box,
# (c) any of the 12 box edges meets the triangle.
func _world_triangle_hits_map_box(a: Vector3, b: Vector3, c: Vector3, box: AABB, edge_from: PackedVector3Array, edge_to: PackedVector3Array) -> bool:
	var lo: Vector3 = a.min(b.min(c))
	var hi: Vector3 = a.max(b.max(c))
	var b0: Vector3 = box.position
	var b1: Vector3 = b0 + box.size
	# Separated AABBs cannot meet. Touching the boundary still falls through to the exact tests.
	if hi.x < b0.x or lo.x > b1.x or hi.y < b0.y or lo.y > b1.y or hi.z < b0.z or lo.z > b1.z:
		return false
	if box.has_point(a) or box.has_point(b) or box.has_point(c):
		return true
	if box.intersects_segment(a, b) or box.intersects_segment(b, c) or box.intersects_segment(c, a):
		return true
	for ei: int in range(edge_from.size()):
		var hit: Variant = Geometry3D.segment_intersects_triangle(edge_from[ei], edge_to[ei], a, b, c)
		if hit != null:
			return true
	return false


# [M-15] Table value, or -1 when the surface is not luminous. holo/lens keep authored energy × 0.8.
# "oled" is tested before "led" because the shorter token is a substring.
func _m15_emission_energy(blob: String, existing_energy: float = 1.0, emission_on: bool = false) -> float:
	var n: String = blob.to_lower().replace("_", "").replace("-", "")
	if n.contains("luminaire") or n.contains("ceilingpanel") or n.contains("lightstrip"):
		return 2.0
	if n.contains("headersign") or n.contains("signage"):
		return 1.5
	if n.contains("oled") or n.contains("amber"):
		return 1.2
	if n.contains("status") or n.contains("led"):
		return 3.0
	if n.contains("holo") or n.contains("lens"):
		# M-34 already applied the ×0.8 rule during material upgrade. Don't apply it twice.
		if emission_on and existing_energy > 0.0:
			return existing_energy
		return 0.8
	return -1.0


func _make_observation_window_glass_material() -> StandardMaterial3D:
	var glass_mat: StandardMaterial3D = StandardMaterial3D.new()
	glass_mat.resource_name = "Mat_ObservationWindowGlass"
	glass_mat.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
	glass_mat.albedo_color = Color(0.70, 0.82, 0.88, 0.14)
	glass_mat.metallic = 0.0
	glass_mat.metallic_specular = 0.5
	glass_mat.roughness = 0.04
	glass_mat.rim_enabled = true
	glass_mat.rim = 0.35
	glass_mat.rim_tint = 0.6
	glass_mat.cull_mode = BaseMaterial3D.CULL_BACK
	glass_mat.depth_draw_mode = BaseMaterial3D.DEPTH_DRAW_DISABLED
	return glass_mat


func _append_facing_tri(verts: PackedVector3Array, norms: PackedVector3Array, a: Vector3, b: Vector3, c: Vector3, face_dir: Vector3) -> void:
	var fn: Vector3 = (b - a).cross(c - a)
	if fn.dot(face_dir) < 0.0:
		var swap: Vector3 = b
		b = c
		c = swap
		fn = -fn
	var nrm: Vector3 = face_dir.normalized()
	if fn.length() > 0.0000001:
		nrm = fn.normalized()
	verts.append(a)
	verts.append(b)
	verts.append(c)
	norms.append(nrm)
	norms.append(nrm)
	norms.append(nrm)


func _spawn_centered_mesh(parent: Node3D, verts: PackedVector3Array, norms: PackedVector3Array, mat: Material, node_name: String, priority: int, sorting_offset: float) -> void:
	if verts.is_empty():
		return
	var centroid: Vector3 = Vector3.ZERO
	for v: Vector3 in verts:
		centroid += v
	centroid /= float(verts.size())
	var st: SurfaceTool = SurfaceTool.new()
	st.begin(Mesh.PRIMITIVE_TRIANGLES)
	for i: int in range(verts.size()):
		st.set_normal(norms[i])
		st.add_vertex(verts[i] - centroid)
	var mi: MeshInstance3D = MeshInstance3D.new()
	mi.name = node_name
	var built: ArrayMesh = st.commit()
	if built != null and built.get_surface_count() > 0:
		built.surface_set_name(0, node_name)
	mi.mesh = built
	mi.position = centroid
	# render_priority lives on Material. Duplicate so strip (-1) and caps (-2) can differ.
	var use_mat: Material = mat.duplicate() if mat != null else null
	if use_mat != null:
		use_mat.render_priority = priority
	mi.material_override = use_mat
	mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	mi.sorting_offset = sorting_offset
	parent.add_child(mi)


func _add_facing_tri(st: SurfaceTool, a: Vector3, b: Vector3, c: Vector3, face_dir: Vector3) -> void:
	var fn: Vector3 = (b - a).cross(c - a)
	if fn.dot(face_dir) < 0.0:
		st.add_vertex(a)
		st.add_vertex(c)
		st.add_vertex(b)
	else:
		st.add_vertex(a)
		st.add_vertex(b)
		st.add_vertex(c)


func _add_facing_quad(st: SurfaceTool, a: Vector3, b: Vector3, c: Vector3, d: Vector3, face_dir: Vector3) -> void:
	_add_facing_tri(st, a, b, c, face_dir)
	_add_facing_tri(st, a, c, d, face_dir)


# [M-17] Opaque ribs every 6° across the 36° wedge (5 interior + 2 edges), plus a 1.2 m cap ring.
func _add_observation_mullions(cyl_node: Node3D, a0: float, cap_x_neg: float, cap_x_pos: float) -> void:
	var half_rad: float = deg_to_rad(18.0)
	var r_out: float = 199.0
	var r_in: float = 198.8
	var half_ang: float = 0.15 / r_out
	var st: SurfaceTool = SurfaceTool.new()
	st.begin(Mesh.PRIMITIVE_TRIANGLES)
	for i: int in range(7):
		var ang: float = a0 - half_rad + deg_to_rad(6.0) * float(i)
		_add_mullion_rib(st, ang - half_ang, ang + half_ang, r_in, r_out, cap_x_neg, cap_x_pos)
	_add_cap_perimeter_ring(st, cap_x_neg, 1.0, 198.8, 200.0)
	_add_cap_perimeter_ring(st, cap_x_pos, -1.0, 198.8, 200.0)
	st.generate_normals()
	var mi: MeshInstance3D = MeshInstance3D.new()
	mi.name = "ObservationWindowMullions"
	mi.mesh = st.commit()
	var mat: StandardMaterial3D = StandardMaterial3D.new()
	mat.resource_name = "Mat_ObservationWindowMullion"
	mat.albedo_color = Color("#1A1E24")
	mat.metallic = 1.0
	mat.roughness = 0.65
	mat.cull_mode = BaseMaterial3D.CULL_BACK
	var hull_tex: Texture2D = _load_tex("facade_titanium_gunmetal_hull.png")
	if hull_tex != null:
		mat.albedo_texture = hull_tex
		mat.uv1_triplanar = true
		mat.uv1_scale = Vector3(2.0, 2.0, 2.0)
	mi.material_override = mat
	mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_ON
	cyl_node.add_child(mi)


func _add_mullion_rib(st: SurfaceTool, ang0: float, ang1: float, r_in: float, r_out: float, x0: float, x1: float) -> void:
	var mid: float = (ang0 + ang1) * 0.5
	var p000: Vector3 = _drum_shell_point(x0, r_in, ang0)
	var p001: Vector3 = _drum_shell_point(x0, r_in, ang1)
	var p010: Vector3 = _drum_shell_point(x0, r_out, ang0)
	var p011: Vector3 = _drum_shell_point(x0, r_out, ang1)
	var p100: Vector3 = _drum_shell_point(x1, r_in, ang0)
	var p101: Vector3 = _drum_shell_point(x1, r_in, ang1)
	var p110: Vector3 = _drum_shell_point(x1, r_out, ang0)
	var p111: Vector3 = _drum_shell_point(x1, r_out, ang1)
	var toward_axis: Vector3 = Vector3(0.0, -cos(mid), -sin(mid))
	var away_axis: Vector3 = -toward_axis
	_add_facing_quad(st, p000, p100, p101, p001, toward_axis)
	_add_facing_quad(st, p010, p011, p111, p110, away_axis)
	_add_facing_quad(st, p000, p010, p110, p100, Vector3(0.0, sin(ang0), -cos(ang0)))
	_add_facing_quad(st, p001, p101, p111, p011, Vector3(0.0, -sin(ang1), cos(ang1)))
	_add_facing_quad(st, p000, p001, p011, p010, Vector3(-1.0, 0.0, 0.0))
	_add_facing_quad(st, p100, p110, p111, p101, Vector3(1.0, 0.0, 0.0))


func _add_cap_perimeter_ring(st: SurfaceTool, cap_x: float, inward_sign: float, r_in: float, r_out: float) -> void:
	var x_near: float = cap_x + inward_sign * 0.02
	var x_far: float = cap_x + inward_sign * 0.10
	var segs: int = 64
	var face_near: Vector3 = Vector3(-inward_sign, 0.0, 0.0)
	var face_far: Vector3 = Vector3(inward_sign, 0.0, 0.0)
	for s: int in range(segs):
		var t0: float = TAU * float(s) / float(segs)
		var t1: float = TAU * float(s + 1) / float(segs)
		var a0: Vector3 = Vector3(x_near, 200.0 + r_in * cos(t0), r_in * sin(t0))
		var b0: Vector3 = Vector3(x_near, 200.0 + r_in * cos(t1), r_in * sin(t1))
		var c0: Vector3 = Vector3(x_near, 200.0 + r_out * cos(t0), r_out * sin(t0))
		var d0: Vector3 = Vector3(x_near, 200.0 + r_out * cos(t1), r_out * sin(t1))
		var a1: Vector3 = Vector3(x_far, 200.0 + r_in * cos(t0), r_in * sin(t0))
		var b1: Vector3 = Vector3(x_far, 200.0 + r_in * cos(t1), r_in * sin(t1))
		var c1: Vector3 = Vector3(x_far, 200.0 + r_out * cos(t0), r_out * sin(t0))
		var d1: Vector3 = Vector3(x_far, 200.0 + r_out * cos(t1), r_out * sin(t1))
		_add_facing_quad(st, a0, b0, d0, c0, face_near)
		_add_facing_quad(st, a1, c1, d1, b1, face_far)
		var inner_dir: Vector3 = Vector3(0.0, -cos((t0 + t1) * 0.5), -sin((t0 + t1) * 0.5))
		_add_facing_quad(st, a0, a1, b1, b0, inner_dir)
		_add_facing_quad(st, c0, d0, d1, c1, -inner_dir)


# [M-04] Double-sided so a hull face whose normal points inward still blocks the sun.
func _enable_hull_shadows(root: Node3D) -> void:
	if root == null:
		return
	var stack: Array[Node] = [root]
	while not stack.is_empty():
		var c: Node = stack.pop_back()
		var nm: String = String(c.name)
		if nm.begins_with("ObservationWindowGlass"):
			if c is GeometryInstance3D:
				(c as GeometryInstance3D).cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
		elif c is MeshInstance3D:
			var mi: MeshInstance3D = c as MeshInstance3D
			if _mesh_has_opaque_surface(mi):
				mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_DOUBLE_SIDED
		for ch: Node in c.get_children():
			stack.append(ch)


func _mesh_has_opaque_surface(mi: MeshInstance3D) -> bool:
	if mi.mesh == null:
		return false
	for s_idx: int in range(mi.mesh.get_surface_count()):
		var mat: Material = mi.get_active_material(s_idx)
		if mat is BaseMaterial3D:
			if (mat as BaseMaterial3D).transparency == BaseMaterial3D.TRANSPARENCY_DISABLED:
				return true
		elif mat != null:
			return true
		else:
			return true
	return false


# Observation window: 36 degree radial wedge, full length, plus glass end caps.
# The drum pivot is not touched. GLB local +X is the spin axis; the axis sits at local (y = 200, z = 0)
# because the mesh node is offset by (0, -200, 0). Centroids are measured in that cyl_node frame.
func _cut_observation_window(cyl_node: Node3D, cyl_pivot: Node3D) -> void:
	# World centre direction: overhead, 60 deg from +Y toward -Z, so the deck looks up through the wedge.
	var d_w: Vector3 = Vector3(0.0, cos(deg_to_rad(60.0)), -sin(deg_to_rad(60.0)))
	# Pivot rotation only. The GLB child is translated, not rotated, so this is the GLB direction.
	var d: Vector3 = cyl_pivot.global_transform.basis.inverse() * d_w
	var a0: float = atan2(d.z, d.y)
	var half_rad: float = deg_to_rad(18.0)
	var removed_wedge: int = 0
	var removed_caps: int = 0
	var removed_map: int = 0
	# Outermost removed cap-triangle x on each end. Authored span if that end has no cap triangles.
	var cap_x_neg: float = -368.0
	var cap_x_pos: float = 354.0
	var found_neg: bool = false
	var found_pos: bool = false

	var stack: Array[Node] = [cyl_node]
	var meshes: Array[MeshInstance3D] = []
	while not stack.is_empty():
		var n: Node = stack.pop_back()
		if n is MeshInstance3D:
			meshes.append(n as MeshInstance3D)
		for ch: Node in n.get_children():
			stack.append(ch)

	# World AABB x -60..60, y -1..40, z -45..45. Twelve edges, four along each axis.
	var map_box: AABB = AABB(Vector3(-60.0, -1.0, -45.0), Vector3(120.0, 41.0, 90.0))
	var map_e0: PackedVector3Array = PackedVector3Array([
		Vector3(-60.0, -1.0, -45.0), Vector3(-60.0, 40.0, -45.0), Vector3(-60.0, -1.0, 45.0), Vector3(-60.0, 40.0, 45.0),
		Vector3(-60.0, -1.0, -45.0), Vector3(60.0, -1.0, -45.0), Vector3(-60.0, -1.0, 45.0), Vector3(60.0, -1.0, 45.0),
		Vector3(-60.0, -1.0, -45.0), Vector3(-60.0, 40.0, -45.0), Vector3(60.0, -1.0, -45.0), Vector3(60.0, 40.0, -45.0),
	])
	var map_e1: PackedVector3Array = PackedVector3Array([
		Vector3(60.0, -1.0, -45.0), Vector3(60.0, 40.0, -45.0), Vector3(60.0, -1.0, 45.0), Vector3(60.0, 40.0, 45.0),
		Vector3(-60.0, 40.0, -45.0), Vector3(60.0, 40.0, -45.0), Vector3(-60.0, 40.0, 45.0), Vector3(60.0, 40.0, 45.0),
		Vector3(-60.0, -1.0, 45.0), Vector3(-60.0, 40.0, 45.0), Vector3(60.0, -1.0, 45.0), Vector3(60.0, 40.0, 45.0),
	])

	for mi: MeshInstance3D in meshes:
		if mi.mesh == null or mi.mesh.get_surface_count() <= 0:
			continue
		var src: Mesh = mi.mesh
		# cyl_node-local = affine_inverse(cyl_node) * mi.global. Includes this instance's own transform.
		var to_cyl: Transform3D = cyl_node.global_transform.affine_inverse() * mi.global_transform
		var dst: ArrayMesh = ArrayMesh.new()
		for si: int in range(src.get_surface_count()):
			var arrays: Array = src.surface_get_arrays(si)
			# Active material wins (upgrade overrides). Fall back to the surface material.
			var mat: Material = mi.get_active_material(si)
			if mat == null:
				mat = src.surface_get_material(si)
			var prim: Mesh.PrimitiveType = src.surface_get_primitive_type(si)
			var verts_ok: bool = arrays.size() > Mesh.ARRAY_INDEX and arrays[Mesh.ARRAY_VERTEX] is PackedVector3Array
			# Lines and other non-triangle surfaces stay whole. A triangle surface with no positions is dropped.
			if prim != Mesh.PRIMITIVE_TRIANGLES:
				var pass_i: int = dst.get_surface_count()
				dst.add_surface_from_arrays(prim, arrays)
				if mat != null:
					dst.surface_set_material(pass_i, mat)
				continue
			if not verts_ok:
				continue
			var verts: PackedVector3Array = arrays[Mesh.ARRAY_VERTEX]
			if verts.is_empty():
				continue
			# Indexed surfaces use ARRAY_INDEX. Non-indexed vertices are already in triangle order.
			var index_v: Variant = arrays[Mesh.ARRAY_INDEX]
			var indices: PackedInt32Array = PackedInt32Array()
			if index_v is PackedInt32Array and (index_v as PackedInt32Array).size() >= 3:
				indices = index_v as PackedInt32Array
			else:
				indices.resize(verts.size())
				for vi: int in range(verts.size()):
					indices[vi] = vi
			var local_verts: PackedVector3Array = PackedVector3Array()
			local_verts.resize(verts.size())
			for vi2: int in range(verts.size()):
				local_verts[vi2] = to_cyl * verts[vi2]
			var tri_count: int = indices.size() / 3
			var kept: PackedInt32Array = PackedInt32Array()
			kept.resize(tri_count * 3)
			var kept_n: int = 0
			var vcount: int = local_verts.size()
			for t: int in range(tri_count):
				var i0: int = indices[t * 3]
				var i1: int = indices[t * 3 + 1]
				var i2: int = indices[t * 3 + 2]
				if i0 < 0 or i1 < 0 or i2 < 0 or i0 >= vcount or i1 >= vcount or i2 >= vcount:
					continue
				var p0: Vector3 = local_verts[i0]
				var p1: Vector3 = local_verts[i1]
				var p2: Vector3 = local_verts[i2]
				var c: Vector3 = (p0 + p1 + p2) / 3.0
				var r: float = Vector2(c.y - 200.0, c.z).length()
				var ang: float = atan2(c.z, c.y - 200.0)
				# angle_difference wraps, so the wedge stays correct across the +/- PI seam.
				var drop_wedge: bool = r >= 120.0 and absf(angle_difference(ang, a0)) <= half_rad
				var fn: Vector3 = (p1 - p0).cross(p2 - p0)
				var fn_len: float = fn.length()
				if fn_len > 0.0000001:
					fn = fn / fn_len
				else:
					fn = Vector3.ZERO
				# End caps face along the spin axis. r >= 20 leaves the tiny hub at the axis.
				var drop_cap: bool = absf(c.x) >= 330.0 and absf(fn.x) > 0.85 and r >= 20.0
				# Drum skin through the playable map is a flat ceiling over the deck and hides the window.
				# local_verts are cyl_node-local; world = cyl_node.global_transform * local_vertex.
				# Drop the face when it meets the map volume: a vertex inside, a triangle edge through the
				# box, or a box edge through the triangle.
				var w0: Vector3 = cyl_node.global_transform * p0
				var w1: Vector3 = cyl_node.global_transform * p1
				var w2: Vector3 = cyl_node.global_transform * p2
				var drop_map: bool = _world_triangle_hits_map_box(w0, w1, w2, map_box, map_e0, map_e1)
				if drop_wedge:
					removed_wedge += 1
				if drop_cap:
					removed_caps += 1
					if c.x < 0.0:
						if (not found_neg) or c.x < cap_x_neg:
							cap_x_neg = c.x
						found_neg = true
					elif c.x > 0.0:
						if (not found_pos) or c.x > cap_x_pos:
							cap_x_pos = c.x
						found_pos = true
				if drop_map:
					removed_map += 1
				if drop_wedge or drop_cap or drop_map:
					continue
				kept[kept_n] = i0
				kept_n += 1
				kept[kept_n] = i1
				kept_n += 1
				kept[kept_n] = i2
				kept_n += 1
			if kept_n <= 0:
				continue
			kept.resize(kept_n)
			# New index into the original vertex buffers. LODs are not copied, so a lower LOD cannot seal the hole.
			arrays[Mesh.ARRAY_INDEX] = kept
			var new_si: int = dst.get_surface_count()
			dst.add_surface_from_arrays(Mesh.PRIMITIVE_TRIANGLES, arrays)
			if mat != null:
				dst.surface_set_material(new_si, mat)
		# Overrides were baked onto dst above. Clear them so the rebuilt surfaces show those materials.
		for oi: int in range(src.get_surface_count()):
			mi.set_surface_override_material(oi, null)
		mi.mesh = dst

	print("[CYL-WINDOW] removed_wedge=%d removed_caps=%d removed_map=%d a0_deg=%.3f" % [removed_wedge, removed_caps, removed_map, rad_to_deg(a0)])

	# [M-15] No blanket self-emission. Only named luminous surfaces emit; the night side is ambient.
	for emi: MeshInstance3D in meshes:
		if emi.mesh == null:
			continue
		for s_idx: int in range(emi.mesh.get_surface_count()):
			var emat: Material = emi.get_active_material(s_idx)
			if emat is BaseMaterial3D:
				var bm: BaseMaterial3D = emat as BaseMaterial3D
				var dup: BaseMaterial3D = bm.duplicate() as BaseMaterial3D
				if dup == null:
					continue
				var blob: String = (bm.resource_name + " " + String(emi.name)).to_lower()
				var energy: float = _m15_emission_energy(blob, dup.emission_energy_multiplier, dup.emission_enabled)
				if energy < 0.0:
					dup.emission_enabled = false
					dup.emission_energy_multiplier = 0.0
				else:
					dup.emission_enabled = true
					dup.emission = Color(1, 1, 1, 1)
					dup.emission_energy_multiplier = energy
					if dup.emission_texture == null and dup.albedo_texture != null:
						dup.emission_texture = dup.albedo_texture
					if dup.emission_texture != null:
						dup.emission_operator = BaseMaterial3D.EMISSION_OP_MULTIPLY
				emi.set_surface_override_material(s_idx, dup)

	# [M-17]/[M-18] Three single-sided glass meshes. Each origin sits on its own centroid.
	# Normals face the habitat interior. From outside the hull the glass is not drawn.
	var glass_mat: StandardMaterial3D = _make_observation_window_glass_material()
	var wedge_segs: int = 12
	var strip_r: float = 199.0
	var strip_v: PackedVector3Array = PackedVector3Array()
	var strip_n: PackedVector3Array = PackedVector3Array()
	for seg: int in range(wedge_segs):
		var ang0: float = a0 - half_rad + (half_rad * 2.0) * float(seg) / float(wedge_segs)
		var ang1: float = a0 - half_rad + (half_rad * 2.0) * float(seg + 1) / float(wedge_segs)
		var n0: Vector3 = Vector3(0.0, cos(ang0), sin(ang0))
		var n1: Vector3 = Vector3(0.0, cos(ang1), sin(ang1))
		var p_n0: Vector3 = Vector3(-400.0, 200.0 + strip_r * n0.y, strip_r * n0.z)
		var p_n1: Vector3 = Vector3(-400.0, 200.0 + strip_r * n1.y, strip_r * n1.z)
		var p_f0: Vector3 = Vector3(400.0, 200.0 + strip_r * n0.y, strip_r * n0.z)
		var p_f1: Vector3 = Vector3(400.0, 200.0 + strip_r * n1.y, strip_r * n1.z)
		var mid: Vector3 = (p_n0 + p_n1 + p_f0) / 3.0
		var inward: Vector3 = Vector3(0.0, 200.0 - mid.y, -mid.z)
		_append_facing_tri(strip_v, strip_n, p_n0, p_f0, p_n1, inward)
		_append_facing_tri(strip_v, strip_n, p_n1, p_f0, p_f1, inward)
	_spawn_centered_mesh(cyl_node, strip_v, strip_n, glass_mat, "ObservationWindowGlass_Strip", -1, -50.0)
	var disc_r: float = 200.0
	var disc_segs: int = 48
	var cap_xs: Array[float] = [cap_x_neg, cap_x_pos]
	var cap_names: Array[String] = ["ObservationWindowGlass_CapA", "ObservationWindowGlass_CapB"]
	for cap_i: int in range(cap_xs.size()):
		var cap_x: float = cap_xs[cap_i]
		var cap_v: PackedVector3Array = PackedVector3Array()
		var cap_n: PackedVector3Array = PackedVector3Array()
		var interior_x: Vector3 = Vector3(1.0 if cap_x < 0.0 else -1.0, 0.0, 0.0)
		var center: Vector3 = Vector3(cap_x, 200.0, 0.0)
		for ds: int in range(disc_segs):
			var t0: float = TAU * float(ds) / float(disc_segs)
			var t1: float = TAU * float(ds + 1) / float(disc_segs)
			var rim0: Vector3 = Vector3(cap_x, 200.0 + disc_r * cos(t0), disc_r * sin(t0))
			var rim1: Vector3 = Vector3(cap_x, 200.0 + disc_r * cos(t1), disc_r * sin(t1))
			_append_facing_tri(cap_v, cap_n, center, rim0, rim1, interior_x)
		_spawn_centered_mesh(cyl_node, cap_v, cap_n, glass_mat, cap_names[cap_i], -2, 0.0)
	_add_observation_mullions(cyl_node, a0, cap_x_neg, cap_x_pos)
	_add_recreation_grass_slab(cyl_node, a0)


# One hard-edged triangle. Smooth group is set on every vertex so generate_normals
# does not blend this face into a neighbour that shares the corner position.
func _add_slab_tri(st: SurfaceTool, group: int, a: Vector3, b: Vector3, c: Vector3) -> void:
	st.set_smooth_group(group)
	st.set_uv(_slab_uv(a))
	st.add_vertex(a)
	st.set_smooth_group(group)
	st.set_uv(_slab_uv(b))
	st.add_vertex(b)
	st.set_smooth_group(group)
	st.set_uv(_slab_uv(c))
	st.add_vertex(c)


func _slab_uv(p: Vector3) -> Vector2:
	var ang: float = atan2(p.z, p.y - 200.0)
	var rel: float = angle_difference(ang, _slab_uv_a0)
	var span: float = _slab_uv_a1 - _slab_uv_a0
	var u: float = 0.0
	if absf(span) > 0.0001:
		u = clampf(rel / span, 0.0, 1.0)
	var width: float = _slab_uv_x1 - _slab_uv_x0
	var v: float = 0.0
	if absf(width) > 0.0001:
		v = clampf((p.x - _slab_uv_x0) / width, 0.0, 1.0)
	return Vector2(u, v)


# Axis sits at local (y = 200, z = 0). ang is atan2(z, y - 200), matching the window cut.
func _drum_shell_point(along_x: float, radius: float, ang: float) -> Vector3:
	return Vector3(along_x, 200.0 + radius * cos(ang), radius * sin(ang))


# Recreation placeholder opposite the window. Curved inner-shell slab, 36 degree wedge
# centred at a0 + PI. Top at r = 198 faces the axis; bottom at r = 199.5. Drum triangles
# under the slab are kept.
func _add_recreation_grass_slab(cyl_node: Node3D, a0: float) -> void:
	var a_rec: float = a0 + PI
	var half_rad: float = deg_to_rad(18.0)
	var segs: int = 24
	var x0: float = -360.0
	var x1: float = 350.0
	var r_top: float = 198.0
	var r_bot: float = 199.5
	_slab_uv_x0 = x0
	_slab_uv_x1 = x1
	_slab_uv_a0 = a_rec - half_rad
	_slab_uv_a1 = a_rec + half_rad
	var st: SurfaceTool = SurfaceTool.new()
	st.begin(Mesh.PRIMITIVE_TRIANGLES)
	for seg: int in range(segs):
		var ang0: float = a_rec - half_rad + (half_rad * 2.0) * float(seg) / float(segs)
		var ang1: float = a_rec - half_rad + (half_rad * 2.0) * float(seg + 1) / float(segs)
		var top00: Vector3 = _drum_shell_point(x0, r_top, ang0)
		var top01: Vector3 = _drum_shell_point(x0, r_top, ang1)
		var top10: Vector3 = _drum_shell_point(x1, r_top, ang0)
		var top11: Vector3 = _drum_shell_point(x1, r_top, ang1)
		var bot00: Vector3 = _drum_shell_point(x0, r_bot, ang0)
		var bot01: Vector3 = _drum_shell_point(x0, r_bot, ang1)
		var bot10: Vector3 = _drum_shell_point(x1, r_bot, ang0)
		var bot11: Vector3 = _drum_shell_point(x1, r_bot, ang1)
		# Top: clockwise from the axis, so the generated normal points toward the axis.
		_add_slab_tri(st, 1, top00, top01, top10)
		_add_slab_tri(st, 1, top01, top11, top10)
		# Bottom: opposite winding, normal away from the axis.
		_add_slab_tri(st, 2, bot00, bot10, bot01)
		_add_slab_tri(st, 2, bot01, bot10, bot11)
		# Cap at local x = -360, normal -X.
		_add_slab_tri(st, 3, top00, bot00, top01)
		_add_slab_tri(st, 3, top01, bot00, bot01)
		# Cap at local x = 350, normal +X.
		_add_slab_tri(st, 4, top10, top11, bot10)
		_add_slab_tri(st, 4, top11, bot11, bot10)
	var a_lo: float = a_rec - half_rad
	var a_hi: float = a_rec + half_rad
	var lo_top0: Vector3 = _drum_shell_point(x0, r_top, a_lo)
	var lo_top1: Vector3 = _drum_shell_point(x1, r_top, a_lo)
	var lo_bot0: Vector3 = _drum_shell_point(x0, r_bot, a_lo)
	var lo_bot1: Vector3 = _drum_shell_point(x1, r_bot, a_lo)
	var hi_top0: Vector3 = _drum_shell_point(x0, r_top, a_hi)
	var hi_top1: Vector3 = _drum_shell_point(x1, r_top, a_hi)
	var hi_bot0: Vector3 = _drum_shell_point(x0, r_bot, a_hi)
	var hi_bot1: Vector3 = _drum_shell_point(x1, r_bot, a_hi)
	# Wedge sides. Outward is the decreasing-angle direction at a_lo, increasing at a_hi.
	_add_slab_tri(st, 5, lo_top0, lo_top1, lo_bot0)
	_add_slab_tri(st, 5, lo_top1, lo_bot1, lo_bot0)
	_add_slab_tri(st, 6, hi_top0, hi_bot0, hi_top1)
	_add_slab_tri(st, 6, hi_top1, hi_bot0, hi_bot1)
	st.generate_normals()
	var grass_mi: MeshInstance3D = MeshInstance3D.new()
	grass_mi.name = "RecreationGrassSlab"
	grass_mi.mesh = st.commit()
	var grass_mat: StandardMaterial3D = StandardMaterial3D.new()
	# [M-35] 2 m tiles: mesh UVs are 0–1 across the arc and the axial width.
	var arc_len: float = r_top * (half_rad * 2.0)
	var slab_w: float = x1 - x0
	grass_mat.albedo_color = Color(1, 1, 1, 1)
	grass_mat.roughness = 1.0
	grass_mat.cull_mode = BaseMaterial3D.CULL_BACK
	grass_mat.uv1_scale = Vector3(arc_len / 2.0, slab_w / 2.0, 1.0)
	var grass_alb: Texture2D = _load_tex("qa03/rec_grass_albedo.png")
	var grass_nrm: Texture2D = _load_tex("qa03/rec_grass_normal.png")
	var grass_orm: Texture2D = _load_tex("qa03/rec_grass_orm.png")
	if grass_alb != null:
		grass_mat.albedo_texture = grass_alb
	if grass_nrm != null:
		grass_mat.normal_enabled = true
		grass_mat.normal_texture = grass_nrm
		grass_mat.normal_scale = 0.6
	if grass_orm != null:
		grass_mat.roughness_texture = grass_orm
		grass_mat.roughness_texture_channel = BaseMaterial3D.TEXTURE_CHANNEL_GREEN
		grass_mat.ao_enabled = true
		grass_mat.ao_texture = grass_orm
		grass_mat.ao_texture_channel = BaseMaterial3D.TEXTURE_CHANNEL_RED
		grass_mat.ao_light_affect = 0.3
	grass_mi.material_override = grass_mat
	cyl_node.add_child(grass_mi)
	print("[CYL-REC] grass slab a_deg=%.3f" % rad_to_deg(a_rec))


func _make_signage_skin_material(v_offset: float, v_scale: float) -> StandardMaterial3D:
	var mat: StandardMaterial3D = StandardMaterial3D.new()
	mat.albedo_color = Color(1.0, 1.0, 1.0, 1.0)
	mat.roughness = 0.28
	mat.metallic = 0.65
	mat.uv1_scale = Vector3(1.0, v_scale, 1.0)
	mat.uv1_offset = Vector3(0.0, v_offset, 0.0)
	var t_alb: Texture2D = _load_tex("sector_door_signage_skin_albedo.png")
	var t_emi: Texture2D = _load_tex("sector_door_signage_skin_emission.png")
	var t_nrm: Texture2D = _load_tex("sector_door_signage_skin_normal.png")
	if t_alb != null:
		mat.albedo_texture = t_alb
	if t_emi != null:
		mat.emission_enabled = true
		mat.emission = Color(1.0, 1.0, 1.0, 1.0)
		mat.emission_texture = t_emi
		mat.emission_operator = BaseMaterial3D.EMISSION_OP_MULTIPLY
		mat.emission_energy_multiplier = 0.85
	if t_nrm != null:
		mat.normal_enabled = true
		mat.normal_texture = t_nrm
		mat.normal_scale = 0.85
	return mat


func _add_skinned_door_header_sign(parent: Node3D, nm: String, row_idx: int, pos: Vector3, rot_y_deg: float, width_m: float = 2.04, height_m: float = 0.30) -> void:
	var holder: Node3D = Node3D.new()
	holder.name = nm
	holder.position = pos
	holder.rotation_degrees = Vector3(0.0, rot_y_deg, 0.0)
	parent.add_child(holder)

	# Flush textured signboard skin face applied directly to the front face of the doorway header lintel beam (zero floating box!)
	var face: MeshInstance3D = MeshInstance3D.new()
	face.name = nm + "_SkinFace"
	var qm: QuadMesh = QuadMesh.new()
	qm.size = Vector2(width_m, height_m)
	face.mesh = qm
	var v_scale: float = 220.0 / 2048.0
	var v_offset: float = float(row_idx) * v_scale
	face.material_override = _make_signage_skin_material(v_offset, v_scale)
	face.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	holder.add_child(face)


func _build_crisp_3d_signage_and_wall_monitor(parent: Node3D) -> void:
	var sign_root: Node3D = Node3D.new()
	sign_root.name = "SkinnedArchitecturalSignage"
	parent.add_child(sign_root)

	# 1. Flush-mounted Textured Doorway Header Skins directly on the front face of all 6 Portal Lintel Beams (zero Label3D, zero beam clipping!)
	# - Open_Portal_201 (APT 201, lintel Y = 6.985..7.345m -> center Y = 7.165m, front face Z = 2.610m -> skin at Z = 2.607m)
	_add_skinned_door_header_sign(sign_root, "HeaderSign_APT201", 0, Vector3(-11.20, 7.165, 2.606), 180.0, 2.32, 0.32)
	# - Open_Arch_2C (Alcove 2C, lintel Y = 6.885..7.245m -> center Y = 7.065m, front face Z = -3.690m -> skin at Z = -3.694m)
	_add_skinned_door_header_sign(sign_root, "HeaderSign_ALCOVE2C", 1, Vector3(-11.50, 7.065, -3.694), 180.0, 2.12, 0.32)
	# - Open_Portal_202 (APT 202, lintel Y = 6.985..7.345m -> center Y = 7.165m, front face Z = 2.610m -> skin at Z = 2.606m)
	_add_skinned_door_header_sign(sign_root, "HeaderSign_APT202", 2, Vector3(7.80, 7.165, 2.606), 180.0, 2.32, 0.32)
	# - Open_Portal_1A (RM 1A Laundry Lounge, lintel Y = 2.835..3.195m -> center Y = 3.015m, front face Z = 2.710m -> skin at Z = 2.706m)
	_add_skinned_door_header_sign(sign_root, "HeaderSign_RM1A", 3, Vector3(-8.50, 3.015, 2.706), 180.0, 2.72, 0.32)
	# - Open_Portal_1B (RM 1B Bot Substation, lintel Y = 2.835..3.195m -> center Y = 3.015m, front face Z = 2.710m -> skin at Z = 2.706m)
	_add_skinned_door_header_sign(sign_root, "HeaderSign_RM1B", 4, Vector3(4.50, 3.015, 2.706), 180.0, 2.52, 0.32)
	# - Open_Portal_Sector_Exit (Sector-4 Promenade Exit, lintel Y = 3.035..3.395m -> center Y = 3.215m, atrium face Z = -8.760m, exterior face Z = -9.040m)
	_add_skinned_door_header_sign(sign_root, "HeaderSign_Sector4Exit_Interior", 5, Vector3(0.0, 3.215, -8.756), 0.0, 2.92, 0.32)
	_add_skinned_door_header_sign(sign_root, "HeaderSign_Sector4Exit_Exterior", 5, Vector3(0.0, 3.215, -9.044), 180.0, 2.92, 0.32)

	# 2. APT 201 Recessed Wall Diagnostic / Hab-7 Telemetry Monitor with Flush Textured OLED Screen Skin
	var mon_root: Node3D = Node3D.new()
	mon_root.name = "Apt201_WallDiagnosticMonitor"
	mon_root.position = Vector3(-7.80, 6.00, 2.86)
	sign_root.add_child(mon_root)

	var bezel_mi: MeshInstance3D = MeshInstance3D.new()
	bezel_mi.name = "MonitorAnodizedBezel"
	var bezel_bm: BoxMesh = BoxMesh.new()
	bezel_bm.size = Vector3(1.94, 1.14, 0.05)
	bezel_mi.mesh = bezel_bm
	var bezel_mat: StandardMaterial3D = StandardMaterial3D.new()
	bezel_mat.albedo_color = Color(0.15, 0.18, 0.22, 1.0)
	bezel_mat.metallic = 0.85
	bezel_mat.roughness = 0.25
	bezel_mi.material_override = bezel_mat
	bezel_mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	mon_root.add_child(bezel_mi)

	var scr_mi: MeshInstance3D = MeshInstance3D.new()
	scr_mi.name = "MonitorOLEDScreenSkin"
	var scr_qm: QuadMesh = QuadMesh.new()
	scr_qm.size = Vector2(1.82, 1.02)
	scr_mi.mesh = scr_qm
	scr_mi.position = Vector3(0.0, 0.0, 0.028)
	var mon_mat: StandardMaterial3D = _make_signage_skin_material(1320.0 / 2048.0, 728.0 / 2048.0)
	mon_mat.roughness = 0.12
	mon_mat.metallic = 0.18
	scr_mi.material_override = mon_mat
	scr_mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	mon_root.add_child(scr_mi)


func _retire_apartment_workbench(sector: Node3D) -> void:
	# Rev C.2 moved #26 out of the building. The Rev C shell has no Apartment_Workbench node; if one is
	# present it stays in INTERIOR_ARCH_NODE_NAMES but is hidden and non-colliding.
	var wb: Node = _lookup_sector_node(sector, "Apartment_Workbench")
	if wb == null:
		return
	if wb is Node3D:
		(wb as Node3D).visible = false
	var stack: Array[Node] = [wb]
	while not stack.is_empty():
		var c: Node = stack.pop_back()
		if c is CollisionShape3D:
			(c as CollisionShape3D).disabled = true
		elif c is CollisionObject3D:
			(c as CollisionObject3D).collision_layer = 0
			(c as CollisionObject3D).collision_mask = 0
		for ch: Node in c.get_children():
			stack.append(ch)


func _assemble_open_doorless_sector() -> void:
	for ch: Node in _arch_container.get_children():
		ch.free()

	var sector_path: String = _find_first_existing(SECTOR_GLB_PATHS)
	var sector_node: Node3D = _load_glb_scene(sector_path, 0.65)
	if sector_node != null:
		sector_node.name = "PrefaceResidentialSector_Doorless"
		_arch_container.add_child(sector_node)
		_remove_baked_leaf_doors_and_grates(sector_node)
		# Hide before trimesh build so the retired bench never gets a collider.
		_retire_apartment_workbench(sector_node)
		if not _batch_render:
			var n_col: int = _add_sector_trimesh_collisions(sector_node)
			if _validate_only:
				print("[PrefacePlayableArea] Trimesh colliders: ", n_col)
	else:
		push_warning("[PrefacePlayableArea] Sector GLB not found in SECTOR_GLB_PATHS")
	_spawn_rev_c_stair_core(_arch_container)
	_add_architectural_shadow_occluders(_arch_container)
	if not _batch_render:
		_add_safety_floor_colliders(_arch_container)
		_add_glass_balustrade_colliders(_arch_container)
		_add_m58_edge_guards(_arch_container)

	_build_cylinder_hab7_fullscale_world(_arch_container)
	_build_crisp_3d_signage_and_wall_monitor(_arch_container)
	if not _batch_render:
		_build_cylinder_gravity_ring(_arch_container)


# Rev C switchback (M-70). Both GLBs use the sector's building-plan origin.
func _spawn_rev_c_stair_core(parent: Node3D) -> void:
	var specs: Array[Dictionary] = [
		{"path": STAIR_SET_GLB, "name": "StairSetSwitchback"},
		{"path": STAIR_GUARD_GLB, "name": "StairGuardHandrail"},
	]
	var root_for_fallback: Node3D = parent
	for spec: Dictionary in specs:
		var node: Node3D = _load_glb_scene(String(spec["path"]), 0.65)
		if node == null:
			push_warning("[M-70] missing %s" % String(spec["path"]))
			continue
		node.name = String(spec["name"])
		node.transform = Transform3D.IDENTITY
		parent.add_child(node)
		_stair_build_col_shapes(node)
		if String(spec["name"]) == "StairSetSwitchback":
			root_for_fallback = node
	var tally: Dictionary = _stair_tally_col_bodies(parent)
	var fallback_n: int = _stair_fallback_walk_surfaces(root_for_fallback)
	var ramps: int = int(tally["ramps"])
	var guards: int = int(tally["guards"])
	if fallback_n > 0:
		push_warning("[M-70] stair walk surfaces fallback=%d" % fallback_n)
	if guards < 18:
		push_warning("[M-70] guard hulls %d/18" % guards)
	print("[M-70] stair core loaded ramps=%d guards=%d fallback_ramps=%d" % [ramps, guards, fallback_n])


func _stair_is_col_mesh(mi: MeshInstance3D) -> bool:
	# Visible treads (Flight1_Cast, Treads_Slate, Nosing_Emergency, Mid_Landing,
	# L2_Landing, Guard_Glass) are not col meshes and must not get a trimesh.
	var nm: String = String(mi.name).to_lower()
	if nm.contains("colonly") or nm.contains("convcol") or nm.ends_with("_col"):
		return true
	if mi.mesh == null:
		return false
	var rn: String = String(mi.mesh.resource_name).to_lower()
	if not rn.ends_with("_col"):
		return false
	return nm.contains("flight") or nm.contains("ramp") or nm.contains("landing") or nm.contains("guard_glass")


func _stair_build_col_shapes(root: Node3D) -> void:
	var stack: Array[Node] = [root]
	var meshes: Array[MeshInstance3D] = []
	while not stack.is_empty():
		var curr: Node = stack.pop_back()
		if curr is MeshInstance3D:
			meshes.append(curr as MeshInstance3D)
		for ch: Node in curr.get_children():
			stack.append(ch)
	for mi: MeshInstance3D in meshes:
		if not is_instance_valid(mi) or not _stair_is_col_mesh(mi):
			continue
		var nm: String = String(mi.name)
		var low: String = nm.to_lower()
		var holder: Node = mi.get_parent()
		var already: bool = holder is StaticBody3D or holder is CollisionShape3D
		if not already:
			for ch: Node in mi.get_children():
				if ch is StaticBody3D or ch is CollisionShape3D:
					already = true
					break
		mi.visible = false
		if already or holder == null:
			continue
		var faces: PackedVector3Array = PackedVector3Array()
		if mi.mesh != null:
			faces = mi.mesh.get_faces()
		var xf: Transform3D = mi.transform
		mi.name = nm + "_Vis"
		if faces.size() < 3:
			continue
		var body: StaticBody3D = StaticBody3D.new()
		body.name = nm
		body.collision_layer = 1
		body.collision_mask = 1
		body.transform = xf
		holder.add_child(body)
		var cs: CollisionShape3D = CollisionShape3D.new()
		cs.name = nm + "_Shape"
		if low.contains("convcol"):
			var convex: ConvexPolygonShape3D = ConvexPolygonShape3D.new()
			convex.points = faces
			convex.margin = 0.0
			cs.shape = convex
		else:
			var concave: ConcavePolygonShape3D = ConcavePolygonShape3D.new()
			concave.data = faces
			concave.margin = 0.0
			cs.shape = concave
		body.add_child(cs)


func _stair_walk_stem_match(low: String, stem: String) -> bool:
	if low.ends_with("_shape") or low.ends_with("_vis"):
		return false
	return low == stem + "-colonly" or low == stem + "_col" or low.begins_with(stem + "-col")


func _stair_tally_col_bodies(root: Node) -> Dictionary:
	var ramps: int = 0
	var guards: int = 0
	var stack: Array[Node] = [root]
	while not stack.is_empty():
		var c: Node = stack.pop_back()
		if c is StaticBody3D or c is CollisionShape3D:
			var low: String = String(c.name).to_lower()
			if low.begins_with("guard_glass_") and (low.contains("convcol") or low.ends_with("_col")) and not low.ends_with("_shape") and not low.ends_with("_vis"):
				guards += 1
			elif _stair_walk_stem_match(low, "flight1_ramp") or _stair_walk_stem_match(low, "flight2_ramp") or _stair_walk_stem_match(low, "mid_landing") or _stair_walk_stem_match(low, "l2_landing"):
				ramps += 1
		for ch: Node in c.get_children():
			stack.append(ch)
	return {"ramps": ramps, "guards": guards}


func _stair_has_named_col(root: Node, token: String) -> bool:
	var stem: String = token.split("-")[0].to_lower()
	var stack: Array[Node] = [root]
	while not stack.is_empty():
		var c: Node = stack.pop_back()
		if (c is StaticBody3D or c is CollisionShape3D) and _stair_walk_stem_match(String(c.name).to_lower(), stem):
			return true
		for ch: Node in c.get_children():
			stack.append(ch)
	return false


func _stair_add_box(parent: Node3D, nm: String, x0: float, x1: float, y0: float, y1: float, z0: float, z1: float) -> void:
	var body: StaticBody3D = StaticBody3D.new()
	body.name = nm
	body.collision_layer = 1
	body.collision_mask = 1
	parent.add_child(body)
	var cs: CollisionShape3D = CollisionShape3D.new()
	cs.name = nm + "_Shape"
	var shape: BoxShape3D = BoxShape3D.new()
	shape.size = Vector3(absf(x1 - x0), absf(y1 - y0), absf(z1 - z0))
	shape.margin = 0.0
	cs.shape = shape
	cs.position = Vector3((x0 + x1) * 0.5, (y0 + y1) * 0.5, (z0 + z1) * 0.5)
	body.add_child(cs)


# Top face is the segment (za, ya) -> (zb, yb). Same construction as
# stair_core_colliders_rev_c.slab_between: drop the box by TH/2, then
# Basis(RIGHT, -ang) with ang = atan2(dy, dz).
# Flight 2 check (ang > 0, rises toward +Z): local +Z maps to (0, sin(ang), cos(ang))
# and local +Y maps to (0, cos(ang), -sin(ang)), so the normal stays upward.
func _stair_add_ramp(parent: Node3D, nm: String, x0: float, x1: float, za: float, ya: float, zb: float, yb: float) -> void:
	if zb < za:
		var swap_z: float = za
		var swap_y: float = ya
		za = zb
		ya = yb
		zb = swap_z
		yb = swap_y
	var ang: float = atan2(yb - ya, zb - za)
	var length: float = Vector2(zb - za, yb - ya).length()
	var mid: Vector3 = Vector3((x0 + x1) * 0.5, (ya + yb) * 0.5, (za + zb) * 0.5)
	var body: StaticBody3D = StaticBody3D.new()
	body.name = nm
	body.collision_layer = 1
	body.collision_mask = 1
	body.transform = Transform3D(Basis(Vector3.RIGHT, -ang), mid)
	parent.add_child(body)
	var cs: CollisionShape3D = CollisionShape3D.new()
	cs.name = nm + "_Shape"
	var shape: BoxShape3D = BoxShape3D.new()
	shape.size = Vector3(absf(x1 - x0), 0.20, length)
	shape.margin = 0.0
	cs.shape = shape
	cs.position = Vector3(0.0, -0.10, 0.0)
	body.add_child(cs)


func _stair_fallback_walk_surfaces(parent: Node3D) -> int:
	var rise: float = 4.2
	var r: float = rise / 26.0
	var tread: float = 0.28
	var yl: float = 16.0 * r
	var zs: float = -8.9
	var zn: float = -0.8
	var zl: float = zs + 1.5
	var z1b: float = zl + 15.0 * tread
	var z2t: float = zl + 9.0 * tread
	var added: int = 0
	if not _stair_has_named_col(parent, "Flight1_Ramp-colonly"):
		_stair_add_ramp(parent, "Flight1_Ramp-colonly", -1.9, -0.4, z1b + tread, 0.0, zl, yl)
		added += 1
	if not _stair_has_named_col(parent, "Flight2_Ramp-colonly"):
		_stair_add_ramp(parent, "Flight2_Ramp-colonly", 0.4, 1.9, zl - tread, yl, z2t, rise)
		added += 1
	if not _stair_has_named_col(parent, "Mid_Landing-colonly"):
		_stair_add_box(parent, "Mid_Landing-colonly", -1.9, 1.9, yl - 0.25, yl, zs, zl)
		added += 1
	if not _stair_has_named_col(parent, "L2_Landing-colonly"):
		_stair_add_box(parent, "L2_Landing-colonly", -1.9, 1.9, rise - 0.30, rise, z2t, zn)
		added += 1
	return added


# ------------------------------------------------------------------------------
# Pickups & #04 Wrist rig (BUG-06)
# ------------------------------------------------------------------------------
func _instantiate_pickup_model(path: String, kind: String) -> Node3D:
	if _pickup_templates.has(kind):
		var tpl: Node3D = _pickup_templates[kind] as Node3D
		if tpl != null and is_instance_valid(tpl):
			return tpl.duplicate() as Node3D
	var loaded: Node3D = _load_glb_scene(path, 0.85)
	if loaded != null:
		_pickup_templates[kind] = loaded.duplicate()
	return loaded


func _spawn_pickup(path: String, nm: String, kind: String, label: String, pos: Vector3, sc: float, count_max: bool = true) -> void:
	if count_max:
		_inventory_max[kind] = int(_inventory_max[kind]) + 1
	if _collected_pickup_ids.has(nm):
		return
	var node: Node3D = _instantiate_pickup_model(path, kind)
	if node == null:
		return
	node.name = nm
	node.position = pos
	node.scale = Vector3(sc, sc, sc)
	_props_container.add_child(node)
	_interactables.append({"node": node, "id": nm, "kind": kind, "label": label, "collected": false, "pickup": true})


func _add_support_box(body: StaticBody3D, part_name: String, sz: Vector3, local_pos: Vector3, mat: Material) -> void:
	var cs := CollisionShape3D.new()
	cs.name = part_name + "_Shape"
	var shape := BoxShape3D.new()
	shape.size = sz
	shape.margin = 0.0
	cs.shape = shape
	cs.position = local_pos
	body.add_child(cs)
	var mi := MeshInstance3D.new()
	mi.name = part_name + "_Mesh"
	var bm := BoxMesh.new()
	bm.size = sz
	mi.mesh = bm
	mi.position = local_pos
	mi.material_override = mat
	body.add_child(mi)


## M-08 / GEO-12. Pickup origins are the mesh bottom. The slab top meets that y.
## A post runs down to the floor so the slab does not float. L1 floor y=0.12, L2 slab top y=4.2.
func _add_pickup_support(pickup_name: String, pos: Vector3) -> void:
	if _props_container == null:
		return
	var nm := pickup_name + "_Support"
	if _props_container.get_node_or_null(nm) != null:
		return
	var floor_y: float = 0.12 if pos.y < 3.0 else 4.2
	var slab_t := 0.04
	var post_top: float = pos.y - slab_t
	if post_top <= floor_y + 0.001:
		return
	var body := StaticBody3D.new()
	body.name = nm
	body.position = Vector3(pos.x, 0.0, pos.z)
	_props_container.add_child(body)
	var mat := StandardMaterial3D.new()
	mat.albedo_color = Color(0.22, 0.24, 0.27)
	mat.roughness = 0.55
	mat.metallic = 0.4
	var slab_y: float = pos.y - slab_t * 0.5
	var post_h: float = post_top - floor_y
	var post_y: float = floor_y + post_h * 0.5
	# 0.42 m top is wider than the scaled spool/cell and stays off the nearby walls.
	_add_support_box(body, "Shelf", Vector3(0.42, slab_t, 0.42), Vector3(0.0, slab_y, 0.0), mat)
	_add_support_box(body, "Post", Vector3(0.12, post_h, 0.12), Vector3(0.0, post_y, 0.0), mat)


func _spawn_interior_pickups(initial_setup: bool = false) -> int:
	var wire_path: String = _find_first_existing(PICKUP_WIRE_PATHS)
	var batt_path: String = _find_first_existing(PICKUP_BATT_PATHS)

	# Rev C.2 removed the four APT 201 workbench pickups (wire, BCI, jelly, battery) with the terminal.
	var specs: Array[Array] = [
		[wire_path, "Alcove2C_SuperWire_Expansion", "wire", "SUPER-WIRE SPOOL", Vector3(-11.55, 5.02, -4.95), 1.15],
		[batt_path, "Alcove2C_Battery_Expansion", "batt", "+5A BATTERY CELL", Vector3(-10.75, 5.02, -4.95), 1.15],
		[batt_path, "Apt202_Desk_Battery_Cell", "batt", "+5A BATTERY CELL", Vector3(10.70, 5.10, 7.20), 1.10],
		[wire_path, "Room1A_Laundry_SuperWire_Spool", "wire", "SUPER-WIRE SPOOL", Vector3(-6.15, 0.98, 7.25), 1.15],
		[batt_path, "Room1B_Substation_Battery_Cell", "batt", "+5A BATTERY CELL", Vector3(7.20, 0.98, 7.10), 1.15]
	]
	var spawned: int = 0
	for s: Array in specs:
		var nm: String = String(s[1])
		var pos: Vector3 = s[4] as Vector3
		_spawn_pickup(String(s[0]), nm, String(s[2]), String(s[3]), pos, float(s[5]), initial_setup)
		_add_pickup_support(nm, pos)
		if not _collected_pickup_ids.has(nm):
			spawned += 1

	# Rev C.2 removed Apt201_ToolWall_DiagnosticTerminal (the workbench objective) and
	# Hatch_D204_EmitterPanel (the 204 emitter-wall door beat). No #24 lockers are spawned.
	return spawned


# Rev C.2 ghost of #26. Literal plan rect F(-13.9, 6.4, -10.2, 8.9): 3.7 x 2.5 m, center (-12.05, 7.65).
# Flat decal on the Section 2 L2 floor datum (y=4.415). No collider. #54 decal GLB is not modeled.
func _spawn_apt201_bench_outline() -> void:
	if _props_container == null:
		return
	if _props_container.get_node_or_null("Apt201_ExBench_DustOutline") != null:
		return
	var deck: MeshInstance3D = MeshInstance3D.new()
	deck.name = "Apt201_ExBench_DustOutline"
	var quad: QuadMesh = QuadMesh.new()
	quad.size = Vector2(3.7, 2.5)
	quad.orientation = PlaneMesh.FACE_Y
	deck.mesh = quad
	# [M-48] 6 mm above the previous 4.418 placement. Lit, so emergency ambient/sun dims it. No collider.
	deck.position = Vector3(-12.05, 4.203, 7.65) # [M-71] Rev C L2 floor 4.20 + 3 mm (was the pre-Rev C 4.415 datum)
	var mat: StandardMaterial3D = StandardMaterial3D.new()
	mat.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
	mat.albedo_color = Color(1, 1, 1, 1)
	mat.roughness = 1.0
	mat.metallic = 0.0
	mat.cull_mode = BaseMaterial3D.CULL_BACK
	mat.depth_draw_mode = BaseMaterial3D.DEPTH_DRAW_DISABLED
	var dust_tex: Texture2D = _load_tex("qa03/apt201_bench_dust_outline_decal.png")
	if dust_tex != null:
		mat.albedo_texture = dust_tex
	mat.render_priority = -1
	deck.material_override = mat
	deck.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	_props_container.add_child(deck)


# Baked one-shot / loop clips. Pivot is bottom-centre, front is local +Z, back is local -Z.
# Loaded Rev C shell: L1 floor top y=0.12. Generator L2 slab top is 4.2
# (preface_sector_rev_c_generator.py L2). placement_assert reads this const.
# Yaw 180 maps local -Z onto world +Z (back toward the north wall, inner face z=8.9).
# Yaw 0 maps local -Z onto world -Z.
# Yaw 90 maps local -Z onto world -X. Yaw -90 maps local -Z onto world +X.
# Static Rev C props are REV_C_STATIC_PROP_SPECS, not in this list.
# Not placed: #18 cubbies, #24 lockers, #17 lab bench, #26 workbench, #29 specimen shelf,
# #31 emitter bench, #33 tiered planter, window desks.
const ANIMATED_PROP_SPECS: Array[Dictionary] = [
	{
		# Laundry north wall. 8 mm off inner face z=8.9 (a gap of 0 fails the wall check).
		# x -1.64 keeps a 0.03 m gap east of Prop39 after that seat clears the 101 pier.
		"id": "Prop38_FoldingCounter",
		"path": "res://assets/models/folding_counter_fold_leaf_3p0.glb",
		"position": Vector3(-1.64, 0.12, 8.592),
		"yaw": 180.0,
		"mount": "wall",
		"label": "LAUNDRY FOLDING COUNTER",
		"toggle": ["Leaf_Fold_Up", "Leaf_Fold_Down"],
		"action": "",
		"idle": ""
	},
	{
		# Laundry north wall, east of the 101|Laundry pier (solid x -4.6..-4.4). 8 mm off z=8.9.
		# Footprint local x ±0.6 sits at world x -4.37..-3.17, clear of that pier, with the front zone south of it.
		"id": "Prop39_FlipSeat",
		"path": "res://assets/models/laundry_bench_wall_flip_seat.glb",
		"position": Vector3(-3.77, 0.12, 8.692),
		"yaw": 180.0,
		"mount": "wall",
		"label": "LAUNDRY FLIP SEAT",
		"toggle": ["Seat_Flip_Down", "Seat_Flip_Up"],
		"action": "",
		"idle": ""
	},
	{
		# M-44. Maintenance east wall, inner face x=5.9. Mesh depth 0.8 (local Z -0.4..0.4).
		# Yaw -90 maps local -Z onto world +X, so the back is 8 mm off the wall.
		# Width 2.5 m. Centre z 2.40 puts the footprint at z 1.15..3.65, 0.15 m clear of the
		# corridor wall (inner face z=1.0). North of that is open floor; Kelvin is at z=6.0,
		# and the Maintenance door (x 2.2..4.2) does not reach this x.
		"id": "Prop42_Substation",
		"path": "res://assets/models/substation_wall_ladder_busway.glb",
		"position": Vector3(5.492, 0.12, 2.40),
		"yaw": -90.0,
		"mount": "wall",
		"label": "MAINTENANCE SUBSTATION",
		"toggle": [],
		"action": "Cell_Swap",
		"idle": "Port_Ready_Blink"
	},
	{
		# Room 101 east wall. Partition inner face is x=-4.6 (not the old lounge face at x=-4.90).
		# Local -Z depth is 0.25, yaw -90 maps that onto +X. Pivot is 0.258 m west (8 mm gap).
		"id": "Prop43_SparesDispenser",
		"path": "res://assets/models/spares_gravity_dispenser.glb",
		"position": Vector3(-4.858, 0.12, 5.20),
		"yaw": -90.0,
		"mount": "wall",
		"label": "MAINTENANCE SPARES DISPENSER",
		"toggle": [],
		"action": "Capsule_Drop",
		"idle": "Pick_Ready_Blink"
	}
]


# Bottom-centre, local +Z front. Section 2 vectors, except the Dobsonian, both lab crates and the
# cycler lightbox, which use Rev C plan rects in this same frame (XZ identity, L1 floor y=0.12, L2 floor y=4.2).
# 104/204 lamps sit on the floor. The window-desk GLBs are not placed.
const REV_C_STATIC_PROP_SPECS: Array[Dictionary] = [
	{
		# #32 room 203 south wall. Bunk slot X -11.2..-10.3. Back plate is local z=-0.1, so the
		# pivot sits at z=-8.8 and the plate meets the inner face z=-8.9. Yaw 0 faces +Z into the room.
		"id": "Cycler_Route_Lightbox",
		"path": "res://assets/models/cycler_route_lightbox.glb",
		"position": Vector3(-10.75, 4.2, -8.8),
		"yaw": 0.0
	},
	{
		# #30 room 104. Mirrored bin slot center (9.2, -8.6). +Z is the objective, toward the south window.
		"id": "Telescope_Pier_Dobsonian",
		"path": "res://assets/models/telescope_pier_dobsonian.glb",
		"position": Vector3(9.2, 0.12, -8.6),
		"yaw": 180.0
	},
	{
		# #14 Section 2.
		"id": "Tea_Set_Rail_Caddy",
		"path": "res://assets/models/tea_set_rail_caddy.glb",
		"position": Vector3(1.50, 0.12, 7.89),
		"yaw": 180.0
	},
	{
		# #23 room 102. Section 2.
		"id": "Suit_Storage_Service_Combo",
		"path": "res://assets/models/suit_storage_service_combo.glb",
		"position": Vector3(7.82, 0.12, 4.85),
		"yaw": -90.0
	},
	{
		# #36 Section 2. Pivot offset is already in the vector.
		"id": "Clutter_Kit_Magnet_Dock",
		"path": "res://assets/models/clutter_kit_magnet_dock.glb",
		"position": Vector3(5.69, 4.2, 5.025),
		"yaw": 90.0
	},
	{
		# M-42 / #55. Yaw 90 maps the 1.3 m width onto world Z (4.70..6.00) and the 0.3 m depth
		# onto world X. Centre x=1.40 is footprint x 1.25..1.55, clear of the tool wall (x<=1.1)
		# and of the tea caddy (z 7.7..8.1).
		"id": "Lost_And_Found_Rail_Bins",
		"path": "res://assets/models/lost_and_found_rail_bins.glb",
		"position": Vector3(1.40, -0.27, 5.35), # [M-64/LAY-21] mesh bottom is +0.39 over the pivot; this rests it on the L1 floor 0.12
		"yaw": 90.0
	},
	{
		# #53 room 104. Plan F(7.4, -8.9, 8.4, -8.3), center (7.9, -8.6). Front glyph into the room.
		"id": "Lab_Crate_Frame_104",
		"path": "res://assets/models/lab_crate_frame_104.glb",
		"position": Vector3(7.9, 0.12, -8.6),
		"yaw": 0.0
	},
	{
		# #53 room 204. Plan F(10.3, -8.9, 11.2, -8.2), center (10.75, -8.55).
		"id": "Lab_Crate_Frame_204",
		"path": "res://assets/models/lab_crate_frame_204.glb",
		"position": Vector3(10.75, 4.2, -8.55),
		"yaw": 0.0
	},
	{
		# #27 beside the 201 chair. Plan center (-13.2, 5.6). Rail hooks reach local y=-0.035,
		# so the pivot is 0.035 above the L2 datum and the hooks sit on it. Head points south at the chair.
		"id": "Task_Lamp_201",
		"path": "res://assets/models/task_lamp_rail_slider.glb",
		"position": Vector3(-13.2, 4.235, 5.6), # [M-65/LAY-22] Rev C L2 floor 4.20 + 0.035 hook offset (was the old 4.415 datum)
		"yaw": 180.0
	},
	{
		# M-43 / #27 room 104. No desk under (5.0, -8.7). Lowest mesh is local y=-0.035,
		# so the pivot is 0.035 above the L1 floor (y=0.12). Yaw 0 points the boom at +Z, into the room.
		"id": "Task_Lamp_104",
		"path": "res://assets/models/task_lamp_rail_slider.glb",
		"position": Vector3(5.0, 0.155, -8.7),
		"yaw": 0.0
	},
	{
		# M-43 / #27 room 204. Same XZ, dropped onto the L2 slab top (y=4.2).
		"id": "Task_Lamp_204",
		"path": "res://assets/models/task_lamp_rail_slider.glb",
		"position": Vector3(5.0, 4.235, -8.7),
		"yaw": 0.0
	},
	{
		# #16 reading chair. Plan F(-13.4, 4.2, -12.4, 5.2), center (-12.9, 4.7). +Z faces the west window.
		"id": "Armchair_Reading_201",
		"path": "res://assets/models/armchair_swivel_pedestal.glb",
		"position": Vector3(-12.9, 4.2, 4.7),
		"yaw": -90.0
	},
	{
		# #34 rail cradles, room 102 plan F(10.3, 6, 11, 6.7), center (10.65, 6.35). Floor-referenced pivot.
		"id": "Potted_Plants_Rail_Cradles_102",
		"path": "res://assets/models/potted_plants_rail_cradles.glb",
		"position": Vector3(10.65, -0.08, 6.35), # [M-72/LAY-24] mesh bottom is +0.20 over the pivot; rests on the L1 floor 0.12
		"yaw": 0.0
	},
	{
		# #34 pocket column, room 203 bin slot center (-9.2, -8.6), against the south wall.
		"id": "Potted_Plants_Pocket_Column_203",
		"path": "res://assets/models/potted_plants_pocket_column.glb",
		"position": Vector3(-9.2, 4.2, -8.6),
		"yaw": 0.0
	},
	{
		# GEO-11 / Rev C.3. Room 101 west wall, inner face x=-13.9. Yaw +90 maps local +Z
		# onto world +X (front) and local -Z onto world -X (back plate on the wall).
		# Centre of plan rect x -13.9..-13.4, z 4.5..7.0. The mesh is 2.7 m along local X,
		# so its world-Z extent around this centre is 4.40..7.10. Height 2.1 m.
		"id": "Wardrobe_101",
		"path": "res://assets/models/wardrobe_openbays_rails.glb",
		"position": Vector3(-13.65, 0.02, 5.75), # [M-66/LAY-23] mesh bottom is +0.10 over the pivot; rests on the L1 floor 0.12
		"scale": Vector3(0.925926, 1.0, 1.0), # Trim to the 2.5 m plan rect (z 4.5..7.0): mesh is 2.7 m along local X. Y untouched, so it stays on the floor.
		"yaw": 90.0
	}
]


func _resolve_anim_clip(ap: AnimationPlayer, clip: String) -> String:
	if clip == "":
		return ""
	if ap.has_animation(clip):
		return clip
	for listed: String in ap.get_animation_list():
		if listed == clip or listed.ends_with("/" + clip):
			return listed
	return ""


func _apply_anim_clip(ap: AnimationPlayer, clip: String, looped: bool) -> String:
	var resolved: String = _resolve_anim_clip(ap, clip)
	if resolved == "":
		return ""
	var anim: Animation = ap.get_animation(resolved)
	if anim != null:
		anim.loop_mode = Animation.LOOP_LINEAR if looped else Animation.LOOP_NONE
	return resolved


# One box from the mesh AABB, in the prop's local frame. Same transform walk placement_assert uses.
func _prop_mesh_aabb(root: Node3D) -> AABB:
	var merged := AABB()
	var any := false
	if root is MeshInstance3D and (root as MeshInstance3D).mesh != null:
		merged = (root as MeshInstance3D).get_aabb()
		any = true
	var stack: Array = []
	for child: Node in root.get_children():
		stack.append([child, Transform3D.IDENTITY])
	while not stack.is_empty():
		var item: Array = stack.pop_back()
		var curr: Node = item[0] as Node
		var parent_xf: Transform3D = item[1] as Transform3D
		var xf: Transform3D = parent_xf
		if curr is Node3D:
			xf = parent_xf * (curr as Node3D).transform
		if curr is MeshInstance3D:
			var mi: MeshInstance3D = curr as MeshInstance3D
			if mi.mesh != null:
				var bb: AABB = xf * mi.get_aabb()
				if any:
					merged = merged.merge(bb)
				else:
					merged = bb
					any = true
		for grandchild: Node in curr.get_children():
			stack.append([grandchild, xf])
	if not any:
		return AABB()
	return merged


func _add_prop_aabb_body(root: Node3D) -> void:
	if root == null or root.get_node_or_null("PropAabbBody") != null:
		return
	var box: AABB = _prop_mesh_aabb(root)
	if box.size.x <= 0.0001 or box.size.y <= 0.0001 or box.size.z <= 0.0001:
		push_warning("[PrefacePlayableArea] No mesh AABB for " + String(root.name))
		return
	var body := StaticBody3D.new()
	body.name = "PropAabbBody"
	var shape_node := CollisionShape3D.new()
	var shape := BoxShape3D.new()
	shape.size = box.size
	shape_node.shape = shape
	shape_node.position = box.get_center()
	body.add_child(shape_node)
	root.add_child(body)


func _spawn_rev_c_static_props() -> void:
	if _props_container == null:
		return
	for spec: Dictionary in REV_C_STATIC_PROP_SPECS:
		var id: String = String(spec["id"])
		if _props_container.get_node_or_null(id) != null:
			continue
		var path: String = String(spec["path"])
		if not FileAccess.file_exists(_resolve_path(path)):
			push_warning("[PrefacePlayableArea] Static prop GLB missing: " + path)
			continue
		var node: Node3D = _load_glb_scene(path, 0.85)
		if node == null:
			push_warning("[PrefacePlayableArea] Static prop failed to load: " + path)
			continue
		node.name = id
		node.position = spec["position"] as Vector3
		node.rotation_degrees = Vector3(0.0, float(spec["yaw"]), 0.0)
		# Optional per-spec scale (local axes). Default 1.
		node.scale = spec.get("scale", Vector3.ONE) as Vector3
		_props_container.add_child(node)
		_add_prop_aabb_body(node)
	_spawn_apt201_bench_outline()


func _spawn_animated_props() -> void:
	if _props_container == null:
		return
	for spec: Dictionary in ANIMATED_PROP_SPECS:
		var id: String = String(spec["id"])
		if _props_container.get_node_or_null(id) != null:
			continue
		var path: String = String(spec["path"])
		if not FileAccess.file_exists(_resolve_path(path)):
			push_warning("[PrefacePlayableArea] Animated prop GLB missing: " + path)
			continue
		var node: Node3D = _load_glb_scene(path, 0.85)
		if node == null:
			push_warning("[PrefacePlayableArea] Animated prop failed to load: " + path)
			continue
		node.name = id
		node.position = spec["position"] as Vector3
		node.rotation_degrees = Vector3(0.0, float(spec["yaw"]), 0.0)
		_props_container.add_child(node)
		_add_prop_aabb_body(node)
		_interactables.append({
			"node": node,
			"id": id,
			"kind": "anim_prop",
			"label": String(spec["label"]),
			"collected": false,
			"pickup": false,
			"spec": spec,
			"toggle_i": 0
		})
		var idle_clip: String = String(spec.get("idle", ""))
		if idle_clip == "":
			continue
		var ap_idle: AnimationPlayer = _find_anim_player(node)
		if ap_idle == null:
			push_warning("[PrefacePlayableArea] No AnimationPlayer on " + id)
			continue
		var idle_name: String = _apply_anim_clip(ap_idle, idle_clip, true)
		if idle_name == "":
			push_warning("[PrefacePlayableArea] Missing idle clip %s on %s" % [idle_clip, id])
		else:
			ap_idle.play(idle_name)


func _populate_pickups_and_wrist_rig() -> void:
	for ch: Node in _props_container.get_children():
		ch.free()
	_interactables.clear()
	for k: String in _inventory_max.keys():
		_inventory_max[k] = 0

	_spawn_interior_pickups(true)
	_spawn_animated_props()
	_spawn_rev_c_static_props()

	# [t38u]/[t39u] Functional RFID doors across all 6 Residential Sector portals
	_build_rfid_forcefield_doors(_props_container)

	# #04 Bio-Luminescent Neural Tendon Smart-Sleeve (lower-left of 1st-person view)
	if _camera != null:
		if _fp_wrist_holder != null and is_instance_valid(_fp_wrist_holder):
			_fp_wrist_holder.free()
		_fp_wrist_holder = Node3D.new()
		_fp_wrist_holder.name = "CenterScreenWrist04Holder"
		_camera.add_child(_fp_wrist_holder)
		_fp_wrist_model = _load_glb_scene(_find_first_existing(WRIST_04_PATHS), 0.75)
		if _fp_wrist_model != null:
			_fp_wrist_model.name = "Wrist04_NeuralTendonSleeve"
			_set_tree_cast_shadow(_fp_wrist_model, GeometryInstance3D.SHADOW_CASTING_SETTING_OFF)
			_fp_wrist_holder.add_child(_fp_wrist_model)
			# Holder origin == wrist pivot so lowered/raised poses are authored at the wrist.
			_fp_wrist_model.position = -WRIST_PIVOT_IN_MODEL
			_fp_wrist_holder.position = ARM_RAISED_POS
			_fp_wrist_holder.rotation_degrees = ARM_RAISED_ROT_DEG
			_build_first_person_wrist_pulse_rings()


func _strip_surfaces_by_mat_substr(mi: MeshInstance3D, drop_substrs: Array[String]) -> void:
	if mi == null or mi.mesh == null:
		return
	var src: ArrayMesh = mi.mesh as ArrayMesh
	if src == null:
		return
	var dst: ArrayMesh = ArrayMesh.new()
	var mats: Array[Material] = []
	for si: int in range(src.get_surface_count()):
		var mat: Material = mi.get_active_material(si)
		var m_src: Material = src.surface_get_material(si)
		var nm: String = ((mat.resource_name if mat != null else "") + " " + (m_src.resource_name if m_src != null else "")).to_lower()
		var drop: bool = false
		for sub: String in drop_substrs:
			if nm.contains(sub):
				drop = true
				break
		if not drop:
			dst.add_surface_from_arrays(src.surface_get_primitive_type(si), src.surface_get_arrays(si))
			mats.append(mat)
	mi.mesh = dst
	for si2: int in range(mats.size()):
		mi.set_surface_override_material(si2, mats[si2])


func _build_first_person_wrist_pulse_rings() -> void:
	# [t31u] Clean up the static wrist GLB at load time so zero holographic rings or stand pedestals
	# are visible unless [F] is actively pulsing:
	#  - Holo_Projection_Rings: clear baked 3-torus mesh (replaced by dynamic PulseRings below).
	#  - Cuff_Aperture_Assembly: hide the 3 baked cyan/UV torus rings & translucent holo sleeve shell;
	#    keep the machined steel cuff pins, Spool_SuperWire_Cuff, Forearm_Base sleeve, and Wrist_Joint hand.
	#  - Forearm_Base: strip the octagonal display-stand pedestal base (gunmetal + UV ring) so only the
	#    anatomical forearm sleeve remains.
	if _fp_wrist_model == null:
		return
	var anchor: Node3D = _fp_wrist_model
	var ring_pos: Vector3 = Vector3(0.0, 0.235, 0.135)
	var st: Array[Node] = [_fp_wrist_model]
	while not st.is_empty():
		var c: Node = st.pop_back()
		if c is MeshInstance3D and (c as MeshInstance3D).mesh != null:
			var mi: MeshInstance3D = c as MeshInstance3D
			var mname: String = (String(mi.name) + " " + String(mi.mesh.resource_name)).to_lower()
			if mname.contains("holo_projection_rings"):
				mi.mesh = null
				anchor = mi
				ring_pos = Vector3.ZERO
			elif mname.contains("cuff_aperture_assembly"):
				_strip_surfaces_by_mat_substr(mi, ["emissive", "holo"])
			elif mname.contains("forearm_base"):
				_strip_surfaces_by_mat_substr(mi, ["gunmetal", "emissive"])
			elif mname.contains("spool_superwire"):
				_strip_surfaces_by_mat_substr(mi, ["emissive", "copper"])
		for ch: Node in c.get_children():
			st.append(ch)
	_pulse_rings.clear()
	_pulse_rings_root = Node3D.new()
	_pulse_rings_root.name = "PulseRings"
	_pulse_rings_root.position = ring_pos
	_pulse_rings_root.rotation_degrees = Vector3(65.0, 0.0, 0.0)
	_pulse_rings_root.visible = false
	anchor.add_child(_pulse_rings_root)
	var cfgs: Array = [[0.036, 0.0, COLOR_CYAN], [0.052, 0.016, Color("#7B5CFF")], [0.066, 0.032, COLOR_CYAN]]
	for i: int in range(cfgs.size()):
		var c: Array = cfgs[i]
		var r: float = float(c[0])
		var ring: MeshInstance3D = MeshInstance3D.new()
		ring.name = "RFID_PulseRing_%02d" % (i + 1)
		var tm: TorusMesh = TorusMesh.new()
		tm.inner_radius = r - 0.0035
		tm.outer_radius = r + 0.0035
		tm.rings = 40
		tm.ring_segments = 8
		ring.mesh = tm
		ring.position = Vector3(0.0, float(c[1]), 0.0)
		var col: Color = c[2] as Color
		var m: StandardMaterial3D = StandardMaterial3D.new()
		m.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
		m.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
		m.blend_mode = BaseMaterial3D.BLEND_MODE_ADD
		m.cull_mode = BaseMaterial3D.CULL_DISABLED
		m.albedo_color = Color(col.r, col.g, col.b, 0.0)
		ring.material_override = m
		ring.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
		_pulse_rings_root.add_child(ring)
		_pulse_rings.append(ring)

	# [HW-03] Connected tactical forearm sleeve extension behind the wrist cuff so looking down never shows a floating glove
	if _fp_wrist_model.get_node_or_null("ForearmSleeveExtension") == null:
		var sleeve_mi: MeshInstance3D = MeshInstance3D.new()
		sleeve_mi.name = "ForearmSleeveExtension"
		var scm: CylinderMesh = CylinderMesh.new()
		scm.top_radius = 0.046
		scm.bottom_radius = 0.058
		scm.height = 0.34
		scm.radial_segments = 16
		sleeve_mi.mesh = scm
		sleeve_mi.position = Vector3(0.0, 0.175, 0.25)
		sleeve_mi.rotation_degrees = Vector3(84.0, 0.0, 0.0)
		var sl_mat: StandardMaterial3D = StandardMaterial3D.new()
		sl_mat.albedo_color = Color(0.14, 0.17, 0.21, 1.0)
		sl_mat.roughness = 0.62
		sl_mat.metallic = 0.25
		sleeve_mi.material_override = sl_mat
		sleeve_mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
		_fp_wrist_model.add_child(sleeve_mi)


func _update_pulse_rings() -> void:
	if _pulse_rings_root == null:
		return
	var active: bool = _rfid_pulse_timer > 0.0
	_pulse_rings_root.visible = active
	if not active:
		return
	var elapsed: float = RFID_PULSE_DURATION - _rfid_pulse_timer
	var env: float = clampf(minf(elapsed / 0.15, _rfid_pulse_timer / 0.35), 0.0, 1.0)
	for i: int in range(_pulse_rings.size()):
		var ring: MeshInstance3D = _pulse_rings[i]
		var ph: float = fmod(elapsed * 1.6 + float(i) / 3.0, 1.0)
		var sc: float = 0.75 + ph * 0.9
		ring.scale = Vector3(sc, 1.0, sc)
		var m: StandardMaterial3D = ring.material_override as StandardMaterial3D
		m.albedo_color.a = 0.9 * (1.0 - ph) * env


func _update_first_person_arm(delta: float) -> void:
	if _fp_wrist_holder == null or _player_body == null or _camera == null:
		return
	if _rfid_pulse_timer > 0.0:
		_rfid_pulse_timer = maxf(_rfid_pulse_timer - delta, 0.0)
	if _interact_reach_timer > 0.0:
		_interact_reach_timer = maxf(_interact_reach_timer - delta, 0.0)
	var f_held: bool = _preset_active < 0 and not _capture_hud and Input.is_action_pressed("rfid_pulse")
	var target_raise: float = 1.0 if (f_held or _rfid_pulse_timer > 0.0 or _interact_reach_timer > 0.0) else 0.0
	_arm_raise_blend = move_toward(_arm_raise_blend, target_raise, delta * ARM_RAISE_SPEED)

	# Sinusoidal walk swing (State B) driven by real horizontal ground speed.
	var hv: Vector3 = _player_body.velocity
	hv -= _player_body.up_direction * hv.dot(_player_body.up_direction)
	var hs: float = hv.length()
	var moving: bool = hs > 0.15 and _player_body.is_on_floor()
	var sprint_ratio: float = clampf((hs - WALK_SPEED) / (SPRINT_SPEED - WALK_SPEED), 0.0, 1.0)
	var target_amp: float = clampf(hs / WALK_SPEED, 0.0, 1.0) if moving else 0.0
	if moving:
		_walk_phase = fmod(_walk_phase + delta * lerpf(5.8, 8.6, sprint_ratio), TAU)
	_walk_swing_amp = move_toward(_walk_swing_amp, target_amp, delta * 6.0)
	var smooth_blend: float = smoothstep(0.0, 1.0, _arm_raise_blend)
	var swing_s: float = sin(_walk_phase) * _walk_swing_amp

	# State A: lowered at the left side in _player_body (torso/yaw) space — never pitches with the camera.
	var low_pos: Vector3 = ARM_LOWERED_POS + Vector3(0.0, absf(swing_s) * WALK_SWING_LIFT, -swing_s * WALK_SWING_Z)
	var low_rot: Vector3 = ARM_LOWERED_ROT_DEG + Vector3(swing_s * WALK_SWING_PITCH_DEG, 0.0, 0.0)
	var lowered_xf: Transform3D = _player_body.global_transform * Transform3D(Basis.from_euler(low_rot * (PI / 180.0)), low_pos)
	# State C: raised into the camera viewing pose.
	var raised_xf: Transform3D = _camera.global_transform * Transform3D(Basis.from_euler(ARM_RAISED_ROT_DEG * (PI / 180.0)), ARM_RAISED_POS)
	_fp_wrist_holder.global_transform = lowered_xf.interpolate_with(raised_xf, smooth_blend)
	_update_pulse_rings()


func _hand_body_local() -> Transform3D:
	return _player_body.global_transform.affine_inverse() * _fp_wrist_holder.global_transform


func _wrist_world_points() -> PackedVector3Array:
	var pts: PackedVector3Array = PackedVector3Array()
	if _fp_wrist_model == null:
		return pts
	var st: Array[Node] = [_fp_wrist_model]
	while not st.is_empty():
		var c: Node = st.pop_back()
		if c is MeshInstance3D and (c as MeshInstance3D).mesh != null and not String(c.name).begins_with("RFID_PulseRing") and String(c.name) != "ForearmSleeveExtension":
			var mi: MeshInstance3D = c as MeshInstance3D
			var bb: AABB = mi.get_aabb()
			for k: int in range(8):
				pts.append(mi.global_transform * bb.get_endpoint(k))
			pts.append(mi.global_transform * bb.get_center())
		for ch: Node in c.get_children():
			st.append(ch)
	return pts


func _hand_points_in_view() -> int:
	var n: int = 0
	for p: Vector3 in _wrist_world_points():
		if _camera.is_position_in_frustum(p) and not _camera.is_position_behind(p):
			n += 1
	return n


# ------------------------------------------------------------------------------
# Animations (BUG-04)
# ------------------------------------------------------------------------------
func _find_anim_player(actor: Node) -> AnimationPlayer:
	var stack: Array[Node] = [actor]
	while not stack.is_empty():
		var curr: Node = stack.pop_back()
		if curr is AnimationPlayer:
			return curr as AnimationPlayer
		for ch: Node in curr.get_children():
			stack.append(ch)
	return null


func _play_actor_anim(actor: Node3D, preferred_names: Array, seek_t: float) -> void:
	if actor == null:
		return
	var ap: AnimationPlayer = _find_anim_player(actor)
	if ap == null:
		return
	var alist: PackedStringArray = ap.get_animation_list()
	var chosen: String = ""
	for pname in preferred_names:
		if alist.has(String(pname)):
			chosen = String(pname)
			break
	if chosen == "":
		for a: String in alist:
			if a != "RESET":
				chosen = a
				break
	if chosen == "":
		return
	var frozen: bool = _batch_render or _validate_only
	if not frozen:
		var anim: Animation = ap.get_animation(chosen)
		if anim != null:
			anim.loop_mode = Animation.LOOP_LINEAR
	ap.play(chosen)
	var anim_len: float = ap.get_animation(chosen).length if ap.get_animation(chosen) != null else 0.0
	if anim_len > 0.0:
		ap.seek(fmod(seek_t, anim_len), true)
	if frozen:
		ap.advance(0.0)
		ap.speed_scale = 0.0
	else:
		ap.speed_scale = 1.0


# ------------------------------------------------------------------------------
# #05 Hammerhead bots, residents, Rostov (BUG-05)
# ------------------------------------------------------------------------------
func _spawn_bot(paths: Array, nm: String, label: String, dept: String, status: String, pos: Vector3, yaw: float, anims: Array, t: float) -> void:
	var bot: Node3D = _load_glb_scene(_find_first_existing(paths), 0.85)
	if bot == null:
		return
	bot.name = nm
	bot.position = pos
	bot.rotation_degrees = Vector3(0.0, yaw, 0.0)
	bot.scale = Vector3(1.18, 1.18, 1.18)
	_actors_container.add_child(bot)
	_play_actor_anim(bot, anims, t)
	_interactables.append({"node": bot, "kind": "bot", "label": label, "dept": dept, "status": status, "collected": false, "pickup": false})


func _populate_johnny5_bots_and_citizens() -> void:
	for ch: Node in _actors_container.get_children():
		ch.free()

	# Each #05 Hammerhead stationed at its functional post.
	_spawn_bot(BOT_SPROCKET_PATHS, "Hammerhead05_Sprocket_0419_Engineering", "SPROCKET #0419", "D-01 // ENGINEERING",
		"Sector-4 service junction relay nominal. Exit bulkhead counterweight synced.", Vector3(-1.45, 0.06, -6.45), 35.0, ["DiagnosticPoint", "Idle"], 0.70)
	_spawn_bot(BOT_SWEEP_PATHS, "Hammerhead05_Sweep_0812_CivicSanitation", "SWEEP #0812", "D-02 // CIVIC & SANITATION",
		"Mezzanine sanitation patrol 72% complete. Particulate index: low.", Vector3(-2.40, 4.29, 2.60), -65.0, ["WalkCycle", "Idle"], 0.35)
	_spawn_bot(BOT_KELVIN_PATHS, "Hammerhead05_Kelvin_0204_Science", "KELVIN #0204", "D-03 // SCIENCE",
		"Room 1B substation diagnostic rack: thermal drift +0.4K. Recommend thermal jelly.", Vector3(5.60, 0.06, 6.00), 45.0, ["DiagnosticProbe", "DiagnosticPoint", "Idle"], 0.65)
	_spawn_bot(BOT_CLOVER_PATHS, "Hammerhead05_Clover_0631_AgriBiosphere", "CLOVER #0631", "D-04 // AGRI-BIOSPHERE",
		"Atrium planter soil moisture 41%. Aeroponic herbs thriving.", Vector3(2.20, 0.06, -1.80), 90.0, ["Idle", "DiagnosticPoint"], 0.50)

	var comm_path: String = _find_first_existing(COMMUTER_PATHS)
	for c_cfg: Dictionary in [
		{"name": "Resident_UpperGallery_01", "pos": Vector3(2.80, 4.29, 2.65), "rot_y": -80.0, "anim": "WalkCycle", "t": 0.25},
		{"name": "Resident_StairLanding_02", "pos": Vector3(10.65, 2.21, -4.85), "rot_y": 180.0, "anim": "WalkCycle", "t": 0.55},
		{"name": "Resident_Lounge1A_03", "pos": Vector3(-4.20, 0.12, 2.20), "rot_y": 145.0, "anim": "WristRaiseDemo", "t": 1.10},
		{"name": "Resident_ConcourseExit_04", "pos": Vector3(0.55, 0.12, -6.85), "rot_y": 175.0, "anim": "WalkCycle", "t": 0.15},
		{"name": "Resident_ConcoursePromenade_05", "pos": Vector3(-0.75, 0.12, -4.45), "rot_y": 170.0, "anim": "WalkCycle", "t": 0.75}
	]:
		var cnode: Node3D = _load_glb_scene(comm_path, 0.55)
		if cnode != null:
			cnode.name = String(c_cfg["name"])
			cnode.position = c_cfg["pos"] as Vector3
			cnode.rotation_degrees = Vector3(0.0, float(c_cfg["rot_y"]), 0.0)
			_actors_container.add_child(cnode)
			_play_actor_anim(cnode, [String(c_cfg["anim"])], float(c_cfg["t"]))

	_rostov_root = _load_glb_scene(_find_first_existing(ROSTOV_PATHS), 0.6)
	if _rostov_root != null:
		_rostov_root.name = "PlayerTech_KaelenRostov"
		_rostov_root.position = Vector3(-1.25, 0.06, -3.15)
		_rostov_root.rotation_degrees = Vector3(0.0, 175.0, 0.0)
		_actors_container.add_child(_rostov_root)
		_play_actor_anim(_rostov_root, ["WalkCycle"], 0.15)


# ------------------------------------------------------------------------------
# Lighting ([t3u] grounded & purposeful) + N toggle
# ------------------------------------------------------------------------------
func _build_ceiling_luminaire(nm: String, pos: Vector3, col: Color, panel_sz: Vector2) -> void:
	var holder: Node3D = Node3D.new()
	holder.name = nm + "_Fixture"
	holder.position = pos + Vector3(0.0, 0.22, 0.0)
	_lights_container.add_child(holder)

	var bezel: MeshInstance3D = MeshInstance3D.new()
	bezel.name = "LuminaireBezel"
	var bmesh: BoxMesh = BoxMesh.new()
	bmesh.size = Vector3(panel_sz.x + 0.12, 0.05, panel_sz.y + 0.12)
	bezel.mesh = bmesh
	bezel.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	var bmat: StandardMaterial3D = StandardMaterial3D.new()
	bmat.albedo_color = Color(0.24, 0.27, 0.31, 1.0)
	bmat.metallic = 0.82
	bmat.roughness = 0.28
	bezel.material_override = bmat
	holder.add_child(bezel)

	var diff: MeshInstance3D = MeshInstance3D.new()
	diff.name = "LuminaireDiffuser"
	var dmesh: BoxMesh = BoxMesh.new()
	dmesh.size = Vector3(panel_sz.x, 0.025, panel_sz.y)
	diff.mesh = dmesh
	diff.position = Vector3(0.0, -0.025, 0.0)
	diff.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	var dmat: StandardMaterial3D = StandardMaterial3D.new()
	dmat.albedo_color = col
	dmat.roughness = 0.18
	dmat.emission_enabled = true
	dmat.emission = col
	dmat.emission_energy_multiplier = 0.85
	diff.material_override = dmat
	holder.add_child(diff)


func _setup_sector_lighting() -> void:
	for ch: Node in _lights_container.get_children():
		ch.free()
	_task_lights.clear()
	_task_base.clear()
	_spot_lights.clear()
	_spot_base.clear()

	# Directional sun. 2-split shadows, 60 m, so the opaque drum hull occludes everything outside the window.
	_sun = DirectionalLight3D.new()
	_sun.name = "AtriumGoldenHourSunlight"
	_sun.rotation_degrees = Vector3(-72.0, -162.0, 0.0)
	# [CYL-02] Snapshot after the authored rotation. _process spins this about +X with the starfield.
	_sun_base_basis = _sun.basis
	# Unfiltered space sun. Energy is 1.4 at full exposure, then scaled by elevation in _process.
	_sun.light_color = Color("#FFF6EA")
	_sun.light_energy = 1.4
	_sun.shadow_enabled = true
	_sun.directional_shadow_mode = DirectionalLight3D.SHADOW_PARALLEL_2_SPLITS
	_sun.directional_shadow_max_distance = 60.0
	_sun.shadow_bias = 0.03
	_sun.shadow_normal_bias = 1.5
	_sun.shadow_blur = 1.0
	_sun.light_angular_distance = 0.5
	_lights_container.add_child(_sun)

	_fill = DirectionalLight3D.new()
	_fill.name = "AtriumSkyBounceFill"
	_fill.rotation_degrees = Vector3(-42.0, -145.0, 0.0)
	_fill.light_color = Color("#C8DCF0")
	_fill.light_energy = 0.28
	_fill.shadow_enabled = false
	_lights_container.add_child(_fill)

	# Box-projected ReflectionProbe covering the 28m x 18m x 9m residential atrium for grounded metallic & glass reflections.
	# [M-19] Godot 4.7 gl_compatibility supports ReflectionProbe, at most 2 overlapping any mesh. This is the only one.
	var renderer: String = RenderingServer.get_current_rendering_method()
	if renderer == "gl_compatibility" or renderer == "forward_plus" or renderer == "mobile":
		var rprobe: ReflectionProbe = ReflectionProbe.new()
		rprobe.name = "AtriumBoxReflectionProbe"
		rprobe.position = Vector3(0.0, 4.4, 0.0)
		rprobe.size = Vector3(30.0, 10.0, 20.0)
		rprobe.box_projection = true
		rprobe.interior = true
		rprobe.intensity = 0.3
		rprobe.ambient_mode = ReflectionProbe.AMBIENT_ENVIRONMENT
		rprobe.update_mode = ReflectionProbe.UPDATE_ALWAYS
		_lights_container.add_child(rprobe)
		_reflection_probe = rprobe
		_probe_rebake_frames = 2
	else:
		push_warning("[M-19] ReflectionProbe skipped; renderer has no probe support: " + renderer)

	# Physical ceiling luminaires + clean room lighting (OmniLight3D shadow_enabled = false so rooms never have 2 competing sets of shadows
	# or cast L2 character shadows down through floor slabs onto L1).
	for l_cfg: Dictionary in [
		# [REV-C2] Ceiling light for the #27 reading lamp. Not Apt201_Workbench_TaskLight; that objective is gone.
		{"name": "Apt201_TaskLamp27", "pos": Vector3(-13.2, 6.4, 5.6), "col": Color("#F5E2C4"), "e": 0.70, "r": 6.0, "sh": false, "sz": Vector2(0.4, 0.4)},
		{"name": "Apt202_Desk_TaskLight", "pos": Vector3(9.80, 7.55, 6.20), "col": Color("#F5E2C4"), "e": 0.85, "r": 9.5, "sh": false, "sz": Vector2(1.40, 0.36)},
		{"name": "Stairwell_Landing_SafetyLight", "pos": Vector3(10.40, 7.80, -1.60), "col": Color("#EDE0C8"), "e": 0.85, "r": 11.0, "sh": false, "sz": Vector2(1.20, 0.32)},
		{"name": "Room1A_Lounge_Light", "pos": Vector3(-8.20, 3.62, 5.80), "col": Color("#F5E2C4"), "e": 0.84, "r": 9.5, "sh": false, "sz": Vector2(1.40, 0.36)},
		{"name": "Room1B_Substation_ServiceBayLight", "pos": Vector3(4.80, 3.62, 5.80), "col": Color("#EAE6DC"), "e": 0.90, "r": 10.8, "sh": false, "sz": Vector2(1.50, 0.38)},
		{"name": "Atrium_Midhead_BounceFill", "pos": Vector3(0.0, 7.85, -2.20), "col": Color("#EBF0F5"), "e": 0.74, "r": 16.0, "sh": false, "sz": Vector2(2.20, 0.45)}
	]:
		var lpos: Vector3 = l_cfg["pos"] as Vector3
		var lcol: Color = l_cfg["col"] as Color
		_build_ceiling_luminaire(String(l_cfg["name"]), lpos, lcol, l_cfg["sz"] as Vector2)
		var omni: OmniLight3D = OmniLight3D.new()
		omni.name = String(l_cfg["name"])
		omni.position = lpos
		omni.light_color = lcol
		omni.light_energy = float(l_cfg["e"])
		omni.omni_range = float(l_cfg["r"])
		omni.omni_attenuation = 1.2
		if bool(l_cfg["sh"]):
			omni.shadow_enabled = true
			omni.shadow_bias = 0.05
			omni.shadow_normal_bias = 1.5
			omni.shadow_blur = 1.5
		else:
			omni.shadow_enabled = false
		_lights_container.add_child(omni)
		_task_lights.append(omni)
		_task_base.append({"col": lcol, "e": l_cfg["e"]})

	# Single downward ceiling SpotLight3D for enclosed rooms (APT 201 & Room 1B) with floor-clamped range (3.55m)
	# so interior props cast exactly 1 clean downward shadow and never reach any lower deck.
	for s_cfg: Dictionary in [
		{"name": "Apt201_CeilingDownSpot", "pos": Vector3(-8.45, 7.55, 6.40), "col": Color("#F5E2C4"), "e": 0.42, "r": 3.50, "ang": 62.0},
		{"name": "Room1B_CeilingDownSpot", "pos": Vector3(4.80, 3.62, 5.80), "col": Color("#EAE6DC"), "e": 0.42, "r": 3.60, "ang": 64.0}
	]:
		var sp: SpotLight3D = SpotLight3D.new()
		sp.name = String(s_cfg["name"])
		sp.position = s_cfg["pos"] as Vector3
		sp.rotation_degrees = Vector3(-90.0, 0.0, 0.0)
		sp.light_color = s_cfg["col"] as Color
		sp.light_energy = float(s_cfg["e"])
		sp.spot_range = float(s_cfg["r"])
		sp.spot_angle = float(s_cfg["ang"])
		sp.spot_angle_attenuation = 0.85
		sp.shadow_enabled = true
		sp.shadow_bias = 0.02
		sp.shadow_normal_bias = 1.0
		sp.shadow_blur = 1.4
		_lights_container.add_child(sp)
		_spot_lights.append(sp)
		_spot_base.append({"col": s_cfg["col"], "e": s_cfg["e"]})

	_register_m15_emissives(self)
	_cache_authored_lighting()
	_apply_daylight_sun_fill()


func _cache_authored_lighting() -> void:
	_sun_energy_authored = 1.4
	_fill_energy_authored = 0.28
	if _world_env != null and _world_env.environment != null:
		_ambient_energy_authored = _world_env.environment.ambient_light_energy
		_ambient_color_authored = _world_env.environment.ambient_light_color


func _sun_elevation_deg() -> float:
	if _sun == null:
		return 90.0
	# Light rays travel along -Z. The sun sits along +Z. Deck up is world +Y.
	var toward_sun: Vector3 = _sun.global_transform.basis.z
	return rad_to_deg(asin(clampf(toward_sun.normalized().dot(Vector3.UP), -1.0, 1.0)))


func _sun_energy_factor() -> float:
	return clampf((_sun_elevation_deg() + 5.0) / 15.0, 0.0, 1.0)


func _nominal_sun_energy() -> float:
	return _sun_energy_authored * _sun_energy_factor()


func _nominal_fill_energy() -> float:
	var factor: float = _sun_energy_factor()
	return _fill_energy_authored * (0.5 + 0.5 * factor)


func _apply_daylight_sun_fill() -> void:
	if _sun != null:
		_sun.light_energy = _nominal_sun_energy()
	if _fill != null:
		_fill.light_energy = _nominal_fill_energy()


func _apply_ambient(col: Color, energy: float) -> void:
	if _world_env == null or _world_env.environment == null:
		return
	_world_env.environment.ambient_light_color = col
	_world_env.environment.ambient_light_energy = energy


func _apply_flicker_scale(scale: float) -> void:
	if _sun != null:
		_sun.light_energy = _nominal_sun_energy() * scale
	if _fill != null:
		_fill.light_energy = _nominal_fill_energy() * scale
	_apply_ambient(_ambient_color_authored, _ambient_energy_authored * scale)
	for i: int in range(_task_lights.size()):
		var l: OmniLight3D = _task_lights[i]
		l.light_color = _task_base[i]["col"] as Color
		l.light_energy = float(_task_base[i]["e"]) * scale
	for i: int in range(_spot_lights.size()):
		var s: SpotLight3D = _spot_lights[i]
		s.light_color = _spot_base[i]["col"] as Color
		s.light_energy = float(_spot_base[i]["e"]) * scale
	for rec: Dictionary in _emissive_mats:
		var mat: BaseMaterial3D = rec["mat"] as BaseMaterial3D
		if mat != null:
			mat.emission_energy_multiplier = float(rec["energy"]) * scale


func _apply_emergency_blend(t: float) -> void:
	var u: float = clampf(t, 0.0, 1.0)
	var emerg_amb: Color = Color("#3A1A16")
	var emerg_task: Color = Color("#C2402A")
	if _sun != null:
		_sun.light_energy = lerpf(_nominal_sun_energy() * 0.8, 0.05, u)
	if _fill != null:
		_fill.light_energy = lerpf(_nominal_fill_energy() * 0.8, 0.03, u)
	_apply_ambient(_ambient_color_authored.lerp(emerg_amb, u), lerpf(_ambient_energy_authored * 0.8, 0.10, u))
	for i: int in range(_task_lights.size()):
		var l: OmniLight3D = _task_lights[i]
		var base_c: Color = _task_base[i]["col"] as Color
		var base_e: float = float(_task_base[i]["e"])
		l.light_color = base_c.lerp(emerg_task, u)
		l.light_energy = lerpf(base_e * 0.8, base_e * 0.25, u)
	for i: int in range(_spot_lights.size()):
		var sp: SpotLight3D = _spot_lights[i]
		var base_e2: float = float(_spot_base[i]["e"])
		sp.light_energy = lerpf(base_e2 * 0.8, base_e2 * 0.15, u)
	for rec2: Dictionary in _emissive_mats:
		var mat2: BaseMaterial3D = rec2["mat"] as BaseMaterial3D
		if mat2 == null:
			continue
		var base_em: float = float(rec2["energy"])
		mat2.emission_energy_multiplier = lerpf(base_em * 0.8, float(rec2["emergency"]), u)


func _snapshot_restore_sources() -> void:
	_restore_sun = _sun.light_energy if _sun != null else 0.05
	_restore_fill = _fill.light_energy if _fill != null else 0.03
	_restore_amb_color = _ambient_color_authored
	_restore_amb_energy = _ambient_energy_authored
	if _world_env != null and _world_env.environment != null:
		_restore_amb_color = _world_env.environment.ambient_light_color
		_restore_amb_energy = _world_env.environment.ambient_light_energy
	_restore_task.clear()
	for i: int in range(_task_lights.size()):
		var l: OmniLight3D = _task_lights[i]
		_restore_task.append({"col": l.light_color, "e": l.light_energy})
	_restore_spot_energy.clear()
	for sp: SpotLight3D in _spot_lights:
		_restore_spot_energy.append(sp.light_energy)
	_restore_emissive_energy.clear()
	for rec: Dictionary in _emissive_mats:
		var mat: BaseMaterial3D = rec["mat"] as BaseMaterial3D
		var e: float = float(rec["energy"])
		if mat != null:
			e = mat.emission_energy_multiplier
		_restore_emissive_energy.append(e)


func _apply_restore_global(t: float) -> void:
	var u: float = clampf(t, 0.0, 1.0)
	if _sun != null:
		_sun.light_energy = lerpf(_restore_sun, _nominal_sun_energy(), u)
	if _fill != null:
		_fill.light_energy = lerpf(_restore_fill, _nominal_fill_energy(), u)
	_apply_ambient(_restore_amb_color.lerp(_ambient_color_authored, u), lerpf(_restore_amb_energy, _ambient_energy_authored, u))


func _apply_restore_task(t: float, i: int) -> void:
	if i < 0 or i >= _task_lights.size() or i >= _restore_task.size():
		return
	var u: float = clampf(t, 0.0, 1.0)
	var l: OmniLight3D = _task_lights[i]
	var from_c: Color = _restore_task[i]["col"] as Color
	var from_e: float = float(_restore_task[i]["e"])
	var base_c: Color = _task_base[i]["col"] as Color
	var base_e: float = float(_task_base[i]["e"])
	l.light_color = from_c.lerp(base_c, u)
	l.light_energy = lerpf(from_e, base_e, u)


func _apply_restore_spot(t: float, i: int) -> void:
	if i < 0 or i >= _spot_lights.size() or i >= _restore_spot_energy.size():
		return
	var base_e: float = float(_spot_base[i]["e"])
	_spot_lights[i].light_energy = lerpf(_restore_spot_energy[i], base_e, clampf(t, 0.0, 1.0))


func _apply_restore_emissive(t: float, i: int) -> void:
	if i < 0 or i >= _emissive_mats.size() or i >= _restore_emissive_energy.size():
		return
	var mat: BaseMaterial3D = _emissive_mats[i]["mat"] as BaseMaterial3D
	if mat == null:
		return
	var base_e: float = float(_emissive_mats[i]["energy"])
	mat.emission_energy_multiplier = lerpf(_restore_emissive_energy[i], base_e, clampf(t, 0.0, 1.0))


func _on_light_tween_done(serial: int) -> void:
	if serial == _light_tween_serial:
		_lighting_tween_active = false


func _start_light_tween() -> Tween:
	_light_tween_serial += 1
	var serial: int = _light_tween_serial
	if _light_tween != null and is_instance_valid(_light_tween):
		_light_tween.kill()
	var tw: Tween = create_tween()
	_light_tween = tw
	_lighting_tween_active = true
	tw.finished.connect(_on_light_tween_done.bind(serial))
	return tw


func _register_m15_emissives(root: Node) -> void:
	_emissive_mats.clear()
	if root == null:
		return
	var seen: Dictionary = {}
	var stack: Array[Node] = [root]
	while not stack.is_empty():
		var c: Node = stack.pop_back()
		if c is MeshInstance3D:
			var mi: MeshInstance3D = c as MeshInstance3D
			if mi.mesh != null:
				for s_idx: int in range(mi.mesh.get_surface_count()):
					var mat: Material = mi.get_active_material(s_idx)
					if mat is BaseMaterial3D:
						var bm: BaseMaterial3D = mat as BaseMaterial3D
						if not bm.emission_enabled:
							continue
						var blob: String = (String(mi.name) + " " + bm.resource_name).to_lower()
						if _m15_emission_energy(blob, bm.emission_energy_multiplier) < 0.0:
							continue
						var id: int = bm.get_instance_id()
						if seen.has(id):
							continue
						seen[id] = true
						var emerg: float = bm.emission_energy_multiplier * 0.10
						if blob.replace("_", "").contains("emergency"):
							emerg = 2.5
						_emissive_mats.append({"mat": bm, "energy": bm.emission_energy_multiplier, "emergency": emerg})
		for ch: Node in c.get_children():
			stack.append(ch)


func _retrigger_reflection_probe() -> void:
	if _reflection_probe == null or not is_instance_valid(_reflection_probe):
		return
	_reflection_probe.interior = true
	_reflection_probe.intensity = 0.3
	_reflection_probe.update_mode = ReflectionProbe.UPDATE_ALWAYS
	_probe_rebake_frames = 2


func _set_emergency_lighting(on: bool) -> void:
	_emergency = on
	var tw: Tween = _start_light_tween()
	if on:
		# 3 brownouts in 0.3 s (×0.4 → ×1 → ×0.2 → ×0.8), then 1.2 s expo ease-out to emergency.
		_apply_flicker_scale(0.4)
		tw.tween_interval(0.075)
		tw.tween_callback(_apply_flicker_scale.bind(1.0))
		tw.tween_interval(0.075)
		tw.tween_callback(_apply_flicker_scale.bind(0.2))
		tw.tween_interval(0.075)
		tw.tween_callback(_apply_flicker_scale.bind(0.8))
		tw.tween_interval(0.075)
		tw.tween_method(_apply_emergency_blend, 0.0, 1.0, 1.2).set_trans(Tween.TRANS_EXPO).set_ease(Tween.EASE_OUT)
	else:
		# 2.5 s sine from the live values (including a half-finished flicker) back to the cache.
		# Luminaires, spots and emissives stagger 0.08 s per entry. Sun, fill and ambient do not.
		_snapshot_restore_sources()
		tw.set_parallel(true)
		tw.tween_method(_apply_restore_global, 0.0, 1.0, 2.5).set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
		var slot: int = 0
		for i: int in range(_task_lights.size()):
			tw.tween_method(_apply_restore_task.bind(i), 0.0, 1.0, 2.5).set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT).set_delay(0.08 * float(slot))
			slot += 1
		for j: int in range(_spot_lights.size()):
			tw.tween_method(_apply_restore_spot.bind(j), 0.0, 1.0, 2.5).set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT).set_delay(0.08 * float(slot))
			slot += 1
		for k: int in range(_emissive_mats.size()):
			tw.tween_method(_apply_restore_emissive.bind(k), 0.0, 1.0, 2.5).set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT).set_delay(0.08 * float(slot))
			slot += 1
	_show_toast("SOLAR FLARE PROTOCOL // EMERGENCY LIGHTING ENGAGED" if on else "NOMINAL 5500K DAYLIGHT RESTORED", 3.0)


# ------------------------------------------------------------------------------
# Materials (BUG-07 guard + [t3u] emission)
# ------------------------------------------------------------------------------
func _set_tree_cast_shadow(root: Node3D, mode: GeometryInstance3D.ShadowCastingSetting) -> void:
	if root == null:
		return
	var st: Array[Node] = [root]
	while not st.is_empty():
		var c: Node = st.pop_back()
		if c is GeometryInstance3D:
			(c as GeometryInstance3D).cast_shadow = mode
		for ch: Node in c.get_children():
			st.append(ch)


func _blob_has(blob: String, keys: Array) -> bool:
	for key in keys:
		if blob.contains(String(key)):
			return true
	return false


# Used only when the glTF albedo is white. null means there is no table tint.
func _prop_glass_tint(blob: String) -> Variant:
	if _blob_has(blob, ["viewport", "window"]):
		return Color(0.70, 0.82, 0.88, 0.14)
	if blob.contains("hydro"):
		return Color(0.72, 0.90, 0.80, 0.22)
	if _blob_has(blob, ["suitbay", "locker"]):
		return Color(0.75, 0.85, 0.95, 0.18)
	if blob.contains("sonic_shield"):
		return Color(0.80, 0.86, 0.95, 0.20)
	if _blob_has(blob, ["autodoc", "med"]):
		return Color(0.85, 0.92, 0.95, 0.20)
	if blob.contains("transom"):
		return Color(0.72, 0.80, 0.86, 0.32)
	return null


func _upgrade_sector_materials(root: Node3D, emission_mult: float = 0.65) -> void:
	var stack: Array[Node] = [root]
	var to_convert: Array[ImporterMeshInstance3D] = []
	while not stack.is_empty():
		var curr: Node = stack.pop_back()
		if curr is ImporterMeshInstance3D:
			to_convert.append(curr as ImporterMeshInstance3D)
		for ch: Node in curr.get_children():
			stack.append(ch)

	for imp: ImporterMeshInstance3D in to_convert:
		if not is_instance_valid(imp):
			continue
		if imp.mesh == null or imp.mesh.get_surface_count() <= 0:
			continue
		var built_mesh: ArrayMesh = imp.mesh.get_mesh()
		if built_mesh == null or built_mesh.get_surface_count() <= 0:
			continue
		var orig_name: String = imp.name
		var mi: MeshInstance3D = MeshInstance3D.new()
		mi.transform = imp.transform
		mi.visible = imp.visible
		mi.mesh = built_mesh
		var p: Node = imp.get_parent()
		var children_to_move: Array[Node] = []
		for ch: Node in imp.get_children():
			children_to_move.append(ch)
		for ch: Node in children_to_move:
			imp.remove_child(ch)
			mi.add_child(ch)
		if p != null:
			var idx: int = imp.get_index()
			p.remove_child(imp)
			mi.name = orig_name
			p.add_child(mi)
			p.move_child(mi, idx)
		imp.free()

	var mstack: Array[Node] = [root]
	while not mstack.is_empty():
		var curr: Node = mstack.pop_back()
		if curr is MeshInstance3D:
			var mi: MeshInstance3D = curr as MeshInstance3D
			if mi.mesh != null and mi.mesh.get_surface_count() > 0:
				var has_opaque_surface: bool = false
				var mesh_nm: String = String(mi.mesh.resource_name).to_lower()
				for s_idx: int in range(mi.mesh.get_surface_count()):
					var mat: Material = mi.get_active_material(s_idx)
					if mat is StandardMaterial3D:
						var smat: StandardMaterial3D = (mat as StandardMaterial3D).duplicate() as StandardMaterial3D
						var mname: String = smat.resource_name.to_lower()
						var pname: String = mi.name.to_lower()
						var blob: String = mname + " " + pname + " " + mesh_nm
						# [M-34] Keep the glTF cull. DISABLED only for thin single-plane parts.
						if _blob_has(blob, ["foliage", "leaf", "card", "decal", "cloth", "transom", "holo", "field"]):
							smat.cull_mode = BaseMaterial3D.CULL_DISABLED
						var is_glass: bool = _blob_has(blob, ["glass", "translucent", "holo", "lens", "viewport", "transom", "sonic_shield"]) or pname.contains("glass") or pname.contains("window")
						if is_glass:
							smat.render_priority = 0
							var authored: Color = smat.albedo_color
							var authored_rough: float = smat.roughness
							smat.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
							smat.metallic = 0.0
							smat.metallic_specular = 0.5
							smat.roughness = maxf(authored_rough, 0.04)
							if _blob_has(blob, ["holo", "lens"]):
								var base_e: float = smat.emission_energy_multiplier if smat.emission_enabled else emission_mult
								smat.albedo_color = Color(authored.r, authored.g, authored.b, 0.35)
								smat.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
								smat.cull_mode = BaseMaterial3D.CULL_DISABLED
								smat.emission_enabled = true
								smat.emission = Color(authored.r, authored.g, authored.b, 1.0)
								smat.emission_energy_multiplier = base_e * 0.8
							else:
								smat.emission_enabled = false
								var white: bool = authored.r > 0.97 and authored.g > 0.97 and authored.b > 0.97
								var tint: Variant = _prop_glass_tint(blob) if white else null
								if tint is Color:
									smat.albedo_color = tint as Color
								else:
									smat.albedo_color = Color(authored.r, authored.g, authored.b, clampf(authored.a, 0.14, 0.40))
						else:
							has_opaque_surface = true
							if mname.contains("amber") or mname.contains("hazard"):
								smat.emission_enabled = true
								smat.albedo_color = COLOR_AMBER
								smat.emission = COLOR_AMBER
								smat.emission_energy_multiplier = emission_mult
							elif mname.contains("cyan") or mname.contains("emerald") or mname.contains("uv"):
								smat.emission_enabled = true
								smat.albedo_color = COLOR_CYAN
								smat.emission = COLOR_CYAN
								smat.emission_energy_multiplier = emission_mult
							elif smat.emission_enabled or smat.emission_texture != null:
								smat.emission_enabled = true
								if smat.emission_texture != null:
									smat.emission = Color(1.0, 1.0, 1.0, 1.0)
									smat.emission_operator = BaseMaterial3D.EMISSION_OP_MULTIPLY
								smat.emission_energy_multiplier = emission_mult
						mi.set_surface_override_material(s_idx, smat)
					else:
						has_opaque_surface = true
				if has_opaque_surface:
					mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_DOUBLE_SIDED
				else:
					mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
		for ch: Node in curr.get_children():
			mstack.append(ch)


# ------------------------------------------------------------------------------
# Camera presets (batch renders + 1-4 hotkeys)
# ------------------------------------------------------------------------------
func apply_camera_preset(idx: int) -> void:
	if idx < 0 or idx >= CAMERAS.size() or _camera == null:
		return
	var c: Dictionary = CAMERAS[idx]
	_camera.near = 0.02
	_camera.far = 6500.0
	_camera.fov = float(c["fov"])
	_camera.global_position = c["pos"] as Vector3
	_camera.look_at(c["target"] as Vector3, Vector3.UP)

	var show_fp: bool = bool(c["fp_wrist"])
	if _fp_wrist_holder != null:
		_fp_wrist_holder.visible = show_fp
		if show_fp and _fp_wrist_model != null:
			_play_actor_anim(_fp_wrist_model, ["RFIDPulse", "WristRaiseInspect"], 0.45)

	# Rostov staging only applies to the deterministic batch renders (in F5 he is the player avatar).
	if _rostov_root != null and _player_body == null:
		_rostov_root.visible = not show_fp
		if idx == 1:
			_rostov_root.position = Vector3(1.20, 4.29, 2.35)
			_rostov_root.rotation_degrees = Vector3(0.0, 95.0, 0.0)
		elif idx == 2:
			_rostov_root.position = Vector3(1.85, 0.12, 3.65)
			_rostov_root.rotation_degrees = Vector3(0.0, 35.0, 0.0)
		elif idx == 3:
			_rostov_root.position = Vector3(-0.85, 0.12, -4.65)
			_rostov_root.rotation_degrees = Vector3(0.0, 172.0, 0.0)


# ------------------------------------------------------------------------------
# Player controller (BUG-03)
# ------------------------------------------------------------------------------
func _setup_player_controller() -> void:
	_player_body = CharacterBody3D.new()
	_player_body.name = "PlayerBody"
	_player_body.floor_max_angle = deg_to_rad(50.0)
	_player_body.floor_snap_length = 0.35
	_player_body.floor_stop_on_slope = true
	add_child(_player_body)
	var cs: CollisionShape3D = CollisionShape3D.new()
	cs.name = "PlayerCapsule"
	var cap: CapsuleShape3D = CapsuleShape3D.new()
	cap.radius = 0.35
	cap.height = 1.75
	cs.shape = cap
	cs.position = Vector3(0.0, 0.875 + 0.12, 0.0)  # bottom 0.12m above origin clears the 0.15m apartment floor finish
	_player_body.add_child(cs)
	_player_body.global_position = SPAWN_POS
	_player_body.rotation_degrees = Vector3(0.0, SPAWN_YAW_DEG, 0.0)

	_camera_pivot = Node3D.new()
	_camera_pivot.name = "CameraPivot"
	_camera_pivot.position = Vector3(0.0, 1.50 + 0.12, 0.0)
	# [QA-05] Rest pose of the FP camera mount. Step ease / landing dip assign Y from this.
	_fp_cam_base_pos = _camera_pivot.position
	_fp_cam_base_set = true
	_player_body.add_child(_camera_pivot)

	_spring_arm = SpringArm3D.new()
	_spring_arm.name = "ThirdPersonSpringArm"
	_spring_arm.spring_length = 0.0
	_spring_arm.margin = 0.12
	_spring_arm.add_excluded_object(_player_body.get_rid())
	_camera_pivot.add_child(_spring_arm)

	if _camera != null:
		_camera.top_level = false
		_camera.get_parent().remove_child(_camera)
		_spring_arm.add_child(_camera)
		_camera.transform = Transform3D.IDENTITY
		_camera.fov = 70.0
		_camera.near = 0.02
		_camera.far = 6500.0
		_camera.current = true

	if _rostov_root != null:
		_rostov_root.get_parent().remove_child(_rostov_root)
		_player_body.add_child(_rostov_root)
		_rostov_root.position = Vector3(0.0, 0.12, 0.0)
		_rostov_root.rotation_degrees = Vector3(0.0, 180.0, 0.0)
		_rostov_anim = ""
		_set_rostov_anim("Idle")

	if _fp_wrist_holder != null:
		# [t31u] Arm is no longer glued to the camera: its pose is solved every physics frame in body space.
		_fp_wrist_holder.get_parent().remove_child(_fp_wrist_holder)
		add_child(_fp_wrist_holder)
		_fp_wrist_holder.top_level = true
		_arm_raise_blend = 0.0
	if _camera != null:
		_flashlight = SpotLight3D.new()
		_flashlight.name = "PlayerFlashlight"
		_flashlight.position = Vector3(0.10, -0.06, -0.05)
		_flashlight.light_color = Color("#FFF1DC")
		_flashlight.light_energy = 2.4
		_flashlight.spot_range = 16.0
		_flashlight.spot_angle = 26.0
		_flashlight.spot_angle_attenuation = 0.9
		_flashlight.shadow_enabled = true
		_flashlight.shadow_bias = 0.03
		_flashlight.visible = false
		_camera.add_child(_flashlight)
	if _fp_wrist_model != null:
		_play_actor_anim(_fp_wrist_model, ["Idle", "WristRaiseInspect"], 0.0)
	_apply_view_mode()
	_update_first_person_arm(0.0)


func _toggle_flashlight() -> void:
	if _flashlight == null:
		return
	_flashlight.visible = not _flashlight.visible
	_show_toast("FLASHLIGHT " + ("ON" if _flashlight.visible else "OFF"), 1.2)


func _set_rostov_anim(nm: String) -> void:
	if _rostov_root == null or _rostov_anim == nm:
		return
	_rostov_anim = nm
	if nm == "WalkCycle":
		_play_actor_anim(_rostov_root, ["WalkCycle", "Walk", "Idle"], 0.0)
	else:
		_play_actor_anim(_rostov_root, ["Idle", "IdleCurious", "IdleBreathing", "WalkCycle"], 0.0)


func _apply_view_mode() -> void:
	if _spring_arm == null:
		return
	if _third_person:
		_spring_arm.spring_length = TP_ARM_LENGTH
		_spring_arm.position = Vector3(0.45, 0.20, 0.0)
	else:
		_spring_arm.spring_length = 0.0
		_spring_arm.position = Vector3.ZERO
	if _fp_wrist_holder != null:
		_fp_wrist_holder.visible = not _third_person and _preset_active < 0
	if _rostov_root != null:
		_rostov_root.visible = _third_person or _preset_active >= 0
	_pitch = clampf(_pitch, deg_to_rad(-60.0) if _third_person else deg_to_rad(PITCH_MIN_DEG), deg_to_rad(45.0) if _third_person else deg_to_rad(PITCH_MAX_DEG))
	if _camera_pivot != null:
		_camera_pivot.rotation = Vector3(_pitch, 0.0, 0.0)


func _toggle_view() -> void:
	if _preset_active >= 0:
		_return_to_player()
	_third_person = not _third_person
	_apply_view_mode()
	_show_toast("VIEW: " + ("3RD-PERSON [ROSTOV #02]" if _third_person else "1ST-PERSON [WRIST #04]"), 1.8)


func _activate_preset(idx: int) -> void:
	if _camera == null:
		return
	_preset_active = idx
	_camera.top_level = true
	apply_camera_preset(idx)
	if _rostov_root != null:
		_rostov_root.visible = true
	_show_toast("SHOWCASE CAM %02d // [0] RETURNS TO PLAYER" % (idx + 1), 2.2)


func _return_to_player() -> void:
	if _camera == null:
		return
	_preset_active = -1
	_camera.top_level = false
	_camera.transform = Transform3D.IDENTITY
	_camera.fov = 70.0
	_apply_view_mode()


func _respawn() -> void:
	if _player_body == null:
		return
	_player_body.global_position = SPAWN_POS
	_player_body.velocity = Vector3.ZERO
	_player_body.rotation_degrees = Vector3(0.0, SPAWN_YAW_DEG, 0.0)
	_show_toast("TELEMETRY LOST — RESPAWNED IN APT 201", 2.0)


func _unhandled_input(event: InputEvent) -> void:
	if _player_body == null or _capture_hud:
		return
	# Troubleshoot UI is modal: no look, no [E], no other gameplay keys. The holo still takes GUI input.
	if _troubleshoot_ui_open():
		return
	if event is InputEventMouseButton and (event as InputEventMouseButton).pressed:
		if Input.mouse_mode != Input.MOUSE_MODE_CAPTURED:
			Input.mouse_mode = Input.MOUSE_MODE_CAPTURED
			get_viewport().set_input_as_handled()
			return
	if event is InputEventMouseMotion and (Input.mouse_mode == Input.MOUSE_MODE_CAPTURED or _qa_hand) and _preset_active < 0:
		var mm: InputEventMouseMotion = event as InputEventMouseMotion
		# screen_relative is unscaled by canvas_items stretch; relative was scaled by base_res/window_res (x1.44 in a 1331 px window), which made look speed window-size dependent (Patch Windows hand QA 18/20).
		# [QA-05] Pitch sign stays as authored (no invert-Y). Scale is _mouse_sens.
		_player_body.rotate_object_local(Vector3.UP, -mm.screen_relative.x * _mouse_sens)
		_pitch -= mm.screen_relative.y * _mouse_sens
		_apply_pitch()
		return
	if event is InputEventKey:
		var ke: InputEventKey = event as InputEventKey
		if not ke.pressed or ke.echo:
			return
		# [M-23] E / F / Tab (and V) come from the InputMap actions, not hardcoded keys.
		if event.is_action_pressed("toggle_view"):
			_toggle_view()
			return
		if event.is_action_pressed("interact"):
			_interact()
			return
		if event.is_action_pressed("rfid_pulse"):
			_trigger_rfid_pulse()
			return
		# [SYS-16] Debug/system keys come from InputMap actions (project.godot), not hardcoded keys.
		if event.is_action_pressed("release_mouse"):
			Input.mouse_mode = Input.MOUSE_MODE_VISIBLE
		elif event.is_action_pressed("toggle_gravity_ring"):
			_toggle_gravity_ring_test()
		elif event.is_action_pressed("toggle_flashlight"):
			_toggle_flashlight()
		elif event.is_action_pressed("toggle_lighting"):
			_set_emergency_lighting(not _emergency)
		elif event.is_action_pressed("preset_1"):
			_activate_preset(0)
		elif event.is_action_pressed("preset_2"):
			_activate_preset(1)
		elif event.is_action_pressed("preset_3"):
			_activate_preset(2)
		elif event.is_action_pressed("preset_4"):
			_activate_preset(3)
		elif event.is_action_pressed("return_to_player"):
			_return_to_player()
			_show_toast("ACTIVE PLAYER CONTROL", 1.5)
		else:
			return
		get_viewport().set_input_as_handled()


func _apply_pitch() -> void:
	var lo: float = deg_to_rad(-60.0) if _third_person else deg_to_rad(PITCH_MIN_DEG)
	var hi: float = deg_to_rad(45.0) if _third_person else deg_to_rad(PITCH_MAX_DEG)
	_pitch = clampf(_pitch, lo, hi)
	if _camera_pivot != null:
		_camera_pivot.rotation = Vector3(_pitch, 0.0, 0.0)


# [QA-05] Ease step-up and landing dip back to 0, then assign a negative local Y on the
# FP camera pivot (it holds the FP camera). SpringArm rewrites the camera node's transform,
# so the offset stays on the pivot. Rest pose is stored once and assigned, never stacked.
# Third person and a detached showcase camera keep the rest pose. No walk bob.
func _qa05_ease_fp_camera(delta: float) -> void:
	_step_ease_offset = move_toward(_step_ease_offset, 0.0, (STEP_HEIGHT / STEP_EASE_S) * delta)
	_land_dip = move_toward(_land_dip, 0.0, (LAND_DIP_M / 0.18) * delta)
	if _camera_pivot == null:
		return
	if not _fp_cam_base_set:
		_fp_cam_base_pos = _camera_pivot.position
		_fp_cam_base_set = true
	var y_off: float = 0.0
	if not _third_person and (_camera == null or not _camera.top_level):
		y_off = -(_step_ease_offset + _land_dip)
	var pos: Vector3 = _fp_cam_base_pos
	pos.y += y_off
	_camera_pivot.position = pos


## [SYS-23] Rise of a walkable step top just ahead of the capsule, or -1.0 if none. Rays use the
## body's own mask and skip the player. The reach is STEP_HEIGHT + 0.10 so the 0.40 m edges QA
## already climbs (the capsule rode up them) keep working.
func _step_rise_ahead(b: CharacterBody3D, dir: Vector3, up_dir: Vector3, walk_cos: float, contact: Vector3) -> float:
	var space: PhysicsDirectSpaceState3D = b.get_world_3d().direct_space_state
	var reach: float = STEP_HEIGHT + 0.10
	var base: Vector3 = b.global_position + up_dir * 0.12
	var q0: PhysicsRayQueryParameters3D = PhysicsRayQueryParameters3D.create(base + up_dir * 0.30, base - up_dir * 0.30, b.collision_mask, [b.get_rid()])
	var h0: Dictionary = space.intersect_ray(q0)
	if h0.is_empty():
		return -1.0
	var ground_up: float = (h0["position"] as Vector3).dot(up_dir)
	# Sample just past the wall contact (at feet height), then further in for chamfered edges
	# (curbs); the first walkable hit is the step top.
	var c_flat: Vector3 = contact - up_dir * (contact - base).dot(up_dir)
	for off: float in [0.05, 0.15, 0.25]:
		var ahead: Vector3 = c_flat + dir * off
		var q1: PhysicsRayQueryParameters3D = PhysicsRayQueryParameters3D.create(ahead + up_dir * reach, ahead - up_dir * 0.05, b.collision_mask, [b.get_rid()])
		var h1: Dictionary = space.intersect_ray(q1)
		if h1.is_empty():
			continue
		if (h1["normal"] as Vector3).dot(up_dir) < walk_cos - 0.001:
			continue
		var rise: float = (h1["position"] as Vector3).dot(up_dir) - ground_up
		if rise > reach - 0.005:
			return -1.0
		return rise
	return -1.0
func _physics_process(delta: float) -> void:
	# Stall flicker has to tick on physics frames: --qa-forcefield-door awaits physics_frame,
	# and a physics catch-up burst can run those frames before the next idle _process.
	_ff_tick_active_stalls(delta)
	_apply_ring_box_gravity(delta)
	_process_core_transits(delta)
	if _player_body == null:
		return
	var b: CharacterBody3D = _player_body
	if not _player_transit.is_empty():
		# [QA-05] Buffer and coyote still drain while a core transit owns the body.
		_jump_buffer_t = maxf(_jump_buffer_t - delta, -1.0)
		_coyote_t = maxf(_coyote_t - delta, -1.0)
		_qa05_ease_fp_camera(delta)
		_update_first_person_arm(delta)
		return
	var controls: bool = _preset_active < 0 and not _capture_hud and not _troubleshoot_ui_open()

	var input_dir: Vector2 = Vector2.ZERO
	var sprint: bool = false
	# [QA-05] Held `jump` stays sampled and must not start a jump.
	@warning_ignore("unused_variable")
	var jump: bool = false
	if controls:
		# Keyboard look: Q / Left = turn left, Right = turn right, PageUp / PageDown = look up / down.
		var yaw_in: float = 0.0
		# [SYS-16] Keyboard look from InputMap: look_left (Q, Left), look_right (Right).
		if Input.is_action_pressed("look_left"):
			yaw_in += 1.0
		if Input.is_action_pressed("look_right"):
			yaw_in -= 1.0
		if yaw_in != 0.0:
			b.rotate_object_local(Vector3.UP, yaw_in * KEY_LOOK_SPEED * delta)
		var pitch_in: float = 0.0
		if Input.is_action_pressed("look_up"):
			pitch_in += 1.0
		if Input.is_action_pressed("look_down"):
			pitch_in -= 1.0
		if pitch_in != 0.0:
			_pitch += pitch_in * KEY_LOOK_SPEED * 0.6 * delta
			_apply_pitch()
		# [INPUT-01] Movement is the Input Map. _qa_key still feeds these actions: it sets physical_keycode,
		# and project.godot binds W/A/S/D, Shift, and Space on both keycode and physical_keycode.
		input_dir = Input.get_vector("move_left", "move_right", "move_forward", "move_back")
		sprint = Input.is_action_pressed("sprint")
		jump = Input.is_action_pressed("jump")

	# [t34u] Local "up" = world up normally, or toward the cylinder axis inside the spin-gravity ring.
	var in_ring: bool = _in_gravity_ring(b.global_position)
	var up_dir: Vector3 = _ring_up_at(b.global_position, b.global_basis.y) if in_ring else Vector3.UP
	_orient_node_to_up(b, up_dir, delta)
	b.up_direction = up_dir
	var g_vec: Vector3 = _ring_gravity_at(b.global_position) if in_ring else Vector3.DOWN * GRAVITY

	var basis: Basis = b.global_transform.basis
	var dir: Vector3 = basis.x * input_dir.x + basis.z * input_dir.y
	dir -= up_dir * dir.dot(up_dir)
	if dir.length_squared() > 0.0001:
		dir = dir.normalized()
	var speed: float = SPRINT_SPEED if sprint else WALK_SPEED

	# [QA-05] Accelerate toward the wish velocity. A fresh jump press fills the buffer; holding does not repeat.
	var v_up: float = b.velocity.dot(up_dir)
	if not b.is_on_floor():
		v_up = (b.velocity + g_vec * delta).dot(up_dir)
	# [SYS-19] Check first, count down after, so both windows are the full 0.10 s.
	# Timers rest at -1.0 (inactive); a timer counts while >= -0.0001.
	if controls and Input.is_action_just_pressed("jump"):
		_jump_buffer_t = JUMP_BUFFER_S
	if b.is_on_floor():
		_coyote_t = COYOTE_S
	if _jump_buffer_t >= -0.0001 and _coyote_t >= -0.0001:
		v_up = JUMP_VELOCITY
		_jump_buffer_t = -1.0
		_coyote_t = -1.0
	_jump_buffer_t = maxf(_jump_buffer_t - delta, -1.0)
	_coyote_t = maxf(_coyote_t - delta, -1.0)
	var h: Vector3 = b.velocity - up_dir * b.velocity.dot(up_dir)
	var target: Vector3 = dir * speed
	if b.is_on_floor():
		if dir != Vector3.ZERO:
			h = h.move_toward(target, GROUND_ACCEL * delta)
		else:
			h = h.move_toward(Vector3.ZERO, GROUND_FRICTION * delta)
	elif dir != Vector3.ZERO:
		h = h.move_toward(target, AIR_ACCEL * delta)
	b.velocity = h + up_dir * v_up

	# Smooth step-up over small ledges (thresholds, treads, slab lips) — only for wall-like hits,
	# so gently curving floors (cylinder ring) never trigger a bogus step.
	var step_pre_up: float = NAN
	if b.is_on_floor() and dir != Vector3.ZERO:
		var motion: Vector3 = dir * speed * delta
		var hit: KinematicCollision3D = KinematicCollision3D.new()
		# [SYS-21] Step on any face too steep to walk (floor_max_angle 50 deg), not only normal.y < 0.5.
		var walk_cos: float = cos(b.floor_max_angle)
		if b.test_move(b.global_transform, motion, hit) and hit.get_normal().dot(up_dir) < walk_cos - 0.001:
			# [SYS-22/23/24] Find the step top with rays: one under the body (current ground) and one
			# just ahead of the capsule, where the top is flat (the capsule's down-probe used to land on the
			# edge corner, refuse for a tick and zero the speed). Raise by the measured rise, not STEP_HEIGHT,
			# so the body lands on the top instead of sinking back down the edge (camera dip).
			# A true wall leaves no walkable top within reach, so it never steps.
			var rise_step: float = _step_rise_ahead(b, dir, up_dir, walk_cos, hit.get_position())
			var up: Vector3 = up_dir * (rise_step + 0.004)
			if rise_step > 0.02 and not b.test_move(b.global_transform, up) and not b.test_move(b.global_transform.translated(up), motion):
				step_pre_up = (b.global_position).dot(up_dir)
				b.global_position += up

	var was_on_floor: bool = b.is_on_floor()
	var up_vel_before: float = v_up
	b.move_and_slide()
	# [SYS-18] Ease the camera by the rise actually gained after the slide settles, not STEP_HEIGHT.
	if not is_nan(step_pre_up):
		var rise: float = clampf(b.global_position.dot(up_dir) - step_pre_up, 0.0, STEP_HEIGHT + 0.10)
		_step_ease_offset = minf(_step_ease_offset + rise, 0.4)
	# [QA-05] Hard landing dip from the pre-slide up-velocity. No continuous bob.
	if not was_on_floor and b.is_on_floor():
		var fall_speed: float = -up_vel_before
		if fall_speed >= LAND_DIP_MIN_FALL:
			_land_dip = LAND_DIP_M * clampf(fall_speed / 8.0, 0.4, 1.0)
	for sc_i: int in range(b.get_slide_collision_count()):
		var scol: KinematicCollision3D = b.get_slide_collision(sc_i)
		if _qa_egress:
			var slide_n: Object = scol.get_collider()
			if slide_n is Node:
				_qa_last_slide_path = String((slide_n as Node).get_path())
		if scol.get_collider() is RigidBody3D:
			(scol.get_collider() as RigidBody3D).apply_central_impulse(-scol.get_normal() * 1.4)

	if not in_ring and b.global_position.y < -8.0:
		_respawn()
	_update_interior_streaming(b.global_position)
	_qa05_ease_fp_camera(delta)
	_update_first_person_arm(delta)

	var hvel: Vector3 = b.velocity - up_dir * b.velocity.dot(up_dir)
	var moving: bool = hvel.length() > 0.2 and b.is_on_floor()
	_set_rostov_anim("WalkCycle" if moving else "Idle")
	if _rostov_root != null:
		var ap: AnimationPlayer = _find_anim_player(_rostov_root)
		if ap != null and moving:
			ap.speed_scale = 1.45 if sprint else 1.0


# ------------------------------------------------------------------------------
# Interaction (E) & RFID pulse (R) (BUG-06)
# ------------------------------------------------------------------------------
func _player_probe_point() -> Vector3:
	if _player_body == null:
		return Vector3.ZERO
	return _player_body.global_position + Vector3(0.0, 1.0, 0.0)


func _find_nearest_interactable(max_dist: float) -> Dictionary:
	var best: Dictionary = {}
	var best_d: float = max_dist
	var pp: Vector3 = _player_probe_point()
	for it: Dictionary in _interactables:
		if bool(it["collected"]):
			continue
		if not is_instance_valid(it["node"]):
			continue
		var n: Node3D = it["node"] as Node3D
		if n == null or not n.is_inside_tree():
			continue
		var target: Vector3 = n.global_position
		if String(it["kind"]) == "bot":
			target += Vector3(0.0, 0.7, 0.0)
		var d: float = pp.distance_to(target)
		if d < best_d:
			best_d = d
			best = it
	return best


func _interact() -> void:
	# [5DB-03] [E] does nothing while the troubleshoot holo is already up.
	if _troubleshoot_ui_open():
		return
	if not _third_person:
		_interact_reach_timer = INTERACT_REACH_DURATION
	if _player_body != null and _start_core_transit(_player_body, true):
		_show_toast("CORIOLIS CORE LIFT // TRANSITING TO OPPOSITE FLOOR", 2.4)
		return
	# [QA-HUB-01] [E] at a hub (in range, facing it, on its side of the wall) toggles that ONE door and takes
	# priority over pickups; otherwise [E] behaves as before.
	var door_changes: Array[String] = _scan_rfid_doors(_player_probe_point())
	if not door_changes.is_empty():
		if _fp_wrist_model != null and not _third_person:
			_play_actor_anim(_fp_wrist_model, ["RFIDPulse", "Idle"], 0.0)
		_show_toast("RFID ACCESS // " + ", ".join(door_changes), 2.4)
		return
	var it: Dictionary = _find_nearest_interactable(INTERACT_RANGE)
	if it.is_empty():
		_show_toast("NOTHING IN REACH // MOVE WITHIN 2.8m", 1.6)
		return
	var kind: String = String(it["kind"])
	if bool(it["pickup"]):
		it["collected"] = true
		var picked: Node3D = it["node"] as Node3D
		_collected_pickup_ids[String(it.get("id", picked.name))] = true
		picked.visible = false
		picked.queue_free()
		_inventory[kind] = int(_inventory[kind]) + 1
		_show_toast("COLLECTED %s  [%d/%d]" % [String(it["label"]), int(_inventory[kind]), int(_inventory_max[kind])], 2.6)
		if _fp_wrist_model != null and not _third_person:
			_play_actor_anim(_fp_wrist_model, ["WristRaiseInspect", "Idle"], 0.0)
	elif kind == "bot":
		_show_toast("%s  (%s)\n\"%s\"" % [String(it["label"]), String(it["dept"]), String(it["status"])], 4.5)
		var bot_node: Node3D = it["node"] as Node3D
		_play_actor_anim(bot_node, ["Celebrate", "Idle"], 0.0)
	elif kind == "rfid_door":
		# Hub scan missed (range, facing, or the wrong side of the wall): refused RFID, collider stays on.
		var refused_id: String = String(it.get("door_id", ""))
		if refused_id != "":
			deny_flicker(refused_id)
		_trigger_rfid_pulse()
	elif kind == "terminal":
		# [REV-C2] The WORKBENCH TERMINAL toast is gone with the APT 201 bench. This alcove tool-wall terminal stays.
		var total: int = 0
		var have: int = 0
		for k: String in _inventory.keys():
			total += int(_inventory_max[k])
			have += int(_inventory[k])
		_show_toast("TOOL WALL TERMINAL // Sector-4 bulkhead relay: JAMMED AT 40%%.\nUpgrade kit %d/%d gathered. Need: +5A cell + Super-Wire on [RESET]." % [have, total], 4.5)
	elif kind == "troubleshoot":
		# [5DB-01] Replaces the retired PcbaPythonPuzzleUI. The simple board is the D-204 hatch service.
		open_troubleshoot_simple("D-204")
	elif kind == "anim_prop":
		var prop_node: Node3D = it["node"] as Node3D
		var prop_id: String = String(it.get("id", prop_node.name if prop_node != null else ""))
		var spec: Dictionary = it.get("spec", {}) as Dictionary
		var ap_prop: AnimationPlayer = _find_anim_player(prop_node) if prop_node != null else null
		if ap_prop == null:
			push_warning("[PrefacePlayableArea] No AnimationPlayer on " + prop_id)
		else:
			var toggles: Array = spec.get("toggle", []) as Array
			if toggles.size() >= 2:
				var ti: int = int(it.get("toggle_i", 0))
				if ti < 0 or ti >= toggles.size():
					ti = 0
				var played: String = _apply_anim_clip(ap_prop, String(toggles[ti]), false)
				if played == "":
					push_warning("[PrefacePlayableArea] Missing toggle clip %s on %s" % [String(toggles[ti]), prop_id])
				else:
					ap_prop.play(played)
					it["toggle_i"] = (ti + 1) % toggles.size()
			else:
				var action_clip: String = String(spec.get("action", ""))
				var played_a: String = _apply_anim_clip(ap_prop, action_clip, false)
				if played_a == "":
					push_warning("[PrefacePlayableArea] Missing action clip %s on %s" % [action_clip, prop_id])
				else:
					ap_prop.play(played_a)
					var idle_clip: String = String(spec.get("idle", ""))
					var idle_name: String = _apply_anim_clip(ap_prop, idle_clip, true)
					if idle_name != "":
						ap_prop.queue(idle_name)
					elif idle_clip != "":
						push_warning("[PrefacePlayableArea] Missing idle clip %s on %s" % [idle_clip, prop_id])
		_show_toast(String(it.get("label", prop_id)), 2.4)


func _trigger_rfid_pulse() -> void:
	if _player_body == null:
		return
	if _fp_wrist_model != null:
		_play_actor_anim(_fp_wrist_model, ["RFIDPulse", "Idle"], 0.0)
	# [t31u] Raises the wrist and shows the dynamic PulseRings only for the pulse duration.
	_rfid_pulse_timer = RFID_PULSE_DURATION

	var lines: PackedStringArray = PackedStringArray()
	lines.append("#04 WRIST RFID PULSE // 13.56 MHz // RANGE 12.0m")
	var pp: Vector3 = _player_probe_point()
	var door_changes: Array[String] = []  # [QA-HUB-01] doors are opened with [E] at their hub, not by the [F] pulse
	var found: Array[Dictionary] = []
	for it: Dictionary in _interactables:
		if bool(it["collected"]):
			continue
		if not is_instance_valid(it["node"]):
			continue
		var n: Node3D = it["node"] as Node3D
		if n == null or not n.is_inside_tree():
			continue
		var d: float = pp.distance_to(n.global_position)
		if d <= 12.0:
			found.append({"it": it, "d": d})
	found.sort_custom(func(a: Dictionary, b: Dictionary) -> bool: return float(a["d"]) < float(b["d"]))
	for f: Dictionary in found.slice(0, 6):
		var it2: Dictionary = f["it"]
		var tag: String = String(it2["label"])
		if String(it2["kind"]) == "bot":
			tag += "  " + String(it2["dept"]) + "  [ACK]"
		lines.append("  > %-34s %5.1fm" % [tag, float(f["d"])])
	if found.is_empty():
		lines.append("  > NO TAGS RESPONDING")
	if _hud_scan != null:
		_hud_scan.text = "\n".join(lines)
		_hud_scan.visible = true
	_scan_t = 6.0
	var door_note: String = (" // " + ", ".join(door_changes)) if not door_changes.is_empty() else ""
	_show_toast("RFID PULSE EMITTED // %d TAG(S) RESPONDED%s" % [found.size(), door_note], 2.4)


# ------------------------------------------------------------------------------
# HUD
# ------------------------------------------------------------------------------
func _make_panel(parent: Control, pos: Vector2, size: Vector2, accent: Color) -> Panel:
	var p: Panel = Panel.new()
	p.position = pos
	p.size = size
	p.mouse_filter = Control.MOUSE_FILTER_IGNORE
	var sb: StyleBoxFlat = StyleBoxFlat.new()
	sb.bg_color = Color(0.05, 0.07, 0.09, 0.72)
	sb.border_color = Color(accent.r, accent.g, accent.b, 0.85)
	sb.border_width_left = 3
	sb.border_width_top = 1
	sb.border_width_right = 1
	sb.border_width_bottom = 1
	sb.set_corner_radius_all(4)
	p.add_theme_stylebox_override("panel", sb)
	parent.add_child(p)
	return p


func _make_label(parent: Control, pos: Vector2, txt: String, fsize: int, col: Color) -> Label:
	var l: Label = Label.new()
	l.position = pos
	l.text = txt
	l.mouse_filter = Control.MOUSE_FILTER_IGNORE
	l.add_theme_font_size_override("font_size", fsize)
	l.add_theme_color_override("font_color", col)
	l.add_theme_color_override("font_shadow_color", Color(0, 0, 0, 0.8))
	l.add_theme_constant_override("shadow_offset_x", 1)
	l.add_theme_constant_override("shadow_offset_y", 1)
	parent.add_child(l)
	return l


func _build_hud() -> void:
	if _batch_render:
		return
	_hud = CanvasLayer.new()
	_hud.name = "Aegis7DiegeticHUD"
	_hud.layer = 5
	add_child(_hud)
	var root: Control = Control.new()
	root.name = "HUDRoot"
	root.set_anchors_preset(Control.PRESET_FULL_RECT)
	root.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_hud.add_child(root)

	var white: Color = Color("#DCE3EA")
	var dim: Color = Color("#8C98A4")

	# Top-left status panel hidden for clean immersive 1st-person viewport (Todo #3 — no permanent HUD banners)
	var tl: Panel = _make_panel(root, Vector2(24, 22), Vector2(560, 160), COLOR_CYAN)
	tl.visible = false
	_make_label(tl, Vector2(16, 10), "AEGIS-7 // HAB-7 RESIDENTIAL ATRIUM", 20, Color("#9FD3E0"))
	_hud_zone = _make_label(tl, Vector2(16, 44), "ZONE: --", 15, white)
	_hud_view = _make_label(tl, Vector2(16, 68), "VIEW: --", 15, white)
	_hud_light = _make_label(tl, Vector2(16, 92), "LIGHTING: --", 15, white)
	_hud_inv = _make_label(tl, Vector2(16, 120), "BCI: 0/1 | JELLY: 0/1 | WIRE: 0/3 | BATT: 0/4", 15, Color("#E2C79A"))

	# [t38u] Precision-centered geometric HUD reticle synced directly to get_viewport().get_visible_rect().size * 0.5
	var reticle_box: Control = Control.new()
	reticle_box.name = "ReticleBox"
	reticle_box.custom_minimum_size = Vector2(24, 24)
	reticle_box.size = Vector2(24, 24)
	reticle_box.mouse_filter = Control.MOUSE_FILTER_IGNORE
	root.add_child(reticle_box)
	reticle_box.set_anchors_and_offsets_preset(Control.PRESET_CENTER, Control.PRESET_MODE_KEEP_SIZE)
	reticle_box.grow_horizontal = Control.GROW_DIRECTION_BOTH
	reticle_box.grow_vertical = Control.GROW_DIRECTION_BOTH
	_reticle_box = reticle_box
	_sync_reticle_to_viewport_center()
	var vp: Viewport = get_viewport()
	if vp != null and not vp.size_changed.is_connected(_sync_reticle_to_viewport_center):
		vp.size_changed.connect(_sync_reticle_to_viewport_center)

	for r: Rect2 in [
		Rect2(11, 11, 2, 2),  # Exact 2x2 center dot at (11..13, 11..13) of 24x24 box -> (959..961, 539..541)
		Rect2(0, 11, 8, 2),   # Left tick
		Rect2(16, 11, 8, 2),  # Right tick
		Rect2(11, 0, 2, 8),   # Top tick
		Rect2(11, 16, 2, 8)   # Bottom tick
	]:
		var cr: ColorRect = ColorRect.new()
		cr.position = r.position
		cr.size = r.size
		cr.color = Color(0.88, 0.95, 0.98, 0.92)
		cr.mouse_filter = Control.MOUSE_FILTER_IGNORE
		reticle_box.add_child(cr)

	var center: Control = Control.new()
	center.set_anchors_preset(Control.PRESET_CENTER)
	center.mouse_filter = Control.MOUSE_FILTER_IGNORE
	root.add_child(center)
	_hud_prompt = _make_label(center, Vector2(-260, 26), "", 17, Color("#9FD3E0"))
	_hud_prompt.custom_minimum_size = Vector2(520, 0)
	_hud_prompt.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_hud_toast = _make_label(center, Vector2(-420, 120), "", 16, Color("#E8EEF3"))
	_hud_toast.custom_minimum_size = Vector2(840, 0)
	_hud_toast.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER

	# Right-side RFID telemetry readout
	var tr_anchor: Control = Control.new()
	tr_anchor.set_anchors_preset(Control.PRESET_TOP_RIGHT)
	tr_anchor.mouse_filter = Control.MOUSE_FILTER_IGNORE
	root.add_child(tr_anchor)
	_hud_scan = _make_label(tr_anchor, Vector2(-640, 26), "", 14, Color("#9FD3E0"))
	_hud_scan.visible = false

	# Training-wheel bottom controls legend bar stripped per [t22u] Todo #3


func _zone_name(p: Vector3) -> String:
	if p.y > 3.4:
		if p.x < -5.2 and p.z > 2.75:
			return "APT 201 — LEAD TECH QUARTERS"
		if p.x > 5.2 and p.z > 2.75:
			return "APT 202 — QUARTERMASTER QUARTERS"
		if p.x < -7.5 and p.z < 1.2:
			return "ALCOVE 2C — ENGINEERING SUPPLY"
		if p.x > 7.5 and p.z < 1.2:
			return "EAST STAIR LANDING"
		return "L2 MEZZANINE GALLERY"
	if p.x > 9.0 and p.z < -2.0 and p.y > 0.3:
		return "EAST STAIR-RAMP CONNECTOR"
	# [REAL-03] RM 1A / RM 1B only inside the enclosed room interiors (sector glb room-shell bounds, walls inset).
	if ROOM_1A_INTERIOR.has_point(p):
		return "RM 1A — LAUNDRY LOUNGE"
	if ROOM_1B_INTERIOR.has_point(p):
		return "RM 1B — BOT SUBSTATION"
	if p.z < -9.1:
		return "SECTOR-4 PROMENADE — CYLINDER HAB-7"
	if p.z < -7.0:
		return "SOUTH SERVICE VESTIBULE"
	return "L1 ATRIUM CONCOURSE"


func _update_hud() -> void:
	if _hud == null or _player_body == null:
		return
	_hud_zone.text = "ZONE: " + _zone_name(_player_body.global_position)
	if _preset_active >= 0:
		_hud_view.text = "VIEW: SHOWCASE CAM %02d  [0] PLAYER" % (_preset_active + 1)
	else:
		_hud_view.text = "VIEW: " + ("3RD-PERSON [ROSTOV #02]" if _third_person else "1ST-PERSON [WRIST #04]")
	_hud_light.text = "LIGHTING: " + ("SOLAR FLARE EMERGENCY" if _emergency else "NOMINAL 5500K DAYLIGHT")
	_hud_light.add_theme_color_override("font_color", Color("#E07A5F") if _emergency else Color("#DCE3EA"))
	_hud_inv.text = "BCI: %d/%d | JELLY: %d/%d | WIRE: %d/%d | BATT: %d/%d" % [
		int(_inventory["bci"]), int(_inventory_max["bci"]), int(_inventory["jelly"]), int(_inventory_max["jelly"]),
		int(_inventory["wire"]), int(_inventory_max["wire"]), int(_inventory["batt"]), int(_inventory_max["batt"])]
	_nearest = _find_nearest_interactable(INTERACT_RANGE)
	# [QA-HUB-01] the door prompt mirrors exactly what an [E] press would do (same single-target rule; door first).
	var scan_door: Dictionary = _scan_target_door(_player_probe_point()) if _preset_active < 0 else {}
	if _preset_active >= 0 or (_nearest.is_empty() and scan_door.is_empty()):
		_hud_prompt.text = ""
	elif not scan_door.is_empty():
		_hud_prompt.text = "[E] RFID SCAN // %s // %s" % [String(scan_door["label"]), "CLOSE" if bool(scan_door["open"]) else "OPEN"]
	else:
		var knd: String = String(_nearest["kind"])
		if knd == "rfid_door":
			_hud_prompt.text = ""
		else:
			var verb: String = "PICK UP" if bool(_nearest["pickup"]) else "QUERY"
			if knd == "troubleshoot":
				verb = "OPEN"
			_hud_prompt.text = "[E] %s %s" % [verb, String(_nearest["label"])]


func _show_toast(msg: String, dur: float) -> void:
	if _hud_toast == null:
		return
	_hud_toast.text = msg
	_hud_toast.modulate.a = 1.0
	_toast_t = dur


# ------------------------------------------------------------------------------
# Frame loop
# ------------------------------------------------------------------------------
func _process(delta: float) -> void:
	_frame_counter += 1
	_time += delta
	if _starfield_cylinder != null and is_instance_valid(_starfield_cylinder):
		_starfield_cylinder.rotate_x(STARFIELD_ROT_SPEED * delta)
		# [CYL-02] The sun rides the backdrop. The habitat drum is not rotated.
		if is_instance_valid(_sun):
			_sun.basis = Basis(Vector3.RIGHT, _starfield_cylinder.rotation.x) * _sun_base_basis
			# Elevation fade. Emergency and its tween own the energy while they run.
			if not _lighting_tween_active and not _emergency:
				_apply_daylight_sun_fill()
	if _probe_rebake_frames > 0 and _reflection_probe != null and is_instance_valid(_reflection_probe):
		_probe_rebake_frames -= 1
		if _probe_rebake_frames <= 0:
			_reflection_probe.update_mode = ReflectionProbe.UPDATE_ONCE
	_ff_tick_active_stalls(delta)
	_update_rfid_doors(delta)
	_sync_reticle_to_viewport_center()
	if _qa_ext_render:
		_process_qa_exterior_render()
		return
	if _batch_render:
		_process_batch_render()
		return
	if _validate_only and _frame_counter >= 4:
		get_tree().quit(0)
		return

	if _toast_t > 0.0 and _hud_toast != null:
		_toast_t -= delta
		_hud_toast.modulate.a = clampf(_toast_t / 0.6, 0.0, 1.0)
	if _scan_t > 0.0 and _hud_scan != null:
		_scan_t -= delta
		_hud_scan.modulate.a = clampf(_scan_t / 0.8, 0.0, 1.0)
		if _scan_t <= 0.0:
			_hud_scan.visible = false
	_update_hud()
	if _capture_hud:
		_process_capture_f5_hud()


func _save_qa_png(fname: String) -> Image:
	var img: Image = get_viewport().get_texture().get_image()
	if img == null or img.is_empty():
		push_warning("[PrefacePlayableArea] Empty viewport image for " + fname)
		return null
	var dir_abs: String = _resolve_path(QA_DIR)
	DirAccess.make_dir_recursive_absolute(dir_abs)
	var out: String = dir_abs + "/" + fname
	if img.save_png(out) == OK:
		print("[PrefacePlayableArea] Saved F5 HUD capture ", out)
	return img


func _process_capture_f5_hud() -> void:
	match _frame_counter:
		20:
			# [REV-C2] 1st-person inside APT 201 (open floor; the workbench objective is gone). Raise the #04 wrist ([F] pulse) so the sleeve + rings + [E] prompt are in frame.
			_third_person = false
			_player_body.rotation_degrees = Vector3(0.0, -146.0, 0.0)
			_pitch = deg_to_rad(-16.0)
			_apply_view_mode()
			_trigger_rfid_pulse()
			_arm_raise_blend = 1.0  # capture frames can outrun physics ticks; pin the raised pose
			_update_first_person_arm(0.0)
		47, 48:
			# Software-rendered capture frames take ~0.9 s each, so re-arm the 1.8 s pulse right before the grab.
			_rfid_pulse_timer = RFID_PULSE_DURATION
			_arm_raise_blend = 1.0
			_update_first_person_arm(0.0)
		50:
			_save_qa_png("qa_f5_hud_1st_person.png")
			_rfid_pulse_timer = 0.0
			_arm_raise_blend = 0.0
			_update_first_person_arm(0.0)
			# 3rd-person: Rostov on the L1 atrium concourse facing the planters, side rooms, and mezzanine.
			_player_body.global_position = Vector3(-0.60, 0.15, -4.60)
			_player_body.velocity = Vector3.ZERO
			_player_body.rotation_degrees = Vector3(0.0, 168.0, 0.0)
			_third_person = true
			_pitch = deg_to_rad(-9.0)
			_apply_view_mode()
		62:
			_trigger_rfid_pulse()
		70:
			_save_qa_png("qa_f5_hud_3rd_person.png")
			_rfid_pulse_timer = 0.0
			_arm_raise_blend = 0.0
			_update_first_person_arm(0.0)
			# Alcove 2C / L2 West Gallery looking down at the L1 atrium floor (matching Jared [t16u] angle).
			_third_person = false
			_player_body.global_position = Vector3(-9.20, 4.25, -1.80)
			_player_body.velocity = Vector3.ZERO
			_player_body.rotation_degrees = Vector3(0.0, -118.0, 0.0)
			_pitch = deg_to_rad(-24.0)
			_apply_view_mode()
		82:
			_save_qa_png("qa_f5_hud_alcove2c_atrium_lookdown.png")
			if _hud_scan != null:
				_hud_scan.visible = false
			_scan_t = 0.0
			# [REV-C2] Shot 1: Inside APT 201 showing solid bulkhead wall + Wall Diagnostic Monitor (X=-7.8, Z=2.86) + open floor (workbench removed) + clean HUD
			_third_person = false
			_player_body.global_position = Vector3(-9.15, 4.35, 5.45)
			_player_body.velocity = Vector3.ZERO
			_player_body.rotation_degrees = Vector3(0.0, -24.0, 0.0)
			_pitch = deg_to_rad(-2.0)
			_apply_view_mode()
		94:
			_save_qa_png("apt201_wall_monitor_and_clean_hud.png")
			# Shot 2: L2 corridor. The old stand at z=1.95 was the north gallery (M-41). z=0 is inside the corridor.
			_third_person = false
			_player_body.global_position = Vector3(-4.20, 4.25, 0.0)
			_player_body.velocity = Vector3.ZERO
			_player_body.rotation_degrees = Vector3(0.0, -94.0, 0.0)
			_pitch = deg_to_rad(3.0)
			_apply_view_mode()
		106:
			_save_qa_png("l2_north_gallery_unblocked.png")
			# Shot 3: Close-up of RM 1B — BOT FABRICATION & SUBSTATION flush lintel skin and Kelvin #0204 showing zero fuzzy text
			_third_person = false
			_player_body.global_position = Vector3(4.50, 0.12, 0.45)
			_player_body.velocity = Vector3.ZERO
			_player_body.rotation_degrees = Vector3(0.0, 180.0, 0.0)
			_pitch = deg_to_rad(18.0)
			_apply_view_mode()
		118:
			_save_qa_png("room1b_crisp_signage_close.png")
			# Shot 4: Looking out Sector-4 Promenade Exit and standing on exterior promenade deck looking up at full-scale Cylinder Hab-7 map
			_third_person = false
			_player_body.global_position = Vector3(0.0, 0.12, -6.50)
			_player_body.velocity = Vector3.ZERO
			_player_body.rotation_degrees = Vector3(0.0, 0.0, 0.0)
			_pitch = deg_to_rad(14.0)
			_apply_view_mode()
		130:
			_save_qa_png("cylinder_hab7_promenade_view.png")
		134:
			print("[PrefacePlayableArea] F5 HUD capture complete.")
			get_tree().quit(0)


func _process_batch_render() -> void:
	if DisplayServer.get_name() == "headless":
		get_tree().quit(0)
		return
	if _frame_counter < 6:
		return
	if _render_step >= CAMERAS.size():
		print("[PrefacePlayableArea] Completed all ", CAMERAS.size(), " open residential building renders!")
		get_tree().quit(0)
		return
	if _render_wait == 0:
		apply_camera_preset(_render_step)
		_render_wait = 1
		return
	_render_wait += 1
	if _render_wait >= 6:
		var c: Dictionary = CAMERAS[_render_step]
		var cam_name: String = String(c["name"])
		var short_alias: String = "res_cam_%02d" % (_render_step + 1)
		var img: Image = get_viewport().get_texture().get_image()
		if img != null and not img.is_empty():
			for out_dir: String in OUT_DIRS:
				var abs_dir: String = _resolve_path(out_dir)
				DirAccess.make_dir_recursive_absolute(abs_dir)
				var f1: String = abs_dir + "/" + cam_name + ".png"
				var f2: String = abs_dir + "/" + short_alias + ".png"
				if img.save_png(f1) == OK:
					print("[PrefacePlayableArea] Saved ", f1)
				img.save_png(f2)
		_render_step += 1
		_render_wait = 0


# ------------------------------------------------------------------------------
# [t31u] Automated hand-rig + controls QA  (`-- --qa-hand-controls`)
# Drives the REAL input path via Input.parse_input_event and logs PASS/FAIL lines.
# ------------------------------------------------------------------------------
func _qa_key(code: Key, pressed: bool) -> void:
	var ev: InputEventKey = InputEventKey.new()
	ev.keycode = code
	ev.physical_keycode = code
	ev.pressed = pressed
	Input.parse_input_event(ev)


func _qa_tap(code: Key) -> void:
	_qa_key(code, true)
	await _qa_idle(3)
	_qa_key(code, false)
	await _qa_idle(2)


func _qa_idle(n: int) -> void:
	# Parsed input is flushed once per idle (process) frame, which can span several physics ticks.
	for i: int in range(n):
		await get_tree().process_frame


func _qa_mouse(rel: Vector2) -> void:
	var mm: InputEventMouseMotion = InputEventMouseMotion.new()
	mm.relative = rel
	mm.screen_relative = rel
	Input.parse_input_event(mm)


func _qa_frames(n: int) -> void:
	for i: int in range(n):
		await get_tree().physics_frame


func _qa_check(nm: String, ok: bool, detail: String) -> void:
	var line: String = "%s | %s | %s" % ["PASS" if ok else "FAIL", nm, detail]
	print("[HAND-QA] ", line)
	_qa_log.append(line)
	if not ok:
		_qa_failures += 1


func _qa_place(pos: Vector3, yaw_deg: float, pitch_deg: float) -> void:
	_player_body.global_position = pos
	_player_body.velocity = Vector3.ZERO
	_player_body.rotation_degrees = Vector3(0.0, yaw_deg, 0.0)
	_pitch = deg_to_rad(pitch_deg)
	_apply_pitch()
	_update_interior_streaming(pos)


## Exterior deck spot that is not embedded in a prop. Rings of 1 m out to 12 m from preferred.
## Y is the downward-ray hit + 0.05. The capsule must be clear, with 3 m on +X/-X/+Z/-Z and 2.5 m headroom.
func _qa_find_clear_spot(preferred: Vector3) -> Vector3:
	if _player_body == null:
		return preferred
	var cs: CollisionShape3D = _player_body.get_node_or_null("PlayerCapsule") as CollisionShape3D
	if cs == null or cs.shape == null:
		return preferred
	var world: World3D = _player_body.get_world_3d()
	if world == null or world.direct_space_state == null:
		return preferred
	var space: PhysicsDirectSpaceState3D = world.direct_space_state
	var exclude: Array[RID] = [_player_body.get_rid()]
	for ring: int in range(0, 13):
		var radius: float = float(ring)
		var steps: int = 1 if ring == 0 else maxi(8, ceili(TAU * radius))
		for step: int in steps:
			var ang: float = 0.0 if steps <= 1 else TAU * float(step) / float(steps)
			var x: float = preferred.x + cos(ang) * radius
			var z: float = preferred.z + sin(ang) * radius
			# Stay on the promenade deck, inside the rails (x ±18, z -45) and outside the interior floor.
			if x < -17.0 or x > 17.0 or z < -44.0 or z > -9.6:
				continue
			var down: Dictionary = _qa_deck_ray(space, Vector3(x, 8.0, z), Vector3(x, -1.0, z), exclude)
			if down.is_empty():
				continue
			var hy: float = (down["position"] as Vector3).y
			# Reject roofs and tall props. Deck, platform, and the low guideway are in this band.
			if hy < -0.05 or hy > 0.80:
				continue
			var spot: Vector3 = Vector3(x, hy + 0.05, z)
			if _qa_spot_clear(space, cs, spot, exclude):
				return spot
	return preferred


func _qa_deck_ray(space: PhysicsDirectSpaceState3D, from: Vector3, to: Vector3, exclude: Array[RID]) -> Dictionary:
	var rq: PhysicsRayQueryParameters3D = PhysicsRayQueryParameters3D.create(from, to)
	rq.exclude = exclude
	rq.collide_with_bodies = true
	rq.collide_with_areas = false
	rq.hit_from_inside = false
	return space.intersect_ray(rq)


func _qa_spot_clear(space: PhysicsDirectSpaceState3D, cs: CollisionShape3D, spot: Vector3, exclude: Array[RID]) -> bool:
	var q: PhysicsShapeQueryParameters3D = PhysicsShapeQueryParameters3D.new()
	q.shape = cs.shape
	q.transform = Transform3D(Basis.IDENTITY, spot) * cs.transform
	q.exclude = exclude
	q.collide_with_bodies = true
	q.collide_with_areas = false
	if not space.intersect_shape(q, 1).is_empty():
		return false
	# cast_motion moves the player's capsule. -Z is the yaw-0 sprint (~2.7 m over 20 frames).
	var motions: Array[Vector3] = [
		Vector3(3.0, 0.0, 0.0), Vector3(-3.0, 0.0, 0.0),
		Vector3(0.0, 0.0, 3.0), Vector3(0.0, 0.0, -3.0),
		Vector3(0.0, 2.5, 0.0),
	]
	for motion: Vector3 in motions:
		q.motion = motion
		var frac: PackedFloat32Array = space.cast_motion(q)
		if frac.is_empty() or frac[0] < 0.999:
			return false
	return true


## Yaw 0 faces world -Z. Pitch is the camera pivot X rotation (negative looks down).
func _qa_aim_at(target: Vector3) -> void:
	if _player_body == null:
		return
	var eye: Vector3 = _player_body.global_position + Vector3(0.0, 1.62, 0.0)
	if _camera != null and _camera.is_inside_tree():
		eye = _camera.global_position
	var dir: Vector3 = target - eye
	var horiz: float = Vector2(dir.x, dir.z).length()
	if horiz < 0.00001 and absf(dir.y) < 0.00001:
		return
	# forward = (-sin(yaw), 0, -cos(yaw)); yaw 0 is -Z, yaw 180 is +Z.
	var yaw: float = atan2(-dir.x, -dir.z)
	var pitch: float = atan2(dir.y, maxf(horiz, 0.00001))
	_player_body.rotation_degrees = Vector3(0.0, rad_to_deg(yaw), 0.0)
	_player_body.velocity = Vector3.ZERO
	_pitch = pitch
	_apply_pitch()


## Door-local point, shifted with the hub (local -Z seat and local +X tangent) so [E] range stays put.
func _qa_follow_hub_seat(door: Dictionary, local_pt: Vector3) -> Vector3:
	var pt: Vector3 = local_pt
	pt.x += float(door.get("hub_tangent_shift", 0.0))
	pt.z -= float(door.get("hub_seat", 0.0))
	var root: Node3D = door["root"] as Node3D
	return root.global_transform * pt


func _qa_capture(fname: String) -> Image:
	if DisplayServer.get_name() == "headless":
		return null
	await RenderingServer.frame_post_draw
	return _save_qa_png(fname)


func _qa_hand_row(frame: int) -> String:
	var hl: Transform3D = _hand_body_local()
	return "| %3d | %6.3f | %+6.3f | %+7.3f | %7.2f | %6.2f |" % [frame, _walk_phase, sin(_walk_phase) * _walk_swing_amp, hl.origin.z, rad_to_deg(hl.basis.get_euler().x), _walk_swing_amp]


func _run_hand_controls_qa() -> void:
	if _player_body == null or _camera == null or _fp_wrist_holder == null:
		_qa_check("setup", false, "player/camera/wrist missing")
		get_tree().quit(1)
		return
	if _hud_toast != null:
		_hud_toast.visible = false
	_third_person = false
	_apply_view_mode()
	await _qa_frames(10)

	# --- 1. Neutral straight-ahead: hand 100% out of view (Promenade deck, open space) ---
	_qa_place(Vector3(0.0, 0.25, -12.0), 0.0, -4.0)
	await _qa_frames(30)
	_qa_check("floor_contact", _player_body.is_on_floor(), "is_on_floor=%s y=%.3f" % [_player_body.is_on_floor(), _player_body.global_position.y])
	var vis_neutral: int = _hand_points_in_view()
	_qa_check("neutral_hand_out_of_view", vis_neutral == 0 and _arm_raise_blend == 0.0, "pitch=-4 blend=%.2f hand_pts_in_frustum=%d/%d" % [_arm_raise_blend, vis_neutral, _wrist_world_points().size()])
	_qa_check("pulse_rings_hidden_idle", _pulse_rings_root != null and not _pulse_rings_root.visible, "PulseRings.visible=%s" % [_pulse_rings_root.visible if _pulse_rings_root != null else "null"])
	await _qa_capture("hand_qa_01_neutral_out_of_view.png")
	for pd: float in [-12.0, -20.0]:
		_qa_place(_player_body.global_position, 0.0, pd)
		await _qa_frames(3)
		_qa_check("standing_hand_out_of_view_pitch_%d" % int(pd), _hand_points_in_view() == 0, "pitch=%d pts_in_frustum=%d" % [int(pd), _hand_points_in_view()])

	# --- 2. Mouse look (yaw + pitch clamps -80..+75) ---
	_qa_place(_player_body.global_position, 0.0, -4.0)
	await _qa_frames(2)
	var yaw0: float = _player_body.rotation.y
	_qa_mouse(Vector2(200.0, 0.0))
	await _qa_idle(3)
	var dyaw: float = rad_to_deg(_player_body.rotation.y - yaw0)
	_qa_check("mouse_yaw", absf(dyaw - rad_to_deg(-200.0 * MOUSE_SENS)) < 0.5, "dyaw=%.2f deg (expected %.2f)" % [dyaw, rad_to_deg(-200.0 * MOUSE_SENS)])
	_qa_mouse(Vector2(0.0, -6000.0))
	await _qa_idle(3)
	_qa_check("mouse_pitch_clamp_up", absf(rad_to_deg(_pitch) - PITCH_MAX_DEG) < 0.05, "pitch=%.2f" % rad_to_deg(_pitch))
	_qa_mouse(Vector2(0.0, 12000.0))
	await _qa_idle(3)
	_qa_check("mouse_pitch_clamp_down", absf(rad_to_deg(_pitch) - PITCH_MIN_DEG) < 0.05, "pitch=%.2f" % rad_to_deg(_pitch))
	_qa_place(Vector3(0.0, 0.25, -11.0), 0.0, -4.0)
	await _qa_frames(10)
	_qa_mouse(Vector2(0.0, deg_to_rad(48.0) / MOUSE_SENS))
	await _qa_idle(3)
	_qa_check("mouse_pitch_look_down", absf(rad_to_deg(_pitch) + 52.0) < 0.2, "pitch=%.2f (target -52)" % rad_to_deg(_pitch))

	# --- 3. W walk + sinusoidal arm swing table (looking down -52 deg) ---
	var p0: Vector3 = _player_body.global_position
	_walk_phase = 0.0
	_qa_key(KEY_W, true)
	var table: PackedStringArray = PackedStringArray()
	table.append("| frame | walk_phase | swing_s | hand_body_local_z | hand_pitch_deg | amp |")
	table.append("|---|---|---|---|---|---|")
	var max_err: float = 0.0
	var z_min: float = 10.0
	var z_max: float = -10.0
	var vis_fwd: int = 0
	var vis_back: int = 0
	for f: int in range(72):
		await _qa_frames(1)
		table.append(_qa_hand_row(f))
		var hl: Transform3D = _hand_body_local()
		var s_now: float = sin(_walk_phase) * _walk_swing_amp
		var expect_z: float = ARM_LOWERED_POS.z - s_now * WALK_SWING_Z
		max_err = maxf(max_err, absf(hl.origin.z - expect_z))
		z_min = minf(z_min, hl.origin.z)
		z_max = maxf(z_max, hl.origin.z)
		if s_now > 0.95:
			vis_fwd = max(vis_fwd, _hand_points_in_view())
		elif s_now < -0.95:
			vis_back = max(vis_back, _hand_points_in_view())
	var walk_speed: float = Vector2(_player_body.velocity.x, _player_body.velocity.z).length()
	_qa_key(KEY_W, false)
	var disp: Vector3 = _player_body.global_position - p0
	# Deterministic 1920x1080 captures at the exact forward (+1.0) and backward (-1.0) extrema of the swing cycle.
	_walk_swing_amp = 1.0
	_walk_phase = PI * 0.5
	_update_first_person_arm(0.0)
	vis_fwd = max(vis_fwd, _hand_points_in_view())
	var img_fwd: Image = await _qa_capture("hand_qa_02a_look_down_swing_forward.png")
	_walk_swing_amp = 1.0
	_walk_phase = PI * 1.5
	_update_first_person_arm(0.0)
	vis_back = max(vis_back, _hand_points_in_view())
	var img_back: Image = await _qa_capture("hand_qa_02b_look_down_swing_back.png")
	var got_fwd: bool = true
	var got_back: bool = true
	_qa_check("W_forward_move", disp.z < -3.0 and absf(disp.x) < 0.3, "disp=(%.2f, %.2f, %.2f) speed=%.2f m/s" % [disp.x, disp.y, disp.z, walk_speed])
	_qa_check("walk_speed", absf(walk_speed - WALK_SPEED) < 0.1, "%.2f m/s (expected %.1f)" % [walk_speed, WALK_SPEED])
	_qa_check("arm_swing_sinusoidal", max_err < 0.004, "max |z - (z0 - sin(phase)*amp*0.22)| = %.5f m over 96 frames" % max_err)
	_qa_check("arm_swing_range", z_min < -0.47 and z_max > -0.09, "hand_body_local_z range [%.3f, %.3f] m" % [z_min, z_max])
	_qa_check("look_down_swing_forward_visible", got_fwd and vis_fwd > 0, "captured=%s pts_in_frustum=%d" % [got_fwd, vis_fwd])
	_qa_check("look_down_swing_back_visible", got_back and vis_back > 0, "captured=%s pts_in_frustum=%d" % [got_back, vis_back])
	_qa_check("no_rings_while_walking", not _pulse_rings_root.visible, "PulseRings.visible=%s" % _pulse_rings_root.visible)
	if img_fwd != null and img_back != null:
		var combo: Image = Image.create(1920, 1080, false, img_fwd.get_format())
		combo.blit_rect(img_fwd, Rect2i(300, 0, 960, 1080), Vector2i(0, 0))
		combo.blit_rect(img_back, Rect2i(300, 0, 960, 1080), Vector2i(960, 0))
		combo.fill_rect(Rect2i(958, 0, 4, 1080), Color(0.9, 0.95, 1.0, 1.0))
		combo.save_png(_resolve_path(QA_DIR) + "/hand_qa_02_look_down_walking_swing.png")
		print("[PrefacePlayableArea] Saved combined swing comparison")

	# --- 4. Stop: swing amplitude eases back to 0 ---
	await _qa_frames(30)
	var hl_stop: Transform3D = _hand_body_local()
	_qa_check("stop_swing_eases_out", _walk_swing_amp < 0.001 and absf(hl_stop.origin.z - ARM_LOWERED_POS.z) < 0.002, "amp=%.3f z=%.3f" % [_walk_swing_amp, hl_stop.origin.z])

	# --- 5. Shift sprint, A / S / D strafe ---
	var move_spot: Vector3 = _qa_find_clear_spot(Vector3(-4.0, 0.12, -12.0))
	_qa_place(move_spot, 0.0, -4.0)
	await _qa_frames(10)
	_qa_key(KEY_SHIFT, true)
	_qa_key(KEY_W, true)
	await _qa_frames(20)
	var ph_a: float = _walk_phase
	await _qa_frames(1)
	var dph: float = fposmod(_walk_phase - ph_a, TAU) * 60.0
	var sp: float = Vector2(_player_body.velocity.x, _player_body.velocity.z).length()
	_qa_key(KEY_W, false)
	_qa_key(KEY_SHIFT, false)
	_qa_check("shift_sprint", absf(sp - SPRINT_SPEED) < 0.1 and absf(dph - 8.6) < 0.2, "speed=%.2f m/s swing_freq=%.2f rad/s" % [sp, dph])
	for kd: Array in [[KEY_A, Vector3(-1, 0, 0), "A_strafe_left"], [KEY_D, Vector3(1, 0, 0), "D_strafe_right"], [KEY_S, Vector3(0, 0, 1), "S_backpedal"]]:
		_qa_place(move_spot, 0.0, -4.0)
		await _qa_frames(8)
		var q0: Vector3 = _player_body.global_position
		_qa_key(kd[0] as Key, true)
		await _qa_frames(20)
		_qa_key(kd[0] as Key, false)
		var dq: Vector3 = _player_body.global_position - q0
		dq.y = 0.0
		var dirn: Vector3 = kd[1] as Vector3
		_qa_check(String(kd[2]), dq.length() > 1.0 and dq.normalized().dot(dirn) > 0.98, "disp=(%.2f, %.2f)" % [dq.x, dq.z])
	await _qa_frames(10)

	# --- 6. Space jump ---
	var y0: float = _player_body.global_position.y
	var y_peak: float = y0
	_qa_key(KEY_SPACE, true)
	await _qa_idle(3)
	_qa_key(KEY_SPACE, false)
	var landed: bool = false
	for jf: int in range(90):
		await _qa_frames(1)
		y_peak = maxf(y_peak, _player_body.global_position.y)
		if jf > 10 and _player_body.is_on_floor():
			landed = true
			break
	_qa_check("space_jump", y_peak - y0 > 0.9 and landed, "rise=%.2f m landed=%s" % [y_peak - y0, landed])

	# --- 7. [F] wrist raise + RFID PulseRings (APT 201 open floor) ---
	# [REV-C2] The workbench objective is gone. This spot stays on open floor east of the dust outline.
	_qa_place(Vector3(-8.50, 4.30, 6.35), 180.0, -14.0)
	await _qa_frames(30)
	_qa_check("apt201_lowered_out_of_view", _hand_points_in_view() == 0 and not _pulse_rings_root.visible, "pts_in_frustum=%d rings=%s" % [_hand_points_in_view(), _pulse_rings_root.visible])
	await _qa_capture("hand_qa_00_apt201_lowered_reference.png")
	await _qa_tap(KEY_F)
	await _qa_frames(30)
	var vis_raised: int = _hand_points_in_view()
	_qa_check("F_raise_blend", _arm_raise_blend > 0.999, "blend=%.3f pulse_timer=%.2f" % [_arm_raise_blend, _rfid_pulse_timer])
	_qa_check("F_hand_in_view", vis_raised > 0, "pts_in_frustum=%d" % vis_raised)
	_qa_check("F_pulse_rings_visible", _pulse_rings_root.visible, "PulseRings.visible=%s" % _pulse_rings_root.visible)
	await _qa_capture("hand_qa_03_raised_wrist_rfid_pulse.png")
	await _qa_frames(130)
	_qa_check("F_pulse_ends_rings_hidden", not _pulse_rings_root.visible and _rfid_pulse_timer == 0.0, "rings=%s timer=%.2f" % [_pulse_rings_root.visible, _rfid_pulse_timer])
	await _qa_frames(40)
	_qa_check("F_arm_lowers_after_pulse", _arm_raise_blend == 0.0 and _hand_points_in_view() == 0, "blend=%.2f pts=%d" % [_arm_raise_blend, _hand_points_in_view()])
	_qa_key(KEY_F, true)
	await _qa_frames(40)
	var held_blend: float = _arm_raise_blend
	await _qa_frames(120)
	_qa_check("F_hold_keeps_raised", held_blend > 0.999 and _arm_raise_blend > 0.999, "blend after 2.7s hold=%.3f" % _arm_raise_blend)
	_qa_key(KEY_F, false)
	await _qa_frames(40)

	# --- 8. [E] interact reach + pickup removal ---
	# Rev C.2 removed the APT 201 workbench pickups. This uses the 202 desk cell.
	# Stand 0.75 m on its +Z side. Yaw 0 faces -Z, toward the pickup.
	var wall_pick: Node3D = _props_container.get_node_or_null("Apt202_Desk_Battery_Cell") as Node3D
	var wall_aim: Vector3 = wall_pick.global_position if wall_pick != null else Vector3(10.70, 5.10, 7.20)
	_qa_place(Vector3(wall_aim.x, 4.30, wall_aim.z + 0.75), 0.0, 0.0)
	await _qa_frames(8)
	if wall_pick != null and is_instance_valid(wall_pick):
		wall_aim = wall_pick.global_position
	_qa_place(Vector3(wall_aim.x, 4.30, wall_aim.z + 0.75), 0.0, 0.0)
	_qa_aim_at(wall_aim)
	# Place leaves a few frames of slide, and [E] is parsed on a later idle frame. Sample nearest only after that slide stops,
	# or the node this check waits on is a different pickup than the one _interact queue_frees.
	await _qa_frames(8)
	_qa_aim_at(wall_aim)
	_player_body.velocity = Vector3.ZERO
	var n_before: int = 0
	for it: Dictionary in _interactables:
		if bool(it["pickup"]) and not bool(it["collected"]):
			n_before += 1
	var target: Dictionary = _find_nearest_interactable(INTERACT_RANGE)
	var tgt_node: Node3D = target.get("node", null) as Node3D
	var tgt_id: String = String(target.get("id", ""))
	var tgt_label: String = String(target.get("label", "none"))
	var inv_before: int = 0
	for k: String in _inventory.keys():
		inv_before += int(_inventory[k])
	var collected_before: Dictionary = {}
	for cid: String in _collected_pickup_ids.keys():
		collected_before[cid] = true
	_qa_key(KEY_E, true)
	await _qa_idle(1)
	await _qa_frames(12)
	var reach_blend: float = _arm_raise_blend
	_qa_key(KEY_E, false)
	await _qa_frames(2)
	var n_after: int = 0
	for it2: Dictionary in _interactables:
		if bool(it2["pickup"]) and not bool(it2["collected"]):
			n_after += 1
	var inv_after: int = 0
	for k2: String in _inventory.keys():
		inv_after += int(_inventory[k2])
	var new_ids: PackedStringArray = PackedStringArray()
	for cid2: String in _collected_pickup_ids.keys():
		if not collected_before.has(cid2):
			new_ids.append(cid2)
	var collected_id: String = ",".join(new_ids)
	# queue_free drops the pickup at the end of an idle frame. A physics-frame check can still see it.
	# Removed-from-tree counts as freed. Gameplay (queue_free in _interact) is unchanged.
	var node_freed: bool = tgt_node == null or not is_instance_valid(tgt_node) or not tgt_node.is_inside_tree()
	var freed_wait: int = 0
	while not node_freed and freed_wait < 10:
		await get_tree().process_frame
		freed_wait += 1
		node_freed = tgt_node == null or not is_instance_valid(tgt_node) or not tgt_node.is_inside_tree()
	_qa_check("E_pickup_collected_removed", n_after == n_before - 1 and inv_after == inv_before + 1 and node_freed and collected_id == tgt_id and tgt_id != "", "target=%s target_id=%s collected_id=%s pickups %d->%d inventory %d->%d node_freed=%s" % [tgt_label, tgt_id, collected_id, n_before, n_after, inv_before, inv_after, node_freed])
	_qa_check("E_reach_raises_arm", reach_blend > 0.5, "blend 12 physics frames after [E]=%.2f" % reach_blend)
	await _qa_frames(60)
	_qa_check("E_reach_lowers_again", _arm_raise_blend == 0.0, "blend=%.2f" % _arm_raise_blend)

	# --- 9. [V] view toggle & [R] flashlight ---
	await _qa_tap(KEY_V)
	await _qa_frames(3)
	_qa_check("V_third_person", _third_person and not _fp_wrist_holder.visible and _spring_arm.spring_length > 3.0, "third=%s wrist_visible=%s arm=%.1f" % [_third_person, _fp_wrist_holder.visible, _spring_arm.spring_length])
	await _qa_tap(KEY_V)
	await _qa_frames(3)
	_qa_check("V_back_to_first_person", not _third_person and _fp_wrist_holder.visible and _spring_arm.spring_length == 0.0, "third=%s wrist_visible=%s" % [_third_person, _fp_wrist_holder.visible])
	await _qa_tap(KEY_R)
	_qa_check("R_flashlight_on", _flashlight != null and _flashlight.visible, "visible=%s" % _flashlight.visible)
	await _qa_tap(KEY_R)
	_qa_check("R_flashlight_off", _flashlight != null and not _flashlight.visible, "visible=%s" % _flashlight.visible)

	# --- Report ---
	var out: PackedStringArray = PackedStringArray()
	out.append("# Hand-rig & controls QA log ([t31u])")
	out.append("display=%s  failures=%d" % [DisplayServer.get_name(), _qa_failures])
	out.append("")
	out.append_array(_qa_log)
	out.append("")
	out.append("## Sinusoidal arm swing — W walk, pitch -52 deg (physics 60 Hz)")
	out.append_array(table)
	var dir_abs: String = _resolve_path(QA_DIR)
	DirAccess.make_dir_recursive_absolute(dir_abs)
	var fn: String = dir_abs + ("/hand_controls_qa_log_headless.md" if DisplayServer.get_name() == "headless" else "/hand_controls_qa_log.md")
	var fa: FileAccess = FileAccess.open(fn, FileAccess.WRITE)
	if fa != null:
		fa.store_string("\n".join(out) + "\n")
		fa.close()
	print("[HAND-QA] DONE failures=", _qa_failures, " log=", fn)
	get_tree().quit(1 if _qa_failures > 0 else 0)


# ------------------------------------------------------------------------------
# [t34u] Cylinder radial spin gravity: 360 deg walkable ring, planted boxes, Coriolis core transit
#   Gravity inside the ring = radial_outward * g * (rho / R)  (spin-gravity profile, 1 g at the floor)
#   Local up = -radial_outward (toward the cylinder axis). Crossing the axis flips it to the opposite floor.
# ------------------------------------------------------------------------------
var _last_transit_report: Dictionary = {}
var _last_box_transit_report: Dictionary = {}


func _ring_radial(p: Vector3) -> Vector3:
	var d: Vector3 = p - RING_CENTER
	return d - RING_AXIS * d.dot(RING_AXIS)


func _ring_rho(p: Vector3) -> float:
	return _ring_radial(p).length()


func _ring_theta_deg(p: Vector3) -> float:
	var r: Vector3 = _ring_radial(p)
	return fposmod(rad_to_deg(atan2(r.x, -r.y)), 360.0)


func _in_gravity_ring(p: Vector3) -> bool:
	if _ring_root == null:
		return false
	var along: float = (p - RING_CENTER).dot(RING_AXIS)
	return absf(along) < RING_LENGTH * 0.5 + 0.5 and _ring_rho(p) < RING_RADIUS + 1.5


func _ring_up_at(p: Vector3, fallback: Vector3) -> Vector3:
	var r: Vector3 = _ring_radial(p)
	if r.length() < 0.03:
		return fallback
	return -r.normalized()


func _ring_gravity_at(p: Vector3) -> Vector3:
	var r: Vector3 = _ring_radial(p)
	var rho: float = r.length()
	if rho < 0.001:
		return Vector3.ZERO
	return (r / rho) * GRAVITY * clampf(rho / RING_RADIUS, 0.0, 1.2)


func _ring_floor_point(theta_deg: float, z: float, inset: float) -> Vector3:
	var th: float = deg_to_rad(theta_deg)
	var outward: Vector3 = Vector3(sin(th), -cos(th), 0.0)
	return RING_CENTER + outward * (RING_RADIUS - inset) + RING_AXIS * z


func _ring_frame(theta_deg: float) -> Basis:
	# y = local up (toward axis), -z = walking tangent (increasing theta), x = y cross z.
	var th: float = deg_to_rad(theta_deg)
	var up: Vector3 = -Vector3(sin(th), -cos(th), 0.0)
	var tang: Vector3 = Vector3(cos(th), sin(th), 0.0)
	return Basis(up.cross(-tang), up, -tang)


func _orient_node_to_up(n: Node3D, up: Vector3, delta: float) -> float:
	# Minimal-arc rotation of the node basis so basis.y -> up, rate-limited for smoothness. Returns step (rad).
	var gb: Basis = n.global_basis.orthonormalized()
	var cur: Vector3 = gb.y
	var d: float = clampf(cur.dot(up), -1.0, 1.0)
	if d > 0.9999999:
		return 0.0
	var axis: Vector3 = cur.cross(up)
	if axis.length_squared() < 1e-10:
		axis = RING_AXIS  # exact 180 deg flip at the core: roll around the cylinder axis
	var ang: float = acos(d)
	var step: float = minf(ang, RING_ORIENT_RATE * delta) if delta > 0.0 else ang
	n.global_basis = (Basis(axis.normalized(), step) * gb).orthonormalized()
	return step


func _ring_mat(col: Color, emissive: float = 0.0, alpha: float = 1.0) -> StandardMaterial3D:
	var m: StandardMaterial3D = StandardMaterial3D.new()
	m.albedo_color = Color(col.r, col.g, col.b, alpha)
	m.roughness = 0.55
	m.metallic = 0.25
	m.cull_mode = BaseMaterial3D.CULL_DISABLED
	if alpha < 1.0:
		m.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
	if emissive > 0.0:
		m.emission_enabled = true
		m.emission = col
		m.emission_energy_multiplier = emissive
	return m


func _build_cylinder_gravity_ring(parent: Node3D) -> void:
	_ring_root = Node3D.new()
	_ring_root.name = "CylinderSpinGravityTestRing"
	parent.add_child(_ring_root)
	_ring_root.global_position = RING_CENTER

	# 1. Collision: 72 tangent floor tiles (inner faces at rho = R) + 2 end-cap discs.
	var body: StaticBody3D = StaticBody3D.new()
	body.name = "RingFloorColliders"
	_ring_root.add_child(body)
	var seg_w: float = 2.0 * RING_RADIUS * tan(PI / float(RING_SEGMENTS)) * 1.04
	for i: int in range(RING_SEGMENTS):
		var th: float = deg_to_rad(360.0 * float(i) / float(RING_SEGMENTS))
		var outward: Vector3 = Vector3(sin(th), -cos(th), 0.0)
		var cs: CollisionShape3D = CollisionShape3D.new()
		cs.name = "FloorTile_%02d" % i
		var bs: BoxShape3D = BoxShape3D.new()
		bs.size = Vector3(seg_w, 0.6, RING_LENGTH + 1.0)
		cs.shape = bs
		cs.transform = Transform3D(Basis(Vector3(cos(th), sin(th), 0.0), -outward, RING_AXIS), outward * (RING_RADIUS + 0.3))
		body.add_child(cs)
	for sgn: float in [-1.0, 1.0]:
		var cap: CollisionShape3D = CollisionShape3D.new()
		cap.name = "EndCap_%s" % ("North" if sgn > 0.0 else "South")
		var cyl: CylinderShape3D = CylinderShape3D.new()
		cyl.radius = RING_RADIUS + 0.8
		cyl.height = 0.5
		cap.shape = cyl
		cap.transform = Transform3D(Basis(Vector3.RIGHT, PI * 0.5), RING_AXIS * sgn * (RING_LENGTH * 0.5 + 0.25))
		body.add_child(cap)

	# 2. Visuals: deck shell, angle stripes (0/90/180/270 coloured), seams every 15 deg, end walls.
	var shell: MeshInstance3D = MeshInstance3D.new()
	shell.name = "RingDeckShell"
	var cm: CylinderMesh = CylinderMesh.new()
	cm.top_radius = RING_RADIUS + 0.01
	cm.bottom_radius = RING_RADIUS + 0.01
	cm.height = RING_LENGTH
	cm.radial_segments = RING_SEGMENTS
	cm.rings = 1
	cm.cap_top = false
	cm.cap_bottom = false
	shell.mesh = cm
	shell.rotation = Vector3(PI * 0.5, 0.0, 0.0)
	var deck: StandardMaterial3D = _ring_mat(Color(0.42, 0.46, 0.52))
	var deck_tex: Texture2D = _load_tex("mat_deck_floor_albedo.png")
	if deck_tex != null:
		deck.albedo_texture = deck_tex
		deck.albedo_color = Color(0.8, 0.82, 0.86)
		deck.uv1_scale = Vector3(24.0, 8.0, 1.0)
	shell.material_override = deck
	shell.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	_ring_root.add_child(shell)
	var marker_cols: Dictionary = {0: Color("#2E96B2"), 90: Color("#C47D2B"), 180: Color("#7B5CFF"), 270: Color("#3FAF6A")}
	for k: int in range(24):
		var th_m: int = k * 15
		var big: bool = marker_cols.has(th_m)
		var stripe: MeshInstance3D = MeshInstance3D.new()
		stripe.name = "AngleStripe_%03d" % th_m
		var sb: BoxMesh = BoxMesh.new()
		sb.size = Vector3(0.7 if big else 0.08, 0.02, RING_LENGTH - 0.2)
		stripe.mesh = sb
		var thr: float = deg_to_rad(float(th_m))
		var outw: Vector3 = Vector3(sin(thr), -cos(thr), 0.0)
		stripe.transform = Transform3D(Basis(Vector3(cos(thr), sin(thr), 0.0), -outw, RING_AXIS), outw * (RING_RADIUS - 0.005))
		stripe.material_override = _ring_mat(marker_cols[th_m] if big else Color(0.12, 0.14, 0.17), 0.9 if big else 0.0)
		stripe.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
		_ring_root.add_child(stripe)
	for sgn2: float in [-1.0, 1.0]:
		var wall: MeshInstance3D = MeshInstance3D.new()
		wall.name = "EndWall_%s" % ("North" if sgn2 > 0.0 else "South")
		var wm: CylinderMesh = CylinderMesh.new()
		wm.top_radius = RING_RADIUS + 0.02
		wm.bottom_radius = RING_RADIUS + 0.02
		wm.height = 0.1
		wm.radial_segments = RING_SEGMENTS
		wall.mesh = wm
		wall.transform = Transform3D(Basis(Vector3.RIGHT, PI * 0.5), RING_AXIS * sgn2 * (RING_LENGTH * 0.5))
		var wmat: StandardMaterial3D = _ring_mat(Color(0.62, 0.66, 0.72), 0.25)
		if deck_tex != null:
			wmat.albedo_texture = deck_tex
			wmat.uv1_scale = Vector3(6.0, 6.0, 1.0)
		wall.material_override = wmat
		wall.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
		_ring_root.add_child(wall)
		var trim: MeshInstance3D = MeshInstance3D.new()
		trim.name = "EndWallLightTrim_%s" % ("North" if sgn2 > 0.0 else "South")
		var trm: TorusMesh = TorusMesh.new()
		trm.inner_radius = RING_RADIUS - 0.18
		trm.outer_radius = RING_RADIUS - 0.02
		trm.rings = 96
		trim.mesh = trm
		trim.transform = Transform3D(Basis(Vector3.RIGHT, PI * 0.5), RING_AXIS * sgn2 * (RING_LENGTH * 0.5 - 0.1))
		trim.material_override = _ring_mat(Color("#F2ECE0"), 1.2)
		trim.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
		_ring_root.add_child(trim)

	# 3. Coriolis core transit shaft along the theta 0 <-> 180 diameter at z = RING_SHAFT_Z.
	var shaft: MeshInstance3D = MeshInstance3D.new()
	shaft.name = "CoriolisCoreTransitShaft"
	var shm: CylinderMesh = CylinderMesh.new()
	shm.top_radius = 1.05
	shm.bottom_radius = 1.05
	shm.height = RING_RADIUS * 2.0 - 0.1
	shm.cap_top = false
	shm.cap_bottom = false
	shaft.mesh = shm
	shaft.position = RING_AXIS * RING_SHAFT_Z
	shaft.material_override = _ring_mat(Color(0.45, 0.85, 1.0), 0.25, 0.16)
	shaft.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	_ring_root.add_child(shaft)
	for rail_x: float in [-1.0, 1.0]:
		var rail: MeshInstance3D = MeshInstance3D.new()
		rail.name = "ShaftGuideRail_%s" % ("W" if rail_x < 0.0 else "E")
		var rbm: BoxMesh = BoxMesh.new()
		rbm.size = Vector3(0.08, RING_RADIUS * 2.0 - 0.1, 0.08)
		rail.mesh = rbm
		rail.position = RING_AXIS * RING_SHAFT_Z + Vector3(rail_x * 1.08, 0.0, 0.0)
		rail.material_override = _ring_mat(Color(0.75, 0.78, 0.82))
		_ring_root.add_child(rail)
	var core: MeshInstance3D = MeshInstance3D.new()
	core.name = "CoriolisCoreRing"
	var tm: TorusMesh = TorusMesh.new()
	tm.inner_radius = 1.15
	tm.outer_radius = 1.35
	core.mesh = tm
	core.position = RING_AXIS * RING_SHAFT_Z
	core.material_override = _ring_mat(Color("#2E96B2"), 1.4)
	_ring_root.add_child(core)
	for pad_th: float in [0.0, 180.0]:
		var pad: MeshInstance3D = MeshInstance3D.new()
		pad.name = "CoreLiftPad_%03d" % int(pad_th)
		var pm: CylinderMesh = CylinderMesh.new()
		pm.top_radius = 1.0
		pm.bottom_radius = 1.0
		pm.height = 0.04
		pad.mesh = pm
		var pr: float = deg_to_rad(pad_th)
		var po: Vector3 = Vector3(sin(pr), -cos(pr), 0.0)
		pad.transform = Transform3D(Basis(Vector3(cos(pr), sin(pr), 0.0), -po, RING_AXIS), po * (RING_RADIUS - 0.02) + RING_AXIS * RING_SHAFT_Z)
		pad.material_override = _ring_mat(COLOR_AMBER, 0.8)
		_ring_root.add_child(pad)

	# 4. Lighting along the cylinder axis.
	for lz: float in [-6.0, 0.0, 6.0]:
		var om: OmniLight3D = OmniLight3D.new()
		om.name = "RingAxisLight_%d" % int(lz)
		om.position = RING_AXIS * lz
		om.light_color = Color("#F2ECE0")
		om.light_energy = 1.6
		om.omni_range = 15.0
		om.shadow_enabled = false
		_ring_root.add_child(om)

	# 5. Physical boxes around the full ring + a core-transit test box on the theta 0 lift pad.
	var box_cols: Array = [Color("#D95B26"), Color("#2E96B2"), Color("#C47D2B"), Color("#7B5CFF"), Color("#3FAF6A"), Color("#E0C060"), Color("#B03A48"), Color("#8C98A4")]
	for bi: int in range(8):
		_spawn_ring_box("RingBox_%03d" % (bi * 45), float(bi * 45), RING_BOX_Z, box_cols[bi])
	_spawn_ring_box("CoreTransitBox", 0.0, RING_SHAFT_Z - 0.55, Color("#F2F2F2"))


func _spawn_ring_box(nm: String, theta_deg: float, z: float, col: Color) -> RigidBody3D:
	var rb: RigidBody3D = RigidBody3D.new()
	rb.name = nm
	rb.mass = 20.0
	rb.gravity_scale = 0.0  # custom radial spin gravity applied in _apply_ring_box_gravity()
	rb.can_sleep = false
	rb.continuous_cd = true
	rb.linear_damp = 0.05
	rb.angular_damp = 0.5
	var cs: CollisionShape3D = CollisionShape3D.new()
	var bs: BoxShape3D = BoxShape3D.new()
	bs.size = Vector3.ONE * RING_BOX_SIZE
	cs.shape = bs
	rb.add_child(cs)
	var mi: MeshInstance3D = MeshInstance3D.new()
	var bm: BoxMesh = BoxMesh.new()
	bm.size = Vector3.ONE * RING_BOX_SIZE
	mi.mesh = bm
	mi.material_override = _ring_mat(col, 0.15)
	rb.add_child(mi)
	_ring_root.add_child(rb)
	rb.global_transform = Transform3D(_ring_frame(theta_deg), _ring_floor_point(theta_deg, z, RING_BOX_SIZE * 0.5 + 0.02))
	_gravity_boxes.append({"body": rb, "home_theta": theta_deg, "rest_t": 0.0})
	return rb


func _is_transiting(n: Node3D) -> bool:
	for tr: Dictionary in _core_transits:
		if tr["node"] == n:
			return true
	return false


func _apply_ring_box_gravity(delta: float) -> void:
	for bx: Dictionary in _gravity_boxes:
		var rb: RigidBody3D = bx["body"] as RigidBody3D
		if rb == null or not is_instance_valid(rb) or rb.freeze:
			continue
		rb.apply_central_force(_ring_gravity_at(rb.global_position) * rb.mass)
		# A box left resting on a lift pad for 1.5 s rides the Coriolis core lift to the opposite floor.
		if _qa_cyl:
			continue
		var on_pad: bool = false
		for pt: float in [0.0, 180.0]:
			if rb.global_position.distance_to(_ring_floor_point(pt, RING_SHAFT_Z, RING_BOX_SIZE * 0.5)) < 0.9:
				on_pad = true
		var rt: float = float(bx["rest_t"])
		if on_pad and rb.linear_velocity.length() < 0.1 and rt >= 0.0:
			rt += delta
			if rt > 1.5:
				rt = -6.0  # cooldown after arrival so it does not immediately bounce back
				_start_core_transit(rb, false)
		elif rt > 0.0:
			rt = 0.0
		elif rt < 0.0:
			rt = minf(rt + delta, 0.0)
		bx["rest_t"] = rt


func _start_core_transit(n: Node3D, is_player: bool) -> bool:
	if n == null or _ring_root == null or _is_transiting(n) or not _in_gravity_ring(n.global_position):
		return false
	var inset: float = -RING_FEET_OFFSET if is_player else RING_BOX_SIZE * 0.5 + 0.02
	var pad_a: Vector3 = _ring_floor_point(0.0, RING_SHAFT_Z, inset)
	var pad_b: Vector3 = _ring_floor_point(180.0, RING_SHAFT_Z, inset)
	var p: Vector3 = n.global_position
	var from_a: bool = p.distance_to(pad_a) <= p.distance_to(pad_b)
	var start_pad: Vector3 = pad_a if from_a else pad_b
	if p.distance_to(start_pad) > CORE_PAD_RADIUS:
		return false
	var tr: Dictionary = {
		"node": n, "is_player": is_player, "t": 0.0, "dur": CORE_TRANSIT_DURATION,
		"start": p, "from": start_pad, "to": pad_b if from_a else pad_a,
		"last_up": n.global_basis.y, "min_rho": 1e9, "max_step": 0.0, "flipped": false,
	}
	if not is_player:
		var rb: RigidBody3D = n as RigidBody3D
		rb.freeze_mode = RigidBody3D.FREEZE_MODE_KINEMATIC
		rb.freeze = true
	else:
		_player_body.velocity = Vector3.ZERO
		_player_transit = tr
	_core_transits.append(tr)
	return true


func _process_core_transits(delta: float) -> void:
	var done: Array[Dictionary] = []
	for tr: Dictionary in _core_transits:
		var n: Node3D = tr["node"] as Node3D
		if n == null or not is_instance_valid(n):
			done.append(tr)
			continue
		tr["t"] = float(tr["t"]) + delta
		var k: float = clampf(float(tr["t"]) / float(tr["dur"]), 0.0, 1.0)
		var ks: float = smoothstep(0.0, 1.0, k)
		# Ride the shaft line through rho = 0 at the core; ease any lateral pad offset out in the first 15%.
		var on_line: Vector3 = (tr["from"] as Vector3).lerp(tr["to"] as Vector3, ks)
		var lateral: Vector3 = (tr["start"] as Vector3) - (tr["from"] as Vector3)
		var pos: Vector3 = on_line + lateral * (1.0 - smoothstep(0.0, 0.15, k))
		n.global_position = pos
		tr["min_rho"] = minf(float(tr["min_rho"]), _ring_rho(pos))
		var prev_up: Vector3 = tr["last_up"] as Vector3
		var up: Vector3 = _ring_up_at(pos, prev_up)
		if up.dot(prev_up) < -0.5:
			tr["flipped"] = true  # crossed the axis: radial gravity now points at the opposite floor
		tr["last_up"] = up
		var step: float = _orient_node_to_up(n, up, delta)
		tr["max_step"] = maxf(float(tr["max_step"]), step)
		if bool(tr["is_player"]):
			_player_body.up_direction = up
			_player_body.velocity = Vector3.ZERO
		if k >= 1.0:
			done.append(tr)
	for tr2: Dictionary in done:
		_core_transits.erase(tr2)
		var n2: Node3D = tr2["node"] as Node3D
		if bool(tr2["is_player"]):
			_player_transit = {}
			_last_transit_report = tr2
		elif n2 != null and is_instance_valid(n2):
			var rb: RigidBody3D = n2 as RigidBody3D
			rb.freeze = false
			rb.linear_velocity = Vector3.ZERO
			rb.angular_velocity = Vector3.ZERO
			_last_box_transit_report = tr2


func _place_player_in_ring(theta_deg: float, z: float) -> void:
	_player_body.global_transform = Transform3D(_ring_frame(theta_deg), _ring_floor_point(theta_deg, z, -RING_FEET_OFFSET))
	_player_body.velocity = Vector3.ZERO
	_player_body.up_direction = _player_body.global_basis.y


func _toggle_gravity_ring_test() -> void:
	if _player_body == null or _ring_root == null or not _player_transit.is_empty():
		return
	if _in_gravity_ring(_player_body.global_position):
		_player_body.up_direction = Vector3.UP
		_respawn()
	else:
		_place_player_in_ring(0.0, RING_WALK_Z)
		_show_toast("SPIN-GRAVITY TEST RING // WALK 360 DEG  [E] ON AMBER PAD = CORIOLIS CORE LIFT  [G] EXIT", 3.5)


# ------------------------------------------------------------------------------
# [t34u] Automated cylinder spin-gravity QA  (`-- --qa-cylinder-gravity`)
# ------------------------------------------------------------------------------
func _qa_grid(imgs: Array, fname: String) -> void:
	var valid: Array[Image] = []
	for im in imgs:
		if im != null:
			valid.append(im as Image)
	if valid.size() < imgs.size() or valid.is_empty():
		return
	var combo: Image = Image.create(1920, 1080, false, valid[0].get_format())
	for i: int in range(valid.size()):
		var tile: Image = valid[i].duplicate() as Image
		tile.resize(960, 540, Image.INTERPOLATE_BILINEAR)
		combo.blit_rect(tile, Rect2i(0, 0, 960, 540), Vector2i((i % 2) * 960, (i / 2) * 540))
	combo.fill_rect(Rect2i(958, 0, 4, 1080), Color(0.9, 0.95, 1.0))
	combo.fill_rect(Rect2i(0, 538, 1920, 4), Color(0.9, 0.95, 1.0))
	combo.save_png(_resolve_path(QA_DIR) + "/" + fname)
	print("[CYL-QA] Saved ", fname)


func _qa_free_cam(pos: Vector3, target: Vector3, up: Vector3, fov: float) -> void:
	# SpringArm3D rewrites its child camera transform every physics tick; pause it for the free QA camera.
	if _spring_arm != null:
		_spring_arm.set_physics_process_internal(false)
	_camera.top_level = true
	_camera.global_transform = Transform3D(Basis.looking_at(target - pos, up), pos)
	_camera.fov = fov
	if _fp_wrist_holder != null:
		_fp_wrist_holder.visible = false


func _qa_player_cam() -> void:
	if _spring_arm != null:
		_spring_arm.set_physics_process_internal(true)
	_camera.top_level = false
	_camera.transform = Transform3D.IDENTITY
	_camera.fov = 70.0
	_apply_view_mode()


func _qa_cyl_check(nm: String, ok: bool, detail: String) -> void:
	var line: String = "%s | %s | %s" % ["PASS" if ok else "FAIL", nm, detail]
	print("[CYL-QA] ", line)
	_qa_log.append(line)
	if not ok:
		_qa_failures += 1


func _qa_face_align(n: Node3D, up: Vector3) -> float:
	var gb: Basis = n.global_basis
	return maxf(absf(gb.x.dot(up)), maxf(absf(gb.y.dot(up)), absf(gb.z.dot(up))))


func _run_cylinder_gravity_qa() -> void:
	if _player_body == null or _camera == null or _ring_root == null:
		_qa_cyl_check("setup", false, "player/camera/ring missing")
		get_tree().quit(1)
		return
	if _hud_toast != null:
		_hud_toast.visible = false
	_third_person = false
	_apply_view_mode()
	var R: float = RING_RADIUS
	var foot_rho: float = R + RING_FEET_OFFSET
	var box_rho: float = R - RING_BOX_SIZE * 0.5

	# ---------------- STEP 1: full 360 deg walk around the inner ring ----------------
	_place_player_in_ring(0.0, RING_WALK_Z)
	_pitch = deg_to_rad(8.0)
	_apply_pitch()
	await _qa_frames(40)
	foot_rho = _ring_rho(_player_body.global_position)
	_qa_cyl_check("step1_spawn_on_floor_theta0", _player_body.is_on_floor(), "on_floor=%s rho=%.3f theta=%.1f" % [_player_body.is_on_floor(), foot_rho, _ring_theta_deg(_player_body.global_position)])
	var shots: Array = [await _qa_capture("gravity_step1_walk_000deg.png")]
	var table: PackedStringArray = PackedStringArray()
	table.append("| milestone | frame | theta_deg | rho_m | on_floor | basis_y . local_up | basis_y world |")
	table.append("|---|---|---|---|---|---|---|")
	_qa_key(KEY_SHIFT, true)
	_qa_key(KEY_W, true)
	await _qa_idle(2)
	var last_th: float = _ring_theta_deg(_player_body.global_position)
	var travelled: float = 0.0
	var frames: int = 0
	var floor_frames: int = 0
	var min_align: float = 1.0
	var max_rho_err: float = 0.0
	var next_ms: int = 90
	while travelled < 366.0 and frames < 1500:
		await _qa_frames(1)
		frames += 1
		var pp: Vector3 = _player_body.global_position
		var th_now: float = _ring_theta_deg(pp)
		travelled += wrapf(th_now - last_th, -180.0, 180.0)
		last_th = th_now
		var align: float = _player_body.global_basis.y.dot(_ring_up_at(pp, Vector3.UP))
		min_align = minf(min_align, align)
		if _player_body.is_on_floor():
			floor_frames += 1
			max_rho_err = maxf(max_rho_err, absf(_ring_rho(pp) - foot_rho))
		if travelled >= float(next_ms) and next_ms <= 360:
			var by: Vector3 = _player_body.global_basis.y
			table.append("| %d deg | %d | %.1f | %.3f | %s | %.5f | (%.2f, %.2f, %.2f) |" % [next_ms, frames, th_now, _ring_rho(pp), _player_body.is_on_floor(), align, by.x, by.y, by.z])
			if next_ms < 360:
				shots.append(await _qa_capture("gravity_step1_walk_%03ddeg.png" % next_ms))
			next_ms += 90
	_qa_key(KEY_W, false)
	_qa_key(KEY_SHIFT, false)
	await _qa_idle(2)
	await _qa_frames(20)
	_qa_cyl_check("step1_full_360_traversed", travelled >= 360.0, "travelled=%.1f deg (%.1f m) in %d physics frames, sprint W" % [travelled, deg_to_rad(travelled) * R, frames])
	_qa_cyl_check("step1_stays_on_local_floor", float(floor_frames) / float(maxi(frames, 1)) > 0.98 and max_rho_err < 0.08, "on_floor %d/%d frames, max |rho - %.3f| = %.4f m" % [floor_frames, frames, foot_rho, max_rho_err])
	_qa_cyl_check("step1_basis_tracks_radial_up", min_align > 0.995, "min dot(basis.y, -radial_outward) = %.5f over the loop" % min_align)
	_qa_cyl_check("step1_back_at_start_on_floor", _player_body.is_on_floor() and absf(wrapf(_ring_theta_deg(_player_body.global_position), -180.0, 180.0)) < 25.0, "theta=%.1f on_floor=%s" % [_ring_theta_deg(_player_body.global_position), _player_body.is_on_floor()])
	_qa_grid(shots, "gravity_step1_360_walk_angles.png")

	# ---------------- STEP 2: boxes at 0..315 deg stay planted on their local floor ----------------
	var box_rows: PackedStringArray = PackedStringArray()
	box_rows.append("| box | home_theta | theta_now | rho_center | speed_m_s | face_align | drift_deg |")
	box_rows.append("|---|---|---|---|---|---|---|")
	var ring_boxes: Array[RigidBody3D] = []
	var homes: Array[float] = []
	for bx: Dictionary in _gravity_boxes:
		if String((bx["body"] as Node).name).begins_with("RingBox_"):
			ring_boxes.append(bx["body"] as RigidBody3D)
			homes.append(float(bx["home_theta"]))
	await _qa_frames(60)
	# Kick every box toward the axis (1.6 m/s) — spin gravity must pull it back onto its own local floor.
	for rbk: RigidBody3D in ring_boxes:
		rbk.linear_velocity = _ring_up_at(rbk.global_position, Vector3.UP) * 1.6
	await _qa_frames(300)
	var planted_ok: int = 0
	for bi: int in range(ring_boxes.size()):
		var rb2: RigidBody3D = ring_boxes[bi]
		var p2: Vector3 = rb2.global_position
		var fa2: float = _qa_face_align(rb2, _ring_up_at(p2, Vector3.UP))
		var rho_c: float = _ring_rho(p2)
		var spd: float = rb2.linear_velocity.length()
		var drift: float = absf(wrapf(_ring_theta_deg(p2) - homes[bi], -180.0, 180.0))
		if absf(rho_c - box_rho) < 0.06 and spd < 0.05 and fa2 > 0.995 and drift < 3.0:
			planted_ok += 1
		box_rows.append("| %s | %.0f | %.2f | %.3f | %.4f | %.5f | %.2f |" % [rb2.name, homes[bi], _ring_theta_deg(p2), rho_c, spd, fa2, drift])
	_qa_cyl_check("step2_8_boxes_planted_0_to_315", planted_ok == 8 and ring_boxes.size() == 8, "%d/%d boxes flat on local floor (rho %.2f +/- 0.06, speed < 0.05, face-aligned > 0.995, drift < 3 deg) after a 1.6 m/s axis-ward kick" % [planted_ok, ring_boxes.size(), box_rho])
	_qa_free_cam(RING_CENTER - RING_AXIS * (RING_LENGTH * 0.5 - 0.3), RING_CENTER + RING_AXIS * RING_BOX_Z, Vector3.UP, 92.0)
	await _qa_idle(2)
	await _qa_capture("gravity_step2_ring_boxes_planted.png")
	_qa_player_cam()

	# ---------------- STEP 3: Coriolis core transit flips gravity + re-orients ----------------
	var tbox: RigidBody3D = null
	for bx5: Dictionary in _gravity_boxes:
		if String((bx5["body"] as Node).name) == "CoreTransitBox":
			tbox = bx5["body"] as RigidBody3D
	var g_before: Vector3 = _ring_gravity_at(tbox.global_position).normalized()
	var ext_shots: Array = []
	_qa_cyl_check("step3_box_transit_started", _start_core_transit(tbox, false), "from theta=%.1f rho=%.3f" % [_ring_theta_deg(tbox.global_position), _ring_rho(tbox.global_position)])
	var bguard: int = 0
	while _is_transiting(tbox) and bguard < 600:
		await _qa_frames(1)
		bguard += 1
	await _qa_frames(150)
	var g_after: Vector3 = _ring_gravity_at(tbox.global_position).normalized()
	var tb_align: float = _qa_face_align(tbox, _ring_up_at(tbox.global_position, Vector3.UP))
	var brep: Dictionary = _last_box_transit_report
	_qa_cyl_check("step3_box_crossed_core_rho0", float(brep.get("min_rho", 99.0)) < 0.1 and bool(brep.get("flipped", false)), "min_rho=%.3f flipped=%s" % [float(brep.get("min_rho", 99.0)), brep.get("flipped", false)])
	_qa_cyl_check("step3_box_gravity_flipped_planted_opposite", g_before.dot(g_after) < -0.99 and absf(_ring_theta_deg(tbox.global_position) - 180.0) < 3.0 and absf(_ring_rho(tbox.global_position) - box_rho) < 0.06 and tbox.linear_velocity.length() < 0.05 and tb_align > 0.995,
		"gravity dir before=(%.2f, %.2f, %.2f) after=(%.2f, %.2f, %.2f) theta=%.1f rho=%.3f speed=%.4f face_align=%.4f" % [g_before.x, g_before.y, g_before.z, g_after.x, g_after.y, g_after.z, _ring_theta_deg(tbox.global_position), _ring_rho(tbox.global_position), tbox.linear_velocity.length(), tb_align])

	# Player transit via the real [E] input on the theta 0 amber lift pad
	_place_player_in_ring(0.0, RING_SHAFT_Z)
	_pitch = deg_to_rad(60.0)
	_apply_pitch()
	await _qa_frames(30)
	var t_shots: Array = [await _qa_capture("gravity_step3a_on_lift_pad.png")]
	var up_before: Vector3 = _player_body.global_basis.y
	await _qa_tap(KEY_E)
	var started: bool = not _player_transit.is_empty() or not _last_transit_report.is_empty()
	_qa_cyl_check("step3_player_E_starts_core_transit", started, "transit_active=%s" % started)
	var mid_shot: bool = false
	var guard: int = 0
	while not _player_transit.is_empty() and guard < 900:
		await _qa_frames(1)
		guard += 1
		if not mid_shot and float(_player_transit.get("t", 0.0)) > CORE_TRANSIT_DURATION * 0.55:
			mid_shot = true
			t_shots.append(await _qa_capture("gravity_step3b_core_crossing_flip.png"))
	await _qa_frames(90)
	var prep: Dictionary = _last_transit_report
	var pp3: Vector3 = _player_body.global_position
	var up_loc: Vector3 = _ring_up_at(pp3, Vector3.UP)
	var p_align: float = _player_body.global_basis.y.dot(up_loc)
	var cam_align: float = _camera_pivot.global_basis.x.dot(_player_body.global_basis.x)
	var rate_lim: float = RING_ORIENT_RATE / float(Engine.physics_ticks_per_second) + 0.001
	_qa_cyl_check("step3_player_crossed_core_rho0", float(prep.get("min_rho", 99.0)) < 0.1 and bool(prep.get("flipped", false)), "min_rho=%.3f flipped=%s" % [float(prep.get("min_rho", 99.0)), prep.get("flipped", false)])
	_qa_cyl_check("step3_player_smooth_reorient", float(prep.get("max_step", 9.0)) <= rate_lim, "max basis rotation per physics frame = %.4f rad (limit %.4f, 180 deg in ~%.2f s)" % [float(prep.get("max_step", 9.0)), rate_lim, PI / RING_ORIENT_RATE])
	var by3: Vector3 = _player_body.global_basis.y
	_qa_cyl_check("step3_player_on_opposite_floor_flipped", _player_body.is_on_floor() and absf(_ring_theta_deg(pp3) - 180.0) < 3.0 and p_align > 0.995 and up_before.dot(by3) < -0.99 and cam_align > 0.999,
		"on_floor=%s theta=%.1f rho=%.3f body_up=(%.2f, %.2f, %.2f) dot(up_before)=%.3f body_align=%.4f camera_pivot_x_align=%.4f" % [_player_body.is_on_floor(), _ring_theta_deg(pp3), _ring_rho(pp3), by3.x, by3.y, by3.z, up_before.dot(by3), p_align, cam_align])
	_pitch = deg_to_rad(8.0)
	_apply_pitch()
	await _qa_frames(3)
	t_shots.append(await _qa_capture("gravity_step3c_landed_opposite_floor.png"))
	var th0: float = _ring_theta_deg(_player_body.global_position)
	_qa_key(KEY_W, true)
	await _qa_idle(2)
	await _qa_frames(120)
	_qa_key(KEY_W, false)
	await _qa_idle(2)
	await _qa_frames(20)
	var dth: float = absf(wrapf(_ring_theta_deg(_player_body.global_position) - th0, -180.0, 180.0))
	_qa_cyl_check("step3_walk_on_flipped_floor", _player_body.is_on_floor() and dth > 15.0 and absf(_ring_rho(_player_body.global_position) - foot_rho) < 0.08, "walked %.1f deg (%.2f m) along the new floor, on_floor=%s" % [dth, deg_to_rad(dth) * R, _player_body.is_on_floor()])
	_qa_free_cam(RING_CENTER - RING_AXIS * (RING_LENGTH * 0.5 - 0.3) + Vector3(0.0, 3.0, 0.0), RING_CENTER + RING_AXIS * RING_SHAFT_Z, Vector3.UP, 80.0)
	await _qa_idle(2)
	t_shots.append(await _qa_capture("gravity_step3d_shaft_overview.png"))
	_qa_player_cam()
	_qa_grid(t_shots, "gravity_step3_core_transit_flip.png")

	# ---------------- Report ----------------
	var out: PackedStringArray = PackedStringArray()
	out.append("# Cylinder radial spin-gravity QA log ([t34u])")
	out.append("")
	out.append("display=%s  failures=%d  ring: R=%.1f m, L=%.1f m, center=%s, axis=%s, g(rho)=9.8*rho/R, orient rate=%.1f rad/s" % [DisplayServer.get_name(), _qa_failures, RING_RADIUS, RING_LENGTH, str(RING_CENTER), str(RING_AXIS), RING_ORIENT_RATE])
	out.append("")
	out.append_array(_qa_log)
	out.append("")
	out.append("## Step 1 - 360 deg sprint walk milestones")
	out.append("")
	out.append_array(table)
	out.append("")
	out.append("## Step 2 - ring boxes after settle + 1.6 m/s axis-ward kick (300 physics frames)")
	out.append("")
	out.append_array(box_rows)
	var dir_abs: String = _resolve_path(QA_DIR)
	DirAccess.make_dir_recursive_absolute(dir_abs)
	var fn: String = dir_abs + ("/cylinder_gravity_qa_log_headless.md" if DisplayServer.get_name() == "headless" else "/cylinder_gravity_qa_log.md")
	var fa: FileAccess = FileAccess.open(fn, FileAccess.WRITE)
	if fa != null:
		fa.store_string("\n".join(out) + "\n")
		fa.close()
	print("[CYL-QA] DONE failures=", _qa_failures, " log=", fn)
	get_tree().quit(1 if _qa_failures > 0 else 0)


# ------------------------------------------------------------------------------
# [t38u] 1. Viewport-centered Reticle + 2. Rotating Distant Starfield Cylinder + 3. RFID Force-Field Doors ([t45u])
# ------------------------------------------------------------------------------
func _sync_reticle_to_viewport_center() -> void:
	var vp: Viewport = get_viewport()
	if vp == null:
		return
	var vp_sz: Vector2 = vp.get_visible_rect().size
	if _reticle_box == null or not is_instance_valid(_reticle_box):
		return
	# [QA-FF-05] anchor-centred (PRESET_CENTER, grow both) so the layout engine keeps it centred in any
	# parent rect (Windows embedded Game view, live resize); no manual pixel positioning.
	_reticle_center_px = vp_sz * 0.5
	if _reticle_box.anchor_left != 0.5 or _reticle_box.anchor_top != 0.5 or _reticle_box.size != Vector2(24.0, 24.0):
		_reticle_box.size = Vector2(24.0, 24.0)
		_reticle_box.set_anchors_and_offsets_preset(Control.PRESET_CENTER, Control.PRESET_MODE_KEEP_SIZE)
		_reticle_box.grow_horizontal = Control.GROW_DIRECTION_BOTH
		_reticle_box.grow_vertical = Control.GROW_DIRECTION_BOTH


func _make_procedural_starfield_texture() -> ImageTexture:
	if _tex_cache.has("__procedural_starfield__"):
		return _tex_cache["__procedural_starfield__"] as ImageTexture
	var w: int = 1024
	var h: int = 512
	var img: Image = Image.create(w, h, false, Image.FORMAT_RGBA8)
	img.fill(Color(0.008, 0.011, 0.018, 1.0))

	# Subtle galactic dust / nebula band undulating across the cylinder sky
	for y: int in range(h):
		var v: float = float(y) / float(h)
		var band_dist: float = absf(v - 0.50)
		if band_dist < 0.24:
			var w_band: float = 1.0 - (band_dist / 0.24)
			w_band = w_band * w_band
			for x: int in range(w):
				var u: float = float(x) / float(w)
				var wave: float = 0.5 + 0.5 * sin(u * TAU * 2.0 + sin(u * TAU * 5.0) * 0.6)
				var neb: float = w_band * (0.35 + 0.65 * wave)
				var base_c: Color = img.get_pixel(x, y)
				var tint: Color = Color(0.045, 0.085, 0.145, 1.0) if int(x + y) % 2 == 0 else Color(0.075, 0.055, 0.130, 1.0)
				img.set_pixel(x, y, base_c.lerp(tint, neb * 0.55))

	# Deterministic PRNG for multi-scale stars (pinpoint field stars + medium stars + bright navigational beacons)
	var rng: RandomNumberGenerator = RandomNumberGenerator.new()
	rng.seed = 704192026
	var palette: Array[Color] = [
		Color(0.96, 0.98, 1.00, 1.0),
		Color(0.78, 0.90, 1.00, 1.0),
		Color(1.00, 0.92, 0.78, 1.0),
		Color(0.68, 0.86, 1.00, 1.0),
		Color(1.00, 0.80, 0.62, 1.0),
		Color(0.86, 0.78, 1.00, 1.0)
	]
	# 2600 stars, each at least 2 px wide so the mips keep them.
	for i: int in range(2600):
		var sx: int = rng.randi_range(0, w - 2)
		var sy: int = rng.randi_range(0, h - 2)
		var b: float = rng.randf_range(0.55, 1.0)
		var col: Color = palette[i % palette.size()] * b
		col.a = 1.0
		for ox: int in range(2):
			for oy: int in range(2):
				img.set_pixel(sx + ox, sy + oy, col)
	# 420 medium 2x2 / cross stars
	for i: int in range(420):
		var mx: int = rng.randi_range(2, w - 3)
		var my: int = rng.randi_range(2, h - 3)
		var mc: Color = palette[i % palette.size()]
		img.set_pixel(mx, my, Color(1.0, 1.0, 1.0, 1.0))
		for off: Vector2i in [Vector2i(1, 0), Vector2i(-1, 0), Vector2i(0, 1), Vector2i(0, -1)]:
			var p: Vector2i = Vector2i(mx, my) + off
			img.set_pixel(p.x, p.y, img.get_pixel(p.x, p.y).lerp(mc, 0.82))
	# 95 bright navigational cluster beacons with soft glow & diffraction cross
	for i: int in range(95):
		var bx: int = rng.randi_range(4, w - 5)
		var by: int = rng.randi_range(4, h - 5)
		var bc: Color = palette[i % palette.size()]
		for dy: int in range(-3, 4):
			for dx: int in range(-3, 4):
				var dist: float = sqrt(float(dx * dx + dy * dy))
				if dist <= 3.2:
					var falloff: float = clampf(1.0 - dist / 3.2, 0.0, 1.0)
					if dx == 0 or dy == 0:
						falloff = maxf(falloff, 0.65 * (1.0 - dist / 3.5))
					var px: int = clampi(bx + dx, 0, w - 1)
					var py: int = clampi(by + dy, 0, h - 1)
					img.set_pixel(px, py, img.get_pixel(px, py).lerp(bc, falloff))
		img.set_pixel(bx, by, Color(1.0, 1.0, 1.0, 1.0))

	img.generate_mipmaps()
	var tex: ImageTexture = ImageTexture.create_from_image(img)
	_tex_cache["__procedural_starfield__"] = tex
	return tex


func _build_starfield_outer_cylinder(parent: Node3D) -> void:
	# [t38u] Massive far-offset outer starfield cylinder coaxial with Cylinder Hab-7.
	# Same axis as CylinderHab7_DrumAxisPivot: world +X through (135, 187.2, 0). No valley roll (a full shell).
	# This shell spins about that axis in _process; the habitat drum stays stationary (no spin animation).
	_starfield_cylinder = Node3D.new()
	_starfield_cylinder.name = "StarfieldOuterCylinder"
	_starfield_cylinder.position = Vector3(135.0, 187.2, 0.0)
	parent.add_child(_starfield_cylinder)

	var star_tex: ImageTexture = _make_procedural_starfield_texture()
	var smat: StandardMaterial3D = StandardMaterial3D.new()
	smat.resource_name = "Mat_StarfieldOuterCylinder"
	smat.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	smat.cull_mode = BaseMaterial3D.CULL_DISABLED
	smat.albedo_color = Color(1.0, 1.0, 1.0, 1.0)
	smat.albedo_texture = star_tex
	# 9 tiles around the circumference (~1536 m) and 3 along the length (1600 m).
	smat.uv1_scale = Vector3(9.0, 3.0, 1.0)
	smat.texture_filter = BaseMaterial3D.TEXTURE_FILTER_LINEAR_WITH_MIPMAPS_ANISOTROPIC

	var barrel: MeshInstance3D = MeshInstance3D.new()
	barrel.name = "StarfieldOuterBarrelMesh"
	var cm: CylinderMesh = CylinderMesh.new()
	cm.top_radius = STARFIELD_CYL_RADIUS
	cm.bottom_radius = STARFIELD_CYL_RADIUS
	cm.height = STARFIELD_CYL_LENGTH
	cm.radial_segments = 96
	cm.rings = 1
	cm.cap_top = false
	cm.cap_bottom = false
	barrel.mesh = cm
	# CylinderMesh height is along local Y. -90 deg about Z maps that axis onto parent +X (world +X).
	# Parent then spins about X, so the shell stays coaxial with the habitat drum.
	barrel.rotation_degrees = Vector3(0.0, 0.0, -90.0)
	barrel.material_override = smat
	barrel.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	barrel.extra_cull_margin = 16384.0
	_starfield_cylinder.add_child(barrel)

	# [M-33] Separate planar caps. CylinderMesh caps shared the barrel UV scale and smeared the stars.
	var cap_mat: StandardMaterial3D = smat.duplicate() as StandardMaterial3D
	cap_mat.resource_name = "Mat_StarfieldOuterCap"
	cap_mat.cull_mode = BaseMaterial3D.CULL_BACK
	cap_mat.uv1_triplanar = false
	cap_mat.uv1_scale = Vector3(4.0, 4.0, 1.0)
	cap_mat.texture_filter = BaseMaterial3D.TEXTURE_FILTER_LINEAR_WITH_MIPMAPS_ANISOTROPIC
	var cap_size: float = STARFIELD_CYL_RADIUS * 2.0
	var half_len: float = STARFIELD_CYL_LENGTH * 0.5
	# Negative end: PlaneMesh FACE_X normal is +X, which faces back into the cylinder.
	var cap_neg: MeshInstance3D = MeshInstance3D.new()
	cap_neg.name = "StarfieldOuterCap_NegX"
	var pm_neg: PlaneMesh = PlaneMesh.new()
	pm_neg.size = Vector2(cap_size, cap_size)
	pm_neg.orientation = PlaneMesh.FACE_X
	cap_neg.mesh = pm_neg
	cap_neg.position = Vector3(-half_len, 0.0, 0.0)
	cap_neg.material_override = cap_mat
	cap_neg.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	cap_neg.extra_cull_margin = 16384.0
	_starfield_cylinder.add_child(cap_neg)
	# Positive end: flip the normal to -X so this face also points inward.
	var cap_pos: MeshInstance3D = MeshInstance3D.new()
	cap_pos.name = "StarfieldOuterCap_PosX"
	var pm_pos: PlaneMesh = PlaneMesh.new()
	pm_pos.size = Vector2(cap_size, cap_size)
	pm_pos.orientation = PlaneMesh.FACE_X
	cap_pos.mesh = pm_pos
	cap_pos.position = Vector3(half_len, 0.0, 0.0)
	cap_pos.rotation_degrees = Vector3(0.0, 180.0, 0.0)
	cap_pos.material_override = cap_mat
	cap_pos.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	cap_pos.extra_cull_margin = 16384.0
	_starfield_cylinder.add_child(cap_pos)


# ------------------------------------------------------------------------------
# [t39u]-[t40u] Dynamic interior despawn / respawn streaming (no loading screens)
# ------------------------------------------------------------------------------
const INTERIOR_ARCH_NODE_NAMES := [
	"Apartment_Furniture_And_Props", "Apartment_Workbench", "Apartment_Bunk_Pod", "Alcove_2C_Storage_Nook",
	"Atrium_Planters_And_Benches", "Room_2B_Interior_Props", "Side_Room_East_Medbay"
]
const INTERIOR_TASK_LIGHT_PREFIXES := ["Apt201_", "Apt202_", "Room1A_", "Room1B_"]


func _is_interior_task_light(l: Node) -> bool:
	for pfx: String in INTERIOR_TASK_LIGHT_PREFIXES:
		if String(l.name).begins_with(pfx):
			return true
	return false


func _despawn_building_interiors() -> int:
	if not _interiors_loaded:
		return 0
	var managed: int = 0
	_interior_detached_records.clear()
	# 1. Free every interior pickup, terminal, hatch panel, and baked anim-prop (doors stay — they are the building envelope).
	var keep_items: Array[Dictionary] = []
	for it: Dictionary in _interactables:
		var k: String = String(it["kind"])
		if bool(it["pickup"]) or k == "terminal" or k == "troubleshoot" or k == "anim_prop":
			var raw: Variant = it["node"]
			if is_instance_valid(raw):
				var n: Node3D = raw as Node3D
				if n.get_parent() != null:
					n.get_parent().remove_child(n)
				n.queue_free()
				managed += 1
		else:
			keep_items.append(it)
	_interactables = keep_items
	for ch: Node in _props_container.get_children():
		if String(ch.name) == DOORS_ROOT_NAME:
			continue
		_props_container.remove_child(ch)
		ch.queue_free()
		managed += 1
	# 2. Detach interior furniture / room-prop subtrees from the residential sector GLB.
	var sector: Node3D = _arch_container.get_node_or_null("PrefaceResidentialSector_Doorless") as Node3D
	if sector != null:
		var stack: Array[Node] = [sector]
		var found: Array[Node3D] = []
		while not stack.is_empty():
			var c: Node = stack.pop_back()
			if not is_instance_valid(c) or _is_baked_leaf_door_name(String(c.name)):
				continue
			if c != sector and c is Node3D and INTERIOR_ARCH_NODE_NAMES.has(String(c.name)):
				found.append(c as Node3D)
				continue
			for ch2: Node in c.get_children():
				stack.append(ch2)
		for n3: Node3D in found:
			var par: Node = n3.get_parent()
			_interior_detached_records.append({"node": n3, "parent": par, "index": n3.get_index()})
			par.remove_child(n3)
			managed += 1
	# 3. Detach interior bots / residents (Sector-4 vestibule actors at Z <= -7.5 stay).
	for a: Node in _actors_container.get_children():
		if a is Node3D and (a as Node3D).position.z > -7.5:
			_interior_detached_records.append({"node": a, "parent": _actors_container, "index": a.get_index()})
	for rec: Dictionary in _interior_detached_records:
		var an: Node = rec["node"] as Node
		if an.get_parent() == _actors_container:
			_actors_container.remove_child(an)
			managed += 1
	# 4. Disable interior room task lights.
	for l: OmniLight3D in _task_lights:
		if _is_interior_task_light(l):
			l.visible = false
			managed += 1
	for sl: Node in _lights_container.get_children():
		if sl is SpotLight3D and _is_interior_task_light(sl):
			(sl as SpotLight3D).visible = false
	_interior_managed_count = managed
	_interiors_loaded = false
	print("[InteriorStreaming] DESPAWNED %d interior nodes/lights (player on Sector-4 Promenade)" % managed)
	return managed


func _respawn_building_interiors() -> int:
	if _interiors_loaded:
		return 0
	var restored: int = 0
	# Re-attach in reverse detach order so original child indices are restored cleanly.
	for i: int in range(_interior_detached_records.size() - 1, -1, -1):
		var rec: Dictionary = _interior_detached_records[i]
		var n: Node = rec["node"] as Node
		var par: Node = rec["parent"] as Node
		if n == null or not is_instance_valid(n) or par == null or not is_instance_valid(par):
			continue
		if n.get_parent() == null:
			par.add_child(n)
			par.move_child(n, mini(int(rec["index"]), par.get_child_count() - 1))
			restored += 1
	_interior_detached_records.clear()
	restored += _spawn_interior_pickups(false)
	_spawn_animated_props()
	_spawn_rev_c_static_props()
	for l: OmniLight3D in _task_lights:
		l.visible = true
	for sl: Node in _lights_container.get_children():
		if sl is SpotLight3D:
			(sl as SpotLight3D).visible = true
	_interiors_loaded = true
	# [M-19] The probe is UPDATE_ONCE. Rebake for two frames after interiors stream back in.
	_retrigger_reflection_probe()
	print("[InteriorStreaming] RESPAWNED %d interior nodes (collected pickups preserved: %d)" % [restored, _collected_pickup_ids.size()])
	return restored


func _update_interior_streaming(player_pos: Vector3) -> void:
	if _qa_placement:
		return
	if _props_container == null or _arch_container == null:
		return
	# [QA-FF-02] interiors stay loaded while the Sector-4 exit field is open or opening (line of sight inside).
	var exit_open: bool = _sector4_exit_open_or_opening()
	if _interiors_loaded:
		if player_pos.z < INTERIOR_DESPAWN_Z and not _in_gravity_ring(player_pos) and not exit_open:
			_despawn_building_interiors()
	elif player_pos.z >= INTERIOR_RESPAWN_Z or _in_gravity_ring(player_pos) or exit_open:
		_respawn_building_interiors()


func _sector4_exit_open_or_opening() -> bool:
	var d: Dictionary = _find_door("DOOR_SECTOR4_EXIT")
	if d.is_empty():
		return false
	return bool(d["open"]) or _door_dissolve(d) > 0.0


func get_interior_streaming_status() -> Dictionary:
	var n_pick: int = 0
	for it: Dictionary in _interactables:
		if bool(it["pickup"]) and not bool(it["collected"]):
			var raw: Variant = it["node"]
			if is_instance_valid(raw) and (raw as Node3D).is_inside_tree():
				n_pick += 1
	return {
		"interiors_loaded": _interiors_loaded,
		"managed_count": _interior_managed_count,
		"detached_nodes": _interior_detached_records.size(),
		"live_pickups": n_pick,
		"collected_ids": _collected_pickup_ids.keys(),
		"door_type": "rfid_forcefield"
	}


# ------------------------------------------------------------------------------
# [t45u] RFID FORCE-FIELD DOOR (single design, all 6 portals)
#   Model : FORCEFIELD_DOOR_GLB (Rook: Frame, FrameInset, EmitterStrip, RFIDPanel, StatusLight, FieldPlane;
#           bottom-centre pivot, +Z = player-facing side, 1.50 x 2.45 m clear opening, 1.82 x 2.61 m outer frame)
#   Shader: FORCEFIELD_DOOR_SHADER (Rook, used as-is; one ShaderMaterial per door on FieldPlane.material_override)
#   Python UI hook: set_door_field(door_id, opacity, color) + DOOR_FIELD_JSON polling (tools/door_field_ui.py)
# ------------------------------------------------------------------------------
func _dbox(parent: Node3D, nm: String, sz: Vector3, pos: Vector3, mat: Material, rot_deg: Vector3 = Vector3.ZERO, shadow: bool = true) -> MeshInstance3D:
	var mi: MeshInstance3D = MeshInstance3D.new()
	mi.name = nm
	var bm: BoxMesh = BoxMesh.new()
	bm.size = sz
	mi.mesh = bm
	mi.position = pos
	mi.rotation_degrees = rot_deg
	mi.material_override = mat
	if not shadow:
		mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	parent.add_child(mi)
	return mi


func _ff_static_box(parent: Node3D, nm: String, sz: Vector3, pos: Vector3) -> CollisionShape3D:
	var body: StaticBody3D = StaticBody3D.new()
	body.name = nm
	body.position = pos
	parent.add_child(body)
	var cs: CollisionShape3D = CollisionShape3D.new()
	cs.name = nm + "_Shape"
	var bs: BoxShape3D = BoxShape3D.new()
	bs.size = sz
	cs.shape = bs
	body.add_child(cs)
	return cs


func _ff_load_shader() -> Shader:
	if _ff_shader != null:
		return _ff_shader
	var abs_p: String = _resolve_path(FORCEFIELD_DOOR_SHADER)
	if FileAccess.file_exists(abs_p):
		var sh: Shader = Shader.new()
		sh.code = FileAccess.get_file_as_string(abs_p)
		_ff_shader = sh
	else:
		push_error("[FORCEFIELD] shader missing: " + FORCEFIELD_DOOR_SHADER)
	return _ff_shader


func _ff_instance_model(glb_path: String = FORCEFIELD_DOOR_GLB) -> Node3D:
	# Runtime GLTF load by path (new files from Rook are picked up automatically); parsed state cached per path.
	if not _glb_cache.has(glb_path):
		var abs_p: String = _resolve_path(glb_path)
		if not FileAccess.file_exists(abs_p):
			push_error("[FORCEFIELD] glb missing: " + glb_path)
			return null
		var doc: GLTFDocument = GLTFDocument.new()
		var st: GLTFState = GLTFState.new()
		if doc.append_from_file(abs_p, st) != OK:
			push_error("[FORCEFIELD] glb load failed: " + abs_p)
			return null
		_glb_cache[glb_path] = [doc, st]
	var pair: Array = _glb_cache[glb_path] as Array
	var root: Node = (pair[0] as GLTFDocument).generate_scene(pair[1] as GLTFState)
	if not (root is Node3D):
		if root != null:
			root.free()
		return null
	var r3: Node3D = root as Node3D
	# Runtime GLTF import may yield ImporterMeshInstance3D nodes: convert to plain MeshInstance3D (names kept).
	var stack: Array[Node] = [r3]
	var imps: Array[ImporterMeshInstance3D] = []
	while not stack.is_empty():
		var c: Node = stack.pop_back()
		if c is ImporterMeshInstance3D:
			imps.append(c as ImporterMeshInstance3D)
		for ch: Node in c.get_children():
			stack.append(ch)
	for imp: ImporterMeshInstance3D in imps:
		var mi: MeshInstance3D = MeshInstance3D.new()
		mi.transform = imp.transform
		mi.mesh = imp.mesh.get_mesh() if imp.mesh != null else null
		var p: Node = imp.get_parent()
		var nm: String = String(imp.name)
		var idx: int = imp.get_index()
		p.remove_child(imp)
		imp.free()
		mi.name = nm
		p.add_child(mi)
		p.move_child(mi, idx)
	return r3


func _clear_rfid_doors(parent: Node3D) -> void:
	var old: Node = parent.get_node_or_null(DOORS_ROOT_NAME)
	if old != null:
		parent.remove_child(old)
		old.free()
	_rfid_doors.clear()
	var keep: Array[Dictionary] = []
	for it: Dictionary in _interactables:
		if String(it["kind"]) != "rfid_door":
			keep.append(it)
	_interactables = keep


## M-41. APT 201/202 are pinned to the Rev C corridor faces. The other RFID doors follow
## the Door_* marker on the loaded shell. Godot can drop an empty glTF node, so each
## door keeps the generator pose (preface_sector_rev_c_generator.py DOORS).
func _rfid_door_world_pos(door_id: String, marker_name: String, fallback: Vector3) -> Vector3:
	if door_id == "DOOR_APT201":
		return Vector3(-3.0, 4.2, 0.8)
	if door_id == "DOOR_APT202":
		return Vector3(3.0, 4.2, 0.8)
	if marker_name != "" and _arch_container != null:
		var marker: Node3D = _lookup_sector_node(_arch_container, marker_name) as Node3D
		if marker != null and is_instance_valid(marker) and marker.is_inside_tree():
			return marker.global_position
	push_warning("[PrefacePlayableArea] %s marker %s missing; using %s" % [door_id, marker_name, str(fallback)])
	return fallback


func _build_rfid_forcefield_doors(parent: Node3D) -> void:
	_clear_rfid_doors(parent)
	var doors_root: Node3D = Node3D.new()
	doors_root.name = DOORS_ROOT_NAME
	parent.add_child(doors_root)
	var shader: Shader = _ff_load_shader()
	var m_infill: StandardMaterial3D = StandardMaterial3D.new()
	m_infill.albedo_color = Color(0.78, 0.80, 0.83)
	m_infill.metallic = 0.35
	m_infill.roughness = 0.38

	# Widths are the Rev C wall cuts (1.5 / 2.0 / 2.6). The frame mesh stays 1.82 x 2.61.
	var door_specs: Array[Dictionary] = [
		{"id": "DOOR_APT201", "label": "APT 201 // RFID FORCE-FIELD DOOR", "marker": "Door_201", "fallback": Vector3(-3.0, 4.2, 0.8), "w": 1.50, "h": 2.55},
		{"id": "DOOR_ALCOVE2C", "label": "ALCOVE 2C // RFID FORCE-FIELD DOOR", "marker": "Door_203", "fallback": Vector3(-4.5, 4.2, -0.8), "w": 1.50, "h": 2.45},
		{"id": "DOOR_APT202", "label": "APT 202 // RFID FORCE-FIELD DOOR", "marker": "Door_202", "fallback": Vector3(3.0, 4.2, 0.8), "w": 1.50, "h": 2.55},
		{"id": "DOOR_RM1A", "label": "RM 1A LAUNDRY // RFID FORCE-FIELD DOOR", "marker": "Door_Laundry", "fallback": Vector3(-2.0, 0.0, 0.8), "w": 1.50, "h": 2.60},
		{"id": "DOOR_RM1B", "label": "RM 1B SUBSTATION // RFID FORCE-FIELD DOOR", "marker": "Door_Maintenance", "fallback": Vector3(3.2, 0.0, 0.8), "w": 2.00, "h": 2.60},
		{"id": "DOOR_SECTOR4_EXIT", "label": "SECTOR-4 PROMENADE EXIT // RFID FORCE-FIELD DOOR", "marker": "Door_Sector4_Exit", "fallback": Vector3(0.0, 0.0, -9.1), "w": 2.60, "h": 2.80}
	]
	for spec: Dictionary in door_specs:
		var did: String = String(spec["id"])
		var dpos: Vector3 = _rfid_door_world_pos(did, String(spec["marker"]), spec["fallback"] as Vector3)
		var pw: float = float(spec["w"])
		var ph: float = float(spec["h"])
		# Model +Z is the hub side. North-wall doors (z > 0) face the corridor, world -Z.
		# South-wall doors and the Sector-4 exit face +Z.
		var face_neg_z: bool = did != "DOOR_SECTOR4_EXIT" and dpos.z > 0.0
		var droot: Node3D = Node3D.new()
		droot.name = did
		droot.position = dpos
		droot.rotation_degrees = Vector3(0.0, 180.0 if face_neg_z else 0.0, 0.0)  # model +Z -> player side
		doors_root.add_child(droot)

		var model: Node3D = _ff_instance_model()
		if model == null:
			continue
		model.name = "ForceFieldDoorModel"
		droot.add_child(model)
		var n_field: MeshInstance3D = model.find_child("FieldPlane", true, false) as MeshInstance3D
		# [Bulkhead Hub] the hub replaces the door glb's own RFIDPanel + StatusLight: hide them.
		for retired: String in ["RFIDPanel", "StatusLight"]:
			var rn: Node3D = model.find_child(retired, true, false) as Node3D
			if rn != null:
				rn.visible = false

		var fmat: ShaderMaterial = _ff_new_field_material(shader)
		if n_field != null and is_instance_valid(n_field):
			n_field.material_override = fmat
			n_field.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
			# [M-18] Door fields draw over the observation window (strip -1 / caps -2).
			fmat.render_priority = 1
		# One emissive material per emitter part per door, tinted to the field colour by set_door_field().
		var emit_mats: Dictionary = {}
		for en: String in FF_EMITTER_ENERGY.keys():
			var n_e: MeshInstance3D = model.find_child(en, true, false) as MeshInstance3D
			if n_e == null or not is_instance_valid(n_e):
				continue
			var em_m: StandardMaterial3D = StandardMaterial3D.new()
			em_m.albedo_color = FF_DEFAULT_COLOR
			em_m.emission_enabled = true
			em_m.emission = FF_DEFAULT_COLOR
			em_m.emission_energy_multiplier = float(FF_EMITTER_ENERGY[en])
			if en == "EmitterStrip":
				_ff_apply_coil_textures(em_m, true)
			n_e.material_override = em_m
			emit_mats[en] = em_m
		var threshold_mat: StandardMaterial3D = _ff_bind_threshold(model, false)
		var hub: Dictionary = _build_door_hub(droot, did)
		var lmat: StandardMaterial3D = hub.get("glow_mat") as StandardMaterial3D

		# Wall fit: close any gap between the 1.82 x 2.61 m frame and the wider/taller baked portal opening.
		# Visual infill stays 5 mm inside the 0.30 m wall faces (no coplanar faces -> no z-fighting).
		var half_pw: float = pw * 0.5
		var infill_d: float = 0.29
		if half_pw > FF_FRAME_HALF_W + 0.005:
			var iw: float = half_pw - FF_FRAME_HALF_W + 0.03
			for sx: float in [-1.0, 1.0]:
				_dbox(droot, "PortalInfill_%s" % ("L" if sx < 0.0 else "R"), Vector3(iw, ph + 0.03, infill_d),
					Vector3(sx * (FF_FRAME_HALF_W + iw * 0.5), (ph + 0.03) * 0.5, 0.0), m_infill)
		if ph > FF_FRAME_H + 0.005:
			var ih: float = ph - FF_FRAME_H + 0.03
			_dbox(droot, "PortalInfill_Top", Vector3(FF_FRAME_HALF_W * 2.0, ih, infill_d), Vector3(0.0, FF_FRAME_H + ih * 0.5, 0.0), m_infill)
		# Colliders: jambs leave a walkable opening; the field box (unchanged 1.50 m) is the closed-door block.
		# [DOOR-04] If a jamb's inner face sits inside the spec width w, push it out so the clear width is
		# at least min(w, 2.6) - 0.1 and at least 1.5 m. Closed FieldCollider size stays FF_OPEN_W.
		var field_cs: CollisionShape3D = null
		if not _batch_render:
			var clear_w: float = maxf(minf(pw, 2.6) - 0.1, 1.5)
			var inner_half: float = FF_OPEN_W * 0.5
			if inner_half * 2.0 < pw:
				inner_half = maxf(inner_half, clear_w * 0.5)
			var outer_half: float = maxf(half_pw, FF_FRAME_HALF_W) + 0.03
			if inner_half > outer_half - 0.02:
				inner_half = maxf(outer_half - 0.02, FF_OPEN_W * 0.5)
			var side_w: float = maxf(outer_half - inner_half, 0.02)
			for sx2: float in [-1.0, 1.0]:
				_ff_static_box(droot, "PortalJambCollider_%s" % ("L" if sx2 < 0.0 else "R"), Vector3(side_w, ph + 0.03, 0.30),
					Vector3(sx2 * (inner_half + side_w * 0.5), (ph + 0.03) * 0.5, 0.0))
			var top_h: float = maxf(ph, FF_FRAME_H) - FF_OPEN_H + 0.03
			_ff_static_box(droot, "PortalHeaderCollider", Vector3(maxf(pw, FF_FRAME_HALF_W * 2.0), top_h, 0.30), Vector3(0.0, FF_OPEN_H + top_h * 0.5, 0.0))
			field_cs = _ff_static_box(droot, "FieldCollider", Vector3(FF_OPEN_W, FF_OPEN_H, 0.20), Vector3(0.0, FF_OPEN_H * 0.5, 0.0))

		# [E] RFID scan target = the hub's ScanZone (fallback: a doorway anchor if the hub glb is missing).
		var tag_anchor: Node3D = hub.get("scan_zone") as Node3D
		if tag_anchor == null:
			tag_anchor = Node3D.new()
			tag_anchor.name = did + "_RFIDTag"
			tag_anchor.position = Vector3(0.0, 1.35, 0.0)
			droot.add_child(tag_anchor)
		var d_entry: Dictionary = {
			"id": did,
			"label": String(spec["label"]),
			"root": droot,
			"center": tag_anchor.global_position if tag_anchor.is_inside_tree() else dpos + Vector3(0.0, 1.25, 0.0),
			"hub": hub.get("root"),
			"glow_nodes": hub.get("glow_nodes", []),
			"arm_pivot": hub.get("arm_pivot"),
			"dock_marker": hub.get("dock_marker"),
			"dock_hook": false,
			"arm_deployed": false,
			"arm_tween": null,
			"glow_tween": null,
			"field_mat": fmat,
			"emit_mats": emit_mats,
			"led_mat": lmat,
			"field_collider": field_cs,
			"threshold_mat": threshold_mat,
			"tween": null,
			"surge_tween": null,
			"close_pending": false,
			"close_retry_t": 0.0,
			"close_blocker": "",
			"open": false,
			"dissolve": 0.0,
			"opacity": FF_DEFAULT_OPACITY,
			"field_color": FF_DEFAULT_COLOR,
			"ff_state": "locked",
			"strength": 1.0,
			"stall_t": 0.0,
			"stall_clock": 0.0,
			"deny_t": 0.0,
			"split": false,
			"half_a_on": true,
			"half_b_on": true,
			"split_synced": false,
			"split_cycled": false,
			"mat_a": null,
			"mat_b": null,
			"col_a": null,
			"col_b": null,
			"field_a": null,
			"field_b": null,
			"coil_in_phase": true
		}
		_ff_apply_state_textures(d_entry, "locked")
		_rfid_doors.append(d_entry)
		_interactables.append({
			"node": tag_anchor,
			"kind": "rfid_door",
			"label": String(spec["label"]),
			"door_id": did,
			"collected": false,
			"pickup": false
		})
	print("[FORCEFIELD] doors=%d glb=%s shader=%s" % [_rfid_doors.size(), FORCEFIELD_DOOR_GLB, FORCEFIELD_DOOR_SHADER])
	print("[FORCEFIELD] door field overrides: newer of %s | %s  (user dir: %s)" % [_resolve_path(DOOR_FIELD_JSON_DEV), _resolve_path(DOOR_FIELD_JSON_USER), OS.get_user_data_dir()])
	_poll_door_field_json()  # apply any saved overrides at boot


func _build_door_hub(droot: Node3D, did: String) -> Dictionary:
	var hub_root: Node3D = _ff_instance_model(DOOR_HUB_GLB)
	if hub_root == null:
		return {}
	hub_root.name = "DoorHub_" + did
	hub_root.position = HUB_MOUNT_OFFSET + Vector3(0.0, 0.0, HUB_WALL_STANDOFF)
	droot.add_child(hub_root)
	# Per-door glow material (amber idle) shared by the 8 state-glow parts.
	var gm: StandardMaterial3D = StandardMaterial3D.new()
	gm.albedo_color = HUB_AMBER
	gm.emission_enabled = true
	gm.emission = HUB_AMBER
	gm.emission_energy_multiplier = 2.0
	var glow_nodes: Array = []
	for gp: String in HUB_GLOW_PARTS:
		var gn: MeshInstance3D = hub_root.find_child(gp, true, false) as MeshInstance3D
		if gn != null:
			gn.material_override = gm
			glow_nodes.append(gn)
	# Coupler arm: modelled DEPLOYED; reparent arm parts under a Y pivot and default to STOWED (+90 deg).
	var piv: Node3D = Node3D.new()
	piv.name = "CouplerArm_StowPivot"
	piv.position = HUB_ARM_PIVOT
	var arm_parent: Node = hub_root
	var first_arm: Node3D = hub_root.find_child(HUB_ARM_PARTS[0], true, false) as Node3D
	if first_arm != null:
		arm_parent = first_arm.get_parent()
	arm_parent.add_child(piv)
	for ap: String in HUB_ARM_PARTS:
		var an: Node3D = hub_root.find_child(ap, true, false) as Node3D
		if an != null:
			var keep: Transform3D = an.transform
			an.get_parent().remove_child(an)
			piv.add_child(an)
			an.transform = Transform3D(keep.basis, keep.origin - HUB_ARM_PIVOT)
	piv.rotation_degrees = Vector3(0.0, HUB_ARM_STOWED_DEG, 0.0)
	# Sprocket park marker on the floor dock pad (origin, facing +Z in the hub frame).
	var mk: Marker3D = Marker3D.new()
	mk.name = "SprocketDock_" + did
	mk.position = HUB_DOCK_POS
	hub_root.add_child(mk)
	return {
		"root": hub_root,
		"glow_mat": gm,
		"glow_nodes": glow_nodes,
		"arm_pivot": piv,
		"dock_marker": mk,
		"scan_zone": hub_root.find_child("ScanZone", true, false) as Node3D
	}


## Public hook: force Sprocket's dock state for a door (in addition to live proximity to the SprocketDock marker).
func sprocket_dock(door_id: String, parked: bool) -> bool:
	var d: Dictionary = _find_door(door_id)
	if d.is_empty():
		return false
	d["dock_hook"] = parked
	return true


func _fit_dock_pad_to_floor(door: Dictionary) -> void:
	# Baked floors sit above some door pivots (ground floor ~+0.115 m), so lift the 13 mm dock pad + park marker
	# onto the real floor surface (one-time downward ray; no floor cut).
	var mk: Marker3D = door["dock_marker"] as Marker3D
	var hub_root: Node3D = door["hub"] as Node3D
	var space: PhysicsDirectSpaceState3D = get_world_3d().direct_space_state
	if space == null or hub_root == null:
		return
	var base: Vector3 = mk.global_position - Vector3(0.0, HUB_DOCK_POS.y, 0.0)
	var rq: PhysicsRayQueryParameters3D = PhysicsRayQueryParameters3D.create(base + Vector3(0.0, 0.8, 0.0), base - Vector3(0.0, 0.5, 0.0))
	if _player_body != null:
		rq.exclude = [_player_body.get_rid()]
	var hit: Dictionary = space.intersect_ray(rq)
	if hit.is_empty():
		return
	var lift: float = clampf((hit["position"] as Vector3).y - base.y, 0.0, 0.30)
	for pn: String in ["DockPad", "DockPad_InductionRing", "DockPad_Chevrons"]:
		var n: Node3D = hub_root.find_child(pn, true, false) as Node3D
		if n != null:
			n.position.y += lift
	mk.position.y += lift
	door["pad_fitted"] = true
	door["pad_lift"] = lift


## Nine hub-face samples. Each entry is the hit distance along local -Z, or -1 if nothing is hit within `depth`.
func _hub_back_hit_distances(door: Dictionary, depth: float) -> Array[float]:
	var out: Array[float] = []
	var hub_root: Node3D = door["hub"] as Node3D
	var space: PhysicsDirectSpaceState3D = get_world_3d().direct_space_state
	if hub_root == null or space == null:
		return out
	var xf: Transform3D = hub_root.global_transform
	for hx: float in HUB_BACKING_SAMPLE_X:
		for hy: float in HUB_BACKING_SAMPLE_Y:
			var origin: Vector3 = xf * Vector3(hx, hy, 0.0)
			var rq: PhysicsRayQueryParameters3D = PhysicsRayQueryParameters3D.create(origin, xf * Vector3(hx, hy, -depth))
			if _player_body != null:
				rq.exclude = [_player_body.get_rid()]
			var hit: Dictionary = space.intersect_ray(rq)
			if hit.is_empty():
				out.append(-1.0)
			else:
				out.append(origin.distance_to(hit["position"] as Vector3))
	return out


func _hub_median(vals: Array[float]) -> float:
	var s: Array[float] = []
	s.append_array(vals)
	s.sort()
	var n: int = s.size()
	if n <= 0:
		return 0.0
	if n % 2 == 1:
		return s[n >> 1]
	return (s[(n >> 1) - 1] + s[n >> 1]) * 0.5


func _hub_backing_misses(door: Dictionary, depth: float) -> int:
	# Same 9-point grid as seating (HUB_BACKING_SAMPLE_X/Y). Count points with no solid within `depth`.
	var hub_root: Node3D = door["hub"] as Node3D
	var space: PhysicsDirectSpaceState3D = get_world_3d().direct_space_state
	if hub_root == null or space == null:
		return -1
	var dists: Array[float] = _hub_back_hit_distances(door, depth)
	var expect: int = HUB_BACKING_SAMPLE_X.size() * HUB_BACKING_SAMPLE_Y.size()
	var misses: int = maxi(0, expect - dists.size())
	for d: float in dists:
		if d < 0.0:
			misses += 1
	return misses


func _nudge_hub_to_wall(door: Dictionary) -> Dictionary:
	# Back-normal seat from the hub's current pose. Median of hits within 0.30 m, then move by d - 3 mm.
	var hub_root: Node3D = door["hub"] as Node3D
	var hits: Array[float] = []
	for dist: float in _hub_back_hit_distances(door, HUB_SEAT_RAY_DEPTH):
		if dist >= 0.0 and dist <= HUB_SEAT_RAY_DEPTH:
			hits.append(dist)
	if hub_root == null or hits.size() < HUB_SEAT_MIN_HITS:
		return {"ok": false, "d": 0.0, "nudge": 0.0, "hits": hits.size()}
	var d_med: float = _hub_median(hits)
	var nudge: float = d_med - HUB_SEAT_GAP
	var back: Vector3 = -hub_root.global_transform.basis.z
	if back.length_squared() > 0.0000001:
		hub_root.global_position += back.normalized() * nudge
	return {"ok": true, "d": d_med, "nudge": nudge, "hits": hits.size()}


func _remember_hub_center(door: Dictionary) -> void:
	var hub_root: Node3D = door["hub"] as Node3D
	if hub_root == null:
		return
	var scan_n: Node3D = hub_root.find_child("ScanZone", true, false) as Node3D
	door["center"] = scan_n.global_position if scan_n != null else hub_root.global_position


func _fit_hub_backing(door: Dictionary) -> void:
	# [D670-04] Seat on the wall along local -Z. If any of the 9 face rays still miss within 5 cm
	# (one column overhangs the portal), slide along local X, 1 cm steps, both ways, up to 0.35 m.
	# Take the smallest shift that lands 9/9 within 5 cm (away from the doorway first) and re-seat.
	# HubWallBacking only if no shift works. Same path for every door.
	# [QA-BK-01] APT201's real wall is the west pier, so a seated hub gets no HubWallBacking.
	# ALCOVE2C has no east jamb since M-70; it uses the normal seat/HubWallBacking path.
	# Door roots are not moved. A seated hit is not given a second backing slab.
	var hub_root: Node3D = door["hub"] as Node3D
	var space: PhysicsDirectSpaceState3D = get_world_3d().direct_space_state
	if hub_root == null or space == null:
		return
	var did: String = String(door["id"])
	door["backing_checked"] = true
	door["hub_seat"] = 0.0
	door["hub_tangent_shift"] = 0.0
	door["backing_added"] = false
	var seated: Dictionary = _nudge_hub_to_wall(door)
	if bool(seated["ok"]):
		door["hub_seat"] = float(seated["nudge"])
	var base_pos: Vector3 = hub_root.global_position
	var base_seat: float = float(door["hub_seat"])
	if bool(seated["ok"]) and _hub_backing_misses(door, HUB_BACKING_MAX_GAP) == 0:
		_remember_hub_center(door)
		print("[HUB] %s: seated d=%.4f shift=%.4f hits=9/9" % [did, base_seat + HUB_SEAT_GAP, 0.0])
		return
	var tangent: Vector3 = hub_root.global_transform.basis.x
	if tangent.length_squared() <= 0.0000001:
		if absf(base_seat) > 0.0000001:
			_remember_hub_center(door)
		_hub_add_wall_backing(door, hub_root)
		return
	tangent = tangent.normalized()
	var root_n: Node3D = door["root"] as Node3D
	var along: float = 0.0
	if root_n != null:
		along = (base_pos - root_n.global_position).dot(tangent)
	var away: float = -1.0 if along < 0.0 else 1.0
	var step_signs: Array[float] = [away, -away]
	var n_steps: int = int(round(HUB_TANGENT_MAX / HUB_TANGENT_STEP))
	var found: bool = false
	var best_lat: float = 0.0
	var best_seat: float = base_seat
	for step_i: int in range(1, n_steps + 1):
		var mag: float = HUB_TANGENT_STEP * float(step_i)
		for sgn: float in step_signs:
			hub_root.global_position = base_pos + tangent * (sgn * mag)
			var nudged: Dictionary = _nudge_hub_to_wall(door)
			if not bool(nudged["ok"]):
				continue
			if _hub_backing_misses(door, HUB_BACKING_MAX_GAP) != 0:
				continue
			found = true
			best_lat = sgn * mag
			best_seat = base_seat + float(nudged["nudge"])
			break
		if found:
			break
	if found:
		door["hub_seat"] = best_seat
		door["hub_tangent_shift"] = best_lat
		_remember_hub_center(door)
		print("[HUB] %s: seated d=%.4f shift=%.4f hits=9/9" % [did, best_seat + HUB_SEAT_GAP, best_lat])
		return
	hub_root.global_position = base_pos
	door["hub_seat"] = base_seat
	door["hub_tangent_shift"] = 0.0
	if absf(base_seat) > 0.0000001:
		_remember_hub_center(door)
	_hub_add_wall_backing(door, hub_root)


func _hub_add_wall_backing(door: Dictionary, hub_root: Node3D) -> void:
	var did: String = String(door["id"])
	var sz: Vector3 = Vector3(0.695, 1.44, 0.25)
	var ctr: Vector3 = Vector3(0.1275, 1.10, -0.020 - sz.z * 0.5)
	var m: StandardMaterial3D = StandardMaterial3D.new()
	m.albedo_color = Color(0.26, 0.29, 0.33)
	m.metallic = 0.8
	m.roughness = 0.34
	var t: Texture2D = _load_tex("facade_titanium_gunmetal_hull.png")
	if t != null:
		m.albedo_texture = t
	_dbox(hub_root, "HubWallBacking", sz, ctr, m)
	var body: StaticBody3D = StaticBody3D.new()
	body.name = "HubWallBacking_Collider"
	body.position = ctr
	hub_root.add_child(body)
	var cs: CollisionShape3D = CollisionShape3D.new()
	var bs: BoxShape3D = BoxShape3D.new()
	bs.size = sz
	cs.shape = bs
	body.add_child(cs)
	door["backing_added"] = true
	print("[HUB] %s: fallback backing" % did)


func _update_hub_docks() -> void:
	var spr: Node3D = _actors_container.get_node_or_null(SPROCKET_NODE) as Node3D if _actors_container != null else null
	var spr_ok: bool = spr != null and is_instance_valid(spr) and spr.is_inside_tree() and spr.visible
	for door: Dictionary in _rfid_doors:
		var mk: Marker3D = door.get("dock_marker") as Marker3D
		if mk == null or not is_instance_valid(mk):
			continue
		if not bool(door.get("pad_fitted", false)):
			_fit_dock_pad_to_floor(door)
		if not bool(door.get("backing_checked", false)) and _frame_counter >= 3:
			_fit_hub_backing(door)
		var parked: bool = bool(door["dock_hook"])
		if not parked and spr_ok:
			var dv: Vector3 = spr.global_position - mk.global_position
			parked = Vector2(dv.x, dv.z).length() < HUB_DOCK_RADIUS and absf(dv.y) < 0.4
		if parked != bool(door["arm_deployed"]):
			door["arm_deployed"] = parked
			var piv: Node3D = door["arm_pivot"] as Node3D
			var old: Variant = door["arm_tween"]
			if old is Tween and (old as Tween).is_valid():
				(old as Tween).kill()
			var tw: Tween = create_tween()
			tw.tween_property(piv, "rotation_degrees:y", 0.0 if parked else HUB_ARM_STOWED_DEG, 0.6).set_trans(Tween.TRANS_SINE)
			door["arm_tween"] = tw


func _find_door(door_id: String) -> Dictionary:
	for d: Dictionary in _rfid_doors:
		if String(d["id"]) == door_id:
			return d
	return {}


func _door_dissolve(door: Dictionary) -> float:
	var m: ShaderMaterial = door["field_mat"] as ShaderMaterial
	return float(m.get_shader_parameter("dissolve")) if m != null else 0.0


func _set_door_light(door: Dictionary, open_state: bool) -> void:
	# Snap the hub's 8 glow parts (one shared per-door material) to the final state colour.
	var old: Variant = door.get("glow_tween")
	if old is Tween and (old as Tween).is_valid():
		(old as Tween).kill()
	var lmat: StandardMaterial3D = door["led_mat"] as StandardMaterial3D
	if lmat != null:
		var col: Color = FF_LIGHT_GREEN if open_state else HUB_AMBER
		lmat.albedo_color = col
		lmat.emission = col


func _tween_door_light(door: Dictionary, open_state: bool, dur: float) -> void:
	# Access grant -> tween amber to green over the dissolve; close -> back to amber.
	var old: Variant = door.get("glow_tween")
	if old is Tween and (old as Tween).is_valid():
		(old as Tween).kill()
	var lmat: StandardMaterial3D = door["led_mat"] as StandardMaterial3D
	if lmat == null:
		return
	var col: Color = FF_LIGHT_GREEN if open_state else HUB_AMBER
	var tw: Tween = create_tween().set_parallel(true)
	tw.tween_property(lmat, "emission", col, maxf(dur, 0.001))
	tw.tween_property(lmat, "albedo_color", col, maxf(dur, 0.001))
	door["glow_tween"] = tw


func _ff_tex(fname: String) -> Texture2D:
	if _ff_tex_cache.has(fname):
		return _ff_tex_cache[fname] as Texture2D
	var res_p: String = FF_TEX_DIR + fname
	var tex: Texture2D = null
	if ResourceLoader.exists(res_p):
		var loaded: Resource = ResourceLoader.load(res_p)
		if loaded is Texture2D:
			tex = loaded as Texture2D
	if tex == null:
		var abs_p: String = _resolve_path(res_p)
		if FileAccess.file_exists(abs_p):
			var img: Image = Image.new()
			if img.load(abs_p) == OK and not img.is_empty():
				tex = ImageTexture.create_from_image(img)
	_ff_tex_cache[fname] = tex
	return tex


func _ff_new_field_material(shader: Shader) -> ShaderMaterial:
	var fmat: ShaderMaterial = ShaderMaterial.new()
	fmat.shader = shader
	fmat.set_shader_parameter("field_color", FF_DEFAULT_COLOR)
	fmat.set_shader_parameter("opacity", FF_DEFAULT_OPACITY)
	fmat.set_shader_parameter("dissolve", 0.0)
	fmat.set_shader_parameter("static_strength", FF_BASE_STATIC)
	fmat.set_shader_parameter("jitter_strength", FF_BASE_JITTER)
	fmat.set_shader_parameter("arc_strength", FF_BASE_ARC)
	fmat.set_shader_parameter("stall_amount", 0.0)
	fmat.set_shader_parameter("split_seam", 0.0)
	var stall_mask: Texture2D = _ff_tex("ff_field_stall_noise_mask.png")
	var seam_a: Texture2D = _ff_tex("ff_split_seam_albedo.png")
	var seam_e: Texture2D = _ff_tex("ff_split_seam_emission.png")
	if stall_mask != null:
		fmat.set_shader_parameter("stall_noise_mask", stall_mask)
	if seam_a != null:
		fmat.set_shader_parameter("split_seam_albedo", seam_a)
	if seam_e != null:
		fmat.set_shader_parameter("split_seam_emission", seam_e)
	return fmat


func _ff_apply_coil_textures(mat: StandardMaterial3D, in_phase: bool) -> void:
	if mat == null:
		return
	var alb: Texture2D = _ff_tex("ff_emitter_coil_albedo.png")
	var orm: Texture2D = _ff_tex("ff_emitter_coil_orm.png")
	var emi_name: String = "ff_emitter_coil_emission_inphase.png" if in_phase else "ff_emitter_coil_emission_outphase.png"
	var emi: Texture2D = _ff_tex(emi_name)
	if alb != null:
		mat.albedo_texture = alb
	if orm != null:
		mat.ao_enabled = true
		mat.ao_texture = orm
		mat.ao_texture_channel = BaseMaterial3D.TEXTURE_CHANNEL_RED
		mat.roughness_texture = orm
		mat.roughness_texture_channel = BaseMaterial3D.TEXTURE_CHANNEL_GREEN
		mat.metallic_texture = orm
		mat.metallic_texture_channel = BaseMaterial3D.TEXTURE_CHANNEL_BLUE
	if emi != null:
		mat.emission_enabled = true
		mat.emission_texture = emi


func _ff_set_threshold_state(mat: StandardMaterial3D, ready_state: bool) -> void:
	if mat == null:
		return
	var alb: Texture2D = _ff_tex("ff_threshold_strip_albedo.png")
	var emi: Texture2D = _ff_tex("ff_threshold_strip_cyan_emission.png" if ready_state else "ff_threshold_strip_amber_emission.png")
	if alb != null:
		mat.albedo_texture = alb
	mat.emission_enabled = true
	mat.emission = FF_READY_CYAN if ready_state else HUB_AMBER
	mat.emission_energy_multiplier = 1.8
	mat.roughness = 0.6
	mat.metallic = 0.0
	if emi != null:
		mat.emission_texture = emi


func _ff_bind_threshold(model: Node, ready_state: bool) -> StandardMaterial3D:
	if model == null or not is_instance_valid(model):
		return null
	var mi: MeshInstance3D = null
	var stack: Array[Node] = [model]
	while not stack.is_empty():
		var c: Node = stack.pop_back()
		if not is_instance_valid(c):
			continue
		if c is MeshInstance3D and String(c.name).to_lower().contains("threshold"):
			mi = c as MeshInstance3D
			break
		for ch: Node in c.get_children():
			stack.append(ch)
	if mi == null:
		return null
	var m: StandardMaterial3D = StandardMaterial3D.new()
	_ff_set_threshold_state(m, ready_state)
	mi.material_override = m
	return m


func _ff_mats(door: Dictionary) -> Array[ShaderMaterial]:
	var out: Array[ShaderMaterial] = []
	var primary: ShaderMaterial = door.get("field_mat") as ShaderMaterial
	if primary != null:
		out.append(primary)
	if bool(door.get("split", false)):
		var ma: ShaderMaterial = door.get("mat_a") as ShaderMaterial
		var mb: ShaderMaterial = door.get("mat_b") as ShaderMaterial
		if ma != null and ma != primary:
			out.append(ma)
		if mb != null and mb != primary:
			out.append(mb)
	return out


func _ff_apply_calib_on_door(door: Dictionary, state: String) -> void:
	var root: Node = door.get("root") as Node
	if root == null or not is_instance_valid(root):
		return
	var cell: int = 1
	if state == "ready" or state == "open":
		cell = 2
	elif state == "off":
		cell = 0
	var alb: Texture2D = _ff_tex("ff_calib_node_albedo.png")
	var emi: Texture2D = _ff_tex("ff_calib_node_emission_states.png")
	for i: int in range(1, 4):
		var n: MeshInstance3D = root.find_child("Node_Calib_%02d" % i, true, false) as MeshInstance3D
		if n == null or not is_instance_valid(n):
			continue
		var m: StandardMaterial3D = n.material_override as StandardMaterial3D
		if m == null:
			m = StandardMaterial3D.new()
			m.emission_enabled = true
			n.material_override = m
		if alb != null:
			m.albedo_texture = alb
		if emi != null:
			m.emission_texture = emi
		m.uv1_scale = Vector3(1.0 / 3.0, 1.0, 1.0)
		m.uv1_offset = Vector3(float(cell) / 3.0, 0.0, 0.0)
		var energy: float = 2.5 if cell > 0 else 0.0
		if state == "stall" and cell > 0:
			energy = 2.5 * (0.85 + 0.15 * sin(_time * TAU))
		m.emission_energy_multiplier = energy


func _ff_apply_state_textures(door: Dictionary, state: String) -> void:
	var amber: bool = state == "locked" or state == "stall" or state == "deny"
	var alb: Texture2D = _ff_tex("ff_field_lockout_amber_albedo.png" if amber else "ff_field_ready_cyan_albedo.png")
	var emi: Texture2D = _ff_tex("ff_field_lockout_amber_emission.png" if amber else "ff_field_ready_cyan_emission.png")
	var stall: float = 1.0 if (state == "stall" or state == "deny") else 0.0
	for mat: ShaderMaterial in _ff_mats(door):
		if alb != null:
			mat.set_shader_parameter("state_albedo", alb)
		if emi != null:
			mat.set_shader_parameter("state_emission", emi)
		mat.set_shader_parameter("stall_amount", stall)
	var tmat: StandardMaterial3D = door.get("threshold_mat") as StandardMaterial3D
	if tmat != null:
		_ff_set_threshold_state(tmat, not amber)
	_ff_apply_calib_on_door(door, state)


func _ff_set_cs(cs: CollisionShape3D, enabled: bool) -> void:
	if cs != null and is_instance_valid(cs):
		cs.set_deferred("disabled", not enabled)


func _ff_field_key(n: Node) -> String:
	var nm: String = String(n.name)
	if nm.ends_with("_Shape"):
		nm = nm.substr(0, nm.length() - 6)
	if not nm.begins_with("FieldCollider") and n.get_parent() != null and String(n.get_parent().name).begins_with("FieldCollider"):
		nm = String(n.get_parent().name)
	return nm


func _ff_is_field_collider_node(n: Node) -> bool:
	var nm: String = String(n.name)
	if nm.begins_with("FieldCollider") and (n is CollisionShape3D or n is CollisionObject3D):
		return true
	return n is CollisionShape3D and n.get_parent() != null and String(n.get_parent().name).begins_with("FieldCollider")


## Closed: the single field stays up, or each split half follows its power. Open: every field collider is off.
func _ff_field_node_on(door: Dictionary, n: Node, force_on: bool) -> bool:
	var key: String = _ff_field_key(n)
	var split: bool = bool(door.get("split", false))
	var open_state: bool = bool(door.get("open", false))
	if key.begins_with("FieldCollider_A"):
		if not split:
			return false
		if force_on:
			return true
		if open_state:
			return false
		return bool(door.get("half_a_on", true))
	if key.begins_with("FieldCollider_B"):
		if not split:
			return false
		if force_on:
			return true
		if open_state:
			return false
		return bool(door.get("half_b_on", true))
	if split:
		return false
	return force_on or not open_state


func _ff_apply_colliders(door: Dictionary, force_on: bool = false) -> void:
	var root: Node = door.get("root") as Node
	if root != null and is_instance_valid(root):
		var stack: Array[Node] = [root]
		while not stack.is_empty():
			var n: Node = stack.pop_back()
			if _ff_is_field_collider_node(n):
				var on: bool = _ff_field_node_on(door, n, force_on)
				if n is CollisionShape3D:
					_ff_set_cs(n as CollisionShape3D, on)
				elif n is CollisionObject3D:
					var layer: int = 1 if on else 0
					(n as CollisionObject3D).set_deferred("collision_layer", layer)
					(n as CollisionObject3D).set_deferred("collision_mask", layer)
			for ch: Node in n.get_children():
				stack.append(ch)
	# Dictionary refs, same rule, so a shape stored before it is parented still toggles.
	var split: bool = bool(door.get("split", false))
	if not split:
		var blocking: bool = force_on or not bool(door.get("open", false))
		_ff_set_cs(door.get("field_collider") as CollisionShape3D, blocking)
	else:
		_ff_set_cs(door.get("field_collider") as CollisionShape3D, false)
		var a_on: bool = true
		var b_on: bool = true
		if force_on:
			a_on = true
			b_on = true
		elif bool(door.get("open", false)):
			a_on = false
			b_on = false
		else:
			a_on = bool(door.get("half_a_on", true))
			b_on = bool(door.get("half_b_on", true))
		_ff_set_cs(door.get("col_a") as CollisionShape3D, a_on)
		_ff_set_cs(door.get("col_b") as CollisionShape3D, b_on)
	_sync_door_nav_link(door)


func _ff_write_noise_params(door: Dictionary, opacity: float, static_s: float, jitter: float, arc: float, stall_amount: float) -> void:
	for mat: ShaderMaterial in _ff_mats(door):
		mat.set_shader_parameter("opacity", opacity)
		mat.set_shader_parameter("static_strength", static_s)
		mat.set_shader_parameter("jitter_strength", jitter)
		mat.set_shader_parameter("arc_strength", arc)
		mat.set_shader_parameter("stall_amount", stall_amount)


func _ff_set_dissolve_all(door: Dictionary, v: float) -> void:
	for mat: ShaderMaterial in _ff_mats(door):
		mat.set_shader_parameter("dissolve", v)


func _ff_set_seam_amount(door: Dictionary, amount: float) -> void:
	for mat: ShaderMaterial in _ff_mats(door):
		mat.set_shader_parameter("split_seam", amount)


func _ff_noise(salt: float, t: float) -> float:
	# Hash the per-door stall clock. Global _time / _frame_counter only move in _process,
	# which does not run between the physics frames the stall QA samples.
	var s: float = sin(t * 17.13 + salt * 1.37) * 43758.5453
	return s - floor(s)


func _ff_kill_tweens(door: Dictionary) -> void:
	for key: String in ["tween", "surge_tween", "glow_tween"]:
		var old: Variant = door.get(key)
		if old is Tween and (old as Tween).is_valid():
			(old as Tween).kill()


func _ff_set_coil_phase(door: Dictionary, in_phase: bool) -> void:
	door["coil_in_phase"] = in_phase
	var ems: Dictionary = door.get("emit_mats", {}) as Dictionary
	if ems.is_empty():
		return
	var strip: StandardMaterial3D = ems.get("EmitterStrip") as StandardMaterial3D
	if strip != null:
		_ff_apply_coil_textures(strip, in_phase)
	var root: Node = door.get("root") as Node
	if root == null or not is_instance_valid(root):
		return
	for nm: String in ["Emitter_Coil_A", "Emitter_Coil_B", "EmitterCoil_A", "EmitterCoil_B"]:
		var mi: MeshInstance3D = root.find_child(nm, true, false) as MeshInstance3D
		if mi == null or not is_instance_valid(mi):
			continue
		var m: StandardMaterial3D = mi.material_override as StandardMaterial3D
		if m == null:
			m = StandardMaterial3D.new()
			m.emission_enabled = true
			mi.material_override = m
		_ff_apply_coil_textures(m, in_phase)


func _ff_apply_half_visuals(door: Dictionary) -> void:
	var level: float = _door_dissolve(door)
	var op: float = float(door.get("opacity", FF_DEFAULT_OPACITY))
	var ma: ShaderMaterial = door.get("mat_a") as ShaderMaterial
	var mb: ShaderMaterial = door.get("mat_b") as ShaderMaterial
	if ma != null:
		if bool(door.get("half_a_on", true)):
			ma.set_shader_parameter("dissolve", level)
			ma.set_shader_parameter("opacity", op)
		else:
			ma.set_shader_parameter("dissolve", 1.0)
			ma.set_shader_parameter("opacity", 0.0)
	if mb != null:
		if bool(door.get("half_b_on", true)):
			mb.set_shader_parameter("dissolve", level)
			mb.set_shader_parameter("opacity", op)
		else:
			mb.set_shader_parameter("dissolve", 1.0)
			mb.set_shader_parameter("opacity", 0.0)


func _ff_half_mesh(negative_x: bool) -> ArrayMesh:
	var hw: float = FF_OPEN_W * 0.5
	var h: float = FF_OPEN_H
	var x0: float = -hw if negative_x else 0.0
	var x1: float = 0.0 if negative_x else hw
	var u0: float = 0.0 if negative_x else 0.5
	var u1: float = 0.5 if negative_x else 1.0
	var st: SurfaceTool = SurfaceTool.new()
	st.begin(Mesh.PRIMITIVE_TRIANGLES)
	var nrm: Vector3 = Vector3(0.0, 0.0, 1.0)
	var verts: Array[Vector3] = [Vector3(x0, 0.0, 0.0), Vector3(x1, 0.0, 0.0), Vector3(x1, h, 0.0), Vector3(x0, 0.0, 0.0), Vector3(x1, h, 0.0), Vector3(x0, h, 0.0)]
	var uvs: Array[Vector2] = [Vector2(u0, 0.0), Vector2(u1, 0.0), Vector2(u1, 1.0), Vector2(u0, 0.0), Vector2(u1, 1.0), Vector2(u0, 1.0)]
	for i: int in range(verts.size()):
		st.set_normal(nrm)
		st.set_uv(uvs[i])
		st.add_vertex(verts[i])
	return st.commit()


func _ff_find_field_plane(root: Node) -> MeshInstance3D:
	if root == null or not is_instance_valid(root):
		return null
	var n: MeshInstance3D = root.find_child("FieldPlane", true, false) as MeshInstance3D
	if n == null or not is_instance_valid(n):
		return null
	if bool(n.get_meta("replaced_by_split", false)):
		return null
	return n


func _ff_tick_stall(door: Dictionary, delta: float) -> void:
	# _process and _physics_process both call in. Apply delta once per physics frame
	# so the ~2 s stall does not run at double speed when idle and physics are paired.
	if delta > 0.0:
		var phys: int = Engine.get_physics_frames()
		if int(door.get("stall_tick_frame", -1)) == phys:
			return
		door["stall_tick_frame"] = phys
		door["stall_clock"] = float(door.get("stall_clock", 0.0)) + delta
		door["stall_t"] = float(door.get("stall_t", 0.0)) - delta
		if float(door["stall_t"]) <= 0.0:
			_ff_surge_from_stall(door)
			return
	var clock: float = float(door.get("stall_clock", 0.0))
	var n0: float = _ff_noise(1.7, clock)
	var n1: float = _ff_noise(4.2, clock)
	var n2: float = _ff_noise(8.9, clock)
	var n3: float = _ff_noise(12.4, clock)
	var base_op: float = float(door.get("opacity", FF_DEFAULT_OPACITY)) * FF_STALL_STRENGTH
	var op: float = clampf(base_op * lerpf(0.72, 1.28, n0), 0.08, base_op * 1.35)
	_ff_write_noise_params(door, op, lerpf(0.62, 0.98, n1), lerpf(0.008, 0.016, n2), lerpf(0.45, 1.35, n3), lerpf(0.85, 1.0, n0))
	door["strength"] = FF_STALL_STRENGTH
	_ff_apply_colliders(door, true)
	_ff_apply_calib_on_door(door, "stall")


func _ff_surge_from_stall(door: Dictionary) -> void:
	door["ff_state"] = "locked"
	door["stall_t"] = 0.0
	door["stall_clock"] = 0.0
	door["strength"] = 1.0
	door["open"] = false
	door["dissolve"] = 0.0
	_ff_set_dissolve_all(door, 0.0)
	_ff_write_noise_params(door, float(door.get("opacity", FF_DEFAULT_OPACITY)), FF_BASE_STATIC, FF_BASE_JITTER, FF_BASE_ARC, 0.0)
	_ff_apply_state_textures(door, "locked")
	_ff_apply_colliders(door, true)
	_sync_door_nav_link(door)
	_set_door_light(door, false)
	var lmat: StandardMaterial3D = door.get("led_mat") as StandardMaterial3D
	if lmat != null:
		var tw: Tween = create_tween()
		tw.tween_property(lmat, "emission_energy_multiplier", 4.2, 0.08)
		tw.tween_property(lmat, "emission_energy_multiplier", 2.0, 0.22)
		door["surge_tween"] = tw


func _ff_tick_deny(door: Dictionary, delta: float) -> void:
	door["deny_t"] = float(door.get("deny_t", 0.0)) - delta
	var elapsed: float = FF_DENY_TIME - float(door["deny_t"])
	var pulse: float = 1.0 if elapsed < 0.08 else clampf(float(door["deny_t"]) / FF_DENY_TIME, 0.0, 1.0)
	var base_op: float = float(door.get("deny_opacity", door.get("opacity", FF_DEFAULT_OPACITY)))
	var op: float = clampf(base_op * lerpf(1.0, 1.6, pulse), 0.0, 1.0)
	_ff_write_noise_params(door, op, lerpf(FF_BASE_STATIC, 0.9, pulse), lerpf(FF_BASE_JITTER, 0.012, pulse), lerpf(FF_BASE_ARC, 1.6, pulse), lerpf(0.4, 1.0, pulse))
	var lmat: StandardMaterial3D = door.get("led_mat") as StandardMaterial3D
	if lmat != null:
		lmat.emission = HUB_AMBER
		lmat.albedo_color = HUB_AMBER
		lmat.emission_energy_multiplier = lerpf(2.0, 4.5, pulse)
	_ff_apply_colliders(door, true)
	if float(door["deny_t"]) <= 0.0:
		_ff_end_deny(door)


func _ff_end_deny(door: Dictionary) -> void:
	var op: float = float(door.get("deny_opacity", door.get("opacity", FF_DEFAULT_OPACITY)))
	_ff_write_noise_params(door, op, float(door.get("deny_static", FF_BASE_STATIC)), float(door.get("deny_jitter", FF_BASE_JITTER)), float(door.get("deny_arc", FF_BASE_ARC)), 0.0)
	var ready: bool = bool(door.get("open", false))
	door["ff_state"] = "open" if ready else "locked"
	door["deny_t"] = 0.0
	_ff_apply_state_textures(door, "ready" if ready else "locked")
	var lmat: StandardMaterial3D = door.get("led_mat") as StandardMaterial3D
	if lmat != null:
		var col: Color = door.get("deny_light", HUB_AMBER) as Color
		lmat.emission = col
		lmat.albedo_color = col
		lmat.emission_energy_multiplier = float(door.get("deny_energy", 2.0))
	_ff_apply_colliders(door, false)
	_sync_door_nav_link(door)


## Partial-power stall. Field stays near 40% strength with noise on opacity, static, jitter and arcs.
## FieldCollider stays on. Hub light stays amber. After `duration` seconds the field surges back to 100%.
func stall_door(door_id: String, duration: float = 2.0) -> bool:
	var door: Dictionary = _find_door(door_id)
	if door.is_empty():
		return false
	_ff_kill_tweens(door)
	var dur: float = duration if duration > 0.0 else FF_STALL_TIME
	door["ff_state"] = "stall"
	door["stall_t"] = dur
	door["stall_dur"] = dur
	door["stall_clock"] = 0.0
	door["stall_tick_frame"] = -1
	door["strength"] = FF_STALL_STRENGTH
	door["open"] = false
	door["close_pending"] = false
	door["dissolve"] = 0.0
	_ff_set_dissolve_all(door, 0.0)
	_ff_apply_state_textures(door, "stall")
	_set_door_light(door, false)
	_ff_apply_colliders(door, true)
	_sync_door_nav_link(door)
	_ff_tick_stall(door, 0.0)
	return true


## 0.3 s amber deny pulse. The field collider stays on for the whole pulse.
func deny_flicker(door_id: String) -> bool:
	var door: Dictionary = _find_door(door_id)
	if door.is_empty():
		return false
	if String(door.get("ff_state", "")) == "stall":
		return true
	var running: Variant = door.get("tween")
	if running is Tween and (running as Tween).is_valid() and (running as Tween).is_running():
		return false
	if String(door.get("ff_state", "")) == "deny":
		door["deny_t"] = FF_DENY_TIME
		return true
	var mat: ShaderMaterial = door.get("field_mat") as ShaderMaterial
	door["deny_opacity"] = float(door.get("opacity", FF_DEFAULT_OPACITY)) if mat == null else _ff_shader_float(mat, "opacity", float(door.get("opacity", FF_DEFAULT_OPACITY)))
	door["deny_static"] = _ff_shader_float(mat, "static_strength", FF_BASE_STATIC)
	door["deny_jitter"] = _ff_shader_float(mat, "jitter_strength", FF_BASE_JITTER)
	door["deny_arc"] = _ff_shader_float(mat, "arc_strength", FF_BASE_ARC)
	var lmat: StandardMaterial3D = door.get("led_mat") as StandardMaterial3D
	if lmat != null:
		door["deny_light"] = lmat.emission
		door["deny_energy"] = lmat.emission_energy_multiplier
	door["ff_state"] = "deny"
	door["deny_t"] = FF_DENY_TIME
	_ff_apply_state_textures(door, "deny")
	_set_door_light(door, false)
	_ff_apply_colliders(door, true)
	_sync_door_nav_link(door)
	return true


func _ff_shader_float(mat: ShaderMaterial, key: String, fallback: float) -> float:
	if mat == null:
		return fallback
	var v: Variant = mat.get_shader_parameter(key)
	if v == null:
		return fallback
	return float(v)


## Replace FieldPlane with FieldPlane_A / FieldPlane_B. Each half has its own ShaderMaterial and FieldCollider.
## The 6 residential doors stay single-plane until this is called.
func enable_split_field(door_id: String) -> bool:
	var door: Dictionary = _find_door(door_id)
	if door.is_empty():
		return false
	if bool(door.get("split", false)):
		return true
	var root: Node3D = door.get("root") as Node3D
	var base: ShaderMaterial = door.get("field_mat") as ShaderMaterial
	if root == null or not is_instance_valid(root) or base == null:
		return false
	var plane: MeshInstance3D = _ff_find_field_plane(root)
	if plane == null:
		return false
	var mat_a: ShaderMaterial = base.duplicate() as ShaderMaterial
	var mat_b: ShaderMaterial = base.duplicate() as ShaderMaterial
	var parent: Node = plane.get_parent()
	var a: MeshInstance3D = MeshInstance3D.new()
	a.name = "FieldPlane_A"
	a.mesh = _ff_half_mesh(true)
	a.transform = plane.transform
	a.material_override = mat_a
	a.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	mat_a.render_priority = 1
	var b: MeshInstance3D = MeshInstance3D.new()
	b.name = "FieldPlane_B"
	b.mesh = _ff_half_mesh(false)
	b.transform = plane.transform
	b.material_override = mat_b
	b.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	mat_b.render_priority = 1
	parent.add_child(a)
	parent.add_child(b)
	plane.visible = false
	plane.set_meta("replaced_by_split", true)
	door["split"] = true
	door["mat_a"] = mat_a
	door["mat_b"] = mat_b
	door["field_a"] = a
	door["field_b"] = b
	door["half_a_on"] = true
	door["half_b_on"] = true
	door["split_synced"] = false
	door["split_cycled"] = false
	if not _batch_render:
		door["col_a"] = _ff_static_box(root, "FieldCollider_A", Vector3(FF_OPEN_W * 0.5, FF_OPEN_H, 0.20), Vector3(-FF_OPEN_W * 0.25, FF_OPEN_H * 0.5, 0.0))
		door["col_b"] = _ff_static_box(root, "FieldCollider_B", Vector3(FF_OPEN_W * 0.5, FF_OPEN_H, 0.20), Vector3(FF_OPEN_W * 0.25, FF_OPEN_H * 0.5, 0.0))
	_ff_set_cs(door.get("field_collider") as CollisionShape3D, false)
	_ff_set_seam_amount(door, 1.0)
	_ff_set_coil_phase(door, false)
	_ff_apply_state_textures(door, "ready" if bool(door.get("open", false)) else "locked")
	_ff_apply_half_visuals(door)
	_ff_apply_colliders(door, false)
	return true


## `half` is "A" or "B". `on` powers that half. Both on after a half has been dropped counts as in sync.
func set_split_half(door_id: String, half: String, on: bool) -> bool:
	var door: Dictionary = _find_door(door_id)
	if door.is_empty() or not bool(door.get("split", false)):
		return false
	var h: String = half.strip_edges().to_upper()
	var which: String = ""
	if h == "A" or h.ends_with("_A"):
		which = "A"
	elif h == "B" or h.ends_with("_B"):
		which = "B"
	else:
		return false
	if which == "A":
		door["half_a_on"] = on
	else:
		door["half_b_on"] = on
	if not on:
		door["split_cycled"] = true
		door["split_synced"] = false
	else:
		door["split_synced"] = bool(door.get("half_a_on", false)) and bool(door.get("half_b_on", false)) and bool(door.get("split_cycled", false))
	_ff_apply_half_visuals(door)
	var show_seam: bool = not bool(door.get("split_synced", false)) and not bool(door.get("open", false))
	_ff_set_seam_amount(door, 1.0 if show_seam else 0.0)
	_ff_set_coil_phase(door, bool(door.get("split_synced", false)))
	var hold: bool = String(door.get("ff_state", "")) == "stall" or String(door.get("ff_state", "")) == "deny"
	_ff_apply_colliders(door, hold)
	return true


## Release dissolve only when both halves are powered and in sync. Otherwise the field stays up.
func sync_collapse(door_id: String) -> bool:
	var door: Dictionary = _find_door(door_id)
	if door.is_empty() or not bool(door.get("split", false)):
		return false
	var in_sync: bool = bool(door.get("half_a_on", false)) and bool(door.get("half_b_on", false)) and bool(door.get("split_synced", false))
	if not in_sync:
		return false
	_ff_set_seam_amount(door, 0.0)
	_ff_set_coil_phase(door, true)
	_set_door_open_state(door, true)
	return true


func _ff_opening_blocked(door: Dictionary, local_x: float) -> bool:
	var droot: Node3D = door.get("root") as Node3D
	if droot == null or not is_instance_valid(droot):
		return false
	var space: PhysicsDirectSpaceState3D = get_world_3d().direct_space_state
	if space == null:
		return false
	var xf: Transform3D = droot.global_transform
	var origin: Vector3 = Vector3(local_x, FF_OPEN_H * 0.5, 0.0)
	var rq: PhysicsRayQueryParameters3D = PhysicsRayQueryParameters3D.create(xf * (origin + Vector3(0.0, 0.0, 0.16)), xf * (origin + Vector3(0.0, 0.0, -0.16)))
	if _player_body != null:
		rq.exclude = [_player_body.get_rid()]
	var hit: Dictionary = space.intersect_ray(rq)
	var ray_hit: bool = false
	if not hit.is_empty():
		var cn: Node = hit.get("collider") as Node
		ray_hit = cn != null and String(cn.name).contains("FieldCollider")
	var q: PhysicsShapeQueryParameters3D = PhysicsShapeQueryParameters3D.new()
	var bs: BoxShape3D = BoxShape3D.new()
	bs.size = Vector3(0.18, 0.18, 0.12)
	q.shape = bs
	q.transform = xf * Transform3D(Basis.IDENTITY, origin)
	q.collide_with_bodies = true
	q.collide_with_areas = false
	if _player_body != null:
		q.exclude = [_player_body.get_rid()]
	var shape_hit: bool = false
	for h: Dictionary in space.intersect_shape(q, 8):
		var sn: Node = h.get("collider") as Node
		if sn != null and String(sn.name).contains("FieldCollider"):
			shape_hit = true
	return ray_hit and shape_hit


func _finish_door_field(door: Dictionary, open_state: bool) -> void:
	door["dissolve"] = 1.0 if open_state else 0.0
	var st: String = String(door.get("ff_state", ""))
	if st != "stall" and st != "deny":
		door["ff_state"] = "open" if open_state else "locked"
		door["strength"] = 1.0
		_ff_apply_state_textures(door, "ready" if open_state else "locked")
	_ff_apply_colliders(door, false)
	_sync_door_nav_link(door)
	_set_door_light(door, open_state)


func _door_opening_blocker(door: Dictionary) -> String:
	# [QA-FF-01 / QA-HUB-01] Overlap test of a thin box exactly in the opening: 1.50 x 2.45 m x 0.35 m deep,
	# centred on the field plane. The hub front / Sprocket dock pad (>= 0.6 m out) never counts.
	var droot: Node3D = door["root"] as Node3D
	if droot == null or not is_instance_valid(droot) or not droot.is_inside_tree():
		return ""
	var xf: Transform3D = droot.global_transform
	# a) Physics bodies (player CharacterBody3D, RigidBody3D props); static wall/door bodies are ignored.
	var q: PhysicsShapeQueryParameters3D = PhysicsShapeQueryParameters3D.new()
	var bs: BoxShape3D = BoxShape3D.new()
	bs.size = Vector3(FF_OPEN_W, FF_OPEN_H, FF_OCCUPANCY_DEPTH)
	q.shape = bs
	q.transform = xf * Transform3D(Basis.IDENTITY, Vector3(0.0, FF_OPEN_H * 0.5, 0.0))
	q.collide_with_bodies = true
	q.collide_with_areas = false
	var space: PhysicsDirectSpaceState3D = get_world_3d().direct_space_state
	if space != null:
		for hit: Dictionary in space.intersect_shape(q, 16):
			var col: Object = hit.get("collider")
			if col is CharacterBody3D or col is RigidBody3D:
				return String((col as Node).name)
	# b) Collider-less actors (Johnny-5 bots, citizens) and props: their origin must be inside the same box.
	var inv: Transform3D = xf.affine_inverse()
	for cont: Node3D in [_actors_container, _props_container]:
		if cont == null:
			continue
		for ch: Node in cont.get_children():
			if not (ch is Node3D) or String(ch.name) == DOORS_ROOT_NAME or ch.is_queued_for_deletion() or not (ch as Node3D).visible:
				continue
			var lp: Vector3 = inv * (ch as Node3D).global_position
			if absf(lp.x) <= FF_OPEN_W * 0.5 and absf(lp.z) <= FF_OCCUPANCY_DEPTH * 0.5 and lp.y >= -0.10 and lp.y <= FF_OPEN_H:
				return String(ch.name)
	return ""


func _set_door_open_state(door: Dictionary, open_target: bool) -> void:
	# Valid [E] hub scan: tween shader dissolve 0->1 (open) or 1->0 (close) over DOOR_DISSOLVE_TIME;
	# collision + status light switch only when the tween finishes.
	if open_target:
		door["close_pending"] = false
	elif bool(door["open"]) or _door_dissolve(door) > 0.0:
		# [QA-FF-01] never close the field on something standing in the opening: hold open, retry every 0.5 s.
		var blocker: String = _door_opening_blocker(door)
		if blocker != "":
			door["close_pending"] = true
			door["close_retry_t"] = FF_CLOSE_RETRY_SEC
			door["close_blocker"] = blocker
			return
		door["close_pending"] = false
	door["open"] = open_target
	if String(door.get("ff_state", "")) == "stall" or String(door.get("ff_state", "")) == "deny":
		door["stall_t"] = 0.0
		door["deny_t"] = 0.0
		_ff_write_noise_params(door, float(door.get("opacity", FF_DEFAULT_OPACITY)), FF_BASE_STATIC, FF_BASE_JITTER, FF_BASE_ARC, 0.0)
	door["ff_state"] = "open" if open_target else "locked"
	door["strength"] = 1.0
	_ff_apply_state_textures(door, "ready" if open_target else "locked")
	_sync_door_nav_link(door)
	var mats: Array[ShaderMaterial] = _ff_mats(door)
	if mats.is_empty():
		return
	_ff_kill_tweens(door)
	var target: float = 1.0 if open_target else 0.0
	var dur: float = DOOR_DISSOLVE_TIME * absf(target - _door_dissolve(door))
	var tw: Tween = create_tween().set_parallel(true)
	for mat: ShaderMaterial in mats:
		tw.tween_property(mat, "shader_parameter/dissolve", target, maxf(dur, 0.001))
	tw.chain().tween_callback(_finish_door_field.bind(door, open_target))
	door["tween"] = tw
	_tween_door_light(door, open_target, maxf(dur, 0.001))


func _set_door_dissolve_immediate(door: Dictionary, v: float) -> void:
	# QA/screenshot helper: jump to a dissolve value without tweening.
	_ff_kill_tweens(door)
	door["stall_t"] = 0.0
	door["deny_t"] = 0.0
	door["strength"] = 1.0
	var clamped: float = clampf(v, 0.0, 1.0)
	_ff_write_noise_params(door, float(door.get("opacity", FF_DEFAULT_OPACITY)), FF_BASE_STATIC, FF_BASE_JITTER, FF_BASE_ARC, 0.0)
	_ff_set_dissolve_all(door, clamped)
	door["close_pending"] = false
	door["open"] = clamped >= 0.999
	door["ff_state"] = "open" if bool(door["open"]) else "locked"
	_finish_door_field(door, clamped >= 0.999)
	door["dissolve"] = clamped


## Public Python-UI hook: per-door field opacity (0..1) + RGBA colour; tints EmitterStrip, EmitterNodes, Conduits to match.
func set_door_field(door_id: String, opacity: float, color: Color) -> bool:
	var door: Dictionary = _find_door(door_id)
	if door.is_empty():
		return false
	var op: float = clampf(opacity, 0.0, 1.0)
	door["opacity"] = op
	door["field_color"] = color
	for mat_sf: ShaderMaterial in _ff_mats(door):
		mat_sf.set_shader_parameter("field_color", color)
		if String(door.get("ff_state", "")) != "stall":
			mat_sf.set_shader_parameter("opacity", op)
	if bool(door.get("split", false)) and String(door.get("ff_state", "")) != "stall":
		_ff_apply_half_visuals(door)
	var emc: Color = Color(color.r, color.g, color.b, 1.0)
	for em_v: Variant in (door["emit_mats"] as Dictionary).values():
		var em: StandardMaterial3D = em_v as StandardMaterial3D
		em.albedo_color = emc
		em.emission = emc
	return true


func _scan_target_door(origin: Vector3) -> Dictionary:
	# [QA-HUB-01] An [E] door scan acts on ONE door: the nearest in-range doorway in front of the camera
	# (flattened dot >= SCAN_FACING_DOT). Facing the doorway centre OR the hub ScanZone (door["center"])
	# counts. Each target uses the same horizontal range, SCAN_ZONE_RANGE.
	# [EXIT-01] Both sides of every RFID door use the doorway-centre test. That centre is door root + (0, 1, 0).
	# Horizontal (XZ) distance from the player body must be <= SCAN_ZONE_RANGE, and abs(dy) <= 1.6 m so
	# another floor never qualifies. The ScanZone alternate is only the hub side of the doorway: the dock
	# pad looks at the hub, and the far side of the wall (qa_hub_01_far_side_of_wall_noop) stays a no-op.
	var fwd: Vector3 = (-_camera.global_transform.basis.z) if _camera != null else Vector3.FORWARD
	fwd.y = 0.0
	if fwd.length() < 0.001:
		return {}
	fwd = fwd.normalized()
	var body: Vector3 = _player_body.global_position if _player_body != null else origin
	var best: Dictionary = {}
	var best_d: float = INF
	for door: Dictionary in _rfid_doors:
		var droot: Node3D = door["root"] as Node3D
		if droot == null or not is_instance_valid(droot) or not droot.is_inside_tree():
			continue
		var target: Vector3 = droot.global_position + Vector3(0.0, 1.0, 0.0)
		var horiz: float = Vector2(body.x - target.x, body.z - target.z).length()
		var dy: float = absf(body.y - target.y)
		if horiz > SCAN_ZONE_RANGE or dy > 1.6 or horiz > best_d:
			continue
		if not _scan_faces_door_or_hub(fwd, body, target, droot, door):
			continue
		best_d = horiz
		best = door
	return best


func _scan_faces_point(fwd: Vector3, body: Vector3, point: Vector3) -> bool:
	var horiz: float = Vector2(body.x - point.x, body.z - point.z).length()
	if horiz > SCAN_ZONE_RANGE:
		return false
	var flat: Vector3 = point - body
	flat.y = 0.0
	if flat.length() <= 0.05:
		return true
	return fwd.dot(flat.normalized()) >= SCAN_FACING_DOT


func _scan_faces_door_or_hub(fwd: Vector3, body: Vector3, doorway: Vector3, droot: Node3D, door: Dictionary) -> bool:
	if _scan_faces_point(fwd, body, doorway):
		return true
	var hub_v: Variant = door.get("center", null)
	if not (hub_v is Vector3):
		return false
	var hub: Vector3 = hub_v as Vector3
	if not _scan_faces_point(fwd, body, hub):
		return false
	return _scan_on_hub_side(body, droot, hub)


## True when the body is on the same side of the door plane as the hub ScanZone (local +Z, basis.z).
func _scan_on_hub_side(body: Vector3, droot: Node3D, hub: Vector3) -> bool:
	var n: Vector3 = droot.global_transform.basis.z
	n.y = 0.0
	if n.length_squared() < 0.0000001:
		return true
	n = n.normalized()
	var origin: Vector3 = droot.global_position
	var player_side: float = (body.x - origin.x) * n.x + (body.z - origin.z) * n.z
	var hub_side: float = (hub.x - origin.x) * n.x + (hub.z - origin.z) * n.z
	return player_side * hub_side > 0.0


func _scan_rfid_doors(origin: Vector3) -> Array[String]:
	var opened_labels: Array[String] = []
	var door: Dictionary = _scan_target_door(origin)
	if door.is_empty():
		return opened_labels
	if String(door.get("ff_state", "")) == "stall":
		deny_flicker(String(door["id"]))
		opened_labels.append("%s (DENIED)" % String(door["id"]))
		return opened_labels
	if not bool(door["open"]):
		_set_door_open_state(door, true)
		opened_labels.append("%s (OPENED)" % String(door["id"]))
	else:
		# Close; the occupancy test (QA-FF-01) holds it open while anything (incl. the player) is in the opening.
		_set_door_open_state(door, false)
		if bool(door["close_pending"]):
			opened_labels.append("%s (CLOSE HELD: %s IN DOORWAY)" % [String(door["id"]), String(door["close_blocker"])])
		else:
			opened_labels.append("%s (CLOSED)" % String(door["id"]))
	return opened_labels


func _ff_tick_active_stalls(delta: float) -> void:
	for door: Dictionary in _rfid_doors:
		if String(door.get("ff_state", "")) == "stall":
			_ff_tick_stall(door, delta)


func _update_rfid_doors(delta: float) -> void:
	_update_hub_docks()
	for door: Dictionary in _rfid_doors:
		var st: String = String(door.get("ff_state", ""))
		if st == "deny":
			_ff_tick_deny(door, delta)
		elif st != "stall":
			door["dissolve"] = _door_dissolve(door)
		if bool(door["close_pending"]):
			door["close_retry_t"] = float(door["close_retry_t"]) - delta
			if float(door["close_retry_t"]) <= 0.0:
				_set_door_open_state(door, false)
	_door_json_poll_t += delta
	if _door_json_poll_t >= DOOR_FIELD_POLL_SEC:
		_door_json_poll_t = 0.0
		_poll_door_field_json()


func _door_field_json_path() -> String:
	# [QA-FF-06] poll BOTH res://config/door_fields.json (dev checkout; absent/unreadable in exports) and
	# user://door_fields.json in every run, and use whichever exists with the newer modified time.
	var best: String = ""
	var best_mt: int = -1
	for cand: String in [DOOR_FIELD_JSON_DEV, DOOR_FIELD_JSON_USER]:
		var ap: String = _resolve_path(cand)
		if FileAccess.file_exists(ap):
			var mt: int = int(FileAccess.get_modified_time(ap))
			if mt > best_mt:
				best_mt = mt
				best = cand
	if best != "":
		return best
	return DOOR_FIELD_JSON_DEV if OS.has_feature("editor") else DOOR_FIELD_JSON_USER


func _poll_door_field_json() -> void:
	# External Python UI writes DOOR_FIELD_JSON = {door_id|"ALL": {"opacity": f, "color": [r,g,b,a]}}.
	# Re-read only when the modified time changes (plus a short re-check window for same-second writes).
	var src: String = _door_field_json_path()
	var abs_p: String = _resolve_path(src)
	if not FileAccess.file_exists(abs_p):
		return
	var mt: int = int(FileAccess.get_modified_time(abs_p))
	if mt != _door_json_mtime or src != _door_json_src:
		_door_json_mtime = mt
		_door_json_src = src
		_door_json_recheck_until = _time + 1.5
	elif _time > _door_json_recheck_until:
		return
	var txt: String = FileAccess.get_file_as_string(abs_p)
	var hsh: int = txt.hash()
	if hsh == _door_json_hash:
		return
	_door_json_hash = hsh
	var n_applied: int = apply_door_field_overrides(JSON.parse_string(txt))
	print("[FORCEFIELD] applied %d door field override(s) from %s" % [n_applied, src])


func apply_door_field_overrides(data: Variant) -> int:
	if not (data is Dictionary):
		return 0
	var applied: int = 0
	var dd: Dictionary = data as Dictionary
	var keys: Array = dd.keys()
	keys.sort_custom(func(a: Variant, b: Variant) -> bool: return String(a) == "ALL" and String(b) != "ALL")
	for k: Variant in keys:
		var e: Variant = dd[k]
		if not (e is Dictionary):
			continue
		var ed: Dictionary = e as Dictionary
		var c_arr: Array = ed.get("color", [FF_DEFAULT_COLOR.r, FF_DEFAULT_COLOR.g, FF_DEFAULT_COLOR.b, 1.0]) as Array
		var col: Color = Color(float(c_arr[0]), float(c_arr[1]), float(c_arr[2]), float(c_arr[3]) if c_arr.size() > 3 else 1.0)
		var op: float = float(ed.get("opacity", FF_DEFAULT_OPACITY))
		var ids: Array[String] = []
		if String(k) == "ALL":
			for d: Dictionary in _rfid_doors:
				ids.append(String(d["id"]))
		else:
			ids.append(String(k))
		for id: String in ids:
			if set_door_field(id, op, col):
				applied += 1
	return applied


# ------------------------------------------------------------------------------
# [t45u] Force-field door screenshots (`-- --qa-forcefield-door`)
# ------------------------------------------------------------------------------
func _run_door_hub_shot() -> void:
	# [Bulkhead Hub] one in-game 1920x1080 shot of DOOR_RM1B: field door + hub + floor dock pad.
	if DisplayServer.get_name() != "headless":
		DisplayServer.window_set_size(Vector2i(1920, 1080))
	if _hud != null:
		_hud.visible = false
	_third_person = false
	_apply_view_mode()
	await _qa_frames(10)
	var door: Dictionary = _find_door("DOOR_RM1B")
	var droot: Node3D = door["root"] as Node3D
	var xf: Transform3D = droot.global_transform
	var fill: OmniLight3D = OmniLight3D.new()
	fill.position = xf * Vector3(1.0, 2.2, 1.9)
	fill.light_color = Color("#F2ECE2")
	fill.light_energy = 1.4
	fill.omni_range = 6.0
	add_child(fill)
	_qa_free_cam(xf * Vector3(0.55, 1.55, 2.75), xf * Vector3(0.85, 0.95, 0.0), Vector3.UP, 60.0)
	await _qa_idle(8)
	var img: Image = await _qa_capture("door_hub_ingame_rm1b.png")
	for did2: Dictionary in _rfid_doors:
		print("[HUB-SHOT] %s pad_lift=%.3f m" % [did2["id"], float(did2.get("pad_lift", -1.0))])
	fill.queue_free()
	print("[HUB-SHOT] DONE saved=%s" % (img != null))
	get_tree().quit(0 if img != null else 1)


func _run_forcefield_door_qa() -> void:
	if _camera == null:
		print("[FF-DOOR-QA] FAIL camera missing")
		get_tree().quit(1)
		return
	if DisplayServer.get_name() != "headless":
		DisplayServer.window_set_size(Vector2i(1920, 1080))
	if _hud != null:
		_hud.visible = false
	_third_person = false
	_apply_view_mode()
	await _qa_frames(10)
	var door: Dictionary = _find_door("DOOR_RM1B")
	var dpos: Vector3 = (door["root"] as Node3D).global_position
	var fill: OmniLight3D = OmniLight3D.new()
	fill.name = "FFDoorFillLight"
	fill.position = dpos + Vector3(-0.6, 2.25, -1.9)
	fill.light_color = Color("#F2ECE2")
	fill.light_energy = 1.6
	fill.omni_range = 7.0
	fill.shadow_enabled = true
	fill.shadow_bias = 0.03
	add_child(fill)
	var fill2: OmniLight3D = OmniLight3D.new()
	fill2.name = "FFDoorRimFill"
	fill2.position = dpos + Vector3(1.4, 1.2, -1.2)
	fill2.light_color = Color("#DCE6F0")
	fill2.light_energy = 0.55
	fill2.omni_range = 4.5
	add_child(fill2)
	_qa_free_cam(dpos + Vector3(-0.35, 1.40, -2.55), dpos + Vector3(0.10, 1.30, 0.0), Vector3.UP, 62.0)
	var saved: int = 0
	var shots: Array[Array] = [[0.0, "forcefield_door_closed.png"], [0.5, "forcefield_door_mid_dissolve.png"], [1.0, "forcefield_door_open.png"]]
	for sh: Array in shots:
		_set_door_dissolve_immediate(door, float(sh[0]))
		await _qa_idle(6)
		if await _qa_capture(String(sh[1])) != null:
			saved += 1
	_set_door_dissolve_immediate(door, 0.0)
	set_door_field("DOOR_RM1B", 0.4, Color(0.0, 1.0, 1.0, 1.0))
	await _qa_idle(6)
	if await _qa_capture("forcefield_door_custom_color.png") != null:
		saved += 1
	set_door_field("DOOR_RM1B", FF_DEFAULT_OPACITY, FF_DEFAULT_COLOR)
	fill.queue_free()
	fill2.queue_free()
	_qa_player_cam()
	print("[FF-DOOR-QA] Force-Field Doors")
	var checks_ok: bool = await _qa_forcefield_door_checks(door)
	print("[FF-DOOR-QA] DONE saved=%d/4" % saved)
	get_tree().quit(0 if saved == 4 and checks_ok else 1)


## Stall keeps the collider on at partial strength, a ray and a shape through the opening stay blocked,
## and a split field releases only after both halves have cycled back into sync.
func _qa_forcefield_door_checks(door: Dictionary) -> bool:
	var ok_all: bool = true
	var residential_single: bool = true
	for d: Dictionary in _rfid_doors:
		if bool(d.get("split", false)):
			residential_single = false
	if not _ff_qa_line("residential_not_split", residential_single, "doors=%d" % _rfid_doors.size()):
		ok_all = false

	var stalled: bool = stall_door("DOOR_RM1B", FF_STALL_TIME)
	var mat: ShaderMaterial = door.get("field_mat") as ShaderMaterial
	var op_lo: float = 1000.0
	var op_hi: float = -1.0
	var st_lo: float = 1000.0
	var st_hi: float = -1.0
	var sample_n: int = 0
	while sample_n < 4:
		# Several physics frames apart, so _physics_process runs _ff_tick_stall between reads.
		for _gap: int in range(4):
			await get_tree().physics_frame
		var op_s: float = _ff_shader_float(mat, "opacity", -1.0)
		var st_s: float = _ff_shader_float(mat, "static_strength", -1.0)
		op_lo = minf(op_lo, op_s)
		op_hi = maxf(op_hi, op_s)
		st_lo = minf(st_lo, st_s)
		st_hi = maxf(st_hi, st_s)
		sample_n += 1
	var strength: float = float(door.get("strength", -1.0))
	var partial: bool = op_lo > 0.05 and op_hi < FF_DEFAULT_OPACITY * 0.70 and st_lo > 0.50 and absf(strength - FF_STALL_STRENGTH) < 0.021
	var flickered: bool = (op_hi - op_lo) > 0.0008 or (st_hi - st_lo) > 0.0008
	var cs: CollisionShape3D = door.get("field_collider") as CollisionShape3D
	var collider_on: bool = cs != null and is_instance_valid(cs) and not cs.disabled
	var led: StandardMaterial3D = door.get("led_mat") as StandardMaterial3D
	var amber: bool = led != null and led.emission.is_equal_approx(HUB_AMBER)
	var stall_ok: bool = stalled and partial and flickered and collider_on and amber and String(door.get("ff_state", "")) == "stall"
	if not _ff_qa_line("stall_partial_collider_on", stall_ok, "samples=%d strength=%.2f opacity=%.3f..%.3f static=%.3f..%.3f collider_on=%s amber=%s" % [sample_n, strength, op_lo, op_hi, st_lo, st_hi, collider_on, amber]):
		ok_all = false
	var blocked: bool = _ff_opening_blocked(door, 0.0)
	if not _ff_qa_line("stall_ray_shape_blocked", blocked, "ray+shape through opening hit FieldCollider"):
		ok_all = false

	_ff_surge_from_stall(door)
	await _qa_frames(2)

	var pre_split: bool = not sync_collapse("DOOR_RM1B")
	if not _ff_qa_line("sync_before_split_refused", pre_split, "sync_collapse"):
		ok_all = false
	var split_on: bool = enable_split_field("DOOR_RM1B")
	await _qa_frames(3)
	var pre_cycle: bool = split_on and not sync_collapse("DOOR_RM1B")
	if not _ff_qa_line("sync_before_cycle_refused", pre_cycle, "split=%s synced=%s" % [split_on, bool(door.get("split_synced", false))]):
		ok_all = false
	var dropped: bool = set_split_half("DOOR_RM1B", "A", false)
	await _qa_frames(2)
	var mid_sync: bool = dropped and not sync_collapse("DOOR_RM1B")
	var b_blocks: bool = _ff_opening_blocked(door, 0.25)
	var a_clear: bool = not _ff_opening_blocked(door, -0.25)
	if not _ff_qa_line("split_half_holds_until_sync", mid_sync and b_blocks and a_clear, "B_blocked=%s A_clear=%s" % [b_blocks, a_clear]):
		ok_all = false
	var raised: bool = set_split_half("DOOR_RM1B", "A", true)
	var released: bool = raised and sync_collapse("DOOR_RM1B")
	if not _ff_qa_line("sync_collapse_when_synced", released, "both halves on after a drop"):
		ok_all = false
	await get_tree().create_timer(DOOR_DISSOLVE_TIME + 0.25).timeout
	await _qa_frames(3)
	var col_a: CollisionShape3D = door.get("col_a") as CollisionShape3D
	var col_b: CollisionShape3D = door.get("col_b") as CollisionShape3D
	var halves_off: bool = col_a != null and col_b != null and col_a.disabled and col_b.disabled
	var dissolved: bool = _door_dissolve(door) >= 0.999 and bool(door.get("open", false))
	var clear: bool = not _ff_opening_blocked(door, -0.25) and not _ff_opening_blocked(door, 0.25)
	if not _ff_qa_line("release_after_full_sync", dissolved and halves_off and clear, "dissolve=%.3f open=%s colliders_off=%s" % [_door_dissolve(door), bool(door.get("open", false)), halves_off]):
		ok_all = false
	var others: bool = true
	for d2: Dictionary in _rfid_doors:
		if String(d2.get("id", "")) != "DOOR_RM1B" and bool(d2.get("split", false)):
			others = false
	if not _ff_qa_line("other_doors_not_split", others, "split enabled on DOOR_RM1B only"):
		ok_all = false
	return ok_all


func _ff_qa_line(nm: String, ok: bool, detail: String) -> bool:
	print("[FF-DOOR-QA] %s | %s | %s" % ["PASS" if ok else "FAIL", nm, detail])
	return ok


func _qa_t38_check(nm: String, ok: bool, detail: String) -> void:
	var line: String = "%s | %s | %s" % ["PASS" if ok else "FAIL", nm, detail]
	print("[T38-QA] ", line)
	_qa_log.append(line)
	if not ok:
		_qa_failures += 1


func _run_reticle_stars_doors_qa() -> void:
	if _player_body == null or _camera == null:
		_qa_t38_check("setup", false, "player/camera missing")
		get_tree().quit(1)
		return
	if _hud_toast != null:
		_hud_toast.visible = false
	_third_person = false
	_apply_view_mode()
	await _qa_frames(15)

	# ---------------- 1. RETICLE / CROSSHAIR CENTERING & RAYCAST ALIGNMENT ----------------
	var stretch_mode: String = String(ProjectSettings.get_setting("display/window/stretch/mode", ""))
	var stretch_aspect: String = String(ProjectSettings.get_setting("display/window/stretch/aspect", ""))
	_qa_t38_check("reticle_project_stretch_settings", stretch_mode == "canvas_items" and stretch_aspect == "expand",
		"mode=%s aspect=%s" % [stretch_mode, stretch_aspect])

	var test_sizes: Array[Vector2i] = [Vector2i(1920, 1080), Vector2i(1600, 900), Vector2i(1280, 800), Vector2i(1920, 1080)]
	for sz: Vector2i in test_sizes:
		if DisplayServer.get_name() != "headless":
			DisplayServer.window_set_size(sz)
		else:
			get_viewport().size = sz
		await _qa_idle(3)
		_sync_reticle_to_viewport_center()
		var vp_sz: Vector2 = get_viewport().get_visible_rect().size
		var expected_c: Vector2 = vp_sz * 0.5
		var box_center: Vector2 = _reticle_box.position + _reticle_box.size * 0.5 if _reticle_box != null else Vector2(-999, -999)
		var err_px: float = box_center.distance_to(expected_c)
		var ray_dir: Vector3 = _camera.project_ray_normal(expected_c).normalized()
		var cam_fwd: Vector3 = (-_camera.global_transform.basis.z).normalized()
		var dot_align: float = ray_dir.dot(cam_fwd)
		_qa_t38_check("reticle_centered_%dx%d" % [sz.x, sz.y], err_px < 0.01 and dot_align > 0.999999,
			"vp=%s reticle_center=%s expected=%s err=%.4f px ray_dot=%.8f" % [str(vp_sz), str(box_center), str(expected_c), err_px, dot_align])

	# [REV-C2] Aim inside APT 201 at the open floor (workbench removed) and capture reticle centered check
	_qa_place(Vector3(-8.50, 4.30, 6.10), 180.0, -10.0)
	await _qa_frames(15)
	_sync_reticle_to_viewport_center()
	await _qa_capture("qa_reticle_centered_check.png")

	# ---------------- 2. ROTATING DISTANT STARFIELD CYLINDER vs STATIONARY VESSEL ----------------
	var hab_world: Node3D = _arch_container.get_node_or_null("CylinderHab7_FullScale_World") as Node3D
	var star_barrel: MeshInstance3D = _starfield_cylinder.get_node_or_null("StarfieldOuterBarrelMesh") as MeshInstance3D if _starfield_cylinder != null else null
	var star_cyl_mesh: CylinderMesh = star_barrel.mesh as CylinderMesh if star_barrel != null else null
	var star_r: float = star_cyl_mesh.top_radius if star_cyl_mesh != null else 0.0
	var star_l: float = star_cyl_mesh.height if star_cyl_mesh != null else 0.0
	_qa_t38_check("starfield_outer_cylinder_geometry", _starfield_cylinder != null and star_r >= 1800.0 and star_l >= 4000.0 and _camera.far >= 5000.0,
		"exists=%s R=%.1f m L=%.1f m camera_far=%.1f m" % [_starfield_cylinder != null, star_r, star_l, _camera.far])

	# Promenade deck, looking along the cylinder axis (world +X, yaw -90) toward the end-cap starfield vista.
	_qa_place(Vector3(0.0, 0.25, -32.0), -90.0, 12.0)
	await _qa_frames(15)
	var hab_xf0: Transform3D = hab_world.global_transform if hab_world != null else Transform3D.IDENTITY
	var star_rot0: float = _starfield_cylinder.rotation.x if _starfield_cylinder != null else 0.0
	var img_star1: Image = await _qa_capture("qa_outer_starfield_rotating_1.png")
	await _qa_frames(90)
	var hab_xf1: Transform3D = hab_world.global_transform if hab_world != null else Transform3D.IDENTITY
	var star_rot1: float = _starfield_cylinder.rotation.x if _starfield_cylinder != null else 0.0
	# Advance starfield rotation by an extra visual arc so the two screenshots clearly show star rotation
	if _starfield_cylinder != null:
		_starfield_cylinder.rotate_x(deg_to_rad(14.0))
	var img_star2: Image = await _qa_capture("qa_outer_starfield_rotating_2.png")
	var d_star_rot: float = absf(star_rot1 - star_rot0)
	var d_hab_pos: float = hab_xf0.origin.distance_to(hab_xf1.origin)
	var d_hab_rot: float = hab_xf0.basis.get_rotation_quaternion().angle_to(hab_xf1.basis.get_rotation_quaternion())
	_qa_t38_check("starfield_rotates_while_vessel_stationary", d_star_rot > 0.04 and d_hab_pos < 0.0001 and d_hab_rot < 0.0001,
		"star_drot=%.4f rad (%.2f deg) hab_dpos=%.6f hab_drot=%.6f" % [d_star_rot, rad_to_deg(d_star_rot), d_hab_pos, d_hab_rot])
	if img_star1 != null and img_star2 != null:
		var star_diff: int = 0
		for py: int in range(60, 420, 8):
			for px: int in range(560, 1360, 8):
				if img_star1.get_pixel(px, py).to_abgr32() != img_star2.get_pixel(px, py).to_abgr32():
					star_diff += 1
		_qa_t38_check("starfield_pixels_visible_and_moving", star_diff > 15, "changed_sky_sample_pixels=%d" % star_diff)

	# Normal play: on the deck, looking through the observation window. The drum stays visible and does not spin.
	# _qa_place yaw is body yaw (0 faces -Z: atan2(-dir.x, -dir.z)). Pitch is the camera-pivot X rotation.
	# _apply_pitch clamps first person to PITCH_MIN_DEG..PITCH_MAX_DEG (-80..75). Eye is the camera pivot (1.62 m).
	var axis_point: Vector3 = Vector3(0.0, 187.2, 0.0)
	var win_dw: Vector3 = Vector3(0.0, cos(deg_to_rad(60.0)), -sin(deg_to_rad(60.0)))
	var window_p: Vector3 = axis_point + win_dw * 200.0
	var eye: Vector3 = Vector3(0.0, 0.25 + 1.50 + 0.12, -20.0)
	var aim: Vector3 = window_p - eye
	if aim.length_squared() > 0.0000001:
		aim = aim.normalized()
	var win_yaw: float = rad_to_deg(atan2(-aim.x, -aim.z))
	var win_pitch: float = rad_to_deg(asin(clampf(aim.y, -1.0, 1.0)))
	win_pitch = clampf(win_pitch, PITCH_MIN_DEG, PITCH_MAX_DEG)
	_qa_place(Vector3(0.0, 0.25, -20.0), win_yaw, win_pitch)
	await _qa_frames(15)
	var img_win1: Image = await _qa_capture("qa_window_starfield_1.png")
	await _qa_frames(120)
	if _starfield_cylinder != null:
		_starfield_cylinder.rotate_x(deg_to_rad(6.0))
	var img_win2: Image = await _qa_capture("qa_window_starfield_2.png")
	if img_win1 != null and img_win2 != null and img_win1.get_width() > 0 and img_win1.get_height() > 0 and img_win2.get_width() > 0 and img_win2.get_height() > 0:
		var ww: int = mini(img_win1.get_width(), img_win2.get_width())
		var wh: int = mini(img_win1.get_height(), img_win2.get_height())
		var win_diff: int = 0
		# Central band of a 1920x1080 frame (x 560..1360, y 160..760, step 8). Smaller images use the same fractions.
		for y_ref: int in range(160, 760, 8):
			var pyw: int = clampi(int(round(float(y_ref) * float(wh) / 1080.0)), 0, wh - 1)
			for x_ref: int in range(560, 1360, 8):
				var pxw: int = clampi(int(round(float(x_ref) * float(ww) / 1920.0)), 0, ww - 1)
				if img_win1.get_pixel(pxw, pyw).to_abgr32() != img_win2.get_pixel(pxw, pyw).to_abgr32():
					win_diff += 1
		_qa_t38_check("window_starfield_visible_and_moving", win_diff > 15, "changed_window_pixels=%d" % win_diff)

	# ---------------- 3. [t45u] ALL 6 RFID FORCE-FIELD DOORS ----------------
	_qa_t38_check("rfid_doors_count_6", _rfid_doors.size() == 6, "door_count=%d" % _rfid_doors.size())
	var door_img_closed: Image = null
	var door_img_opened: Image = null
	for i: int in range(_rfid_doors.size()):
		var door: Dictionary = _rfid_doors[i]
		var did: String = String(door["id"])
		var dpos: Vector3 = (door["root"] as Node3D).global_position
		var fcs: CollisionShape3D = door["field_collider"] as CollisionShape3D
		var lm: StandardMaterial3D = door["led_mat"] as StandardMaterial3D
		var fm: ShaderMaterial = door["field_mat"] as ShaderMaterial
		_set_door_dissolve_immediate(door, 0.0)
		await _qa_frames(4)
		_qa_t38_check("%s_forcefield_shader_material" % did.to_lower(), fm != null and fm.shader != null and fm.shader.code.contains("uniform float dissolve") and (fm.get_shader_parameter("field_color") as Color).is_equal_approx(FF_DEFAULT_COLOR),
			"shader=%s field_color=%s" % [FORCEFIELD_DOOR_SHADER, (fm.get_shader_parameter("field_color") as Color).to_html()])
		# [Bulkhead Hub] present at the door-local mount offset, [E] target is its ScanZone, 8 glow parts amber
		var hub_n: Node3D = door.get("hub") as Node3D
		var exp_xf: Transform3D = (door["root"] as Node3D).global_transform * Transform3D(Basis.IDENTITY, HUB_MOUNT_OFFSET + Vector3(0.0, 0.0, HUB_WALL_STANDOFF))
		var seat_m: float = float(door.get("hub_seat", 0.0))
		var shift_m: float = float(door.get("hub_tangent_shift", 0.0))
		var back_dir: Vector3 = -exp_xf.basis.z
		if back_dir.length_squared() > 0.0000001:
			back_dir = back_dir.normalized()
		var tangent_dir: Vector3 = exp_xf.basis.x
		if tangent_dir.length_squared() > 0.0000001:
			tangent_dir = tangent_dir.normalized()
		var exp_pos: Vector3 = exp_xf.origin + back_dir * seat_m + tangent_dir * shift_m
		var hub_err: float = hub_n.global_position.distance_to(exp_pos) if hub_n != null else 99.0
		var hub_rot_err: float = hub_n.global_transform.basis.get_rotation_quaternion().angle_to(exp_xf.basis.get_rotation_quaternion()) if hub_n != null else 9.0
		var scan_target: String = ""
		for it_q: Dictionary in _interactables:
			if String(it_q["kind"]) == "rfid_door" and String(it_q.get("door_id", "")) == did:
				scan_target = String((it_q["node"] as Node).name)
		_qa_t38_check("%s_bulkhead_hub_mounted" % did.to_lower(), hub_n != null and hub_err < 0.001 and hub_rot_err < 0.001 and scan_target == "ScanZone",
			"hub=%s pos_err=%.4f m rot_err=%.4f offset=%s+standoff %.3f seat=%.4f shift=%.4f scan_target=%s" % [hub_n.name if hub_n != null else "MISSING", hub_err, hub_rot_err, str(HUB_MOUNT_OFFSET), HUB_WALL_STANDOFF, seat_m, shift_m, scan_target])
		var back_miss: int = _hub_backing_misses(door, HUB_BACKING_MAX_GAP)
		_qa_t38_check("%s_hub_solid_wall_behind_5cm" % did.to_lower(), back_miss == 0,
			"seating grid 9 rays from hub face: misses=%d backing_panel_added=%s" % [back_miss, door.get("backing_added", false)])
		var glow_amber: bool = (door["glow_nodes"] as Array).size() == 8
		for gn0: Variant in door["glow_nodes"]:
			glow_amber = glow_amber and (gn0 as MeshInstance3D).material_override == lm
		_qa_t38_check("%s_closed_state" % did.to_lower(), _door_dissolve(door) == 0.0 and fcs != null and not fcs.disabled and lm.emission.is_equal_approx(HUB_AMBER) and glow_amber,
			"dissolve=%.3f collision_on=%s light=%s" % [_door_dissolve(door), fcs != null and not fcs.disabled, lm.emission.to_html(false)])
		# Same side test as the door mount: north-wall doors are approached from the corridor (smaller z).
		var from_south: bool = did != "DOOR_SECTOR4_EXIT" and dpos.z > 0.0
		var start_z: float = (dpos.z - 1.55) if from_south else (dpos.z + 1.55)
		# Corridor clear is z -0.8..0.8. A 1.55 m offset plus the 0.35 m capsule hits the far wall.
		# ±0.40 leaves 5 cm between the capsule and the wall face.
		if absf(dpos.z) <= 1.2:
			start_z = clampf(start_z, -0.40, 0.40)
		var yaw_deg: float = 180.0 if from_south else 0.0
		_qa_place(Vector3(dpos.x, dpos.y + 0.05, start_z), yaw_deg, -4.0)
		await _qa_frames(12)
		if did == "DOOR_APT201":
			door_img_closed = await _qa_capture("qa_rfid_door_apt201_closed.png")
		# Walk into the closed field: its collider must stop the player before dpos.z
		_qa_key(KEY_W, true)
		await _qa_idle(2)
		await _qa_frames(28)
		_qa_key(KEY_W, false)
		await _qa_idle(2)
		var z_blocked: float = _player_body.global_position.z
		var blocked_ok: bool = (z_blocked < dpos.z - 0.30) if from_south else (z_blocked > dpos.z + 0.30)
		_qa_t38_check("%s_blocks_when_closed" % did.to_lower(), blocked_ok and not bool(door["open"]),
			"door_z=%.2f player_stopped_at_z=%.2f open=%s" % [dpos.z, z_blocked, door["open"]])
		# [E] hub scan -> dissolve tween 0->1 over 0.8 s, then collision off + light green
		# [QA-HUB-01] scans now need to be within 1.4 m of (and facing) the hub ScanZone
		var scan_spot: Vector3 = _qa_follow_hub_seat(door, Vector3(0.80, 0.05, 1.0))
		_qa_place(scan_spot, yaw_deg, -4.0)
		await _qa_frames(6)
		Engine.time_scale = 0.05  # slow the 0.8 s tween so a mid-dissolve sample is reliable under xvfb
		await _qa_tap(KEY_E)
		await _qa_idle(1)
		var mid_d: float = _door_dissolve(door)
		var mid_light_amber: bool = not lm.emission.is_equal_approx(FF_LIGHT_GREEN)  # glow still tweening toward green
		var mid_coll: bool = fcs != null and not fcs.disabled
		Engine.time_scale = 1.0
		await get_tree().create_timer(1.0).timeout
		await _qa_frames(3)
		var d_open: float = _door_dissolve(door)
		var opened_ok: bool = bool(door["open"]) and d_open >= 0.999 and fcs != null and fcs.disabled and lm.emission.is_equal_approx(FF_LIGHT_GREEN)
		_qa_t38_check("%s_E_scan_dissolves_open" % did.to_lower(), opened_ok and mid_d > 0.0 and mid_d < 1.0 and mid_light_amber and mid_coll,
			"during_tween dissolve=%.3f glow_not_yet_green=%s collision_on=%s | after dissolve=%.3f collision_off=%s light=%s" % [mid_d, mid_light_amber, mid_coll, d_open, fcs != null and fcs.disabled, lm.emission.to_html(false)])
		var glow_green: bool = (door["glow_nodes"] as Array).size() == 8 and lm.emission.is_equal_approx(FF_LIGHT_GREEN)
		for gn1: Variant in door["glow_nodes"]:
			glow_green = glow_green and (gn1 as MeshInstance3D).material_override == lm
		_qa_t38_check("%s_hub_8_glow_parts_green_on_grant" % did.to_lower(), glow_green, "parts=%d emission=%s" % [(door["glow_nodes"] as Array).size(), lm.emission.to_html(false)])
		if did == "DOOR_APT201":
			door_img_opened = await _qa_capture("qa_rfid_door_apt201_opened.png")
		_qa_place(Vector3(dpos.x, dpos.y + 0.05, start_z), yaw_deg, -4.0)
		await _qa_frames(4)
		_qa_key(KEY_W, true)
		await _qa_idle(2)
		await _qa_frames(42)
		_qa_key(KEY_W, false)
		await _qa_idle(2)
		var z_through: float = _player_body.global_position.z
		var through_ok: bool = (z_through > dpos.z + 0.45) if from_south else (z_through < dpos.z - 0.45)
		_qa_t38_check("%s_walk_through_when_open" % did.to_lower(), through_ok,
			"door_z=%.2f player_crossed_to_z=%.2f" % [dpos.z, z_through])
		# Close: step back out to the hub and [E] again -> dissolve 1->0, collision on, amber
		_qa_place(scan_spot, yaw_deg, -4.0)
		await _qa_frames(6)
		await _qa_tap(KEY_E)
		await get_tree().create_timer(1.0).timeout
		await _qa_frames(3)
		var closed_ok: bool = not bool(door["open"]) and _door_dissolve(door) <= 0.001 and fcs != null and not fcs.disabled and lm.emission.is_equal_approx(HUB_AMBER)
		_qa_t38_check("%s_E_scan_closes_back_glow_amber" % did.to_lower(), closed_ok,
			"dissolve=%.3f collision_on=%s light=%s" % [_door_dissolve(door), fcs != null and not fcs.disabled, lm.emission.to_html(false)])

	# [REAL-03] zone labels: room names only inside the enclosed room interiors
	var zone_ok: bool = true
	var zone_desc: PackedStringArray = PackedStringArray()
	for zc: Array in [[Vector3(-8.5, 0.3, 5.4), "RM 1A", true], [Vector3(-8.5, 0.3, 2.2), "RM 1A", false], [Vector3(-13.2, 0.3, 5.0), "RM 1A", false],
			[Vector3(4.5, 0.3, 5.4), "RM 1B", true], [Vector3(4.5, 0.3, 2.2), "RM 1B", false], [Vector3(-2.0, 0.3, 5.0), "RM 1", false]]:
		var zn: String = _zone_name(zc[0] as Vector3)
		var ok_z: bool = zn.begins_with(String(zc[1])) == bool(zc[2])
		zone_ok = zone_ok and ok_z
		zone_desc.append("%s->'%s'" % [str(zc[0]), zn])
	_qa_t38_check("real_03_room_zone_labels_interior_only", zone_ok, " | ".join(zone_desc))
	# [REAL-02] rays across the L2 landing-edge rail hit its collider (glass layer only).
	var space_g: PhysicsDirectSpaceState3D = get_world_3d().direct_space_state
	var g_hits: PackedStringArray = PackedStringArray()
	var g_ok: bool = true
	var g_rays: Array[Array] = []
	for gx: float in [-1.5, -0.76, 0.1]:
		g_rays.append([Vector3(gx, 4.8, -5.2), Vector3(gx, 4.8, -4.4), "MezzanineGlassBalustrade_L2Edge"])
	for gr: Array in g_rays:
		var rqg: PhysicsRayQueryParameters3D = PhysicsRayQueryParameters3D.create(gr[0] as Vector3, gr[1] as Vector3, GLASS_QA_LAYER_BIT)
		rqg.exclude = [_player_body.get_rid()]
		var hg: Dictionary = space_g.intersect_ray(rqg)
		var hname: String = String((hg["collider"] as Node).name) if not hg.is_empty() else "none"
		g_ok = g_ok and hname == String(gr[2])
		g_hits.append("%s@%s hit=%s" % [String(gr[2]).trim_prefix("MezzanineGlassBalustrade_"), str(gr[0]), hname])
	_qa_t38_check("real_02_glass_balustrade_collider_hit", g_ok, ", ".join(g_hits))

	# [QA-HUB-01] single-target scan: RM1B only (APT202 upstairs untouched), facing away / out of range = no-op
	var h_rb: Dictionary = _find_door("DOOR_RM1B")
	var h_up: Dictionary = _find_door("DOOR_APT202")
	for dq: Dictionary in _rfid_doors:
		_set_door_dissolve_immediate(dq, 0.0)
	var h_xf: Transform3D = (h_rb["root"] as Node3D).global_transform
	var rb_front: Vector3 = _qa_follow_hub_seat(h_rb, Vector3(0.80, 0.05, 1.0))
	_qa_place(rb_front, 180.0, -4.0)
	await _qa_frames(6)
	_update_hud()
	var prompt_txt: String = _hud_prompt.text if _hud_prompt != null else ""
	await _qa_tap(KEY_E)
	await get_tree().create_timer(1.0).timeout
	var n_open: int = 0
	for dq2: Dictionary in _rfid_doors:
		if bool(dq2["open"]):
			n_open += 1
	_qa_t38_check("qa_hub_01_scan_toggles_only_rm1b", bool(h_rb["open"]) and not bool(h_up["open"]) and _door_dissolve(h_up) == 0.0 and n_open == 1 and prompt_txt.contains("RM 1B") and prompt_txt.ends_with("OPEN"),
		"rm1b_open=%s apt202_open=%s apt202_dissolve=%.2f doors_open=%d prompt='%s'" % [h_rb["open"], h_up["open"], _door_dissolve(h_up), n_open, prompt_txt])
	# Held close via a real scan while a bot stands in the opening
	var h_bot: Node3D = _actors_container.get_node_or_null("Hammerhead05_Kelvin_0204_Science") as Node3D
	if h_bot != null:
		var h_home: Vector3 = h_bot.global_position
		h_bot.global_position = (h_rb["root"] as Node3D).global_position
		await _qa_tap(KEY_E)
		await _qa_frames(3)
		var held_scan: bool = bool(h_rb["close_pending"]) and bool(h_rb["open"])
		h_bot.global_position = h_home
		await get_tree().create_timer(0.6 + DOOR_DISSOLVE_TIME + 0.3).timeout
		_qa_t38_check("qa_hub_01_scan_close_held_while_occupied", held_scan and not bool(h_rb["open"]) and _door_dissolve(h_rb) <= 0.001,
			"held=%s then open=%s dissolve=%.3f" % [held_scan, h_rb["open"], _door_dissolve(h_rb)])
	_set_door_dissolve_immediate(h_rb, 0.0)
	_qa_place(rb_front, 0.0, -4.0)  # facing away from the hub
	await _qa_frames(6)
	_update_hud()
	var prompt_away: String = _hud_prompt.text if _hud_prompt != null else ""
	await _qa_tap(KEY_E)
	await get_tree().create_timer(0.4).timeout
	_qa_t38_check("qa_hub_01_facing_away_noop", not bool(h_rb["open"]) and _door_dissolve(h_rb) == 0.0 and not prompt_away.contains("RFID SCAN"),
		"rm1b_open=%s dissolve=%.2f prompt='%s'" % [h_rb["open"], _door_dissolve(h_rb), prompt_away])
	_qa_place(h_xf * Vector3(0.80, 0.05, 2.70), 180.0, -4.0)  # ~2.3 m from the ScanZone, facing it
	await _qa_frames(6)
	var far_d: float = _player_probe_point().distance_to(h_rb["center"] as Vector3)
	await _qa_tap(KEY_E)
	await get_tree().create_timer(0.4).timeout
	var any_open: bool = false
	for dq3: Dictionary in _rfid_doors:
		any_open = any_open or bool(dq3["open"])
	_qa_t38_check("qa_hub_01_out_of_range_noop", not any_open and far_d > SCAN_ZONE_RANGE, "dist=%.2f m any_door_open=%s" % [far_d, any_open])
	# Far side of the wall (inside RM1B, facing the hub through the wall): no-op
	_qa_place(h_xf * Vector3(0.95, 0.05, -0.55), 0.0, -4.0)  # behind the wall, ~0.75 m from the ScanZone, facing it
	await _qa_frames(6)
	var far_side_d: float = _player_probe_point().distance_to(h_rb["center"] as Vector3)
	await _qa_tap(KEY_E)
	await get_tree().create_timer(0.4).timeout
	_qa_t38_check("qa_hub_01_far_side_of_wall_noop", not bool(h_rb["open"]) and _door_dissolve(h_rb) == 0.0 and far_side_d < SCAN_ZONE_RANGE,
		"dist=%.2f m (in range) rm1b_open=%s" % [far_side_d, h_rb["open"]])
	# [E] at the hub with a pickup in reach: door toggles, nothing is picked up
	var pk: Dictionary = {}
	for itp: Dictionary in _interactables:
		if bool(itp["pickup"]) and not bool(itp["collected"]) and is_instance_valid(itp["node"]):
			pk = itp
			break
	var hub_spot: Vector3 = rb_front
	if not pk.is_empty():
		var pk_node: Node3D = pk["node"] as Node3D
		var pk_home: Vector3 = pk_node.global_position
		var inv_snapshot: String = str(_inventory)
		_qa_place(hub_spot, 180.0, -4.0)
		pk_node.global_position = hub_spot + Vector3(0.0, 1.0, -0.35)
		await _qa_frames(4)
		var pk_in_reach: bool = not _find_nearest_interactable(INTERACT_RANGE).is_empty() and bool(_find_nearest_interactable(INTERACT_RANGE)["pickup"])
		await _qa_tap(KEY_E)
		await get_tree().create_timer(1.0).timeout
		var not_picked: bool = not bool(pk["collected"]) and str(_inventory) == inv_snapshot
		_qa_t38_check("qa_hub_01_E_toggles_door_not_pickup", bool(h_rb["open"]) and not_picked and pk_in_reach,
			"rm1b_open=%s pickup=%s in_reach=%s collected=%s inventory_unchanged=%s" % [h_rb["open"], String(pk["label"]), pk_in_reach, pk["collected"], str(_inventory) == inv_snapshot])
		pk_node.global_position = pk_home
	else:
		_qa_t38_check("qa_hub_01_E_toggles_door_not_pickup", false, "no live pickup to test with")
	# Player standing on the Sprocket dock pad can close the door (pad is outside the thin occupancy box)
	_set_door_dissolve_immediate(h_rb, 1.0)
	var pad_pos: Vector3 = (h_rb["dock_marker"] as Marker3D).global_position
	_qa_place(pad_pos, 180.0, -4.0)
	await _qa_frames(6)
	await _qa_tap(KEY_E)
	await get_tree().create_timer(1.1).timeout
	_qa_t38_check("qa_hub_01_player_on_dock_pad_can_close", not bool(h_rb["open"]) and not bool(h_rb["close_pending"]) and _door_dissolve(h_rb) <= 0.001,
		"open=%s pending=%s blocker='%s' dissolve=%.3f dist_to_scanzone=%.2f" % [h_rb["open"], h_rb["close_pending"], String(h_rb["close_blocker"]), _door_dissolve(h_rb), _player_probe_point().distance_to(h_rb["center"] as Vector3)])

	# [QA-FF-01] close is held while a bot / rigid body is in the opening, then completes once it is clear
	var ob_door: Dictionary = _find_door("DOOR_RM1B")
	var ob_root: Node3D = ob_door["root"] as Node3D
	var ob_cs: CollisionShape3D = ob_door["field_collider"] as CollisionShape3D
	var bot: Node3D = _actors_container.get_node_or_null("Hammerhead05_Kelvin_0204_Science") as Node3D
	_qa_place(Vector3(0.0, 0.25, -6.0), 0.0, 0.0)
	await _qa_frames(4)
	if bot != null:
		var bot_home: Vector3 = bot.global_position
		_set_door_dissolve_immediate(ob_door, 1.0)
		await _qa_frames(3)
		bot.global_position = ob_root.global_position + Vector3(0.0, -0.06, 0.0)
		_set_door_open_state(ob_door, false)
		await get_tree().create_timer(1.3).timeout
		var held_ok: bool = bool(ob_door["close_pending"]) and bool(ob_door["open"]) and _door_dissolve(ob_door) >= 0.999 and ob_cs.disabled
		_qa_t38_check("qa_ff_01_close_held_while_bot_in_doorway", held_ok,
			"blocker=%s pending=%s open=%s dissolve=%.3f collision_off=%s (after 1.3 s, 2 retries)" % [String(ob_door["close_blocker"]), ob_door["close_pending"], ob_door["open"], _door_dissolve(ob_door), ob_cs.disabled])
		bot.global_position = bot_home
		await get_tree().create_timer(0.6 + DOOR_DISSOLVE_TIME + 0.3).timeout
		await _qa_frames(3)
		var lm1: StandardMaterial3D = ob_door["led_mat"] as StandardMaterial3D
		_qa_t38_check("qa_ff_01_closes_once_bot_clear", not bool(ob_door["close_pending"]) and not bool(ob_door["open"]) and _door_dissolve(ob_door) <= 0.001 and not ob_cs.disabled and lm1.emission.is_equal_approx(HUB_AMBER),
			"pending=%s open=%s dissolve=%.3f collision_on=%s light=%s" % [ob_door["close_pending"], ob_door["open"], _door_dissolve(ob_door), not ob_cs.disabled, lm1.emission.to_html(false)])
	else:
		_qa_t38_check("qa_ff_01_close_held_while_bot_in_doorway", false, "Kelvin bot missing")
	# Rigid body (crate) in the opening
	var crate: RigidBody3D = RigidBody3D.new()
	crate.name = "QA_DoorwayCrate"
	crate.freeze = true
	var crate_cs: CollisionShape3D = CollisionShape3D.new()
	var crate_bs: BoxShape3D = BoxShape3D.new()
	crate_bs.size = Vector3(0.4, 0.4, 0.4)
	crate_cs.shape = crate_bs
	crate.add_child(crate_cs)
	add_child(crate)
	_set_door_dissolve_immediate(ob_door, 1.0)
	crate.global_position = ob_root.global_position + Vector3(0.3, 0.25, 0.0)
	await _qa_frames(4)
	_set_door_open_state(ob_door, false)
	await _qa_frames(2)
	var crate_held: bool = bool(ob_door["close_pending"]) and bool(ob_door["open"]) and String(ob_door["close_blocker"]) == "QA_DoorwayCrate"
	crate.queue_free()
	await get_tree().create_timer(0.6 + DOOR_DISSOLVE_TIME + 0.3).timeout
	await _qa_frames(3)
	_qa_t38_check("qa_ff_01_rigidbody_blocks_then_closes", crate_held and not bool(ob_door["open"]) and _door_dissolve(ob_door) <= 0.001 and not ob_cs.disabled,
		"held_by=%s then open=%s dissolve=%.3f collision_on=%s" % ["QA_DoorwayCrate" if crate_held else "none", ob_door["open"], _door_dissolve(ob_door), not ob_cs.disabled])

	# [Bulkhead Hub] coupler arm stowed by default on all 6; deploys when Sprocket parks on the dock pad
	var all_stowed: bool = true
	for dz: Dictionary in _rfid_doors:
		var pz: Node3D = dz["arm_pivot"] as Node3D
		all_stowed = all_stowed and pz != null and absf(pz.rotation_degrees.y - HUB_ARM_STOWED_DEG) < 0.5 and not bool(dz["arm_deployed"])
	_qa_t38_check("hub_coupler_arm_stowed_by_default_x6", all_stowed, "stowed_deg=%.1f" % HUB_ARM_STOWED_DEG)
	var spr: Node3D = _actors_container.get_node_or_null(SPROCKET_NODE) as Node3D
	var rb_door: Dictionary = _find_door("DOOR_RM1B")
	var rb_piv: Node3D = rb_door["arm_pivot"] as Node3D
	if spr != null:
		var spr_home: Transform3D = spr.global_transform
		var mk_rb: Marker3D = rb_door["dock_marker"] as Marker3D
		spr.global_transform = mk_rb.global_transform
		await get_tree().create_timer(0.9).timeout
		var dep_deg: float = rb_piv.rotation_degrees.y
		var dep_ok: bool = bool(rb_door["arm_deployed"]) and absf(dep_deg) < 0.5
		spr.global_transform = spr_home
		await get_tree().create_timer(0.9).timeout
		_qa_t38_check("hub_arm_deploys_on_sprocket_dock_rm1b", dep_ok and not bool(rb_door["arm_deployed"]) and absf(rb_piv.rotation_degrees.y - HUB_ARM_STOWED_DEG) < 0.5,
			"marker=%s parked_deg=%.1f after_leave_deg=%.1f" % [mk_rb.name, dep_deg, rb_piv.rotation_degrees.y])
	else:
		_qa_t38_check("hub_arm_deploys_on_sprocket_dock_rm1b", false, "Sprocket node missing")
	var a2: Dictionary = _find_door("DOOR_APT201")
	sprocket_dock("DOOR_APT201", true)
	await get_tree().create_timer(0.9).timeout
	var hook_deg: float = (a2["arm_pivot"] as Node3D).rotation_degrees.y
	sprocket_dock("DOOR_APT201", false)
	await get_tree().create_timer(0.9).timeout
	_qa_t38_check("hub_sprocket_dock_hook", absf(hook_deg) < 0.5 and absf((a2["arm_pivot"] as Node3D).rotation_degrees.y - HUB_ARM_STOWED_DEG) < 0.5,
		"hook parked_deg=%.1f released_deg=%.1f" % [hook_deg, (a2["arm_pivot"] as Node3D).rotation_degrees.y])

	# set_door_field(): opacity clamp + field colour + emitter tint, per-door material isolation, JSON override path
	var d0: Dictionary = _find_door("DOOR_RM1B")
	var d1: Dictionary = _find_door("DOOR_RM1A")
	var cyan: Color = Color(0.0, 1.0, 1.0, 1.0)
	var ok_set: bool = set_door_field("DOOR_RM1B", 0.4, cyan)
	var m0: ShaderMaterial = d0["field_mat"] as ShaderMaterial
	var em_ok: bool = (d0["emit_mats"] as Dictionary).size() == 3
	var em_desc: PackedStringArray = PackedStringArray()
	for en2: String in (d0["emit_mats"] as Dictionary).keys():
		var e0: StandardMaterial3D = (d0["emit_mats"] as Dictionary)[en2] as StandardMaterial3D
		em_ok = em_ok and e0.emission.is_equal_approx(cyan) and is_equal_approx(e0.emission_energy_multiplier, float(FF_EMITTER_ENERGY[en2]))
		em_desc.append("%s=%s@%.1f" % [en2, e0.emission.to_html(false), e0.emission_energy_multiplier])
	var op0: float = float(m0.get_shader_parameter("opacity"))
	var c0: Color = m0.get_shader_parameter("field_color") as Color
	var other_op: float = float((d1["field_mat"] as ShaderMaterial).get_shader_parameter("opacity"))
	_qa_t38_check("set_door_field_opacity_color_emitter", ok_set and is_equal_approx(op0, 0.4) and c0.is_equal_approx(cyan) and em_ok and is_equal_approx(other_op, FF_DEFAULT_OPACITY),
		"opacity=%.3f color=%s emitters[%s] other_door_opacity=%.3f" % [op0, c0.to_html(), ", ".join(em_desc), other_op])
	set_door_field("DOOR_RM1B", 7.0, cyan)
	var op_hi: float = float(m0.get_shader_parameter("opacity"))
	set_door_field("DOOR_RM1B", -3.0, cyan)
	var op_lo: float = float(m0.get_shader_parameter("opacity"))
	_qa_t38_check("set_door_field_clamps_opacity", is_equal_approx(op_hi, 1.0) and is_equal_approx(op_lo, 0.0), "7.0->%.2f -3.0->%.2f" % [op_hi, op_lo])
	var n_json: int = apply_door_field_overrides(JSON.parse_string('{"ALL": {"opacity": 0.45, "color": [0.45, 0.92, 1.0, 1.0]}, "DOOR_RM1A": {"opacity": 0.7, "color": [1.0, 0.2, 0.6, 1.0]}}'))
	var op_a: float = float((d1["field_mat"] as ShaderMaterial).get_shader_parameter("opacity"))
	_qa_t38_check("door_field_json_overrides", n_json == 7 and is_equal_approx(op_a, 0.7) and is_equal_approx(float(m0.get_shader_parameter("opacity")), 0.45),
		"applied=%d rm1a_opacity=%.2f rm1b_opacity=%.2f json=%s" % [n_json, op_a, float(m0.get_shader_parameter("opacity")), _door_field_json_path()])
	apply_door_field_overrides({"ALL": {"opacity": FF_DEFAULT_OPACITY, "color": [FF_DEFAULT_COLOR.r, FF_DEFAULT_COLOR.g, FF_DEFAULT_COLOR.b, 1.0]}})

	if door_img_closed != null and door_img_opened != null:
		var combo: Image = Image.create(1920, 1080, false, door_img_closed.get_format())
		var left_im: Image = door_img_closed.duplicate() as Image
		var right_im: Image = door_img_opened.duplicate() as Image
		combo.blit_rect(left_im, Rect2i(480, 0, 960, 1080), Vector2i(0, 0))
		combo.blit_rect(right_im, Rect2i(480, 0, 960, 1080), Vector2i(960, 0))
		combo.fill_rect(Rect2i(958, 0, 4, 1080), Color(0.90, 0.95, 1.0, 1.0))
		combo.save_png(_resolve_path(QA_DIR) + "/qa_rfid_door_closed_vs_opened.png")
		print("[T38-QA] Saved qa_rfid_door_closed_vs_opened.png")

	# ---------------- 4. [t39u]-[t40u] DYNAMIC INTERIOR DESPAWN / RESPAWN ----------------
	_qa_place(Vector3(-6.0, 0.25, -2.0), 0.0, 0.0)
	await _qa_frames(6)
	_qa_t38_check("interior_loaded_at_start", _interiors_loaded, "status=%s" % str(get_interior_streaming_status()))
	# Rev C.2 removed the APT 201 workbench pickups. Collect the 202 desk cell so it stays collected across the stream.
	# Stand 0.75 m on its +Z side. Yaw 0 faces -Z, at the cell.
	var bci_pick: Node3D = _props_container.get_node_or_null("Apt202_Desk_Battery_Cell") as Node3D
	var bci_aim: Vector3 = bci_pick.global_position if bci_pick != null else Vector3(10.70, 5.10, 7.20)
	_qa_place(Vector3(bci_aim.x, 4.30, bci_aim.z + 0.75), 0.0, 0.0)
	await _qa_frames(8)
	if bci_pick != null and is_instance_valid(bci_pick):
		bci_aim = bci_pick.global_position
	_qa_place(Vector3(bci_aim.x, 4.30, bci_aim.z + 0.75), 0.0, 0.0)
	_qa_aim_at(bci_aim)
	_update_hud()
	var bci_label: String = String(_nearest.get("label", ""))
	var bci_prompt: String = _hud_prompt.text if _hud_prompt != null else ""
	_qa_t38_check("reticle_target_bci_headband", bci_label == "+5A BATTERY CELL" and bci_prompt.contains("+5A BATTERY CELL"),
		"label=%s prompt='%s'" % [bci_label, bci_prompt])
	var inv_before: int = int(_inventory["batt"])
	_interact()
	await _qa_frames(4)
	var collected_ok: bool = _collected_pickup_ids.has("Apt202_Desk_Battery_Cell") and int(_inventory["batt"]) == inv_before + 1
	_qa_t38_check("pickup_collected_before_exit", collected_ok, "collected=%s inv_batt=%d" % [str(_collected_pickup_ids.keys()), int(_inventory["batt"])])
	var live_before: int = int(get_interior_streaming_status()["live_pickups"])
	var wb: Node = _lookup_sector_node(_arch_container, "Apartment_Workbench")
	var wb_retired: bool = wb == null or (wb is Node3D and not (wb as Node3D).visible)
	_qa_t38_check("qa_ff_02_thresholds", is_equal_approx(INTERIOR_DESPAWN_Z, -14.0) and is_equal_approx(INTERIOR_RESPAWN_Z, -13.0) and INTERIOR_DESPAWN_Z < INTERIOR_RESPAWN_Z,
		"despawn_z=%.2f respawn_z=%.2f" % [INTERIOR_DESPAWN_Z, INTERIOR_RESPAWN_Z])
	# Exit door open -> interiors must stay loaded even beyond the despawn line
	var exit_d: Dictionary = _find_door("DOOR_SECTOR4_EXIT")
	_set_door_dissolve_immediate(exit_d, 1.0)
	_qa_place(Vector3(0.0, 0.25, -16.0), 0.0, 0.0)
	await _qa_frames(8)
	_qa_t38_check("qa_ff_02_stays_loaded_while_exit_open", _interiors_loaded, "z=-16.0 exit_open=%s loaded=%s" % [exit_d["open"], _interiors_loaded])
	_set_door_dissolve_immediate(exit_d, 0.0)
	_qa_place(Vector3(0.0, 0.25, -16.0), 0.0, 0.0)
	await _qa_frames(8)
	var st_out: Dictionary = get_interior_streaming_status()
	var props_left: int = 0
	for pc: Node in _props_container.get_children():
		if String(pc.name) != DOORS_ROOT_NAME and not pc.is_queued_for_deletion():
			props_left += 1
	var actors_in: int = 0
	for ac: Node in _actors_container.get_children():
		if ac is Node3D and (ac as Node3D).position.z > -7.5:
			actors_in += 1
	_qa_t38_check("interior_despawn_on_promenade_exit", not _interiors_loaded and _interior_managed_count > 0 and props_left == 0 and actors_in == 0 and wb_retired and _rfid_doors.size() == 6,
		"z=-16.0 (exit closed) loaded=%s managed=%d props_left=%d interior_actors_left=%d workbench_hidden_or_absent=%s doors=%d" % [_interiors_loaded, _interior_managed_count, props_left, actors_in, wb_retired, _rfid_doors.size()])
	await _qa_capture("qa_interior_despawned_promenade.png")
	_qa_place(Vector3(0.0, 0.25, -13.5), 180.0, 0.0)
	await _qa_frames(6)
	_qa_t38_check("qa_ff_02_hysteresis_band_stays_despawned", not _interiors_loaded, "z=-13.5 loaded=%s" % _interiors_loaded)
	_qa_place(Vector3(0.0, 0.25, -12.5), 180.0, 0.0)
	await _qa_frames(8)
	var st_in: Dictionary = get_interior_streaming_status()
	var bci_respawned: bool = _props_container.get_node_or_null("Apt202_Desk_Battery_Cell") != null
	var actors_back: int = 0
	for ac2: Node in _actors_container.get_children():
		if ac2 is Node3D and (ac2 as Node3D).position.z > -7.5:
			actors_back += 1
	_qa_t38_check("interior_respawn_on_vestibule_reentry", _interiors_loaded and int(st_in["live_pickups"]) == live_before and not bci_respawned and actors_back > 0 and wb_retired and int(_inventory["batt"]) == inv_before + 1,
		"z=-12.5 loaded=%s live_pickups=%d (before exit %d) collected_bci_respawned=%s interior_actors=%d workbench_hidden_or_absent=%s" % [_interiors_loaded, int(st_in["live_pickups"]), live_before, bci_respawned, actors_back, wb_retired])

	var out: PackedStringArray = PackedStringArray()
	out.append("# Reticle, Rotating Outer Starfield & RFID Force-Field Doors QA ([t38u]/[t45u])")
	out.append("")
	out.append("display=%s  failures=%d" % [DisplayServer.get_name(), _qa_failures])
	out.append("")
	out.append_array(_qa_log)
	var dir_abs: String = _resolve_path(QA_DIR)
	DirAccess.make_dir_recursive_absolute(dir_abs)
	var fn: String = dir_abs + ("/reticle_stars_doors_qa_log_headless.md" if DisplayServer.get_name() == "headless" else "/reticle_stars_doors_qa_log.md")
	var fa: FileAccess = FileAccess.open(fn, FileAccess.WRITE)
	if fa != null:
		fa.store_string("\n".join(out) + "\n")
		fa.close()
	print("[T38-QA] DONE failures=", _qa_failures, " log=", fn)
	get_tree().quit(1 if _qa_failures > 0 else 0)


# ------------------------------------------------------------------------------
# Simple troubleshoot UI (Hatch Field Emitter D-204)
# ------------------------------------------------------------------------------
func _troubleshoot_ui_open() -> bool:
	return _ts_ui != null and is_instance_valid(_ts_ui) and not _ts_ui.is_queued_for_deletion()


func open_troubleshoot_simple(device_id: String = "D-204") -> TroubleshootSimpleUI:
	if _ts_ui != null and is_instance_valid(_ts_ui) and not _ts_ui.is_queued_for_deletion():
		_ts_ui.device_id = device_id
		Input.mouse_mode = Input.MOUSE_MODE_VISIBLE
		return _ts_ui
	var packed := load("res://scenes/ui/troubleshoot_simple.tscn") as PackedScene
	if packed == null:
		push_error("[Troubleshoot] missing res://scenes/ui/troubleshoot_simple.tscn")
		return null
	_ts_layer = CanvasLayer.new()
	_ts_layer.name = "TroubleshootSimpleLayer"
	_ts_layer.layer = 40
	add_child(_ts_layer)
	var ui := packed.instantiate() as TroubleshootSimpleUI
	if ui == null:
		push_error("[Troubleshoot] scene root is not TroubleshootSimpleUI")
		_ts_layer.queue_free()
		_ts_layer = null
		return null
	ui.name = "TroubleshootSimpleUI"
	ui.device_id = device_id
	ui.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	_ts_layer.add_child(ui)
	_ts_ui = ui
	Input.mouse_mode = Input.MOUSE_MODE_VISIBLE
	ui.field_released.connect(_on_troubleshoot_field_released)
	ui.exited.connect(_on_troubleshoot_exited)
	return ui


func _on_troubleshoot_field_released(_device_id: String) -> void:
	# Win releases the field (dissolve open). A wrong pin only stalls inside the UI.
	# Rev C.2 removed the 204 emitter wall and Hatch_D204_EmitterPanel. DOOR_D204 is not in this sector.
	_set_hatch_field_open(true)
	var door: Dictionary = _find_door("DOOR_D204")
	if door.is_empty():
		print("[TS] D-204 released (no hatch door in this sector yet)")
		return
	_set_door_open_state(door, true)


func _on_troubleshoot_exited() -> void:
	Input.mouse_mode = Input.MOUSE_MODE_CAPTURED
	if _ts_layer != null and is_instance_valid(_ts_layer):
		_ts_layer.queue_free()
	_ts_layer = null
	_ts_ui = null


func _ts_qa(nm: String, ok: bool, detail: String) -> void:
	print("[TS-QA] %s | %s | %s" % ["PASS" if ok else "FAIL", nm, detail])
	if not ok:
		_qa_failures += 1


func _ts_save_png(fname: String) -> bool:
	await RenderingServer.frame_post_draw
	var tex: ViewportTexture = get_viewport().get_texture()
	if tex == null:
		_ts_qa("screenshot_" + fname.get_basename(), false, "no viewport texture")
		return false
	var img: Image = tex.get_image()
	if img == null or img.is_empty():
		_ts_qa("screenshot_" + fname.get_basename(), false, "empty viewport image")
		return false
	var dir: String = ProjectSettings.globalize_path("res://renders/queue_2026-10-31")
	DirAccess.make_dir_recursive_absolute(dir)
	var path: String = dir.path_join(fname)
	var err: Error = img.save_png(path)
	var ok: bool = err == OK
	_ts_qa("screenshot_" + fname.get_basename(), ok, path if ok else "save error %s" % err)
	return ok


func _run_troubleshoot_simple_qa() -> void:
	_qa_failures = 0
	if DisplayServer.get_name() != "headless":
		DisplayServer.window_set_size(Vector2i(1920, 1080))
	await get_tree().process_frame
	await get_tree().process_frame
	var ui: TroubleshootSimpleUI = open_troubleshoot_simple("D-204")
	if ui == null:
		_ts_qa("ui_opened", false, "null")
		get_tree().quit(1)
		return
	var box: Dictionary = {"n": 0}
	ui.field_released.connect(func(id: String) -> void:
		box["n"] = int(box["n"]) + 1
		box["id"] = id
	)
	await get_tree().process_frame
	await get_tree().process_frame
	_ts_qa("initial_not_won", not ui.is_won() and not ui.is_break_repaired(), "won=%s repaired=%s" % [ui.is_won(), ui.is_break_repaired()])
	await _ts_save_png("troubleshoot_simple_ui.png")
	ui.commit_pin("3")
	_ts_qa("pin3_without_repair", not ui.is_won() and int(box["n"]) == 0, "won=%s released=%d status=%s" % [ui.is_won(), int(box["n"]), ui.status_text()])
	ui.repair_break()
	_ts_qa("repair_continuous", ui.is_break_repaired() and not ui.is_won(), "repaired=%s won=%s wire=%d" % [ui.is_break_repaired(), ui.is_won(), ui.consumable_count("wire")])
	ui.commit_pin("1")
	var stalled: bool = ui.status_text().contains("[FIELD STALLED AT 40%]")
	_ts_qa("commit1_stalled", stalled and not ui.is_won(), "status=%s won=%s" % [ui.status_text(), ui.is_won()])
	ui.commit_pin("3")
	var won_status: bool = ui.status_text().contains("[FIELD RELEASED]")
	_ts_qa("commit3_won", ui.is_won() and int(box["n"]) == 1 and won_status and String(box.get("id", "")) == "D-204", "won=%s released=%d id=%s status=%s" % [ui.is_won(), int(box["n"]), String(box.get("id", "")), ui.status_text()])
	var still_open: bool = is_instance_valid(ui) and ui.is_inside_tree() and ui.visible and not ui.is_queued_for_deletion()
	_ts_qa("ui_open_after_win", still_open, "visible=%s in_tree=%s" % [ui.visible if is_instance_valid(ui) else false, ui.is_inside_tree() if is_instance_valid(ui) else false])
	var board: Control = ui.find_child("BoardView", true, false) as Control
	if board != null:
		board.queue_redraw()
	await get_tree().process_frame
	await _ts_save_png("troubleshoot_simple_ui_won.png")
	var exit_btn: Button = ui.find_child("ExitButton", true, false) as Button
	if exit_btn == null:
		_ts_qa("exit_closes", false, "ExitButton missing")
	else:
		exit_btn.pressed.emit()
		var closed: bool = (not is_instance_valid(ui)) or ui.is_queued_for_deletion() or not ui.visible
		_ts_qa("exit_closes", closed, "queued=%s visible=%s" % [ui.is_queued_for_deletion() if is_instance_valid(ui) else true, ui.visible if is_instance_valid(ui) else false])
	# Rev C.2 removed the 204 door beat, so there is no panel to aim at. Open the board directly
	# and still check that [E] and look are locked while it is up.
	var panel: Node3D = _props_container.get_node_or_null("Hatch_D204_EmitterPanel") as Node3D
	var opened_ok: bool = false
	if panel == null:
		opened_ok = true
		_ts_qa("e_aim_hatch_opens_ui", true, "door beat removed")
		open_troubleshoot_simple("D-204")
		await get_tree().process_frame
	else:
		var aim: Vector3 = panel.global_position
		_qa_place(Vector3(aim.x, 4.30, aim.z + 0.35), 0.0, 0.0)
		aim = panel.global_position
		_qa_aim_at(aim)
		var nearest_id: String = String(_find_nearest_interactable(INTERACT_RANGE).get("id", ""))
		var cam_fwd: Vector3 = (-_camera.global_transform.basis.z).normalized() if _camera != null else Vector3.FORWARD
		var to_panel: Vector3 = aim - (_camera.global_position if _camera != null else _player_body.global_position)
		var aimed_dot: float = cam_fwd.dot(to_panel.normalized()) if to_panel.length_squared() > 0.0001 else 0.0
		_interact()
		await get_tree().process_frame
		opened_ok = nearest_id == "Hatch_D204_EmitterPanel" and aimed_dot > 0.99 and _troubleshoot_ui_open() and _ts_ui.device_id == "D-204" and _ts_ui.visible
		_ts_qa("e_aim_hatch_opens_ui", opened_ok, "nearest=%s aimed_dot=%.4f open=%s device=%s" % [nearest_id, aimed_dot, _troubleshoot_ui_open(), _ts_ui.device_id if _troubleshoot_ui_open() else ""])
	var held: TroubleshootSimpleUI = _ts_ui
	_interact()
	var ignored_ok: bool = held != null and is_instance_valid(held) and _ts_ui == held and _troubleshoot_ui_open() and not held.is_won()
	_ts_qa("e_ignored_while_ui_open", ignored_ok, "same=%s won=%s" % [_ts_ui == held, held.is_won() if held != null and is_instance_valid(held) else true])
	var yaw_locked: float = _player_body.rotation.y
	var pitch_locked: float = _pitch
	_qa_mouse(Vector2(240.0, -40.0))
	await _qa_idle(2)
	var look_locked: bool = absf(_player_body.rotation.y - yaw_locked) < 0.0001 and absf(_pitch - pitch_locked) < 0.0001
	_ts_qa("look_locked_while_open", look_locked, "dyaw=%.5f dpitch=%.5f" % [_player_body.rotation.y - yaw_locked, _pitch - pitch_locked])
	print("[TS-QA] SUMMARY failures=%d e_aim_hatch_opens_ui=%s e_ignored_while_ui_open=%s look_locked_while_open=%s" % [_qa_failures, "PASS" if opened_ok else "FAIL", "PASS" if ignored_ok else "FAIL", "PASS" if look_locked else "FAIL"])
	print("[TS-QA] DONE failures=", _qa_failures)
	get_tree().quit(0 if _qa_failures == 0 else 1)


# ------------------------------------------------------------------------------
# [EXIT-01] Leave APT 201 from inside (`-- --qa-player-exit`)
# Real controller only: _qa_place for the spawn, then _qa_key / _qa_tap and physics frames.
# ------------------------------------------------------------------------------
func _run_qa_player_exit() -> void:
	var failures: int = 0
	if _player_body == null:
		print("[EXIT-QA] FAIL | spawn | player body missing")
		print("[EXIT-QA] FAIL | walk_to_door | player body missing")
		print("[EXIT-QA] FAIL | press_e | player body missing")
		print("[EXIT-QA] FAIL | face_neg_z | player body missing")
		print("[EXIT-QA] FAIL | corridor | player body missing")
		print("[EXIT-QA] DONE failures=5")
		get_tree().quit(1)
		return
	_qa_place(SPAWN_POS, 0.0, -4.0)
	await _qa_frames(20)
	var start_pos: Vector3 = _player_body.global_position
	print("[EXIT-QA] PASS | spawn | start=%s" % str(start_pos))
	var door: Dictionary = _find_door("DOOR_APT201")
	if door.is_empty():
		failures += 4
		print("[EXIT-QA] FAIL | walk_to_door | DOOR_APT201 missing")
		print("[EXIT-QA] FAIL | press_e | DOOR_APT201 missing")
		print("[EXIT-QA] FAIL | face_neg_z | DOOR_APT201 missing")
		print("[EXIT-QA] FAIL | corridor | DOOR_APT201 missing")
		print("[EXIT-QA] DONE failures=%d" % failures)
		get_tree().quit(1)
		return
	var root_pos: Vector3 = (door["root"] as Node3D).global_position
	# Opening is root.x ± 0.75. A straight walk at the root stops west of that span (spawn is
	# northwest), and the later -Z walk hits the wall. Stand on the centreline, 1.15 m north
	# of the door: inside the 2 m flat scan, clear of the closed field and the z=1.0 wall.
	var stand: Vector3 = Vector3(root_pos.x, root_pos.y, root_pos.z + 1.15)
	var dir: Vector3 = stand - _player_body.global_position
	_player_body.rotation_degrees.y = rad_to_deg(atan2(-dir.x, -dir.z))
	_qa_key(KEY_W, true)
	await _qa_idle(2)
	var walked: int = 0
	var horiz: float = Vector2(_player_body.global_position.x, _player_body.global_position.z).distance_to(Vector2(root_pos.x, root_pos.z))
	var x_err: float = absf(_player_body.global_position.x - root_pos.x)
	while walked < 280 and (horiz > 1.3 or x_err > 0.08):
		var pos_now: Vector3 = _player_body.global_position
		var aim: Vector3 = stand
		# Already south of the stand: correct X only, do not walk into the closed field.
		if pos_now.z < root_pos.z + 1.05:
			aim = Vector3(root_pos.x, pos_now.y, pos_now.z)
		dir = aim - pos_now
		dir.y = 0.0
		if dir.length() > 0.02:
			_player_body.rotation_degrees.y = rad_to_deg(atan2(-dir.x, -dir.z))
		await get_tree().physics_frame
		walked += 1
		horiz = Vector2(_player_body.global_position.x, _player_body.global_position.z).distance_to(Vector2(root_pos.x, root_pos.z))
		x_err = absf(_player_body.global_position.x - root_pos.x)
	_qa_key(KEY_W, false)
	await _qa_idle(2)
	# Face the doorway so the RFID scan (2 m flat, facing) still opens it.
	dir = root_pos - _player_body.global_position
	dir.y = 0.0
	if dir.length() > 0.05:
		_player_body.rotation_degrees.y = rad_to_deg(atan2(-dir.x, -dir.z))
	horiz = Vector2(_player_body.global_position.x, _player_body.global_position.z).distance_to(Vector2(root_pos.x, root_pos.z))
	if horiz <= 1.3:
		print("[EXIT-QA] PASS | walk_to_door | horiz=%.2f m frames=%d pos=%s" % [horiz, walked, str(_player_body.global_position)])
	else:
		failures += 1
		print("[EXIT-QA] FAIL | walk_to_door | horiz=%.2f m frames=%d pos=%s" % [horiz, walked, str(_player_body.global_position)])
	await _qa_tap(KEY_E)
	await get_tree().create_timer(1.2).timeout
	if bool(door["open"]):
		print("[EXIT-QA] PASS | press_e | open=true")
	else:
		failures += 1
		print("[EXIT-QA] FAIL | press_e | open=false dist3=%.2f pos=%s" % [_player_probe_point().distance_to(door["center"] as Vector3), str(_player_body.global_position)])
	_player_body.rotation_degrees.y = 0.0
	var fwd: Vector3 = (-_camera.global_transform.basis.z) if _camera != null else Vector3(0.0, 0.0, -1.0)
	if fwd.z >= 0.0:
		_player_body.rotation_degrees.y = 180.0
		if _camera != null:
			fwd = -_camera.global_transform.basis.z
	_qa_key(KEY_W, true)
	await _qa_idle(2)
	var out_frames: int = 0
	while out_frames < 180 and _player_body.global_position.z >= root_pos.z - 1.0:
		await get_tree().physics_frame
		out_frames += 1
	_qa_key(KEY_W, false)
	await _qa_idle(2)
	var end_z: float = _player_body.global_position.z
	if end_z < root_pos.z - 1.0:
		print("[EXIT-QA] PASS | face_neg_z | yaw=%.1f fwd_z=%.3f frames=%d z=%.2f" % [_player_body.rotation_degrees.y, fwd.z, out_frames, end_z])
	else:
		failures += 1
		print("[EXIT-QA] FAIL | face_neg_z | yaw=%.1f fwd_z=%.3f frames=%d z=%.2f need<%.2f" % [_player_body.rotation_degrees.y, fwd.z, out_frames, end_z, root_pos.z - 1.0])
	var end_pos: Vector3 = _player_body.global_position
	var y_delta: float = absf(end_pos.y - root_pos.y)
	if end_pos.z < root_pos.z - 1.0 and y_delta <= 1.0:
		print("[EXIT-QA] PASS | corridor | pos=%s root=%s" % [str(end_pos), str(root_pos)])
	else:
		failures += 1
		print("[EXIT-QA] FAIL | corridor | pos=%s root=%s z_need<%.2f y_delta=%.2f" % [str(end_pos), str(root_pos), root_pos.z - 1.0, y_delta])
	print("[EXIT-QA] DONE failures=%d" % failures)
	get_tree().quit(0 if failures == 0 else 1)


# ------------------------------------------------------------------------------
# [EGRESS] Spawn at SPAWN_POS and walk to the tram (`-- --qa-egress`)
# Real controller only: no _qa_place and no position writes after the normal spawn.
# Steering is mouse yaw; KEY_W is held except while scanning a door.
# ------------------------------------------------------------------------------
func _qa_egress_steer(target_xz: Vector2) -> void:
	# [QA-05] Mouse-look applies yaw -= screen_relative.x * _mouse_sens, so +dx turns right.
	# angle_error is that mouse-x sense: positive when the waypoint is to the right.
	var fwd: Vector3 = -_player_body.global_transform.basis.z
	fwd.y = 0.0
	var to: Vector3 = Vector3(target_xz.x - _player_body.global_position.x, 0.0, target_xz.y - _player_body.global_position.z)
	if fwd.length() < 0.001 or to.length() < 0.05:
		return
	var signed_left: float = fwd.normalized().signed_angle_to(to.normalized(), Vector3.UP)
	var angle_error: float = -signed_left
	var dx: float = clampf(angle_error / _mouse_sens, -40.0, 40.0)
	_qa_mouse(Vector2(dx, 0.0))


func _qa_egress_door_ready(door: Dictionary) -> bool:
	if door.is_empty():
		return false
	var droot: Node3D = door.get("root") as Node3D
	if droot == null or not is_instance_valid(droot):
		return false
	var target: Vector3 = droot.global_position + Vector3(0.0, 1.0, 0.0)
	var body: Vector3 = _player_body.global_position
	var horiz: float = Vector2(body.x - target.x, body.z - target.z).length()
	if horiz > 2.0 or absf(body.y - target.y) > 1.6:
		return false
	var fwd: Vector3 = (-_camera.global_transform.basis.z) if _camera != null else -_player_body.global_transform.basis.z
	fwd.y = 0.0
	var flat: Vector3 = target - body
	flat.y = 0.0
	if flat.length() <= 0.05:
		return true
	if fwd.length() < 0.001:
		return false
	return fwd.normalized().dot(flat.normalized()) >= SCAN_FACING_DOT


func _qa_egress_print_route(wps: Array[Dictionary]) -> void:
	var parts: PackedStringArray = PackedStringArray()
	for wp: Dictionary in wps:
		parts.append(String(wp["label"]))
	print("[EGRESS-QA] route=%s" % "; ".join(parts))


func _run_qa_egress() -> void:
	var failures: int = 0
	var wps: Array[Dictionary] = [
		{"label": "(-6.0, 4.5)", "xz": Vector2(-6.0, 4.5), "door": ""},
		# Closed DOOR_APT201 now sits on this crossing. Open it before walking to z=0.
		{"label": "(-3.0, 1.8)", "xz": Vector2(-3.0, 1.8), "door": "DOOR_APT201"},
		{"label": "(-3.0, 0.0)", "xz": Vector2(-3.0, 0.0), "door": ""},
		{"label": "(1.15, 0.0)", "xz": Vector2(1.15, 0.0), "door": ""},
		{"label": "(1.15, -2.8)", "xz": Vector2(1.15, -2.8), "door": ""},
		{"label": "(1.15, -4.88)", "xz": Vector2(1.15, -4.88), "door": ""},
		{"label": "(1.15, -6.14)", "xz": Vector2(1.15, -6.14), "door": ""},
		{"label": "(1.15, -7.4)", "xz": Vector2(1.15, -7.4), "door": ""},
		{"label": "(1.15, -8.15)", "xz": Vector2(1.15, -8.15), "door": ""},
		{"label": "(-1.15, -8.15)", "xz": Vector2(-1.15, -8.15), "door": ""},
		{"label": "(-1.15, -5.3)", "xz": Vector2(-1.15, -5.3), "door": ""},
		{"label": "(-1.15, -3.2)", "xz": Vector2(-1.15, -3.2), "door": ""},
		{"label": "(-1.15, -2.0)", "xz": Vector2(-1.15, -2.0), "door": ""},
		{"label": "(1.15, -2.0)", "xz": Vector2(1.15, -2.0), "door": ""},
		{"label": "(1.15, -8.15)", "xz": Vector2(1.15, -8.15), "door": ""},
		{"label": "DOOR_SECTOR4_EXIT (0.0, -7.9)", "xz": Vector2(0.0, -7.9), "door": "DOOR_SECTOR4_EXIT"},
		{"label": "(0.0, -9.8)", "xz": Vector2(0.0, -9.8), "door": ""},
		{"label": "(1.6, -10.5)", "xz": Vector2(1.6, -10.5), "door": ""},
		{"label": "(2.9, -11.5)", "xz": Vector2(2.9, -11.5), "door": ""},
		{"label": "(8.9, -15.9)", "xz": Vector2(8.9, -15.9), "door": ""},
		{"label": "(10.2, -16.3)", "xz": Vector2(10.2, -16.3), "door": ""},
		{"label": "(12.3, -16.7)", "xz": Vector2(12.3, -16.7), "door": ""},
		# [M-46] Reachable tram point. (12.8, -16.6) stopped 1.24 m short on shelter #15.
		# Shelter footprint is X 12..18, Z -16.57..-15.27, so (11.0, -16.1) is west of the glass.
		{"label": "(11.0, 0.30, -16.1)", "xz": Vector2(11.0, -16.1), "door": "", "final": true}
	]
	_qa_egress_print_route(wps)
	if _player_body == null:
		for wp0: Dictionary in wps:
			print("[EGRESS-QA] FAIL | %s | pos=(missing) frames=0" % String(wp0["label"]))
			print("[EGRESS-QA] last_slide=%s" % _qa_last_slide_path)
		print("[EGRESS-QA] DONE failures=%d" % wps.size())
		get_tree().quit(1)
		return
	# Normal spawn already placed the body at SPAWN_POS. Wait for it to settle; do not write position.
	await _qa_frames(30)
	var holding_w: bool = false
	for i: int in range(wps.size()):
		var wp: Dictionary = wps[i]
		var xz: Vector2 = wp["xz"] as Vector2
		var door_id: String = String(wp["door"])
		var is_final: bool = bool(wp.get("final", false))
		var door: Dictionary = _find_door(door_id) if door_id != "" else {}
		if not holding_w:
			_qa_key(KEY_W, true)
			await _qa_idle(2)
			holding_w = true
		var frames: int = 0
		var arrived: bool = false
		while frames < 900:
			var pos: Vector3 = _player_body.global_position
			var horiz: float = Vector2(pos.x, pos.z).distance_to(xz)
			var aim: Vector2 = xz
			if door_id != "" and not door.is_empty():
				var droot: Node3D = door.get("root") as Node3D
				if droot != null:
					aim = Vector2(droot.global_position.x, droot.global_position.z)
			_qa_egress_steer(aim if door_id != "" else xz)
			if door_id != "":
				if _qa_egress_door_ready(door) or horiz < 0.8:
					arrived = true
					break
			elif is_final and horiz <= 1.5 and pos.y >= 0.25:
				arrived = true
				break
			elif horiz < 0.8:
				arrived = true
				break
			await get_tree().physics_frame
			frames += 1
		var ok: bool = false
		if door_id != "":
			_qa_key(KEY_W, false)
			await _qa_idle(2)
			holding_w = false
			var face_left: int = 900 - frames
			var faced: int = 0
			while not _qa_egress_door_ready(door) and faced < face_left:
				var droot2: Node3D = door.get("root") as Node3D
				if droot2 != null:
					_qa_egress_steer(Vector2(droot2.global_position.x, droot2.global_position.z))
				await get_tree().physics_frame
				faced += 1
			frames += faced
			if _qa_egress_door_ready(door):
				await _qa_tap(KEY_E)
				await get_tree().create_timer(1.0).timeout
				ok = bool(door.get("open", false))
			else:
				ok = false
		elif is_final:
			var end_p: Vector3 = _player_body.global_position
			var end_h: float = Vector2(end_p.x, end_p.z).distance_to(xz)
			# Raised platform. Within 1.5 m of (11.0, -16.1) and y >= 0.25 (deck about 0.30).
			ok = end_h <= 1.5 and end_p.y >= 0.25
		else:
			ok = arrived
		var here: Vector3 = _player_body.global_position
		print("[EGRESS-QA] %s | %s | pos=%s frames=%d" % ["PASS" if ok else "FAIL", String(wp["label"]), str(here), frames])
		if not ok:
			failures += 1
			print("[EGRESS-QA] last_slide=%s" % _qa_last_slide_path)
	if holding_w:
		_qa_key(KEY_W, false)
		await _qa_idle(1)
	print("[EGRESS-QA] DONE failures=%d" % failures)
	get_tree().quit(0 if failures == 0 else 1)


func _run_qa_drawcalls() -> void:
	await _qa_frames(60)
	var poses: Array[Dictionary] = [
		{"name": "P1_spawn_apt201", "pos": SPAWN_POS + Vector3(0.0, 1.6, 0.0), "target": SPAWN_POS + Vector3(3.0, 1.4, -4.0)},
		{"name": "P2_L2_stairwell", "pos": Vector3(1.15, 5.8, 0.0), "target": Vector3(1.15, 4.6, -6.0)},
		{"name": "P3_exterior_plaza", "pos": Vector3(0.0, 1.7, -11.0), "target": Vector3(10.0, 1.0, -16.0)},
		{"name": "P4_tram_platform", "pos": Vector3(11.0, 2.0, -16.1), "target": Vector3(-6.0, 3.0, -10.0)},
	]
	for pose: Dictionary in poses:
		_qa_free_cam(pose["pos"] as Vector3, pose["target"] as Vector3, Vector3.UP, 70.0)
		await _qa_frames(90)
		var sum_dc: float = 0.0
		var sum_obj: float = 0.0
		var sum_prim: float = 0.0
		var sum_fps: float = 0.0
		var n: int = 120
		for _i: int in range(n):
			sum_dc += float(RenderingServer.get_rendering_info(RenderingServer.RENDERING_INFO_TOTAL_DRAW_CALLS_IN_FRAME))
			sum_obj += float(RenderingServer.get_rendering_info(RenderingServer.RENDERING_INFO_TOTAL_OBJECTS_IN_FRAME))
			sum_prim += float(RenderingServer.get_rendering_info(RenderingServer.RENDERING_INFO_TOTAL_PRIMITIVES_IN_FRAME))
			sum_fps += Engine.get_frames_per_second()
			await get_tree().process_frame
		print("[DRAWCALLS] %s draw_calls=%d objects=%d primitives=%d fps=%.1f" % [
			String(pose["name"]),
			int(round(sum_dc / float(n))),
			int(round(sum_obj / float(n))),
			int(round(sum_prim / float(n))),
			sum_fps / float(n),
		])
	print("[DRAWCALLS] DONE")
	get_tree().quit(0)


# ------------------------------------------------------------------------------
# Exterior placements v1.3 (design/exterior_placements_v1_3.json)
# ------------------------------------------------------------------------------
func _ext_base(asset: String) -> String:
	return asset.get_file().get_basename()


func _ext_is_surface_sticker(asset: String) -> bool:
	# Decals, litter, scuffs, wear, and desire-path: no collision, no shadow.
	var n: String = asset.to_lower()
	return n.contains("decal") or n.contains("litter") or n.contains("scuff") or n.contains("wear") or n.contains("desire")


func _ext_is_solid(asset: String) -> bool:
	var base: String = _ext_base(asset)
	if base.begins_with("ext_paving_") or base.begins_with("ext_curb_"):
		return true
	return base == "ext_platform_infill" or base == "ext_kerb_ramp" or base == "ext_tram_platform_kerb" or base == "ext_maglev_guideway" or base == "ext_canal_edge" or base == "ext_tram_shelter" or base == "ext_maglev_car_body" or base == "ext_maglev_magnet_module" or base == "hydro_planter_tiered_exterior"


func _ext_packed_scene(asset: String) -> PackedScene:
	if _ext_scene_cache.has(asset):
		return _ext_scene_cache[asset] as PackedScene
	var path: String = "res://assets/models/" + asset.get_file()
	var packed: PackedScene = null
	if ResourceLoader.exists(path) or FileAccess.file_exists(ProjectSettings.globalize_path(path)):
		packed = load(path) as PackedScene
	if packed == null:
		push_warning("[EXT] missing asset %s" % path)
	_ext_scene_cache[asset] = packed
	return packed


func _ext_collect_meshes(root: Node) -> Array[MeshInstance3D]:
	var out: Array[MeshInstance3D] = []
	var stack: Array[Node] = [root]
	while not stack.is_empty():
		var n: Node = stack.pop_back()
		if n is MeshInstance3D and (n as MeshInstance3D).mesh != null:
			out.append(n as MeshInstance3D)
		var kids: Array[Node] = []
		for ch: Node in n.get_children():
			kids.append(ch)
		for i: int in range(kids.size() - 1, -1, -1):
			stack.append(kids[i])
	return out


func _ext_rel_transform(root: Node3D, node: Node3D) -> Transform3D:
	var xf: Transform3D = Transform3D.IDENTITY
	var current: Node = node
	while current != null and current != root:
		if current is Node3D:
			xf = (current as Node3D).transform * xf
		current = current.get_parent()
	return xf


## Visual mesh bounds in `inst` local space. Collision helpers are not part of the prop top.
func _ext_local_visual_aabb(inst: Node3D) -> Dictionary:
	var merged: AABB = AABB()
	var any: bool = false
	var stack: Array[Node] = [inst]
	while not stack.is_empty():
		var curr: Node = stack.pop_back()
		if curr is MeshInstance3D:
			var mi: MeshInstance3D = curr as MeshInstance3D
			if _ext_mesh_is_visual(mi, inst):
				var bb: AABB = _ext_rel_transform(inst, mi) * mi.get_aabb()
				if any:
					merged = merged.merge(bb)
				else:
					merged = bb
					any = true
		for ch: Node in curr.get_children():
			stack.append(ch)
	return {"ok": any, "aabb": merged}


## [M-59] Peaked cap over the car body. Seat tops (world y about 0.66..0.75) and the
## roof are inside the prism, and the faces rise about 70 deg so they are not floors
## (floor_max_angle is 50 deg). Inset from the body keeps it off the platform and
## clear of the boarding point (11.0, 0.30, -16.1).
func _ext_add_tram_nostand_cap(inst: Node3D) -> void:
	var merged: Dictionary = _ext_local_visual_aabb(inst)
	if not bool(merged["ok"]):
		return
	var bb: AABB = merged["aabb"] as AABB
	if bb.size.x < 4.0 or bb.size.z < 1.0 or bb.size.y < 1.5:
		return
	var x0: float = bb.position.x + 0.20
	var x1: float = bb.position.x + bb.size.x - 0.20
	var z0: float = bb.position.z + 0.20
	var z1: float = bb.position.z + bb.size.z - 0.20
	var y0: float = bb.position.y + 0.16
	var yp: float = bb.position.y + bb.size.y + 0.20
	var zc: float = (z0 + z1) * 0.5
	var body: StaticBody3D = StaticBody3D.new()
	body.name = "TramRoofNoStand"
	body.collision_layer = 1
	body.collision_mask = 1
	var cs: CollisionShape3D = CollisionShape3D.new()
	cs.name = "TramRoofNoStand_Shape"
	var shape: ConvexPolygonShape3D = ConvexPolygonShape3D.new()
	shape.margin = 0.0
	shape.points = PackedVector3Array([
		Vector3(x0, y0, z0), Vector3(x0, y0, z1), Vector3(x0, yp, zc),
		Vector3(x1, y0, z0), Vector3(x1, y0, z1), Vector3(x1, yp, zc),
	])
	cs.shape = shape
	body.add_child(cs)
	inst.add_child(body)


## Thin lid on the visual top so a down-ray hits the infill top, not the body under the paver joints.
func _ext_add_infill_top_cap(inst: Node3D, body: StaticBody3D) -> void:
	var merged: Dictionary = _ext_local_visual_aabb(inst)
	if not bool(merged["ok"]):
		return
	var bb: AABB = merged["aabb"] as AABB
	if bb.size.x < 0.05 or bb.size.z < 0.05:
		return
	var thick: float = 0.004
	var top: float = bb.position.y + bb.size.y
	var cs: CollisionShape3D = CollisionShape3D.new()
	cs.name = "ExtTopCap"
	var shape: BoxShape3D = BoxShape3D.new()
	shape.size = Vector3(bb.size.x, thick, bb.size.z)
	shape.margin = 0.0
	cs.shape = shape
	cs.position = Vector3(bb.get_center().x, top - thick * 0.5, bb.get_center().z)
	body.add_child(cs)


func _ext_hit_on_ground_prop(collider: Object) -> bool:
	if not (collider is Node):
		return false
	var n: Node = collider as Node
	while n != null:
		if n.has_meta("ext_asset"):
			return _ext_spawn_kind(String(n.get_meta("ext_asset"))) == EXT_KIND_GROUND
		n = n.get_parent()
	return false


## Vertex lies on the interior side of the Rev C north wall, inside the shell span, and low enough to step on.
func _ext_shell_lip_inside(p: Vector3) -> bool:
	return p.z > -8.90 and p.z < -8.0 and p.x >= -14.2 and p.x <= 14.2 and p.y < 1.0


## Keep a vertex when it is on or outside the wall, or outside the shell's x span.
func _ext_shell_lip_safe(p: Vector3) -> bool:
	return p.z <= -8.90 or p.z >= -8.0 or p.x < -14.2 or p.x > 14.2


## [GEO-17/M-73] True when every triangle entered the shell and this shape must not be added.
## Reads the shared trimesh and writes a new per-instance shape. Does not touch _ext_shape_cache.
func _ext_clip_shell_lip(cs: CollisionShape3D, inst_world: Transform3D) -> bool:
	var shape: ConcavePolygonShape3D = cs.shape as ConcavePolygonShape3D
	if shape == null:
		return false
	var face_xf: Transform3D = inst_world * cs.transform
	var src: PackedVector3Array = shape.data
	var crosses: bool = false
	var vi: int = 0
	while vi + 2 < src.size():
		if _ext_shell_lip_inside(face_xf * src[vi]) or _ext_shell_lip_inside(face_xf * src[vi + 1]) or _ext_shell_lip_inside(face_xf * src[vi + 2]):
			crosses = true
			break
		vi += 3
	if not crosses:
		return false
	var kept: PackedVector3Array = PackedVector3Array()
	vi = 0
	while vi + 2 < src.size():
		var w0: Vector3 = face_xf * src[vi]
		var w1: Vector3 = face_xf * src[vi + 1]
		var w2: Vector3 = face_xf * src[vi + 2]
		if _ext_shell_lip_safe(w0) and _ext_shell_lip_safe(w1) and _ext_shell_lip_safe(w2):
			kept.append(src[vi])
			kept.append(src[vi + 1])
			kept.append(src[vi + 2])
		vi += 3
	_ext_shell_clipped += 1
	if kept.is_empty():
		return true
	var clipped: ConcavePolygonShape3D = ConcavePolygonShape3D.new()
	clipped.margin = 0.0
	clipped.data = kept
	cs.shape = clipped
	return false


func _ext_add_solid_collision(inst: Node3D, asset: String) -> void:
	var meshes: Array[MeshInstance3D] = _ext_collect_meshes(inst)
	var fill: bool = not _ext_shape_cache.has(asset)
	var cached: Array = []
	if fill:
		cached.resize(meshes.size())
	else:
		cached = _ext_shape_cache[asset] as Array
	var unique: Dictionary = {}
	var body: StaticBody3D = StaticBody3D.new()
	body.name = "ExtCollision"
	var any: bool = false
	# [GEO-17/M-73] Ground and curb lips that cross z=-8.90 are clipped per instance.
	var clip_shell: bool = _ext_spawn_kind(asset) == EXT_KIND_GROUND or _ext_base(asset).begins_with("ext_curb")
	# Collision is built before the prop is parented. global_transform is invalid until then.
	# The exterior root is identity, so the placement transform already written on inst is the world transform.
	var inst_world: Transform3D = inst.transform
	if inst.is_inside_tree():
		inst_world = inst.global_transform
	for i: int in range(meshes.size()):
		var mi: MeshInstance3D = meshes[i]
		var shape: ConcavePolygonShape3D = null
		if fill:
			if mi.mesh.get_surface_count() <= 0:
				cached[i] = null
				continue
			var mid: int = mi.mesh.get_instance_id()
			if unique.has(mid):
				shape = unique[mid] as ConcavePolygonShape3D
			else:
				shape = mi.mesh.create_trimesh_shape()
				if shape != null:
					# Shared across instances of this asset. Margin 0 keeps the hit on the mesh.
					shape.margin = 0.0
					# [M-46] Two-sided trimesh. One-sided ext faces let the capsule sink past a face and pin on the
					# hidden side (tram platform end (11.81, 0.34, -16.74) on ExtShape_0, paving/curb seam (7.62, -17.95)).
					shape.backface_collision = true
				unique[mid] = shape
			cached[i] = shape
		elif i < cached.size():
			shape = cached[i] as ConcavePolygonShape3D
		if shape == null:
			continue
		var cs: CollisionShape3D = CollisionShape3D.new()
		cs.name = "ExtShape_%d" % i
		cs.shape = shape
		cs.transform = _ext_rel_transform(inst, mi)
		if clip_shell and _ext_clip_shell_lip(cs, inst_world):
			cs.free()
			continue
		body.add_child(cs)
		any = true
	if fill:
		_ext_shape_cache[asset] = cached
	if any and _ext_base(asset) == "ext_platform_infill":
		_ext_add_infill_top_cap(inst, body)
	if any:
		inst.add_child(body)


func _ext_spawn_kind(asset: String) -> int:
	if _ext_is_surface_sticker(asset):
		return EXT_KIND_DECAL
	var base: String = _ext_base(asset)
	if base == "ext_maglev_car_body":
		return EXT_KIND_CAR
	if base.begins_with("ext_paving_") or base == "ext_platform_infill" or base == "ext_kerb_ramp" or base == "ext_canal_edge" or base == "ext_maglev_guideway":
		return EXT_KIND_GROUND
	return EXT_KIND_SOLID


func _ext_mark_spawned(spawned: int) -> void:
	set_meta("exterior_spawned", true)
	var ext_root: Node3D = get_node_or_null("ExteriorPlacements_v1_3") as Node3D
	if ext_root != null:
		_ext_batch_multimesh(ext_root)
	print("[EXT] spawned=%d" % spawned)
	print("[GEO-17] ext shapes clipped at shell z -8.90: %d" % _ext_shell_clipped)
	exterior_spawned.emit()


## [M-07] One MultiMesh per repeated exterior mesh. Source MeshInstance3D nodes stay (hidden)
## so collision, metas, and ExtCollision are unchanged.
func _ext_batch_multimesh(root: Node3D) -> void:
	var candidates: Array[MeshInstance3D] = []
	var placed: Array[Node] = []
	for child: Node in root.get_children():
		placed.append(child)
	for child: Node in placed:
		if not child.is_in_group("exterior_placement"):
			continue
		if not child.has_meta("ext_asset"):
			continue
		var asset: String = String(child.get_meta("ext_asset"))
		if _ext_base(asset) == "ext_maglev_car_body" or _ext_spawn_kind(asset) == EXT_KIND_DECAL:
			continue
		for n: Node in child.find_children("*", "MeshInstance3D", true, false):
			var mi: MeshInstance3D = n as MeshInstance3D
			if mi == null or not mi.visible or mi.mesh == null or not mi.skeleton.is_empty():
				continue
			candidates.append(mi)
	var mesh_counts: Dictionary = {}
	for mi: MeshInstance3D in candidates:
		var mid: int = mi.mesh.get_instance_id()
		mesh_counts[mid] = int(mesh_counts.get(mid, 0)) + 1
	# Key: mesh resource, material_override, cast_shadow, active material of each surface.
	var groups: Dictionary = {}
	for mi2: MeshInstance3D in candidates:
		if int(mesh_counts.get(mi2.mesh.get_instance_id(), 0)) < 8:
			continue
		var mo: Material = mi2.material_override
		var mo_id: int = mo.get_instance_id() if mo != null else 0
		var surf_ids: String = ""
		var sc_key: int = mi2.mesh.get_surface_count()
		for s: int in range(sc_key):
			var am: Material = mi2.get_active_material(s)
			var am_id: int = am.get_instance_id() if am != null else 0
			if s > 0:
				surf_ids += ","
			surf_ids += str(am_id)
		var key: String = "%d|%d|%d|%s" % [mi2.mesh.get_instance_id(), mo_id, int(mi2.cast_shadow), surf_ids]
		if not groups.has(key):
			groups[key] = []
		(groups[key] as Array).append(mi2)
	var group_n: int = 0
	var inst_n: int = 0
	for key_v: Variant in groups.keys():
		var members: Array = groups[key_v] as Array
		if members.size() < 8:
			continue
		var first: MeshInstance3D = members[0] as MeshInstance3D
		if first == null or first.mesh == null:
			continue
		var use_mesh: Mesh = first.mesh
		var surf_count: int = use_mesh.get_surface_count()
		var had_surface_override: bool = false
		for s_ov: int in range(surf_count):
			if first.get_surface_override_material(s_ov) != null:
				had_surface_override = true
				break
		if had_surface_override:
			var dup: Mesh = use_mesh.duplicate() as Mesh
			if dup != null and dup.get_surface_count() == surf_count:
				for s_set: int in range(surf_count):
					var ov: Material = first.get_surface_override_material(s_set)
					if ov != null:
						dup.surface_set_material(s_set, ov)
				use_mesh = dup
			else:
				var built: ArrayMesh = ArrayMesh.new()
				for s_set2: int in range(surf_count):
					built.add_surface_from_arrays(use_mesh.surface_get_primitive_type(s_set2), use_mesh.surface_get_arrays(s_set2))
					var ov2: Material = first.get_surface_override_material(s_set2)
					var keep: Material = ov2 if ov2 != null else use_mesh.surface_get_material(s_set2)
					if keep != null:
						built.surface_set_material(s_set2, keep)
				use_mesh = built
		var mm: MultiMesh = MultiMesh.new()
		mm.transform_format = MultiMesh.TRANSFORM_3D
		mm.mesh = use_mesh
		mm.instance_count = members.size()
		for i: int in range(members.size()):
			var member: MeshInstance3D = members[i] as MeshInstance3D
			mm.set_instance_transform(i, root.global_transform.affine_inverse() * member.global_transform)
		var mesh_label: String = first.mesh.resource_name
		if mesh_label == "":
			mesh_label = first.name
		var cleaned: String = ""
		for ci: int in range(mesh_label.length()):
			var ch: String = mesh_label.substr(ci, 1)
			var ok_ch: bool = (ch >= "a" and ch <= "z") or (ch >= "A" and ch <= "Z") or (ch >= "0" and ch <= "9") or ch == "_" or ch == "-"
			cleaned += ch if ok_ch else "_"
		if cleaned == "":
			cleaned = "mesh"
		if cleaned.length() > 48:
			cleaned = cleaned.substr(0, 48)
		var mmi: MultiMeshInstance3D = MultiMeshInstance3D.new()
		mmi.name = "ExtMM_%d_%s" % [group_n, cleaned]
		mmi.multimesh = mm
		mmi.material_override = first.material_override
		mmi.cast_shadow = first.cast_shadow
		mmi.gi_mode = first.gi_mode
		mmi.layers = first.layers
		# [VIS-20] Group AABBs are tens of metres wide; per-group range culling pops whole curb rows. A MultiMesh is one draw call, so no range.
		mmi.visibility_range_end = 0.0
		root.add_child(mmi)
		for item: Variant in members:
			var hide_mi: MeshInstance3D = item as MeshInstance3D
			if hide_mi != null:
				hide_mi.visible = false
		inst_n += members.size()
		group_n += 1
	print("[M-07] ext multimesh groups=%d instances=%d" % [group_n, inst_n])


func _ext_has_collision_relation(mi: Node) -> bool:
	var p: Node = mi.get_parent()
	while p != null:
		if p is CollisionObject3D:
			return true
		p = p.get_parent()
	var stack: Array[Node] = []
	for ch: Node in mi.get_children():
		stack.append(ch)
	while not stack.is_empty():
		var n: Node = stack.pop_back()
		if n is CollisionObject3D or n is CollisionShape3D:
			return true
		for ch: Node in n.get_children():
			stack.append(ch)
	return false


func _ext_ground_mesh_ok(mi: MeshInstance3D) -> bool:
	if mi.mesh == null or mi.mesh.get_surface_count() <= 0:
		return false
	if _ext_has_collision_relation(mi):
		return false
	var aabb: AABB = mi.global_transform * mi.get_aabb()
	var top: float = aabb.position.y + aabb.size.y
	if top < -0.5 or top > 0.6:
		return false
	if aabb.size.y > 0.8:
		return false
	if aabb.size.x < 1.5 and aabb.size.z < 1.5:
		return false
	var centre: Vector3 = aabb.get_center()
	# Exterior only: promenade (z < -8.5) or the side walks (|x| > 15).
	if centre.z >= -8.5 and absf(centre.x) <= 15.0:
		return false
	return true


func _ext_add_ground_colliders() -> int:
	var meshes: Array[MeshInstance3D] = []
	var stack: Array[Node] = [self]
	while not stack.is_empty():
		var n: Node = stack.pop_back()
		if n is MeshInstance3D:
			meshes.append(n as MeshInstance3D)
		for ch: Node in n.get_children():
			stack.append(ch)
	var count: int = 0
	for mi: MeshInstance3D in meshes:
		if not _ext_ground_mesh_ok(mi):
			continue
		var shape: ConcavePolygonShape3D = mi.mesh.create_trimesh_shape()
		if shape == null:
			continue
		shape.margin = 0.0
		var body: StaticBody3D = StaticBody3D.new()
		body.name = "ExtGroundCol"
		body.add_to_group("ext_ground_col")
		var cs: CollisionShape3D = CollisionShape3D.new()
		cs.name = "ExtGroundShape"
		cs.shape = shape
		body.add_child(cs)
		mi.add_child(body)
		count += 1
	return count


func _ext_name_is_helper(nm: String) -> bool:
	var n: String = nm.to_lower()
	if n.contains("collision") or n.contains("collider") or n.contains("helper") or n.contains("proxy") or n.contains("colonly") or n.contains("ucx"):
		return true
	return n.ends_with("_col") or n.ends_with("-col") or n.contains("_col_") or n.contains("-col-")


## Visual meshes only. Collision-only and helper nodes (and anything parented under them) are not the prop bottom.
func _ext_mesh_is_visual(mi: MeshInstance3D, root_n: Node) -> bool:
	if mi.mesh == null or not mi.visible:
		return false
	var n: Node = mi
	while n != null:
		if _ext_name_is_helper(String(n.name)):
			return false
		if n != root_n and (n is CollisionObject3D or n is CollisionShape3D):
			return false
		if n == root_n:
			break
		n = n.get_parent()
	return true


func _ext_union_mesh_aabb(root_n: Node3D, visual_only: bool) -> Dictionary:
	var merged: AABB = AABB()
	var any: bool = false
	var stack: Array[Node] = [root_n]
	while not stack.is_empty():
		var curr: Node = stack.pop_back()
		if curr is MeshInstance3D:
			var mi: MeshInstance3D = curr as MeshInstance3D
			if mi.mesh != null and (not visual_only or _ext_mesh_is_visual(mi, root_n)):
				var bb: AABB = mi.global_transform * mi.get_aabb()
				if any:
					merged = merged.merge(bb)
				else:
					merged = bb
					any = true
		for ch: Node in curr.get_children():
			stack.append(ch)
	return {"ok": any, "aabb": merged}


func _ext_merged_aabb(root_n: Node3D) -> Dictionary:
	var visual: Dictionary = _ext_union_mesh_aabb(root_n, true)
	if bool(visual["ok"]):
		return visual
	return _ext_union_mesh_aabb(root_n, false)


func _ext_collider_is_under(root_n: Node, collider: Object) -> bool:
	if not (collider is Node):
		return false
	var n: Node = collider as Node
	while n != null:
		if n == root_n:
			return true
		n = n.get_parent()
	return false


func _ext_collision_rids(root_n: Node) -> Array[RID]:
	var rids: Array[RID] = []
	var stack: Array[Node] = [root_n]
	while not stack.is_empty():
		var n: Node = stack.pop_back()
		if n is CollisionObject3D:
			rids.append((n as CollisionObject3D).get_rid())
		for ch: Node in n.get_children():
			stack.append(ch)
	return rids


func _ext_snap_exclude(inst: Node3D, kind: int, ext_root: Node) -> Array[RID]:
	var exclude: Array[RID] = []
	var asset: String = String(inst.get_meta("ext_asset", ""))
	# Always drop this prop's bodies so the ray cannot land on its own roof or posts.
	exclude.append_array(_ext_collision_rids(inst))
	if kind == EXT_KIND_GROUND:
		# Placement colliders only. ExtGroundExtension stays outside this root so these rays hit it.
		exclude.append_array(_ext_collision_rids(ext_root))
		return exclude
	for ch: Node in ext_root.get_children():
		if not (ch is Node3D):
			continue
		var ch_asset: String = String(ch.get_meta("ext_asset", ""))
		var ch_kind: int = _ext_spawn_kind(ch_asset)
		if ch == inst:
			exclude.append_array(_ext_collision_rids(ch))
			continue
		if kind == EXT_KIND_DECAL:
			# Track scuffs rest on the guideway. The car and magnet are stacked above it.
			if asset.to_lower().contains("scuff") and (ch_kind == EXT_KIND_CAR or _ext_base(ch_asset) == "ext_maglev_magnet_module"):
				exclude.append_array(_ext_collision_rids(ch))
			continue
		# Infill, paving, kerb ramp, guideway, and canal edge are ground. A solid stands on them,
		# so their bodies stay in the down-ray. Decals are not a support surface.
		if ch_kind == EXT_KIND_GROUND or ch_kind == EXT_KIND_DECAL:
			continue
		# Cars keep magnet modules (and the guideway, which is ground-like).
		if kind == EXT_KIND_CAR and _ext_base(ch_asset) == "ext_maglev_magnet_module":
			continue
		exclude.append_array(_ext_collision_rids(ch))
	return exclude


func _ext_ray(space: PhysicsDirectSpaceState3D, from: Vector3, to: Vector3, exclude: Array[RID]) -> Dictionary:
	var rq: PhysicsRayQueryParameters3D = PhysicsRayQueryParameters3D.create(from, to)
	rq.exclude = exclude
	rq.collide_with_bodies = true
	rq.collide_with_areas = false
	rq.hit_from_inside = false
	return space.intersect_ray(rq)


func _ext_max_hit_y(inst: Node3D, aabb: AABB, exclude: Array[RID]) -> Dictionary:
	var world: World3D = inst.get_world_3d()
	if world == null:
		return {"ok": false, "y": 0.0}
	var space: PhysicsDirectSpaceState3D = world.direct_space_state
	if space == null:
		return {"ok": false, "y": 0.0}
	var start_y: float = aabb.position.y + aabb.size.y + EXT_SNAP_ABOVE
	var end_y: float = inst.global_position.y - EXT_SNAP_DEPTH
	var pts: Array[Vector2] = []
	var centre: Vector3 = aabb.get_center()
	pts.append(Vector2(centre.x, centre.z))
	var inset_x: float = minf(EXT_CORNER_INSET, maxf(aabb.size.x * 0.49, 0.0))
	var inset_z: float = minf(EXT_CORNER_INSET, maxf(aabb.size.z * 0.49, 0.0))
	var x0: float = aabb.position.x + inset_x
	var x1: float = aabb.position.x + aabb.size.x - inset_x
	var z0: float = aabb.position.z + inset_z
	var z1: float = aabb.position.z + aabb.size.z - inset_z
	pts.append(Vector2(x0, z0))
	pts.append(Vector2(x1, z0))
	pts.append(Vector2(x0, z1))
	pts.append(Vector2(x1, z1))
	var hits: Array[float] = []
	var ground_hits: Array[float] = []
	var center_y: float = 0.0
	var have_center: bool = false
	for i: int in range(pts.size()):
		var p: Vector2 = pts[i]
		var hit: Dictionary = _ext_ray(space, Vector3(p.x, start_y, p.y), Vector3(p.x, end_y, p.y), exclude)
		if hit.is_empty() or _ext_collider_is_under(inst, hit.get("collider")):
			continue
		var hy: float = (hit["position"] as Vector3).y
		if i == 0:
			center_y = hy
			have_center = true
		hits.append(hy)
		if _ext_hit_on_ground_prop(hit.get("collider")):
			ground_hits.append(hy)
	# Ground-like samples (centre + inset corners) report their highest hit, so a joint in the
	# infill body cannot hide the paver top. Other hits keep the guardrail lift filter.
	var filtered: Dictionary = _ext_support_from_hits(hits, center_y, have_center)
	if ground_hits.is_empty():
		return filtered
	var top_y: float = ground_hits[0]
	for gy: float in ground_hits:
		top_y = maxf(top_y, gy)
	if not bool(filtered["ok"]) or top_y > float(filtered["y"]):
		return {"ok": true, "y": top_y}
	return filtered


## Highest support that is still within EXT_SUPPORT_LIFT of the centre hit.
## A footprint corner on PromenadeEastGuardrail (top y 1.245) must not lift the whole prop.
func _ext_support_from_hits(hits: Array[float], center_y: float, have_center: bool) -> Dictionary:
	if hits.is_empty():
		return {"ok": false, "y": 0.0}
	var anchor: float = center_y if have_center else hits[0]
	if not have_center:
		for h: float in hits:
			anchor = minf(anchor, h)
	var best: float = -INF
	var any: bool = false
	for h2: float in hits:
		if h2 > anchor + EXT_SUPPORT_LIFT:
			continue
		if not any or h2 > best:
			best = h2
			any = true
	if not any:
		return {"ok": true, "y": anchor}
	return {"ok": true, "y": best}


func _ext_magnet_top_for_car(car_aabb: AABB, ext_root: Node) -> Dictionary:
	var c: Vector3 = car_aabb.get_center()
	var best_d: float = INF
	var best_y: float = 0.0
	var any: bool = false
	for ch: Node in ext_root.get_children():
		if not (ch is Node3D):
			continue
		if _ext_base(String(ch.get_meta("ext_asset", ""))) != "ext_maglev_magnet_module":
			continue
		var merged: Dictionary = _ext_merged_aabb(ch as Node3D)
		if not bool(merged["ok"]):
			continue
		var bb: AABB = merged["aabb"] as AABB
		var mc: Vector3 = bb.get_center()
		var d: float = Vector2(c.x, c.z).distance_to(Vector2(mc.x, mc.z))
		if d < best_d:
			best_d = d
			best_y = bb.position.y + bb.size.y
			any = true
	if not any or best_d > 2.0:
		return {"ok": false, "y": 0.0}
	return {"ok": true, "y": best_y}


const EXT_MAGLEV_GAP := 0.015 # m, magnet module underside to guideway top (spec 0.015 +/- 0.005)


func _ext_snap_instance(inst: Node3D, kind: int, ext_root: Node) -> void:
	var merged: Dictionary = _ext_merged_aabb(inst)
	var asset: String = String(inst.get_meta("ext_asset", ""))
	var eid: int = int(inst.get_meta("ext_id", -1))
	if not bool(merged["ok"]):
		push_warning("[EXT] no ground under id=%s asset=%s (empty aabb)" % [str(eid), asset])
		return
	var aabb: AABB = merged["aabb"] as AABB
	var hit: Dictionary = _ext_max_hit_y(inst, aabb, _ext_snap_exclude(inst, kind, ext_root))
	# Plan stack: car body bottom rests on its magnet module top.
	if kind == EXT_KIND_CAR:
		var mag: Dictionary = _ext_magnet_top_for_car(aabb, ext_root)
		if bool(mag["ok"]):
			hit = {"ok": true, "y": float(mag["y"])}
	if not bool(hit["ok"]):
		push_warning("[EXT] no ground under id=%s asset=%s" % [str(eid), asset])
		return
	var lift: float = EXT_DECAL_LIFT if kind == EXT_KIND_DECAL else 0.0
	# [MAGLEV] Magnet modules hover EXT_MAGLEV_GAP over the guideway; the car body rests on the module top.
	if _ext_base(asset) == "ext_maglev_magnet_module":
		lift = EXT_MAGLEV_GAP
	var target: float = float(hit["y"]) + lift
	if kind == EXT_KIND_DECAL and target < float(hit["y"]):
		target = float(hit["y"])
	var bottom: float = aabb.position.y
	inst.global_position.y += target - bottom


func _ext_fill_buckets(buckets: Array) -> bool:
	var fa: FileAccess = FileAccess.open(EXT_PLACEMENTS_PATH, FileAccess.READ)
	if fa == null:
		push_warning("[EXT] cannot open %s" % EXT_PLACEMENTS_PATH)
		return false
	var parsed: Variant = JSON.parse_string(fa.get_as_text())
	fa.close()
	if parsed == null or not (parsed is Dictionary):
		push_warning("[EXT] %s did not parse" % EXT_PLACEMENTS_PATH)
		return false
	var raw: Variant = (parsed as Dictionary).get("placements", [])
	if not (raw is Array):
		push_warning("[EXT] %s has no placements array" % EXT_PLACEMENTS_PATH)
		return false
	var placements: Array = raw as Array
	for i: int in range(placements.size()):
		var item: Variant = placements[i]
		if not (item is Dictionary):
			push_warning("[EXT] skip index %d (not an object)" % i)
			continue
		var entry: Dictionary = item as Dictionary
		var asset: String = String(entry.get("asset", ""))
		if asset == "":
			push_warning("[EXT] skip index %d (empty asset)" % i)
			continue
		entry["_i"] = i
		var kind: int = _ext_spawn_kind(asset)
		var bucket: Array = buckets[kind]
		bucket.append(entry)
		buckets[kind] = bucket
	return true


## Rev C north interior: outer x -14.1..14.1, north-wall centerline z=9.0, so z < 9.0.
func _ext_curb_in_rev_c_interior(inst: Node3D) -> bool:
	var merged: Dictionary = _ext_merged_aabb(inst)
	if not bool(merged["ok"]):
		return false
	var interior: AABB = AABB(Vector3(-14.1, 0.0, 0.0), Vector3(28.2, 9.1, 9.0))
	return (merged["aabb"] as AABB).intersects(interior)


func _ext_spawn_one(entry: Dictionary, root: Node3D) -> bool:
	var asset: String = String(entry.get("asset", ""))
	var packed: PackedScene = _ext_packed_scene(asset)
	if packed == null:
		return false
	var inst_n: Node = packed.instantiate()
	if inst_n == null or not (inst_n is Node3D):
		if inst_n != null:
			inst_n.free()
		push_warning("[EXT] %s did not instance a Node3D" % asset)
		return false
	var inst: Node3D = inst_n as Node3D
	var eid: int = int(entry.get("id", -1))
	var idx: int = int(entry.get("_i", 0))
	inst.name = "Ext_%d_%s_%d" % [eid, _ext_base(asset), idx]
	inst.position = Vector3(float(entry.get("x", 0.0)), float(entry.get("y", 0.0)), float(entry.get("z", 0.0)))
	var euler: Vector3 = inst.rotation_degrees
	euler.y = float(entry.get("rot_deg", 0.0))
	inst.rotation_degrees = euler
	inst.set_meta("ext_id", eid)
	inst.set_meta("ext_asset", asset)
	inst.add_to_group("exterior_placement")
	var kind: int = _ext_spawn_kind(asset)
	if kind == EXT_KIND_DECAL:
		_set_tree_cast_shadow(inst, GeometryInstance3D.SHADOW_CASTING_SETTING_OFF)
	elif _ext_is_solid(asset):
		_ext_add_solid_collision(inst, asset)
	if _ext_base(asset) == "ext_maglev_car_body":
		_ext_add_tram_nostand_cap(inst)
	root.add_child(inst)
	# North planter curbs cross this interior and clip the wall-mounted props.
	if _ext_base(asset).begins_with("ext_curb_") and _ext_curb_in_rev_c_interior(inst):
		root.remove_child(inst)
		inst.free()
		return false
	_ext_snap_instance(inst, kind, root)
	_ext_apply_visibility_range(inst, kind)
	return true


func _ext_apply_visibility_range(inst: Node3D, kind: int) -> void:
	# [M-07] Cull small exterior props by distance. Ground, guideway and the tram car stay visible.
	# Fade disabled so materials/lighting are unchanged; only far draw calls are skipped.
	if kind == EXT_KIND_GROUND or kind == EXT_KIND_CAR:
		return
	var end_m: float = 25.0 if kind == EXT_KIND_DECAL else 40.0
	for n: Node in inst.find_children("*", "GeometryInstance3D", true, false):
		var gi: GeometryInstance3D = n as GeometryInstance3D
		if gi.visibility_range_end > 0.0:
			continue
		gi.visibility_range_end = end_m
		gi.visibility_range_end_margin = 4.0
		gi.visibility_range_fade_mode = GeometryInstance3D.VISIBILITY_RANGE_FADE_DISABLED


func _ext_deck_slab() -> MeshInstance3D:
	return find_child("PromenadePlazaDeckSlab", true, false) as MeshInstance3D


func _ext_deck_material() -> Material:
	var deck := _ext_deck_slab()
	if deck == null:
		return null
	var mat := deck.get_active_material(0)
	if mat != null:
		return mat
	mat = deck.get_surface_override_material(0)
	if mat != null:
		return mat
	return deck.material_override


func _ext_deck_world_aabb() -> AABB:
	var deck := _ext_deck_slab()
	if deck == null or deck.mesh == null:
		return AABB()
	return deck.global_transform * deck.mesh.get_aabb()


func _ext_push_xz_rect(out: Array[Rect2], x: float, z: float, w: float, d: float) -> void:
	if w > 0.001 and d > 0.001:
		out.append(Rect2(x, z, w, d))


func _ext_ground_strips(slab: AABB) -> Array[Rect2]:
	# Up to four rectangles around the deck AABB, inside the margin rect, with no overlap of the deck.
	var out: Array[Rect2] = []
	var tx0 := EXT_GROUND_X0
	var tx1 := EXT_GROUND_X1
	var tz0 := EXT_GROUND_Z0
	var tz1 := EXT_GROUND_Z1
	if slab.size.x <= 0.0 or slab.size.z <= 0.0:
		_ext_push_xz_rect(out, tx0, tz0, tx1 - tx0, tz1 - tz0)
		return out
	var sx0 := slab.position.x
	var sx1 := sx0 + slab.size.x
	var sz0 := slab.position.z
	var sz1 := sz0 + slab.size.z
	var hx0 := clampf(sx0, tx0, tx1)
	var hx1 := clampf(sx1, tx0, tx1)
	var hz0 := clampf(sz0, tz0, tz1)
	var hz1 := clampf(sz1, tz0, tz1)
	_ext_push_xz_rect(out, tx0, tz0, hx0 - tx0, tz1 - tz0)
	_ext_push_xz_rect(out, hx1, tz0, tx1 - hx1, tz1 - tz0)
	_ext_push_xz_rect(out, hx0, tz0, hx1 - hx0, hz0 - tz0)
	_ext_push_xz_rect(out, hx0, hz1, hx1 - hx0, tz1 - hz1)
	return out


func _ext_strip_name(rect: Rect2, slab: AABB) -> String:
	if slab.size.x <= 0.0:
		return "ExtGroundStrip"
	var sx0 := slab.position.x
	var sx1 := sx0 + slab.size.x
	var sz0 := slab.position.z
	var sz1 := sz0 + slab.size.z
	var rcx := rect.position.x + rect.size.x * 0.5
	var rcz := rect.position.y + rect.size.y * 0.5
	if rcx < sx0 - 0.001:
		return "ExtGroundWest"
	if rcx > sx1 + 0.001:
		return "ExtGroundEast"
	if rcz < sz0 - 0.001:
		return "ExtGroundSouth"
	if rcz > sz1 + 0.001:
		return "ExtGroundNorth"
	return "ExtGroundStrip"


func _ext_add_ground_strip(host: Node3D, rect: Rect2, mat: Material, nm: String) -> void:
	var mi := MeshInstance3D.new()
	mi.name = nm
	var bm := BoxMesh.new()
	bm.size = Vector3(rect.size.x, EXT_GROUND_THICK, rect.size.y)
	mi.mesh = bm
	mi.position = Vector3(rect.position.x + rect.size.x * 0.5, EXT_GROUND_TOP_Y - EXT_GROUND_THICK * 0.5, rect.position.y + rect.size.y * 0.5)
	if mat != null:
		mi.material_override = mat
	var body := StaticBody3D.new()
	body.name = "ExtGroundBody"
	body.add_to_group("ext_ground_col")
	var cs := CollisionShape3D.new()
	cs.name = "ExtGroundShape"
	var shape := BoxShape3D.new()
	shape.size = bm.size
	shape.margin = 0.0
	cs.shape = shape
	body.add_child(cs)
	mi.add_child(body)
	host.add_child(mi)


func _ext_add_ground_extension() -> void:
	var host := Node3D.new()
	host.name = "ExtGroundExtension"
	add_child(host)
	var slab := _ext_deck_world_aabb()
	if slab.size.x <= 0.0:
		push_warning("[EXT] PromenadePlazaDeckSlab missing; ground extension covers the full margin")
	var mat := _ext_deck_material()
	for rect: Rect2 in _ext_ground_strips(slab):
		_ext_add_ground_strip(host, rect, mat, _ext_strip_name(rect, slab))


func _spawn_exterior_placements() -> void:
	_ext_add_ground_extension()
	var n_ground: int = _ext_add_ground_colliders()
	print("[EXT] ground_colliders=%d" % n_ground)
	await get_tree().physics_frame
	var root: Node3D = Node3D.new()
	root.name = "ExteriorPlacements_v1_3"
	add_child(root)
	# Ground-like, then solids, then cars (on magnets), then decals. A physics frame between
	# groups lets the next group snap onto colliders from the previous one.
	var buckets: Array = [[], [], [], []]
	var spawned: int = 0
	if not _ext_fill_buckets(buckets):
		_ext_mark_spawned(0)
		return
	var order: Array[int] = [EXT_KIND_GROUND, EXT_KIND_SOLID, EXT_KIND_CAR, EXT_KIND_DECAL]
	for kind: int in order:
		var batch: Array = buckets[kind]
		for item: Variant in batch:
			if item is Dictionary and _ext_spawn_one(item as Dictionary, root):
				spawned += 1
		await get_tree().physics_frame
	_ext_mark_spawned(spawned)


func _process_qa_exterior_render() -> void:
	if _camera == null:
		push_warning("[EXT] no camera for exterior render")
		get_tree().quit(1)
		return
	if _frame_counter < EXT_RENDER_SETTLE_FRAMES:
		return
	if _ext_shot_frames < 0:
		if _hud != null:
			_hud.visible = false
		_ext_aim_shot(_ext_shot)
		_ext_shot_frames = 0
		return
	_ext_shot_frames += 1
	if _ext_shot_frames < EXT_RENDER_HOLD_FRAMES:
		return
	_ext_save_shot(_ext_shot)
	_ext_shot += 1
	if _ext_shot >= EXT_RENDER_VIEWS.size():
		print("[EXT] exterior render done")
		get_tree().quit(0)
		return
	_ext_aim_shot(_ext_shot)
	_ext_shot_frames = 0


func _ext_aim_shot(idx: int) -> void:
	var view: Dictionary = EXT_RENDER_VIEWS[idx]
	_qa_free_cam(view["pos"] as Vector3, view["at"] as Vector3, Vector3.UP, 58.0)
	_camera.current = true
	print("[EXT] render %s" % String(view["name"]))


func _ext_save_shot(idx: int) -> void:
	var shot_name: String = String(EXT_RENDER_VIEWS[idx]["name"])
	var rel: String = "%s/item4_%s.png" % [EXT_RENDER_DIR, shot_name]
	var tex: ViewportTexture = get_viewport().get_texture()
	if tex == null:
		push_warning("[EXT] no viewport texture for %s" % rel)
		return
	var img: Image = tex.get_image()
	if img == null or img.is_empty():
		push_warning("[EXT] empty viewport image for %s" % rel)
		return
	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(EXT_RENDER_DIR))
	var abs_path: String = ProjectSettings.globalize_path(rel)
	if img.save_png(abs_path) == OK:
		print("[EXT] saved %s" % rel)
	else:
		push_warning("[EXT] failed to save %s" % rel)
