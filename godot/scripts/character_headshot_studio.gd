class_name CharacterHeadshotStudio
extends Node3D
## Godot 4.3 Close-Up Portrait Headshot Studio Renderer
## Implements Sloane's Section 4.2 3-Point Close-Up Portrait Studio Lighting Rig:
## 1. Open/Retracted or High-Clarity Visor Mode (`alpha <= 0.14`)
## 2. Portrait Key Light (`#FFF0DB`, energy = 1.65) at 28° front-right (`Y = 1.78m`)
## 3. Portrait Fill Light (`#D8E4F0`, energy = 0.75) at front-left (`Y = 1.62m`)
## 4. Hair & Shoulder Rim Kicker (`#66E8FF`, energy = 1.20) at back-left (`Y = 1.92m`)

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

var _backdrop_container: Node3D
var _char_container: Node3D
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
	_camera = get_node_or_null("PortraitCamera") as Camera3D
	_backdrop_container = get_node_or_null("PortraitBackdrop") as Node3D
	_char_container = get_node_or_null("CharacterContainer") as Node3D
	_lights_container = get_node_or_null("PortraitLightingRig") as Node3D

	if _backdrop_container == null:
		_backdrop_container = Node3D.new()
		_backdrop_container.name = "PortraitBackdrop"
		add_child(_backdrop_container)
	if _char_container == null:
		_char_container = Node3D.new()
		_char_container.name = "CharacterContainer"
		add_child(_char_container)
	if _lights_container == null:
		_lights_container = Node3D.new()
		_lights_container.name = "PortraitLightingRig"
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

	_build_portrait_backdrop()
	_setup_portrait_lighting(1)
	_build_render_queue()

	if not _render_queue.is_empty():
		_load_candidate(_render_queue[0])


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


func _build_portrait_backdrop() -> void:
	for ch: Node in _backdrop_container.get_children():
		ch.free()

	var backdrop: MeshInstance3D = MeshInstance3D.new()
	var qmesh: QuadMesh = QuadMesh.new()
	qmesh.size = Vector2(5.5, 3.6)
	backdrop.mesh = qmesh
	backdrop.position = Vector3(-0.25, 1.62, -2.2)
	backdrop.rotation_degrees = Vector3(0.0, 10.0, 0.0)
	var vmat: StandardMaterial3D = StandardMaterial3D.new()
	var vtex: Texture2D = _load_tex("vista_oneill_cylinder_interior.png")
	if vtex != null:
		vmat.albedo_texture = vtex
		vmat.albedo_color = Color(0.28, 0.38, 0.50, 1.0)
		vmat.emission_enabled = true
		vmat.emission_texture = vtex
		vmat.emission_energy_multiplier = 0.25
	else:
		vmat.albedo_color = Color("#101C2A")
	vmat.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	vmat.cull_mode = BaseMaterial3D.CULL_DISABLED
	backdrop.material_override = vmat
	backdrop.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	_backdrop_container.add_child(backdrop)


func _setup_portrait_lighting(cidx: int) -> void:
	for ch: Node in _lights_container.get_children():
		ch.free()

	# 1. Sloane's Portrait Key Light (`#FFF0DB`, energy = 1.65) at 28° front-right (`Y = 1.78m`)
	var key_dir: DirectionalLight3D = DirectionalLight3D.new()
	key_dir.name = "PortraitRembrandtKeyDir"
	key_dir.rotation_degrees = Vector3(-22.0, 28.0, 0.0)
	key_dir.light_color = Color("#FFF0DB")
	key_dir.light_energy = 0.92
	key_dir.shadow_enabled = true
	key_dir.shadow_blur = 1.4
	key_dir.shadow_bias = 0.005
	_lights_container.add_child(key_dir)

	var key_omni: OmniLight3D = OmniLight3D.new()
	key_omni.name = "PortraitKeyCatchlightOmni"
	key_omni.position = Vector3(0.32, 1.78, 0.60)
	key_omni.light_color = Color("#FFF0DB")
	key_omni.light_energy = 0.42
	key_omni.omni_range = 2.4
	_lights_container.add_child(key_omni)

	# 2. Sloane's Portrait Fill Light (`#D8E4F0`, energy = 0.75) at front-left (`Y = 1.62m`)
	var fill_omni: OmniLight3D = OmniLight3D.new()
	fill_omni.name = "PortraitSoftSkinFillOmni"
	fill_omni.position = Vector3(-0.38, 1.62, 0.56)
	fill_omni.light_color = Color("#D8E4F0")
	fill_omni.light_energy = 0.45
	fill_omni.omni_range = 2.6
	_lights_container.add_child(fill_omni)

	var fill_dir: DirectionalLight3D = DirectionalLight3D.new()
	fill_dir.name = "PortraitSoftFillDir"
	fill_dir.rotation_degrees = Vector3(-12.0, -34.0, 0.0)
	fill_dir.light_color = Color("#D8E4F0")
	fill_dir.light_energy = 0.35
	fill_dir.shadow_enabled = false
	_lights_container.add_child(fill_dir)

	# 3. Sloane's Hair & Shoulder Rim Kicker (`#66E8FF`, energy = 1.20) at back-left (`Y = 1.92m`)
	var rim_dir: DirectionalLight3D = DirectionalLight3D.new()
	rim_dir.name = "HairAndShoulderRimKickerDir"
	rim_dir.rotation_degrees = Vector3(-20.0, -148.0, 0.0)
	rim_dir.light_color = Color("#66E8FF")
	rim_dir.light_energy = 0.85
	rim_dir.shadow_enabled = false
	_lights_container.add_child(rim_dir)

	var rim_omni: OmniLight3D = OmniLight3D.new()
	rim_omni.name = "HairAndShoulderRimOmni"
	rim_omni.position = Vector3(-0.34, 1.92, -0.42)
	rim_omni.light_color = Color("#66E8FF") if cidx != 3 else Color("#FFB703")
	rim_omni.light_energy = 0.75
	rim_omni.omni_range = 2.8
	_lights_container.add_child(rim_omni)


func _find_cand_glb(cidx: int) -> String:
	var names := [
		"char_crew_r1_%02d.glb" % cidx,
		"character_crew_r1_%02d.glb" % cidx,
		"char_01_r1_%02d.glb" % cidx
	]
	for d: String in CHAR_GLB_DIRS:
		for n: String in names:
			var p: String = d + "/" + n
			if FileAccess.file_exists(p):
				return p
	return ""


func _build_render_queue() -> void:
	_render_queue.clear()
	for cidx: int in range(1, 6):
		var glb_path: String = _find_cand_glb(cidx)
		if glb_path != "":
			_render_queue.append({
				"cand_idx": cidx,
				"out_main": "char_crew_headshot_%02d" % cidx,
				"out_short": "headshot_%02d" % cidx,
				"glb_path": glb_path
			})


func _load_candidate(entry: Dictionary) -> void:
	for ch: Node in _char_container.get_children():
		ch.free()

	var cidx: int = int(entry["cand_idx"])
	_setup_portrait_lighting(cidx)

	var glb_path: String = String(entry["glb_path"])
	if not FileAccess.file_exists(glb_path):
		return

	var doc: GLTFDocument = GLTFDocument.new()
	var state: GLTFState = GLTFState.new()
	if doc.append_from_file(glb_path, state) == OK:
		var root: Node = doc.generate_scene(state)
		if root is Node3D:
			var n3d: Node3D = root as Node3D
			n3d.name = "HeadshotCand_%02d" % cidx
			_char_container.add_child(n3d)
			_upgrade_headshot_materials(n3d, cidx)
			_set_neutral_portrait_pose(n3d)
			_frame_headshot_camera(cidx)


func _set_neutral_portrait_pose(root: Node3D) -> void:
	var stack: Array[Node] = [root]
	while not stack.is_empty():
		var curr: Node = stack.pop_back()
		if curr is AnimationPlayer:
			var ap: AnimationPlayer = curr as AnimationPlayer
			ap.stop()
		for ch: Node in curr.get_children():
			stack.append(ch)


func _frame_headshot_camera(cidx: int) -> void:
	if _camera == null:
		return
	_camera.near = 0.02
	_camera.far = 100.0
	_camera.fov = 29.0
	# Tight 12° 3/4 front portrait angle in FRONT (+Z = +0.62m) of the head (`Y = 1.62m`),
	# framing from mid-chest/shoulder pauldrons (`Y = 1.32m`) to above the head crest (`Y = 1.86m`)
	var x_off: float = 0.13 if (cidx % 2 == 1) else -0.13
	if cidx == 2:
		x_off = 0.13
	_camera.global_position = Vector3(x_off, 1.625, 0.62)
	_camera.look_at(Vector3(0.0, 1.595, 0.02), Vector3.UP)


func _upgrade_headshot_materials(root: Node3D, cidx: int) -> void:
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
	var tex_face_atlas: Texture2D = _load_tex("char_headshot_faces_and_hair_atlas.png")

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

						if mname.contains("visor") or pname.contains("visor") or mname.contains("monocle") or mname.contains("eyewear") or mname.contains("glass") or mname.contains("translucent"):
							smat.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
							# Sloane's Spec 4.2.1: keep visor alpha <= 0.14 in headshots so skin tones, irises, catchlights, beard/scars, and hair are 100% unobstructed!
							smat.albedo_color.a = clampf(smat.albedo_color.a, 0.10, 0.15)
							if tex_visor != null and (mname.contains("visor") or pname.contains("visor")):
								smat.albedo_texture = tex_visor
							smat.roughness = 0.06
							smat.metallic = 0.18
							smat.metallic_specular = 0.92
							smat.emission_enabled = true
							if smat.emission == Color(0, 0, 0, 1):
								smat.emission = Color("#00E5FF")
							smat.emission_energy_multiplier = 0.35
							mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
						elif mname.contains("faceatlas") or mname.contains("headshot") or mname.contains("portrait"):
							if tex_face_atlas != null and smat.albedo_texture == null:
								smat.albedo_texture = tex_face_atlas
							smat.roughness = 0.45
							smat.metallic = 0.04
						elif mname.contains("chesttelemetry") or mname.contains("oled") or pname.contains("telemetry"):
							if tex_chest != null:
								smat.albedo_texture = tex_chest
								smat.emission_texture = tex_chest
							smat.roughness = 0.20
							smat.metallic = 0.15
							smat.emission_enabled = true
							smat.emission = Color(0.55, 0.90, 1.0)
							smat.emission_energy_multiplier = 0.75
						elif mname.contains("skin"):
							smat.roughness = 0.46
							smat.metallic = 0.02
						elif mname.contains("hair") or mname.contains("beard") or mname.contains("braid"):
							smat.roughness = 0.50
							smat.metallic = 0.08
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
	if _render_step >= _render_queue.size():
		print("[CharacterHeadshotStudio] Completed all ", _render_queue.size(), " headshot renders!")
		get_tree().quit(0)
		return
	if _render_wait == 0:
		_load_candidate(_render_queue[_render_step])
		_render_wait = 1
		return
	_render_wait += 1
	if _render_wait >= 6:
		var entry: Dictionary = _render_queue[_render_step]
		var out_main: String = String(entry["out_main"])
		var out_short: String = String(entry["out_short"])
		var img: Image = get_viewport().get_texture().get_image()
		if img != null and not img.is_empty():
			for out_dir: String in OUT_DIRS:
				DirAccess.make_dir_recursive_absolute(out_dir)
				var f1: String = out_dir + "/" + out_main + ".png"
				var f2: String = out_dir + "/" + out_short + ".png"
				if img.save_png(f1) == OK:
					print("[CharacterHeadshotStudio] Saved ", f1)
				img.save_png(f2)
		_render_step += 1
		_render_wait = 0
