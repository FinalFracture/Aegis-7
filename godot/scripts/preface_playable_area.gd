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

# RFID pulse
var _pulse_ring: MeshInstance3D
var _pulse_t: float = -1.0

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
	if OS.get_environment("RENDER_ALL") == "1" or OS.get_environment("CAPTURE_SCREENSHOTS") == "1":
		_batch_render = true
	if OS.get_environment("VALIDATE_ONLY") == "1":
		_validate_only = true
	if _capture_hud:
		_batch_render = false
	if DisplayServer.get_name() == "headless" and not _batch_render:
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
		_show_toast("WELCOME HOME, ROSTOV. APT 201 // HAB-7 RESIDENTIAL ATRIUM", 5.0)
	if _validate_only:
		print("[PrefacePlayableArea] Validate OK | interactables=", _interactables.size(), " | player=", _player_body != null)


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
			if nm.contains("door_slide") or nm.contains("door_apt") or nm.contains("door_leaf") or nm.contains("maint_grate"):
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


func _add_safety_floor_colliders(parent: Node3D) -> void:
	var body: StaticBody3D = StaticBody3D.new()
	body.name = "SectorSafetyFloorColliders"
	parent.add_child(body)
	var boxes: Array[Dictionary] = [
		{"name": "GroundFloorDeck", "size": Vector3(32.0, 0.4, 24.0), "pos": Vector3(0.0, -0.2, 0.0), "rot_x": 0.0},
		{"name": "UpperL2NorthDeck", "size": Vector3(28.0, 0.24, 8.0), "pos": Vector3(0.0, 4.08, 5.0), "rot_x": 0.0},
		{"name": "UpperL2WestWing", "size": Vector3(6.0, 0.24, 10.5), "pos": Vector3(-11.0, 4.08, -3.8), "rot_x": 0.0},
		{"name": "UpperL2EastStairLanding", "size": Vector3(6.3, 0.24, 3.4), "pos": Vector3(10.65, 4.08, -0.5), "rot_x": 0.0}
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
	if not _batch_render:
		_add_safety_floor_colliders(_arch_container)

	for v_cfg: Dictionary in [
		{"name": "EastAtriumValleyVista", "pos": Vector3(16.4, 4.5, 0.0), "rot_y": -90.0, "sz": Vector2(24.0, 12.0)},
		{"name": "SouthOpenPromenadeThresholdVista", "pos": Vector3(0.0, 3.8, -13.2), "rot_y": 0.0, "sz": Vector2(24.0, 11.0)}
	]:
		var bdrop: MeshInstance3D = MeshInstance3D.new()
		bdrop.name = String(v_cfg["name"])
		var qmesh: QuadMesh = QuadMesh.new()
		qmesh.size = v_cfg["sz"] as Vector2
		bdrop.mesh = qmesh
		bdrop.position = v_cfg["pos"] as Vector3
		bdrop.rotation_degrees = Vector3(0.0, float(v_cfg["rot_y"]), 0.0)
		var vmat: StandardMaterial3D = StandardMaterial3D.new()
		var vtex: Texture2D = _load_tex("vista_oneill_cylinder_interior.png")
		if vtex != null:
			vmat.albedo_texture = vtex
			vmat.albedo_color = Color(0.72, 0.75, 0.78, 1.0)
			vmat.emission_enabled = true
			vmat.emission_texture = vtex
			vmat.emission_energy_multiplier = 0.45
		vmat.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
		vmat.cull_mode = BaseMaterial3D.CULL_DISABLED
		bdrop.material_override = vmat
		bdrop.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
		_arch_container.add_child(bdrop)


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

	# Apt 201 engineering workbench (benchtop Y = 5.12m): staged on left half so CUE-001 scorch mark & 03:14 UTC note on right (-8.6..-9.5) are unobstructed!
	_spawn_pickup(wire_path, "Workbench_SuperWire_Spool", "wire", "SUPER-WIRE SPOOL", Vector3(-8.28, 5.12, 7.55), 1.05)
	_spawn_pickup(bci_path, "Workbench_BCI_Headband", "bci", "BCI HEADBAND", Vector3(-7.95, 5.12, 7.58), 1.10)
	_spawn_pickup(jelly_path, "Workbench_Thermal_Jelly", "jelly", "THERMAL JELLY CANISTER", Vector3(-7.64, 5.12, 7.58), 1.05)
	_spawn_pickup(batt_path, "Workbench_Battery_Cell", "batt", "+5A BATTERY CELL", Vector3(-7.35, 5.12, 7.55), 1.05)
	# Alcove 2C engineering supply shelf, Apt 202 desk, Room 1A folding counter, Room 1B substation service bench.
	_spawn_pickup(wire_path, "Alcove2C_SuperWire_Expansion", "wire", "SUPER-WIRE SPOOL", Vector3(-11.85, 5.02, -4.95), 1.15)
	_spawn_pickup(batt_path, "Alcove2C_Battery_Expansion", "batt", "+5A BATTERY CELL", Vector3(-11.05, 5.02, -4.95), 1.15)
	_spawn_pickup(batt_path, "Apt202_Desk_Battery_Cell", "batt", "+5A BATTERY CELL", Vector3(10.70, 5.10, 7.20), 1.10)
	_spawn_pickup(wire_path, "Room1A_Laundry_SuperWire_Spool", "wire", "SUPER-WIRE SPOOL", Vector3(-6.15, 0.98, 7.25), 1.15)
	_spawn_pickup(batt_path, "Room1B_Substation_Battery_Cell", "batt", "+5A BATTERY CELL", Vector3(7.20, 0.98, 7.10), 1.15)

	# Workbench diagnostic terminal (query-only — CUE-001 03:14 UTC Bus B-14 oscilloscope log)
	var term: Node3D = Node3D.new()
	term.name = "Workbench_DiagnosticTerminal"
	term.position = Vector3(-9.17, 5.50, 8.05)
	_props_container.add_child(term)
	_interactables.append({"node": term, "kind": "terminal", "label": "APT 201 WORKBENCH OSCILLOSCOPE", "collected": false, "pickup": false})

	# Room 1B Sub-Bus B-14 Telemetry Relay Rack (query-only — CUE-003 broken seal 2026-10-19 // 03:14)
	var sub_rack: Node3D = Node3D.new()
	sub_rack.name = "Substation_TelemetryRack_B14"
	sub_rack.position = Vector3(4.70, 1.15, 7.85)
	_props_container.add_child(sub_rack)
	_interactables.append({"node": sub_rack, "kind": "substation_rack", "label": "RM 1B SUB-BUS B-14 RELAY RACK", "collected": false, "pickup": false})

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
			_fp_wrist_holder.add_child(_fp_wrist_model)
			_fp_wrist_model.position = Vector3(0.0, -0.18, 0.0)
			_fp_wrist_holder.position = Vector3(-0.14, -0.12, -0.44)
			_fp_wrist_holder.rotation_degrees = Vector3(24.0, -24.0, -10.0)


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
		"Sector-4 relay nominal. Note: Unlogged 48.2 kW / 412 Hz draw on Bus B-14 at 03:14 UTC traced to RM 1B.", Vector3(-1.45, 0.06, -6.45), 35.0, ["DiagnosticPoint", "Idle"], 0.70)
	_spawn_bot(BOT_SWEEP_PATHS, "Hammerhead05_Sweep_0812_CivicSanitation", "SWEEP #0812", "D-02 // CIVIC & SANITATION",
		"Mezzanine patrol 72% complete. Logged single-tread rubber skid & cryo-coolant trace from East Stairwell into RM 1B.", Vector3(-2.40, 4.29, 2.60), -65.0, ["WalkCycle", "Idle"], 0.35)
	_spawn_bot(BOT_KELVIN_PATHS, "Hammerhead05_Kelvin_0204_Science", "KELVIN #0204 [PUDDLE]", "D-03 // SCIENCE",
		"Left tread actuator drag (-18% since 2026-10-19 03:14 UTC). Sub-Bus B-14 Hatch 04 sealed. [WARN: ID PUDDLE_0204 OVERWRITTEN].", Vector3(5.60, 0.06, 6.00), 45.0, ["DiagnosticProbe", "DiagnosticPoint", "Idle"], 0.65)
	_spawn_bot(BOT_CLOVER_PATHS, "Hammerhead05_Clover_0631_AgriBiosphere", "CLOVER #0631", "D-04 // AGRI-BIOSPHERE",
		"Atrium planter soil moisture 41%. Condenser line pressure steady after 03:14 UTC Bus B-14 brownout.", Vector3(2.20, 0.06, -1.80), 90.0, ["Idle", "DiagnosticPoint"], 0.50)

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
func _setup_sector_lighting() -> void:
	for ch: Node in _lights_container.get_children():
		ch.free()
	_task_lights.clear()
	_task_base.clear()

	_sun = DirectionalLight3D.new()
	_sun.name = "AtriumGoldenHourSunlight"
	_sun.rotation_degrees = Vector3(-38.0, 52.0, 0.0)
	_sun.light_color = Color("#FFF3DC")
	_sun.light_energy = 0.78
	_sun.shadow_enabled = true
	_sun.shadow_blur = 1.4
	_sun.shadow_bias = 0.02
	_lights_container.add_child(_sun)

	_fill = DirectionalLight3D.new()
	_fill.name = "AtriumSkyBounceFill"
	_fill.rotation_degrees = Vector3(-28.0, -135.0, 0.0)
	_fill.light_color = Color("#C8DCF0")
	_fill.light_energy = 0.34
	_fill.shadow_enabled = false
	_lights_container.add_child(_fill)

	# Balanced mid-key localized task lights + subtle mid-atrium overhead fill light ([t4u]).
	for l_cfg: Dictionary in [
		{"name": "Apt201_Workbench_TaskLight", "pos": Vector3(-8.45, 6.15, 7.45), "col": Color("#F5DFBC"), "e": 0.92, "r": 9.5},
		{"name": "Apt202_Desk_TaskLight", "pos": Vector3(10.50, 6.15, 6.80), "col": Color("#F5DFBC"), "e": 0.82, "r": 9.0},
		{"name": "Stairwell_Landing_SafetyLight", "pos": Vector3(10.40, 6.40, -1.60), "col": Color("#EDE0C8"), "e": 0.85, "r": 10.5},
		{"name": "Room1A_Lounge_Light", "pos": Vector3(-8.20, 3.10, 6.40), "col": Color("#F5DFBC"), "e": 0.80, "r": 9.5},
		{"name": "Room1B_Substation_ServiceBayLight", "pos": Vector3(5.60, 3.10, 6.60), "col": Color("#EAE6DC"), "e": 0.95, "r": 11.0},
		{"name": "Atrium_Midhead_BounceFill", "pos": Vector3(0.0, 6.80, -1.50), "col": Color("#E8EDF2"), "e": 0.72, "r": 15.0}
	]:
		var omni: OmniLight3D = OmniLight3D.new()
		omni.name = String(l_cfg["name"])
		omni.position = l_cfg["pos"] as Vector3
		omni.light_color = l_cfg["col"] as Color
		omni.light_energy = float(l_cfg["e"])
		omni.omni_range = float(l_cfg["r"])
		omni.omni_attenuation = 1.35
		_lights_container.add_child(omni)
		_task_lights.append(omni)
		_task_base.append({"col": l_cfg["col"], "e": l_cfg["e"]})


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
				mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_ON
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
							mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
						elif mname.contains("amber") or mname.contains("hazard"):
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
	_camera.far = 500.0
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
		_camera.current = true

	if _rostov_root != null:
		_rostov_root.get_parent().remove_child(_rostov_root)
		_player_body.add_child(_rostov_root)
		_rostov_root.position = Vector3(0.0, 0.12, 0.0)
		_rostov_root.rotation_degrees = Vector3(0.0, 180.0, 0.0)
		_rostov_anim = ""
		_set_rostov_anim("Idle")

	if _fp_wrist_model != null:
		_play_actor_anim(_fp_wrist_model, ["Idle", "WristRaiseInspect"], 0.0)
	_apply_view_mode()


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
	_pitch = clampf(_pitch, deg_to_rad(-60.0) if _third_person else deg_to_rad(-85.0), deg_to_rad(45.0) if _third_person else deg_to_rad(85.0))
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
	if event is InputEventMouseMotion and Input.mouse_mode == Input.MOUSE_MODE_CAPTURED and _preset_active < 0:
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
			KEY_R:
				_trigger_rfid_pulse()
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
	var lo: float = deg_to_rad(-60.0) if _third_person else deg_to_rad(-85.0)
	var hi: float = deg_to_rad(45.0) if _third_person else deg_to_rad(85.0)
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
	var it: Dictionary = _find_nearest_interactable(INTERACT_RANGE)
	if it.is_empty():
		_show_toast("NOTHING IN REACH // MOVE WITHIN 2.8m", 1.6)
		return
	var kind: String = String(it["kind"])
	if bool(it["pickup"]):
		it["collected"] = true
		(it["node"] as Node3D).visible = false
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
		_show_toast("OSCILLOSCOPE [2026-10-19 03:14 UTC] // 13.56MHz / 412Hz spike on BUS B-14 (48.2 kW).\nUnit #0204 re-keyed [PUDDLE -> KELVIN]; Coil C3 blown during A7-0204-MEM dump. Kit: %d/%d." % [have, total], 5.0)
	elif kind == "substation_rack":
		_show_toast("RM 1B RELAY RACK [SEAL BROKEN 2026-10-19 03:14 UTC] // Ghost Stencil: SEC-04 TELEMETRY RELAY.\nBus B-14 log purged; Unit #0204 flashed from D-04/HYDRO [PUDDLE] to D-03 SCIENCE [KELVIN].", 5.0)


func _trigger_rfid_pulse() -> void:
	if _player_body == null:
		return
	if _fp_wrist_model != null:
		_play_actor_anim(_fp_wrist_model, ["RFIDPulse", "Idle"], 0.0)
	if _pulse_ring != null and is_instance_valid(_pulse_ring):
		_pulse_ring.queue_free()
	_pulse_ring = MeshInstance3D.new()
	_pulse_ring.name = "Wrist04_RFIDPulseRing"
	var torus: TorusMesh = TorusMesh.new()
	torus.inner_radius = 0.92
	torus.outer_radius = 1.0
	torus.rings = 48
	torus.ring_segments = 8
	_pulse_ring.mesh = torus
	var mat: StandardMaterial3D = StandardMaterial3D.new()
	mat.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	mat.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
	mat.albedo_color = Color(COLOR_CYAN.r, COLOR_CYAN.g, COLOR_CYAN.b, 0.85)
	mat.emission_enabled = true
	mat.emission = COLOR_CYAN
	mat.emission_energy_multiplier = 1.2
	mat.cull_mode = BaseMaterial3D.CULL_DISABLED
	_pulse_ring.material_override = mat
	_pulse_ring.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	add_child(_pulse_ring)
	_pulse_ring.global_position = _player_body.global_position + Vector3(0.0, 1.05, 0.0)
	_pulse_ring.scale = Vector3(0.3, 0.3, 0.3)
	_pulse_t = 0.0

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

	# Top-left status panel
	var tl: Panel = _make_panel(root, Vector2(24, 22), Vector2(560, 160), COLOR_CYAN)
	_make_label(tl, Vector2(16, 10), "AEGIS-7 // HAB-7 RESIDENTIAL ATRIUM", 20, Color("#9FD3E0"))
	_hud_zone = _make_label(tl, Vector2(16, 44), "ZONE: --", 15, white)
	_hud_view = _make_label(tl, Vector2(16, 68), "VIEW: --", 15, white)
	_hud_light = _make_label(tl, Vector2(16, 92), "LIGHTING: --", 15, white)
	_hud_inv = _make_label(tl, Vector2(16, 120), "BCI: 0/1 | JELLY: 0/1 | WIRE: 0/3 | BATT: 0/4", 15, Color("#E2C79A"))

	# Center crosshair
	var center: Control = Control.new()
	center.set_anchors_preset(Control.PRESET_CENTER)
	center.mouse_filter = Control.MOUSE_FILTER_IGNORE
	root.add_child(center)
	for r: Rect2 in [Rect2(-11, -1, 8, 2), Rect2(3, -1, 8, 2), Rect2(-1, -11, 2, 8), Rect2(-1, 3, 2, 8)]:
		var cr: ColorRect = ColorRect.new()
		cr.position = r.position
		cr.size = r.size
		cr.color = Color(0.85, 0.92, 0.95, 0.85)
		cr.mouse_filter = Control.MOUSE_FILTER_IGNORE
		center.add_child(cr)
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

	# Bottom-left controls bar
	var bl_anchor: Control = Control.new()
	bl_anchor.set_anchors_preset(Control.PRESET_BOTTOM_LEFT)
	bl_anchor.mouse_filter = Control.MOUSE_FILTER_IGNORE
	root.add_child(bl_anchor)
	var bl: Panel = _make_panel(bl_anchor, Vector2(24, -58), Vector2(1240, 36), COLOR_AMBER)
	_make_label(bl, Vector2(14, 7), "[WASD] Move  [Shift] Sprint  [Space] Jump  [Mouse] Look  [V/Tab] 1st/3rd Person  [E] Interact/Pickup  [R] Wrist RFID Pulse  [N] Emergency Lights  [1-4] Cams  [0] Player", 14, dim.lerp(white, 0.5))


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
	if _pulse_t >= 0.0 and _pulse_ring != null and is_instance_valid(_pulse_ring):
		_pulse_t += delta
		var s: float = 0.3 + _pulse_t * 9.0
		_pulse_ring.scale = Vector3(s, 1.0, s)
		var m: StandardMaterial3D = _pulse_ring.material_override as StandardMaterial3D
		m.albedo_color.a = clampf(0.85 * (1.0 - _pulse_t / 1.3), 0.0, 0.85)
		if _player_body != null:
			_pulse_ring.global_position = _player_body.global_position + Vector3(0.0, 1.05, 0.0)
		if _pulse_t > 1.3:
			_pulse_ring.queue_free()
			_pulse_ring = null
			_pulse_t = -1.0
	if _emergency:
		var e: float = 0.30 + 0.22 * (0.5 + 0.5 * sin(_time * 3.2))
		for l: OmniLight3D in _task_lights:
			l.light_energy = e
	_update_hud()
	if _capture_hud:
		_process_capture_f5_hud()


func _save_qa_png(fname: String) -> void:
	var img: Image = get_viewport().get_texture().get_image()
	if img == null or img.is_empty():
		push_warning("[PrefacePlayableArea] Empty viewport image for " + fname)
		return
	var dir_abs: String = _resolve_path(QA_DIR)
	DirAccess.make_dir_recursive_absolute(dir_abs)
	var out: String = dir_abs + "/" + fname
	if img.save_png(out) == OK:
		print("[PrefacePlayableArea] Saved F5 HUD capture ", out)


func _process_capture_f5_hud() -> void:
	match _frame_counter:
		20:
			# 1st-person: turn toward the Apt 201 workbench so the pickups + [E] prompt + #04 sleeve are in frame.
			_third_person = false
			_player_body.rotation_degrees = Vector3(0.0, -146.0, 0.0)
			_pitch = deg_to_rad(-16.0)
			_apply_view_mode()
		50:
			_save_qa_png("qa_f5_hud_1st_person.png")
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
		72:
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
