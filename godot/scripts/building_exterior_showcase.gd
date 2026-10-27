class_name BuildingExteriorShowcase
extends Node3D
## Parameterized Godot 4 Exterior Showcase & Batch Renderer ("Aegis-7 Exterior Standard")
## Supports:
## - bldg_01 .. bldg_20 (res://../assets/glb/buildings/bldg_XX/bldg_XX_r1_01..05.glb)
## - prop_01 .. prop_05 (res://../assets/glb/props/prop_XX/prop_XX_r1_01..05.glb)
## - cylinder (res://../assets/glb/cylinder/cylinder_r1_01..05.glb)

const BLDG_GLB_ROOT := "res://../assets/glb/buildings"
const PROP_GLB_ROOT := "res://../assets/glb/props"
const CYL_GLB_ROOT := "res://../assets/glb/cylinder"
const CYL_INT_GLB_ROOT := "res://../assets/glb/cylinder_interior"
const CYL_INT_TEX_DIR := "res://../assets/textures/cylinder_interior"
const SHARED_TEX_DIR := "res://../assets/textures"
const BLDG_TEX_DIR := "res://../assets/textures/buildings"

const GODOT_RENDERS_ROOT := "res://renders"
const ASSETS_RENDERS_ROOT := "res://../assets/renders"

var _stage_container: Node3D
var _model_container: Node3D
var _lights_container: Node3D
var _camera: Camera3D

var _tex_cache: Dictionary = {}
var _batch_render: bool = false
var _validate_only: bool = false
var _target_id: String = ""
var _render_queue: Array[Dictionary] = []
var _frame_counter: int = 0
var _render_step: int = 0
var _render_wait: int = 0


func _ready() -> void:
	_camera = get_node_or_null("ShowcaseCamera") as Camera3D
	_stage_container = get_node_or_null("ExteriorStage") as Node3D
	_model_container = get_node_or_null("BuildingContainer") as Node3D
	_lights_container = get_node_or_null("LightingRig") as Node3D

	if _stage_container == null:
		_stage_container = Node3D.new()
		_stage_container.name = "ExteriorStage"
		add_child(_stage_container)
	if _model_container == null:
		_model_container = Node3D.new()
		_model_container.name = "BuildingContainer"
		add_child(_model_container)
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
		elif arg.begins_with("--bldg="):
			_target_id = arg.substr(7)
		elif arg.begins_with("--target="):
			_target_id = arg.substr(9)

	if OS.get_environment("TARGET_BLDG") != "":
		_target_id = OS.get_environment("TARGET_BLDG")
	if OS.get_environment("RENDER_ALL") == "1" or OS.get_environment("CAPTURE_SCREENSHOTS") == "1":
		_batch_render = true
	if OS.get_environment("VALIDATE_ONLY") == "1":
		_validate_only = true

	if DisplayServer.get_name() == "headless" and not _batch_render:
		_validate_only = true

	_build_exterior_stage()
	_setup_lighting_rig(1)
	_build_render_queue()

	if not _render_queue.is_empty():
		_load_candidate(_render_queue[0])


func _load_tex(fname: String) -> Texture2D:
	if _tex_cache.has(fname):
		return _tex_cache[fname] as Texture2D
	for d: String in [CYL_INT_TEX_DIR, BLDG_TEX_DIR, SHARED_TEX_DIR, SHARED_TEX_DIR + "/bunk_round2"]:
		var p: String = d + "/" + fname
		if FileAccess.file_exists(p):
			var img: Image = Image.new()
			if img.load(p) == OK and not img.is_empty():
				img.generate_mipmaps()
				var tex: ImageTexture = ImageTexture.create_from_image(img)
				_tex_cache[fname] = tex
				return tex
	return null


func _build_exterior_stage() -> void:
	for ch: Node in _stage_container.get_children():
		ch.free()

	var plaza: MeshInstance3D = MeshInstance3D.new()
	plaza.name = "AegisPlazaDeck"
	var pmesh: CylinderMesh = CylinderMesh.new()
	pmesh.top_radius = 28.0
	pmesh.bottom_radius = 29.0
	pmesh.height = 0.6
	pmesh.radial_segments = 16
	plaza.mesh = pmesh
	plaza.position = Vector3(0.0, -0.30, 0.0)
	var pmat: StandardMaterial3D = StandardMaterial3D.new()
	pmat.albedo_color = Color("#161B22")
	pmat.metallic = 0.35
	pmat.roughness = 0.42
	var dtex: Texture2D = _load_tex("carbon_slate_frame.png")
	if dtex != null:
		pmat.albedo_texture = dtex
		pmat.uv1_scale = Vector3(8.0, 8.0, 1.0)
	plaza.material_override = pmat
	_stage_container.add_child(plaza)

	var pad_ring: MeshInstance3D = MeshInstance3D.new()
	pad_ring.name = "PlazaOctagonalPad"
	var rmesh: CylinderMesh = CylinderMesh.new()
	rmesh.top_radius = 9.5
	rmesh.bottom_radius = 9.8
	rmesh.height = 0.08
	rmesh.radial_segments = 8
	pad_ring.mesh = rmesh
	pad_ring.position = Vector3(0.0, 0.02, 0.0)
	var rmat: StandardMaterial3D = StandardMaterial3D.new()
	rmat.albedo_color = Color("#1F2630")
	rmat.metallic = 0.55
	rmat.roughness = 0.32
	pad_ring.material_override = rmat
	_stage_container.add_child(pad_ring)

	var backdrop: MeshInstance3D = MeshInstance3D.new()
	backdrop.name = "ONeillCylinderSkyBackdrop"
	var qmesh: QuadMesh = QuadMesh.new()
	qmesh.size = Vector2(96.0, 54.0)
	backdrop.mesh = qmesh
	backdrop.position = Vector3(-10.0, 16.0, -26.0)
	backdrop.rotation_degrees = Vector3(0.0, 18.0, 0.0)
	var vmat: StandardMaterial3D = StandardMaterial3D.new()
	var vtex: Texture2D = _load_tex("vista_oneill_cylinder_interior.png")
	if vtex != null:
		vmat.albedo_texture = vtex
		vmat.emission_enabled = true
		vmat.emission_texture = vtex
		vmat.emission_energy_multiplier = 1.15
	else:
		vmat.albedo_color = Color("#0F1E2E")
	vmat.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	vmat.cull_mode = BaseMaterial3D.CULL_DISABLED
	backdrop.material_override = vmat
	backdrop.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	_stage_container.add_child(backdrop)


func _setup_lighting_rig(bldg_idx: int) -> void:
	for ch: Node in _lights_container.get_children():
		ch.free()

	var sun: DirectionalLight3D = DirectionalLight3D.new()
	sun.name = "SolarMirrorKeyLight"
	sun.rotation_degrees = Vector3(-42.0, 35.0, 0.0)
	sun.light_color = Color("#FFF6E8")
	sun.light_energy = 1.35
	sun.shadow_enabled = true
	sun.shadow_bias = 0.02
	_lights_container.add_child(sun)

	var fill: DirectionalLight3D = DirectionalLight3D.new()
	fill.name = "CylinderEarthlightBounceFill"
	fill.rotation_degrees = Vector3(-25.0, -140.0, 0.0)
	fill.light_color = Color("#7CC8FF")
	fill.light_energy = 0.55
	fill.shadow_enabled = false
	_lights_container.add_child(fill)

	var rim: DirectionalLight3D = DirectionalLight3D.new()
	rim.name = "ArchitecturalRimBacklight"
	rim.rotation_degrees = Vector3(-15.0, 165.0, 0.0)
	rim.light_color = Color("#00E5FF")
	rim.light_energy = 0.40
	rim.shadow_enabled = false
	_lights_container.add_child(rim)

	_add_omni("PlazaCyanRim_Front", Vector3(8.5, 4.5, 9.5), Color("#00E5FF"), 1.65, 22.0)
	_add_omni("AtriumInternalGlow", Vector3(2.2, 7.5, 1.5), Color("#00E5FF"), 1.85, 18.0)
	_add_omni("PlazaAmberPerimeter", Vector3(-7.5, 2.5, 8.5), Color("#FF9500"), 1.45, 18.0)
	var accent_col: Color = Color("#7B5CFF") if (bldg_idx in [3, 4, 5, 6, 10, 12, 17, 18, 20]) else Color("#00E5FF")
	_add_omni("SpireCrownAccent", Vector3(1.5, 14.5, 2.5), accent_col, 1.65, 20.0)


func _add_omni(lname: String, pos: Vector3, col: Color, energy: float, rng: float) -> OmniLight3D:
	var omni: OmniLight3D = OmniLight3D.new()
	omni.name = lname
	omni.position = pos
	omni.light_color = col
	omni.light_energy = energy
	omni.omni_range = rng
	_lights_container.add_child(omni)
	return omni


func _build_render_queue() -> void:
	_render_queue.clear()
	var targets: Array[String] = []
	if _target_id == "setpieces" or _target_id == "interior_setpieces":
		for i: int in range(1, 6):
			targets.append("interior_setpiece_%02d" % i)
	elif _target_id == "phase3":
		for i: int in range(1, 6):
			targets.append("prop_%02d" % i)
		for i: int in range(16, 21):
			targets.append("bldg_%02d" % i)
	elif _target_id != "":
		targets.append(_target_id)
	else:
		for i: int in range(1, 21):
			targets.append("bldg_%02d" % i)

	for tid: String in targets:
		if tid.begins_with("prop_"):
			var pidx: int = int(tid.substr(5, 2))
			for cidx: int in range(1, 6):
				var cname: String = "%s_r1_%02d" % [tid, cidx]
				var glb_path: String = "%s/%s/%s.glb" % [PROP_GLB_ROOT, tid, cname]
				if FileAccess.file_exists(glb_path):
					_render_queue.append({
						"category": "props",
						"item_id": tid,
						"item_idx": pidx,
						"cand_idx": cidx,
						"cand_name": cname,
						"glb_path": glb_path
					})
		elif tid.begins_with("interior_setpiece_"):
			var spidx: int = int(tid.substr(18, 2))
			for cidx: int in range(1, 6):
				var cname: String = "%s_r1_%02d" % [tid, cidx]
				var glb_path: String = "%s/setpiece_%02d/%s.glb" % [CYL_INT_GLB_ROOT, spidx, cname]
				if FileAccess.file_exists(glb_path):
					_render_queue.append({
						"category": "cylinder_interior",
						"item_id": tid,
						"item_idx": spidx,
						"cand_idx": cidx,
						"cand_name": cname,
						"glb_path": glb_path
					})
		elif tid == "cylinder" or tid == "cylinder_round1":
			for cidx: int in range(1, 6):
				var cname: String = "cylinder_r1_%02d" % cidx
				var glb_path: String = "%s/%s.glb" % [CYL_GLB_ROOT, cname]
				if FileAccess.file_exists(glb_path):
					_render_queue.append({
						"category": "cylinder",
						"item_id": "cylinder_round1",
						"item_idx": cidx,
						"cand_idx": cidx,
						"cand_name": cname,
						"glb_path": glb_path
					})
		else:
			var bidx: int = int(tid.substr(5, 2))
			for cidx: int in range(1, 6):
				var cname: String = "%s_r1_%02d" % [tid, cidx]
				var glb_path: String = "%s/%s/%s.glb" % [BLDG_GLB_ROOT, tid, cname]
				if FileAccess.file_exists(glb_path):
					_render_queue.append({
						"category": "buildings",
						"item_id": tid,
						"item_idx": bidx,
						"cand_idx": cidx,
						"cand_name": cname,
						"glb_path": glb_path
					})


func _load_candidate(entry: Dictionary) -> void:
	for ch: Node in _model_container.get_children():
		ch.free()

	_setup_lighting_rig(int(entry["item_idx"]))
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
			_model_container.add_child(n3d)
			_upgrade_materials(n3d)
			_frame_building_camera(n3d, String(entry["category"]))


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

						if mname.contains("glass") or mname.contains("translucent") or mname.contains("atrium") or mname.contains("dome") or pname.contains("glass") or pname.contains("curtain") or pname.contains("canopy"):
							smat.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
							smat.albedo_color.a = clampf(smat.albedo_color.a, 0.24, 0.34)
							smat.roughness = 0.08
							smat.metallic = 0.15
							smat.metallic_specular = 0.92
							mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
						elif mname.contains("oled") or mname.contains("sign") or mname.contains("beacon") or mname.contains("window_lit") or mname.contains("telemetry") or mname.contains("facade_lit"):
							smat.emission_enabled = true
							if smat.albedo_texture != null:
								smat.emission_texture = smat.albedo_texture
							if smat.emission == Color(0, 0, 0, 1):
								smat.emission = Color(0.20, 0.85, 1.0)
							smat.emission_energy_multiplier = 1.65
						elif smat.emission_enabled or mname.contains("emissive") or mname.contains("led") or mname.contains("plasma") or mname.contains("holo"):
							smat.emission_enabled = true
							if smat.emission == Color(0, 0, 0, 1):
								smat.emission = smat.albedo_color
							smat.emission_energy_multiplier = 2.0

						mi.set_surface_override_material(s_idx, smat)
		for ch: Node in curr.get_children():
			mstack.append(ch)


func _frame_building_camera(root: Node3D, category: String) -> void:
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
		min_v = Vector3(-6.0, 0.0, -5.0)
		max_v = Vector3(6.0, 18.0, 5.0)

	var center: Vector3 = (min_v + max_v) * 0.5
	var sz: Vector3 = max_v - min_v

	if category == "props":
		var max_dim: float = maxf(sz.x, maxf(sz.y, sz.z))
		var dist: float = clampf(max_dim * 1.48, 5.2, 16.5)
		var cam_pos := Vector3(center.x + dist * 0.62, center.y + sz.y * 0.28, center.z + dist * 0.82)
		var look_target := Vector3(center.x, center.y * 0.94, center.z)
		_camera.global_position = cam_pos
		_camera.fov = 38.0
		_camera.look_at(look_target, Vector3.UP)
	elif category == "cylinder_interior":
		_stage_container.visible = true
		_camera.far = 4000.0
		var max_dim: float = maxf(sz.x, maxf(sz.y, sz.z))
		var dist: float = clampf(max_dim * 1.15, 28.0, 78.0)
		var cam_pos := Vector3(center.x + dist * 0.65, center.y + sz.y * 0.45, center.z + dist * 0.85)
		var look_target := Vector3(center.x, center.y * 0.88, center.z)
		_camera.global_position = cam_pos
		_camera.fov = 38.0
		_camera.look_at(look_target, Vector3.UP)
	elif category == "cylinder":
		_stage_container.visible = false
		_camera.far = 8000.0
		var cam_pos := Vector3(440.0, 420.0, 940.0)
		var look_target := Vector3(0.0, 200.0, 0.0)
		_camera.global_position = cam_pos
		_camera.fov = 38.0
		_camera.look_at(look_target, Vector3.UP)
	else:
		var scale_f: float = clampf(sz.y / 17.5, 0.88, 1.25)
		var cam_pos := Vector3(16.5 * scale_f, 13.5 * scale_f, 19.5 * scale_f)
		var look_target := Vector3(center.x, maxf(7.5 * scale_f, center.y * 0.92), center.z)
		_camera.global_position = cam_pos
		_camera.fov = 38.0
		_camera.look_at(look_target, Vector3.UP)


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
		print("[BuildingShowcase] Completed all ", _render_queue.size(), " renders!")
		get_tree().quit(0)
		return
	if _render_wait == 0:
		_load_candidate(_render_queue[_render_step])
		_render_wait = 1
		return
	_render_wait += 1
	if _render_wait >= 5:
		var entry: Dictionary = _render_queue[_render_step]
		var cat: String = String(entry["category"])
		var tid: String = String(entry["item_id"])
		var cname: String = String(entry["cand_name"])
		var img: Image = get_viewport().get_texture().get_image()
		if img != null and not img.is_empty():
			for root_dir: String in [GODOT_RENDERS_ROOT, ASSETS_RENDERS_ROOT]:
				var out_dir: String = root_dir + "/" + cat + "/" + tid
				if cat == "cylinder":
					out_dir = root_dir + "/cylinder"
				DirAccess.make_dir_recursive_absolute(out_dir)
				var out_file: String = out_dir + "/" + cname + ".png"
				if img.save_png(out_file) == OK:
					print("[BuildingShowcase] Saved ", out_file)
		_render_step += 1
		_render_wait = 0
