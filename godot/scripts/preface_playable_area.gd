class_name PrefacePlayableArea
extends Node3D
## Aegis-7 // Cylinder Hab-7 — Playable 2-Story Preface Residential Sector (press F5).
## - Portable `res://` asset resolution (BUG-02), locked #05 Hammerhead department bots (BUG-05),
##   live looping animations (BUG-04), null-mesh guard (BUG-07), static collisions + walkable
##   CharacterBody3D 1st/3rd-person controller (BUG-03), interactive pickups / bot queries /
##   #04 Wrist RFID pulse + diegetic HUD (BUG-06).
## - [t3u] grounded low-key lighting, controlled saturation, single eye-level room placards.
## Command-line flags (after `--`): `--render-all` (4 showcase cams), `--validate-only`, `--capture-f5-hud`.

const SECTOR_GLB_PATHS := [
	"res://assets/models/environments/preface_residential_sector.glb",
	"res://assets/models/preface_residential_sector.glb",
	"res://assets/models/environments/preface_residential_two_story_block.glb"
]
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

const CAMERAS := [
	{"name": "cam_01_top_floor_apartment_open_portal", "pos": Vector3(-6.55, 5.72, 4.85), "target": Vector3(-10.45, 5.05, 6.35), "fov": 58.0, "fp_wrist": true},
	{"name": "cam_02_two_story_atrium_staircase_and_sweep_bot", "pos": Vector3(-6.20, 5.95, 2.05), "target": Vector3(5.80, 2.55, -3.20), "fov": 58.0, "fp_wrist": false},
	{"name": "cam_03_open_side_rooms_and_puddle_substation", "pos": Vector3(3.65, 1.85, 0.35), "target": Vector3(4.65, 1.25, 6.50), "fov": 56.0, "fp_wrist": false},
	{"name": "cam_04_ground_concourse_open_exit_and_faction_bots", "pos": Vector3(-2.35, 2.05, -1.65), "target": Vector3(0.15, 1.35, -8.85), "fov": 55.0, "fp_wrist": false}
]

# Player controller tuning
const SPAWN_POS := Vector3(-9.35, 4.25, 6.20)
const SPAWN_YAW_DEG := 28.0  # Faces Apt 201's open portal (X = -11.2m, Z = +2.75m)
const WALK_SPEED := 5.2
const SPRINT_SPEED := 8.2
const JUMP_VELOCITY := 4.8
const GRAVITY := 9.8
const STEP_HEIGHT := 0.32
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
const STARFIELD_ROT_SPEED := 0.045     # rad/s (~2.58 deg/s around longitudinal cylinder axis)
const SCAN_ZONE_RANGE := 1.4          # [QA-HUB-01] max 3D distance probe point -> hub ScanZone
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
var _rostov_anim: String = ""

# Interactables & inventory
var _interactables: Array[Dictionary] = []
var _inventory: Dictionary = {"bci": 0, "jelly": 0, "wire": 0, "batt": 0}
var _inventory_max: Dictionary = {"bci": 0, "jelly": 0, "wire": 0, "batt": 0}
var _nearest: Dictionary = {}

# Lighting
var _sun: DirectionalLight3D
var _fill: DirectionalLight3D
var _task_lights: Array[OmniLight3D] = []
var _task_base: Array[Dictionary] = []
var _emergency: bool = false
var _time: float = 0.0

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
var _qa_cyl: bool = false
var _qa_t38: bool = false
var _qa_ff_door: bool = false
var _qa_hub_shot: bool = false
var _qa_ts: bool = false
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
		elif arg == "--qa-door-hub-shot":
			_qa_hub_shot = true
			_qa_hand = true
		elif arg == "--qa-troubleshoot-simple":
			_qa_ts = true
			_qa_hand = true
		elif arg == "--qa-placement":
			_qa_placement = true
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
	if DisplayServer.get_name() == "headless" and not _batch_render and not _qa_hand and not _qa_placement:
		_validate_only = true
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
		{"name": "Occ_L2_NorthGallerySlab", "size": Vector3(27.8, 0.30, 7.8), "pos": Vector3(0.0, 4.02, 5.0)},
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
		{"name": "UpperL2NorthDeck", "size": Vector3(28.0, 0.24, 8.0), "pos": Vector3(0.0, 4.08, 5.0), "rot_x": 0.0},
		# PATH-06 Fixed: Trimmed UpperL2WestWing to Z = -6.60m..+9.00m (no invisible floor south of Z = -6.60m)
		{"name": "UpperL2WestWing", "size": Vector3(6.5, 0.24, 15.6), "pos": Vector3(-10.65, 4.08, 1.20), "rot_x": 0.0},
		{"name": "UpperL2EastStairLanding", "size": Vector3(6.3, 0.24, 3.4), "pos": Vector3(10.65, 4.08, -0.5), "rot_x": 0.0},
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
	# East Stair-Ramp Connector: smooth sloped box from (Y 4.20, Z -2.20) down to (Y 0.00, Z -7.80) at X = 10.65m
	var run: float = 5.60
	var rise: float = 4.20
	var slope_len: float = sqrt(run * run + rise * rise)
	var ang: float = -atan2(rise, run)
	var up_local: Vector3 = Vector3(0.0, cos(ang), sin(ang))
	var top_center: Vector3 = Vector3(10.65, 2.10 + 0.12, -5.00)
	boxes.append({"name": "EastStairRampConnector", "size": Vector3(2.95, 0.20, slope_len + 0.30), "pos": top_center - up_local * 0.10, "rot_x": ang})
	for b: Dictionary in boxes:
		var cs: CollisionShape3D = CollisionShape3D.new()
		cs.name = String(b["name"])
		var shape: BoxShape3D = BoxShape3D.new()
		shape.size = b["size"] as Vector3
		cs.shape = shape
		cs.position = b["pos"] as Vector3
		cs.rotation = Vector3(float(b["rot_x"]), 0.0, 0.0)
		body.add_child(cs)




func _add_glass_balustrade_colliders(parent: Node3D) -> void:
	# [REAL-02] Mezzanine_Glass_Balustrade has no collider of its own: one thin StaticBody3D per glass run,
	# matching the glb panes (y 4.405..5.465). North run x[-7.6,7.6] @ z 1.25; west run z[-6.4,1.2] @ x -7.55.
	# Neither run crosses the east stair (x >= 9.16) or any doorway (doors at z 2.75 / x -11.5).
	var runs: Array[Dictionary] = [
		{"name": "MezzanineGlassBalustrade_North", "size": Vector3(15.2, 1.06, 0.06), "pos": Vector3(0.0, 4.935, 1.25)},
		{"name": "MezzanineGlassBalustrade_West", "size": Vector3(0.06, 1.06, 7.6), "pos": Vector3(-7.55, 4.935, -2.6)}
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


func _build_cylinder_hab7_fullscale_world(parent: Node3D) -> void:
	var hab_root: Node3D = Node3D.new()
	hab_root.name = "CylinderHab7_FullScale_World"
	parent.add_child(hab_root)

	# 1. Instantiate the full-scale 800m x 400m (R = 200m) O'Neill Cylinder Hab-7 Interior Megastructure
	# Aligned so the Residential Sector Atrium (Z = -9.15m..+9.0m) sits at the Sector-4 Promenade Bay (Valley A bottom nadir)
	# and looking South out Open_Portal_Sector_Exit (-Z) or up through the Atrium Skylight (+Y) looks straight down the
	# curving 800m cylinder axis with paired axial solar rails, Ring-A..Ring-E ribs, agricultural terraces,
	# opposite habitation blocks curving overhead at 120 deg and 240 deg, and the central zero-G docking hub!
	var cyl_path: String = _find_first_existing(CYLINDER_MAP_PATHS)
	var cyl_pivot: Node3D = Node3D.new()
	cyl_pivot.name = "CylinderHab7_DrumAxisPivot"
	# Cylinder local X is axial [-368..+354]; rotate -90 deg Y so axial +X maps to -Z (looking out Sector-4 Promenade Exit)
	# and roll 43 deg around local X so Valley A (137 deg) sits at bottom nadir (180 deg, Y = -14.5m below axis Y = 185.5m).
	cyl_pivot.position = Vector3(0.0, 185.5, -135.0)
	cyl_pivot.rotation_degrees = Vector3(0.0, -90.0, 43.0)
	hab_root.add_child(cyl_pivot)

	var cyl_node: Node3D = _load_glb_scene(cyl_path, 0.85)
	if cyl_node != null:
		cyl_node.name = "CylinderHab7_FullScale_Mesh"
		cyl_node.position = Vector3(0.0, -200.0, 0.0)
		_set_tree_cast_shadow(cyl_node, GeometryInstance3D.SHADOW_CASTING_SETTING_OFF)
		cyl_pivot.add_child(cyl_node)

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
	rail_mat.roughness = 0.28

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
	# Rev C.2 moved #26 out of the building. The sector GLB still contains Apartment_Workbench, so it stays
	# in INTERIOR_ARCH_NODE_NAMES (streaming still detaches it) but is hidden and non-colliding.
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
	_add_architectural_shadow_occluders(_arch_container)
	if not _batch_render:
		_add_safety_floor_colliders(_arch_container)
		_add_glass_balustrade_colliders(_arch_container)

	_build_cylinder_hab7_fullscale_world(_arch_container)
	_build_crisp_3d_signage_and_wall_monitor(_arch_container)
	if not _batch_render:
		_build_cylinder_gravity_ring(_arch_container)


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


func _spawn_interior_pickups(initial_setup: bool = false) -> int:
	var wire_path: String = _find_first_existing(PICKUP_WIRE_PATHS)
	var batt_path: String = _find_first_existing(PICKUP_BATT_PATHS)
	var bci_path: String = _find_first_existing(PICKUP_BCI_PATHS)
	var jelly_path: String = _find_first_existing(PICKUP_JELLY_PATHS)

	var specs: Array[Array] = [
		[wire_path, "Apt201_ToolWall_SuperWire_Spool", "wire", "SUPER-WIRE SPOOL", Vector3(-13.30, 5.02, -4.95), 1.10],
		[bci_path, "Apt201_ToolWall_BCI_Headband", "bci", "BCI HEADBAND", Vector3(-12.85, 5.02, -4.95), 1.15],
		[jelly_path, "Apt201_ToolWall_Thermal_Jelly", "jelly", "THERMAL JELLY CANISTER", Vector3(-12.40, 5.02, -4.95), 1.10],
		[batt_path, "Apt201_ToolWall_Battery_Cell", "batt", "+5A BATTERY CELL", Vector3(-11.95, 5.02, -4.95), 1.10],
		# +0.3 X: the old X -11.85 spool sat 0.10 m from the tool-wall cell at X -11.95.
		[wire_path, "Alcove2C_SuperWire_Expansion", "wire", "SUPER-WIRE SPOOL", Vector3(-11.55, 5.02, -4.95), 1.15],
		[batt_path, "Alcove2C_Battery_Expansion", "batt", "+5A BATTERY CELL", Vector3(-10.75, 5.02, -4.95), 1.15],
		[batt_path, "Apt202_Desk_Battery_Cell", "batt", "+5A BATTERY CELL", Vector3(10.70, 5.10, 7.20), 1.10],
		[wire_path, "Room1A_Laundry_SuperWire_Spool", "wire", "SUPER-WIRE SPOOL", Vector3(-6.15, 0.98, 7.25), 1.15],
		[batt_path, "Room1B_Substation_Battery_Cell", "batt", "+5A BATTERY CELL", Vector3(7.20, 0.98, 7.10), 1.15]
	]
	var spawned: int = 0
	for s: Array in specs:
		var nm: String = String(s[1])
		_spawn_pickup(String(s[0]), nm, String(s[2]), String(s[3]), s[4] as Vector3, float(s[5]), initial_setup)
		if not _collected_pickup_ids.has(nm):
			spawned += 1

	var term: Node3D = Node3D.new()
	term.name = "Apt201_ToolWall_DiagnosticTerminal"
	term.position = Vector3(-12.60, 5.50, -5.30)
	_props_container.add_child(term)
	_interactables.append({"node": term, "id": "Apt201_ToolWall_DiagnosticTerminal", "kind": "terminal", "label": "APT 201 TOOL WALL TERMINAL", "collected": false, "pickup": false})
	spawned += 1
	# [5DB-03] D-204 hatch emitter. No hatch door mesh in this sector yet; [E] opens the simple troubleshoot UI.
	# Sits on the APT 201 tool wall, beside the terminal and clear of the pickup row at z=-4.95.
	var hatch: Node3D = Node3D.new()
	hatch.name = "Hatch_D204_EmitterPanel"
	hatch.position = Vector3(-11.20, 5.45, -5.30)
	_props_container.add_child(hatch)
	_interactables.append({"node": hatch, "id": "Hatch_D204_EmitterPanel", "kind": "troubleshoot", "label": "HATCH FIELD EMITTER D-204", "collected": false, "pickup": false})
	spawned += 1
	return spawned


# Baked one-shot / loop clips. Pivot is bottom-centre, front is local +Z, back is local -Z.
# Hall floor top is y=0.235. Yaw 180 maps local -Z onto world +Z (north wall face z=8.76).
# Yaw 90 maps local -Z onto world -X (west wall).
const ANIMATED_PROP_SPECS: Array[Dictionary] = [
	{
		# north wall z 8.76, laundry segment x -3.48..-0.48, clear of pillar at x -0.28..0.28
		"id": "Prop38_FoldingCounter",
		"path": "res://assets/models/folding_counter_fold_leaf_3p0.glb",
		"position": Vector3(-1.98, 0.235, 8.45),
		"yaw": 180.0,
		"mount": "wall",
		"label": "LAUNDRY FOLDING COUNTER",
		"toggle": ["Leaf_Fold_Up", "Leaf_Fold_Down"],
		"action": "",
		"idle": ""
	},
	{
		# bare north-wall segment x -4.90..-3.70 (z 8.76), clear of #38 (x -3.48) and the corner chamfer; moved off the wood-topped counter block in Side_Room_East_Lounge
		"id": "Prop39_FlipSeat",
		"path": "res://assets/models/laundry_bench_wall_flip_seat.glb",
		"position": Vector3(-4.30, 0.235, 8.55),
		"yaw": 180.0,
		"mount": "wall",
		"label": "LAUNDRY FLIP SEAT",
		"toggle": ["Seat_Flip_Down", "Seat_Flip_Up"],
		"action": "",
		"idle": ""
	},
	{
		# footprint x 9.43..11.93, clear of pillar x 12.2
		"id": "Prop42_Substation",
		"path": "res://assets/models/substation_wall_ladder_busway.glb",
		"position": Vector3(10.68, 0.235, 8.35),
		"yaw": 180.0,
		"mount": "wall",
		"label": "MAINTENANCE SUBSTATION",
		"toggle": [],
		"action": "Cell_Swap",
		"idle": "Port_Ready_Blink"
	},
	{
		# footprint x 7.38..9.28, east of the 15 mm floor plate x<=7.25 z 7.55..8.15 that sat in its front zone
		"id": "Prop43_SparesDispenser",
		"path": "res://assets/models/spares_gravity_dispenser.glb",
		"position": Vector3(8.33, 0.235, 8.50),
		"yaw": 180.0,
		"mount": "wall",
		"label": "MAINTENANCE SPARES DISPENSER",
		"toggle": [],
		"action": "Capsule_Drop",
		"idle": "Pick_Ready_Blink"
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
	var f_held: bool = _preset_active < 0 and not _capture_hud and Input.is_physical_key_pressed(KEY_F)
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

	# Skylight directional sun angled steeply (-64 deg) through the central atrium skylight opening
	# with 4-split PSSM cascades & calibrated normal bias so L2 floor slabs cast solid shadows and never peter-pan.
	_sun = DirectionalLight3D.new()
	_sun.name = "AtriumGoldenHourSunlight"
	_sun.rotation_degrees = Vector3(-72.0, -162.0, 0.0)
	_sun.light_color = Color("#FFF4E0")
	_sun.light_energy = 0.78
	_sun.shadow_enabled = true
	_sun.directional_shadow_mode = DirectionalLight3D.SHADOW_PARALLEL_4_SPLITS
	_sun.directional_shadow_max_distance = 45.0
	_sun.shadow_bias = 0.015
	_sun.shadow_normal_bias = 1.0
	_sun.shadow_blur = 1.2
	_lights_container.add_child(_sun)

	_fill = DirectionalLight3D.new()
	_fill.name = "AtriumSkyBounceFill"
	_fill.rotation_degrees = Vector3(-42.0, -145.0, 0.0)
	_fill.light_color = Color("#C8DCF0")
	_fill.light_energy = 0.28
	_fill.shadow_enabled = false
	_lights_container.add_child(_fill)

	# Box-projected ReflectionProbe covering the 28m x 18m x 9m residential atrium for grounded metallic & glass reflections.
	var rprobe: ReflectionProbe = ReflectionProbe.new()
	rprobe.name = "AtriumBoxReflectionProbe"
	rprobe.position = Vector3(0.0, 4.4, 0.0)
	rprobe.size = Vector3(30.0, 10.0, 20.0)
	rprobe.box_projection = true
	rprobe.intensity = 0.3
	rprobe.ambient_mode = ReflectionProbe.AMBIENT_ENVIRONMENT
	rprobe.update_mode = ReflectionProbe.UPDATE_ONCE
	_lights_container.add_child(rprobe)

	# Physical ceiling luminaires + clean room lighting (OmniLight3D shadow_enabled = false so rooms never have 2 competing sets of shadows
	# or cast L2 character shadows down through floor slabs onto L1).
	for l_cfg: Dictionary in [
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


func _set_emergency_lighting(on: bool) -> void:
	_emergency = on
	if _sun != null:
		_sun.light_energy = 0.05 if on else 0.78
	if _fill != null:
		_fill.light_energy = 0.04 if on else 0.34
	for i: int in range(_task_lights.size()):
		var l: OmniLight3D = _task_lights[i]
		if on:
			l.light_color = Color("#C2402A")
		else:
			l.light_color = _task_base[i]["col"] as Color
			l.light_energy = float(_task_base[i]["e"])
	if _world_env != null and _world_env.environment != null:
		_world_env.environment.ambient_light_energy = 0.07 if on else 0.36
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
				for s_idx: int in range(mi.mesh.get_surface_count()):
					var mat: Material = mi.get_active_material(s_idx)
					if mat is StandardMaterial3D:
						var smat: StandardMaterial3D = (mat as StandardMaterial3D).duplicate() as StandardMaterial3D
						var mname: String = smat.resource_name.to_lower()
						var pname: String = mi.name.to_lower()
						smat.cull_mode = BaseMaterial3D.CULL_DISABLED
						if mname.contains("glass") or mname.contains("translucent") or mname.contains("holo") or mname.contains("lens") or pname.contains("glass") or pname.contains("window"):
							smat.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
							smat.albedo_color = Color(0.35, 0.42, 0.47, clampf(smat.albedo_color.a, 0.22, 0.30))
							smat.roughness = 0.08
							smat.metallic = 0.16
							smat.metallic_specular = 0.75
							if mname.contains("holo") or mname.contains("lens"):
								smat.emission_enabled = true
								smat.emission_energy_multiplier = emission_mult * 0.8
							else:
								smat.emission_enabled = false
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
		_player_body.rotate_object_local(Vector3.UP, -mm.screen_relative.x * MOUSE_SENS)
		_pitch -= mm.screen_relative.y * MOUSE_SENS
		_apply_pitch()
		return
	if event is InputEventKey:
		var ke: InputEventKey = event as InputEventKey
		if not ke.pressed or ke.echo:
			return
		match ke.physical_keycode:
			KEY_ESCAPE:
				Input.mouse_mode = Input.MOUSE_MODE_VISIBLE
			KEY_G:
				_toggle_gravity_ring_test()
			KEY_V, KEY_TAB:
				_toggle_view()
			KEY_E:
				_interact()
			KEY_F:
				_trigger_rfid_pulse()
			KEY_R:
				_toggle_flashlight()
			KEY_N:
				_set_emergency_lighting(not _emergency)
			KEY_1:
				_activate_preset(0)
			KEY_2:
				_activate_preset(1)
			KEY_3:
				_activate_preset(2)
			KEY_4:
				_activate_preset(3)
			KEY_0:
				_return_to_player()
				_show_toast("ACTIVE PLAYER CONTROL", 1.5)
			_:
				return
		get_viewport().set_input_as_handled()


func _apply_pitch() -> void:
	var lo: float = deg_to_rad(-60.0) if _third_person else deg_to_rad(PITCH_MIN_DEG)
	var hi: float = deg_to_rad(45.0) if _third_person else deg_to_rad(PITCH_MAX_DEG)
	_pitch = clampf(_pitch, lo, hi)
	if _camera_pivot != null:
		_camera_pivot.rotation = Vector3(_pitch, 0.0, 0.0)


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
		_update_first_person_arm(delta)
		return
	var controls: bool = _preset_active < 0 and not _capture_hud and not _troubleshoot_ui_open()

	var input_dir: Vector2 = Vector2.ZERO
	var sprint: bool = false
	var jump: bool = false
	if controls:
		# Keyboard look: Q / Left = turn left, Right = turn right, PageUp / PageDown = look up / down.
		var yaw_in: float = 0.0
		if Input.is_physical_key_pressed(KEY_Q) or Input.is_physical_key_pressed(KEY_LEFT):
			yaw_in += 1.0
		if Input.is_physical_key_pressed(KEY_RIGHT):
			yaw_in -= 1.0
		if yaw_in != 0.0:
			b.rotate_object_local(Vector3.UP, yaw_in * KEY_LOOK_SPEED * delta)
		var pitch_in: float = 0.0
		if Input.is_physical_key_pressed(KEY_PAGEUP):
			pitch_in += 1.0
		if Input.is_physical_key_pressed(KEY_PAGEDOWN):
			pitch_in -= 1.0
		if pitch_in != 0.0:
			_pitch += pitch_in * KEY_LOOK_SPEED * 0.6 * delta
			_apply_pitch()
		if Input.is_physical_key_pressed(KEY_W) or Input.is_physical_key_pressed(KEY_UP):
			input_dir.y -= 1.0
		if Input.is_physical_key_pressed(KEY_S) or Input.is_physical_key_pressed(KEY_DOWN):
			input_dir.y += 1.0
		if Input.is_physical_key_pressed(KEY_A):
			input_dir.x -= 1.0
		if Input.is_physical_key_pressed(KEY_D):
			input_dir.x += 1.0
		sprint = Input.is_physical_key_pressed(KEY_SHIFT)
		jump = Input.is_physical_key_pressed(KEY_SPACE)

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

	var v_up: float = b.velocity.dot(up_dir)
	if not b.is_on_floor():
		v_up = (b.velocity + g_vec * delta).dot(up_dir)
	elif jump:
		v_up = JUMP_VELOCITY
	b.velocity = dir * speed + up_dir * v_up

	# Smooth step-up over small ledges (thresholds, treads, slab lips) — only for wall-like hits,
	# so gently curving floors (cylinder ring) never trigger a bogus step.
	if b.is_on_floor() and dir != Vector3.ZERO:
		var motion: Vector3 = dir * speed * delta
		var hit: KinematicCollision3D = KinematicCollision3D.new()
		if b.test_move(b.global_transform, motion, hit) and hit.get_normal().dot(up_dir) < 0.5:
			var up: Vector3 = up_dir * STEP_HEIGHT
			if not b.test_move(b.global_transform, up) and not b.test_move(b.global_transform.translated(up), motion):
				b.global_position += up

	b.move_and_slide()
	for sc_i: int in range(b.get_slide_collision_count()):
		var scol: KinematicCollision3D = b.get_slide_collision(sc_i)
		if scol.get_collider() is RigidBody3D:
			(scol.get_collider() as RigidBody3D).apply_central_impulse(-scol.get_normal() * 1.4)

	if not in_ring and b.global_position.y < -8.0:
		_respawn()
	_update_interior_streaming(b.global_position)
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
		_starfield_cylinder.rotate_z(STARFIELD_ROT_SPEED * delta)
	_ff_tick_active_stalls(delta)
	_update_rfid_doors(delta)
	_sync_reticle_to_viewport_center()
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
	if _emergency:
		var e: float = 0.30 + 0.22 * (0.5 + 0.5 * sin(_time * 3.2))
		for l: OmniLight3D in _task_lights:
			l.light_energy = e
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
			# 1st-person: turn toward the Apt 201 workbench and raise the #04 wrist ([F] pulse) so the sleeve + rings + [E] prompt are in frame.
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
			# Shot 1: Inside APT 201 showing solid bulkhead wall + new Wall Diagnostic Monitor (X=-7.8, Z=2.86) + workbench + clean HUD
			_third_person = false
			_player_body.global_position = Vector3(-9.15, 4.35, 5.45)
			_player_body.velocity = Vector3.ZERO
			_player_body.rotation_degrees = Vector3(0.0, -24.0, 0.0)
			_pitch = deg_to_rad(-2.0)
			_apply_view_mode()
		94:
			_save_qa_png("apt201_wall_monitor_and_clean_hud.png")
			# Shot 2: L2 North Mezzanine Gallery showing unobstructed walkway (PATH-01 fixed), Sweep #0812, and crisp APT 202 lintel skin
			_third_person = false
			_player_body.global_position = Vector3(-4.20, 4.25, 1.95)
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
	_qa_place(Vector3(0.0, 0.25, -15.0), 0.0, -4.0)
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
		_qa_place(Vector3(0.0, 0.25, -20.0), 0.0, -4.0)
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

	# --- 7. [F] wrist raise + RFID PulseRings (APT 201 workbench) ---
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

	# --- 8. [E] interact reach + pickup removal (APT 201 tool wall) ---
	# Stand on the shelf's +Z side and aim at the BCI. Yaw 180 faces +Z, away from the wall at Z -4.95.
	var wall_pick: Node3D = _props_container.get_node_or_null("Apt201_ToolWall_BCI_Headband") as Node3D
	var wall_aim: Vector3 = wall_pick.global_position if wall_pick != null else Vector3(-12.85, 5.02, -4.95)
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
	# 2600 pinpoint stars
	for i: int in range(2600):
		var sx: int = rng.randi_range(0, w - 1)
		var sy: int = rng.randi_range(0, h - 1)
		var b: float = rng.randf_range(0.55, 1.0)
		var col: Color = palette[i % palette.size()] * b
		col.a = 1.0
		img.set_pixel(sx, sy, col)
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
	# [t38u] Massive far-offset outer starfield cylinder coaxial with Cylinder Hab-7 axis (Y = 185.5m, Z-axis).
	# The outer starfield cylinder rotates in _process(delta) while CylinderHab7_FullScale_World stays 100% stationary!
	_starfield_cylinder = Node3D.new()
	_starfield_cylinder.name = "StarfieldOuterCylinder"
	_starfield_cylinder.position = Vector3(0.0, 185.5, -135.0)
	parent.add_child(_starfield_cylinder)

	var star_tex: ImageTexture = _make_procedural_starfield_texture()
	var smat: StandardMaterial3D = StandardMaterial3D.new()
	smat.resource_name = "Mat_StarfieldOuterCylinder"
	smat.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	smat.cull_mode = BaseMaterial3D.CULL_DISABLED
	smat.albedo_color = Color(1.0, 1.0, 1.0, 1.0)
	smat.albedo_texture = star_tex
	smat.uv1_scale = Vector3(6.0, 3.0, 1.0)
	smat.texture_filter = BaseMaterial3D.TEXTURE_FILTER_LINEAR_WITH_MIPMAPS

	var barrel: MeshInstance3D = MeshInstance3D.new()
	barrel.name = "StarfieldOuterBarrelMesh"
	var cm: CylinderMesh = CylinderMesh.new()
	cm.top_radius = STARFIELD_CYL_RADIUS
	cm.bottom_radius = STARFIELD_CYL_RADIUS
	cm.height = STARFIELD_CYL_LENGTH
	cm.radial_segments = 96
	cm.rings = 1
	cm.cap_top = true
	cm.cap_bottom = true
	barrel.mesh = cm
	# CylinderMesh height is along local Y; rotate 90 deg around X so the cylinder axis aligns with world Z.
	barrel.rotation = Vector3(PI * 0.5, 0.0, 0.0)
	barrel.material_override = smat
	barrel.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	barrel.extra_cull_margin = 16384.0
	_starfield_cylinder.add_child(barrel)


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
	for l: OmniLight3D in _task_lights:
		l.visible = true
	for sl: Node in _lights_container.get_children():
		if sl is SpotLight3D:
			(sl as SpotLight3D).visible = true
	_interiors_loaded = true
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

	var door_specs: Array[Dictionary] = [
		{"id": "DOOR_APT201", "label": "APT 201 // RFID FORCE-FIELD DOOR", "pos": Vector3(-11.20, 4.32, 2.75), "w": 2.00, "h": 2.55},
		{"id": "DOOR_ALCOVE2C", "label": "ALCOVE 2C // RFID FORCE-FIELD DOOR", "pos": Vector3(-11.50, 4.32, -3.55), "w": 1.80, "h": 2.45},
		{"id": "DOOR_APT202", "label": "APT 202 // RFID FORCE-FIELD DOOR", "pos": Vector3(7.80, 4.32, 2.75), "w": 2.00, "h": 2.55},
		{"id": "DOOR_RM1A", "label": "RM 1A LAUNDRY // RFID FORCE-FIELD DOOR", "pos": Vector3(-8.50, 0.12, 2.85), "w": 2.40, "h": 2.60},
		{"id": "DOOR_RM1B", "label": "RM 1B SUBSTATION // RFID FORCE-FIELD DOOR", "pos": Vector3(4.50, 0.12, 2.85), "w": 2.20, "h": 2.60},
		{"id": "DOOR_SECTOR4_EXIT", "label": "SECTOR-4 PROMENADE EXIT // RFID FORCE-FIELD DOOR", "pos": Vector3(0.0, 0.12, -8.90), "w": 2.60, "h": 2.80}
	]
	for spec: Dictionary in door_specs:
		var did: String = String(spec["id"])
		var dpos: Vector3 = spec["pos"] as Vector3
		var pw: float = float(spec["w"])
		var ph: float = float(spec["h"])
		# Player-facing (atrium) side is world -Z for the 4 room portals, +Z for Sector-4 exit & Alcove 2C.
		var face_neg_z: bool = (did != "DOOR_SECTOR4_EXIT" and did != "DOOR_ALCOVE2C")
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
		# Colliders: everything outside the 1.50 x 2.45 m clear opening is solid; the field itself is a toggled box.
		var field_cs: CollisionShape3D = null
		if not _batch_render:
			var side_w: float = maxf(half_pw, FF_FRAME_HALF_W) - FF_OPEN_W * 0.5 + 0.03
			for sx2: float in [-1.0, 1.0]:
				_ff_static_box(droot, "PortalJambCollider_%s" % ("L" if sx2 < 0.0 else "R"), Vector3(side_w, ph + 0.03, 0.30),
					Vector3(sx2 * (FF_OPEN_W * 0.5 + side_w * 0.5), (ph + 0.03) * 0.5, 0.0))
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
	# HubWallBacking only if no shift works (ALCOVE2C has no wall). Same path for every door.
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


func _ff_apply_colliders(door: Dictionary, force_on: bool = false) -> void:
	var split: bool = bool(door.get("split", false))
	if not split:
		var blocking: bool = force_on or not bool(door.get("open", false))
		_ff_set_cs(door.get("field_collider") as CollisionShape3D, blocking)
		return
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
	var b: MeshInstance3D = MeshInstance3D.new()
	b.name = "FieldPlane_B"
	b.mesh = _ff_half_mesh(false)
	b.transform = plane.transform
	b.material_override = mat_b
	b.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
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
	# [QA-HUB-01] An [E] door scan acts on ONE door: the one whose hub ScanZone is nearest, within SCAN_ZONE_RANGE
	# (3D, so other floors never qualify) and roughly in front of the camera (flattened dot >= SCAN_FACING_DOT).
	var fwd: Vector3 = (-_camera.global_transform.basis.z) if _camera != null else Vector3.FORWARD
	fwd.y = 0.0
	if fwd.length() < 0.001:
		return {}
	fwd = fwd.normalized()
	var best: Dictionary = {}
	var best_d: float = SCAN_ZONE_RANGE
	for door: Dictionary in _rfid_doors:
		var droot: Node3D = door["root"] as Node3D
		if droot == null or not is_instance_valid(droot) or not droot.is_inside_tree():
			continue
		var target: Vector3 = door["center"] as Vector3
		var d: float = origin.distance_to(target)
		if d > best_d:
			continue
		var flat: Vector3 = target - origin
		flat.y = 0.0
		if flat.length() > 0.05 and fwd.dot(flat.normalized()) < SCAN_FACING_DOT:
			continue
		# Must be on the hub's side of the wall: (player - hub) . hub outward +Z normal > 0
		var hub_n: Node3D = door.get("hub") as Node3D
		if hub_n != null and (origin - hub_n.global_position).dot(hub_n.global_transform.basis.z.normalized()) <= 0.0:
			continue
		best_d = d
		best = door
	return best


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

	# Aim inside APT 201 at the workbench and capture reticle centered check
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

	# Place player outside on the Sector-4 Promenade deck looking toward the forward end-cap starfield vista
	_qa_place(Vector3(0.0, 0.25, -32.0), 0.0, 12.0)
	await _qa_frames(15)
	var hab_xf0: Transform3D = hab_world.global_transform if hab_world != null else Transform3D.IDENTITY
	var star_rot0: float = _starfield_cylinder.rotation.z if _starfield_cylinder != null else 0.0
	var img_star1: Image = await _qa_capture("qa_outer_starfield_rotating_1.png")
	await _qa_frames(90)
	var hab_xf1: Transform3D = hab_world.global_transform if hab_world != null else Transform3D.IDENTITY
	var star_rot1: float = _starfield_cylinder.rotation.z if _starfield_cylinder != null else 0.0
	# Advance starfield rotation by an extra visual arc so the two screenshots clearly show star rotation
	if _starfield_cylinder != null:
		_starfield_cylinder.rotate_z(deg_to_rad(14.0))
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
		var from_south: bool = (did != "DOOR_SECTOR4_EXIT" and did != "DOOR_ALCOVE2C")
		var start_z: float = (dpos.z - 1.55) if from_south else (dpos.z + 1.55)
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
	# [REAL-02] rays across the mezzanine glass hit its own colliders
	var space_g: PhysicsDirectSpaceState3D = get_world_3d().direct_space_state
	var g_hits: PackedStringArray = PackedStringArray()
	var g_ok: bool = true
	# Rays across each run (3 points per run, y 4.5 / 4.9 / 5.4) masked to the glass layer: every one must hit the run.
	var g_rays: Array[Array] = []
	for gx: float in [-6.0, 0.0, 6.0]:
		g_rays.append([Vector3(gx, 4.5 + absf(gx) * 0.075, 0.7), Vector3(gx, 4.5 + absf(gx) * 0.075, 1.8), "MezzanineGlassBalustrade_North"])
	for gz: float in [-5.5, -2.6, 0.6]:
		g_rays.append([Vector3(-7.0, 4.9, gz), Vector3(-8.1, 4.9, gz), "MezzanineGlassBalustrade_West"])
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
	# Collect the BCI headband on the APT 201 tool wall first so we can verify it stays collected.
	# Yaw 180 at (-12.85, 4.30, -4.20) faces +Z, away from the shelf at Z -4.95, so [E] used to take the spool.
	var bci_pick: Node3D = _props_container.get_node_or_null("Apt201_ToolWall_BCI_Headband") as Node3D
	var bci_aim: Vector3 = bci_pick.global_position if bci_pick != null else Vector3(-12.85, 5.02, -4.95)
	_qa_place(Vector3(bci_aim.x, 4.30, bci_aim.z + 0.75), 0.0, 0.0)
	await _qa_frames(8)
	if bci_pick != null and is_instance_valid(bci_pick):
		bci_aim = bci_pick.global_position
	_qa_place(Vector3(bci_aim.x, 4.30, bci_aim.z + 0.75), 0.0, 0.0)
	_qa_aim_at(bci_aim)
	_update_hud()
	var bci_label: String = String(_nearest.get("label", ""))
	var bci_prompt: String = _hud_prompt.text if _hud_prompt != null else ""
	_qa_t38_check("reticle_target_bci_headband", bci_label == "BCI HEADBAND" and bci_prompt.contains("BCI HEADBAND"),
		"label=%s prompt='%s'" % [bci_label, bci_prompt])
	var inv_before: int = int(_inventory["bci"])
	_interact()
	await _qa_frames(4)
	var collected_ok: bool = _collected_pickup_ids.has("Apt201_ToolWall_BCI_Headband") and int(_inventory["bci"]) == inv_before + 1
	_qa_t38_check("pickup_collected_before_exit", collected_ok, "collected=%s inv_bci=%d" % [str(_collected_pickup_ids.keys()), int(_inventory["bci"])])
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
	var bci_respawned: bool = _props_container.get_node_or_null("Apt201_ToolWall_BCI_Headband") != null
	var actors_back: int = 0
	for ac2: Node in _actors_container.get_children():
		if ac2 is Node3D and (ac2 as Node3D).position.z > -7.5:
			actors_back += 1
	_qa_t38_check("interior_respawn_on_vestibule_reentry", _interiors_loaded and int(st_in["live_pickups"]) == live_before and not bci_respawned and actors_back > 0 and wb_retired and int(_inventory["bci"]) == inv_before + 1,
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
	# The hatch id is DOOR_D204; this sector has no hatch door mesh yet.
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
	# [5DB-03] Stand on the panel's +Z side and aim with the D670-01 helper, then [E].
	# z + 0.35 keeps the probe nearer the emitter than the pickup row on z=-4.95.
	var panel: Node3D = _props_container.get_node_or_null("Hatch_D204_EmitterPanel") as Node3D
	var aim: Vector3 = panel.global_position if panel != null else Vector3(-11.20, 5.45, -5.30)
	_qa_place(Vector3(aim.x, 4.30, aim.z + 0.35), 0.0, 0.0)
	if panel != null and is_instance_valid(panel):
		aim = panel.global_position
	_qa_aim_at(aim)
	var nearest_id: String = String(_find_nearest_interactable(INTERACT_RANGE).get("id", ""))
	var cam_fwd: Vector3 = (-_camera.global_transform.basis.z).normalized() if _camera != null else Vector3.FORWARD
	var to_panel: Vector3 = aim - (_camera.global_position if _camera != null else _player_body.global_position)
	var aimed_dot: float = cam_fwd.dot(to_panel.normalized()) if to_panel.length_squared() > 0.0001 else 0.0
	_interact()
	await get_tree().process_frame
	var opened_ok: bool = nearest_id == "Hatch_D204_EmitterPanel" and aimed_dot > 0.99 and _troubleshoot_ui_open() and _ts_ui.device_id == "D-204" and _ts_ui.visible
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
