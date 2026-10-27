class_name Room07CommandBridge
extends Node3D

const SHELL_GLB_PATH := "res://../assets/glb/rooms/room_07_command_bridge_shell.glb"
const WINNERS_GLB_DIR := "res://../assets/glb/winners"
const ROOMS_GLB_DIR := "res://../assets/glb/rooms"
const SHARED_TEX_DIR := "res://../assets/textures"

const OUT_DIRS := [
	"res://renders/rooms/room_07",
	"res://../assets/renders/rooms/room_07"
]

const PLACEMENTS := [
	{"slot": "Hero_Holographic_Bridge_Console", "file": "bridge_console_winner_01_dual_zone_holotable_tower.glb", "pos": Vector3(0.0, 0.0, -1.15), "rot_y": 0.0, "scale": Vector3(1.0, 1.0, 1.0)},
	{"slot": "Port_Helm_Comms_Station_NW", "file": "walldesk_winner_01_split_comms_station.glb", "pos": Vector3(-3.45, 0.0, -1.95), "rot_y": 90.0, "scale": Vector3(1.0, 1.0, 1.0)},
	{"slot": "Port_Systems_Telemetry_Desk_SW", "file": "walldesk_winner_01_split_comms_station.glb", "pos": Vector3(-3.45, 0.0, 0.85), "rot_y": 90.0, "scale": Vector3(1.0, 1.0, 1.0)},
	{"slot": "Starboard_SpinGravity_Station_NE", "file": "walldesk_winner_01_split_comms_station.glb", "pos": Vector3(3.45, 0.0, -1.95), "rot_y": -90.0, "scale": Vector3(1.0, 1.0, 1.0)},
	{"slot": "Starboard_Sector_Ops_Desk_SE", "file": "walldesk_winner_01_split_comms_station.glb", "pos": Vector3(3.45, 0.0, 0.85), "rot_y": -90.0, "scale": Vector3(1.0, 1.0, 1.0)},
	{"slot": "Bridge_Officer_EVA_Locker", "file": "locker_winner_01_dual_bay_bulkhead.glb", "pos": Vector3(3.55, 0.0, 2.85), "rot_y": -90.0, "scale": Vector3(1.0, 1.0, 1.0)},
	{"slot": "Bridge_Environmental_O2_Panel", "file": "climate_winner_01_split_env_o2_station.glb", "pos": Vector3(-3.75, 0.0, 2.85), "rot_y": 90.0, "scale": Vector3(1.0, 1.0, 1.0)},
	{"slot": "Navigation_Data_Vault", "file": "footlocker_winner_01_split_cargo_trunk.glb", "pos": Vector3(-2.25, 0.0, 3.95), "rot_y": 180.0, "scale": Vector3(1.0, 1.0, 1.0)},
	{"slot": "South_Armored_Bridge_Hatch", "file": "corridor_door_winner_01_dual_zone_portal.glb", "pos": Vector3(0.0, 0.0, 4.45), "rot_y": 180.0, "scale": Vector3(1.0, 1.0, 1.0)},
]

const CAMERAS := [
	{"name": "cam_01_bridge_command_overview", "label": "CAM 01 — COMMAND BRIDGE SYMMETRICAL OVERVIEW", "pos": Vector3(0.0, 2.05, 3.85), "target": Vector3(0.0, 1.15, -2.5), "fov": 58.0},
	{"name": "cam_02_holotable_and_port_navigation", "label": "CAM 02 — HOLOGRAPHIC CYLINDER TABLE & PORT HELM", "pos": Vector3(2.35, 1.65, 0.95), "target": Vector3(-1.65, 1.1, -1.85), "fov": 52.0},
	{"name": "cam_03_starboard_ops_and_aft_ready_bay", "label": "CAM 03 — STARBOARD TELEMETRY & AFT READY BAY", "pos": Vector3(-2.15, 1.55, -0.85), "target": Vector3(3.15, 1.15, 1.25), "fov": 52.0},
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
	for d: String in [SHARED_TEX_DIR, SHARED_TEX_DIR + "/bridge_round1", SHARED_TEX_DIR + "/bunk_round2"]:
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

	var vmat_NorthBridgeCylinderVista: StandardMaterial3D = StandardMaterial3D.new()
	var vtex_NorthBridgeCylinderVista: Texture2D = _load_tex("vista_oneill_cylinder_interior.png")
	if vtex_NorthBridgeCylinderVista != null:
		vmat_NorthBridgeCylinderVista.albedo_texture = vtex_NorthBridgeCylinderVista
		vmat_NorthBridgeCylinderVista.emission_enabled = true
		vmat_NorthBridgeCylinderVista.emission_texture = vtex_NorthBridgeCylinderVista
		vmat_NorthBridgeCylinderVista.emission_energy_multiplier = 1.35
	vmat_NorthBridgeCylinderVista.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	vmat_NorthBridgeCylinderVista.cull_mode = BaseMaterial3D.CULL_DISABLED
	var vmesh_NorthBridgeCylinderVista: MeshInstance3D = MeshInstance3D.new()
	vmesh_NorthBridgeCylinderVista.name = "NorthBridgeCylinderVista"
	var vq_NorthBridgeCylinderVista: QuadMesh = QuadMesh.new()
	vq_NorthBridgeCylinderVista.size = Vector2(8.0, 3.6)
	vmesh_NorthBridgeCylinderVista.mesh = vq_NorthBridgeCylinderVista
	vmesh_NorthBridgeCylinderVista.position = Vector3(0.0, 1.95, -5.4)
	vmesh_NorthBridgeCylinderVista.rotation_degrees = Vector3(0.0, 0.0, 0.0)
	vmesh_NorthBridgeCylinderVista.material_override = vmat_NorthBridgeCylinderVista
	vmesh_NorthBridgeCylinderVista.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	_shell_container.add_child(vmesh_NorthBridgeCylinderVista)

	var vmat_WestBridgeDeepSpaceVista: StandardMaterial3D = StandardMaterial3D.new()
	var vtex_WestBridgeDeepSpaceVista: Texture2D = _load_tex("vista_deep_space.png")
	if vtex_WestBridgeDeepSpaceVista != null:
		vmat_WestBridgeDeepSpaceVista.albedo_texture = vtex_WestBridgeDeepSpaceVista
		vmat_WestBridgeDeepSpaceVista.emission_enabled = true
		vmat_WestBridgeDeepSpaceVista.emission_texture = vtex_WestBridgeDeepSpaceVista
		vmat_WestBridgeDeepSpaceVista.emission_energy_multiplier = 1.35
	vmat_WestBridgeDeepSpaceVista.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	vmat_WestBridgeDeepSpaceVista.cull_mode = BaseMaterial3D.CULL_DISABLED
	var vmesh_WestBridgeDeepSpaceVista: MeshInstance3D = MeshInstance3D.new()
	vmesh_WestBridgeDeepSpaceVista.name = "WestBridgeDeepSpaceVista"
	var vq_WestBridgeDeepSpaceVista: QuadMesh = QuadMesh.new()
	vq_WestBridgeDeepSpaceVista.size = Vector2(5.5, 3.2)
	vmesh_WestBridgeDeepSpaceVista.mesh = vq_WestBridgeDeepSpaceVista
	vmesh_WestBridgeDeepSpaceVista.position = Vector3(-4.85, 1.85, -1.0)
	vmesh_WestBridgeDeepSpaceVista.rotation_degrees = Vector3(0.0, 90.0, 0.0)
	vmesh_WestBridgeDeepSpaceVista.material_override = vmat_WestBridgeDeepSpaceVista
	vmesh_WestBridgeDeepSpaceVista.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	_shell_container.add_child(vmesh_WestBridgeDeepSpaceVista)



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
	sun.rotation_degrees = Vector3(-26.0, -24.0, 0.0)
	sun.light_color = Color("#C4E8FF")
	sun.light_energy = 0.9
	sun.shadow_enabled = true
	sun.shadow_bias = 0.02
	_lights_container.add_child(sun)

	_add_omni("CenterHologramCyan", Vector3(0.0, 1.85, -1.15), Color("#00E5FF"), 1.75, 5.5)
	_add_omni("PortWingTask", Vector3(-2.65, 2.15, -0.55), Color("#E0F4FF"), 1.25, 4.5)
	_add_omni("StarboardWingTask", Vector3(2.65, 2.15, -0.55), Color("#E0F4FF"), 1.25, 4.5)
	_add_omni("AftTacticalAmber", Vector3(0.0, 2.55, 3.45), Color("#FF9500"), 1.25, 4.2)



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
		print("[Room07] All beauty camera renders complete! Exiting cleanly.")
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
					print("[Room07] Saved render: ", out_file)
		_render_step += 1
		_render_wait = 0
