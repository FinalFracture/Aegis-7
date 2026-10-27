class_name PrefaceServiceCallTest
extends Node3D
## Godot 4.3 Interactive Preface Service-Call Test Environment & 3-Cycle Door Troubleshooting Controller
## Implements Vance's `preface_test_environment_and_wrist_spec.md` & Sloane's `sloane_preface_and_wrist_textures_spec.md`:
## - `preface_service_call_room.glb` (`10.0m W x 8.0m D x 4.2m H` Sector-4 Commuter Transit Vestibule)
## - `prop_service_door.glb` (`2.40m W x 2.60m H x 0.38m D` Articulated Dual-Leaf Door with 3-Stage Diagnostic Header)
## - `char_assistant_droid.glb` (`Unit A7-D2`, `1.15m H` with `#D95B26` RFID handshake collar & diagnostic probe arm)
## - `char_citizen_commuter.glb` (`2` Waiting Civilian Commuters demonstrating the wordless wrist-raise gesture)
## - `#02` Lead Technician Kaelen Rostov (`char_crew_r1_02.glb`) + Center-Screen Raised Subdermal Wrist RFID Rig (`prop_wrist_rfid_r1_02.glb`)

const ROOM_GLB_PATHS := [
	"res://assets/models/environments/preface_service_call_room.glb",
	"res://../assets/glb/environments/preface_service_call_room.glb",
	"res://../assets/glb/rooms/preface_service_call_room.glb",
	"res://../assets/glb/preface/preface_service_call_room.glb"
]
const DOOR_GLB_PATHS := [
	"res://assets/models/props/service_door/prop_service_door.glb",
	"res://../assets/glb/props/service_door/prop_service_door.glb",
	"res://../assets/glb/preface/prop_service_door.glb"
]
const DROID_GLB_PATHS := [
	"res://assets/models/characters/char_assistant_droid.glb",
	"res://../assets/glb/characters/char_assistant_droid.glb",
	"res://../assets/glb/character/char_assistant_droid.glb",
	"res://../assets/glb/preface/char_assistant_droid.glb"
]
const COMMUTER_GLB_PATHS := [
	"res://assets/models/characters/char_citizen_commuter.glb",
	"res://../assets/glb/characters/char_citizen_commuter.glb",
	"res://../assets/glb/character/char_citizen_commuter.glb",
	"res://../assets/glb/preface/char_citizen_commuter.glb"
]
const ROSTOV_GLB_PATHS := [
	"res://assets/models/winners/char_crew_winner_01_aegis7_commander.glb",
	"res://../assets/glb/character/char_crew_r1_02.glb"
]
const WRIST_HERO_PATHS := [
	"res://assets/models/winners/prop_wrist_rfid_winner_01_induction_loom.glb",
	"res://assets/models/props/wrist_rfid/prop_wrist_rfid_winner_02.glb",
	"res://assets/models/props/wrist_rfid/prop_wrist_rfid_r1_02.glb",
	"res://../assets/glb/props/wrist_rfid/prop_wrist_rfid_r1_02.glb",
	"res://../assets/glb/wrist_rfid/prop_wrist_rfid_r1_02.glb"
]

const TEX_DIRS := [
	"res://assets/textures/preface",
	"res://assets/textures/wrist_rfid",
	"res://assets/textures",
	"res://assets/textures/character",
	"res://assets/textures/cylinder_interior",
	"res://assets/textures/buildings"
]

const OUT_DIRS := [
	"res://renders/preface",
	"res://../assets/renders/preface",
	"res://renders/wrist_rfid",
	"res://../assets/renders/wrist_rfid"
]

const CAMERAS := [
	{
		"name": "cam_01_initial_commuter_wrist_demo",
		"cycle": 0,
		"pos": Vector3(-2.35, 1.82, 3.05),
		"target": Vector3(0.45, 1.28, -3.55),
		"fov": 55.0,
		"fp_wrist": false,
		"wrist_target": Vector3(1.55, 1.18, -3.65)
	},
	{
		"name": "cam_02_cycle1_center_screen_wrist_scan_40pct_jam",
		"cycle": 1,
		"pos": Vector3(0.82, 1.54, -1.62),
		"target": Vector3(0.48, 1.48, -3.75),
		"fov": 52.0,
		"fp_wrist": true,
		"wrist_target": Vector3(1.48, 1.18, -3.68)
	},
	{
		"name": "cam_03_cycle2_droid_relay_counterweight_sync",
		"cycle": 2,
		"pos": Vector3(-0.35, 1.48, -1.52),
		"target": Vector3(-1.35, 1.12, -3.55),
		"fov": 52.0,
		"fp_wrist": true,
		"wrist_target": Vector3(-1.42, 0.92, -3.45)
	},
	{
		"name": "cam_04_cycle3_final_unlock_commuters_exit",
		"cycle": 3,
		"pos": Vector3(2.25, 1.76, 2.75),
		"target": Vector3(-0.20, 1.26, -3.85),
		"fov": 54.0,
		"fp_wrist": false,
		"wrist_target": Vector3(1.55, 1.18, -3.65)
	}
]

var _room_container: Node3D
var _door_container: Node3D
var _actors_container: Node3D
var _effects_container: Node3D
var _lights_container: Node3D
var _camera: Camera3D

var _door_root: Node3D
var _droid_root: Node3D
var _commuter_a: Node3D
var _commuter_b: Node3D
var _rostov_root: Node3D
var _fp_wrist_holder: Node3D
var _fp_wrist_model: Node3D

var _pedestal_light: OmniLight3D
var _counterweight_light: OmniLight3D
var _relay_light: OmniLight3D
var _wrist_spot: SpotLight3D

var _header_indicators: Array[MeshInstance3D] = []
var _threshold_strip: MeshInstance3D
var _rfid_beam_mesh: MeshInstance3D
var _rfid_pulse_rings: Array[MeshInstance3D] = []

var _tex_cache: Dictionary = {}
var _batch_render: bool = false
var _validate_only: bool = false
var _current_cycle: int = 0
var _frame_counter: int = 0
var _render_step: int = 0
var _render_wait: int = 0


func _ready() -> void:
	_camera = get_node_or_null("SceneCamera") as Camera3D
	_room_container = get_node_or_null("RoomContainer") as Node3D
	_door_container = get_node_or_null("DoorContainer") as Node3D
	_actors_container = get_node_or_null("ActorsContainer") as Node3D
	_effects_container = get_node_or_null("EffectsContainer") as Node3D
	_lights_container = get_node_or_null("LightingRig") as Node3D

	if _room_container == null:
		_room_container = Node3D.new()
		_room_container.name = "RoomContainer"
		add_child(_room_container)
	if _door_container == null:
		_door_container = Node3D.new()
		_door_container.name = "DoorContainer"
		add_child(_door_container)
	if _actors_container == null:
		_actors_container = Node3D.new()
		_actors_container.name = "ActorsContainer"
		add_child(_actors_container)
	if _effects_container == null:
		_effects_container = Node3D.new()
		_effects_container.name = "EffectsContainer"
		add_child(_effects_container)
	if _lights_container == null:
		_lights_container = Node3D.new()
		_lights_container.name = "LightingRig"
		add_child(_lights_container)

	var all_args: PackedStringArray = OS.get_cmdline_args() + OS.get_cmdline_user_args()
	for arg: String in all_args:
		if arg == "--render-all" or arg == "--capture-screenshots" or arg == "--screenshots":
			_batch_render = true
		elif arg == "--validate-only" or arg == "--validate":
			_validate_only = true

	if OS.get_environment("RENDER_ALL") == "1" or OS.get_environment("CAPTURE_SCREENSHOTS") == "1":
		_batch_render = true
	if OS.get_environment("VALIDATE_ONLY") == "1":
		_validate_only = true

	if DisplayServer.get_name() == "headless" and not _batch_render:
		_validate_only = true

	_assemble_preface_environment()
	_setup_vestibule_lighting()
	_build_diegetic_rfid_effects()
	apply_camera_and_cycle_state(0)


func _unhandled_input(event: InputEvent) -> void:
	# Wordless Button-Mash Discovery: any action key or mouse click raises wrist & advances the 3-cycle door loop!
	if event is InputEventKey and (event as InputEventKey).pressed and not (event as InputEventKey).echo:
		_current_cycle = (_current_cycle + 1) % CAMERAS.size()
		apply_camera_and_cycle_state(_current_cycle)
	elif event is InputEventMouseButton and (event as InputEventMouseButton).pressed:
		_current_cycle = (_current_cycle + 1) % CAMERAS.size()
		apply_camera_and_cycle_state(_current_cycle)


func _resolve_path(p: String) -> String:
	if p.begins_with("res://"):
		return ProjectSettings.globalize_path(p).simplify_path()
	return p


func _load_tex(fname: String) -> Texture2D:
	if _tex_cache.has(fname):
		return _tex_cache[fname] as Texture2D
	for d: String in TEX_DIRS:
		var res_p: String = d + "/" + fname
		var abs_p: String = _resolve_path(res_p)
		if FileAccess.file_exists(abs_p):
			var img: Image = Image.new()
			if img.load(abs_p) == OK and not img.is_empty():
				img.generate_mipmaps()
				var tex: ImageTexture = ImageTexture.create_from_image(img)
				_tex_cache[fname] = tex
				return tex
	return null


func _find_first_existing(paths: Array) -> String:
	for p in paths:
		var abs_p: String = _resolve_path(String(p))
		if FileAccess.file_exists(abs_p):
			return abs_p
	return ""


func _load_glb_scene(path: String, is_wrist: bool = false) -> Node3D:
	var abs_p: String = _resolve_path(path)
	if abs_p == "" or not FileAccess.file_exists(abs_p):
		return null
	var doc: GLTFDocument = GLTFDocument.new()
	var state: GLTFState = GLTFState.new()
	if doc.append_from_file(abs_p, state) == OK:
		var root: Node = doc.generate_scene(state)
		if root is Node3D:
			var n3d: Node3D = root as Node3D
			_upgrade_preface_materials(n3d, is_wrist)
			return n3d
	return null


func _get_local_aabb_center(root: Node3D) -> Vector3:
	var min_v := Vector3(99999.0, 99999.0, 99999.0)
	var max_v := Vector3(-99999.0, -99999.0, -99999.0)
	var found: bool = false
	var stack: Array[Node] = [root]
	while not stack.is_empty():
		var curr: Node = stack.pop_back()
		if curr is MeshInstance3D:
			var mi: MeshInstance3D = curr as MeshInstance3D
			if mi.mesh != null:
				var aabb: AABB = mi.mesh.get_aabb()
				var xf: Transform3D = root.global_transform.affine_inverse() * mi.global_transform
				for i: int in range(8):
					var pt: Vector3 = xf * aabb.get_endpoint(i)
					min_v = min_v.min(pt)
					max_v = max_v.max(pt)
					found = true
		for ch: Node in curr.get_children():
			stack.append(ch)
	if not found:
		return Vector3.ZERO
	return (min_v + max_v) * 0.5


func _assemble_preface_environment() -> void:
	for c: Node3D in [_room_container, _door_container, _actors_container]:
		for ch: Node in c.get_children():
			ch.free()

	# 1. Load Sector-4 Commuter Transit Vestibule (`preface_service_call_room.glb`)
	var room_path: String = _find_first_existing(ROOM_GLB_PATHS)
	var room_node: Node3D = _load_glb_scene(room_path, false)
	if room_node != null:
		room_node.name = "PrefaceServiceCallRoom"
		_room_container.add_child(room_node)

	# Panoramic O'Neill Cylinder Promenade Backdrop outside the East Window (`X = +7.5m`) and North Doorway (`Z = -9.5m`)
	for b_cfg: Dictionary in [
		{"name": "EastPromenadeVista", "pos": Vector3(7.6, 2.2, 0.0), "rot_y": -90.0, "sz": Vector2(16.0, 9.0)},
		{"name": "NorthCorridorPromenadeVista", "pos": Vector3(0.0, 2.2, -9.2), "rot_y": 0.0, "sz": Vector2(18.0, 9.5)}
	]:
		var bdrop: MeshInstance3D = MeshInstance3D.new()
		bdrop.name = String(b_cfg["name"])
		var qmesh: QuadMesh = QuadMesh.new()
		qmesh.size = b_cfg["sz"] as Vector2
		bdrop.mesh = qmesh
		bdrop.position = b_cfg["pos"] as Vector3
		bdrop.rotation_degrees = Vector3(0.0, float(b_cfg["rot_y"]), 0.0)
		var vmat: StandardMaterial3D = StandardMaterial3D.new()
		var vtex: Texture2D = _load_tex("vista_oneill_cylinder_interior.png")
		if vtex != null:
			vmat.albedo_texture = vtex
			vmat.albedo_color = Color(0.88, 0.86, 0.80, 1.0)
			vmat.emission_enabled = true
			vmat.emission_texture = vtex
			vmat.emission_energy_multiplier = 0.72
		vmat.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
		vmat.cull_mode = BaseMaterial3D.CULL_DISABLED
		bdrop.material_override = vmat
		bdrop.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
		_room_container.add_child(bdrop)

	# 2. Load Dual-Leaf Malfunctioning Commuter Bulkhead Door (`prop_service_door.glb`)
	var door_path: String = _find_first_existing(DOOR_GLB_PATHS)
	_door_root = _load_glb_scene(door_path, false)
	if _door_root != null:
		_door_root.name = "PropServiceDoor"
		_door_container.add_child(_door_root)
		var dc: Vector3 = _get_local_aabb_center(_door_root)
		if absf(dc.z) < 1.5:
			_door_root.position = Vector3(0.0, 0.0, -3.82)

	# 3. Load Aegis-7 Maintenance Assistant Droid (`char_assistant_droid.glb`, `Unit A7-D2`)
	var droid_path: String = _find_first_existing(DROID_GLB_PATHS)
	_droid_root = _load_glb_scene(droid_path, false)
	if _droid_root != null:
		_droid_root.name = "CharAssistantDroid_A7D2"
		_actors_container.add_child(_droid_root)

	# 4. Load 2 Waiting Hab-7 Civilian Commuters (`char_citizen_commuter.glb`)
	var comm_path: String = _find_first_existing(COMMUTER_GLB_PATHS)
	_commuter_a = _load_glb_scene(comm_path, false)
	if _commuter_a != null:
		_commuter_a.name = "CommuterA_WristDemo"
		_actors_container.add_child(_commuter_a)
	_commuter_b = _load_glb_scene(comm_path, false)
	if _commuter_b != null:
		_commuter_b.name = "CommuterB_Waiting"
		_actors_container.add_child(_commuter_b)

	# 5. Load `#02` Lead Technician Kaelen Rostov (`char_crew_winner_01_aegis7_commander.glb`)
	var rostov_path: String = _find_first_existing(ROSTOV_GLB_PATHS)
	_rostov_root = _load_glb_scene(rostov_path, false)
	if _rostov_root != null:
		_rostov_root.name = "LeadTech_KaelenRostov_02"
		_actors_container.add_child(_rostov_root)

	# 6. Load Center-Screen Raised Subdermal Wrist RFID Rig (`prop_wrist_rfid_r1_02.glb`) parented to Camera
	if _camera != null:
		if _fp_wrist_holder != null and is_instance_valid(_fp_wrist_holder):
			_fp_wrist_holder.free()
		_fp_wrist_holder = Node3D.new()
		_fp_wrist_holder.name = "CenterScreenWristHolder"
		_camera.add_child(_fp_wrist_holder)

		var wrist_path: String = _find_first_existing(WRIST_HERO_PATHS)
		_fp_wrist_model = _load_glb_scene(wrist_path, true)
		if _fp_wrist_model != null:
			_fp_wrist_model.name = "CenterScreenWristRfid_02"
			_fp_wrist_holder.add_child(_fp_wrist_model)
			# Position raised left hand & 68/32 split-cuff in lower-center foreground of the camera view!
			var wc: Vector3 = _get_local_aabb_center(_fp_wrist_model)
			_fp_wrist_model.position = -wc * 0.85
			_fp_wrist_holder.position = Vector3(-0.08, -0.10, -0.44)
			_fp_wrist_holder.rotation_degrees = Vector3(24.0, -22.0, -10.0)


func _build_diegetic_rfid_effects() -> void:
	for ch: Node in _effects_container.get_children():
		ch.free()
	_header_indicators.clear()
	_rfid_pulse_rings.clear()

	# 1. Three Header Calibration Nodes (`Node_Calib_01..03`) above the doorway (`Y = 2.74m, Z = -3.60m`)
	for i: int in range(3):
		var hnode: MeshInstance3D = MeshInstance3D.new()
		hnode.name = "HeaderCalibIndicator_%02d" % (i + 1)
		var cmesh: CylinderMesh = CylinderMesh.new()
		cmesh.top_radius = 0.085
		cmesh.bottom_radius = 0.085
		cmesh.height = 0.04
		cmesh.radial_segments = 16
		hnode.mesh = cmesh
		hnode.position = Vector3(-0.52 + float(i) * 0.52, 2.74, -3.58)
		hnode.rotation_degrees = Vector3(90.0, 0.0, 0.0)
		var hmat: StandardMaterial3D = StandardMaterial3D.new()
		hmat.albedo_color = Color("#FF9500")
		hmat.emission_enabled = true
		hmat.emission = Color("#FF9500")
		hmat.emission_energy_multiplier = 2.2
		hnode.material_override = hmat
		_effects_container.add_child(hnode)
		_header_indicators.append(hnode)

	# 2. Doorway Floor Threshold Status Strip (`Y = 0.015m, Z = -3.62m`)
	_threshold_strip = MeshInstance3D.new()
	_threshold_strip.name = "DoorThresholdStatusStrip"
	var tbox: BoxMesh = BoxMesh.new()
	tbox.size = Vector3(2.35, 0.018, 0.14)
	_threshold_strip.mesh = tbox
	_threshold_strip.position = Vector3(0.0, 0.012, -3.62)
	var tmat: StandardMaterial3D = StandardMaterial3D.new()
	tmat.albedo_color = Color("#FF9500")
	tmat.emission_enabled = true
	tmat.emission = Color("#FF9500")
	tmat.emission_energy_multiplier = 2.2
	_threshold_strip.material_override = tmat
	_effects_container.add_child(_threshold_strip)

	# 3. Diegetic Inductive Coupling Wave Rings & Harmonic Arc between Raised Wrist and Target Pad/Droid
	_rfid_beam_mesh = MeshInstance3D.new()
	_rfid_beam_mesh.name = "InductiveCouplingArcBeam"
	var bmesh: CylinderMesh = CylinderMesh.new()
	bmesh.top_radius = 0.016
	bmesh.bottom_radius = 0.028
	bmesh.height = 1.0
	bmesh.radial_segments = 12
	_rfid_beam_mesh.mesh = bmesh
	var bmat: StandardMaterial3D = StandardMaterial3D.new()
	bmat.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
	bmat.albedo_color = Color(0.0, 0.92, 1.0, 0.58)
	bmat.emission_enabled = true
	bmat.emission = Color("#00E5FF")
	bmat.emission_energy_multiplier = 2.6
	bmat.cull_mode = BaseMaterial3D.CULL_DISABLED
	_rfid_beam_mesh.material_override = bmat
	_effects_container.add_child(_rfid_beam_mesh)

	for r_i: int in range(3):
		var pring: MeshInstance3D = MeshInstance3D.new()
		pring.name = "InductiveWaveRing_%d" % r_i
		var trm: TorusMesh = TorusMesh.new()
		var rad: float = 0.065 + float(r_i) * 0.045
		trm.inner_radius = rad - 0.008
		trm.outer_radius = rad + 0.008
		trm.rings = 20
		trm.ring_segments = 8
		pring.mesh = trm
		var rmat: StandardMaterial3D = StandardMaterial3D.new()
		rmat.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
		rmat.albedo_color = Color(0.0, 0.92, 1.0, 0.72)
		rmat.emission_enabled = true
		rmat.emission = Color("#00E5FF")
		rmat.emission_energy_multiplier = 2.5
		rmat.cull_mode = BaseMaterial3D.CULL_DISABLED
		pring.material_override = rmat
		_effects_container.add_child(pring)
		_rfid_pulse_rings.append(pring)


func _setup_vestibule_lighting() -> void:
	for ch: Node in _lights_container.get_children():
		ch.free()

	# 1. Sloane's East Viewport Promenade Sunlight (`DirectionalLight3D`, `#FFF5E4` 5500K, energy = 1.35)
	var east_sun: DirectionalLight3D = DirectionalLight3D.new()
	east_sun.name = "EastPromenadeSunlight_5500K"
	east_sun.rotation_degrees = Vector3(-34.0, 68.0, 0.0)
	east_sun.light_color = Color("#FFF5E4")
	east_sun.light_energy = 1.35
	east_sun.shadow_enabled = true
	east_sun.shadow_blur = 1.3
	east_sun.shadow_bias = 0.02
	_lights_container.add_child(east_sun)

	# 2. Sloane's Ceiling Coffer Linear Fill (`2 x OmniLight3D` at `Y = 3.85m`, `#E8F1F8` 4800K, energy = 0.85, range = 9.5m)
	for cx: float in [-2.2, 2.2]:
		var coffer_light: OmniLight3D = OmniLight3D.new()
		coffer_light.name = "CeilingCofferFill_%s" % ("W" if cx < 0.0 else "E")
		coffer_light.position = Vector3(cx, 3.85, -0.4)
		coffer_light.light_color = Color("#E8F1F8")
		coffer_light.light_energy = 0.85
		coffer_light.omni_range = 9.5
		_lights_container.add_child(coffer_light)

	# 3. Sloane's Door Pedestal & Header Status Light (`OmniLight3D` at `X = +1.55m, Y = 1.25m, Z = -3.65m`)
	_pedestal_light = OmniLight3D.new()
	_pedestal_light.name = "DoorPedestalStatusLight"
	_pedestal_light.position = Vector3(1.55, 1.25, -3.65)
	_pedestal_light.light_color = Color("#FF9500")
	_pedestal_light.light_energy = 1.15
	_pedestal_light.omni_range = 4.2
	_lights_container.add_child(_pedestal_light)

	# Counterweight Transom Diagnostic Light (`Y = 3.05m, Z = -3.65m`)
	_counterweight_light = OmniLight3D.new()
	_counterweight_light.name = "CounterweightTransomLight"
	_counterweight_light.position = Vector3(0.45, 3.05, -3.55)
	_counterweight_light.light_color = Color("#FF9500")
	_counterweight_light.light_energy = 1.10
	_counterweight_light.omni_range = 3.8
	_lights_container.add_child(_counterweight_light)

	# Relay_Panel_B Left Wall Junction Light (`X = -1.85m, Y = 1.15m, Z = -3.65m`)
	_relay_light = OmniLight3D.new()
	_relay_light.name = "RelayPanelBStatusLight"
	_relay_light.position = Vector3(-1.85, 1.15, -3.65)
	_relay_light.light_color = Color("#FF9500")
	_relay_light.light_energy = 0.95
	_relay_light.omni_range = 3.6
	_lights_container.add_child(_relay_light)

	# 4. Sloane's Center-Screen Raised Wrist Key Light (`SpotLight3D` parented to camera, `#D8F6FF`, energy = 1.10, spot_angle = 32°)
	if _camera != null:
		if _wrist_spot != null and is_instance_valid(_wrist_spot):
			_wrist_spot.free()
		_wrist_spot = SpotLight3D.new()
		_wrist_spot.name = "CenterScreenWristSpotLight"
		_wrist_spot.position = Vector3(0.18, 0.16, 0.05)
		_wrist_spot.rotation_degrees = Vector3(-16.0, 18.0, 0.0)
		_wrist_spot.light_color = Color("#D8F6FF")
		_wrist_spot.light_energy = 1.10
		_wrist_spot.spot_range = 2.2
		_wrist_spot.spot_angle = 32.0
		_camera.add_child(_wrist_spot)


func _set_door_state(cycle: int) -> void:
	if _door_root == null:
		return
	var leaf_l: Node3D = null
	var leaf_r: Node3D = null
	var cw: Node3D = null
	var stack: Array[Node] = [_door_root]
	while not stack.is_empty():
		var curr: Node = stack.pop_back()
		if curr is Node3D:
			var nm: String = curr.name.to_lower()
			if nm.contains("leaf_left") or nm.contains("leaf_a"):
				leaf_l = curr as Node3D
			elif nm.contains("leaf_right") or nm.contains("leaf_b"):
				leaf_r = curr as Node3D
			elif nm.contains("counterweight") or nm.contains("carriage"):
				cw = curr as Node3D
		for ch: Node in curr.get_children():
			stack.append(ch)

	# Cycle 0 (Initial): Leaf_A closed (0.0), Leaf_B wedged 0.18m ajar
	# Cycle 1 (40% Jam): Leaf_A open (-1.05m), Leaf_B jammed at 40% (+0.44m)
	# Cycle 2 (Droid Sync): Both leaves mid-calibration stroke (-0.82m / +0.82m)
	# Cycle 3 (100% Unlocked): Both leaves glided 100% open (-1.10m / +1.10m)
	if cycle == 1:
		_play_actor_anim(_door_root, ["Cycle1_JamAt40"], 0.65)
	elif cycle == 2:
		_play_actor_anim(_door_root, ["Cycle2_CounterweightSync"], 0.85)
	elif cycle == 3:
		_play_actor_anim(_door_root, ["Cycle3_FullOpen"], 1.38)
	if leaf_l != null:
		if cycle == 0:
			leaf_l.position.x = -0.52
		elif cycle == 1:
			leaf_l.position.x = -1.42
		elif cycle == 2:
			leaf_l.position.x = -1.25
		else:
			leaf_l.position.x = -1.48
	if leaf_r != null:
		if cycle == 0:
			leaf_r.position.x = 0.68
		elif cycle == 1:
			leaf_r.position.x = 0.90
		elif cycle == 2:
			leaf_r.position.x = 1.25
		else:
			leaf_r.position.x = 1.48
	if cw != null:
		cw.position.x = 0.35 if cycle <= 1 else -0.55


func _play_actor_anim(actor: Node3D, preferred_names: Array, seek_t: float) -> void:
	if actor == null:
		return
	var stack: Array[Node] = [actor]
	while not stack.is_empty():
		var curr: Node = stack.pop_back()
		if curr is AnimationPlayer:
			var ap: AnimationPlayer = curr as AnimationPlayer
			var alist: PackedStringArray = ap.get_animation_list()
			for pname in preferred_names:
				if alist.has(String(pname)):
					ap.play(String(pname))
					ap.seek(seek_t, true)
					ap.advance(0.0)
					ap.speed_scale = 0.0
					return
			for a: String in alist:
				if a != "RESET":
					ap.play(a)
					ap.seek(seek_t, true)
					ap.advance(0.0)
					ap.speed_scale = 0.0
					return
		for ch: Node in curr.get_children():
			stack.append(ch)


func _set_indicator_color(mi: MeshInstance3D, col: Color, energy: float) -> void:
	if mi == null:
		return
	var smat: StandardMaterial3D = mi.material_override as StandardMaterial3D
	if smat != null:
		smat.albedo_color = col
		smat.emission = col
		smat.emission_energy_multiplier = energy


func apply_camera_and_cycle_state(idx: int) -> void:
	if idx < 0 or idx >= CAMERAS.size() or _camera == null:
		return
	_current_cycle = idx
	var c: Dictionary = CAMERAS[idx]
	var cycle: int = int(c["cycle"])

	# 1. Position Camera
	_camera.near = 0.02
	_camera.far = 500.0
	_camera.fov = float(c["fov"])
	_camera.global_position = c["pos"] as Vector3
	_camera.look_at(c["target"] as Vector3, Vector3.UP)

	# 2. Door Leaves & Header Calibration Nodes
	_set_door_state(cycle)

	if _header_indicators.size() >= 3:
		if cycle == 0:
			# Initial: all 3 header nodes pulsing amber
			for i: int in range(3):
				_set_indicator_color(_header_indicators[i], Color("#FF9500"), 2.0)
			_set_indicator_color(_threshold_strip, Color("#FF9500"), 2.0)
			_pedestal_light.light_color = Color("#FF9500")
			_pedestal_light.light_energy = 1.15
			_counterweight_light.light_color = Color("#FF9500")
			_relay_light.light_color = Color("#FF9500")
		elif cycle == 1:
			# Cycle 1 (40% Jam): Node 1 Cyan `#00E5FF`, Nodes 2-3 Fault Red-Orange `#FF2E1F`
			_set_indicator_color(_header_indicators[0], Color("#00E5FF"), 2.6)
			_set_indicator_color(_header_indicators[1], Color("#FF2E1F"), 2.4)
			_set_indicator_color(_header_indicators[2], Color("#FF9500"), 1.8)
			_set_indicator_color(_threshold_strip, Color("#FF2E1F"), 2.2)
			_pedestal_light.light_color = Color("#00E5FF")
			_pedestal_light.light_energy = 1.35
			_counterweight_light.light_color = Color("#FF2E1F")
			_counterweight_light.light_energy = 1.50
			_relay_light.light_color = Color("#FFB703")
		elif cycle == 2:
			# Cycle 2 (Droid Relay Sync): Nodes 1-2 Cyan `#00E5FF`, Node 3 Handshake Amber `#FFB703`
			_set_indicator_color(_header_indicators[0], Color("#00E5FF"), 2.6)
			_set_indicator_color(_header_indicators[1], Color("#00E5FF"), 2.6)
			_set_indicator_color(_header_indicators[2], Color("#FFB703"), 2.5)
			_set_indicator_color(_threshold_strip, Color("#FFB703"), 2.2)
			_pedestal_light.light_color = Color("#00E5FF")
			_pedestal_light.light_energy = 1.25
			_counterweight_light.light_color = Color("#00E5FF")
			_counterweight_light.light_energy = 1.30
			_relay_light.light_color = Color("#00E5FF")
			_relay_light.light_energy = 1.55
		else:
			# Cycle 3 (100% Unlocked): All 3 header nodes & floor threshold solid `#00E5FF` Cyan (`energy = 1.40`)
			for i: int in range(3):
				_set_indicator_color(_header_indicators[i], Color("#00E5FF"), 2.8)
			_set_indicator_color(_threshold_strip, Color("#00E5FF"), 2.6)
			_pedestal_light.light_color = Color("#00E5FF")
			_pedestal_light.light_energy = 1.40
			_counterweight_light.light_color = Color("#00E5FF")
			_counterweight_light.light_energy = 1.40
			_relay_light.light_color = Color("#00E5FF")
			_relay_light.light_energy = 1.30

	# 3. Position Actors (`Commuter A`, `Commuter B`, `Unit A7-D2 Droid`, `Tech Rostov #02`) per Cycle
	if _commuter_a != null:
		if cycle == 0:
			# Commuter A steps up to RFID pedestal (X=1.25, Z=-3.10) raising left wrist in wordless demonstration!
			_commuter_a.position = Vector3(1.18, 0.0, -2.95)
			_commuter_a.rotation_degrees = Vector3(0.0, 165.0, 0.0)
			_play_actor_anim(_commuter_a, ["WristRaiseDemo", "WalkCycle"], 1.10)
		elif cycle == 1:
			_commuter_a.position = Vector3(2.15, 0.0, -2.25)
			_commuter_a.rotation_degrees = Vector3(0.0, -145.0, 0.0)
			_play_actor_anim(_commuter_a, ["Idle", "WalkCycle"], 0.15)
		elif cycle == 2:
			_commuter_a.position = Vector3(1.85, 0.0, -1.95)
			_commuter_a.rotation_degrees = Vector3(0.0, 170.0, 0.0)
			_play_actor_anim(_commuter_a, ["Idle", "WalkCycle"], 0.15)
		else:
			# Cycle 3: Walking out through the open 2.20m bulkhead doorway waving thank-you!
			_commuter_a.position = Vector3(-0.38, 0.0, -3.55)
			_commuter_a.rotation_degrees = Vector3(0.0, 175.0, 0.0)
			_play_actor_anim(_commuter_a, ["WristRaiseDemo", "WalkCycle"], 1.10)

	if _commuter_b != null:
		if cycle == 0:
			_commuter_b.position = Vector3(2.45, 0.0, -1.55)
			_commuter_b.rotation_degrees = Vector3(0.0, -135.0, 0.0)
			_play_actor_anim(_commuter_b, ["Idle", "WalkCycle"], 0.30)
		elif cycle == 1:
			# Steps forward hopefully as Leaf_A opens
			_commuter_b.position = Vector3(-0.55, 0.0, -2.35)
			_commuter_b.rotation_degrees = Vector3(0.0, 175.0, 0.0)
			_play_actor_anim(_commuter_b, ["WalkCycle"], 0.25)
		elif cycle == 2:
			_commuter_b.position = Vector3(0.95, 0.0, -2.10)
			_commuter_b.rotation_degrees = Vector3(0.0, 165.0, 0.0)
			_play_actor_anim(_commuter_b, ["Idle", "WalkCycle"], 0.10)
		else:
			# Walking through the open doorway right behind Commuter A
			_commuter_b.position = Vector3(0.45, 0.0, -2.85)
			_commuter_b.rotation_degrees = Vector3(0.0, 178.0, 0.0)
			_play_actor_anim(_commuter_b, ["WalkCycle"], 0.15)

	if _droid_root != null:
		if cycle == 0:
			# Standing attentively beside the relay wall pointing headlamp toward the RFID pedestal
			_droid_root.position = Vector3(-1.35, 0.0, -2.85)
			_droid_root.rotation_degrees = Vector3(0.0, 125.0, 0.0)
			_play_actor_anim(_droid_root, ["Idle", "WalkCycle"], 0.20)
		elif cycle == 1:
			# Rolling over toward Relay_Panel_B (`X = -1.85m, Z = -3.55m`)
			_droid_root.position = Vector3(-1.45, 0.0, -3.15)
			_droid_root.rotation_degrees = Vector3(0.0, -155.0, 0.0)
			_play_actor_anim(_droid_root, ["DiagnosticProbe", "WalkCycle"], 0.35)
		elif cycle == 2:
			# Plugged into Relay_Panel_B with probe arm extended and #D95B26 transponder collar angled toward player!
			_droid_root.position = Vector3(-1.42, 0.0, -3.38)
			_droid_root.rotation_degrees = Vector3(0.0, -140.0, 0.0)
			_play_actor_anim(_droid_root, ["DiagnosticProbe", "Idle"], 0.55)
		else:
			# Backed clear of the open doorway, nodding optic head in #00E5FF cyan
			_droid_root.position = Vector3(-1.75, 0.0, -2.65)
			_droid_root.rotation_degrees = Vector3(0.0, 140.0, 0.0)
			_play_actor_anim(_droid_root, ["Idle"], 0.0)

	# 4. Third-Person Lead Tech Rostov (`#02`) vs. First-Person Center-Screen Wrist RFID Rig
	var show_fp_wrist: bool = bool(c["fp_wrist"])
	if _rostov_root != null:
		_rostov_root.visible = not show_fp_wrist
		if cycle == 0:
			_rostov_root.position = Vector3(-0.65, 0.0, 0.45)
			_rostov_root.rotation_degrees = Vector3(0.0, 162.0, 0.0)
			_play_actor_anim(_rostov_root, ["WalkCycle"], 0.15)
		elif cycle == 3:
			_rostov_root.position = Vector3(0.85, 0.0, -0.85)
			_rostov_root.rotation_degrees = Vector3(0.0, -158.0, 0.0)
			_play_actor_anim(_rostov_root, ["WalkCycle"], 0.15)

	if _fp_wrist_holder != null:
		_fp_wrist_holder.visible = show_fp_wrist
		if _wrist_spot != null:
			_wrist_spot.visible = show_fp_wrist
		if show_fp_wrist and _fp_wrist_model != null:
			_play_actor_anim(_fp_wrist_model, ["RFIDPulse", "WristRaiseInspect"], 0.50)

	# 5. Position Diegetic Inductive Coupling Arc & Harmonic Wave Rings
	var w_target: Vector3 = c["wrist_target"] as Vector3
	var w_start: Vector3 = Vector3(1.18, 1.16, -2.95)
	if show_fp_wrist and _fp_wrist_holder != null:
		w_start = _fp_wrist_holder.global_position + Vector3(0.0, 0.04, 0.0)
	elif cycle == 0:
		# Commuter A's raised left wrist coupling with the pedestal (amber lockout flash)
		w_start = Vector3(1.24, 1.18, -3.12)
	elif cycle == 3:
		w_start = Vector3(1.55, 1.18, -3.62)

	var arc_Col: Color = Color("#FF9500") if cycle == 0 else Color("#00E5FF")
	if _rfid_beam_mesh != null:
		_rfid_beam_mesh.visible = (cycle != 3)
		var bmat: StandardMaterial3D = _rfid_beam_mesh.material_override as StandardMaterial3D
		if bmat != null:
			bmat.albedo_color = Color(arc_Col.r, arc_Col.g, arc_Col.b, 0.55)
			bmat.emission = arc_Col
		var mid: Vector3 = (w_start + w_target) * 0.5
		var dist: float = maxf(0.15, w_start.distance_to(w_target))
		_rfid_beam_mesh.global_position = mid
		var cmesh: CylinderMesh = _rfid_beam_mesh.mesh as CylinderMesh
		if cmesh != null:
			cmesh.height = dist
		var dir: Vector3 = (w_target - w_start).normalized()
		if dir.length_squared() > 0.001:
			var up_v: Vector3 = Vector3.UP if absf(dir.dot(Vector3.UP)) < 0.95 else Vector3.RIGHT
			var z_ax: Vector3 = dir.cross(up_v).normalized()
			var x_ax: Vector3 = dir.cross(z_ax).normalized()
			_rfid_beam_mesh.global_transform.basis = Basis(x_ax, dir, z_ax)

	for r_i: int in range(_rfid_pulse_rings.size()):
		var pr: MeshInstance3D = _rfid_pulse_rings[r_i]
		pr.visible = true
		var t_frac: float = float(r_i + 1) / float(_rfid_pulse_rings.size() + 1)
		pr.global_position = w_start.lerp(w_target, t_frac)
		pr.rotation_degrees = Vector3(90.0, 0.0, 0.0)
		var rmat: StandardMaterial3D = pr.material_override as StandardMaterial3D
		if rmat != null:
			rmat.albedo_color = Color(arc_Col.r, arc_Col.g, arc_Col.b, 0.72)
			rmat.emission = arc_Col


func _upgrade_preface_materials(root: Node3D, is_wrist: bool) -> void:
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
		var orig_name: String = imp.name
		var mi: MeshInstance3D = MeshInstance3D.new()
		mi.transform = imp.transform
		if imp.mesh != null and imp.mesh.get_surface_count() > 0:
			mi.mesh = imp.mesh.get_mesh()
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

	var tex_room_alb: Texture2D = _load_tex("preface_test_room_atlas_albedo.png")
	var tex_room_orm: Texture2D = _load_tex("preface_test_room_atlas_orm.png")
	var tex_room_nrm: Texture2D = _load_tex("preface_test_room_atlas_normal.png")
	var tex_room_emi: Texture2D = _load_tex("preface_test_room_atlas_emission.png")
	var tex_room_gls: Texture2D = _load_tex("preface_test_room_glass_translucent.png")

	var tex_wrist_alb: Texture2D = _load_tex("wrist_rfid_atlas_albedo.png")
	var tex_wrist_orm: Texture2D = _load_tex("wrist_rfid_atlas_orm.png")
	var tex_wrist_nrm: Texture2D = _load_tex("wrist_rfid_atlas_normal.png")
	var tex_wrist_emi: Texture2D = _load_tex("wrist_rfid_atlas_emission.png")
	var tex_wrist_hlo: Texture2D = _load_tex("wrist_rfid_holo_translucent.png")

	var mstack: Array[Node] = [root]
	while not mstack.is_empty():
		var curr: Node = mstack.pop_back()
		if curr is MeshInstance3D:
			var mi: MeshInstance3D = curr as MeshInstance3D
			if mi.mesh != null:
				mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_ON
				for s_idx: int in range(mi.mesh.get_surface_count()):
					var mat: Material = mi.get_active_material(s_idx)
					if mat is StandardMaterial3D:
						var smat: StandardMaterial3D = (mat as StandardMaterial3D).duplicate() as StandardMaterial3D
						var mname: String = smat.resource_name.to_lower()
						var pname: String = mi.name.to_lower()
						smat.cull_mode = BaseMaterial3D.CULL_DISABLED
						if smat.emission_texture != null:
							smat.emission_operator = BaseMaterial3D.EMISSION_OP_MULTIPLY

						if mname.contains("glass") or mname.contains("translucent") or mname.contains("transom") or mname.contains("viewport") or mname.contains("holo") or mname.contains("sapphire") or mname.contains("visor") or pname.contains("glass") or pname.contains("transom"):
							smat.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
							smat.albedo_color.a = clampf(smat.albedo_color.a, 0.24, 0.36)
							if is_wrist and tex_wrist_hlo != null:
								smat.albedo_texture = tex_wrist_hlo
								smat.emission_texture = tex_wrist_hlo
							elif not is_wrist and tex_room_gls != null and smat.albedo_texture == null:
								smat.albedo_texture = tex_room_gls
							smat.roughness = 0.08
							smat.metallic = 0.16
							smat.metallic_specular = 0.92
							smat.emission_enabled = true
							if smat.emission == Color(0, 0, 0, 1):
								smat.emission = Color("#00E5FF")
							smat.emission_energy_multiplier = 1.45 if is_wrist else 0.35
							mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
						elif is_wrist and (mname.contains("wrist") or mname.contains("atlas") or mname.contains("subdermal") or mname.contains("cuff")):
							if tex_wrist_alb != null and smat.albedo_texture == null:
								smat.albedo_texture = tex_wrist_alb
							if tex_wrist_nrm != null:
								smat.normal_enabled = true
								smat.normal_texture = tex_wrist_nrm
								smat.normal_scale = 0.65
							if tex_wrist_orm != null:
								smat.ao_enabled = true
								smat.ao_texture = tex_wrist_orm
							if tex_wrist_emi != null:
								smat.emission_enabled = true
								smat.emission_texture = tex_wrist_emi
								smat.emission = Color(1.0, 1.0, 1.0)
								smat.emission_operator = BaseMaterial3D.EMISSION_OP_MULTIPLY
								smat.emission_energy_multiplier = 2.4
						elif not is_wrist and (mname.contains("preface") or mname.contains("room_atlas") or mname.contains("service_door") or mname.contains("commuter") or mname.contains("droid")):
							if tex_room_alb != null and smat.albedo_texture == null:
								smat.albedo_texture = tex_room_alb
							if tex_room_nrm != null:
								smat.normal_enabled = true
								smat.normal_texture = tex_room_nrm
								smat.normal_scale = 0.55
							if tex_room_orm != null:
								smat.ao_enabled = true
								smat.ao_texture = tex_room_orm
							if tex_room_emi != null:
								smat.emission_enabled = true
								smat.emission_texture = tex_room_emi
								smat.emission = Color(1.0, 1.0, 1.0)
								smat.emission_operator = BaseMaterial3D.EMISSION_OP_MULTIPLY
								smat.emission_energy_multiplier = 1.65
						elif smat.emission_enabled or mname.contains("emissive") or mname.contains("led") or mname.contains("vein") or mname.contains("node") or mname.contains("cyan") or mname.contains("amber"):
							smat.emission_enabled = true
							if smat.emission == Color(0, 0, 0, 1):
								smat.emission = smat.albedo_color
							smat.emission_energy_multiplier = 2.4 if is_wrist else 1.85

						mi.set_surface_override_material(s_idx, smat)
		for ch: Node in curr.get_children():
			mstack.append(ch)


func _process(_delta: float) -> void:
	_frame_counter += 1
	if _batch_render:
		_process_batch_render()
		return
	if _validate_only and _frame_counter >= 4:
		get_tree().quit(0)


func _process_batch_render() -> void:
	if DisplayServer.get_name() == "headless":
		get_tree().quit(0)
		return
	if _frame_counter < 6:
		return
	if _render_step >= CAMERAS.size():
		print("[PrefaceServiceCallTest] Completed all ", CAMERAS.size(), " preface test environment renders!")
		get_tree().quit(0)
		return
	if _render_wait == 0:
		apply_camera_and_cycle_state(_render_step)
		_render_wait = 1
		return
	_render_wait += 1
	if _render_wait >= 6:
		var c: Dictionary = CAMERAS[_render_step]
		var cam_name: String = String(c["name"])
		var short_alias: String = "cam_%02d" % (_render_step + 1)
		var img: Image = get_viewport().get_texture().get_image()
		if img != null and not img.is_empty():
			for out_dir_res: String in OUT_DIRS:
				var out_dir: String = _resolve_path(out_dir_res)
				DirAccess.make_dir_recursive_absolute(out_dir)
				var f1: String = out_dir.path_join(cam_name + ".png")
				var f2: String = out_dir.path_join(short_alias + ".png")
				if img.save_png(f1) == OK:
					print("[PrefaceServiceCallTest] Saved ", f1)
				img.save_png(f2)
		_render_step += 1
		_render_wait = 0
