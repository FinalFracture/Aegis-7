class_name CylinderHab7Metropolis
extends Node3D

const WINNERS_DIR := "res://../assets/glb/winners"
const BLDG_GLB_ROOT := "res://../assets/glb/buildings"
const BLDG_TEX_DIR := "res://../assets/textures/buildings"
const SHARED_TEX_DIR := "res://../assets/textures"

const OUT_DIRS := [
	"res://renders/buildings/metropolis",
	"res://../assets/renders/buildings/metropolis"
]

const BUILDINGS := [
	{"slot": "Bldg01_HabSpire", "winners": ["bldg_01_winner_01_hab_spire.glb"], "fallback": "bldg_01/bldg_01_r1_02.glb", "pos": Vector3(-56.0, 0.0, 16.0), "rot_y": 20.0},
	{"slot": "Bldg02_TransitRotunda", "winners": ["bldg_02_winner_01_transit_rotunda.glb"], "fallback": "bldg_02/bldg_02_r1_02.glb", "pos": Vector3(-38.0, 0.0, 22.0), "rot_y": 12.0},
	{"slot": "Bldg03_CulinaryAtrium", "winners": ["bldg_03_winner_01_culinary_atrium.glb"], "fallback": "bldg_03/bldg_03_r1_02.glb", "pos": Vector3(-20.0, 0.0, 18.0), "rot_y": 6.0},
	{"slot": "Bldg04_MedicalTraumaCenter", "winners": ["bldg_04_winner_01_medical_trauma_center.glb"], "fallback": "bldg_04/bldg_04_r1_02.glb", "pos": Vector3(20.0, 0.0, 18.0), "rot_y": -6.0},
	{"slot": "Bldg05_CelestialPromenadeDome", "winners": ["bldg_05_winner_01_celestial_promenade_dome.glb"], "fallback": "bldg_05/bldg_05_r1_02.glb", "pos": Vector3(38.0, 0.0, 22.0), "rot_y": -12.0},
	{"slot": "Bldg06_HydroponicBiodome", "winners": ["bldg_06_winner_01_hydroponic_biodome.glb"], "fallback": "bldg_06/bldg_06_r1_02.glb", "pos": Vector3(-48.0, 0.0, -4.0), "rot_y": 15.0},
	{"slot": "Bldg07_AtmosphericProcessor", "winners": ["bldg_07_winner_01_atmospheric_processor.glb"], "fallback": "bldg_07/bldg_07_r1_02.glb", "pos": Vector3(-24.0, 0.0, -6.0), "rot_y": 8.0},
	{"slot": "Bldg08_AstrometryObservatory", "winners": ["bldg_08_winner_01_astrometry_observatory.glb"], "fallback": "bldg_08/bldg_08_r1_02.glb", "pos": Vector3(0.0, 0.0, 8.0), "rot_y": 0.0},
	{"slot": "Bldg09_AquiferPumpingStation", "winners": ["bldg_09_winner_01_aquifer_pumping_station.glb"], "fallback": "bldg_09/bldg_09_r1_02.glb", "pos": Vector3(24.0, 0.0, -6.0), "rot_y": -8.0},
	{"slot": "Bldg10_CryoSeedVault", "winners": ["bldg_10_winner_01_cryo_seed_vault.glb"], "fallback": "bldg_10/bldg_10_r1_02.glb", "pos": Vector3(48.0, 0.0, -4.0), "rot_y": -15.0},
	{"slot": "Bldg12_FusionReactorComplex", "winners": ["bldg_12_winner_01_fusion_reactor_complex.glb"], "fallback": "bldg_12/bldg_12_r1_02.glb", "pos": Vector3(-52.0, 1.5, -28.0), "rot_y": 18.0},
	{"slot": "Bldg13_CargoLogisticsPort", "winners": ["bldg_13_winner_01_cargo_logistics_port.glb"], "fallback": "bldg_13/bldg_13_r1_02.glb", "pos": Vector3(-26.0, 1.5, -28.0), "rot_y": 8.0},
	{"slot": "Bldg11_CitadelCommandHQ", "winners": ["bldg_11_winner_01_citadel_command_hq.glb"], "fallback": "bldg_11/bldg_11_r1_02.glb", "pos": Vector3(0.0, 2.0, -30.0), "rot_y": 0.0},
	{"slot": "Bldg14_EvaDockingPinnacle", "winners": ["bldg_14_winner_01_eva_docking_pinnacle.glb"], "fallback": "bldg_14/bldg_14_r1_02.glb", "pos": Vector3(26.0, 1.5, -28.0), "rot_y": -8.0},
	{"slot": "Bldg15_SolarMirrorControlPylon", "winners": ["bldg_15_winner_01_solar_mirror_control_pylon.glb", "bldg_15_winner_01_solar_pylon.glb"], "fallback": "bldg_15/bldg_15_r1_02.glb", "pos": Vector3(52.0, 1.5, -28.0), "rot_y": -18.0},
	{"slot": "Bldg16_ShipyardDrydockHall", "winners": ["bldg_16_winner_01_shipyard_drydock_hall.glb"], "fallback": "bldg_16/bldg_16_r1_02.glb", "pos": Vector3(-56.0, 0.0, 34.0), "rot_y": 20.0},
	{"slot": "Bldg17_CoriolisRecreationArena", "winners": ["bldg_17_winner_01_coriolis_recreation_arena.glb"], "fallback": "bldg_17/bldg_17_r1_02.glb", "pos": Vector3(-28.0, 0.0, 36.0), "rot_y": 10.0},
	{"slot": "Bldg18_ColonialHoloMuseum", "winners": ["bldg_18_winner_01_colonial_holo_museum.glb"], "fallback": "bldg_18/bldg_18_r1_02.glb", "pos": Vector3(0.0, 0.0, 32.0), "rot_y": 0.0},
	{"slot": "Bldg19_SynthBreweryRefinery", "winners": ["bldg_19_winner_01_synth_brewery_refinery.glb"], "fallback": "bldg_19/bldg_19_r1_02.glb", "pos": Vector3(28.0, 0.0, 36.0), "rot_y": -10.0},
	{"slot": "Bldg20_MeteorDefenseBastion", "winners": ["bldg_20_winner_01_meteor_defense_bastion.glb"], "fallback": "bldg_20/bldg_20_r1_02.glb", "pos": Vector3(56.0, 0.0, 34.0), "rot_y": -20.0},
	{"slot": "Prop01_MaglevShuttlePylon_W", "winners": ["prop_01_winner_01_maglev_shuttle_pylon.glb"], "fallback": "../props/prop_01/prop_01_r1_02.glb", "pos": Vector3(-30.0, 0.0, 6.0), "rot_y": 0.0},
	{"slot": "Prop01_MaglevShuttlePylon_E", "winners": ["prop_01_winner_01_maglev_shuttle_pylon.glb"], "fallback": "../props/prop_01/prop_01_r1_02.glb", "pos": Vector3(30.0, 0.0, 6.0), "rot_y": 0.0},
	{"slot": "Prop02_HoloWayfindingKiosk", "winners": ["prop_02_winner_01_holo_wayfinding_kiosk.glb"], "fallback": "../props/prop_02/prop_02_r1_02.glb", "pos": Vector3(-8.0, 0.0, 18.0), "rot_y": 15.0},
	{"slot": "Prop03_AtmoScrubberBollard", "winners": ["prop_03_winner_01_atmo_scrubber_bollard.glb"], "fallback": "../props/prop_03/prop_03_r1_02.glb", "pos": Vector3(8.0, 0.0, 18.0), "rot_y": -15.0},
	{"slot": "Prop04_CivicPlanterBenchPod", "winners": ["prop_04_winner_01_civic_planter_bench_pod.glb"], "fallback": "../props/prop_04/prop_04_r1_02.glb", "pos": Vector3(-12.0, 0.0, 26.0), "rot_y": 0.0},
	{"slot": "Prop05_VtolMedevacPadArray", "winners": ["prop_05_winner_01_vtol_medevac_pad_array.glb"], "fallback": "../props/prop_05/prop_05_r1_02.glb", "pos": Vector3(14.0, 0.0, 26.0), "rot_y": 0.0},
]

const CAMERAS := [
	{"name": "cam_01_metropolis_grand_skyline", "label": "CAM 01 — GRAND 15-BUILDING O'NEILL CYLINDER METROPOLIS SKYLINE", "pos": Vector3(0.0, 34.0, 74.0), "target": Vector3(0.0, 8.0, -10.0), "fov": 54.0},
	{"name": "cam_02_west_civic_and_biosphere_wing", "label": "CAM 02 — WEST METROPOLIS: RESIDENTIAL SPIRE, TRANSIT HUB, BIODOME & FUSION CORE", "pos": Vector3(-68.0, 22.0, 52.0), "target": Vector3(-14.0, 8.0, -8.0), "fov": 50.0},
	{"name": "cam_03_east_medical_aquifer_and_docking_wing", "label": "CAM 03 — EAST METROPOLIS: TRAUMA CENTER, CELESTIAL DOME, AQUIFER & EVA PINNACLE", "pos": Vector3(68.0, 22.0, 52.0), "target": Vector3(14.0, 8.0, -8.0), "fov": 50.0},
	{"name": "cam_04_axial_boulevard_toward_command_citadel", "label": "CAM 04 — LOW-ALTITUDE AXIAL PROMENADE TOWARD CENTRAL COMMAND CITADEL", "pos": Vector3(0.0, 9.5, 46.0), "target": Vector3(0.0, 10.5, -30.0), "fov": 48.0},
]

var _stage_container: Node3D
var _buildings_container: Node3D
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
	_stage_container = get_node_or_null("DistrictStage") as Node3D
	_buildings_container = get_node_or_null("DistrictBuildings") as Node3D
	_lights_container = get_node_or_null("DistrictLighting") as Node3D

	if _stage_container == null:
		_stage_container = Node3D.new()
		_stage_container.name = "DistrictStage"
		add_child(_stage_container)
	if _buildings_container == null:
		_buildings_container = Node3D.new()
		_buildings_container.name = "DistrictBuildings"
		add_child(_buildings_container)
	if _lights_container == null:
		_lights_container = Node3D.new()
		_lights_container.name = "DistrictLighting"
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

	_build_district_stage()
	_assemble_buildings()
	_setup_lighting()
	apply_camera_preset(0)


func _load_tex(fname: String) -> Texture2D:
	if _tex_cache.has(fname):
		return _tex_cache[fname] as Texture2D
	for d: String in [BLDG_TEX_DIR, SHARED_TEX_DIR, SHARED_TEX_DIR + "/bunk_round2"]:
		var p: String = d + "/" + fname
		if FileAccess.file_exists(p):
			var img: Image = Image.new()
			if img.load(p) == OK and not img.is_empty():
				img.generate_mipmaps()
				var tex: ImageTexture = ImageTexture.create_from_image(img)
				_tex_cache[fname] = tex
				return tex
	return null


func _build_district_stage() -> void:
	for ch: Node in _stage_container.get_children():
		ch.free()

	# Main Terrace Deck
	var deck: MeshInstance3D = MeshInstance3D.new()
	var bmesh: BoxMesh = BoxMesh.new()
	bmesh.size = Vector3(220.0, 0.8, 140.0)
	deck.mesh = bmesh
	deck.position = Vector3(0.0, -0.4, 0.0)
	var dmat: StandardMaterial3D = StandardMaterial3D.new()
	dmat.albedo_color = Color("#161B22")
	dmat.metallic = 0.35
	dmat.roughness = 0.45
	var ctex: Texture2D = _load_tex("facade_carbon_slate_spandrel.png")
	if ctex != null:
		dmat.albedo_texture = ctex
		dmat.uv1_scale = Vector3(24.0, 18.0, 1.0)
	deck.material_override = dmat
	_stage_container.add_child(deck)

	# Glowing Cyan & Amber Boulevard Guide Strips
	for z_lane: float in [-18.0, -2.0, 12.0]:
		var strip: MeshInstance3D = MeshInstance3D.new()
		var smesh: BoxMesh = BoxMesh.new()
		smesh.size = Vector3(193.6, 0.06, 0.35)
		strip.mesh = smesh
		strip.position = Vector3(0.0, 0.03, z_lane)
		var smat: StandardMaterial3D = StandardMaterial3D.new()
		var col: Color = Color("#00E5FF") if z_lane != -2.0 else Color("#FF9500")
		smat.albedo_color = col
		smat.emission_enabled = true
		smat.emission = col
		smat.emission_energy_multiplier = 2.2
		strip.material_override = smat
		_stage_container.add_child(strip)

	if true:
		var canal: MeshInstance3D = MeshInstance3D.new()
		var cmesh: BoxMesh = BoxMesh.new()
		cmesh.size = Vector3(180.39999999999998, 0.12, 4.5)
		canal.mesh = cmesh
		canal.position = Vector3(0.0, 0.05, 2.0)
		var wmat: StandardMaterial3D = StandardMaterial3D.new()
		wmat.albedo_color = Color(0.0, 0.72, 0.95, 0.65)
		wmat.emission_enabled = true
		wmat.emission = Color("#00B8E6")
		wmat.emission_energy_multiplier = 0.85
		wmat.roughness = 0.08
		wmat.metallic = 0.25
		canal.material_override = wmat
		_stage_container.add_child(canal)

	if true:
		var rail: MeshInstance3D = MeshInstance3D.new()
		var rmesh: BoxMesh = BoxMesh.new()
		rmesh.size = Vector3(187.0, 0.45, 2.2)
		rail.mesh = rmesh
		rail.position = Vector3(0.0, 5.2, 6.0)
		var rmat: StandardMaterial3D = StandardMaterial3D.new()
		rmat.albedo_color = Color("#282E38")
		rmat.metallic = 0.65
		rmat.roughness = 0.30
		rail.material_override = rmat
		_stage_container.add_child(rail)

	# Panoramic O'Neill Cylinder Curved Landscape Backdrop
	var backdrop: MeshInstance3D = MeshInstance3D.new()
	var qmesh: QuadMesh = QuadMesh.new()
	qmesh.size = Vector2(319.0, 95.0)
	backdrop.mesh = qmesh
	backdrop.position = Vector3(0.0, 32.0, -72.8)
	var vmat: StandardMaterial3D = StandardMaterial3D.new()
	var vtex: Texture2D = _load_tex("vista_oneill_cylinder_interior.png")
	if vtex != null:
		vmat.albedo_texture = vtex
		vmat.emission_enabled = true
		vmat.emission_texture = vtex
		vmat.emission_energy_multiplier = 1.15
	vmat.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	vmat.cull_mode = BaseMaterial3D.CULL_DISABLED
	backdrop.material_override = vmat
	backdrop.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	_stage_container.add_child(backdrop)


func _assemble_buildings() -> void:
	for ch: Node in _buildings_container.get_children():
		ch.free()

	for item: Dictionary in BUILDINGS:
		var target_path: String = ""
		var wlist: Array = item["winners"] as Array
		for wfile in wlist:
			var p: String = WINNERS_DIR + "/" + String(wfile)
			if FileAccess.file_exists(p):
				target_path = p
				break
		if target_path == "":
			var fb: String = BLDG_GLB_ROOT + "/" + String(item["fallback"])
			if FileAccess.file_exists(fb):
				target_path = fb
		if target_path == "":
			continue

		var doc: GLTFDocument = GLTFDocument.new()
		var state: GLTFState = GLTFState.new()
		if doc.append_from_file(target_path, state) == OK:
			var root: Node = doc.generate_scene(state)
			if root is Node3D:
				var n3d: Node3D = root as Node3D
				n3d.name = String(item["slot"])
				n3d.position = item["pos"] as Vector3
				n3d.rotation_degrees = Vector3(0.0, float(item["rot_y"]), 0.0)
				_buildings_container.add_child(n3d)
				_upgrade_materials(n3d)


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


func _setup_lighting() -> void:
	for ch: Node in _lights_container.get_children():
		ch.free()

	var sun: DirectionalLight3D = DirectionalLight3D.new()
	sun.name = "AxialCylinderSunlight"
	sun.rotation_degrees = Vector3(-36.0, -28.0, 0.0)
	sun.light_color = Color("#E6F4FF")
	sun.light_energy = 1.35
	sun.shadow_enabled = true
	sun.shadow_bias = 0.02
	_lights_container.add_child(sun)

	var fill: DirectionalLight3D = DirectionalLight3D.new()
	fill.name = "SkyBounceFill"
	fill.rotation_degrees = Vector3(-24.0, 145.0, 0.0)
	fill.light_color = Color("#7CC8FF")
	fill.light_energy = 0.60
	_lights_container.add_child(fill)

	for x_pos: float in [-32.0, 0.0, 32.0]:
		var omni: OmniLight3D = OmniLight3D.new()
		omni.position = Vector3(x_pos, 10.0, 8.0)
		omni.light_color = Color("#00E5FF")
		omni.light_energy = 1.65
		omni.omni_range = 38.0
		_lights_container.add_child(omni)


func apply_camera_preset(idx: int) -> void:
	if idx < 0 or idx >= CAMERAS.size() or _camera == null:
		return
	var c: Dictionary = CAMERAS[idx]
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
		print("[CylinderHab7Metropolis] All camera renders complete!")
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
					print("[CylinderHab7Metropolis] Saved ", out_file)
				# Also save short alias cam_01.png .. cam_04.png
				var short_alias: String = d + "/" + cam_name.substr(0, 6) + ".png"
				img.save_png(short_alias)
		_render_step += 1
		_render_wait = 0
