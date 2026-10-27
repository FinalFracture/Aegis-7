class_name Room02TransitCorridor
extends Node3D
## Room 02 — Orbital Sector Transit Corridor & Airlock Hub ("Aegis-7 Standard": 3.6m W x 12.0m D x 3.2m H)
## Loads res://../assets/glb/rooms/room_02_corridor_shell.glb (7 repeating 45° octagonal titanium ribs
## + 6-bay West translucent observation window gallery), places the West vista_oneill_cylinder_interior.png backdrop
## and North/South portal vista backdrops, mounts all locked Aegis-7 corridor fixtures, and renders the 3 beauty cameras.

const SHELL_GLB_PATH := "res://../assets/glb/rooms/room_02_corridor_shell.glb"
const WINNERS_GLB_DIR := "res://../assets/glb/winners"
const CORRIDOR_R1_DIR := "res://../assets/glb/corridor_round1"
const SHARED_TEX_DIR := "res://../assets/textures"

const OUT_DIRS := [
	"res://renders/rooms/room_02",
	"res://../assets/renders/rooms/room_02"
]

const PLACEMENTS := [
	{
		"slot": "North_Main_Sector_Airlock",
		"file": "corridor_door_winner_01_dual_zone_portal.glb",
		"fallback": "corridor_door_r1_02.glb",
		"pos": Vector3(0.00, 0.00, -5.65),
		"rot_y": 0.0,
		"scale": Vector3.ONE
	},
	{
		"slot": "South_Main_Sector_Airlock",
		"file": "corridor_door_winner_01_dual_zone_portal.glb",
		"fallback": "corridor_door_r1_02.glb",
		"pos": Vector3(0.00, 0.00, 5.65),
		"rot_y": 180.0,
		"scale": Vector3.ONE
	},
	{
		"slot": "Cabin_01_Entry_Portal",
		"file": "corridor_door_r1_01.glb",
		"fallback": "corridor_door_r1_01.glb",
		"pos": Vector3(1.72, 0.00, -2.00),
		"rot_y": -90.0,
		"scale": Vector3(0.85, 0.88, 0.85)
	},
	{
		"slot": "Corridor_LifeSupport_O2_Panel",
		"file": "climate_winner_01_split_env_o2_station.glb",
		"fallback": "climate_winner_01_split_env_o2_station.glb",
		"pos": Vector3(1.62, 0.00, 0.00),
		"rot_y": -90.0,
		"scale": Vector3.ONE
	},
	{
		"slot": "Corridor_EVA_Locker_Alcove",
		"file": "locker_winner_01_dual_bay_bulkhead.glb",
		"fallback": "locker_winner_01_dual_bay_bulkhead.glb",
		"pos": Vector3(1.52, 0.00, 3.00),
		"rot_y": -90.0,
		"scale": Vector3.ONE
	},
	{
		"slot": "Staged_Logistics_Cargo_Crate",
		"file": "footlocker_winner_01_split_cargo_trunk.glb",
		"fallback": "footlocker_winner_01_split_cargo_trunk.glb",
		"pos": Vector3(1.15, 0.00, -4.15),
		"rot_y": -90.0,
		"scale": Vector3.ONE
	}
]

const CAMERAS := [
	{
		"name": "cam_01_axial_corridor_perspective",
		"label": "01 — Axial Corridor Perspective Toward North Airlock Checkpoint",
		"pos": Vector3(0.25, 1.55, 4.65),
		"target": Vector3(-0.15, 1.35, -5.65),
		"fov": 54.0
	},
	{
		"name": "cam_02_window_gallery_and_east_bulkhead",
		"label": "02 — East Stateroom Entry Portal, Climate/O2 Panel & EVA Locker",
		"pos": Vector3(-1.15, 1.48, 1.85),
		"target": Vector3(1.55, 1.25, -1.50),
		"fov": 52.0
	},
	{
		"name": "cam_03_airlock_checkpoint_closeup",
		"label": "03 — North Sector Airlock Checkpoint, Parted Doors & West Cylinder Vista",
		"pos": Vector3(0.85, 1.42, -2.65),
		"target": Vector3(0.00, 1.32, -5.65),
		"fov": 48.0
	}
]

var _shell_container: Node3D
var _fixtures_container: Node3D
var _lights_container: Node3D
var _camera: Camera3D

var _tex_cache: Dictionary = {}
var _batch_render: bool = false
var _validate_only: bool = false
var _frame_counter: int = 0
var _render_step: int = 0
var _render_wait: int = 0


func _ready() -> void:
	_camera = get_node_or_null("RoomCamera") as Camera3D
	_shell_container = get_node_or_null("CorridorShell") as Node3D
	_fixtures_container = get_node_or_null("CorridorFixtures") as Node3D
	_lights_container = get_node_or_null("CorridorLighting") as Node3D

	if _shell_container == null:
		_shell_container = Node3D.new()
		_shell_container.name = "CorridorShell"
		add_child(_shell_container)
	if _fixtures_container == null:
		_fixtures_container = Node3D.new()
		_fixtures_container.name = "CorridorFixtures"
		add_child(_fixtures_container)
	if _lights_container == null:
		_lights_container = Node3D.new()
		_lights_container.name = "CorridorLighting"
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

	_load_corridor_shell_and_vistas()
	_assemble_corridor_fixtures()
	_setup_corridor_lighting()
	apply_camera_preset(0)


func _load_tex(fname: String) -> Texture2D:
	if _tex_cache.has(fname):
		return _tex_cache[fname] as Texture2D
	for d: String in [SHARED_TEX_DIR, SHARED_TEX_DIR + "/corridor_round1", SHARED_TEX_DIR + "/bunk_round2"]:
		var p: String = d + "/" + fname
		if FileAccess.file_exists(p):
			var img: Image = Image.new()
			if img.load(p) == OK and not img.is_empty():
				img.generate_mipmaps()
				var tex: ImageTexture = ImageTexture.create_from_image(img)
				_tex_cache[fname] = tex
				return tex
	return null


func _load_corridor_shell_and_vistas() -> void:
	for ch: Node in _shell_container.get_children():
		ch.free()

	if FileAccess.file_exists(SHELL_GLB_PATH):
		var doc: GLTFDocument = GLTFDocument.new()
		var state: GLTFState = GLTFState.new()
		if doc.append_from_file(SHELL_GLB_PATH, state) == OK:
			var root: Node = doc.generate_scene(state)
			if root is Node3D:
				var n3d: Node3D = root as Node3D
				n3d.name = "Aegis7CorridorShell"
				_shell_container.add_child(n3d)
				_upgrade_materials(n3d)
				print("[Room02] Loaded room_02_corridor_shell.glb")

	# Exterior O'Neill Cylinder Vista Backdrop along the West 6-bay translucent window gallery (X = -2.40m)
	# plus behind North (Z = -6.30m) and South (Z = +6.30m) parted airlocks!
	var vmat: StandardMaterial3D = StandardMaterial3D.new()
	var vtex: Texture2D = _load_tex("vista_oneill_cylinder_interior.png")
	if vtex != null:
		vmat.albedo_texture = vtex
		vmat.emission_enabled = true
		vmat.emission_texture = vtex
		vmat.emission_energy_multiplier = 1.35
	vmat.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	vmat.cull_mode = BaseMaterial3D.CULL_DISABLED

	var west_vista: MeshInstance3D = MeshInstance3D.new()
	west_vista.name = "WestGalleryONeillVista"
	var wq: QuadMesh = QuadMesh.new()
	wq.size = Vector2(13.0, 4.2)
	west_vista.mesh = wq
	west_vista.position = Vector3(-2.40, 1.65, 0.0)
	west_vista.rotation_degrees = Vector3(0.0, 90.0, 0.0)
	west_vista.material_override = vmat
	west_vista.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	_shell_container.add_child(west_vista)

	for z_end: float in [-6.35, 6.35]:
		var end_vista: MeshInstance3D = MeshInstance3D.new()
		end_vista.name = "PortalVista_" + str(z_end)
		var eq: QuadMesh = QuadMesh.new()
		eq.size = Vector2(3.6, 3.2)
		end_vista.mesh = eq
		end_vista.position = Vector3(0.0, 1.55, z_end)
		end_vista.material_override = vmat
		end_vista.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
		_shell_container.add_child(end_vista)


func _assemble_corridor_fixtures() -> void:
	for ch: Node in _fixtures_container.get_children():
		ch.free()

	for item: Dictionary in PLACEMENTS:
		var sname: String = String(item["slot"])
		var p1: String = WINNERS_GLB_DIR + "/" + String(item["file"])
		var p2: String = CORRIDOR_R1_DIR + "/" + String(item["fallback"])
		var target_path: String = p1 if FileAccess.file_exists(p1) else p2
		if not FileAccess.file_exists(target_path):
			continue

		var doc: GLTFDocument = GLTFDocument.new()
		var state: GLTFState = GLTFState.new()
		if doc.append_from_file(target_path, state) == OK:
			var root: Node = doc.generate_scene(state)
			if root is Node3D:
				var n3d: Node3D = root as Node3D
				n3d.name = sname
				n3d.position = item["pos"] as Vector3
				n3d.rotation_degrees = Vector3(0.0, float(item["rot_y"]), 0.0)
				n3d.scale = item["scale"] as Vector3
				_fixtures_container.add_child(n3d)
				_upgrade_materials(n3d)
				print("[Room02] Placed ", sname, " at ", n3d.position)


func _upgrade_materials(root: Node3D) -> void:
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

						if mname.contains("visor") and mname.contains("gold"):
							var vtex: Texture2D = _load_tex("eva_visor_gold_iridium.png")
							if vtex != null:
								smat.albedo_texture = vtex
							smat.albedo_color = Color(1.0, 0.85, 0.42, 1.0)
							smat.metallic = 0.88
							smat.roughness = 0.12
						elif mname.contains("glass") or mname.contains("translucent") or pname.contains("glass") or pname.contains("window") or (pname.contains("door") and not pname.contains("frame") and not pname.contains("leaf") and not pname.contains("panel")):
							smat.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
							smat.albedo_color.a = clampf(smat.albedo_color.a, 0.18, 0.22)
							smat.roughness = 0.08
							smat.metallic = 0.10
							smat.metallic_specular = 0.90
							mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
						elif mname.contains("oled") or mname.contains("status") or mname.contains("telemetry") or mname.contains("manifest"):
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


func _setup_corridor_lighting() -> void:
	for ch: Node in _lights_container.get_children():
		ch.free()

	# 1. Axial Cylinder Sunlight angling in from -X through the 6 West translucent panoramic windows
	var sun: DirectionalLight3D = DirectionalLight3D.new()
	sun.name = "AxialCylinderSunlight"
	sun.rotation_degrees = Vector3(-26.0, -72.0, 0.0)
	sun.light_color = Color("#BCE8FF")
	sun.light_energy = 0.95
	sun.shadow_enabled = true
	sun.shadow_bias = 0.02
	_lights_container.add_child(sun)

	# 2. Repeating Ceiling Cyan Cove Lights (Z = -3.5m, 0.0m, +3.5m, Y = 2.85m)
	for cz: float in [-3.5, 0.0, 3.5]:
		_add_omni("CorridorCyanCove_" + str(cz), Vector3(0.0, 2.85, cz), Color("#00E5FF"), 1.20, 5.5)

	# 3. North & South Airlock Cycling Beacons (Z = ±5.1m, Y = 2.35m)
	for bz: float in [-5.1, 5.1]:
		_add_omni("AirlockBeaconAmber_" + str(bz), Vector3(0.0, 2.35, bz), Color("#FF9500"), 1.45, 4.2)


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
	var c: Dictionary = CAMERAS[idx]
	_camera.global_position = c["pos"] as Vector3
	_camera.fov = float(c["fov"])
	_camera.look_at(c["target"] as Vector3, Vector3.UP)


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
		print("[Room02] All 3 Room 02 beauty camera renders complete! Exiting cleanly.")
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
					print("[Room02] Saved render: ", out_file, " (", img.get_width(), "x", img.get_height(), ")")
		_render_step += 1
		_render_wait = 0
