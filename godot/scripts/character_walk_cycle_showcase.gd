class_name CharacterWalkCycleShowcase
extends Node3D
## Godot 4.3 Multi-Phase WalkCycle & In-Cylinder Promenade Showcase Renderer
## Captures locked winner `#02` (`char_crew_winner_01_aegis7_commander.glb` / `char_crew_r1_02.glb`)
## across 4 distinct WalkCycle keyframe phases (`0%`, `25%`, `50%`, `75%` of `T = 1.20s`),
## a 3/4 Rear Dual-Zone Backpack Rig view, and an In-Situ Cylinder Hab-7 Promenade Walk view.

const WINNERS_DIR := "res://../assets/glb/winners"
const CHAR_GLB_DIRS := [
	"res://../assets/glb/character/char_crew_round1",
	"res://../assets/glb/character",
	"res://../assets/glb/character/char_01",
	"res://../assets/glb/characters"
]
const CHAR_TEX_DIR := "res://../assets/textures/character"
const CYL_INT_TEX_DIR := "res://../assets/textures/cylinder_interior"
const BLDG_TEX_DIR := "res://../assets/textures/buildings"
const SHARED_TEX_DIR := "res://../assets/textures"

const OUT_DIRS := [
	"res://renders/character",
	"res://renders/character/char_crew_round1",
	"res://renders/characters",
	"res://../assets/renders/character",
	"res://../assets/renders/character/char_crew_round1",
	"res://../assets/renders/characters"
]

const WALK_SHOTS := [
	{
		"name": "walk_frame_01_t000",
		"time": 0.00,
		"pos": Vector3(1.55, 1.15, 2.35),
		"target": Vector3(0.0, 0.94, 0.04),
		"fov": 38.0,
		"insitu": false
	},
	{
		"name": "walk_frame_02_t025",
		"time": 0.30,
		"pos": Vector3(1.55, 1.15, 2.35),
		"target": Vector3(0.0, 0.94, 0.04),
		"fov": 38.0,
		"insitu": false
	},
	{
		"name": "walk_frame_03_t050",
		"time": 0.60,
		"pos": Vector3(1.55, 1.15, 2.35),
		"target": Vector3(0.0, 0.94, 0.04),
		"fov": 38.0,
		"insitu": false
	},
	{
		"name": "walk_frame_04_t075",
		"time": 0.90,
		"pos": Vector3(1.55, 1.15, 2.35),
		"target": Vector3(0.0, 0.94, 0.04),
		"fov": 38.0,
		"insitu": false
	},
	{
		"name": "walk_frame_05_rear_3q_rig",
		"time": 0.15,
		"pos": Vector3(-1.55, 1.20, -2.35),
		"target": Vector3(0.0, 0.96, 0.0),
		"fov": 38.0,
		"insitu": false
	},
	{
		"name": "walk_frame_06_promenade_insitu",
		"time": 0.06,
		"pos": Vector3(1.42, 1.04, 2.25),
		"target": Vector3(-0.35, 1.15, -3.50),
		"fov": 42.0,
		"insitu": true
	},
]

var _stage_container: Node3D
var _insitu_city_group: Node3D
var _char_container: Node3D
var _lights_container: Node3D
var _camera: Camera3D
var _char_root: Node3D

var _tex_cache: Dictionary = {}
var _batch_render: bool = false
var _validate_only: bool = false
var _frame_counter: int = 0
var _render_step: int = 0
var _render_wait: int = 0


func _ready() -> void:
	_camera = get_node_or_null("WalkCamera") as Camera3D
	_stage_container = get_node_or_null("PromenadeStage") as Node3D
	_char_container = get_node_or_null("CharacterContainer") as Node3D
	_lights_container = get_node_or_null("LightingRig") as Node3D

	if _stage_container == null:
		_stage_container = Node3D.new()
		_stage_container.name = "PromenadeStage"
		add_child(_stage_container)
	if _char_container == null:
		_char_container = Node3D.new()
		_char_container.name = "CharacterContainer"
		add_child(_char_container)
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

	_build_promenade_stage()
	_setup_walk_lighting()
	_load_hero_character()
	_apply_shot(0)


func _load_tex(fname: String) -> Texture2D:
	if _tex_cache.has(fname):
		return _tex_cache[fname] as Texture2D
	for d: String in [CHAR_TEX_DIR, CYL_INT_TEX_DIR, BLDG_TEX_DIR, SHARED_TEX_DIR]:
		var p: String = d + "/" + fname
		if FileAccess.file_exists(p):
			var img: Image = Image.new()
			if img.load(p) == OK and not img.is_empty():
				img.generate_mipmaps()
				var tex: ImageTexture = ImageTexture.create_from_image(img)
				_tex_cache[fname] = tex
				return tex
	return null


func _build_promenade_stage() -> void:
	for ch: Node in _stage_container.get_children():
		ch.free()

	# 1. Travertine-Alloy Promenade Walk Strip (`terrain_park_promenade_paving.png`)
	var walkway: MeshInstance3D = MeshInstance3D.new()
	var wbox: BoxMesh = BoxMesh.new()
	wbox.size = Vector3(16.0, 0.12, 42.0)
	walkway.mesh = wbox
	walkway.position = Vector3(0.0, -0.06, -12.0)
	var pmat: StandardMaterial3D = StandardMaterial3D.new()
	pmat.albedo_color = Color("#9EA2A8")
	pmat.roughness = 0.42
	pmat.metallic = 0.18
	var ptex: Texture2D = _load_tex("terrain_park_promenade_paving.png")
	if ptex != null:
		pmat.albedo_texture = ptex
		pmat.uv1_scale = Vector3(6.0, 14.0, 1.0)
	walkway.material_override = pmat
	_stage_container.add_child(walkway)

	# 2. Glowing Cyan & Amber Stride-Reference Guide Lines along the Promenade
	for x_rail: float in [-0.65, 0.65]:
		var strip: MeshInstance3D = MeshInstance3D.new()
		var sbox: BoxMesh = BoxMesh.new()
		sbox.size = Vector3(0.05, 0.012, 36.0)
		strip.mesh = sbox
		strip.position = Vector3(x_rail, 0.006, -10.0)
		var smat: StandardMaterial3D = StandardMaterial3D.new()
		var col: Color = Color("#00E5FF") if x_rail > 0.0 else Color("#FFB703")
		smat.albedo_color = col
		smat.emission_enabled = true
		smat.emission = col
		smat.emission_energy_multiplier = 1.85
		strip.material_override = smat
		_stage_container.add_child(strip)

	# 3. Specular Ring-River Canal & Botanical Terrace Flanking the Promenade
	var canal: MeshInstance3D = MeshInstance3D.new()
	var cbox: BoxMesh = BoxMesh.new()
	cbox.size = Vector3(8.0, 0.10, 42.0)
	canal.mesh = cbox
	canal.position = Vector3(-6.2, -0.02, -12.0)
	var wmat: StandardMaterial3D = StandardMaterial3D.new()
	wmat.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
	wmat.albedo_color = Color(0.65, 0.92, 1.0, 0.85)
	var wtex: Texture2D = _load_tex("water_ring_river_specular.png")
	if wtex != null:
		wmat.albedo_texture = wtex
		wmat.uv1_scale = Vector3(3.0, 10.0, 1.0)
	wmat.roughness = 0.08
	wmat.metallic = 0.15
	wmat.emission_enabled = true
	wmat.emission = Color("#28B8E8")
	wmat.emission_energy_multiplier = 0.55
	canal.material_override = wmat
	_stage_container.add_child(canal)

	var park: MeshInstance3D = MeshInstance3D.new()
	var pkbox: BoxMesh = BoxMesh.new()
	pkbox.size = Vector3(12.0, 0.25, 42.0)
	park.mesh = pkbox
	park.position = Vector3(8.5, 0.02, -12.0)
	var bmat: StandardMaterial3D = StandardMaterial3D.new()
	var btex: Texture2D = _load_tex("biome_terraced_botanical_canopy.png")
	if btex != null:
		bmat.albedo_texture = btex
		bmat.uv1_scale = Vector3(4.0, 10.0, 1.0)
	bmat.roughness = 0.72
	park.material_override = bmat
	_stage_container.add_child(park)

	# 4. In-Situ Cylinder Hab-7 Buildings & Street Props Group
	_insitu_city_group = Node3D.new()
	_insitu_city_group.name = "InSituPromenadeCity"
	_stage_container.add_child(_insitu_city_group)

	var bg_items := [
		{"file": WINNERS_DIR + "/prop_02_winner_01_holo_wayfinding_kiosk.glb", "pos": Vector3(-2.2, 0.0, -4.5), "rot_y": 28.0, "sc": 0.85},
		{"file": WINNERS_DIR + "/prop_04_winner_01_civic_planter_bench_pod.glb", "pos": Vector3(2.4, 0.0, -5.2), "rot_y": -25.0, "sc": 0.90},
		{"file": WINNERS_DIR + "/bldg_01_winner_01_hab_spire.glb", "pos": Vector3(-9.5, 0.0, -22.0), "rot_y": 22.0, "sc": 1.0},
		{"file": WINNERS_DIR + "/bldg_02_winner_01_transit_rotunda.glb", "pos": Vector3(8.5, 0.0, -24.0), "rot_y": -20.0, "sc": 1.0},
		{"file": WINNERS_DIR + "/bldg_11_winner_01_citadel_command_hq.glb", "pos": Vector3(-1.2, 0.0, -34.0), "rot_y": 0.0, "sc": 1.15},
	]
	for item: Dictionary in bg_items:
		var p: String = String(item["file"])
		if FileAccess.file_exists(p):
			var doc: GLTFDocument = GLTFDocument.new()
			var state: GLTFState = GLTFState.new()
			if doc.append_from_file(p, state) == OK:
				var r: Node = doc.generate_scene(state)
				if r is Node3D:
					var n3d: Node3D = r as Node3D
					n3d.position = item["pos"] as Vector3
					n3d.rotation_degrees = Vector3(0.0, float(item["rot_y"]), 0.0)
					var sc: float = float(item["sc"])
					n3d.scale = Vector3(sc, sc, sc)
					_insitu_city_group.add_child(n3d)
					_upgrade_character_materials(n3d)

	# Panoramic O'Neill Cylinder Backdrop behind the Promenade
	var backdrop: MeshInstance3D = MeshInstance3D.new()
	var qmesh: QuadMesh = QuadMesh.new()
	qmesh.size = Vector2(68.0, 38.0)
	backdrop.mesh = qmesh
	backdrop.position = Vector3(0.0, 12.0, -48.0)
	var vmat: StandardMaterial3D = StandardMaterial3D.new()
	var vtex: Texture2D = _load_tex("vista_oneill_cylinder_interior.png")
	if vtex != null:
		vmat.albedo_texture = vtex
		vmat.albedo_color = Color(0.68, 0.74, 0.82, 1.0)
		vmat.emission_enabled = true
		vmat.emission_texture = vtex
		vmat.emission_energy_multiplier = 0.65
	vmat.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	vmat.cull_mode = BaseMaterial3D.CULL_DISABLED
	backdrop.material_override = vmat
	backdrop.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	_stage_container.add_child(backdrop)


func _setup_walk_lighting() -> void:
	for ch: Node in _lights_container.get_children():
		ch.free()

	var key_light: DirectionalLight3D = DirectionalLight3D.new()
	key_light.name = "WarmGoldenHourKeyLight"
	key_light.rotation_degrees = Vector3(-38.0, 35.0, 0.0)
	key_light.light_color = Color("#FFE6BF")
	key_light.light_energy = 1.18
	key_light.shadow_enabled = true
	key_light.shadow_blur = 1.2
	key_light.shadow_bias = 0.01
	_lights_container.add_child(key_light)

	var rim_light: DirectionalLight3D = DirectionalLight3D.new()
	rim_light.name = "CyanFresnelRimKicker"
	rim_light.rotation_degrees = Vector3(-24.0, -145.0, 0.0)
	rim_light.light_color = Color("#5CE1E6")
	rim_light.light_energy = 1.20
	rim_light.shadow_enabled = false
	_lights_container.add_child(rim_light)

	var rear_fill: DirectionalLight3D = DirectionalLight3D.new()
	rear_fill.name = "RearBackpackFillLight"
	rear_fill.rotation_degrees = Vector3(-32.0, -165.0, 0.0)
	rear_fill.light_color = Color("#FFF0D8")
	rear_fill.light_energy = 0.85
	rear_fill.shadow_enabled = false
	_lights_container.add_child(rear_fill)

	var bounce_omni: OmniLight3D = OmniLight3D.new()
	bounce_omni.name = "UnderFloorBounceFill"
	bounce_omni.position = Vector3(0.0, 0.60, 1.45)
	bounce_omni.light_color = Color("#8898AA")
	bounce_omni.light_energy = 0.75
	bounce_omni.omni_range = 6.5
	_lights_container.add_child(bounce_omni)

	var visor_fill: OmniLight3D = OmniLight3D.new()
	visor_fill.name = "VisorInteriorHeadFill"
	visor_fill.position = Vector3(0.65, 1.68, 1.35)
	visor_fill.light_color = Color("#FFF4E4")
	visor_fill.light_energy = 0.70
	visor_fill.omni_range = 4.5
	_lights_container.add_child(visor_fill)


func _find_hero_glb() -> String:
	var win_candidates := [
		WINNERS_DIR + "/char_crew_winner_01_aegis7_commander.glb",
		WINNERS_DIR + "/character_crew_winner_01_aegis7_commander.glb",
		WINNERS_DIR + "/char_crew_winner_01.glb",
	]
	for wp: String in win_candidates:
		if FileAccess.file_exists(wp):
			return wp
	for d: String in CHAR_GLB_DIRS:
		for n: String in ["char_crew_r1_02.glb", "character_crew_r1_02.glb", "char_01_r1_02.glb"]:
			var p: String = d + "/" + n
			if FileAccess.file_exists(p):
				return p
	return ""


func _load_hero_character() -> void:
	for ch: Node in _char_container.get_children():
		ch.free()

	var glb_path: String = _find_hero_glb()
	if glb_path == "":
		return

	var doc: GLTFDocument = GLTFDocument.new()
	var state: GLTFState = GLTFState.new()
	if doc.append_from_file(glb_path, state) == OK:
		var root: Node = doc.generate_scene(state)
		if root is Node3D:
			_char_root = root as Node3D
			_char_root.name = "CharCrewWinner02_Aegis7Commander"
			_char_container.add_child(_char_root)
			_upgrade_character_materials(_char_root)


func _apply_shot(idx: int) -> void:
	if idx < 0 or idx >= WALK_SHOTS.size() or _camera == null:
		return
	var s: Dictionary = WALK_SHOTS[idx]
	if _insitu_city_group != null:
		_insitu_city_group.visible = bool(s["insitu"])
	if _char_root != null:
		_seek_or_pose_walk_cycle(_char_root, float(s["time"]))
	_camera.near = 0.05
	_camera.far = 1000.0
	_camera.fov = float(s["fov"])
	_camera.global_position = s["pos"] as Vector3
	_camera.look_at(s["target"] as Vector3, Vector3.UP)


func _seek_or_pose_walk_cycle(root: Node3D, time_sec: float) -> void:
	var anim_player: AnimationPlayer = null
	var stack: Array[Node] = [root]
	while not stack.is_empty():
		var curr: Node = stack.pop_back()
		if curr is AnimationPlayer:
			anim_player = curr as AnimationPlayer
			break
		for ch: Node in curr.get_children():
			stack.append(ch)

	var posed_by_anim: bool = false
	if anim_player != null:
		var anim_list: PackedStringArray = anim_player.get_animation_list()
		var chosen_anim: String = ""
		for a: String in anim_list:
			if a.to_lower().contains("walk"):
				chosen_anim = a
				break
		if chosen_anim == "" and not anim_list.is_empty():
			for a: String in anim_list:
				if a != "RESET":
					chosen_anim = a
					break
		if chosen_anim != "":
			anim_player.play(chosen_anim)
			anim_player.seek(time_sec, true)
			anim_player.advance(0.0)
			anim_player.speed_scale = 0.0
			posed_by_anim = true

	if not posed_by_anim:
		_apply_procedural_walk_pose(root, time_sec)


func _apply_procedural_walk_pose(root: Node3D, time_sec: float) -> void:
	var period: float = 1.20
	var phi: float = (time_sec / period) * TAU
	var node_map: Dictionary = {}
	var stack: Array[Node] = [root]
	while not stack.is_empty():
		var curr: Node = stack.pop_back()
		if curr is Node3D:
			node_map[curr.name.to_lower()] = curr
		for ch: Node in curr.get_children():
			stack.append(ch)

	for k: String in ["hips", "pelvis"]:
		if node_map.has(k):
			var n: Node3D = node_map[k]
			n.position.y = 0.920 - 0.024 * cos(2.0 * phi)
			n.position.x = -0.018 * sin(phi)
			n.rotation_degrees = Vector3(3.5 + 1.5 * cos(2.0 * phi), 5.5 * cos(phi), 3.0 * sin(phi))
	for k: String in ["chest", "torso", "spine"]:
		if node_map.has(k):
			var n: Node3D = node_map[k]
			n.rotation_degrees.y = -6.5 * cos(phi)
	for k: String in ["upperleg_l", "leftupleg", "thigh_l"]:
		if node_map.has(k):
			(node_map[k] as Node3D).rotation_degrees.x = -24.0 * cos(phi) + 2.0
	for k: String in ["upperleg_r", "rightupleg", "thigh_r"]:
		if node_map.has(k):
			(node_map[k] as Node3D).rotation_degrees.x = -24.0 * cos(phi + PI) + 2.0
	for k: String in ["lowerleg_l", "leftleg", "shin_l", "calf_l"]:
		if node_map.has(k):
			(node_map[k] as Node3D).rotation_degrees.x = 24.0 * pow(maxf(0.0, -sin(phi)), 1.3) + 7.0 * maxf(0.0, sin(phi)) + 4.0
	for k: String in ["lowerleg_r", "rightleg", "shin_r", "calf_r"]:
		if node_map.has(k):
			(node_map[k] as Node3D).rotation_degrees.x = 24.0 * pow(maxf(0.0, -sin(phi + PI)), 1.3) + 7.0 * maxf(0.0, sin(phi + PI)) + 4.0
	for k: String in ["upperarm_l", "leftupperarm", "arm_l"]:
		if node_map.has(k):
			(node_map[k] as Node3D).rotation_degrees.x = -22.0 * cos(phi + PI) + 4.0
	for k: String in ["upperarm_r", "rightupperarm", "arm_r"]:
		if node_map.has(k):
			(node_map[k] as Node3D).rotation_degrees.x = -22.0 * cos(phi) + 4.0
	for k: String in ["lowerarm_l", "leftforearm", "forearm_l"]:
		if node_map.has(k):
			(node_map[k] as Node3D).rotation_degrees.x = -20.0 - 14.0 * maxf(0.0, -cos(phi + PI))
	for k: String in ["lowerarm_r", "rightforearm", "forearm_r"]:
		if node_map.has(k):
			(node_map[k] as Node3D).rotation_degrees.x = -20.0 - 14.0 * maxf(0.0, -cos(phi))


func _upgrade_character_materials(root: Node3D) -> void:
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
		if imp.mesh != null:
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

	var tex_armor: Texture2D = _load_tex("char_suit_armor_albedo.png")
	var tex_under: Texture2D = _load_tex("char_undersuit_ribbed_fabric.png")
	var tex_visor: Texture2D = _load_tex("char_visor_hud_translucent.png")
	var tex_chest: Texture2D = _load_tex("char_chest_telemetry_emissive.png")

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

						if mname.contains("visor") or pname.contains("visor") or mname.contains("glass") or mname.contains("translucent"):
							smat.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
							smat.albedo_color = Color(0.76, 0.92, 1.0, 0.14)
							if tex_visor != null and (mname.contains("visor") or pname.contains("visor")):
								smat.albedo_texture = tex_visor
								smat.emission_texture = tex_visor
							smat.roughness = 0.06
							smat.metallic = 0.25
							smat.metallic_specular = 0.95
							smat.emission_enabled = true
							if smat.emission == Color(0, 0, 0, 1):
								smat.emission = Color("#00E5FF")
							smat.emission_energy_multiplier = 0.35
							mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
						elif mname.contains("chesttelemetry") or mname.contains("oled") or pname.contains("telemetry"):
							if tex_chest != null:
								smat.albedo_texture = tex_chest
								smat.emission_texture = tex_chest
							smat.roughness = 0.18
							smat.metallic = 0.15
							smat.emission_enabled = true
							smat.emission = Color(0.65, 0.95, 1.0)
							smat.emission_energy_multiplier = 0.72
						elif mname.contains("aerospacewhite") or mname.contains("armor_white") or pname.contains("armor_white"):
							if tex_armor != null and smat.albedo_texture == null:
								smat.albedo_texture = tex_armor
							smat.roughness = 0.32
							smat.metallic = 0.15
						elif mname.contains("gunmetal") or mname.contains("chassis"):
							if tex_armor != null and smat.albedo_texture == null:
								smat.albedo_texture = tex_armor
							smat.roughness = 0.38
							smat.metallic = 0.78
						elif mname.contains("undersuit") or mname.contains("bellows") or mname.contains("ripstop") or mname.contains("carbonslate"):
							if tex_under != null and smat.albedo_texture == null:
								smat.albedo_texture = tex_under
							smat.roughness = 0.70
							smat.metallic = 0.08
						elif smat.emission_enabled or mname.contains("emissive") or mname.contains("hud") or mname.contains("led") or mname.contains("beacon") or mname.contains("bio"):
							smat.emission_enabled = true
							if smat.emission == Color(0, 0, 0, 1):
								smat.emission = smat.albedo_color
							smat.emission_energy_multiplier = 1.05

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
	if _frame_counter < 5:
		return
	if _render_step >= WALK_SHOTS.size():
		print("[CharacterWalkCycleShowcase] Completed all ", WALK_SHOTS.size(), " walk-cycle renders!")
		get_tree().quit(0)
		return
	if _render_wait == 0:
		_apply_shot(_render_step)
		_render_wait = 1
		return
	_render_wait += 1
	if _render_wait >= 6:
		var s: Dictionary = WALK_SHOTS[_render_step]
		var sname: String = String(s["name"])
		var img: Image = get_viewport().get_texture().get_image()
		if img != null and not img.is_empty():
			for out_dir: String in OUT_DIRS:
				DirAccess.make_dir_recursive_absolute(out_dir)
				var fpath: String = out_dir + "/" + sname + ".png"
				if img.save_png(fpath) == OK:
					print("[CharacterWalkCycleShowcase] Saved ", fpath)
		_render_step += 1
		_render_wait = 0
