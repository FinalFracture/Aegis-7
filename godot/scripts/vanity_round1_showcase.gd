class_name VanityRound1Showcase
extends Node3D
## VanityRound1Showcase for Cylinder Hab-7 (Non-Bunk Sleeping Quarters Fixture #2: Compact Hygiene & Sonic Wash Vanity)
## Imports res://../assets/glb/vanity_round1/vanity_r1_01.glb .. vanity_r1_05.glb
## Configures:
## - Dark gunmetal spacecraft bulkhead studio stage (#1C2128 wall, #14181F metallic composite deck)
## - TRANSPARENCY_ALPHA (cull_mode = CULL_DISABLED, SHADOW_CASTING_SETTING_OFF, low opacity + high specular 0.90)
##   on glass_uv_cubby_violet.png and glass_sonic_shield_translucent.png so the interior 3D orbital-navy towels,
##   sonic grooming wands, and greywater filter cores read clearly
## - High-specular smart-mirror HUD surface (mirror_smart_hud_cyan.png, metallic = 0.92, roughness = 0.06)
## - Per-candidate 3-point + interior practical LED strip lighting rigs (#00E5FF cyan sonic-mist ring/mirror halo,
##   #7B5CFF UV-C sterilizer cubby glow, #FF9500 amber status/valve accent, #E0F4FF crisp medical/grooming key light)

const EXT_GLB_DIR := "res://../assets/glb/vanity_round1"
const RES_GLB_DIR := "res://../assets/glb/vanity_round1"
const EXT_TEX_DIR := "res://../assets/textures/vanity_round1"
const SHARED_TEX_DIR := "res://../assets/textures"
const SPEC_PATH := "res://../design/vanity_round1/vanity_r1_spec.md"

const OUT_DIRS := [
	"res://renders/vanity_round1",
	"res://../assets/renders/vanity_round1"
]

const MATERIAL_TO_TEXTURE := {
	"mat_titanium_gunmetalhull": "titanium_gunmetal_hull.png",
	"mat_composite_aerospacewhite": "composite_aerospace_white.png",
	"mat_carbon_slateframe": "carbon_slate_frame.png",
	"mat_steel_machinedgantry": "steel_machined_gantry.png",
	"mat_fabric_orbitalnavytowel": "fabric_orbital_navy_towel.png",
	"mat_accent_signalorange": "accent_signal_orange.png",
	"mat_mirror_smarthudcyan": "mirror_smart_hud_cyan.png",
	"mat_oled_hygienepanel": "oled_hygiene_panel.png",
	"mat_glass_sonicshield_translucent": "glass_sonic_shield_translucent.png",
	"mat_glass_uvcubby_translucent": "glass_uv_cubby_violet.png"
}

const CANDIDATES := [
	{
		"index": 1,
		"id": "vanity_r1_01",
		"slug": "01_recessed_octagonal_sonic_vanity",
		"title": "01 — Recessed Octagonal Bulkhead Sonic Vanity",
		"cam_yaw_deg": 18.0,
		"cam_pitch_deg": -12.0,
		"cam_dist": 2.48,
		"fov": 46.0
	},
	{
		"index": 2,
		"id": "vanity_r1_02",
		"slug": "02_cantilevered_pod_halo_mirror",
		"title": "02 — Cantilevered Aerospace Pod Basin & Floating Halo Mirror",
		"cam_yaw_deg": -18.0,
		"cam_pitch_deg": -12.0,
		"cam_dist": 2.44,
		"fov": 46.0
	},
	{
		"index": 3,
		"id": "vanity_r1_03",
		"slug": "03_dual_zone_split_uv_decon_station",
		"title": "03 — Dual-Zone Split Grooming & UV Decon Station",
		"cam_yaw_deg": 19.0,
		"cam_pitch_deg": -12.0,
		"cam_dist": 2.54,
		"fov": 46.0
	},
	{
		"index": 4,
		"id": "vanity_r1_04",
		"slug": "04_cylindrical_sonic_mist_alcove",
		"title": "04 — Cylindrical Sonic-Mist Alcove & Privacy Shield Vanity",
		"cam_yaw_deg": -18.0,
		"cam_pitch_deg": -12.0,
		"cam_dist": 2.50,
		"fov": 46.0
	},
	{
		"index": 5,
		"id": "vanity_r1_05",
		"slug": "05_corner_chamfered_crew_wash",
		"title": "05 — Corner-Chamfered Compact Crew Wash & Med-Dispenser",
		"cam_yaw_deg": 20.0,
		"cam_pitch_deg": -12.0,
		"cam_dist": 2.54,
		"fov": 46.0
	}
]

var _stage_container: Node3D
var _model_holder: Node3D
var _lights_container: Node3D
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
		print("[VanityShowcase] Found Sloane's Vanity Round-1 spec at: ", SPEC_PATH)

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


## Builds the dark gunmetal spacecraft bulkhead studio stage (#1C2128 wall, #14181F metallic composite deck)
func _build_showcase_stage() -> void:
	for ch: Node in _stage_container.get_children():
		ch.free()

	# 1. Dark Spacecraft Metallic Composite Deck (#14181F)
	var floor_mi: MeshInstance3D = MeshInstance3D.new()
	floor_mi.name = "SpacecraftCompositeDeck"
	var fbox: BoxMesh = BoxMesh.new()
	fbox.size = Vector3(10.0, 0.08, 9.0)
	floor_mi.mesh = fbox
	floor_mi.position = Vector3(0.0, -0.04, 0.0)
	var fmat: StandardMaterial3D = StandardMaterial3D.new()
	fmat.albedo_color = Color("#14181F")
	fmat.roughness = 0.36
	fmat.metallic = 0.58
	floor_mi.material_override = fmat
	_stage_container.add_child(floor_mi)

	# 2. Dark Gunmetal Spacecraft Bulkhead Wall (#1C2128)
	var wall_mi: MeshInstance3D = MeshInstance3D.new()
	wall_mi.name = "SpacecraftBulkheadWall"
	var wbox: BoxMesh = BoxMesh.new()
	wbox.size = Vector3(10.0, 5.5, 0.12)
	wall_mi.mesh = wbox
	wall_mi.position = Vector3(0.0, 2.70, -0.45)
	var wmat: StandardMaterial3D = StandardMaterial3D.new()
	wmat.albedo_color = Color("#1C2128")
	wmat.roughness = 0.42
	wmat.metallic = 0.65
	wall_mi.material_override = wmat
	_stage_container.add_child(wall_mi)

	# 3. Side Bulkhead Wings (#181C22) for 3/4 camera angles
	for sx: float in [-2.65, 2.65]:
		var side_mi: MeshInstance3D = MeshInstance3D.new()
		side_mi.name = "SpacecraftSideBulkhead_" + str(sx)
		var sbox: BoxMesh = BoxMesh.new()
		sbox.size = Vector3(0.12, 5.5, 8.0)
		side_mi.mesh = sbox
		side_mi.position = Vector3(sx, 2.70, 1.8)
		var smat: StandardMaterial3D = StandardMaterial3D.new()
		smat.albedo_color = Color("#181C22")
		smat.roughness = 0.44
		smat.metallic = 0.65
		side_mi.material_override = smat
		_stage_container.add_child(side_mi)


func show_candidate(idx: int) -> void:
	if idx < 0 or idx >= CANDIDATES.size():
		return
	current_index = idx
	var info: Dictionary = CANDIDATES[idx]
	var cid: String = String(info["id"])
	var ctitle: String = String(info["title"])

	for ch: Node in _model_holder.get_children():
		ch.free()

	var node: Node3D = _load_vanity_glb(cid)
	var aabb := AABB(Vector3(-0.48, 0.0, -0.30), Vector3(0.96, 2.05, 0.60))

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
			var backwall: Node3D = _stage_container.get_node_or_null("SpacecraftBulkheadWall") as Node3D
			if backwall != null:
				backwall.position.z = min_z - 0.08
		print("[VanityShowcase] Loaded ", cid, " (", ctitle, ") | AABB size=", aabb.size)
	else:
		print("[VanityShowcase] Vanity GLB not found yet: ", cid, ".glb")

	_apply_vanity_lighting_rig(idx + 1)
	_frame_camera(info, aabb)


func _load_vanity_glb(cid: String) -> Node3D:
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
						_enhance_vanity_material(smat, mi, idx_1_based)
						mi.set_surface_override_material(s_idx, smat)
		for ch: Node in curr.get_children():
			mstack.append(ch)


func _enhance_vanity_material(smat: StandardMaterial3D, mi: MeshInstance3D, _idx_1_based: int) -> void:
	var mname: String = smat.resource_name.to_lower()
	var pname: String = mi.name.to_lower()
	smat.cull_mode = BaseMaterial3D.CULL_DISABLED
	smat.uv1_scale = Vector3.ONE

	if MATERIAL_TO_TEXTURE.has(mname):
		var tex_file: String = String(MATERIAL_TO_TEXTURE[mname])
		var fresh_tex: Texture2D = _load_tex(tex_file)
		if fresh_tex != null:
			smat.albedo_texture = fresh_tex

	# 1. High-Specular Smart-Mirror HUD Surface (mirror_smart_hud_cyan.png, metallic = 0.92, roughness = 0.06)
	if mname.contains("mirror") or pname.contains("mirror") and not pname.contains("frame") and not pname.contains("halo") and not pname.contains("strip"):
		var mirror_tex: Texture2D = _load_tex("mirror_smart_hud_cyan.png")
		if mirror_tex != null:
			smat.albedo_texture = mirror_tex
			smat.emission_texture = mirror_tex
		smat.albedo_color = Color(0.92, 0.96, 1.0, 1.0)
		smat.metallic = 0.92
		smat.roughness = 0.06
		smat.metallic_specular = 0.95
		smat.emission_enabled = true
		smat.emission = Color(0.18, 0.65, 0.85)
		smat.emission_energy_multiplier = 0.55
		smat.transparency = BaseMaterial3D.TRANSPARENCY_DISABLED
		return

	# 2. Translucent UV-C Sterilizer Cubbies, Privacy Shields & Greywater Sight-Glasses
	# (TRANSPARENCY_ALPHA, cull_mode = CULL_DISABLED, SHADOW_CASTING_SETTING_OFF, low opacity + high specular 0.90)
	if mname.contains("glass") or mname.contains("translucent") or pname.contains("glass") or pname.contains("shield") or (pname.contains("door") and not pname.contains("frame") and not pname.contains("track")):
		smat.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
		if mname.contains("uvcubby") or mname.contains("violet") or pname.contains("uv"):
			var uv_tex: Texture2D = _load_tex("glass_uv_cubby_violet.png")
			if uv_tex != null:
				smat.albedo_texture = uv_tex
			smat.albedo_color = Color(0.88, 0.82, 1.0, 0.19)
		else:
			var sh_tex: Texture2D = _load_tex("glass_sonic_shield_translucent.png")
			if sh_tex != null:
				smat.albedo_texture = sh_tex
			smat.albedo_color = Color(0.84, 0.95, 1.0, 0.18)
		smat.roughness = 0.08
		smat.metallic = 0.10
		smat.metallic_specular = 0.90
		mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
		return

	# 3. OLED Hygiene & H2O Recovery Telemetry Panel (oled_hygiene_panel.png)
	if mname.contains("oled") or mname.contains("hygienepanel") or pname.contains("oled") or pname.contains("telemetry"):
		var oled_tex: Texture2D = _load_tex("oled_hygiene_panel.png")
		if oled_tex != null:
			smat.albedo_texture = oled_tex
			smat.emission_texture = oled_tex
		smat.emission_enabled = true
		smat.emission = Color(0.22, 0.85, 1.0)
		smat.emission_energy_multiplier = 1.65
		return

	# 4. Brushed Machined Steel Fittings (Sonic-Mist Faucet Arches, Drain Rings, Syphon Pipes)
	if mname.contains("steel_machined") or pname.contains("faucet") or pname.contains("syphon"):
		smat.metallic = 0.90
		smat.roughness = 0.20
		smat.metallic_specular = 0.90
		return

	# 5. Emissive LED strips / Sonic Atomizer Rings / UV Sterilizer Tubes / Halo Mirror Rings
	if smat.emission_enabled or mname.contains("emissive") or mname.contains("led") or pname.contains("led") or pname.contains("halo") or pname.contains("atomizer"):
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


func _frame_camera(info: Dictionary, aabb: AABB) -> void:
	if _camera == null:
		return
	var target := Vector3(0.0, maxf(aabb.size.y * 0.50, 1.02), 0.0)
	var yaw_rad: float = deg_to_rad(float(info.get("cam_yaw_deg", 18.0)))
	var pitch_rad: float = deg_to_rad(float(info.get("cam_pitch_deg", -12.0)))
	var dist: float = float(info.get("cam_dist", 2.50))

	var cam_pos := target + Vector3(
		sin(yaw_rad) * cos(pitch_rad) * dist,
		-sin(pitch_rad) * dist,
		cos(yaw_rad) * cos(pitch_rad) * dist
	)
	_camera.global_position = cam_pos
	_camera.fov = float(info.get("fov", 46.0))
	_camera.look_at(target, Vector3.UP)


## Configures Sloane's per-candidate 3-Point + Interior Practical LED Strip Lighting Rigs (vanity_r1_spec.md)
func _apply_vanity_lighting_rig(idx_1_based: int) -> void:
	for ch: Node in _lights_container.get_children():
		ch.free()

	var key: DirectionalLight3D = DirectionalLight3D.new()
	key.name = "MedicalGroomingKeyLight"
	key.shadow_enabled = true
	key.shadow_bias = 0.02
	key.position = Vector3(1.8, 2.3, 2.4)
	key.light_color = Color("#E8F4FF")
	key.light_energy = 1.28
	_lights_container.add_child(key)
	key.look_at(Vector3(0.0, 1.02, 0.0), Vector3.UP)

	var fill: OmniLight3D = OmniLight3D.new()
	fill.name = "FillLight"
	fill.position = Vector3(-1.8, 1.4, 2.0)
	fill.light_color = Color("#78A8D8")
	fill.light_energy = 0.48
	fill.omni_range = 6.5
	_lights_container.add_child(fill)

	var rim: OmniLight3D = OmniLight3D.new()
	rim.name = "RimLight"
	rim.position = Vector3(0.0, 2.4, -1.4)
	rim.light_color = Color("#00E5FF")
	rim.light_energy = 0.88
	rim.omni_range = 5.5
	_lights_container.add_child(rim)

	match idx_1_based:
		1:
			# Candidate 01: Recessed Octagonal Bulkhead Sonic Vanity
			_add_omni("Mirror_IceWhite_Strips", Vector3(-0.12, 1.42, 0.18), Color("#E0F4FF"), 1.35, 1.8)
			_add_omni("Basin_SonicMist_Cyan", Vector3(-0.12, 0.94, 0.16), Color("#00E5FF"), 1.45, 1.8)
			_add_omni("UV_Sterilizer_Cubby_Violet", Vector3(0.32, 1.38, 0.10), Color("#7B5CFF"), 1.55, 1.8)
			_add_omni("Greywater_Bay_Amber", Vector3(0.0, 0.36, 0.15), Color("#FF9500"), 1.15, 1.5)
		2:
			# Candidate 02: Cantilevered Aerospace Pod Basin & Floating Halo Mirror
			_add_omni("Floating_Halo_Mirror_Cyan", Vector3(0.0, 1.36, 0.16), Color("#00E5FF"), 1.55, 2.0)
			_add_omni("Floating_Halo_IceWhite", Vector3(0.0, 1.15, 0.22), Color("#E0F4FF"), 1.35, 1.8)
			_add_omni("Overhead_Locker_UV_Violet", Vector3(0.0, 1.82, 0.12), Color("#7B5CFF"), 1.35, 1.7)
			_add_omni("Syphon_Manifold_Amber", Vector3(0.0, 0.42, 0.12), Color("#FF9500"), 1.15, 1.5)
		3:
			# Candidate 03: Dual-Zone Split Grooming & UV Decon Station
			_add_omni("Left_Alcove_Sonic_Cyan", Vector3(-0.18, 1.18, 0.18), Color("#00E5FF"), 1.50, 2.0)
			_add_omni("Left_Mirror_IceWhite", Vector3(-0.18, 1.55, 0.18), Color("#E0F4FF"), 1.30, 1.8)
			_add_omni("Right_Tower_UV_Violet", Vector3(0.34, 1.25, 0.12), Color("#7B5CFF"), 1.65, 2.1)
			_add_omni("Lower_Reclamation_Amber", Vector3(-0.18, 0.38, 0.16), Color("#FF9500"), 1.20, 1.6)
		4:
			# Candidate 04: Cylindrical Sonic-Mist Alcove & Privacy Shield Vanity
			_add_omni("Overhead_Sonic_Ring_Cyan", Vector3(0.0, 1.82, 0.12), Color("#00E5FF"), 1.60, 2.1)
			_add_omni("Curved_Mirror_IceWhite", Vector3(0.0, 1.32, 0.15), Color("#E0F4FF"), 1.35, 1.8)
			_add_omni("Lower_UV_Filter_Violet", Vector3(0.0, 0.52, 0.14), Color("#7B5CFF"), 1.35, 1.7)
			_add_omni("ToeKick_Amber", Vector3(0.0, 0.16, 0.20), Color("#FF9500"), 1.10, 1.4)
		5:
			# Candidate 05: Corner-Chamfered Compact Crew Wash & Med-Dispenser
			_add_omni("Center_Basin_Sonic_Cyan", Vector3(0.0, 1.12, 0.18), Color("#00E5FF"), 1.50, 2.0)
			_add_omni("Left_Wing_UV_Violet", Vector3(-0.34, 1.38, 0.14), Color("#7B5CFF"), 1.55, 1.8)
			_add_omni("Right_Wing_Med_IceWhite", Vector3(0.34, 1.38, 0.14), Color("#E0F4FF"), 1.35, 1.8)
			_add_omni("Lower_Manifold_Amber", Vector3(0.0, 0.38, 0.16), Color("#FF9500"), 1.25, 1.6)


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
			print("[VanityShowcase] Headless validation complete. Exiting cleanly.")
			get_tree().quit(0)
		return

	if turntable_spinning and _model_holder != null:
		_model_holder.rotate_y(0.45 * delta)


func _process_batch_render() -> void:
	if DisplayServer.get_name() == "headless":
		print("[VanityShowcase] Cannot capture viewport images under headless DisplayServer.")
		get_tree().quit(0)
		return

	if _frame_counter < 6:
		return

	if _render_step >= CANDIDATES.size():
		print("[VanityShowcase] All 5 Compact Hygiene & Sonic Wash Vanity beauty renders complete! Exiting cleanly.")
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
					print("[VanityShowcase] Saved render: ", out_file, " (", img.get_width(), "x", img.get_height(), ")")
		_render_step += 1
		_render_wait = 0
