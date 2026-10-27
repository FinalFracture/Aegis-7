class_name DeskRound1Showcase
extends Node3D
## DeskRound1Showcase for Cylinder Hab-7 (Sci-Fi Crew Desk / Telemetry Workstation — 5 Candidates)
## Imports res://../assets/glb/desk_round1/desk_r1_01.glb .. desk_r1_05.glb
## Supports:
## - True alpha-translucent holo visors, glass work surfaces, and viewport windows (TRANSPARENCY_ALPHA)
## - Switchable exterior_view_mode ("space" vs "cylinder") with NO opaque wall blocking 05_viewport_study_nook's cutout
## - Interactive inspection (keys 1-5, V to toggle vista, Space for turntable) & batch rendering (--render-all)

const EXT_GLB_DIR := "res://../assets/glb/desk_round1"
const RES_GLB_DIR := "res://../assets/glb/desk_round1"
const EXT_TEX_DIR := "res://../assets/textures/bunk_round2"
const SHARED_TEX_DIR := "res://../assets/textures"

const OUT_DIRS := [
	"res://renders/desk_round1",
	"res://../assets/renders/desk_round1"
]

@export_enum("space", "cylinder") var exterior_view_mode: String = "space"

const CANDIDATES := [
	{
		"index": 1,
		"id": "desk_r1_01",
		"slug": "01_wall_cantilever_console",
		"title": "01 — Wall-Mounted Cantilever Holo-Console",
		"has_hull_window": false,
		"default_vista": "space",
		"cam_pos": Vector3(1.55, 1.48, 2.22),
		"cam_target": Vector3(0.0, 0.88, -0.05),
		"fov": 44.0
	},
	{
		"index": 2,
		"id": "desk_r1_02",
		"slug": "02_wraparound_command_station",
		"title": "02 — Wraparound Command Telemetry Station",
		"has_hull_window": false,
		"default_vista": "space",
		"cam_pos": Vector3(1.75, 1.56, 2.45),
		"cam_target": Vector3(0.0, 0.84, 0.0),
		"fov": 45.0
	},
	{
		"index": 3,
		"id": "desk_r1_03",
		"slug": "03_floating_mag_desk",
		"title": "03 — Floating Mag-Lev Glass Workstation",
		"has_hull_window": false,
		"default_vista": "space",
		"cam_pos": Vector3(1.52, 1.38, 2.18),
		"cam_target": Vector3(0.0, 0.72, 0.05),
		"fov": 44.0
	},
	{
		"index": 4,
		"id": "desk_r1_04",
		"slug": "04_engineering_workbench",
		"title": "04 — Heavy Gunmetal Engineering Workbench",
		"has_hull_window": false,
		"default_vista": "space",
		"cam_pos": Vector3(1.62, 1.52, 2.32),
		"cam_target": Vector3(0.0, 0.92, -0.02),
		"fov": 44.0
	},
	{
		"index": 5,
		"id": "desk_r1_05",
		"slug": "05_viewport_study_nook",
		"title": "05 — Translucent Viewport Study Alcove Nook",
		"has_hull_window": true,
		"default_vista": "cylinder",
		"cam_pos": Vector3(1.68, 1.56, 2.42),
		"cam_target": Vector3(0.0, 0.98, -0.05),
		"fov": 44.0
	}
]

var _stage_container: Node3D
var _model_holder: Node3D
var _lights_container: Node3D
var _backwall_mi: MeshInstance3D
var _vista_plane: MeshInstance3D
var _camera: Camera3D

var _tex_cache: Dictionary = {}
var current_index: int = 0
var turntable_spinning: bool = false

var _batch_render: bool = false
var _validate_only: bool = false
var _frame_counter: int = 0
var _render_step: int = 0
var _render_wait: int = 0


func _ready() -> void:
	_camera = get_node_or_null("ShowcaseCamera") as Camera3D
	_stage_container = get_node_or_null("ShowcaseStage") as Node3D
	_model_holder = get_node_or_null("CandidateHolder") as Node3D
	_lights_container = get_node_or_null("ArchetypeLights") as Node3D

	if _stage_container == null:
		_stage_container = Node3D.new()
		_stage_container.name = "ShowcaseStage"
		add_child(_stage_container)
	if _model_holder == null:
		_model_holder = Node3D.new()
		_model_holder.name = "CandidateHolder"
		add_child(_model_holder)
	if _lights_container == null:
		_lights_container = Node3D.new()
		_lights_container.name = "ArchetypeLights"
		add_child(_lights_container)

	var all_args: PackedStringArray = OS.get_cmdline_args() + OS.get_cmdline_user_args()
	for i: int in range(all_args.size()):
		var arg: String = all_args[i]
		if arg == "--render-all" or arg == "--capture-screenshots" or arg == "--screenshots":
			_batch_render = true
		elif arg == "--validate-only" or arg == "--validate":
			_validate_only = true
		elif arg == "--view-mode" and i + 1 < all_args.size():
			exterior_view_mode = all_args[i + 1]

	if DisplayServer.get_name() == "headless" and not _batch_render:
		_validate_only = true

	_build_showcase_stage()
	show_candidate(0)


func _load_tex(fname: String) -> Texture2D:
	if _tex_cache.has(fname):
		return _tex_cache[fname] as Texture2D
	for dir_p: String in [EXT_TEX_DIR, SHARED_TEX_DIR]:
		var full: String = dir_p + "/" + fname
		if FileAccess.file_exists(full):
			var img: Image = Image.new()
			if img.load(full) == OK and not img.is_empty():
				img.generate_mipmaps()
				var tex: ImageTexture = ImageTexture.create_from_image(img)
				_tex_cache[fname] = tex
				return tex
	return null


func _build_showcase_stage() -> void:
	for ch: Node in _stage_container.get_children():
		ch.free()

	# 1. Dark Metallic Composite Deck Floor (#282E38)
	var floor_mi: MeshInstance3D = MeshInstance3D.new()
	floor_mi.name = "SpacecraftDeckFloor"
	var fbox: BoxMesh = BoxMesh.new()
	fbox.size = Vector3(12.0, 0.08, 10.0)
	floor_mi.mesh = fbox
	floor_mi.position = Vector3(0.0, -0.04, 0.0)
	var fmat: StandardMaterial3D = StandardMaterial3D.new()
	fmat.albedo_color = Color("#282E38")
	fmat.roughness = 0.38
	fmat.metallic = 0.55
	floor_mi.material_override = fmat
	_stage_container.add_child(floor_mi)

	# 2. Dark Gunmetal Bulkhead Backwall (#1A1E24) — automatically hidden for 05_viewport_study_nook so no opaque wall blocks its window!
	_backwall_mi = MeshInstance3D.new()
	_backwall_mi.name = "SpacecraftBulkheadWall"
	var wbox: BoxMesh = BoxMesh.new()
	wbox.size = Vector3(11.0, 5.5, 0.12)
	_backwall_mi.mesh = wbox
	_backwall_mi.position = Vector3(0.0, 2.70, -0.92)
	var wmat: StandardMaterial3D = StandardMaterial3D.new()
	wmat.albedo_color = Color("#1A1E24")
	wmat.roughness = 0.42
	wmat.metallic = 0.65
	_backwall_mi.material_override = wmat
	_stage_container.add_child(_backwall_mi)

	# 3. Left Wing Gunmetal Bulkhead Return (#161A20)
	var left_wall_mi: MeshInstance3D = MeshInstance3D.new()
	left_wall_mi.name = "SpacecraftLeftReturnBulkhead"
	var lwbox: BoxMesh = BoxMesh.new()
	lwbox.size = Vector3(0.12, 5.5, 9.0)
	left_wall_mi.mesh = lwbox
	left_wall_mi.position = Vector3(-3.20, 2.70, 2.0)
	var lwmat: StandardMaterial3D = StandardMaterial3D.new()
	lwmat.albedo_color = Color("#161A20")
	lwmat.roughness = 0.44
	lwmat.metallic = 0.65
	left_wall_mi.material_override = lwmat
	_stage_container.add_child(left_wall_mi)

	# 4. Exterior Vista Backdrop Plane (visible behind 05_viewport_study_nook's open translucent window cutout)
	_vista_plane = MeshInstance3D.new()
	_vista_plane.name = "ExteriorVistaPlane"
	var qmesh: QuadMesh = QuadMesh.new()
	qmesh.size = Vector2(1.18, 0.78)
	_vista_plane.mesh = qmesh
	_vista_plane.position = Vector3(0.0, 1.32, -0.56)
	_vista_plane.visible = false
	_stage_container.add_child(_vista_plane)
	_update_vista_material()


func set_exterior_view_mode(mode: String) -> void:
	exterior_view_mode = "cylinder" if mode == "cylinder" else "space"
	_update_vista_material()
	print("[DeskShowcase] Switched exterior_view_mode to: ", exterior_view_mode)


func _update_vista_material() -> void:
	var tex_name: String = "vista_oneill_cylinder_interior.png" if exterior_view_mode == "cylinder" else "vista_deep_space.png"
	var vtex: Texture2D = _load_tex(tex_name)
	var vmat: StandardMaterial3D = StandardMaterial3D.new()
	if vtex != null:
		vmat.albedo_texture = vtex
		vmat.emission_enabled = true
		vmat.emission_texture = vtex
		vmat.emission_energy_multiplier = 1.25
	vmat.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	vmat.cull_mode = BaseMaterial3D.CULL_DISABLED
	if _vista_plane != null:
		_vista_plane.material_override = vmat


func show_candidate(idx: int) -> void:
	if idx < 0 or idx >= CANDIDATES.size():
		return
	current_index = idx
	var info: Dictionary = CANDIDATES[idx]
	var cid: String = String(info["id"])
	var ctitle: String = String(info["title"])
	var has_win: bool = bool(info["has_hull_window"])

	exterior_view_mode = String(info.get("default_vista", "space"))
	_update_vista_material()

	if _vista_plane != null:
		_vista_plane.visible = has_win
	if _backwall_mi != null:
		# Never block the open viewport cutout on 05_viewport_study_nook
		_backwall_mi.visible = not has_win

	for ch: Node in _model_holder.get_children():
		ch.free()

	var node: Node3D = _load_desk_glb(cid)
	if node != null:
		_model_holder.add_child(node)
		_convert_and_upgrade_meshes(node, cid)
		print("[DeskShowcase] Loaded ", cid, " (", ctitle, ") | hull_window=", has_win, " vista=", exterior_view_mode)
	else:
		print("[DeskShowcase] Desk GLB not found: ", cid)

	_apply_desk_lighting_rig(idx + 1)
	if _camera != null:
		_camera.global_position = info["cam_pos"] as Vector3
		_camera.fov = float(info["fov"])
		_camera.look_at(info["cam_target"] as Vector3, Vector3.UP)


func _load_desk_glb(cid: String) -> Node3D:
	var ext_path: String = EXT_GLB_DIR + "/" + cid + ".glb"
	var res_path: String = RES_GLB_DIR + "/" + cid + ".glb"

	if FileAccess.file_exists(ext_path):
		var doc: GLTFDocument = GLTFDocument.new()
		var state: GLTFState = GLTFState.new()
		if doc.append_from_file(ext_path, state) == OK:
			var root: Node = doc.generate_scene(state)
			if root is Node3D:
				return root as Node3D

	if ResourceLoader.exists(res_path):
		var packed: Resource = ResourceLoader.load(res_path)
		if packed is PackedScene:
			var inst: Node = (packed as PackedScene).instantiate()
			if inst is Node3D:
				return inst as Node3D

	return null


func _convert_and_upgrade_meshes(root: Node3D, _cid: String) -> void:
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

						if mname.contains("holovisor") or pname.contains("holoscreen") or pname.contains("holoarc") or pname.contains("visor"):
							smat.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
							var holo_tex: Texture2D = _load_tex("glass_holo_visor_cyan.png")
							if holo_tex != null:
								smat.albedo_texture = holo_tex
								smat.emission_texture = holo_tex
							smat.albedo_color = Color(1.0, 1.0, 1.0, 0.34)
							smat.emission_enabled = true
							smat.emission = Color("#00E5FF")
							smat.emission_energy_multiplier = 0.85
							smat.roughness = 0.08
							smat.metallic = 0.15
							mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
						elif mname.contains("viewport_glass") or pname.contains("glasstop") or pname.contains("hullwindow"):
							smat.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
							var vp_tex: Texture2D = _load_tex("glass_viewport_translucent.png")
							if vp_tex != null:
								smat.albedo_texture = vp_tex
							smat.albedo_color = Color(0.85, 0.95, 1.0, 0.26)
							smat.roughness = 0.08
							smat.metallic = 0.20
							mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
						elif mname.contains("oled") or pname.contains("oled") or pname.contains("monitor"):
							var oled_tex: Texture2D = _load_tex("oled_telemetry_hud.png")
							if oled_tex != null:
								smat.albedo_texture = oled_tex
								smat.emission_texture = oled_tex
							smat.emission_enabled = true
							smat.emission = Color(0.20, 0.85, 1.0)
							smat.emission_energy_multiplier = 1.45
						elif smat.emission_enabled or mname.contains("emissive") or mname.contains("led") or pname.contains("led") or pname.contains("strip") or pname.contains("inductionring") or pname.contains("scannerlight"):
							smat.emission_enabled = true
							if smat.emission == Color(0, 0, 0, 1):
								smat.emission = smat.albedo_color
							smat.emission_energy_multiplier = 2.0

						mi.set_surface_override_material(s_idx, smat)
		for ch: Node in curr.get_children():
			mstack.append(ch)


func _apply_desk_lighting_rig(idx_1_based: int) -> void:
	for ch: Node in _lights_container.get_children():
		ch.free()

	var key: DirectionalLight3D = DirectionalLight3D.new()
	key.name = "KeyLight"
	key.shadow_enabled = true
	key.shadow_bias = 0.02
	key.light_color = Color("#E8F2FF")
	key.light_energy = 1.20
	key.position = Vector3(2.2, 2.6, 2.5)
	_lights_container.add_child(key)
	key.look_at(Vector3(0.0, 0.85, 0.0), Vector3.UP)

	var fill: OmniLight3D = OmniLight3D.new()
	fill.name = "FillLight"
	fill.position = Vector3(-2.3, 1.5, 2.1)
	fill.light_color = Color("#6898D0")
	fill.light_energy = 0.48
	fill.omni_range = 7.0
	_lights_container.add_child(fill)

	var rim: OmniLight3D = OmniLight3D.new()
	rim.name = "RimLight"
	rim.position = Vector3(-1.4, 2.5, -1.5)
	rim.light_color = Color("#98D8FF")
	rim.light_energy = 0.85
	rim.omni_range = 6.0
	_lights_container.add_child(rim)

	match idx_1_based:
		1:
			# 01_wall_cantilever_console: Curved Holo Emitter Cyan + Underglow
			_add_omni("HoloArcCyanGlow", Vector3(0.0, 1.25, -0.05), Color("#00E5FF"), 1.55, 2.5)
			_add_omni("CantileverUnderglow", Vector3(0.0, 0.65, 0.25), Color("#00E5FF"), 0.85, 1.8)
		2:
			# 02_wraparound_command_station: Triple OLED Cyan + Amber Under-Edge
			_add_omni("WraparoundCyanHUD", Vector3(0.0, 1.20, 0.0), Color("#00E5FF"), 1.55, 2.6)
			_add_omni("WraparoundAmberUnder", Vector3(0.0, 0.65, -0.35), Color("#FF9500"), 1.10, 2.2)
		3:
			# 03_floating_mag_desk: Twin Mag-Lev Pylon Cyan Rings + Translucent Glass Glow
			_add_omni("MagPylonLeftCyan", Vector3(-0.62, 0.55, -0.05), Color("#00E5FF"), 1.45, 2.2)
			_add_omni("MagPylonRightCyan", Vector3(0.62, 0.55, -0.05), Color("#00E5FF"), 1.45, 2.2)
		4:
			# 04_engineering_workbench: Articulated Scanner Ice-White Spot + Amber Gantry Strip
			_add_omni("ScannerTaskLight", Vector3(-0.10, 1.25, 0.15), Color("#E6F4FF"), 1.55, 2.4)
			_add_omni("GantryAmberStrip", Vector3(0.0, 1.75, -0.25), Color("#FF9500"), 1.35, 2.4)
		5:
			# 05_viewport_study_nook: Translucent Viewport Cyan Rim + Overhead Amber Task Strip
			_add_omni("ViewportCyanGlow", Vector3(0.0, 1.32, -0.32), Color("#00E5FF"), 1.55, 2.6)
			_add_omni("NookAmberTaskStrip", Vector3(0.0, 1.98, 0.15), Color("#FF9500"), 1.35, 2.4)


func _add_omni(lname: String, pos: Vector3, col: Color, energy: float, rng: float) -> OmniLight3D:
	var omni: OmniLight3D = OmniLight3D.new()
	omni.name = lname
	omni.position = pos
	omni.light_color = col
	omni.light_energy = energy
	omni.omni_range = rng
	_lights_container.add_child(omni)
	return omni


func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventKey:
		var ke: InputEventKey = event as InputEventKey
		if ke.pressed and not ke.echo:
			match ke.keycode:
				KEY_1: show_candidate(0)
				KEY_2: show_candidate(1)
				KEY_3: show_candidate(2)
				KEY_4: show_candidate(3)
				KEY_5: show_candidate(4)
				KEY_RIGHT: show_candidate((current_index + 1) % CANDIDATES.size())
				KEY_LEFT: show_candidate((current_index - 1 + CANDIDATES.size()) % CANDIDATES.size())
				KEY_V: set_exterior_view_mode("cylinder" if exterior_view_mode == "space" else "space")
				KEY_SPACE: turntable_spinning = not turntable_spinning


func _process(delta: float) -> void:
	_frame_counter += 1

	if _batch_render:
		_process_batch_render()
		return

	if _validate_only:
		if _frame_counter >= 4:
			print("[DeskShowcase] Headless validation complete. Exiting cleanly.")
			get_tree().quit(0)
		return

	if turntable_spinning and _model_holder != null:
		_model_holder.rotate_y(0.45 * delta)


func _process_batch_render() -> void:
	if DisplayServer.get_name() == "headless":
		print("[DeskShowcase] Cannot capture viewport images under headless DisplayServer.")
		get_tree().quit(0)
		return

	if _frame_counter < 6:
		return

	if _render_step >= CANDIDATES.size():
		print("[DeskShowcase] All 5 Sci-Fi Crew Desk beauty renders complete! Exiting cleanly.")
		get_tree().quit(0)
		return

	if _render_wait == 0:
		show_candidate(_render_step)
		_render_wait = 1
		return

	_render_wait += 1
	if _render_wait >= 6:
		var info: Dictionary = CANDIDATES[_render_step]
		var cid: String = String(info["id"])
		var img: Image = get_viewport().get_texture().get_image()
		if img != null and not img.is_empty():
			for d: String in OUT_DIRS:
				DirAccess.make_dir_recursive_absolute(d)
				var out_file: String = d + "/" + cid + ".png"
				if img.save_png(out_file) == OK:
					print("[DeskShowcase] Saved render: ", out_file, " (", img.get_width(), "x", img.get_height(), ")")
		_render_step += 1
		_render_wait = 0
