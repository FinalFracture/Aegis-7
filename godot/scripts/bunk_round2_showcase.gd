class_name BunkRound2Showcase
extends Node3D
## BunkRound2Showcase for Cylinder Hab-7 (Round 2 Bunk Pods + 4 Locked Bunk Winners)
## Supports:
## - True alpha-translucent windows (BaseMaterial3D.TRANSPARENCY_ALPHA) with NO opaque wall blocking viewport cutouts
## - Switchable exterior_view_mode ("space" -> vista_deep_space.png vs "cylinder" -> vista_oneill_cylinder_interior.png)
##   via V key or --view-mode space|cylinder CLI argument
## - All 10 Round 2 candidates (bunk_r2_01..10.glb) + the 4 Locked Winners (bunk_winner_01..04.glb)

const EXT_GLB_R2_DIR := "res://../assets/glb/bunk_round2"
const EXT_GLB_WINNERS_DIR := "res://../assets/glb/winners"
const EXT_TEX_R2_DIR := "res://../assets/textures/bunk_round2"
const SHARED_TEX_DIR := "res://../assets/textures"
const SPEC_R2_PATH := "res://../design/bunk_round2/bunk_r2_spec.md"

const OUT_DIRS := [
	"res://renders/bunk_round2",
	"res://../assets/renders/bunk_round2"
]

@export_enum("space", "cylinder") var exterior_view_mode: String = "space"

const CANDIDATES := [
	{
		"index": 1,
		"id": "bunk_r2_01",
		"slug": "01_panoramic_hull_blister_pod",
		"title": "01 — Curved Bubble-Glass Hull Blister Berth",
		"default_vista": "space",
		"cam_pos": Vector3(1.76, 1.58, 2.48),
		"cam_target": Vector3(0.0, 0.90, -0.05)
	},
	{
		"index": 2,
		"id": "bunk_r2_02",
		"slug": "02_hex_aperture_sleep_chamber",
		"title": "02 — Deep Hexagonal Aperture Pod",
		"default_vista": "cylinder",
		"cam_pos": Vector3(1.82, 1.60, 2.55),
		"cam_target": Vector3(0.0, 0.92, -0.05)
	},
	{
		"index": 3,
		"id": "bunk_r2_03",
		"slug": "03_corvette_submarine_rack",
		"title": "03 — Torpedo-Bay Style Recessed Rack",
		"default_vista": "space",
		"cam_pos": Vector3(1.76, 1.56, 2.48),
		"cam_target": Vector3(0.0, 0.88, -0.05)
	},
	{
		"index": 4,
		"id": "bunk_r2_04",
		"slug": "04_sliding_canopy_cockpit_pod",
		"title": "04 — Fighter-Canopy Gullwing Sleep Pod",
		"default_vista": "space",
		"cam_pos": Vector3(1.76, 1.56, 2.48),
		"cam_target": Vector3(0.0, 0.86, -0.05)
	},
	{
		"index": 5,
		"id": "bunk_r2_05",
		"slug": "05_corner_l_viewport_berth",
		"title": "05 — Dual-Window Corner Observation Bunk",
		"default_vista": "cylinder",
		"cam_pos": Vector3(1.80, 1.58, 2.50),
		"cam_target": Vector3(0.0, 0.90, -0.05)
	},
	{
		"index": 6,
		"id": "bunk_r2_06",
		"slug": "06_suspended_gyro_cradle",
		"title": "06 — Gimbaled Centrifuge Sleep Cradle",
		"default_vista": "space",
		"cam_pos": Vector3(1.82, 1.60, 2.58),
		"cam_target": Vector3(0.0, 0.90, -0.05)
	},
	{
		"index": 7,
		"id": "bunk_r2_07",
		"slug": "07_medical_biomonitor_pod",
		"title": "07 — High-Tech Med/Cryo Diagnostic Berth (Winner #2)",
		"default_vista": "space",
		"cam_pos": Vector3(1.76, 1.58, 2.48),
		"cam_target": Vector3(0.0, 0.88, -0.05)
	},
	{
		"index": 8,
		"id": "bunk_r2_08",
		"slug": "08_modular_hex_hive_stack",
		"title": "08 — Twin Offset Honeycomb Crew Pods (Winner #3)",
		"default_vista": "cylinder",
		"cam_pos": Vector3(1.86, 1.68, 2.65),
		"cam_target": Vector3(0.0, 0.98, -0.05)
	},
	{
		"index": 9,
		"id": "bunk_r2_09",
		"slug": "09_observation_lounge_sleeper",
		"title": "09 — Split-Level Daybed & Stargazer Pod (Winner #4)",
		"default_vista": "space",
		"cam_pos": Vector3(1.78, 1.58, 2.50),
		"cam_target": Vector3(0.0, 0.90, -0.05)
	},
	{
		"index": 10,
		"id": "bunk_r2_10",
		"slug": "10_captain_bridge_alcove",
		"title": "10 — Command Deck Observation Berth",
		"default_vista": "cylinder",
		"cam_pos": Vector3(1.82, 1.62, 2.56),
		"cam_target": Vector3(0.0, 0.92, -0.05)
	}
]

const WINNERS := [
	"bunk_winner_01_orbital_viewport",
	"bunk_winner_02_medical_biomonitor",
	"bunk_winner_03_hex_hive_stack",
	"bunk_winner_04_observation_lounge"
]

var _stage_container: Node3D
var _model_holder: Node3D
var _lights_container: Node3D
var _vista_plane: MeshInstance3D
var _side_vista_plane: MeshInstance3D
var _camera: Camera3D

var _tex_cache: Dictionary = {}
var current_index: int = 0
var turntable_spinning: bool = false
var _validate_only: bool = false
var _frame_counter: int = 0


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
		if arg == "--validate-only" or arg == "--validate":
			_validate_only = true
		elif arg == "--view-mode" and i + 1 < all_args.size():
			exterior_view_mode = all_args[i + 1]

	if DisplayServer.get_name() == "headless":
		_validate_only = true

	_build_open_vista_stage()
	show_candidate(0)


func _load_tex(fname: String) -> Texture2D:
	if _tex_cache.has(fname):
		return _tex_cache[fname] as Texture2D
	for dir_p: String in [EXT_TEX_R2_DIR, SHARED_TEX_DIR]:
		var full: String = dir_p + "/" + fname
		if FileAccess.file_exists(full):
			var img: Image = Image.new()
			if img.load(full) == OK and not img.is_empty():
				img.generate_mipmaps()
				var tex: ImageTexture = ImageTexture.create_from_image(img)
				_tex_cache[fname] = tex
				return tex
	return null


## Builds the dark metallic composite deck floor (#282E38) and the unshaded exterior vista backdrop plane
## directly behind the open viewport cutout (with NO opaque backwall blocking the window!).
func _build_open_vista_stage() -> void:
	for ch: Node in _stage_container.get_children():
		ch.free()

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

	_vista_plane = MeshInstance3D.new()
	_vista_plane.name = "ExteriorVistaPlane"
	var qmesh: QuadMesh = QuadMesh.new()
	qmesh.size = Vector2(3.8, 2.5)
	_vista_plane.mesh = qmesh
	_vista_plane.position = Vector3(0.0, 1.25, -0.92)
	_stage_container.add_child(_vista_plane)

	_side_vista_plane = MeshInstance3D.new()
	_side_vista_plane.name = "SideExteriorVistaPlane"
	var sqmesh: QuadMesh = QuadMesh.new()
	sqmesh.size = Vector2(2.0, 2.2)
	_side_vista_plane.mesh = sqmesh
	_side_vista_plane.position = Vector3(-1.35, 1.20, 0.0)
	_side_vista_plane.rotation_degrees = Vector3(0.0, 90.0, 0.0)
	_side_vista_plane.visible = false
	_stage_container.add_child(_side_vista_plane)

	_update_vista_material()


func set_exterior_view_mode(mode: String) -> void:
	exterior_view_mode = "cylinder" if mode == "cylinder" else "space"
	_update_vista_material()
	print("[BunkRound2Showcase] Switched exterior_view_mode to: ", exterior_view_mode)


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
	if _side_vista_plane != null:
		_side_vista_plane.material_override = vmat


func show_candidate(idx: int) -> void:
	if idx < 0 or idx >= CANDIDATES.size():
		return
	current_index = idx
	var info: Dictionary = CANDIDATES[idx]
	var cid: String = String(info["id"])
	exterior_view_mode = String(info.get("default_vista", "space"))
	_update_vista_material()
	if _side_vista_plane != null:
		_side_vista_plane.visible = (cid == "bunk_r2_05")

	for ch: Node in _model_holder.get_children():
		ch.free()

	var node: Node3D = _load_glb_from_path(EXT_GLB_R2_DIR + "/" + cid + ".glb")
	if node != null:
		_model_holder.add_child(node)
		_upgrade_translucent_and_pbr_materials(node)
		print("[BunkRound2Showcase] Loaded ", cid, " | vista=", exterior_view_mode)

	_setup_lights(idx + 1)
	if _camera != null:
		_camera.global_position = info["cam_pos"] as Vector3
		_camera.look_at(info["cam_target"] as Vector3, Vector3.UP)


func show_winner(winner_index_0_to_3: int) -> void:
	if winner_index_0_to_3 < 0 or winner_index_0_to_3 >= WINNERS.size():
		return
	var wid: String = WINNERS[winner_index_0_to_3]
	for ch: Node in _model_holder.get_children():
		ch.free()
	var node: Node3D = _load_glb_from_path(EXT_GLB_WINNERS_DIR + "/" + wid + ".glb")
	if node != null:
		_model_holder.add_child(node)
		_upgrade_translucent_and_pbr_materials(node)
		print("[BunkRound2Showcase] Loaded Locked Winner: ", wid, " | vista=", exterior_view_mode)


func _load_glb_from_path(abs_path: String) -> Node3D:
	if FileAccess.file_exists(abs_path):
		var doc: GLTFDocument = GLTFDocument.new()
		var state: GLTFState = GLTFState.new()
		if doc.append_from_file(abs_path, state) == OK:
			var root: Node = doc.generate_scene(state)
			if root is Node3D:
				return root as Node3D
	return null


func _upgrade_translucent_and_pbr_materials(root: Node3D) -> void:
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
				for s_idx: int in range(mi.mesh.get_surface_count()):
					var mat: Material = mi.get_active_material(s_idx)
					if mat is StandardMaterial3D:
						var smat: StandardMaterial3D = (mat as StandardMaterial3D).duplicate() as StandardMaterial3D
						var mname: String = smat.resource_name.to_lower()
						var pname: String = mi.name.to_lower()
						smat.cull_mode = BaseMaterial3D.CULL_DISABLED
						if mname.contains("glass") or mname.contains("translucent") or mname.contains("visor") or pname.contains("glass") or pname.contains("window") or pname.contains("canopy") or pname.contains("visor"):
							smat.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
							smat.albedo_color.a = clampf(smat.albedo_color.a, 0.18, 0.28)
							smat.roughness = 0.08
							smat.metallic = 0.15
							mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
						mi.set_surface_override_material(s_idx, smat)
		for ch: Node in curr.get_children():
			mstack.append(ch)


func _setup_lights(_idx_1: int) -> void:
	for ch: Node in _lights_container.get_children():
		ch.free()
	var key: DirectionalLight3D = DirectionalLight3D.new()
	key.light_color = Color("#E8F2FF")
	key.light_energy = 1.20
	key.shadow_enabled = true
	key.position = Vector3(2.3, 2.6, 2.5)
	_lights_container.add_child(key)
	key.look_at(Vector3(0.0, 0.9, 0.0), Vector3.UP)

	var cyan_strip: OmniLight3D = OmniLight3D.new()
	cyan_strip.position = Vector3(0.0, 1.55, 0.05)
	cyan_strip.light_color = Color("#00E5FF")
	cyan_strip.light_energy = 1.50
	cyan_strip.omni_range = 2.6
	_lights_container.add_child(cyan_strip)


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
				KEY_6: show_candidate(5)
				KEY_7: show_candidate(6)
				KEY_8: show_candidate(7)
				KEY_9: show_candidate(8)
				KEY_0: show_candidate(9)
				KEY_V: set_exterior_view_mode("cylinder" if exterior_view_mode == "space" else "space")
				KEY_SPACE: turntable_spinning = not turntable_spinning


func _process(delta: float) -> void:
	_frame_counter += 1
	if _validate_only and _frame_counter >= 4:
		print("[BunkRound2Showcase] Headless validation complete. Exiting cleanly.")
		get_tree().quit(0)
		return
	if turntable_spinning and _model_holder != null:
		_model_holder.rotate_y(0.45 * delta)
