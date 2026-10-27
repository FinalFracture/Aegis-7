class_name CylinderInteriorShowcase
extends Node3D
## Full-Scale (800m x 400m, R = 200m) O'Neill Cylinder Hab-7 Interior Showcase & Renderer
## Overhauled with:
## 1. Sloane's Cylinder Interior Biome, Terrain, Water & Lighting Material/Texture Suite:
##    - `biome_terraced_botanical_canopy.png`
##    - `water_ring_river_specular.png`
##    - `terrain_basalt_titanium_cliff_rock.png`
##    - `terrain_park_promenade_paving.png`
##    - `window_clusters_warm_amber_vs_cool_industrial.png` (`u: 0.0-0.5` Warm Amber vs `u: 0.5-1.0` Cool Telemetry)
##    - `sky_axial_golden_hour_gradient.png`
## 2. Vance & Rook's Radially Asymmetric 3-Valley Macro-Biomes (`valley_a`, `valley_b`, `valley_c`),
##    5 Hero Interior Macro-Setpieces (`interior_setpiece_01`..`05`), Multi-Tier Radial Elevations,
##    and Golden-Hour Axial Solar Lighting + Volumetric Aerial Perspective across the 400m diameter.

const WINNERS_DIR := "res://../assets/glb/winners"
const CYL_FALLBACK := "res://../assets/glb/cylinder/cylinder_r1_02.glb"
const CYL_INT_GLB_DIR := "res://../assets/glb/cylinder_interior"
const BLDG_GLB_ROOT := "res://../assets/glb/buildings"
const PROP_GLB_ROOT := "res://../assets/glb/props"
const CYL_INT_TEX_DIR := "res://../assets/textures/cylinder_interior"
const BLDG_TEX_DIR := "res://../assets/textures/buildings"
const SHARED_TEX_DIR := "res://../assets/textures"

const OUT_DIRS := [
	"res://renders/cylinder_interior",
	"res://../assets/renders/cylinder_interior"
]

const CYL_AXIS_Y := 200.0
const CYL_ROLL_DEG := 43.0  # Aligns Valley A (k=1, 137 deg) to dead-bottom 180 deg (Y=14m, Z=0m)
const R_HULL_FLOOR := 185.5

const BUILDING_CATALOG := [
	{"id": "bldg_01", "winner": "bldg_01_winner_01_hab_spire.glb", "fallback": "bldg_01/bldg_01_r1_02.glb"},
	{"id": "bldg_02", "winner": "bldg_02_winner_01_transit_rotunda.glb", "fallback": "bldg_02/bldg_02_r1_02.glb"},
	{"id": "bldg_03", "winner": "bldg_03_winner_01_culinary_atrium.glb", "fallback": "bldg_03/bldg_03_r1_02.glb"},
	{"id": "bldg_04", "winner": "bldg_04_winner_01_medical_trauma_center.glb", "fallback": "bldg_04/bldg_04_r1_02.glb"},
	{"id": "bldg_05", "winner": "bldg_05_winner_01_celestial_promenade_dome.glb", "fallback": "bldg_05/bldg_05_r1_02.glb"},
	{"id": "bldg_06", "winner": "bldg_06_winner_01_hydroponic_biodome.glb", "fallback": "bldg_06/bldg_06_r1_02.glb"},
	{"id": "bldg_07", "winner": "bldg_07_winner_01_atmospheric_processor.glb", "fallback": "bldg_07/bldg_07_r1_02.glb"},
	{"id": "bldg_08", "winner": "bldg_08_winner_01_astrometry_observatory.glb", "fallback": "bldg_08/bldg_08_r1_02.glb"},
	{"id": "bldg_09", "winner": "bldg_09_winner_01_aquifer_pumping_station.glb", "fallback": "bldg_09/bldg_09_r1_02.glb"},
	{"id": "bldg_10", "winner": "bldg_10_winner_01_cryo_seed_vault.glb", "fallback": "bldg_10/bldg_10_r1_02.glb"},
	{"id": "bldg_11", "winner": "bldg_11_winner_01_citadel_command_hq.glb", "fallback": "bldg_11/bldg_11_r1_02.glb"},
	{"id": "bldg_12", "winner": "bldg_12_winner_01_fusion_reactor_complex.glb", "fallback": "bldg_12/bldg_12_r1_02.glb"},
	{"id": "bldg_13", "winner": "bldg_13_winner_01_cargo_logistics_port.glb", "fallback": "bldg_13/bldg_13_r1_02.glb"},
	{"id": "bldg_14", "winner": "bldg_14_winner_01_eva_docking_pinnacle.glb", "fallback": "bldg_14/bldg_14_r1_02.glb"},
	{"id": "bldg_15", "winner": "bldg_15_winner_01_solar_mirror_control_pylon.glb", "fallback": "bldg_15/bldg_15_r1_02.glb"},
	{"id": "bldg_16", "winner": "bldg_16_winner_01_shipyard_drydock_hall.glb", "fallback": "bldg_16/bldg_16_r1_02.glb"},
	{"id": "bldg_17", "winner": "bldg_17_winner_01_coriolis_recreation_arena.glb", "fallback": "bldg_17/bldg_17_r1_02.glb"},
	{"id": "bldg_18", "winner": "bldg_18_winner_01_colonial_holo_museum.glb", "fallback": "bldg_18/bldg_18_r1_02.glb"},
	{"id": "bldg_19", "winner": "bldg_19_winner_01_synth_brewery_refinery.glb", "fallback": "bldg_19/bldg_19_r1_02.glb"},
	{"id": "bldg_20", "winner": "bldg_20_winner_01_meteor_defense_bastion.glb", "fallback": "bldg_20/bldg_20_r1_02.glb"},
]

const PROP_CATALOG := [
	{"id": "prop_01", "winner": "prop_01_winner_01_maglev_shuttle_pylon.glb", "fallback": "prop_01/prop_01_r1_02.glb"},
	{"id": "prop_02", "winner": "prop_02_winner_01_holo_wayfinding_kiosk.glb", "fallback": "prop_02/prop_02_r1_02.glb"},
	{"id": "prop_03", "winner": "prop_03_winner_01_atmo_scrubber_bollard.glb", "fallback": "prop_03/prop_03_r1_02.glb"},
	{"id": "prop_04", "winner": "prop_04_winner_01_civic_planter_bench_pod.glb", "fallback": "prop_04/prop_04_r1_02.glb"},
	{"id": "prop_05", "winner": "prop_05_winner_01_vtol_medevac_pad_array.glb", "fallback": "prop_05/prop_05_r1_02.glb"},
]

const SETPIECE_CATALOG := [
	{"id": "setpiece_01", "winner": "interior_setpiece_01_winner_ring_skybridge_viaduct.glb", "fallback": "setpiece_01/interior_setpiece_01_r1_02.glb"},
	{"id": "setpiece_02", "winner": "interior_setpiece_02_winner_terraced_waterfall_reservoir.glb", "fallback": "setpiece_02/interior_setpiece_02_r1_02.glb"},
	{"id": "setpiece_03", "winner": "interior_setpiece_03_winner_axial_suncore_spoke_hub.glb", "fallback": "setpiece_03/interior_setpiece_03_r1_02.glb"},
	{"id": "setpiece_04", "winner": "interior_setpiece_04_winner_endcap_cliffside_citadel.glb", "fallback": "setpiece_04/interior_setpiece_04_r1_02.glb"},
	{"id": "setpiece_05", "winner": "interior_setpiece_05_winner_elevated_plaza_interchange.glb", "fallback": "setpiece_05/interior_setpiece_05_r1_02.glb"},
]

const CAMERAS := [
	{
		"name": "cam_01_interior_axial_vista",
		"label": "CAM 01 — FORWARD AXIAL MEGASTRUCTURE VISTA (GOLDEN-HOUR SUN SPINE & 3 ASYMMETRIC BIOME VALLEYS)",
		"pos": Vector3(-254.0, 114.0, -44.0),
		"target": Vector3(135.0, 174.0, 14.0),
		"fov": 62.0
	},
	{
		"name": "cam_02_interior_ground_looking_up_curve",
		"label": "CAM 02 — VALLEY A CIVIC ACROPOLIS & SPECULAR RING-RIVER LOOKING UP 360° CURVED WALLS",
		"pos": Vector3(-164.0, 29.0, -4.0),
		"target": Vector3(-12.0, 128.0, 36.0),
		"fov": 68.0
	},
	{
		"name": "cam_03_interior_midring_overlook",
		"label": "CAM 03 — MID-RING TERRACE OVERLOOK ACROSS 400m DIAMETER TO WATERFALL BIOSPHERE & SKYBRIDGE",
		"pos": Vector3(-52.0, 88.0, -138.0),
		"target": Vector3(-24.0, 124.0, 142.0),
		"fov": 64.0
	},
	{
		"name": "cam_04_interior_starport_throat_lookback",
		"label": "CAM 04 — AFT ZERO-G STARPORT THROAT LOOKING BACK TOWARD GOLDEN-HOUR DRUM & ENDCAP CITADEL",
		"pos": Vector3(266.0, 156.0, -52.0),
		"target": Vector3(-15.0, 122.0, 22.0),
		"fov": 65.0
	},
]

var _hull_container: Node3D
var _city_container: Node3D
var _lights_container: Node3D
var _camera: Camera3D

var _tex_cache: Dictionary = {}
var _batch_render: bool = false
var _validate_only: bool = false
var _frame_counter: int = 0
var _render_step: int = 0
var _render_wait: int = 0


func _ready() -> void:
	_camera = get_node_or_null("SceneCamera") as Camera3D
	_hull_container = get_node_or_null("CylinderHullContainer") as Node3D
	_city_container = get_node_or_null("InteriorCityContainer") as Node3D
	_lights_container = get_node_or_null("InteriorLighting") as Node3D

	if _hull_container == null:
		_hull_container = Node3D.new()
		_hull_container.name = "CylinderHullContainer"
		add_child(_hull_container)
	if _city_container == null:
		_city_container = Node3D.new()
		_city_container.name = "InteriorCityContainer"
		add_child(_city_container)
	if _lights_container == null:
		_lights_container = Node3D.new()
		_lights_container.name = "InteriorLighting"
		add_child(_lights_container)

	if _camera != null:
		_camera.near = 0.5
		_camera.far = 8000.0

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

	_load_cylinder_megaship()
	_build_interior_axial_and_valley_infrastructure()
	_populate_asymmetric_three_valleys_and_setpieces()
	_setup_interior_lighting()
	apply_camera_preset(0)


func _load_tex(fname: String) -> Texture2D:
	if _tex_cache.has(fname):
		return _tex_cache[fname] as Texture2D
	for d: String in [CYL_INT_TEX_DIR, SHARED_TEX_DIR, BLDG_TEX_DIR, SHARED_TEX_DIR + "/bunk_round2"]:
		var p: String = d + "/" + fname
		if FileAccess.file_exists(p):
			var img: Image = Image.new()
			if img.load(p) == OK and not img.is_empty():
				img.generate_mipmaps()
				var tex: ImageTexture = ImageTexture.create_from_image(img)
				_tex_cache[fname] = tex
				return tex
	return null


func _load_glb_node(path: String, valley_mode: int = 0) -> Node3D:
	if not FileAccess.file_exists(path):
		return null
	var doc: GLTFDocument = GLTFDocument.new()
	var state: GLTFState = GLTFState.new()
	if doc.append_from_file(path, state) == OK:
		var root: Node = doc.generate_scene(state)
		if root is Node3D:
			var n3d: Node3D = root as Node3D
			_upgrade_materials(n3d, false, valley_mode)
			return n3d
	return null


func _load_cylinder_megaship() -> void:
	for ch: Node in _hull_container.get_children():
		ch.free()

	var cyl_path: String = WINNERS_DIR + "/cylinder_winner_01_aegis7_dual_zone_split.glb"
	if not FileAccess.file_exists(cyl_path):
		cyl_path = CYL_FALLBACK

	var pivot: Node3D = Node3D.new()
	pivot.name = "CylinderAxisPivot"
	pivot.position = Vector3(0.0, CYL_AXIS_Y, 0.0)
	pivot.rotation_degrees = Vector3(CYL_ROLL_DEG, 0.0, 0.0)
	_hull_container.add_child(pivot)

	var doc: GLTFDocument = GLTFDocument.new()
	var state: GLTFState = GLTFState.new()
	if doc.append_from_file(cyl_path, state) == OK:
		var root: Node = doc.generate_scene(state)
		if root is Node3D:
			var n3d: Node3D = root as Node3D
			n3d.name = "CylinderWinner01_Aegis7DualZoneSplit_Overhauled"
			n3d.position = Vector3(0.0, -CYL_AXIS_Y, 0.0)
			pivot.add_child(n3d)
			_upgrade_materials(n3d, true, 0)


func _make_pbr_mat(tex_name: String, albedo: Color, rough: float, metal: float, uv_scale: Vector3, alpha_blend: bool = false, emis_col: Color = Color(0, 0, 0, 1), emis_energy: float = 0.0) -> StandardMaterial3D:
	var mat: StandardMaterial3D = StandardMaterial3D.new()
	mat.albedo_color = albedo
	mat.roughness = rough
	mat.metallic = metal
	mat.cull_mode = BaseMaterial3D.CULL_DISABLED
	var tex: Texture2D = _load_tex(tex_name)
	if tex != null:
		mat.albedo_texture = tex
		mat.uv1_scale = uv_scale
	if alpha_blend:
		mat.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
		mat.metallic_specular = 0.85
	if emis_energy > 0.0:
		mat.emission_enabled = true
		mat.emission = emis_col
		if tex != null:
			mat.emission_texture = tex
		mat.emission_energy_multiplier = emis_energy
	return mat


func _build_interior_axial_and_valley_infrastructure() -> void:
	for ch: Node in _city_container.get_children():
		ch.free()

	var mat_canopy: StandardMaterial3D = _make_pbr_mat("biome_terraced_botanical_canopy.png", Color(1.0, 1.0, 1.0, 1.0), 0.72, 0.02, Vector3(14.0, 4.0, 1.0))
	var mat_water: StandardMaterial3D = _make_pbr_mat("water_ring_river_specular.png", Color(0.65, 0.92, 1.0, 0.86), 0.08, 0.15, Vector3(16.0, 3.0, 1.0), true, Color("#38B8E8"), 0.65)
	var mat_cliff: StandardMaterial3D = _make_pbr_mat("terrain_basalt_titanium_cliff_rock.png", Color(1.0, 1.0, 1.0, 1.0), 0.68, 0.28, Vector3(12.0, 3.0, 1.0))
	var mat_paving: StandardMaterial3D = _make_pbr_mat("terrain_park_promenade_paving.png", Color(1.0, 1.0, 1.0, 1.0), 0.42, 0.18, Vector3(18.0, 4.0, 1.0), false, Color("#FFA518"), 0.35)
	var mat_sky_sun: StandardMaterial3D = _make_pbr_mat("sky_axial_golden_hour_gradient.png", Color(1.0, 0.92, 0.72, 0.78), 0.12, 0.05, Vector3(4.0, 2.0, 1.0), true, Color("#FFD166"), 3.2)

	# 1. Golden-Hour Axial Zero-G Solar Core Diffuser Sheath (`sky_axial_golden_hour_gradient.png`) along habitat drum
	var solar_beam: MeshInstance3D = MeshInstance3D.new()
	solar_beam.name = "AxialGoldenHourSolarSheath"
	var cmesh: CylinderMesh = CylinderMesh.new()
	cmesh.top_radius = 8.8
	cmesh.bottom_radius = 8.8
	cmesh.height = 540.0
	cmesh.radial_segments = 24
	solar_beam.mesh = cmesh
	solar_beam.position = Vector3(-65.0, CYL_AXIS_Y, 0.0)
	solar_beam.rotation_degrees = Vector3(0.0, 0.0, 90.0)
	solar_beam.material_override = mat_sky_sun
	solar_beam.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	_city_container.add_child(solar_beam)

	# Cool Starport Approach Beacon Core only inside the 160m Aft Zero-G Starport Throat (X = +205m .. +365m)
	var aft_beam: MeshInstance3D = MeshInstance3D.new()
	aft_beam.name = "AftStarportBeaconCore"
	var amesh: CylinderMesh = CylinderMesh.new()
	amesh.top_radius = 6.8
	amesh.bottom_radius = 6.8
	amesh.height = 155.0
	amesh.radial_segments = 20
	aft_beam.mesh = amesh
	aft_beam.position = Vector3(282.0, CYL_AXIS_Y, 0.0)
	aft_beam.rotation_degrees = Vector3(0.0, 0.0, 90.0)
	var amat: StandardMaterial3D = StandardMaterial3D.new()
	amat.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
	amat.albedo_color = Color(0.25, 0.90, 1.0, 0.52)
	amat.emission_enabled = true
	amat.emission = Color("#00E5FF")
	amat.emission_energy_multiplier = 2.2
	amat.cull_mode = BaseMaterial3D.CULL_DISABLED
	aft_beam.material_override = amat
	aft_beam.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	_city_container.add_child(aft_beam)

	# 2. VALLEY A (180° Bottom Nadir) — Stepped Travertine-Alloy Promenade, Specular Ring-River & Terraced Botanical Belts
	_add_valley_box_strip(-75.0, 180.0, R_HULL_FLOOR - 0.35, Vector3(13.5, 0.45, 385.0), mat_water)
	for p_off: float in [-5.8, 5.8]:
		_add_valley_box_strip(-75.0, 180.0 + p_off, R_HULL_FLOOR - 0.65, Vector3(15.0, 0.85, 385.0), mat_paving)
	for b_off: float in [-12.5, 12.5]:
		_add_valley_box_strip(-75.0, 180.0 + b_off, R_HULL_FLOOR - 1.35, Vector3(18.0, 1.6, 375.0), mat_canopy)
	for c_off: float in [-21.0, 21.0]:
		_add_valley_box_strip(-75.0, 180.0 + c_off, R_HULL_FLOOR - 3.2, Vector3(22.0, 4.2, 365.0), mat_cliff)

	# 3. VALLEY B (60° Port-Upper Sector) — Sinusoidally Meandering Ring-River, Central Lake Basin & Stepped Botanical Arboretum
	var n_seg: int = 12
	var x_start: float = -255.0
	var x_end: float = 105.0
	var seg_len: float = (x_end - x_start) / float(n_seg)
	for i: int in range(n_seg):
		var sx: float = x_start + (float(i) + 0.5) * seg_len
		var phi_m: float = 60.0 + 9.5 * sin(sx * 0.025)
		var yaw_m: float = 16.0 * cos(sx * 0.025)
		_add_valley_box_strip(sx, phi_m, R_HULL_FLOOR - 0.55, Vector3(18.5, 0.55, seg_len + 6.0), mat_water, yaw_m)
		_add_valley_box_strip(sx, phi_m - 8.5, R_HULL_FLOOR - 1.8, Vector3(24.0, 2.4, seg_len + 4.0), mat_canopy, yaw_m * 0.5)
		_add_valley_box_strip(sx, phi_m + 8.5, R_HULL_FLOOR - 1.8, Vector3(24.0, 2.4, seg_len + 4.0), mat_canopy, yaw_m * 0.5)
	# Central Reservoir Lake at X = -95m, phi = 60°
	_add_valley_box_strip(-95.0, 60.0, R_HULL_FLOOR - 0.85, Vector3(54.0, 0.8, 92.0), mat_water)

	# 4. VALLEY C (300° Starboard-Upper Sector) — Stepped Basalt-Titanium Industrial Switchyard & Signal-Orange Mag-Rail Trench
	_add_valley_box_strip(-75.0, 300.0, R_HULL_FLOOR - 0.9, Vector3(22.0, 1.2, 380.0), mat_cliff)
	for c_off: float in [-14.0, 14.0]:
		_add_valley_box_strip(-75.0, 300.0 + c_off, R_HULL_FLOOR - 2.8, Vector3(24.0, 3.6, 370.0), mat_cliff)


func _add_valley_box_strip(x_pos: float, phi_deg: float, r_floor: float, box_size: Vector3, mat: Material, yaw_deg: float = 0.0) -> void:
	var holder: Node3D = Node3D.new()
	_place_node_on_cylinder(holder, x_pos, phi_deg, r_floor, yaw_deg, 1.0)
	_city_container.add_child(holder)
	var mi: MeshInstance3D = MeshInstance3D.new()
	var bmesh: BoxMesh = BoxMesh.new()
	bmesh.size = box_size
	mi.mesh = bmesh
	mi.material_override = mat
	mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	holder.add_child(mi)


func _place_node_on_cylinder(node: Node3D, x_pos: float, phi_deg: float, r_floor: float, yaw_deg: float, uniform_scale: float) -> void:
	var rad: float = deg_to_rad(phi_deg)
	var cy: float = cos(rad)
	var sz: float = sin(rad)
	var pos := Vector3(x_pos, CYL_AXIS_Y + r_floor * cy, r_floor * sz)
	var up_dir := Vector3(0.0, -cy, -sz).normalized()
	var right_dir := Vector3(0.0, -sz, cy).normalized()
	var back_dir := Vector3(1.0, 0.0, 0.0)
	var b := Basis(right_dir, up_dir, back_dir).rotated(up_dir, deg_to_rad(yaw_deg)).scaled(Vector3(uniform_scale, uniform_scale, uniform_scale))
	node.transform = Transform3D(b, pos)


func _add_terrace_podium(x_pos: float, phi_deg: float, height_m: float, radius_w: float, mat: Material) -> void:
	if height_m <= 0.5:
		return
	var holder: Node3D = Node3D.new()
	_place_node_on_cylinder(holder, x_pos, phi_deg, R_HULL_FLOOR - height_m * 0.5, 0.0, 1.0)
	_city_container.add_child(holder)
	var mi: MeshInstance3D = MeshInstance3D.new()
	var cmesh: CylinderMesh = CylinderMesh.new()
	cmesh.top_radius = radius_w * 0.88
	cmesh.bottom_radius = radius_w
	cmesh.height = height_m
	cmesh.radial_segments = 8
	mi.mesh = cmesh
	mi.material_override = mat
	holder.add_child(mi)


func _populate_asymmetric_three_valleys_and_setpieces() -> void:
	# Load Building Templates in two window/material variants:
	# - `bldg_warm`: Warm Amber/Gold Residential & Civic (`u: 0.0-0.48` of `window_clusters_warm_amber_vs_cool_industrial.png`)
	# - `bldg_cool`: Cool Telemetry Cyan/UV/Orange Industrial & Research (`u: 0.52-0.98`)
	var bldg_warm: Array[Node3D] = []
	var bldg_cool: Array[Node3D] = []
	for item: Dictionary in BUILDING_CATALOG:
		var p: String = WINNERS_DIR + "/" + String(item["winner"])
		if not FileAccess.file_exists(p):
			p = BLDG_GLB_ROOT + "/" + String(item["fallback"])
		bldg_warm.append(_load_glb_node(p, 1))
		bldg_cool.append(_load_glb_node(p, 2))

	var prop_templates: Array[Node3D] = []
	for pitem: Dictionary in PROP_CATALOG:
		var pp: String = WINNERS_DIR + "/" + String(pitem["winner"])
		if not FileAccess.file_exists(pp):
			pp = PROP_GLB_ROOT + "/" + String(pitem["fallback"])
		prop_templates.append(_load_glb_node(pp, 1))

	var sp_templates: Array[Node3D] = []
	for sitem: Dictionary in SETPIECE_CATALOG:
		var sp_path: String = WINNERS_DIR + "/" + String(sitem["winner"])
		if not FileAccess.file_exists(sp_path):
			sp_path = CYL_INT_GLB_DIR + "/" + String(sitem["fallback"])
		sp_templates.append(_load_glb_node(sp_path, 0))

	var mat_cliff: StandardMaterial3D = _make_pbr_mat("terrain_basalt_titanium_cliff_rock.png", Color(1.0, 1.0, 1.0, 1.0), 0.68, 0.28, Vector3(4.0, 2.0, 1.0))
	var mat_canopy: StandardMaterial3D = _make_pbr_mat("biome_terraced_botanical_canopy.png", Color(1.0, 1.0, 1.0, 1.0), 0.72, 0.02, Vector3(4.0, 2.0, 1.0))
	var mat_paving: StandardMaterial3D = _make_pbr_mat("terrain_park_promenade_paving.png", Color(1.0, 1.0, 1.0, 1.0), 0.42, 0.18, Vector3(4.0, 2.0, 1.0))

	# ==========================================================================
	# 1. PLACE THE 5 HERO INTERIOR MACRO-SETPIECES (`interior_setpiece_01`..`05`)
	# ==========================================================================
	# Setpiece 05: Elevated Asymmetric Acropolis Plaza Interchange in Valley A (`phi = 180°`)
	if sp_templates.size() >= 5 and sp_templates[4] != null:
		for x_sp5: float in [-132.0, -52.0]:
			var sp5: Node3D = sp_templates[4].duplicate() as Node3D
			_place_node_on_cylinder(sp5, x_sp5, 180.0, R_HULL_FLOOR, 0.0, 1.65)
			_city_container.add_child(sp5)

	# Setpiece 01: Curved Ring-Spanning Suspension Skybridge & Viaduct Arch climbing walls at X = -112m
	if sp_templates.size() >= 1 and sp_templates[0] != null:
		for phi_sp1: float in [150.0, 210.0, 95.0, 265.0]:
			var sp1: Node3D = sp_templates[0].duplicate() as Node3D
			_place_node_on_cylinder(sp1, -112.0, phi_sp1, R_HULL_FLOOR - 2.0, 0.0, 1.65)
			_city_container.add_child(sp1)

	# Setpiece 02: Stepped Waterfall Hydro-Dam & Emerald Biodome Reservoir in Valley B (`phi = 60°`)
	if sp_templates.size() >= 2 and sp_templates[1] != null:
		for x_sp2: float in [-145.0, -78.0, -12.0]:
			var sp2: Node3D = sp_templates[1].duplicate() as Node3D
			_place_node_on_cylinder(sp2, x_sp2, 60.0, R_HULL_FLOOR - 1.0, 25.0, 1.85)
			_city_container.add_child(sp2)

	# Setpiece 03: Central Axial Zero-G Solar-Plasma Spoke Hub along (Y = 200m, Z = 0m)
	if sp_templates.size() >= 3 and sp_templates[2] != null:
		for x_sp3: float in [-175.0, -55.0, 65.0]:
			var sp3: Node3D = sp_templates[2].duplicate() as Node3D
			sp3.position = Vector3(x_sp3, CYL_AXIS_Y - 18.0, 0.0)
			sp3.scale = Vector3(1.55, 1.55, 1.55)
			_city_container.add_child(sp3)

	# Setpiece 04: Forward Endcap Stepped Cliffside Citadel & Radial Funicular Bowl (`X = -255m`)
	if sp_templates.size() >= 4 and sp_templates[3] != null:
		for phi_sp4: float in [180.0, 60.0, 300.0]:
			var sp4: Node3D = sp_templates[3].duplicate() as Node3D
			_place_node_on_cylinder(sp4, -258.0, phi_sp4, R_HULL_FLOOR - 6.0, 90.0, 1.75)
			_city_container.add_child(sp4)

	# ==========================================================================
	# 2. VALLEY A (`phi = 180°` Bottom Nadir) — Warm Amber Civic Metropolis & Stepped Acropolis
	#    Buildings: 01, 02, 03, 04, 05, 11 (Command Citadel), 14, 17, 18 with oblique yaws & stepped heights
	# ==========================================================================
	var valley_a_placements := [
		# [bldg_num(1..20), x, phi_deg, terrace_h, yaw_deg, scale]
		[11, -78.0, 180.0, 9.5, 0.0, 2.75],    # Central Command Citadel on raised Acropolis Podium
		[18, -118.0, 169.5, 5.5, 52.0, 2.35],  # Colonial Holo-Museum flanking West Acropolis
		[5, -118.0, 190.5, 5.5, -52.0, 2.35],  # Celestial Promenade Geodesic Dome flanking East Acropolis
		[1, -218.0, 171.0, 0.0, 68.0, 2.25],
		[2, -212.0, 189.0, 0.0, -64.0, 2.20],
		[3, -182.0, 161.5, 5.0, 42.0, 2.40],
		[4, -176.0, 198.5, 5.0, -45.0, 2.40],
		[1, -148.0, 171.5, 0.0, 75.0, 2.15],
		[2, -144.0, 188.5, 0.0, -72.0, 2.15],
		[17, -142.0, 156.5, 9.0, 34.0, 2.55],
		[3, -138.0, 203.5, 9.0, -36.0, 2.50],
		[4, -92.0, 159.0, 6.0, 58.0, 2.35],
		[1, -88.0, 201.0, 6.0, -58.0, 2.35],
		[2, -48.0, 170.5, 0.0, 64.0, 2.25],
		[5, -42.0, 189.5, 0.0, -62.0, 2.25],
		[17, -12.0, 160.0, 7.5, 40.0, 2.50],
		[18, -8.0, 200.0, 7.5, -40.0, 2.45],
		[1, 28.0, 171.0, 3.5, 72.0, 2.25],
		[3, 34.0, 189.0, 3.5, -70.0, 2.25],
		[14, 72.0, 164.0, 8.0, 48.0, 2.45],
		[4, 76.0, 196.0, 8.0, -48.0, 2.45],
	]
	for item: Array in valley_a_placements:
		var b_num: int = int(item[0]) - 1
		var bx: float = float(item[1])
		var bphi: float = float(item[2])
		var th: float = float(item[3])
		var byaw: float = float(item[4])
		var bsc: float = float(item[5])
		if th > 0.5:
			_add_terrace_podium(bx, bphi, th, 16.5, mat_paving if th < 7.0 else mat_cliff)
		var tpl: Node3D = bldg_warm[b_num]
		if tpl != null:
			var inst: Node3D = tpl.duplicate() as Node3D
			_place_node_on_cylinder(inst, bx, bphi, R_HULL_FLOOR - th, byaw, bsc)
			_city_container.add_child(inst)

	# Valley A Organic Street Props (Mag-Lev Pylons, Wayfinding Kiosks, Planter Pods & VTOL Pads)
	var va_props := [
		[1, -195.0, 175.2, 0.0, 2.3],
		[1, -128.0, 184.8, 0.0, 2.3],
		[2, -158.0, 176.5, 25.0, 2.4],
		[4, -152.0, 183.5, -20.0, 2.5],
		[5, -98.0, 174.5, 15.0, 2.4],
		[4, -64.0, 184.5, -35.0, 2.5],
		[1, -24.0, 175.2, 0.0, 2.3],
		[2, 12.0, 183.8, 18.0, 2.4],
	]
	for pr: Array in va_props:
		var ptpl: Node3D = prop_templates[int(pr[0]) - 1]
		if ptpl != null:
			var pinst: Node3D = ptpl.duplicate() as Node3D
			_place_node_on_cylinder(pinst, float(pr[1]), float(pr[2]), R_HULL_FLOOR - 0.3, float(pr[3]), float(pr[4]))
			_city_container.add_child(pinst)

	# ==========================================================================
	# 3. VALLEY B (`phi = 60°` Port-Upper Sector) — Emerald Agri-Biosphere & Meandering River
	#    Buildings: 06 (Biodome), 07 (Atmo), 08 (Astrometry), 09 (Aquifer Dam), 10 (Seed Vault)
	# ==========================================================================
	var valley_b_placements := [
		[6, -215.0, 46.0, 4.5, 38.0, 2.50],
		[9, -198.0, 74.0, 6.0, -42.0, 2.45],
		[6, -162.0, 42.0, 8.5, 55.0, 2.60],
		[7, -154.0, 78.0, 7.0, -50.0, 2.40],
		[9, -112.0, 48.0, 5.5, 28.0, 2.55],
		[6, -98.0, 75.5, 9.5, -34.0, 2.65],
		[10, -58.0, 41.0, 12.0, 62.0, 2.50],
		[8, -46.0, 79.0, 14.0, -58.0, 2.60],
		[6, -8.0, 47.0, 5.0, 44.0, 2.45],
		[9, 14.0, 73.0, 6.5, -38.0, 2.45],
		[7, 54.0, 44.0, 9.0, 50.0, 2.40],
		[10, 68.0, 76.0, 10.5, -48.0, 2.50],
	]
	for item: Array in valley_b_placements:
		var b_num: int = int(item[0]) - 1
		var bx: float = float(item[1])
		var bphi: float = float(item[2])
		var th: float = float(item[3])
		var byaw: float = float(item[4])
		var bsc: float = float(item[5])
		_add_terrace_podium(bx, bphi, th, 18.0, mat_canopy)
		var tpl: Node3D = bldg_warm[b_num]
		if tpl != null:
			var inst: Node3D = tpl.duplicate() as Node3D
			_place_node_on_cylinder(inst, bx, bphi, R_HULL_FLOOR - th, byaw, bsc)
			_city_container.add_child(inst)

	# Dense Botanical Planter Groves (`prop_04`) & Scrubber Bollards (`prop_03`) in Valley B
	for gx: float in [-205.0, -145.0, -85.0, -25.0, 35.0]:
		for g_off: float in [-11.0, 11.0]:
			var ptpl4: Node3D = prop_templates[3]
			if ptpl4 != null:
				var pinst4: Node3D = ptpl4.duplicate() as Node3D
				_place_node_on_cylinder(pinst4, gx, 60.0 + g_off, R_HULL_FLOOR - 1.8, gx * 0.7, 3.2)
				_city_container.add_child(pinst4)

	# ==========================================================================
	# 4. VALLEY C (`phi = 300°` Starboard-Upper Sector) — Cool Industrial Port, Shipyard & Fusion Ridge
	#    Buildings: 12 (Fusion), 13 (Cargo), 15 (Solar Pylon), 16 (Shipyard), 19 (Refinery), 20 (Defense)
	# ==========================================================================
	var valley_c_placements := [
		[16, -218.0, 284.0, 5.0, 72.0, 2.55],
		[13, -206.0, 316.0, 5.0, -68.0, 2.50],
		[12, -158.0, 282.0, 8.5, 54.0, 2.60],
		[19, -148.0, 318.0, 7.5, -56.0, 2.50],
		[16, -104.0, 285.0, 6.0, 64.0, 2.65],
		[13, -92.0, 315.0, 6.0, -62.0, 2.55],
		[12, -44.0, 281.0, 10.0, 48.0, 2.65],
		[20, -32.0, 319.0, 11.0, -52.0, 2.60],
		[19, 18.0, 285.0, 6.5, 58.0, 2.50],
		[15, 28.0, 315.0, 8.0, -55.0, 2.55],
		[20, 74.0, 283.0, 9.5, 62.0, 2.60],
		[15, 82.0, 317.0, 9.5, -60.0, 2.55],
	]
	for item: Array in valley_c_placements:
		var b_num: int = int(item[0]) - 1
		var bx: float = float(item[1])
		var bphi: float = float(item[2])
		var th: float = float(item[3])
		var byaw: float = float(item[4])
		var bsc: float = float(item[5])
		_add_terrace_podium(bx, bphi, th, 17.5, mat_cliff)
		var tpl: Node3D = bldg_cool[b_num]
		if tpl != null:
			var inst: Node3D = tpl.duplicate() as Node3D
			_place_node_on_cylinder(inst, bx, bphi, R_HULL_FLOOR - th, byaw, bsc)
			_city_container.add_child(inst)

	# Cleanup temporary templates
	for t: Node3D in bldg_warm:
		if t != null:
			t.free()
	for t: Node3D in bldg_cool:
		if t != null:
			t.free()
	for t: Node3D in prop_templates:
		if t != null:
			t.free()
	for t: Node3D in sp_templates:
		if t != null:
			t.free()


func _upgrade_materials(root: Node3D, is_cylinder_hull: bool, valley_mode: int) -> void:
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

	var tex_win_clusters: Texture2D = _load_tex("window_clusters_warm_amber_vs_cool_industrial.png")
	var tex_canopy: Texture2D = _load_tex("biome_terraced_botanical_canopy.png")
	var tex_water: Texture2D = _load_tex("water_ring_river_specular.png")
	var tex_cliff: Texture2D = _load_tex("terrain_basalt_titanium_cliff_rock.png")
	var tex_paving: Texture2D = _load_tex("terrain_park_promenade_paving.png")
	var tex_sky_gold: Texture2D = _load_tex("sky_axial_golden_hour_gradient.png")

	var mstack: Array[Node] = [root]
	while not mstack.is_empty():
		var curr: Node = mstack.pop_back()
		if curr is MeshInstance3D:
			var mi: MeshInstance3D = curr as MeshInstance3D
			if mi.mesh != null:
				mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF if is_cylinder_hull else GeometryInstance3D.SHADOW_CASTING_SETTING_ON
				for s_idx: int in range(mi.mesh.get_surface_count()):
					var mat: Material = mi.get_active_material(s_idx)
					if mat is StandardMaterial3D:
						var smat: StandardMaterial3D = (mat as StandardMaterial3D).duplicate() as StandardMaterial3D
						var mname: String = smat.resource_name.to_lower()
						var pname: String = mi.name.to_lower()
						smat.cull_mode = BaseMaterial3D.CULL_DISABLED

						# 1. Sloane's New Biome, Water, Cliff, Paving, Sky & Dual-Window Materials
						if mname.contains("water_ring_river") or pname.contains("water_river"):
							smat.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
							smat.albedo_color = Color(0.75, 0.95, 1.0, 0.85)
							if tex_water != null:
								smat.albedo_texture = tex_water
							smat.roughness = 0.08
							smat.metallic = 0.15
							smat.metallic_specular = 0.88
							smat.emission_enabled = true
							smat.emission = Color("#28B8E8")
							smat.emission_energy_multiplier = 0.55
							mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
						elif mname.contains("biome_terraced") or pname.contains("biome_canopy") or mname.contains("foliage"):
							if tex_canopy != null:
								smat.albedo_texture = tex_canopy
							smat.roughness = 0.72
							smat.metallic = 0.02
						elif mname.contains("basalt_titanium") or pname.contains("cliff_basalt"):
							if tex_cliff != null:
								smat.albedo_texture = tex_cliff
							smat.roughness = 0.68
							smat.metallic = 0.28
						elif mname.contains("park_promenade") or pname.contains("promenade_paving"):
							if tex_paving != null:
								smat.albedo_texture = tex_paving
								smat.emission_texture = tex_paving
							smat.roughness = 0.42
							smat.metallic = 0.18
							smat.emission_enabled = true
							smat.emission = Color("#FFA518")
							smat.emission_energy_multiplier = 0.45
						elif mname.contains("axialgoldenhour") or pname.contains("sky_golden_core"):
							if tex_sky_gold != null:
								smat.albedo_texture = tex_sky_gold
								smat.emission_texture = tex_sky_gold
							smat.emission_enabled = true
							smat.emission = Color("#FFD166")
							smat.emission_energy_multiplier = 3.2
							mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
						elif mname.contains("window_warm_amber") or pname.contains("window_warm_amber"):
							if tex_win_clusters != null:
								smat.albedo_texture = tex_win_clusters
								smat.emission_texture = tex_win_clusters
							smat.roughness = 0.35
							smat.metallic = 0.65
							smat.emission_enabled = true
							smat.emission = Color("#FFB703")
							smat.emission_energy_multiplier = 2.2
						elif mname.contains("window_cool_industrial") or pname.contains("window_cool_ind"):
							if tex_win_clusters != null:
								smat.albedo_texture = tex_win_clusters
								smat.emission_texture = tex_win_clusters
							smat.roughness = 0.35
							smat.metallic = 0.65
							smat.emission_enabled = true
							smat.emission = Color("#28E0FF")
							smat.emission_energy_multiplier = 2.2
						elif mname.contains("window_lit") or mname.contains("facade_lit"):
							# Map instanced building windows to Sloane's Dual-Zone Window Atlas!
							if tex_win_clusters != null:
								smat.albedo_texture = tex_win_clusters
								smat.emission_texture = tex_win_clusters
								if valley_mode == 1:
									# Left UV half (u: 0.0 - 0.48): Warm Circadian Amber/Gold Residential & Civic
									smat.uv1_scale = Vector3(0.46, 1.0, 1.0)
									smat.uv1_offset = Vector3(0.02, 0.0, 0.0)
									smat.emission = Color("#FFD166")
								elif valley_mode == 2:
									# Right UV half (u: 0.52 - 0.98): Cool Industrial Telemetry Cyan/UV/Orange
									smat.uv1_scale = Vector3(0.46, 1.0, 1.0)
									smat.uv1_offset = Vector3(0.52, 0.0, 0.0)
									smat.emission = Color("#28E0FF")
								else:
									smat.emission = Color("#FFE0A3")
							smat.roughness = 0.35
							smat.metallic = 0.65
							smat.emission_enabled = true
							smat.emission_energy_multiplier = 2.15
						elif valley_mode == 1 and (mname.contains("aerospacewhite") or pname.contains("aero_white")):
							# Warm Titanium-Alabaster tint for Valley A Civic Metropolis
							smat.albedo_color = Color("#EAE4DC")
						elif valley_mode == 2 and (mname.contains("aerospacewhite") or pname.contains("aero_white")):
							# Cool Brushed Silver-Alloy tint for Valley C Industrial Ridge
							smat.albedo_color = Color("#CBD4E0")
						elif mname.contains("glass") or mname.contains("translucent") or mname.contains("atrium") or mname.contains("dome") or pname.contains("glass") or pname.contains("curtain") or pname.contains("canopy"):
							smat.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
							smat.albedo_color.a = clampf(smat.albedo_color.a, 0.28, 0.38)
							smat.roughness = 0.08
							smat.metallic = 0.15
							smat.metallic_specular = 0.92
							smat.emission_enabled = true
							if mname.contains("emerald") or pname.contains("emerald"):
								smat.emission = Color("#22D890")
							else:
								smat.emission = Color("#38C8FF")
							smat.emission_energy_multiplier = 0.48 if is_cylinder_hull else 0.32
							mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
						elif mname.contains("oled") or mname.contains("sign") or mname.contains("marquee") or mname.contains("beacon") or mname.contains("telemetry"):
							smat.emission_enabled = true
							if smat.albedo_texture != null:
								smat.emission_texture = smat.albedo_texture
							if smat.emission == Color(0, 0, 0, 1):
								smat.emission = Color("#FFB703") if valley_mode == 1 else Color("#28E0FF")
							smat.emission_energy_multiplier = 1.85
						elif smat.emission_enabled or mname.contains("emissive") or mname.contains("led") or mname.contains("plasma") or mname.contains("holo"):
							smat.emission_enabled = true
							if smat.emission == Color(0, 0, 0, 1):
								smat.emission = smat.albedo_color
							smat.emission_energy_multiplier = 2.1

						mi.set_surface_override_material(s_idx, smat)
		for ch: Node in curr.get_children():
			mstack.append(ch)


func _setup_interior_lighting() -> void:
	for ch: Node in _lights_container.get_children():
		ch.free()

	# 1. Sloane's AxialSolarLightRig: Warm Golden-Hour Sunlight `#FFE3B3` + Cross-Cylinder Sky Bounce `#68A6C8`
	#    (Hull has cast_shadow = OFF so directional shadows cast cleanly across buildings & terraced slopes!)
	var sun_golden: DirectionalLight3D = DirectionalLight3D.new()
	sun_golden.name = "KeyAxialGoldenHourSun"
	sun_golden.rotation_degrees = Vector3(-52.0, -24.0, 0.0)
	sun_golden.light_color = Color("#FFE3B3")
	sun_golden.light_energy = 1.65
	sun_golden.shadow_enabled = true
	sun_golden.shadow_blur = 1.5
	sun_golden.shadow_bias = 0.03
	_lights_container.add_child(sun_golden)

	var sky_bounce_up: DirectionalLight3D = DirectionalLight3D.new()
	sky_bounce_up.name = "CrossCylinderSkyBounceUp"
	sky_bounce_up.rotation_degrees = Vector3(48.0, 32.0, 0.0)
	sky_bounce_up.light_color = Color("#FFE8C2")
	sky_bounce_up.light_energy = 0.95
	sky_bounce_up.shadow_enabled = false
	_lights_container.add_child(sky_bounce_up)

	var cerulean_fill: DirectionalLight3D = DirectionalLight3D.new()
	cerulean_fill.name = "CeruleanBotanicalCounterFill"
	cerulean_fill.rotation_degrees = Vector3(-14.0, 125.0, 0.0)
	cerulean_fill.light_color = Color("#68A6C8")
	cerulean_fill.light_energy = 0.55
	cerulean_fill.shadow_enabled = false
	_lights_container.add_child(cerulean_fill)

	# 2. Axial Solar Spine OmniLight3D Array along (Y = 200m, Z = 0m)
	#    Warm Golden-Hour `#FFE3B3` along the habitat drum (-280m..+130m), Cool Starport `#00E5FF` in the aft throat (+250m)
	for ax_x: float in [-260.0, -155.0, -50.0, 55.0, 150.0]:
		var spine_light: OmniLight3D = OmniLight3D.new()
		spine_light.name = "AxialGoldenSunNode_%d" % int(ax_x)
		spine_light.position = Vector3(ax_x, CYL_AXIS_Y, 0.0)
		spine_light.light_color = Color("#FFE3B3")
		spine_light.light_energy = 2.4
		spine_light.omni_range = 320.0
		spine_light.omni_attenuation = 0.85
		_lights_container.add_child(spine_light)

	var starport_light: OmniLight3D = OmniLight3D.new()
	starport_light.name = "AftStarportThroatNode"
	starport_light.position = Vector3(255.0, CYL_AXIS_Y, 0.0)
	starport_light.light_color = Color("#58E8FF")
	starport_light.light_energy = 2.1
	starport_light.omni_range = 280.0
	starport_light.omni_attenuation = 0.85
	_lights_container.add_child(starport_light)

	# 3. Zonal Biome Practical Fill Lights (Warm Amber in Valley A, Emerald in Valley B, Signal-Orange/Cyan in Valley C)
	for vx: float in [-185.0, -80.0, 25.0]:
		# Valley A (180 deg Bottom): Warm Circadian Amber/Gold Promenade Glow
		var va_omni: OmniLight3D = OmniLight3D.new()
		va_omni.position = Vector3(vx, 34.0, 0.0)
		va_omni.light_color = Color("#FFB74D")
		va_omni.light_energy = 1.45
		va_omni.omni_range = 125.0
		_lights_container.add_child(va_omni)

		# Valley B (60 deg Port-Upper): Lush Bioluminescent Emerald & Solar Fill
		var vb_omni: OmniLight3D = OmniLight3D.new()
		vb_omni.position = Vector3(vx, 282.0, 142.0)
		vb_omni.light_color = Color("#52B788")
		vb_omni.light_energy = 1.45
		vb_omni.omni_range = 135.0
		_lights_container.add_child(vb_omni)

		# Valley C (300 deg Starboard-Upper): Cool Telemetry Cyan & Signal-Orange Switchyard Fill
		var vc_omni: OmniLight3D = OmniLight3D.new()
		vc_omni.position = Vector3(vx, 282.0, -142.0)
		vc_omni.light_color = Color("#FF9500") if vx < -100.0 else Color("#28E0FF")
		vc_omni.light_energy = 1.45
		vc_omni.omni_range = 135.0
		_lights_container.add_child(vc_omni)


func apply_camera_preset(idx: int) -> void:
	if idx < 0 or idx >= CAMERAS.size() or _camera == null:
		return
	var c: Dictionary = CAMERAS[idx]
	_camera.near = 0.5
	_camera.far = 8000.0
	_camera.global_position = c["pos"] as Vector3
	_camera.fov = float(c["fov"])
	_camera.look_at(c["target"] as Vector3, Vector3.UP)


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
	if _frame_counter < 6:
		return
	if _render_step >= CAMERAS.size():
		print("[CylinderInteriorShowcase] All 4 overhauled interior camera renders complete!")
		get_tree().quit(0)
		return
	if _render_wait == 0:
		apply_camera_preset(_render_step)
		_render_wait = 1
		return
	_render_wait += 1
	if _render_wait >= 6:
		var c: Dictionary = CAMERAS[_render_step]
		var cam_name: String = String(c["name"])
		var img: Image = get_viewport().get_texture().get_image()
		if img != null and not img.is_empty():
			for d: String in OUT_DIRS:
				DirAccess.make_dir_recursive_absolute(d)
				var out_file: String = d + "/" + cam_name + ".png"
				if img.save_png(out_file) == OK:
					print("[CylinderInteriorShowcase] Saved ", out_file)
				var short_alias: String = d + "/" + cam_name.substr(0, 6) + ".png"
				img.save_png(short_alias)
		_render_step += 1
		_render_wait = 0
