class_name WristRfidShowcase
extends Node3D
## Godot 4.3 5-Candidate Embedded Wrist RFID / Center-Screen Hand-Rig Showcase & Batch Renderer
## Renders `prop_wrist_rfid_r1_01.glb` .. `prop_wrist_rfid_r1_05.glb` with Sloane's 4-Quadrant PBR Atlas
## (`wrist_rfid_atlas_albedo.png`, `wrist_rfid_atlas_orm.png`, `wrist_rfid_atlas_normal.png`,
##  `wrist_rfid_atlas_emission.png`, `wrist_rfid_holo_translucent.png` with `TRANSPARENCY_ALPHA`)
## and Center-Screen Raised Wrist Spotlight (`#D8F6FF`, `emission_energy_multiplier = 2.4`).

const WRIST_GLB_DIRS := [
	"res://assets/models/props/wrist_rfid",
	"res://../assets/glb/props/wrist_rfid",
	"res://../assets/glb/wrist_rfid",
	"res://../assets/glb/props"
]
const TEX_DIRS := [
	"res://../assets/textures/wrist_rfid",
	"res://../assets/textures/preface",
	"res://../assets/textures",
	"res://../assets/textures/character",
	"res://../assets/textures/cylinder_interior"
]

const OUT_DIRS := [
	"res://renders/wrist_rfid",
	"res://renders/props/wrist_rfid",
	"res://renders/preface",
	"res://../assets/renders/wrist_rfid",
	"res://../assets/renders/props/wrist_rfid",
	"res://../assets/renders/preface"
]

var _stage_container: Node3D
var _prop_container: Node3D
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
	_prop_container = get_node_or_null("PropContainer") as Node3D
	_lights_container = get_node_or_null("LightingRig") as Node3D

	if _stage_container == null:
		_stage_container = Node3D.new()
		_stage_container.name = "ShowcaseStage"
		add_child(_stage_container)
	if _prop_container == null:
		_prop_container = Node3D.new()
		_prop_container.name = "PropContainer"
		add_child(_prop_container)
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
		_load_candidate(_render_queue[0])


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

	# 1. Precision Aegis-7 Inductive Calibration Pad beneath the raised wrist rig
	var plinth: MeshInstance3D = MeshInstance3D.new()
	var cmesh: CylinderMesh = CylinderMesh.new()
	cmesh.top_radius = 0.34
	cmesh.bottom_radius = 0.38
	cmesh.height = 0.025
	cmesh.radial_segments = 8
	plinth.mesh = cmesh
	plinth.position = Vector3(0.0, -0.025, 0.0)
	var pmat: StandardMaterial3D = StandardMaterial3D.new()
	pmat.albedo_color = Color("#1A2028")
	pmat.roughness = 0.36
	pmat.metallic = 0.65
	plinth.material_override = pmat
	_stage_container.add_child(plinth)

	# Glowing Cyan RFID Target Ring on the calibration pad
	var ring: MeshInstance3D = MeshInstance3D.new()
	var rmesh: CylinderMesh = CylinderMesh.new()
	rmesh.top_radius = 0.24
	rmesh.bottom_radius = 0.25
	rmesh.height = 0.004
	rmesh.radial_segments = 24
	ring.mesh = rmesh
	ring.position = Vector3(0.0, -0.011, 0.0)
	var rmat: StandardMaterial3D = StandardMaterial3D.new()
	rmat.albedo_color = Color("#00E5FF")
	rmat.emission_enabled = true
	rmat.emission = Color("#00E5FF")
	rmat.emission_energy_multiplier = 1.65
	ring.material_override = rmat
	_stage_container.add_child(ring)

	# Soft Vestibule Backdrop behind the raised hand
	var backdrop: MeshInstance3D = MeshInstance3D.new()
	var qmesh: QuadMesh = QuadMesh.new()
	qmesh.size = Vector2(2.6, 1.6)
	backdrop.mesh = qmesh
	backdrop.position = Vector3(-0.18, 0.14, -0.95)
	backdrop.rotation_degrees = Vector3(0.0, 18.0, 0.0)
	var vmat: StandardMaterial3D = StandardMaterial3D.new()
	var vtex: Texture2D = _load_tex("vista_oneill_cylinder_interior.png")
	if vtex != null:
		vmat.albedo_texture = vtex
		vmat.albedo_color = Color(0.26, 0.36, 0.48, 1.0)
		vmat.emission_enabled = true
		vmat.emission_texture = vtex
		vmat.emission_energy_multiplier = 0.24
	else:
		vmat.albedo_color = Color("#0E1824")
	vmat.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	vmat.cull_mode = BaseMaterial3D.CULL_DISABLED
	backdrop.material_override = vmat
	backdrop.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	_stage_container.add_child(backdrop)


func _setup_lighting(cidx: int) -> void:
	for ch: Node in _lights_container.get_children():
		ch.free()

	# 1. Sloane's Center-Screen Raised Wrist Key SpotLight3D (`#D8F6FF`, energy = 1.10, spot_angle = 32°)
	var wrist_spot: SpotLight3D = SpotLight3D.new()
	wrist_spot.name = "CenterScreenWristKeySpot"
	wrist_spot.position = Vector3(0.32, 0.48, 0.45)
	wrist_spot.light_color = Color("#D8F6FF")
	wrist_spot.light_energy = 1.25
	wrist_spot.spot_range = 2.5
	wrist_spot.spot_angle = 36.0
	wrist_spot.shadow_enabled = true
	_lights_container.add_child(wrist_spot)
	wrist_spot.look_at_from_position(Vector3(0.32, 0.48, 0.45), Vector3(0.0, 0.08, 0.0), Vector3.UP)

	# 2. Warm 5500K Promenade Sun Key (`#FFF5E4`) for skin & metallic chamfer definition
	var sun_key: DirectionalLight3D = DirectionalLight3D.new()
	sun_key.name = "PromenadeWarmSunKey"
	sun_key.rotation_degrees = Vector3(-42.0, 34.0, 0.0)
	sun_key.light_color = Color("#FFF5E4")
	sun_key.light_energy = 1.15
	sun_key.shadow_enabled = true
	sun_key.shadow_bias = 0.005
	_lights_container.add_child(sun_key)

	# 3. Cool Cyan Rim Kicker (`#00E5FF`)
	var rim_dir: DirectionalLight3D = DirectionalLight3D.new()
	rim_dir.name = "CyanFresnelRimKicker"
	rim_dir.rotation_degrees = Vector3(-24.0, -142.0, 0.0)
	rim_dir.light_color = Color("#5CE1E6") if cidx != 3 else Color("#FFB703")
	rim_dir.light_energy = 0.95
	rim_dir.shadow_enabled = false
	_lights_container.add_child(rim_dir)

	# 4. Soft Under-Palm Fill (`#E8F1F8`)
	var fill_omni: OmniLight3D = OmniLight3D.new()
	fill_omni.name = "SoftVestibuleFillOmni"
	fill_omni.position = Vector3(-0.28, 0.25, 0.38)
	fill_omni.light_color = Color("#E8F1F8")
	fill_omni.light_energy = 0.65
	fill_omni.omni_range = 2.2
	_lights_container.add_child(fill_omni)


func _find_cand_glb(cidx: int) -> String:
	var names := [
		"prop_wrist_rfid_r1_%02d.glb" % cidx,
		"wrist_rfid_r1_%02d.glb" % cidx
	]
	for d: String in WRIST_GLB_DIRS:
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
				"cand_name": "prop_wrist_rfid_r1_%02d" % cidx,
				"short_name": "wrist_rfid_r1_%02d" % cidx,
				"glb_path": glb_path
			})


func _load_candidate(entry: Dictionary) -> void:
	for ch: Node in _prop_container.get_children():
		ch.free()

	var cidx: int = int(entry["cand_idx"])
	_setup_lighting(cidx)

	var glb_path: String = String(entry["glb_path"])
	if not FileAccess.file_exists(glb_path):
		return

	var doc: GLTFDocument = GLTFDocument.new()
	var state: GLTFState = GLTFState.new()
	if doc.append_from_file(glb_path, state) == OK:
		var root: Node = doc.generate_scene(state)
		if root is Node3D:
			var n3d: Node3D = root as Node3D
			n3d.name = String(entry["cand_name"])
			_prop_container.add_child(n3d)
			_upgrade_wrist_materials(n3d)
			_seek_wrist_animation(n3d)
			_frame_wrist_camera(n3d)


func _seek_wrist_animation(root: Node3D) -> void:
	var stack: Array[Node] = [root]
	while not stack.is_empty():
		var curr: Node = stack.pop_back()
		if curr is AnimationPlayer:
			var ap: AnimationPlayer = curr as AnimationPlayer
			var alist: PackedStringArray = ap.get_animation_list()
			for pref: String in ["RFIDPulse", "WristRaiseInspect", "Scan"]:
				if alist.has(pref):
					ap.play(pref)
					ap.seek(0.45, true)
					ap.advance(0.0)
					ap.speed_scale = 0.0
					return
		for ch: Node in curr.get_children():
			stack.append(ch)


func _frame_wrist_camera(root: Node3D) -> void:
	if _camera == null:
		return
	var min_v := Vector3(99999.0, 99999.0, 99999.0)
	var max_v := Vector3(-99999.0, -99999.0, -99999.0)
	var found: bool = false

	var stack: Array[Node] = [root]
	while not stack.is_empty():
		var curr: Node = stack.pop_back()
		if curr is MeshInstance3D:
			var mi: MeshInstance3D = curr as MeshInstance3D
			if mi.mesh != null:
				var aabb: AABB = mi.mesh.get_aabb()
				var xf: Transform3D = root.global_transform.affine_inverse() * mi.global_transform
				for i: int in range(8):
					var pt: Vector3 = xf * aabb.get_endpoint(i)
					min_v = min_v.min(pt)
					max_v = max_v.max(pt)
					found = true
		for ch: Node in curr.get_children():
			stack.append(ch)

	if not found:
		min_v = Vector3(-0.08, 0.0, -0.21)
		max_v = Vector3(0.08, 0.14, 0.21)

	var center: Vector3 = (min_v + max_v) * 0.5
	var sz: Vector3 = max_v - min_v
	var max_dim: float = maxf(sz.x, maxf(sz.y, sz.z))
	var dist: float = clampf(max_dim * 1.38, 0.34, 0.78)

	# 3/4 Elevated Dorsal Inspection View so subdermal dorsal vein-nodes, 68/32 split-cuff,
	# and floating translucent sapphire holo rings are front-and-center!
	_camera.near = 0.01
	_camera.far = 100.0
	_camera.fov = 33.0
	var cam_pos := Vector3(center.x + dist * 0.62, center.y + dist * 0.64, center.z + dist * 0.72)
	var look_target := Vector3(center.x, center.y + sz.y * 0.06, center.z)
	_camera.global_position = cam_pos
	_camera.look_at(look_target, Vector3.UP)


func _upgrade_wrist_materials(root: Node3D) -> void:
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

	var tex_albedo: Texture2D = _load_tex("wrist_rfid_atlas_albedo.png")
	var tex_orm: Texture2D = _load_tex("wrist_rfid_atlas_orm.png")
	var tex_norm: Texture2D = _load_tex("wrist_rfid_atlas_normal.png")
	var tex_emis: Texture2D = _load_tex("wrist_rfid_atlas_emission.png")
	var tex_holo: Texture2D = _load_tex("wrist_rfid_holo_translucent.png")

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

						if mname.contains("holo") or mname.contains("sapphire") or mname.contains("translucent") or mname.contains("glass") or mname.contains("lens") or pname.contains("holo") or pname.contains("lens"):
							smat.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
							smat.albedo_color.a = clampf(smat.albedo_color.a, 0.28, 0.44)
							if tex_holo != null:
								smat.albedo_texture = tex_holo
								smat.emission_texture = tex_holo
							smat.roughness = 0.06
							smat.metallic = 0.18
							smat.metallic_specular = 0.92
							smat.emission_enabled = true
							if smat.emission == Color(0, 0, 0, 1):
								smat.emission = Color("#00E5FF")
							smat.emission_energy_multiplier = 1.65
							mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
						elif mname.contains("wrist") or mname.contains("atlas") or mname.contains("subdermal") or mname.contains("cuff") or mname.contains("glove"):
							if tex_albedo != null and smat.albedo_texture == null:
								smat.albedo_texture = tex_albedo
							if tex_norm != null:
								smat.normal_enabled = true
								smat.normal_texture = tex_norm
								smat.normal_scale = 0.65
							if tex_orm != null:
								smat.ao_enabled = true
								smat.ao_texture = tex_orm
							if tex_emis != null:
								smat.emission_enabled = true
								smat.emission_texture = tex_emis
								smat.emission = Color(1.0, 1.0, 1.0)
								smat.emission_operator = BaseMaterial3D.EMISSION_OP_MULTIPLY
								smat.emission_energy_multiplier = 2.4
						elif smat.emission_enabled or mname.contains("emissive") or mname.contains("led") or mname.contains("vein") or mname.contains("node") or mname.contains("cyan") or mname.contains("amber") or mname.contains("emerald"):
							smat.emission_enabled = true
							if smat.emission == Color(0, 0, 0, 1):
								smat.emission = smat.albedo_color
							smat.emission_energy_multiplier = 2.4

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
		print("[WristRfidShowcase] Completed all ", _render_queue.size(), " wrist RFID renders!")
		get_tree().quit(0)
		return
	if _render_wait == 0:
		_load_candidate(_render_queue[_render_step])
		_render_wait = 1
		return
	_render_wait += 1
	if _render_wait >= 6:
		var entry: Dictionary = _render_queue[_render_step]
		var cname: String = String(entry["cand_name"])
		var sname: String = String(entry["short_name"])
		var img: Image = get_viewport().get_texture().get_image()
		if img != null and not img.is_empty():
			for out_dir: String in OUT_DIRS:
				DirAccess.make_dir_recursive_absolute(out_dir)
				var f1: String = out_dir + "/" + cname + ".png"
				var f2: String = out_dir + "/" + sname + ".png"
				if img.save_png(f1) == OK:
					print("[WristRfidShowcase] Saved ", f1)
				img.save_png(f2)
		_render_step += 1
		_render_wait = 0
