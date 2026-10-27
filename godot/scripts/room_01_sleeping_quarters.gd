class_name Room01SleepingQuarters
extends Node3D
## Room 01 — Crew Sleeping Quarters ("Aegis-7 Standard" Full Stateroom Showcase: 6.0m W x 7.0m D x 3.2m H)
## Assembles the Aegis-7 stateroom architectural shell (with open North & West viewport cutouts),
## dual exterior vistas (vista_oneill_cylinder_interior.png North, vista_deep_space.png West),
## all locked Bunk Pod & Sleeping Quarters Fixture winners at Sloane's exact coordinates,
## 7-light Aegis-7 lighting rig, and 4 standardized 1080p beauty camera presets.

const WINNERS_GLB_DIR := "res://../assets/glb/winners"
const SHARED_TEX_DIR := "res://../assets/textures"
const SPEC_PATH := "res://../design/rooms/room_01_sleeping_quarters_spec.md"

const OUT_DIRS := [
	"res://renders/rooms/room_01",
	"res://../assets/renders/rooms/room_01"
]

const PLACEMENTS := [
	{
		"slot": "Bunk_01_OrbitalViewport",
		"file": "bunk_winner_01_orbital_viewport.glb",
		"pos": Vector3(-2.32, 0.00, -1.85),
		"rot_y": 90.0
	},
	{
		"slot": "Bunk_02_ObservationLounge",
		"file": "bunk_winner_04_observation_lounge.glb",
		"pos": Vector3(1.65, 0.00, -2.72),
		"rot_y": 0.0
	},
	{
		"slot": "Bunk_03_HexHiveStack",
		"file": "bunk_winner_03_hex_hive_stack.glb",
		"pos": Vector3(-2.32, 0.00, 0.85),
		"rot_y": 90.0
	},
	{
		"slot": "Fixture_01_EVALocker",
		"file": "locker_winner_01_dual_bay_bulkhead.glb",
		"pos": Vector3(2.52, 0.00, 1.95),
		"rot_y": -90.0
	},
	{
		"slot": "Fixture_02_HygieneVanity",
		"file": "vanity_winner_01_dual_zone_grooming.glb",
		"pos": Vector3(2.62, 0.00, -1.65),
		"rot_y": -90.0
	},
	{
		"slot": "Fixture_03_CabinWallDesk",
		"file": "walldesk_winner_01_split_comms_station.glb",
		"pos": Vector3(2.58, 0.00, 0.15),
		"rot_y": -90.0
	},
	{
		"slot": "Fixture_06_CargoFootlocker",
		"file": "footlocker_winner_01_split_cargo_trunk.glb",
		"pos": Vector3(-1.05, 0.00, -1.85),
		"rot_y": 90.0
	},
	{
		"slot": "Fixture_09_ClimateO2Station",
		"file": "climate_winner_01_split_env_o2_station.glb",
		"pos": Vector3(1.25, 0.00, 3.28),
		"rot_y": 180.0
	}
]

const CAMERAS := [
	{
		"name": "cam_01_overview_south_entry",
		"label": "01 — Wide Overview from South Airlock Entry",
		"pos": Vector3(0.00, 1.75, 3.10),
		"target": Vector3(0.00, 1.05, -1.20),
		"fov": 58.0
	},
	{
		"name": "cam_02_west_bunks_and_footlocker",
		"label": "02 — West Bunk Bays (Deep-Space Viewport) & Split Cargo Footlocker",
		"pos": Vector3(1.95, 1.52, 0.25),
		"target": Vector3(-2.10, 1.00, -0.85),
		"fov": 52.0
	},
	{
		"name": "cam_03_east_aegis_utility_wall",
		"label": "03 — East Aegis-7 Split-Bay Utility Triad (Vanity, Desk & EVA Locker)",
		"pos": Vector3(-1.75, 1.48, 0.20),
		"target": Vector3(2.45, 1.08, 0.15),
		"fov": 52.0
	},
	{
		"name": "cam_04_north_viewport_and_climate",
		"label": "04 — South Entry Bulkhead, Climate/O2 Station & EVA Suit Locker",
		"pos": Vector3(-1.40, 1.55, -1.60),
		"target": Vector3(1.35, 1.15, 2.60),
		"fov": 54.0
	}
]

var _shell_container: Node3D
var _fixtures_container: Node3D
var _lights_container: Node3D
var _camera: Camera3D

var _tex_cache: Dictionary = {}
var current_cam_index: int = 0
var _batch_render: bool = false
var _validate_only: bool = false
var _frame_counter: int = 0
var _render_step: int = 0
var _render_wait: int = 0


func _ready() -> void:
	_camera = get_node_or_null("RoomCamera") as Camera3D
	_shell_container = get_node_or_null("RoomShell") as Node3D
	_fixtures_container = get_node_or_null("FixturesAndBunks") as Node3D
	_lights_container = get_node_or_null("RoomLighting") as Node3D

	if _shell_container == null:
		_shell_container = Node3D.new()
		_shell_container.name = "RoomShell"
		add_child(_shell_container)
	if _fixtures_container == null:
		_fixtures_container = Node3D.new()
		_fixtures_container.name = "FixturesAndBunks"
		add_child(_fixtures_container)
	if _lights_container == null:
		_lights_container = Node3D.new()
		_lights_container.name = "RoomLighting"
		add_child(_lights_container)

	var all_args: PackedStringArray = OS.get_cmdline_args() + OS.get_cmdline_user_args()
	for arg: String in all_args:
		if arg == "--render-all" or arg == "--capture-screenshots" or arg == "--screenshots":
			_batch_render = true
		elif arg == "--validate-only" or arg == "--validate":
			_validate_only = true

	if OS.get_environment("CAPTURE_SCREENSHOTS") == "1" or OS.get_environment("RENDER_ALL") == "1":
		_batch_render = true
	if OS.get_environment("VALIDATE_ONLY") == "1":
		_validate_only = true

	if DisplayServer.get_name() == "headless" and not _batch_render:
		_validate_only = true

	_build_aegis7_stateroom_shell()
	_assemble_all_winners()
	_setup_room01_lighting()
	apply_camera_preset(0)


func _load_tex(fname: String) -> Texture2D:
	if _tex_cache.has(fname):
		return _tex_cache[fname] as Texture2D
	var search_dirs: Array[String] = [
		SHARED_TEX_DIR,
		SHARED_TEX_DIR + "/bunk_round2",
		SHARED_TEX_DIR + "/locker_round1",
		SHARED_TEX_DIR + "/vanity_round1",
		SHARED_TEX_DIR + "/walldesk_round1",
		SHARED_TEX_DIR + "/footlocker_round1",
		SHARED_TEX_DIR + "/climate_round1"
	]
	for d: String in search_dirs:
		var p: String = d + "/" + fname
		if FileAccess.file_exists(p):
			var img: Image = Image.new()
			if img.load(p) == OK and not img.is_empty():
				img.generate_mipmaps()
				var tex: ImageTexture = ImageTexture.create_from_image(img)
				_tex_cache[fname] = tex
				return tex
	return null


func _make_mat(tex_name: String, col: Color, rough: float, metal: float, emissive_col: Color = Color(0, 0, 0, 0), energy: float = 0.0) -> StandardMaterial3D:
	var mat: StandardMaterial3D = StandardMaterial3D.new()
	var tex: Texture2D = _load_tex(tex_name) if tex_name != "" else null
	if tex != null:
		mat.albedo_texture = tex
	mat.albedo_color = col
	mat.roughness = rough
	mat.metallic = metal
	mat.cull_mode = BaseMaterial3D.CULL_DISABLED
	if energy > 0.0:
		mat.emission_enabled = true
		mat.emission = emissive_col
		mat.emission_energy_multiplier = energy
	return mat


## Builds the 6.0m W x 7.0m D x 3.2m H Aegis-7 Stateroom Shell with open North & West viewport cutouts
func _build_aegis7_stateroom_shell() -> void:
	for ch: Node in _shell_container.get_children():
		ch.free()

	var mat_gunmetal: StandardMaterial3D = _make_mat("titanium_gunmetal_hull.png", Color("#1A1E24"), 0.34, 0.78)
	var mat_slate: StandardMaterial3D = _make_mat("carbon_slate_frame.png", Color("#282E38"), 0.40, 0.58)
	var mat_aero_white: StandardMaterial3D = _make_mat("composite_aerospace_white.png", Color("#D8DEE6"), 0.28, 0.08)
	var mat_steel: StandardMaterial3D = _make_mat("steel_machined_gantry.png", Color("#88929E"), 0.22, 0.90)
	var mat_cyan_led: StandardMaterial3D = _make_mat("", Color("#00E5FF"), 0.15, 0.0, Color("#00E5FF"), 2.2)
	var mat_amber_led: StandardMaterial3D = _make_mat("", Color("#FF9500"), 0.15, 0.0, Color("#FF9500"), 2.0)

	# Translucent viewport glass (TRANSPARENCY_ALPHA, SHADOW_CASTING_SETTING_OFF)
	var mat_glass: StandardMaterial3D = StandardMaterial3D.new()
	var gtex: Texture2D = _load_tex("glass_viewport_translucent.png")
	if gtex != null:
		mat_glass.albedo_texture = gtex
	mat_glass.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
	mat_glass.albedo_color = Color(0.84, 0.95, 1.0, 0.18)
	mat_glass.roughness = 0.08
	mat_glass.metallic = 0.10
	mat_glass.metallic_specular = 0.90
	mat_glass.cull_mode = BaseMaterial3D.CULL_DISABLED

	# 1. Floor Deck (6.0m W x 7.0m D at Y = 0.0) + Steel Expansion Strips + Amber Guide Strips (X = ±1.35m)
	_add_box(_shell_container, "DeckFloor", Vector3(6.2, 0.08, 7.2), Vector3(0.0, -0.04, 0.0), mat_slate)
	for z_strip: float in [-2.5, -0.8, 0.8, 2.5]:
		_add_box(_shell_container, "DeckSteelJoint_" + str(z_strip), Vector3(5.8, 0.008, 0.06), Vector3(0.0, 0.002, z_strip), mat_steel)
	for x_guide: float in [-1.35, 1.35]:
		_add_box(_shell_container, "DeckAmberGuide_" + str(x_guide), Vector3(0.04, 0.008, 6.6), Vector3(x_guide, 0.003, 0.0), mat_amber_led, false)

	# 2. Ceiling Deck (6.0m W x 7.0m D at Y = 3.20m) + Coffered Aerospace-White Panels + Cyan Cove Channels (X = ±2.45m)
	_add_box(_shell_container, "CeilingHull", Vector3(6.2, 0.08, 7.2), Vector3(0.0, 3.24, 0.0), mat_gunmetal)
	for z_cof: float in [-2.55, -0.85, 0.85, 2.55]:
		_add_box(_shell_container, "CeilingCoffer_" + str(z_cof), Vector3(4.6, 0.06, 1.45), Vector3(0.0, 3.17, z_cof), mat_aero_white)
	for x_cove: float in [-2.45, 2.45]:
		_add_box(_shell_container, "CeilingCyanCove_" + str(x_cove), Vector3(0.05, 0.03, 6.6), Vector3(x_cove, 2.98, 0.0), mat_cyan_led, false)

	# 3. 5 Repeating 45° Chamfered Octagonal Titanium Structural Ribs (Z = -3.40, -1.70, 0.00, +1.70, +3.40)
	for z_rib: float in [-3.40, -1.70, 0.00, 1.70, 3.40]:
		_add_box(_shell_container, "RibWest_" + str(z_rib), Vector3(0.18, 3.20, 0.18), Vector3(-2.95, 1.60, z_rib), mat_gunmetal)
		_add_box(_shell_container, "RibEast_" + str(z_rib), Vector3(0.18, 3.20, 0.18), Vector3(2.95, 1.60, z_rib), mat_gunmetal)
		_add_box(_shell_container, "RibTop_" + str(z_rib), Vector3(6.00, 0.18, 0.18), Vector3(0.0, 3.11, z_rib), mat_gunmetal)
		# 45° upper corner chamfers
		var ch_w: MeshInstance3D = _add_box(_shell_container, "ChamferUpperW_" + str(z_rib), Vector3(0.65, 0.16, 0.18), Vector3(-2.68, 2.88, z_rib), mat_gunmetal)
		ch_w.rotation_degrees.z = 45.0
		var ch_e: MeshInstance3D = _add_box(_shell_container, "ChamferUpperE_" + str(z_rib), Vector3(0.65, 0.16, 0.18), Vector3(2.68, 2.88, z_rib), mat_gunmetal)
		ch_e.rotation_degrees.z = -45.0

	# 4. East Bulkhead Wall (X = +3.00m) — solid dark titanium bulkhead behind Vanity, Desk, and EVA Locker
	_add_box(_shell_container, "WallEast_Upper", Vector3(0.12, 2.15, 7.0), Vector3(3.04, 2.125, 0.0), mat_gunmetal)
	_add_box(_shell_container, "WallEast_Wainscot", Vector3(0.14, 1.05, 7.0), Vector3(3.03, 0.525, 0.0), mat_slate)
	_add_box(_shell_container, "WallEast_SteelRail", Vector3(0.16, 0.05, 7.0), Vector3(3.02, 1.05, 0.0), mat_steel)

	# 5. West Bulkhead Wall (X = -3.00m) — WITH OPEN VIEWPORT CUTOUTS behind Bunk #1 (Z=-1.85) and Bunk #3 (Z=+0.85)
	_add_box(_shell_container, "WallWest_LowerSill", Vector3(0.12, 0.55, 7.0), Vector3(-3.04, 0.275, 0.0), mat_slate)
	_add_box(_shell_container, "WallWest_UpperHeader", Vector3(0.12, 0.85, 7.0), Vector3(-3.04, 2.775, 0.0), mat_gunmetal)
	_add_box(_shell_container, "WallWest_PierNorth", Vector3(0.12, 1.80, 0.55), Vector3(-3.04, 1.45, -3.22), mat_gunmetal)
	_add_box(_shell_container, "WallWest_PierMid", Vector3(0.12, 1.80, 0.55), Vector3(-3.04, 1.45, -0.50), mat_gunmetal)
	_add_box(_shell_container, "WallWest_PierSouth", Vector3(0.12, 1.80, 1.50), Vector3(-3.04, 1.45, 2.75), mat_gunmetal)

	# West Outer-Hull Deep-Space Vista Backdrop Plane at X = -3.55m
	var mat_space_vista: StandardMaterial3D = StandardMaterial3D.new()
	var stex: Texture2D = _load_tex("vista_deep_space.png")
	if stex != null:
		mat_space_vista.albedo_texture = stex
		mat_space_vista.emission_enabled = true
		mat_space_vista.emission_texture = stex
		mat_space_vista.emission_energy_multiplier = 1.35
	mat_space_vista.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	mat_space_vista.cull_mode = BaseMaterial3D.CULL_DISABLED

	var west_vista: MeshInstance3D = MeshInstance3D.new()
	west_vista.name = "WestOuterHullDeepSpaceVista"
	var wq: QuadMesh = QuadMesh.new()
	wq.size = Vector2(6.6, 2.8)
	west_vista.mesh = wq
	west_vista.position = Vector3(-3.55, 1.55, -0.45)
	west_vista.rotation_degrees = Vector3(0.0, 90.0, 0.0)
	west_vista.material_override = mat_space_vista
	west_vista.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	_shell_container.add_child(west_vista)

	# 6. North Observation Bulkhead (Z = -3.50m) WITH OPEN 3-PANEL PANORAMIC VIEWPORT (X: -1.85..+1.85, Y: 1.05..2.45)
	_add_box(_shell_container, "WallNorth_Lower", Vector3(6.0, 1.05, 0.14), Vector3(0.0, 0.525, -3.54), mat_slate)
	_add_box(_shell_container, "WallNorth_Upper", Vector3(6.0, 0.75, 0.14), Vector3(0.0, 2.825, -3.54), mat_gunmetal)
	_add_box(_shell_container, "WallNorth_LeftPillar", Vector3(1.15, 1.40, 0.14), Vector3(-2.425, 1.75, -3.54), mat_gunmetal)
	_add_box(_shell_container, "WallNorth_RightPillar", Vector3(1.15, 1.40, 0.14), Vector3(2.425, 1.75, -3.54), mat_gunmetal)

	# North Panoramic Viewport Machined-Steel Bezel, Mullions & Translucent Glass
	_add_box(_shell_container, "NorthViewport_Sill", Vector3(3.84, 0.08, 0.22), Vector3(0.0, 1.05, -3.48), mat_steel)
	_add_box(_shell_container, "NorthViewport_Header", Vector3(3.84, 0.08, 0.22), Vector3(0.0, 2.45, -3.48), mat_steel)
	_add_box(_shell_container, "NorthViewport_LeftJamb", Vector3(0.08, 1.48, 0.22), Vector3(-1.86, 1.75, -3.48), mat_steel)
	_add_box(_shell_container, "NorthViewport_RightJamb", Vector3(0.08, 1.48, 0.22), Vector3(1.86, 1.75, -3.48), mat_steel)
	_add_box(_shell_container, "NorthViewport_MullionL", Vector3(0.06, 1.40, 0.18), Vector3(-0.62, 1.75, -3.48), mat_steel)
	_add_box(_shell_container, "NorthViewport_MullionR", Vector3(0.06, 1.40, 0.18), Vector3(0.62, 1.75, -3.48), mat_steel)
	_add_box(_shell_container, "NorthViewport_CyanRim", Vector3(3.70, 0.02, 0.04), Vector3(0.0, 1.09, -3.42), mat_cyan_led, false)
	_add_box(_shell_container, "NorthViewport_Glass", Vector3(3.68, 1.34, 0.02), Vector3(0.0, 1.75, -3.48), mat_glass, false)

	# North Exterior O'Neill Cylinder Interior Vista Backdrop at Z = -4.05m
	var mat_cyl_vista: StandardMaterial3D = StandardMaterial3D.new()
	var ctex: Texture2D = _load_tex("vista_oneill_cylinder_interior.png")
	if ctex != null:
		mat_cyl_vista.albedo_texture = ctex
		mat_cyl_vista.emission_enabled = true
		mat_cyl_vista.emission_texture = ctex
		mat_cyl_vista.emission_energy_multiplier = 1.35
	mat_cyl_vista.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	mat_cyl_vista.cull_mode = BaseMaterial3D.CULL_DISABLED

	var north_vista: MeshInstance3D = MeshInstance3D.new()
	north_vista.name = "NorthONeillCylinderVista"
	var nq: QuadMesh = QuadMesh.new()
	nq.size = Vector2(5.2, 2.8)
	north_vista.mesh = nq
	north_vista.position = Vector3(0.0, 1.75, -4.05)
	north_vista.material_override = mat_cyl_vista
	north_vista.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	_shell_container.add_child(north_vista)

	# 7. South Entry Airlock Bulkhead (Z = +3.50m) with Chamfered Corridor Hatch Frame (X: -0.65..+0.65)
	_add_box(_shell_container, "WallSouth_Left", Vector3(2.35, 3.20, 0.14), Vector3(-1.825, 1.60, 3.54), mat_gunmetal)
	_add_box(_shell_container, "WallSouth_Right", Vector3(2.35, 3.20, 0.14), Vector3(1.825, 1.60, 3.54), mat_gunmetal)
	_add_box(_shell_container, "WallSouth_Header", Vector3(1.30, 0.90, 0.14), Vector3(0.0, 2.75, 3.54), mat_gunmetal)
	_add_box(_shell_container, "SouthAirlock_DoorPanel", Vector3(1.26, 2.30, 0.08), Vector3(0.0, 1.15, 3.52), mat_aero_white)
	_add_box(_shell_container, "SouthAirlock_FrameL", Vector3(0.10, 2.36, 0.20), Vector3(-0.66, 1.18, 3.48), mat_steel)
	_add_box(_shell_container, "SouthAirlock_FrameR", Vector3(0.10, 2.36, 0.20), Vector3(0.66, 1.18, 3.48), mat_steel)
	_add_box(_shell_container, "SouthAirlock_FrameTop", Vector3(1.42, 0.10, 0.20), Vector3(0.0, 2.34, 3.48), mat_steel)
	_add_box(_shell_container, "SouthAirlock_AmberBeacon", Vector3(0.85, 0.03, 0.04), Vector3(0.0, 2.42, 3.42), mat_amber_led, false)


func _add_box(parent: Node3D, bname: String, sz: Vector3, pos: Vector3, mat: Material, casts_shadow: bool = true) -> MeshInstance3D:
	var mi: MeshInstance3D = MeshInstance3D.new()
	mi.name = bname
	var box: BoxMesh = BoxMesh.new()
	box.size = sz
	mi.mesh = box
	mi.position = pos
	mi.material_override = mat
	mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_ON if casts_shadow else GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	parent.add_child(mi)
	return mi


func _assemble_all_winners() -> void:
	for ch: Node in _fixtures_container.get_children():
		ch.free()

	for item: Dictionary in PLACEMENTS:
		var slot_name: String = String(item["slot"])
		var fname: String = String(item["file"])
		var pos: Vector3 = item["pos"] as Vector3
		var rot_y: float = float(item["rot_y"])
		var abs_path: String = WINNERS_GLB_DIR + "/" + fname

		if not FileAccess.file_exists(abs_path):
			print("[Room01] Winner GLB missing: ", abs_path)
			continue

		var doc: GLTFDocument = GLTFDocument.new()
		var state: GLTFState = GLTFState.new()
		if doc.append_from_file(abs_path, state) == OK:
			var root: Node = doc.generate_scene(state)
			if root is Node3D:
				var n3d: Node3D = root as Node3D
				n3d.name = slot_name
				n3d.position = pos
				n3d.rotation_degrees = Vector3(0.0, rot_y, 0.0)
				_fixtures_container.add_child(n3d)
				_upgrade_winner_materials(n3d)
				print("[Room01] Placed ", slot_name, " (", fname, ") at ", pos, " rot_y=", rot_y)


func _upgrade_winner_materials(root: Node3D) -> void:
	var stack: Array[Node] = [root]
	var to_convert: Array[ImporterMeshInstance3D] = []
	while not stack.is_empty():
		var curr: Node = stack.pop_back()
		if curr is ImporterMeshInstance3D:
			to_convert.append(curr as ImporterMeshInstance3D)
		for ch: Node in curr.get_children():
			stack.append(ch)

	for imp: ImporterMeshInstance3D in to_convert:
		var mi: MeshInstance3D = MeshInstance3D.new()
		mi.name = imp.name
		mi.transform = imp.transform
		if imp.mesh != null:
			mi.mesh = imp.mesh.get_mesh()
		var p: Node = imp.get_parent()
		if p != null:
			p.add_child(mi)
			p.remove_child(imp)
			imp.free()

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

						if mname.contains("visor") and mname.contains("gold") or pname.contains("visor") and pname.contains("eva"):
							var vtex: Texture2D = _load_tex("eva_visor_gold_iridium.png")
							if vtex != null:
								smat.albedo_texture = vtex
							smat.albedo_color = Color(1.0, 0.85, 0.42, 1.0)
							smat.metallic = 0.88
							smat.roughness = 0.12
							smat.metallic_specular = 0.92
						elif mname.contains("mirror"):
							var mtex: Texture2D = _load_tex("mirror_smart_hud_cyan.png")
							if mtex != null:
								smat.albedo_texture = mtex
								smat.emission_texture = mtex
							smat.metallic = 0.92
							smat.roughness = 0.06
							smat.emission_enabled = true
							smat.emission = Color(0.18, 0.65, 0.85)
							smat.emission_energy_multiplier = 0.55
						elif mname.contains("glass") or mname.contains("translucent") or pname.contains("glass") or pname.contains("viewport") or pname.contains("window") or (pname.contains("door") and not pname.contains("frame") and not pname.contains("latch")):
							smat.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
							smat.albedo_color.a = clampf(smat.albedo_color.a, 0.18, 0.24)
							smat.roughness = 0.08
							smat.metallic = 0.10
							smat.metallic_specular = 0.90
							mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
						elif mname.contains("oled") or mname.contains("telemetry") or mname.contains("manifest") or mname.contains("sliders"):
							smat.emission_enabled = true
							if smat.albedo_texture != null:
								smat.emission_texture = smat.albedo_texture
							smat.emission = Color(0.22, 0.85, 1.0)
							smat.emission_energy_multiplier = 1.60
						elif smat.emission_enabled or mname.contains("emissive") or mname.contains("led"):
							smat.emission_enabled = true
							if smat.emission == Color(0, 0, 0, 1):
								smat.emission = smat.albedo_color
							smat.emission_energy_multiplier = 2.0

						mi.set_surface_override_material(s_idx, smat)
		for ch: Node in curr.get_children():
			mstack.append(ch)


## Configures Sloane's 7-Light Rig (Section 3 of room_01_sleeping_quarters_spec.md)
func _setup_room01_lighting() -> void:
	for ch: Node in _lights_container.get_children():
		ch.free()

	# 1. DirectionalLight3D (Cylinder_Axial_Skylight)
	var sun: DirectionalLight3D = DirectionalLight3D.new()
	sun.name = "Cylinder_Axial_Skylight"
	sun.rotation_degrees = Vector3(-32.0, -28.0, 0.0)
	sun.light_color = Color("#CFE8FF")
	sun.light_energy = 0.85
	sun.shadow_enabled = true
	sun.shadow_bias = 0.02
	_lights_container.add_child(sun)

	# 2. Ceiling_Cyan_Cove_North
	_add_omni("Ceiling_Cyan_Cove_North", Vector3(0.0, 2.85, -1.65), Color("#00E5FF"), 1.25, 5.5)
	# 3. Ceiling_Cyan_Cove_South
	_add_omni("Ceiling_Cyan_Cove_South", Vector3(0.0, 2.85, 1.65), Color("#00E5FF"), 1.15, 5.5)
	# 4. Bunk_Alcove_Warm_Reading
	_add_omni("Bunk_Alcove_Warm_Reading", Vector3(-1.85, 1.35, -1.85), Color("#FF9500"), 1.35, 3.2)
	# 5. Vanity_And_Desk_Task_Ice
	_add_omni("Vanity_And_Desk_Task_Ice", Vector3(2.10, 1.55, -0.75), Color("#E0F4FF"), 1.45, 3.8)
	# 6. Vanity_UV_Sterilizer_Accent
	_add_omni("Vanity_UV_Sterilizer_Accent", Vector3(2.35, 1.35, -1.45), Color("#7B5CFF"), 1.10, 2.2)
	# 7. Locker_And_Climate_Amber_Safety
	_add_omni("Locker_And_Climate_Amber_Safety", Vector3(1.85, 0.95, 2.10), Color("#FF9500"), 1.15, 3.2)


func _add_omni(lname: String, pos: Vector3, col: Color, energy: float, rng: float) -> OmniLight3D:
	var omni: OmniLight3D = OmniLight3D.new()
	omni.name = lname
	omni.position = pos
	omni.light_color = col
	omni.light_energy = energy
	omni.omni_range = rng
	_lights_container.add_child(omni)
	return omni


func apply_camera_preset(idx: int) -> void:
	if idx < 0 or idx >= CAMERAS.size() or _camera == null:
		return
	current_cam_index = idx
	var c: Dictionary = CAMERAS[idx]
	_camera.global_position = c["pos"] as Vector3
	_camera.fov = float(c["fov"])
	_camera.look_at(c["target"] as Vector3, Vector3.UP)
	print("[Room01] Switched camera to: ", c["name"])


func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventKey:
		var ke: InputEventKey = event as InputEventKey
		if ke.pressed and not ke.echo:
			match ke.keycode:
				KEY_1: apply_camera_preset(0)
				KEY_2: apply_camera_preset(1)
				KEY_3: apply_camera_preset(2)
				KEY_4: apply_camera_preset(3)


func _process(_delta: float) -> void:
	_frame_counter += 1

	if _batch_render:
		_process_batch_render()
		return

	if _validate_only and _frame_counter >= 4:
		print("[Room01] Headless validation complete. Exiting cleanly.")
		get_tree().quit(0)


func _process_batch_render() -> void:
	if DisplayServer.get_name() == "headless":
		get_tree().quit(0)
		return

	if _frame_counter < 6:
		return

	if _render_step >= CAMERAS.size():
		print("[Room01] All 4 Room 01 beauty camera renders complete! Exiting cleanly.")
		get_tree().quit(0)
		return

	if _render_wait == 0:
		apply_camera_preset(_render_step)
		_render_wait = 1
		return

	_render_wait += 1
	if _render_wait >= 6:
		var c: Dictionary = CAMERAS[_render_step]
		var cname: String = String(c["name"])
		var img: Image = get_viewport().get_texture().get_image()
		if img != null and not img.is_empty():
			for d: String in OUT_DIRS:
				DirAccess.make_dir_recursive_absolute(d)
				var out_file: String = d + "/" + cname + ".png"
				if img.save_png(out_file) == OK:
					print("[Room01] Saved render: ", out_file, " (", img.get_width(), "x", img.get_height(), ")")
		_render_step += 1
		_render_wait = 0
