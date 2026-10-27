class_name CorridorRound1Showcase
extends Node3D
## CorridorRound1Showcase for Cylinder Hab-7 (Room 02 Hero Fixture: Pressurized Bulkhead Airlock Hatch & Sector Checkpoint)
## Imports res://../assets/glb/corridor_round1/corridor_door_r1_01.glb .. corridor_door_r1_05.glb
## Configures:
## - Dark gunmetal spacecraft bulkhead studio stage (#1C2128 side bulkheads, #14181F metallic composite deck)
## - Emissive vista_oneill_cylinder_interior.png backdrop plane behind the parted blast-door portal (Z = -0.62m)
##   with NO opaque wall blocking the parted center gap or translucent door inspection windows!
## - TRANSPARENCY_ALPHA (cull_mode = CULL_DISABLED, SHADOW_CASTING_SETTING_OFF, low opacity + high specular 0.90)
##   on glass_airlock_viewport_translucent.png so the next-sector glow and stowed emergency extinguishers/trauma kits
##   behind side locker doors read with crystal clarity
## - Crisp emissive OLED airlock telemetry (oled_airlock_status.png) & brushed steel interlocking dog-latch teeth

const EXT_GLB_DIR := "res://../assets/glb/corridor_round1"
const RES_GLB_DIR := "res://../assets/glb/corridor_round1"
const EXT_TEX_DIR := "res://../assets/textures/corridor_round1"
const SHARED_TEX_DIR := "res://../assets/textures"
const SPEC_PATH := "res://../design/corridor_round1/corridor_door_r1_spec.md"

const OUT_DIRS := [
	"res://renders/corridor_round1",
	"res://../assets/renders/corridor_round1"
]

const MATERIAL_TO_TEXTURE := {
	"mat_titanium_gunmetalhull": "titanium_gunmetal_hull.png",
	"mat_composite_aerospacewhite": "composite_aerospace_white.png",
	"mat_carbon_slateframe": "carbon_slate_frame.png",
	"mat_steel_machinedgantry": "steel_machined_gantry.png",
	"mat_fabric_charcoalflightpad": "fabric_charcoal_flightpad.png",
	"mat_fabric_orbitalnavypad": "fabric_orbital_navy_pad.png",
	"mat_accent_signalorange": "accent_signal_orange.png",
	"mat_oled_airlockstatus": "oled_airlock_status.png",
	"mat_glass_airlockviewport_translucent": "glass_airlock_viewport_translucent.png"
}

const CANDIDATES := [
	{
		"index": 1,
		"id": "corridor_door_r1_01",
		"slug": "01_aegis7_octagonal_biparting_hatch",
		"title": "01 — Aegis-7 Octagonal Bi-Parting Blast Hatch & Checkpoint",
		"cam_yaw_deg": 16.0,
		"cam_pitch_deg": -10.0,
		"cam_dist": 3.25,
		"fov": 46.0
	},
	{
		"index": 2,
		"id": "corridor_door_r1_02",
		"slug": "02_dual_zone_airlock_emergency_sidebay",
		"title": "02 — Dual-Zone Airlock Portal & Emergency O2/Extinguisher Side Bay",
		"cam_yaw_deg": -16.0,
		"cam_pitch_deg": -10.0,
		"cam_dist": 3.35,
		"fov": 46.0
	},
	{
		"index": 3,
		"id": "corridor_door_r1_03",
		"slug": "03_cylindrical_plug_door_doglatch_portal",
		"title": "03 — Cylindrical Plug-Door Pressure Lock & Rotary Dog-Latch Portal",
		"cam_yaw_deg": 17.0,
		"cam_pitch_deg": -10.0,
		"cam_dist": 3.25,
		"fov": 46.0
	},
	{
		"index": 4,
		"id": "corridor_door_r1_04",
		"slug": "04_hex_aperture_wedge_blade_bulkhead",
		"title": "04 — Hex-Aperture Interlocking Wedge-Blade Sector Bulkhead",
		"cam_yaw_deg": -16.0,
		"cam_pitch_deg": -10.0,
		"cam_dist": 3.28,
		"fov": 46.0
	},
	{
		"index": 5,
		"id": "corridor_door_r1_05",
		"slug": "05_panoramic_twin_window_decon_arch",
		"title": "05 — Panoramic Twin-Window Observation Airlock & Decon Arch",
		"cam_yaw_deg": 17.0,
		"cam_pitch_deg": -10.0,
		"cam_dist": 3.30,
		"fov": 46.0
	}
]

var _stage_container: Node3D
var _model_holder: Node3D
var _lights_container: Node3D
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

	if FileAccess.file_exists(SPEC_PATH):
		print("[CorridorShowcase] Found Sloane's Corridor Door Round-1 spec at: ", SPEC_PATH)

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


## Builds the dark metallic composite deck (#14181F), side bulkhead piers (#1C2128), and the emissive
## vista_oneill_cylinder_interior.png backdrop plane behind the parted blast-door portal (no opaque backwall blocking the portal!).
func _build_showcase_stage() -> void:
	for ch: Node in _stage_container.get_children():
		ch.free()

	# 1. Dark Spacecraft Metallic Composite Deck (#14181F)
	var floor_mi: MeshInstance3D = MeshInstance3D.new()
	floor_mi.name = "SpacecraftCompositeDeck"
	var fbox: BoxMesh = BoxMesh.new()
	fbox.size = Vector3(12.0, 0.08, 10.0)
	floor_mi.mesh = fbox
	floor_mi.position = Vector3(0.0, -0.04, 0.0)
	var fmat: StandardMaterial3D = StandardMaterial3D.new()
	fmat.albedo_color = Color("#14181F")
	fmat.roughness = 0.36
	fmat.metallic = 0.58
	floor_mi.material_override = fmat
	_stage_container.add_child(floor_mi)

	# 2. Left & Right Bulkhead Wall Piers (#1C2128) leaving center portal aperture (X: -1.15..+1.15) completely open!
	var wmat: StandardMaterial3D = StandardMaterial3D.new()
	wmat.albedo_color = Color("#1C2128")
	wmat.roughness = 0.42
	wmat.metallic = 0.65

	for sx: float in [-3.40, 3.40]:
		var pier_mi: MeshInstance3D = MeshInstance3D.new()
		pier_mi.name = "BulkheadWingPier_" + str(sx)
		var pbox: BoxMesh = BoxMesh.new()
		pbox.size = Vector3(4.4, 5.5, 0.14)
		pier_mi.mesh = pbox
		pier_mi.position = Vector3(sx, 2.75, -0.35)
		pier_mi.material_override = wmat
		_stage_container.add_child(pier_mi)

	var header_mi: MeshInstance3D = MeshInstance3D.new()
	header_mi.name = "BulkheadPortalHeader"
	var hbox: BoxMesh = BoxMesh.new()
	hbox.size = Vector3(2.8, 2.8, 0.14)
	header_mi.mesh = hbox
	header_mi.position = Vector3(0.0, 4.10, -0.35)
	header_mi.material_override = wmat
	_stage_container.add_child(header_mi)

	# 3. Emissive O'Neill Cylinder Next-Sector Vista Backdrop Plane directly behind the parted doors (Z = -0.68m)
	_vista_plane = MeshInstance3D.new()
	_vista_plane.name = "NextSectorCylinderVista"
	var qmesh: QuadMesh = QuadMesh.new()
	qmesh.size = Vector2(3.6, 3.0)
	_vista_plane.mesh = qmesh
	_vista_plane.position = Vector3(0.0, 1.45, -0.68)

	var vmat: StandardMaterial3D = StandardMaterial3D.new()
	var vtex: Texture2D = _load_tex("vista_oneill_cylinder_interior.png")
	if vtex != null:
		vmat.albedo_texture = vtex
		vmat.emission_enabled = true
		vmat.emission_texture = vtex
		vmat.emission_energy_multiplier = 1.35
	vmat.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	vmat.cull_mode = BaseMaterial3D.CULL_DISABLED
	_vista_plane.material_override = vmat
	_vista_plane.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	_stage_container.add_child(_vista_plane)


func show_candidate(idx: int) -> void:
	if idx < 0 or idx >= CANDIDATES.size():
		return
	current_index = idx
	var info: Dictionary = CANDIDATES[idx]
	var cid: String = String(info["id"])
	var ctitle: String = String(info["title"])

	for ch: Node in _model_holder.get_children():
		ch.free()

	var node: Node3D = _load_corridor_glb(cid)
	var aabb := AABB(Vector3(-1.25, 0.0, -0.32), Vector3(2.50, 2.75, 0.64))

	if node != null:
		_model_holder.add_child(node)
		_convert_and_upgrade_meshes(node, idx + 1)
		var comp_aabb: AABB = _compute_node_aabb(node)
		if comp_aabb.size.length() > 0.1:
			aabb = comp_aabb
			var center_xz := Vector3(
				aabb.position.x + aabb.size.x * 0.5,
				0.0,
				aabb.position.z + aabb.size.z * 0.5
			)
			node.position = -center_xz
			var min_z: float = aabb.position.z - center_xz.z
			if _vista_plane != null:
				_vista_plane.position.z = min_z - 0.25
		print("[CorridorShowcase] Loaded ", cid, " (", ctitle, ") | AABB size=", aabb.size)
	else:
		print("[CorridorShowcase] Corridor Door GLB not found yet: ", cid, ".glb")

	_apply_corridor_lighting_rig(idx + 1)
	_frame_camera(info, aabb)


func _load_corridor_glb(cid: String) -> Node3D:
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


func _convert_and_upgrade_meshes(root: Node3D, idx_1_based: int) -> void:
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
						_enhance_corridor_material(smat, mi, idx_1_based)
						mi.set_surface_override_material(s_idx, smat)
		for ch: Node in curr.get_children():
			mstack.append(ch)


func _enhance_corridor_material(smat: StandardMaterial3D, mi: MeshInstance3D, _idx_1_based: int) -> void:
	var mname: String = smat.resource_name.to_lower()
	var pname: String = mi.name.to_lower()
	smat.cull_mode = BaseMaterial3D.CULL_DISABLED
	smat.uv1_scale = Vector3.ONE

	if MATERIAL_TO_TEXTURE.has(mname):
		var tex_file: String = String(MATERIAL_TO_TEXTURE[mname])
		var fresh_tex: Texture2D = _load_tex(tex_file)
		if fresh_tex != null:
			smat.albedo_texture = fresh_tex

	# 1. Translucent Armored Blast-Door Inspection Windows & Side Locker Glass
	# (TRANSPARENCY_ALPHA, cull_mode = CULL_DISABLED, SHADOW_CASTING_SETTING_OFF, low opacity + high specular 0.90)
	if mname.contains("glass") or mname.contains("translucent") or mname.contains("viewport") or pname.contains("glass") or pname.contains("window") or pname.contains("porthole"):
		smat.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
		var glass_tex: Texture2D = _load_tex("glass_airlock_viewport_translucent.png")
		if glass_tex != null:
			smat.albedo_texture = glass_tex
		smat.albedo_color = Color(0.84, 0.95, 1.0, 0.19)
		smat.roughness = 0.08
		smat.metallic = 0.10
		smat.metallic_specular = 0.90
		mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
		return

	# 2. Sector Access & Differential Pressure OLED Terminal (oled_airlock_status.png)
	if mname.contains("oled") or mname.contains("airlockstatus") or pname.contains("oled") or pname.contains("status") or pname.contains("terminal"):
		var oled_tex: Texture2D = _load_tex("oled_airlock_status.png")
		if oled_tex != null:
			smat.albedo_texture = oled_tex
			smat.emission_texture = oled_tex
		smat.emission_enabled = true
		smat.emission = Color(0.22, 0.85, 1.0)
		smat.emission_energy_multiplier = 1.65
		return

	# 3. Brushed Machined Steel Interlocking Dog-Latch Teeth, Gantry Tracks & Threshold Ramp
	if mname.contains("steel_machined") or pname.contains("dog") or pname.contains("tooth") or pname.contains("teeth") or pname.contains("gantry"):
		smat.metallic = 0.90
		smat.roughness = 0.22
		smat.metallic_specular = 0.90
		return

	# 4. Emissive Airlock Cycling Beacons, Threshold Chevrons & Decon Nozzles
	if smat.emission_enabled or mname.contains("emissive") or mname.contains("led") or pname.contains("led") or pname.contains("beacon") or pname.contains("strip"):
		smat.emission_enabled = true
		if smat.emission == Color(0, 0, 0, 1):
			smat.emission = smat.albedo_color
		smat.emission_energy_multiplier = 2.0


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
	var target := Vector3(0.0, 1.35, 0.0)
	var yaw_rad: float = deg_to_rad(float(info.get("cam_yaw_deg", 16.0)))
	var pitch_rad: float = deg_to_rad(float(info.get("cam_pitch_deg", -10.0)))
	var dist: float = float(info.get("cam_dist", 3.28))

	var cam_pos := target + Vector3(
		sin(yaw_rad) * cos(pitch_rad) * dist,
		-sin(pitch_rad) * dist,
		cos(yaw_rad) * cos(pitch_rad) * dist
	)
	_camera.global_position = cam_pos
	_camera.fov = float(info.get("fov", 46.0))
	_camera.look_at(target, Vector3.UP)


## Configures Sloane's 3-Point + Airlock Cycling Lighting Rig (Section 4 of corridor_door_r1_spec.md)
func _apply_corridor_lighting_rig(idx_1_based: int) -> void:
	for ch: Node in _lights_container.get_children():
		ch.free()

	var key: DirectionalLight3D = DirectionalLight3D.new()
	key.name = "KeyLight"
	key.shadow_enabled = true
	key.shadow_bias = 0.02
	key.position = Vector3(2.4, 2.8, 2.8)
	key.light_color = Color("#E8F2FF")
	key.light_energy = 1.30
	_lights_container.add_child(key)
	key.look_at(Vector3(0.0, 1.35, 0.0), Vector3.UP)

	var fill: OmniLight3D = OmniLight3D.new()
	fill.name = "FillLight"
	fill.position = Vector3(-2.4, 1.6, 2.4)
	fill.light_color = Color("#78A8D8")
	fill.light_energy = 0.48
	fill.omni_range = 7.5
	_lights_container.add_child(fill)

	var rim: OmniLight3D = OmniLight3D.new()
	rim.name = "PortalBacklightCyan"
	rim.position = Vector3(0.0, 1.8, -1.6)
	rim.light_color = Color("#00E5FF")
	rim.light_energy = 1.35
	rim.omni_range = 6.5
	_lights_container.add_child(rim)

	# Airlock practicals
	_add_omni("Arch_Cycling_Beacon_Amber", Vector3(0.0, 2.48, 0.28), Color("#FF9500"), 1.45, 2.4)
	_add_omni("Threshold_And_Checkpoint_Cyan", Vector3(0.85, 1.35, 0.32), Color("#00E5FF"), 1.50, 2.2)

	if idx_1_based == 2:
		_add_omni("Emergency_SideBay_Amber", Vector3(0.92, 0.72, 0.22), Color("#FF9500"), 1.35, 1.8)
	elif idx_1_based == 5:
		_add_omni("Decon_Arch_UV_Violet", Vector3(0.0, 2.15, 0.10), Color("#7B5CFF"), 1.40, 2.2)


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
				KEY_SPACE: turntable_spinning = not turntable_spinning


func _process(delta: float) -> void:
	_frame_counter += 1

	if _batch_render:
		_process_batch_render()
		return

	if _validate_only:
		if _frame_counter >= 4:
			print("[CorridorShowcase] Headless validation complete. Exiting cleanly.")
			get_tree().quit(0)
		return

	if turntable_spinning and _model_holder != null:
		_model_holder.rotate_y(0.45 * delta)


func _process_batch_render() -> void:
	if DisplayServer.get_name() == "headless":
		print("[CorridorShowcase] Cannot capture viewport images under headless DisplayServer.")
		get_tree().quit(0)
		return

	if _frame_counter < 6:
		return

	if _render_step >= CANDIDATES.size():
		print("[CorridorShowcase] All 5 Pressurized Bulkhead Airlock Hatch beauty renders complete! Exiting cleanly.")
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
					print("[CorridorShowcase] Saved render: ", out_file, " (", img.get_width(), "x", img.get_height(), ")")
		_render_step += 1
		_render_wait = 0
