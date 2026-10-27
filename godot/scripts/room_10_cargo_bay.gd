class_name Room10CargoBay
extends Node3D

const SHELL_GLB_PATH := "res://../assets/glb/rooms/room_10_cargo_bay_shell.glb"
const WINNERS_GLB_DIR := "res://../assets/glb/winners"
const ROOMS_GLB_DIR := "res://../assets/glb/rooms"
const SHARED_TEX_DIR := "res://../assets/textures"

const OUT_DIRS := [
	"res://renders/rooms/room_10",
	"res://../assets/renders/rooms/room_10"
]

const PLACEMENTS := [
	{"slot": "Hero_Cargo_Drone_Gantry_West", "file": "cargo_gantry_winner_01_dual_zone_cargo_drone_dock.glb", "pos": Vector3(-3.25, 0.0, -1.65), "rot_y": 90.0, "scale": Vector3(1.0, 1.0, 1.0)},
	{"slot": "Hero_Cargo_Drone_Gantry_East", "file": "cargo_gantry_winner_01_dual_zone_cargo_drone_dock.glb", "pos": Vector3(3.25, 0.0, -1.65), "rot_y": -90.0, "scale": Vector3(1.0, 1.0, 1.0)},
	{"slot": "Center_Magnetic_Pallet_Deck", "file": "cargo_mag_pallet_deck.glb", "pos": Vector3(0.0, 0.0, -0.8), "rot_y": 0.0, "scale": Vector3(1.0, 1.0, 1.0)},
	{"slot": "Staged_Cargo_Trunk_NW", "file": "footlocker_winner_01_split_cargo_trunk.glb", "pos": Vector3(-0.7, 0.12, -1.25), "rot_y": 0.0, "scale": Vector3(1.0, 1.0, 1.0)},
	{"slot": "Staged_Cargo_Trunk_NE", "file": "footlocker_winner_01_split_cargo_trunk.glb", "pos": Vector3(0.7, 0.12, -1.25), "rot_y": 0.0, "scale": Vector3(1.0, 1.0, 1.0)},
	{"slot": "Staged_Cargo_Trunk_SW", "file": "footlocker_winner_01_split_cargo_trunk.glb", "pos": Vector3(-0.7, 0.12, -0.35), "rot_y": 180.0, "scale": Vector3(1.0, 1.0, 1.0)},
	{"slot": "Staged_Cargo_Trunk_SE", "file": "footlocker_winner_01_split_cargo_trunk.glb", "pos": Vector3(0.7, 0.12, -0.35), "rot_y": 180.0, "scale": Vector3(1.0, 1.0, 1.0)},
	{"slot": "Loadmaster_Manifest_Workstation", "file": "walldesk_winner_01_split_comms_station.glb", "pos": Vector3(3.85, 0.0, 1.85), "rot_y": -90.0, "scale": Vector3(1.0, 1.0, 1.0)},
	{"slot": "Cargo_Handler_EVA_Locker", "file": "locker_winner_01_dual_bay_bulkhead.glb", "pos": Vector3(-3.82, 0.0, 1.85), "rot_y": 90.0, "scale": Vector3(1.0, 1.0, 1.0)},
	{"slot": "Bay_Atmospheric_O2_Panel", "file": "climate_winner_01_split_env_o2_station.glb", "pos": Vector3(2.35, 0.0, 4.68), "rot_y": 180.0, "scale": Vector3(1.0, 1.0, 1.0)},
	{"slot": "South_Heavy_Cargo_Hatch", "file": "corridor_door_winner_01_dual_zone_portal.glb", "pos": Vector3(0.0, 0.0, 4.65), "rot_y": 180.0, "scale": Vector3(1.0, 1.0, 1.0)},
]

const CAMERAS := [
	{"name": "cam_01_cargo_bay_symmetrical_overview", "label": "CAM 01 — HIGH-BAY CARGO HOLD SYMMETRICAL OVERVIEW", "pos": Vector3(0.0, 2.15, 4.1), "target": Vector3(0.0, 1.3, -2.5), "fov": 58.0},
	{"name": "cam_02_west_gantry_drone_and_pallet", "label": "CAM 02 — WEST CARGO GANTRY, DRONE DOCK & PALLET", "pos": Vector3(2.35, 1.7, 0.95), "target": Vector3(-2.85, 1.25, -1.55), "fov": 52.0},
	{"name": "cam_03_east_gantry_and_loadmaster_station", "label": "CAM 03 — EAST CARGO GANTRY & LOADMASTER OFFICE", "pos": Vector3(-2.25, 1.6, -0.45), "target": Vector3(3.25, 1.25, 0.45), "fov": 52.0},
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
	_shell_container = get_node_or_null("RoomShell") as Node3D
	_fixtures_container = get_node_or_null("RoomFixtures") as Node3D
	_lights_container = get_node_or_null("RoomLighting") as Node3D

	if _shell_container == null:
		_shell_container = Node3D.new()
		_shell_container.name = "RoomShell"
		add_child(_shell_container)
	if _fixtures_container == null:
		_fixtures_container = Node3D.new()
		_fixtures_container.name = "RoomFixtures"
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

	_load_shell_and_vistas()
	_assemble_fixtures()
	_setup_lighting()
	apply_camera_preset(0)


func _load_tex(fname: String) -> Texture2D:
	if _tex_cache.has(fname):
		return _tex_cache[fname] as Texture2D
	for d: String in [SHARED_TEX_DIR, SHARED_TEX_DIR + "/cargo_round1", SHARED_TEX_DIR + "/bunk_round2"]:
		var p: String = d + "/" + fname
		if FileAccess.file_exists(p):
			var img: Image = Image.new()
			if img.load(p) == OK and not img.is_empty():
				img.generate_mipmaps()
				var tex: ImageTexture = ImageTexture.create_from_image(img)
				_tex_cache[fname] = tex
				return tex
	return null


func _load_shell_and_vistas() -> void:
	for ch: Node in _shell_container.get_children():
		ch.free()

	if FileAccess.file_exists(SHELL_GLB_PATH):
		var doc: GLTFDocument = GLTFDocument.new()
		var state: GLTFState = GLTFState.new()
		if doc.append_from_file(SHELL_GLB_PATH, state) == OK:
			var root: Node = doc.generate_scene(state)
			if root is Node3D:
				var n3d: Node3D = root as Node3D
				n3d.name = "Aegis7RoomShell"
				_shell_container.add_child(n3d)
				_upgrade_materials(n3d)

	var vmat_NorthDockingCylinderVista: StandardMaterial3D = StandardMaterial3D.new()
	var vtex_NorthDockingCylinderVista: Texture2D = _load_tex("vista_oneill_cylinder_interior.png")
	if vtex_NorthDockingCylinderVista != null:
		vmat_NorthDockingCylinderVista.albedo_texture = vtex_NorthDockingCylinderVista
		vmat_NorthDockingCylinderVista.emission_enabled = true
		vmat_NorthDockingCylinderVista.emission_texture = vtex_NorthDockingCylinderVista
		vmat_NorthDockingCylinderVista.emission_energy_multiplier = 1.35
	vmat_NorthDockingCylinderVista.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	vmat_NorthDockingCylinderVista.cull_mode = BaseMaterial3D.CULL_DISABLED
	var vmesh_NorthDockingCylinderVista: MeshInstance3D = MeshInstance3D.new()
	vmesh_NorthDockingCylinderVista.name = "NorthDockingCylinderVista"
	var vq_NorthDockingCylinderVista: QuadMesh = QuadMesh.new()
	vq_NorthDockingCylinderVista.size = Vector2(7.8, 3.6)
	vmesh_NorthDockingCylinderVista.mesh = vq_NorthDockingCylinderVista
	vmesh_NorthDockingCylinderVista.position = Vector3(0.0, 2.15, -5.65)
	vmesh_NorthDockingCylinderVista.rotation_degrees = Vector3(0.0, 0.0, 0.0)
	vmesh_NorthDockingCylinderVista.material_override = vmat_NorthDockingCylinderVista
	vmesh_NorthDockingCylinderVista.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	_shell_container.add_child(vmesh_NorthDockingCylinderVista)

	var vmat_WestFreighterDeepSpaceVista: StandardMaterial3D = StandardMaterial3D.new()
	var vtex_WestFreighterDeepSpaceVista: Texture2D = _load_tex("vista_deep_space.png")
	if vtex_WestFreighterDeepSpaceVista != null:
		vmat_WestFreighterDeepSpaceVista.albedo_texture = vtex_WestFreighterDeepSpaceVista
		vmat_WestFreighterDeepSpaceVista.emission_enabled = true
		vmat_WestFreighterDeepSpaceVista.emission_texture = vtex_WestFreighterDeepSpaceVista
		vmat_WestFreighterDeepSpaceVista.emission_energy_multiplier = 1.35
	vmat_WestFreighterDeepSpaceVista.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	vmat_WestFreighterDeepSpaceVista.cull_mode = BaseMaterial3D.CULL_DISABLED
	var vmesh_WestFreighterDeepSpaceVista: MeshInstance3D = MeshInstance3D.new()
	vmesh_WestFreighterDeepSpaceVista.name = "WestFreighterDeepSpaceVista"
	var vq_WestFreighterDeepSpaceVista: QuadMesh = QuadMesh.new()
	vq_WestFreighterDeepSpaceVista.size = Vector2(5.2, 3.2)
	vmesh_WestFreighterDeepSpaceVista.mesh = vq_WestFreighterDeepSpaceVista
	vmesh_WestFreighterDeepSpaceVista.position = Vector3(-5.15, 2.0, -1.2)
	vmesh_WestFreighterDeepSpaceVista.rotation_degrees = Vector3(0.0, 90.0, 0.0)
	vmesh_WestFreighterDeepSpaceVista.material_override = vmat_WestFreighterDeepSpaceVista
	vmesh_WestFreighterDeepSpaceVista.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	_shell_container.add_child(vmesh_WestFreighterDeepSpaceVista)



func _assemble_fixtures() -> void:
	for ch: Node in _fixtures_container.get_children():
		ch.free()

	for item: Dictionary in PLACEMENTS:
		var sname: String = String(item["slot"])
		var p1: String = WINNERS_GLB_DIR + "/" + String(item["file"])
		var p2: String = ROOMS_GLB_DIR + "/" + String(item["file"])
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
						elif mname.contains("glass") or mname.contains("translucent") or pname.contains("glass") or pname.contains("window") or pname.contains("canopy"):
							smat.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
							smat.albedo_color.a = clampf(smat.albedo_color.a, 0.18, 0.22)
							smat.roughness = 0.08
							smat.metallic = 0.10
							smat.metallic_specular = 0.90
							mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
						elif mname.contains("oled") or mname.contains("status") or mname.contains("telemetry") or mname.contains("manifest") or mname.contains("vitals") or mname.contains("synthesizer") or mname.contains("bioscrubber") or mname.contains("celestial"):
							smat.emission_enabled = true
							if smat.albedo_texture != null:
								smat.emission_texture = smat.albedo_texture
							smat.emission = Color(0.22, 0.85, 1.0)
							smat.emission_energy_multiplier = 1.60
						elif smat.emission_enabled or mname.contains("emissive") or mname.contains("led") or mname.contains("plasma"):
							smat.emission_enabled = true
							if smat.emission == Color(0, 0, 0, 1):
								smat.emission = smat.albedo_color
							smat.emission_energy_multiplier = 2.0

						mi.set_surface_override_material(s_idx, smat)
		for ch: Node in curr.get_children():
			mstack.append(ch)


func _setup_lighting() -> void:
	for ch: Node in _lights_container.get_children():
		ch.free()

	var sun: DirectionalLight3D = DirectionalLight3D.new()
	sun.name = "RoomDirectionalLight"
	sun.rotation_degrees = Vector3(-28.0, -20.0, 0.0)
	sun.light_color = Color("#C8E8FF")
	sun.light_energy = 0.9
	sun.shadow_enabled = true
	sun.shadow_bias = 0.02
	_lights_container.add_child(sun)

	_add_omni("HighBayFlood_N", Vector3(0.0, 3.45, -1.65), Color("#E0F4FF"), 1.45, 6.5)
	_add_omni("HighBayFlood_S", Vector3(0.0, 3.45, 1.85), Color("#E0F4FF"), 1.45, 6.5)
	_add_omni("WestGantryCyan", Vector3(-2.45, 1.65, -1.65), Color("#00E5FF"), 1.45, 4.8)
	_add_omni("EastGantryCyan", Vector3(2.45, 1.65, -1.65), Color("#00E5FF"), 1.45, 4.8)
	_add_omni("PalletAmber", Vector3(0.0, 0.85, -0.8), Color("#FF9500"), 1.35, 4.5)
	_add_omni("CraneAmber_S", Vector3(0.0, 2.85, 3.85), Color("#FF9500"), 1.35, 4.5)



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
		print("[Room10] All beauty camera renders complete! Exiting cleanly.")
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
					print("[Room10] Saved render: ", out_file)
		_render_step += 1
		_render_wait = 0
