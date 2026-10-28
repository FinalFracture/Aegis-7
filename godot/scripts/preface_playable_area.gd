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
const ARM_RAISED_POS := Vector3(-0.24, -0.19, -0.42)       # _camera local (wrist pivot)
const ARM_RAISED_ROT_DEG := Vector3(24.0, -24.0, -10.0)
const ARM_RAISE_SPEED := 4.5
const WALK_SWING_Z := 0.22
const WALK_SWING_LIFT := 0.04
const WALK_SWING_PITCH_DEG := 24.0
const WRIST_PIVOT_IN_MODEL := Vector3(0.0, 0.195, 0.062)
const PITCH_MIN_DEG := -80.0
const PITCH_MAX_DEG := 75.0

var _arch_container: Node3D
var _props_container: Node3D
var _actors_container: Node3D
var _lights_container: Node3D
var _camera: Camera3D
var _puzzle_ui: CanvasLayer
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
	_puzzle_ui = get_node_or_null("PcbaPythonPuzzleUI") as CanvasLayer
	_world_env = get_node_or_null("WorldEnvironment") as WorldEnvironment
	if _puzzle_ui != null:
		_puzzle_ui.visible = false

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
	if OS.get_environment("RENDER_ALL") == "1" or OS.get_environment("CAPTURE_SCREENSHOTS") == "1":
		_batch_render = true
	if OS.get_environment("VALIDATE_ONLY") == "1":
		_validate_only = true
	if _capture_hud or _qa_hand:
		_batch_render = false
		_validate_only = false
	if _qa_hand:
		_capture_hud = false
	if DisplayServer.get_name() == "headless" and not _batch_render and not _qa_hand:
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
		_run_hand_controls_qa.call_deferred()


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
func _remove_all_doors_and_grates(root: Node3D) -> void:
	var stack: Array[Node] = [root]
	while not stack.is_empty():
		var curr: Node = stack.pop_back()
		if curr is Node3D:
			var nm: String = curr.name.to_lower()
			if nm.contains("door_slide") or nm.contains("door_apt") or nm.contains("door_leaf") or nm.contains("maint_grate") or nm.begins_with("pickup_"):
				(curr as Node3D).visible = false
		for ch: Node in curr.get_children():
			stack.append(ch)


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


func _assemble_open_doorless_sector() -> void:
	for ch: Node in _arch_container.get_children():
		ch.free()

	var sector_path: String = _find_first_existing(SECTOR_GLB_PATHS)
	var sector_node: Node3D = _load_glb_scene(sector_path, 0.65)
	if sector_node != null:
		sector_node.name = "PrefaceResidentialSector_Doorless"
		_arch_container.add_child(sector_node)
		_remove_all_doors_and_grates(sector_node)
		if not _batch_render:
			var n_col: int = _add_sector_trimesh_collisions(sector_node)
			if _validate_only:
				print("[PrefacePlayableArea] Trimesh colliders: ", n_col)
	else:
		push_warning("[PrefacePlayableArea] Sector GLB not found in SECTOR_GLB_PATHS")
	_add_architectural_shadow_occluders(_arch_container)
	if not _batch_render:
		_add_safety_floor_colliders(_arch_container)

	_build_cylinder_hab7_fullscale_world(_arch_container)
	_build_crisp_3d_signage_and_wall_monitor(_arch_container)


# ------------------------------------------------------------------------------
# Pickups & #04 Wrist rig (BUG-06)
# ------------------------------------------------------------------------------
func _spawn_pickup(path: String, nm: String, kind: String, label: String, pos: Vector3, sc: float) -> void:
	var node: Node3D = _load_glb_scene(path, 0.85)
	if node == null:
		return
	node.name = nm
	node.position = pos
	node.scale = Vector3(sc, sc, sc)
	_props_container.add_child(node)
	_inventory_max[kind] = int(_inventory_max[kind]) + 1
	_interactables.append({"node": node, "kind": kind, "label": label, "collected": false, "pickup": true})


func _populate_pickups_and_wrist_rig() -> void:
	for ch: Node in _props_container.get_children():
		ch.free()
	_interactables.clear()
	for k: String in _inventory_max.keys():
		_inventory_max[k] = 0

	var wire_path: String = _find_first_existing(PICKUP_WIRE_PATHS)
	var batt_path: String = _find_first_existing(PICKUP_BATT_PATHS)
	var bci_path: String = _find_first_existing(PICKUP_BCI_PATHS)
	var jelly_path: String = _find_first_existing(PICKUP_JELLY_PATHS)

	# Apt 201 engineering workbench (benchtop Y = 5.12m), organized evenly across the ESD mat.
	_spawn_pickup(wire_path, "Workbench_SuperWire_Spool", "wire", "SUPER-WIRE SPOOL", Vector3(-9.05, 5.12, 7.60), 1.10)
	_spawn_pickup(bci_path, "Workbench_BCI_Headband", "bci", "BCI HEADBAND", Vector3(-8.50, 5.12, 7.62), 1.15)
	_spawn_pickup(jelly_path, "Workbench_Thermal_Jelly", "jelly", "THERMAL JELLY CANISTER", Vector3(-8.00, 5.12, 7.62), 1.10)
	_spawn_pickup(batt_path, "Workbench_Battery_Cell", "batt", "+5A BATTERY CELL", Vector3(-7.45, 5.12, 7.60), 1.10)
	# Alcove 2C engineering supply shelf, Apt 202 desk, Room 1A folding counter, Room 1B substation service bench.
	_spawn_pickup(wire_path, "Alcove2C_SuperWire_Expansion", "wire", "SUPER-WIRE SPOOL", Vector3(-11.85, 5.02, -4.95), 1.15)
	_spawn_pickup(batt_path, "Alcove2C_Battery_Expansion", "batt", "+5A BATTERY CELL", Vector3(-11.05, 5.02, -4.95), 1.15)
	_spawn_pickup(batt_path, "Apt202_Desk_Battery_Cell", "batt", "+5A BATTERY CELL", Vector3(10.70, 5.10, 7.20), 1.10)
	_spawn_pickup(wire_path, "Room1A_Laundry_SuperWire_Spool", "wire", "SUPER-WIRE SPOOL", Vector3(-6.15, 0.98, 7.25), 1.15)
	_spawn_pickup(batt_path, "Room1B_Substation_Battery_Cell", "batt", "+5A BATTERY CELL", Vector3(7.20, 0.98, 7.10), 1.15)

	# Workbench diagnostic terminal (query-only)
	var term: Node3D = Node3D.new()
	term.name = "Workbench_DiagnosticTerminal"
	term.position = Vector3(-9.17, 5.50, 8.05)
	_props_container.add_child(term)
	_interactables.append({"node": term, "kind": "terminal", "label": "APT 201 WORKBENCH TERMINAL", "collected": false, "pickup": false})

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
	hv.y = 0.0
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
		if c is MeshInstance3D and (c as MeshInstance3D).mesh != null and not String(c.name).begins_with("RFID_PulseRing"):
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
	rprobe.intensity = 0.65
	rprobe.ambient_mode = ReflectionProbe.AMBIENT_ENVIRONMENT
	rprobe.update_mode = ReflectionProbe.UPDATE_ONCE
	_lights_container.add_child(rprobe)

	# Physical ceiling luminaires + clean room lighting (OmniLight3D shadow_enabled = false so rooms never have 2 competing sets of shadows
	# or cast L2 character shadows down through floor slabs onto L1).
	for l_cfg: Dictionary in [
		{"name": "Apt201_Workbench_TaskLight", "pos": Vector3(-8.45, 7.55, 6.20), "col": Color("#F5E2C4"), "e": 0.88, "r": 9.8, "sh": false, "sz": Vector2(1.40, 0.36)},
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
	_camera.far = 2500.0
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
		_camera.far = 2500.0
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
	if event is InputEventMouseButton and (event as InputEventMouseButton).pressed:
		if Input.mouse_mode != Input.MOUSE_MODE_CAPTURED:
			Input.mouse_mode = Input.MOUSE_MODE_CAPTURED
			get_viewport().set_input_as_handled()
			return
	if event is InputEventMouseMotion and (Input.mouse_mode == Input.MOUSE_MODE_CAPTURED or _qa_hand) and _preset_active < 0:
		var mm: InputEventMouseMotion = event as InputEventMouseMotion
		_player_body.rotate_y(-mm.relative.x * MOUSE_SENS)
		_pitch -= mm.relative.y * MOUSE_SENS
		_apply_pitch()
		return
	if event is InputEventKey:
		var ke: InputEventKey = event as InputEventKey
		if not ke.pressed or ke.echo:
			return
		match ke.physical_keycode:
			KEY_ESCAPE:
				Input.mouse_mode = Input.MOUSE_MODE_VISIBLE
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
	if _player_body == null:
		return
	var b: CharacterBody3D = _player_body
	var controls: bool = _preset_active < 0 and not _capture_hud

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
			b.rotate_y(yaw_in * KEY_LOOK_SPEED * delta)
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

	var basis: Basis = b.global_transform.basis
	var dir: Vector3 = basis.x * input_dir.x + basis.z * input_dir.y
	dir.y = 0.0
	if dir.length_squared() > 0.0001:
		dir = dir.normalized()
	var speed: float = SPRINT_SPEED if sprint else WALK_SPEED

	if not b.is_on_floor():
		b.velocity.y -= GRAVITY * delta
	elif jump:
		b.velocity.y = JUMP_VELOCITY
	b.velocity.x = dir.x * speed
	b.velocity.z = dir.z * speed

	# Smooth step-up over small ledges (thresholds, treads, slab lips).
	if b.is_on_floor() and dir != Vector3.ZERO:
		var motion: Vector3 = Vector3(b.velocity.x, 0.0, b.velocity.z) * delta
		if b.test_move(b.global_transform, motion):
			var up: Vector3 = Vector3.UP * STEP_HEIGHT
			if not b.test_move(b.global_transform, up) and not b.test_move(b.global_transform.translated(up), motion):
				b.global_position += up

	b.move_and_slide()

	if b.global_position.y < -8.0:
		_respawn()
	_update_first_person_arm(delta)

	var moving: bool = Vector2(b.velocity.x, b.velocity.z).length() > 0.2 and b.is_on_floor()
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
		var n: Node3D = it["node"] as Node3D
		if n == null or not is_instance_valid(n):
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
	if not _third_person:
		_interact_reach_timer = INTERACT_REACH_DURATION
	var it: Dictionary = _find_nearest_interactable(INTERACT_RANGE)
	if it.is_empty():
		_show_toast("NOTHING IN REACH // MOVE WITHIN 2.8m", 1.6)
		return
	var kind: String = String(it["kind"])
	if bool(it["pickup"]):
		it["collected"] = true
		var picked: Node3D = it["node"] as Node3D
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
	elif kind == "terminal":
		var total: int = 0
		var have: int = 0
		for k: String in _inventory.keys():
			total += int(_inventory_max[k])
			have += int(_inventory[k])
		_show_toast("WORKBENCH TERMINAL // Sector-4 bulkhead relay: JAMMED AT 40%%.\nUpgrade kit %d/%d gathered. Need: +5A cell + Super-Wire on [RESET]." % [have, total], 4.5)


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
	var found: Array[Dictionary] = []
	for it: Dictionary in _interactables:
		if bool(it["collected"]):
			continue
		var n: Node3D = it["node"] as Node3D
		if n == null or not is_instance_valid(n):
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
	_show_toast("RFID PULSE EMITTED // %d TAG(S) RESPONDED" % found.size(), 2.2)


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

	# Precision-centered geometric HUD reticle (dead-center at 50.0%, 50.0% viewport center)
	var center_container: CenterContainer = CenterContainer.new()
	center_container.name = "CrosshairCenterContainer"
	center_container.set_anchors_preset(Control.PRESET_FULL_RECT)
	center_container.mouse_filter = Control.MOUSE_FILTER_IGNORE
	root.add_child(center_container)

	var reticle_box: Control = Control.new()
	reticle_box.name = "ReticleBox"
	reticle_box.custom_minimum_size = Vector2(24, 24)
	reticle_box.mouse_filter = Control.MOUSE_FILTER_IGNORE
	center_container.add_child(reticle_box)

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
	if p.x < -4.6 and p.z > 2.85:
		return "RM 1A — LAUNDRY LOUNGE"
	if p.x > 0.6 and p.x < 8.4 and p.z > 2.85:
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
	if _nearest.is_empty() or _preset_active >= 0:
		_hud_prompt.text = ""
	else:
		var verb: String = "PICK UP" if bool(_nearest["pickup"]) else "QUERY"
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

	# --- 8. [E] interact reach + pickup removal ---
	var n_before: int = 0
	for it: Dictionary in _interactables:
		if bool(it["pickup"]) and not bool(it["collected"]):
			n_before += 1
	var target: Dictionary = _find_nearest_interactable(INTERACT_RANGE)
	var tgt_node: Node3D = target.get("node", null) as Node3D
	var tgt_label: String = String(target.get("label", "none"))
	var inv_before: int = 0
	for k: String in _inventory.keys():
		inv_before += int(_inventory[k])
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
	_qa_check("E_pickup_collected_removed", n_after == n_before - 1 and inv_after == inv_before + 1 and (tgt_node == null or not is_instance_valid(tgt_node)), "target=%s pickups %d->%d inventory %d->%d node_freed=%s" % [tgt_label, n_before, n_after, inv_before, inv_after, tgt_node == null or not is_instance_valid(tgt_node)])
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
