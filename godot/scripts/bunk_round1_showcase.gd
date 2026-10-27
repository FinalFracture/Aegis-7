class_name BunkRound1Showcase
extends Node3D
## BunkRound1Showcase for Cylinder Hab-7 Prop Variation Tournament (Round 1: Hard Sci-Fi Bunk Pods)
## Loads bunk_r1_01.glb .. bunk_r1_10.glb from res://../assets/glb/bunk_round1/,
## binds clean, low-noise Hard Sci-Fi PBR textures from res://../assets/textures/bunk_round1/,
## places each pod in a sleek dark gunmetal spacecraft bay (#1A1E24 bulkhead plating, #282E38 metallic decking),
## and applies dramatic hard sci-fi lighting rigs (cool-white key/rim + cyan #00E5FF & amber #FF9500 LED accents).

const EXT_GLB_DIR := "res://../assets/glb/bunk_round1"
const RES_GLB_DIR := "res://../assets/glb/bunk_round1"
const EXT_TEX_DIR := "res://../assets/textures/bunk_round1"
const FALLBACK_TEX_DIR := "res://../assets/textures"
const SPEC_PATH := "res://../design/bunk_round1/bunk_r1_spec.md"

const OUT_DIRS := [
	"res://renders/bunk_round1",
	"res://../assets/renders/bunk_round1"
]

const CANDIDATES := [
	{
		"index": 1,
		"id": "bunk_r1_01",
		"slug": "01_aerospace_cryo_berth",
		"title": "01 — Molded White Aerospace Sleep Capsule",
		"cam_pos": Vector3(1.75, 1.56, 2.48),
		"cam_target": Vector3(0.0, 0.88, -0.05),
		"fov": 43.0
	},
	{
		"index": 2,
		"id": "bunk_r1_02",
		"slug": "02_expanse_bulkhead_rack",
		"title": "02 — High-G Armored Bulkhead Berth",
		"cam_pos": Vector3(1.78, 1.60, 2.52),
		"cam_target": Vector3(0.0, 0.90, -0.05),
		"fov": 43.0
	},
	{
		"index": 3,
		"id": "bunk_r1_03",
		"slug": "03_zero_g_mag_couchette",
		"title": "03 — Cantilevered Mag-Lock Orbital Pod",
		"cam_pos": Vector3(1.72, 1.54, 2.44),
		"cam_target": Vector3(0.0, 0.84, -0.05),
		"fov": 43.0
	},
	{
		"index": 4,
		"id": "bunk_r1_04",
		"slug": "04_blast_shutter_pod",
		"title": "04 — Armored Blast-Shutter Crew Pod",
		"cam_pos": Vector3(1.74, 1.54, 2.48),
		"cam_target": Vector3(0.0, 0.86, -0.05),
		"fov": 43.0
	},
	{
		"index": 5,
		"id": "bunk_r1_05",
		"slug": "05_spin_transition_harness_bunk",
		"title": "05 — Zero-G / Spin-Gravity Restraint Pod",
		"cam_pos": Vector3(1.75, 1.56, 2.48),
		"cam_target": Vector3(0.0, 0.88, -0.05),
		"fov": 43.0
	},
	{
		"index": 6,
		"id": "bunk_r1_06",
		"slug": "06_orbital_viewport_pod",
		"title": "06 — Deep-Space Observation Sleep Bay",
		"cam_pos": Vector3(1.75, 1.56, 2.48),
		"cam_target": Vector3(0.0, 0.90, -0.05),
		"fov": 43.0
	},
	{
		"index": 7,
		"id": "bunk_r1_07",
		"slug": "07_stacked_corvette_bunks",
		"title": "07 — Naval Frigate Dual Pod Stack",
		"cam_pos": Vector3(1.85, 1.68, 2.65),
		"cam_target": Vector3(0.0, 0.98, -0.05),
		"fov": 44.0
	},
	{
		"index": 8,
		"id": "bunk_r1_08",
		"slug": "08_recessed_stasis_alcove",
		"title": "08 — Pressurized Stasis-Style Sleep Chamber",
		"cam_pos": Vector3(1.78, 1.54, 2.54),
		"cam_target": Vector3(0.0, 0.84, 0.02),
		"fov": 43.0
	},
	{
		"index": 9,
		"id": "bunk_r1_09",
		"slug": "09_bio_lifesupport_pod",
		"title": "09 — Closed-Loop O2 Scrubber & Hydro-Bay Pod",
		"cam_pos": Vector3(1.75, 1.56, 2.48),
		"cam_target": Vector3(0.0, 0.88, -0.05),
		"fov": 43.0
	},
	{
		"index": 10,
		"id": "bunk_r1_10",
		"slug": "10_command_stateroom_capsule",
		"title": "10 — Officer's Panoramic Smart-Pod",
		"cam_pos": Vector3(1.82, 1.62, 2.58),
		"cam_target": Vector3(0.0, 0.92, -0.05),
		"fov": 43.0
	}
]

var _stage_container: Node3D
var _model_holder: Node3D
var _lights_container: Node3D
var _camera: Camera3D
var _world_env: WorldEnvironment

var _texture_cache: Dictionary = {}
var _discovered_textures: Array[String] = []
var current_index: int = 0
var turntable_spinning: bool = false

var _batch_render: bool = false
var _validate_only: bool = false
var _frame_counter: int = 0
var _render_step: int = 0
var _render_wait: int = 0


func _ready() -> void:
	_world_env = get_node_or_null("WorldEnvironment") as WorldEnvironment
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

	_scan_textures()
	_build_showcase_stage()

	if FileAccess.file_exists(SPEC_PATH):
		print("[BunkShowcase] Found Sloane's Round-1 spec at: ", SPEC_PATH)

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

	show_candidate(0)


func _scan_textures() -> void:
	_discovered_textures.clear()
	_texture_cache.clear()
	for dpath: String in [EXT_TEX_DIR, FALLBACK_TEX_DIR]:
		var dir: DirAccess = DirAccess.open(dpath)
		if dir == null:
			continue
		dir.list_dir_begin()
		var fname: String = dir.get_next()
		while fname != "":
			if not dir.current_is_dir():
				var lower: String = fname.to_lower()
				if lower.ends_with(".png") or lower.ends_with(".jpg") or lower.ends_with(".jpeg"):
					var full: String = dpath + "/" + fname
					if not _discovered_textures.has(full):
						_discovered_textures.append(full)
			fname = dir.get_next()
		dir.list_dir_end()
	print("[BunkShowcase] Discovered ", _discovered_textures.size(), " texture file(s) in bunk_round1 & shared textures.")


func _load_clean_texture(filename: String) -> Texture2D:
	if _texture_cache.has(filename):
		return _texture_cache[filename] as Texture2D

	var candidate_paths: Array[String] = [
		EXT_TEX_DIR + "/" + filename,
		FALLBACK_TEX_DIR + "/" + filename
	]
	for p: String in candidate_paths:
		if FileAccess.file_exists(p):
			var img: Image = Image.new()
			if img.load(p) == OK and not img.is_empty():
				img.generate_mipmaps()
				var tex: ImageTexture = ImageTexture.create_from_image(img)
				_texture_cache[filename] = tex
				return tex
	return null


## Builds a sleek Hard Sci-Fi Spacecraft Bay stage:
## Dark gunmetal titanium bulkhead plating (#1A1E24, roughness 0.42, metallic 0.65)
## and dark metallic composite decking (#282E38, roughness 0.38, metallic 0.55)
## with a subtle recessed cyan/slate deck trim line — ZERO wood, ZERO wallpaper, ZERO busy patterns.
func _build_showcase_stage() -> void:
	for ch: Node in _stage_container.get_children():
		ch.free()

	# 1. Dark Metallic Composite Decking (#282E38, roughness 0.38, metallic 0.55)
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

	# 2. Dark Gunmetal Anodized Titanium Bulkhead Backwall (#1A1E24, roughness 0.42, metallic 0.65)
	var wall_mat: StandardMaterial3D = StandardMaterial3D.new()
	wall_mat.albedo_color = Color("#1A1E24")
	wall_mat.roughness = 0.42
	wall_mat.metallic = 0.65

	var wall_mi: MeshInstance3D = MeshInstance3D.new()
	wall_mi.name = "SpacecraftBulkheadWall"
	var wbox: BoxMesh = BoxMesh.new()
	wbox.size = Vector3(11.0, 5.5, 0.12)
	wall_mi.mesh = wbox
	wall_mi.position = Vector3(0.0, 2.70, -0.78)
	wall_mi.material_override = wall_mat
	_stage_container.add_child(wall_mi)

	# 3. Left Wing Gunmetal Bulkhead Return (#161A20)
	var left_wall_mat: StandardMaterial3D = StandardMaterial3D.new()
	left_wall_mat.albedo_color = Color("#161A20")
	left_wall_mat.roughness = 0.44
	left_wall_mat.metallic = 0.65

	var left_wall_mi: MeshInstance3D = MeshInstance3D.new()
	left_wall_mi.name = "SpacecraftLeftReturnBulkhead"
	var lwbox: BoxMesh = BoxMesh.new()
	lwbox.size = Vector3(0.12, 5.5, 9.0)
	left_wall_mi.mesh = lwbox
	left_wall_mi.position = Vector3(-3.20, 2.70, 2.0)
	left_wall_mi.material_override = left_wall_mat
	_stage_container.add_child(left_wall_mi)

	# 4. Dark Carbon-Slate Structural Base Plinth (#12151A)
	var trim_mat: StandardMaterial3D = StandardMaterial3D.new()
	trim_mat.albedo_color = Color("#12151A")
	trim_mat.roughness = 0.35
	trim_mat.metallic = 0.75

	var baseboard_mi: MeshInstance3D = MeshInstance3D.new()
	baseboard_mi.name = "BulkheadBasePlinth"
	var bbox: BoxMesh = BoxMesh.new()
	bbox.size = Vector3(11.0, 0.10, 0.14)
	baseboard_mi.mesh = bbox
	baseboard_mi.position = Vector3(0.0, 0.05, -0.77)
	baseboard_mi.material_override = trim_mat
	_stage_container.add_child(baseboard_mi)


func show_candidate(idx: int) -> void:
	if idx < 0 or idx >= CANDIDATES.size():
		return
	current_index = idx
	var info: Dictionary = CANDIDATES[idx]
	var cid: String = String(info["id"])
	var ctitle: String = String(info["title"])

	for ch: Node in _model_holder.get_children():
		ch.free()

	var model_node: Node3D = _load_candidate_glb(cid)
	var aabb := AABB(Vector3(-1.10, 0.0, -0.60), Vector3(2.20, 2.00, 1.20))

	if model_node != null:
		_model_holder.add_child(model_node)
		_convert_and_upgrade_meshes(model_node, cid)
		var computed_aabb: AABB = _compute_node_aabb(model_node)
		if computed_aabb.size.length() > 0.1:
			aabb = computed_aabb
			var center_xz := Vector3(
				aabb.position.x + aabb.size.x * 0.5,
				0.0,
				aabb.position.z + aabb.size.z * 0.5
			)
			model_node.position = -center_xz
			var min_z: float = aabb.position.z - center_xz.z
			var backwall: Node3D = _stage_container.get_node_or_null("SpacecraftBulkheadWall") as Node3D
			var baseboard: Node3D = _stage_container.get_node_or_null("BulkheadBasePlinth") as Node3D
			if backwall != null:
				backwall.position.z = min_z - 0.10
			if baseboard != null:
				baseboard.position.z = min_z - 0.09
		print("[BunkShowcase] Loaded ", cid, " (", ctitle, ") | AABB size=", aabb.size)
	else:
		print("[BunkShowcase] Candidate GLB not found yet: ", cid, ".glb")

	_apply_archetype_lighting_rig(idx + 1, aabb)
	_frame_camera(info, aabb)


func _load_candidate_glb(cid: String) -> Node3D:
	var ext_path: String = EXT_GLB_DIR + "/" + cid + ".glb"
	var res_path: String = RES_GLB_DIR + "/" + cid + ".glb"

	if FileAccess.file_exists(ext_path):
		var doc: GLTFDocument = GLTFDocument.new()
		var state: GLTFState = GLTFState.new()
		var err: Error = doc.append_from_file(ext_path, state)
		if err == OK:
			var scene_root: Node = doc.generate_scene(state)
			if scene_root is Node3D:
				return scene_root as Node3D

	if ResourceLoader.exists(res_path):
		var packed: Resource = ResourceLoader.load(res_path)
		if packed is PackedScene:
			var inst: Node = (packed as PackedScene).instantiate()
			if inst is Node3D:
				return inst as Node3D

	return null


func _convert_and_upgrade_meshes(root: Node3D, cid: String) -> void:
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
						_enhance_candidate_material(smat, cid, mi.name.to_lower())
						mi.set_surface_override_material(s_idx, smat)
		for ch: Node in curr.get_children():
			mstack.append(ch)


func _enhance_candidate_material(smat: StandardMaterial3D, _cid: String, part_name: String) -> void:
	var mname: String = smat.resource_name.to_lower()
	smat.cull_mode = BaseMaterial3D.CULL_DISABLED
	smat.uv1_scale = Vector3.ONE

	# Smoked Polycarbonate Canopy / Stasis Shield Glass
	if mname.contains("glass") or mname.contains("canopy") or mname.contains("polycarbonate") or part_name.contains("canopy") or part_name.contains("glass"):
		smat.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
		if smat.albedo_color.a > 0.85:
			smat.albedo_color.a = 0.42
		smat.roughness = 0.08
		smat.metallic = 0.25
		return

	# Emissive Cyan (#00E5FF), Amber (#FF9500), UV/Bio, and Sci-Fi HUD screens
	if mname.contains("hud") or mname.contains("oled") or mname.contains("crt") or mname.contains("telemetry") or part_name.contains("hud") or part_name.contains("oled") or part_name.contains("display"):
		smat.emission_enabled = true
		if smat.albedo_texture != null:
			smat.emission_texture = smat.albedo_texture
		if smat.emission == Color(0, 0, 0, 1):
			smat.emission = Color("#00E5FF")
		smat.emission_energy_multiplier = 1.45
	elif mname.contains("vista") or part_name.contains("viewport") or part_name.contains("vista"):
		smat.emission_enabled = true
		if smat.albedo_texture != null:
			smat.emission_texture = smat.albedo_texture
		smat.emission_energy_multiplier = 1.15
	elif smat.emission_enabled or mname.contains("emissive") or mname.contains("led") or mname.contains("glow") or part_name.contains("led") or part_name.contains("strip") or part_name.contains("glow"):
		smat.emission_enabled = true
		if smat.emission == Color(0, 0, 0, 1):
			smat.emission = smat.albedo_color
		smat.emission_energy_multiplier = 2.1


func _compute_node_aabb(root: Node3D) -> AABB:
	var combined := AABB()
	var first: bool = true
	var stack: Array[Node] = [root]
	while not stack.is_empty():
		var curr: Node = stack.pop_back()
		if curr is MeshInstance3D:
			var mi: MeshInstance3D = curr as MeshInstance3D
			if mi.mesh != null:
				var local_aabb: AABB = mi.mesh.get_aabb()
				var xform_aabb: AABB = mi.transform * local_aabb
				if first:
					combined = xform_aabb
					first = false
				else:
					combined = combined.merge(xform_aabb)
		for ch: Node in curr.get_children():
			stack.append(ch)
	return combined


func _frame_camera(info: Dictionary, _aabb: AABB) -> void:
	if _camera == null:
		return
	var cam_pos: Vector3 = info.get("cam_pos", Vector3(1.78, 1.58, 2.50)) as Vector3
	var cam_target: Vector3 = info.get("cam_target", Vector3(0.0, 0.88, -0.05)) as Vector3
	_camera.global_position = cam_pos
	_camera.fov = float(info.get("fov", 43.0))
	_camera.look_at(cam_target, Vector3.UP)


func _apply_archetype_lighting_rig(index_1_based: int, aabb: AABB) -> void:
	for ch: Node in _lights_container.get_children():
		ch.free()

	var h: float = maxf(aabb.size.y, 1.6)

	# Hard Sci-Fi 3-Point Rig: Crisp Cool-White Aerospace Key + Deep Orbital Blue Fill + Metallic Rim
	var key_light: DirectionalLight3D = DirectionalLight3D.new()
	key_light.name = "AerospaceKeyLight"
	key_light.shadow_enabled = true
	key_light.shadow_bias = 0.02
	key_light.light_color = Color("#E8F2FF")
	key_light.light_energy = 1.15
	key_light.position = Vector3(2.3, 2.7, 2.6)
	_lights_container.add_child(key_light)
	key_light.look_at(Vector3(0.0, 0.9, 0.0), Vector3.UP)

	var fill_light: OmniLight3D = OmniLight3D.new()
	fill_light.name = "OrbitalBayFillLight"
	fill_light.position = Vector3(-2.4, 1.55, 2.2)
	fill_light.light_color = Color("#6898D0")
	fill_light.light_energy = 0.45
	fill_light.omni_range = 7.0
	_lights_container.add_child(fill_light)

	var rim_light: OmniLight3D = OmniLight3D.new()
	rim_light.name = "TitaniumRimLight"
	rim_light.position = Vector3(-1.5, 2.65, -1.6)
	rim_light.light_color = Color("#98D8FF")
	rim_light.light_energy = 0.85
	rim_light.omni_range = 6.0
	_lights_container.add_child(rim_light)

	# Per-Archetype Hard Sci-Fi Practical LED & HUD Accent Lights
	match index_1_based:
		1:
			# 01_aerospace_cryo_berth: Recessed Cyan (#00E5FF) perimeter strip + vitals HUD glow
			_add_omni("CryoCyanPerimeterStrip", Vector3(0.0, 1.48, 0.10), Color("#00E5FF"), 1.65, 2.5)
			_add_omni("VitalsHUDGlow", Vector3(-0.45, 0.95, -0.28), Color("#00E5FF"), 0.85, 1.6)
		2:
			# 02_expanse_bulkhead_rack: Amber (#FF9500) caution strip lighting + cool steel rib fill
			_add_omni("HighGAmberCautionStrip", Vector3(0.0, 1.52, 0.05), Color("#FF9500"), 1.65, 2.5)
			_add_omni("UnderRackCautionGlow", Vector3(0.0, 0.18, 0.48), Color("#FF8C00"), 0.85, 1.8)
		3:
			# 03_zero_g_mag_couchette: Glowing Cyan (#00E5FF) mag-rail indicators + surgical task spots
			_add_omni("MagRailCyanLeft", Vector3(-0.78, 1.05, -0.35), Color("#00E5FF"), 1.45, 2.2)
			_add_omni("MagRailCyanRight", Vector3(0.78, 1.05, -0.35), Color("#00E5FF"), 1.45, 2.2)
			_add_spot("CouchetteTaskSpot", Vector3(-0.45, 1.45, 0.10), Vector3(-0.35, 0.62, 0.0), Color("#E6F4FF"), 1.35, 2.4, 45.0)
		4:
			# 04_blast_shutter_pod: Recessed Amber/White medical-grade sleep bay lighting + telemetry console
			_add_omni("BlastPodMedicalWhite", Vector3(0.0, 1.38, -0.05), Color("#E6F4FF"), 1.40, 2.3)
			_add_omni("BlastPodAmberSeal", Vector3(-0.55, 0.95, 0.25), Color("#FF9500"), 1.15, 2.0)
		5:
			# 05_spin_transition_harness_bunk: Signal-Amber & Cyan EVA lockdown cove lights
			_add_omni("HarnessLockdownAmber", Vector3(0.0, 1.48, -0.15), Color("#FF9500"), 1.50, 2.4)
			_add_omni("HarnessHUDCyan", Vector3(-0.55, 0.98, -0.25), Color("#00E5FF"), 0.95, 1.8)
		6:
			# 06_orbital_viewport_pod: Cyan (#00E5FF) edge-lit viewport frame + deep-space starlight rim
			_add_omni("ViewportCyanEdgeLight", Vector3(0.0, 1.25, -0.30), Color("#00E5FF"), 1.65, 2.6)
			_add_omni("OrbitalReadingBar", Vector3(-0.75, 1.35, -0.10), Color("#E6F4FF"), 1.15, 2.0)
		7:
			# 07_stacked_corvette_bunks: Dual BAY 01 / BAY 02 Cyan interior strip lights + Amber status plates
			_add_omni("CorvetteBay01Cyan", Vector3(-0.15, 0.88, 0.0), Color("#00E5FF"), 1.45, 2.1)
			_add_omni("CorvetteBay02Cyan", Vector3(0.15, 1.78, 0.0), Color("#00E5FF"), 1.45, 2.1)
			_add_omni("StatusPlateAmber", Vector3(-0.85, 1.25, 0.48), Color("#FF9500"), 0.85, 1.6)
		8:
			# 08_recessed_stasis_alcove: Glowing Amber (#FF9500) deck hazard threshold + Cyan stasis chamber cove
			_add_omni("ThresholdHazardAmber", Vector3(0.0, 0.22, 0.58), Color("#FF9500"), 1.55, 2.2)
			_add_omni("StasisChamberCyanCove", Vector3(0.0, 1.38, -0.20), Color("#00E5FF"), 1.45, 2.4)
		9:
			# 09_bio_lifesupport_pod: Cool Ultraviolet/Cyan (#00E5FF / #5CE1E6) bio-oxygenation tube LEDs
			_add_omni("BioO2TubeCyanUV", Vector3(-0.35, 1.55, 0.05), Color("#00E5FF"), 1.60, 2.5)
			_add_omni("BioO2TubeEmerald", Vector3(0.35, 1.55, 0.05), Color("#38F2C8"), 1.35, 2.3)
		10:
			# 10_command_stateroom_capsule: Sweeping Cyan + Warm-White cove arch + twin OLED wings
			_add_omni("CommandOLEDWingL", Vector3(-0.80, 1.12, -0.15), Color("#00E5FF"), 1.45, 2.2)
			_add_omni("CommandOLEDWingR", Vector3(0.80, 1.12, -0.15), Color("#00E5FF"), 1.45, 2.2)
			_add_spot("CommandCoveArchSpot", Vector3(0.0, h * 1.02, 0.75), Vector3(0.0, h * 0.45, 0.0), Color("#E6F4FF"), 1.35, 3.5, 48.0)


func _add_omni(lname: String, pos: Vector3, col: Color, energy: float, rng: float) -> OmniLight3D:
	var omni: OmniLight3D = OmniLight3D.new()
	omni.name = lname
	omni.position = pos
	omni.light_color = col
	omni.light_energy = energy
	omni.omni_range = rng
	_lights_container.add_child(omni)
	return omni


func _add_spot(lname: String, pos: Vector3, target: Vector3, col: Color, energy: float, rng: float, angle: float) -> SpotLight3D:
	var spot: SpotLight3D = SpotLight3D.new()
	spot.name = lname
	spot.position = pos
	spot.light_color = col
	spot.light_energy = energy
	spot.spot_range = rng
	spot.spot_angle = angle
	_lights_container.add_child(spot)
	spot.look_at(target, Vector3.UP)
	return spot


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
				KEY_RIGHT: show_candidate((current_index + 1) % CANDIDATES.size())
				KEY_LEFT: show_candidate((current_index - 1 + CANDIDATES.size()) % CANDIDATES.size())
				KEY_SPACE: turntable_spinning = not turntable_spinning


func _process(delta: float) -> void:
	_frame_counter += 1

	if _batch_render:
		_process_batch_render()
		return

	if _validate_only:
		if _frame_counter >= 4:
			print("[BunkShowcase] Headless validation complete. Exiting cleanly.")
			get_tree().quit(0)
		return

	if turntable_spinning and _model_holder != null:
		_model_holder.rotate_y(0.45 * delta)


func _process_batch_render() -> void:
	if DisplayServer.get_name() == "headless":
		print("[BunkShowcase] Cannot capture viewport images under headless DisplayServer. Run with xvfb-run + opengl3.")
		get_tree().quit(0)
		return

	if _frame_counter < 6:
		return

	if _render_step >= CANDIDATES.size():
		print("[BunkShowcase] All 10 Round-1 Hard Sci-Fi Bunk Pod beauty renders complete! Exiting cleanly.")
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
				var err: Error = img.save_png(out_file)
				if err == OK:
					print("[BunkShowcase] Saved render: ", out_file, " (", img.get_width(), "x", img.get_height(), ")")
		_render_step += 1
		_render_wait = 0
