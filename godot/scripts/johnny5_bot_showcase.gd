class_name Johnny5BotShowcase
extends Node3D
## Godot 4.3 5-Candidate *WALL-E* x *Johnny 5* Utility Robot Showcase & 4-Faction Livery Renderer
## Renders:
## 1. `char_bot_johnny5_r1_01.png` .. `char_bot_johnny5_r1_05.png` (and `char_johnny5_r1_01..05.png`)
## 2. `johnny5_livery_01_sprocket.png`, `johnny5_livery_02_sweep.png`, `johnny5_livery_03_puddle.png`, `johnny5_livery_04_clover.png`

const BOT_GLB_DIRS := [
	"res://assets/models/characters/johnny5",
	"res://assets/models/characters/bots",
	"res://assets/models/characters",
	"res://../assets/glb/characters/johnny5",
	"res://../assets/glb/characters/bots",
	"res://../assets/glb/characters",
	"res://../assets/glb/character"
]

const TEX_DIRS := [
	"res://../assets/textures/preface",
	"res://../assets/textures/residential",
	"res://../assets/textures",
	"res://../assets/textures/cylinder_interior",
	"res://../assets/textures/buildings"
]

const OUT_DIRS := [
	"res://renders/characters/johnny5",
	"res://renders/characters/bots",
	"res://renders/character/bots",
	"res://renders/bots",
	"res://renders/preface",
	"res://../assets/renders/characters/johnny5",
	"res://../assets/renders/characters/bots",
	"res://../assets/renders/character/bots",
	"res://../assets/renders/bots",
	"res://../assets/renders/preface"
]

var _stage_container: Node3D
var _bot_container: Node3D
var _lights_container: Node3D
var _camera: Camera3D

var _tex_cache: Dictionary = {}
var _batch_render: bool = false
var _validate_only: bool = false
var _render_queue: Array[Dictionary] = []
var _frame_counter: int = 0
var _render_step: int = 0
var _render_wait: int = 0


func _ready() -> void:
	_camera = get_node_or_null("ShowcaseCamera") as Camera3D
	_stage_container = get_node_or_null("ShowcaseStage") as Node3D
	_bot_container = get_node_or_null("BotContainer") as Node3D
	_lights_container = get_node_or_null("LightingRig") as Node3D

	if _stage_container == null:
		_stage_container = Node3D.new()
		_stage_container.name = "ShowcaseStage"
		add_child(_stage_container)
	if _bot_container == null:
		_bot_container = Node3D.new()
		_bot_container.name = "BotContainer"
		add_child(_bot_container)
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

	_build_showcase_stage()
	_setup_lighting(1)
	_build_render_queue()

	if not _render_queue.is_empty():
		_load_entry(_render_queue[0])


func _load_tex(fname: String) -> Texture2D:
	if _tex_cache.has(fname):
		return _tex_cache[fname] as Texture2D
	for d: String in TEX_DIRS:
		var p: String = d + "/" + fname
		if FileAccess.file_exists(p):
			var img: Image = Image.new()
			if img.load(p) == OK and not img.is_empty():
				img.generate_mipmaps()
				var tex: ImageTexture = ImageTexture.create_from_image(img)
				_tex_cache[fname] = tex
				return tex
	return null


func _build_showcase_stage() -> void:
	for ch: Node in _stage_container.get_children():
		ch.free()

	# Octagonal Bot Docking Turntable Plinth
	var plinth: MeshInstance3D = MeshInstance3D.new()
	var cmesh: CylinderMesh = CylinderMesh.new()
	cmesh.top_radius = 1.15
	cmesh.bottom_radius = 1.25
	cmesh.height = 0.08
	cmesh.radial_segments = 8
	plinth.mesh = cmesh
	plinth.position = Vector3(0.0, -0.04, 0.0)
	var pmat: StandardMaterial3D = StandardMaterial3D.new()
	pmat.albedo_color = Color("#1C222B")
	pmat.roughness = 0.38
	pmat.metallic = 0.55
	plinth.material_override = pmat
	_stage_container.add_child(plinth)

	# Glowing Cyan Inductive Turntable Ring
	var ring: MeshInstance3D = MeshInstance3D.new()
	var rmesh: CylinderMesh = CylinderMesh.new()
	rmesh.top_radius = 0.72
	rmesh.bottom_radius = 0.75
	rmesh.height = 0.012
	rmesh.radial_segments = 24
	ring.mesh = rmesh
	ring.position = Vector3(0.0, 0.006, 0.0)
	var rmat: StandardMaterial3D = StandardMaterial3D.new()
	rmat.albedo_color = Color("#00E5FF")
	rmat.emission_enabled = true
	rmat.emission = Color("#00E5FF")
	rmat.emission_energy_multiplier = 1.65
	ring.material_override = rmat
	_stage_container.add_child(ring)

	# Floor Deck
	var deck: MeshInstance3D = MeshInstance3D.new()
	var dmesh: CylinderMesh = CylinderMesh.new()
	dmesh.top_radius = 5.5
	dmesh.bottom_radius = 5.6
	dmesh.height = 0.14
	dmesh.radial_segments = 16
	deck.mesh = dmesh
	deck.position = Vector3(0.0, -0.14, 0.0)
	var dmat: StandardMaterial3D = StandardMaterial3D.new()
	dmat.albedo_color = Color("#141920")
	dmat.roughness = 0.55
	dmat.metallic = 0.25
	deck.material_override = dmat
	_stage_container.add_child(deck)

	# Residential Atrium Vista Backdrop
	var backdrop: MeshInstance3D = MeshInstance3D.new()
	var qmesh: QuadMesh = QuadMesh.new()
	qmesh.size = Vector2(12.0, 7.0)
	backdrop.mesh = qmesh
	backdrop.position = Vector3(-0.9, 1.6, -4.2)
	backdrop.rotation_degrees = Vector3(0.0, 20.0, 0.0)
	var vmat: StandardMaterial3D = StandardMaterial3D.new()
	var vtex: Texture2D = _load_tex("vista_oneill_cylinder_interior.png")
	if vtex != null:
		vmat.albedo_texture = vtex
		vmat.albedo_color = Color(0.42, 0.52, 0.64, 1.0)
		vmat.emission_enabled = true
		vmat.emission_texture = vtex
		vmat.emission_energy_multiplier = 0.35
	else:
		vmat.albedo_color = Color("#101A26")
	vmat.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	vmat.cull_mode = BaseMaterial3D.CULL_DISABLED
	backdrop.material_override = vmat
	backdrop.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	_stage_container.add_child(backdrop)


func _setup_lighting(idx: int) -> void:
	for ch: Node in _lights_container.get_children():
		ch.free()

	var key_light: DirectionalLight3D = DirectionalLight3D.new()
	key_light.name = "WarmStudioKeyLight"
	key_light.rotation_degrees = Vector3(-36.0, 32.0, 0.0)
	key_light.light_color = Color("#FFF0D8")
	key_light.light_energy = 1.30
	key_light.shadow_enabled = true
	key_light.shadow_blur = 1.2
	key_light.shadow_bias = 0.01
	_lights_container.add_child(key_light)

	var fill_light: DirectionalLight3D = DirectionalLight3D.new()
	fill_light.name = "SoftFrontLeftFill"
	fill_light.rotation_degrees = Vector3(-18.0, -42.0, 0.0)
	fill_light.light_color = Color("#D0E6F8")
	fill_light.light_energy = 0.68
	fill_light.shadow_enabled = false
	_lights_container.add_child(fill_light)

	var rim_light: DirectionalLight3D = DirectionalLight3D.new()
	rim_light.name = "BackRimKicker"
	rim_light.rotation_degrees = Vector3(-22.0, -148.0, 0.0)
	rim_light.light_color = Color("#5CE1E6") if (idx % 2 == 0) else Color("#FFB703")
	rim_light.light_energy = 1.05
	rim_light.shadow_enabled = false
	_lights_container.add_child(rim_light)

	var eye_catch: OmniLight3D = OmniLight3D.new()
	eye_catch.name = "BinocularLensCatchlight"
	eye_catch.position = Vector3(0.45, 0.98, 1.10)
	eye_catch.light_color = Color("#FFF8EC")
	eye_catch.light_energy = 0.55
	eye_catch.omni_range = 3.5
	_lights_container.add_child(eye_catch)


func _find_bot_glb(names: Array) -> String:
	for d: String in BOT_GLB_DIRS:
		for n in names:
			var p: String = d + "/" + String(n)
			if FileAccess.file_exists(p):
				return p
	return ""


func _build_render_queue() -> void:
	_render_queue.clear()

	# 1. 5 Distinct *WALL-E* x *Johnny 5* Robot Design Candidates (`char_bot_johnny5_r1_01..05.glb`)
	var fallback_factions := [
		"char_johnny5_sprocket_yellow.glb",
		"char_bot_johnny5.glb",
		"char_johnny5_puddle_cyan.glb",
		"char_johnny5_clover_green.glb",
		"char_johnny5_sweep_teal.glb"
	]
	for cidx: int in range(1, 6):
		var glb_p: String = _find_bot_glb([
			"char_bot_johnny5_r1_%02d.glb" % cidx,
			"char_johnny5_r1_%02d.glb" % cidx,
			"johnny5_bot_r1_%02d.glb" % cidx,
			fallback_factions[cidx - 1]
		])
		if glb_p != "":
			_render_queue.append({
				"idx": cidx,
				"out_main": "char_bot_johnny5_r1_%02d" % cidx,
				"out_alt": "johnny5_bot_r1_%02d" % cidx,
				"glb_path": glb_p,
				"anim": "GreetAndPoint" if cidx == 2 else "IdleCurious"
			})

	# 2. 4 Faction Color Liveries on the Shared Chassis (`Sprocket #0419`, `Sweep #0812`, `Puddle #0204`, `Clover #0631`)
	var livery_specs := [
		{"idx": 1, "out": "johnny5_livery_01_sprocket", "alt": "utility_bot_r2_05_livery_01_sprocket", "files": ["char_johnny5_sprocket_yellow.glb", "char_bot_johnny5.glb"], "anim": "GreetAndPoint"},
		{"idx": 2, "out": "johnny5_livery_02_sweep", "alt": "utility_bot_r2_05_livery_02_sweep", "files": ["char_johnny5_sweep_teal.glb", "char_johnny5_bumper_teal.glb"], "anim": "IdleCurious"},
		{"idx": 3, "out": "johnny5_livery_03_puddle", "alt": "utility_bot_r2_05_livery_03_puddle", "files": ["char_johnny5_puddle_cyan.glb", "char_johnny5_valve_blue.glb"], "anim": "DiagnosticPoint"},
		{"idx": 4, "out": "johnny5_livery_04_clover", "alt": "utility_bot_r2_05_livery_04_clover", "files": ["char_johnny5_clover_green.glb"], "anim": "Celebrate"}
	]
	for ls: Dictionary in livery_specs:
		var lp: String = _find_bot_glb(ls["files"] as Array)
		if lp != "":
			_render_queue.append({
				"idx": int(ls["idx"]),
				"out_main": String(ls["out"]),
				"out_alt": String(ls["alt"]),
				"glb_path": lp,
				"anim": String(ls["anim"])
			})


func _load_entry(entry: Dictionary) -> void:
	for ch: Node in _bot_container.get_children():
		ch.free()

	_setup_lighting(int(entry["idx"]))
	var glb_path: String = String(entry["glb_path"])
	if not FileAccess.file_exists(glb_path):
		return

	var doc: GLTFDocument = GLTFDocument.new()
	var state: GLTFState = GLTFState.new()
	if doc.append_from_file(glb_path, state) == OK:
		var root: Node = doc.generate_scene(state)
		if root is Node3D:
			var n3d: Node3D = root as Node3D
			n3d.name = String(entry["out_main"])
			_bot_container.add_child(n3d)
			_upgrade_bot_materials(n3d)
			_pose_bot(n3d, String(entry["anim"]))
			_frame_bot_camera()


func _pose_bot(root: Node3D, preferred_anim: String) -> void:
	var stack: Array[Node] = [root]
	while not stack.is_empty():
		var curr: Node = stack.pop_back()
		if curr is AnimationPlayer:
			var ap: AnimationPlayer = curr as AnimationPlayer
			var alist: PackedStringArray = ap.get_animation_list()
			for pname: String in [preferred_anim, "GreetAndPoint", "IdleCurious", "Celebrate", "Idle"]:
				if alist.has(pname):
					ap.play(pname)
					ap.seek(0.65, true)
					ap.advance(0.0)
					ap.speed_scale = 0.0
					return
		for ch: Node in curr.get_children():
			stack.append(ch)


func _frame_bot_camera() -> void:
	if _camera == null:
		return
	# 3/4 Front Portrait/Full-Body Framing in FRONT (+Z) of the binocular eyes (`Y = 0.85m..1.05m`)
	_camera.near = 0.02
	_camera.far = 100.0
	_camera.fov = 34.0
	_camera.global_position = Vector3(0.76, 0.88, 1.54)
	_camera.look_at(Vector3(0.0, 0.56, 0.02), Vector3.UP)


func _upgrade_bot_materials(root: Node3D) -> void:
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

	var tex_j5_alb: Texture2D = _load_tex("johnny5_utility_bot_atlas_albedo.png")
	var tex_j5_orm: Texture2D = _load_tex("johnny5_utility_bot_atlas_orm.png")
	var tex_j5_nrm: Texture2D = _load_tex("johnny5_utility_bot_atlas_normal.png")
	var tex_j5_emi: Texture2D = _load_tex("johnny5_utility_bot_atlas_emission.png")
	var tex_j5_lns: Texture2D = _load_tex("johnny5_optic_lens_translucent.png")

	var tex_r2_alb: Texture2D = _load_tex("utility_bot_round2_atlas_albedo.png")
	var tex_r2_orm: Texture2D = _load_tex("utility_bot_round2_atlas_orm.png")
	var tex_r2_nrm: Texture2D = _load_tex("utility_bot_round2_atlas_normal.png")
	var tex_r2_emi: Texture2D = _load_tex("utility_bot_round2_atlas_emission.png")
	var tex_r2_vis: Texture2D = _load_tex("utility_bot_round2_visor_translucent.png")

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

						if mname.contains("lens") or mname.contains("visor") or mname.contains("translucent") or mname.contains("glass") or pname.contains("lens") or pname.contains("visor"):
							smat.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
							smat.albedo_color.a = clampf(smat.albedo_color.a, 0.22, 0.34)
							if mname.contains("r2") and tex_r2_vis != null:
								smat.albedo_texture = tex_r2_vis
							elif tex_j5_lns != null and smat.albedo_texture == null:
								smat.albedo_texture = tex_j5_lns
							smat.roughness = 0.06
							smat.metallic = 0.20
							smat.metallic_specular = 0.95
							mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
						elif mname.contains("utilitybotr2") or mname.contains("round2"):
							if tex_r2_alb != null:
								smat.albedo_texture = tex_r2_alb
							if tex_r2_nrm != null:
								smat.normal_enabled = true
								smat.normal_texture = tex_r2_nrm
								smat.normal_scale = 0.65
							if tex_r2_orm != null:
								smat.ao_enabled = true
								smat.ao_texture = tex_r2_orm
							if tex_r2_emi != null:
								smat.emission_enabled = true
								smat.emission_texture = tex_r2_emi
								smat.emission_operator = BaseMaterial3D.EMISSION_OP_MULTIPLY
								smat.emission = Color(1.0, 1.0, 1.0)
								smat.emission_energy_multiplier = 1.65
						elif mname.contains("johnny5") or mname.contains("bot_atlas"):
							if tex_j5_alb != null:
								smat.albedo_texture = tex_j5_alb
							if tex_j5_nrm != null:
								smat.normal_enabled = true
								smat.normal_texture = tex_j5_nrm
								smat.normal_scale = 0.65
							if tex_j5_orm != null:
								smat.ao_enabled = true
								smat.ao_texture = tex_j5_orm
							if tex_j5_emi != null:
								smat.emission_enabled = true
								smat.emission_texture = tex_j5_emi
								smat.emission_operator = BaseMaterial3D.EMISSION_OP_MULTIPLY
								smat.emission = Color(1.0, 1.0, 1.0)
								smat.emission_energy_multiplier = 1.65
						elif smat.emission_enabled or mname.contains("emissive") or mname.contains("led") or mname.contains("cyan") or mname.contains("amber"):
							smat.emission_enabled = true
							if smat.emission == Color(0, 0, 0, 1):
								smat.emission = smat.albedo_color
							smat.emission_energy_multiplier = 1.85

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
	if _render_step >= _render_queue.size():
		print("[Johnny5BotShowcase] Completed all ", _render_queue.size(), " Johnny-5 bot renders!")
		get_tree().quit(0)
		return
	if _render_wait == 0:
		_load_entry(_render_queue[_render_step])
		_render_wait = 1
		return
	_render_wait += 1
	if _render_wait >= 6:
		var entry: Dictionary = _render_queue[_render_step]
		var out_main: String = String(entry["out_main"])
		var out_alt: String = String(entry["out_alt"])
		var img: Image = get_viewport().get_texture().get_image()
		if img != null and not img.is_empty():
			for out_dir: String in OUT_DIRS:
				DirAccess.make_dir_recursive_absolute(out_dir)
				var f1: String = out_dir + "/" + out_main + ".png"
				var f2: String = out_dir + "/" + out_alt + ".png"
				if img.save_png(f1) == OK:
					print("[Johnny5BotShowcase] Saved ", f1)
				if f2 != f1:
					img.save_png(f2)
		_render_step += 1
		_render_wait = 0
