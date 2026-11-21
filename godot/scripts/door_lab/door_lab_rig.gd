class_name DoorLabRig
extends RefCounted
## Isolated mechanical-door lab. All four doors instance GLBs. Pocket and the
## wall hatch use Rook's door_lab models. bay3 and pair use the as-built meshes.
## Nothing here writes back to a glb.

const PEARL := Color(0.847059, 0.870588, 0.901961) # #D8DEE6, blue 0.902 is the approved lab override
const GRAPHITE := Color(0.157, 0.180, 0.220)
const GUN := Color(0.102, 0.118, 0.141)
const ALLOY := Color(0.78, 0.80, 0.82)
const SEAL_C := Color(0.08, 0.08, 0.08)
const ORANGE := Color(0.72, 0.28, 0.05)
const CYAN := Color("#00E5FF")
const WARM := Color("#FFE9D2")
const RIM_C := Color("#CFF7FF")
const SURROUND := Color(0.16, 0.18, 0.21)
const AMBER_PLATE := Color(0.85, 0.45, 0.02)
const GLASS_C := Color(0.55, 0.62, 0.68, 0.35)

const TEX_WHITE := "res://assets/textures/facade_aerospace_white_cladding.png"
const TEX_GUN := "res://assets/textures/facade_titanium_gunmetal_hull.png"
const TEX_STEEL := "res://assets/textures/facade_brushed_steel_gantry.png"
const TEX_SLATE := "res://assets/models/char_bot_r2_05_livery_01_sprocket_facade_carbon_slate_spandrel.png"
const TEX_CYAN := "res://assets/textures/led_cyan_strip.png"
# Rook pass C rev 2: floor-hatch side-wall stay tables, 0.5 deg steps 0..105 (assets/src/door_lab/floor_hatch.py stay_tables).
const STAY_ARM_DEG := [
	0.000, 0.813, 1.628, 2.444, 3.260, 4.078, 4.897, 5.716, 6.537, 7.359, 8.182, 9.005, 9.830, 10.656, 11.482,
	12.310, 13.138, 13.968, 14.798, 15.629, 16.461, 17.293, 18.127, 18.961, 19.797, 20.633, 21.469, 22.307, 23.145, 23.985,
	24.824, 25.665, 26.506, 27.349, 28.191, 29.035, 29.879, 30.724, 31.569, 32.415, 33.262, 34.109, 34.957, 35.806, 36.655,
	37.505, 38.355, 39.206, 40.058, 40.910, 41.762, 42.616, 43.469, 44.323, 45.178, 46.033, 46.889, 47.745, 48.601, 49.458,
	50.316, 51.174, 52.032, 52.891, 53.750, 54.609, 55.469, 56.329, 57.190, 58.051, 58.912, 59.773, 60.635, 61.498, 62.360,
	63.223, 64.086, 64.949, 65.813, 66.677, 67.541, 68.405, 69.270, 70.134, 70.999, 71.865, 72.730, 73.595, 74.461, 75.327,
	76.193, 77.059, 77.925, 78.791, 79.657, 80.523, 81.390, 82.256, 83.123, 83.989, 84.856, 85.722, 86.589, 87.455, 88.322,
	89.188, 90.055, 90.921, 91.787, 92.653, 93.519, 94.385, 95.250, 96.116, 96.981, 97.846, 98.711, 99.575, 100.439, 101.303,
	102.167, 103.031, 103.894, 104.756, 105.619, 106.481, 107.342, 108.203, 109.064, 109.924, 110.784, 111.643, 112.501, 113.359, 114.217,
	115.073, 115.929, 116.785, 117.639, 118.493, 119.346, 120.199, 121.050, 121.901, 122.750, 123.599, 124.447, 125.294, 126.139, 126.984,
	127.827, 128.669, 129.510, 130.349, 131.188, 132.024, 132.860, 133.694, 134.526, 135.357, 136.186, 137.013, 137.838, 138.662, 139.484,
	140.303, 141.121, 141.936, 142.749, 143.560, 144.368, 145.174, 145.977, 146.777, 147.575, 148.370, 149.162, 149.950, 150.736, 151.518,
	152.296, 153.071, 153.842, 154.610, 155.373, 156.132, 156.887, 157.637, 158.383, 159.124, 159.861, 160.592, 161.318, 162.038, 162.753,
	163.462, 164.165, 164.862, 165.553, 166.237, 166.915, 167.586, 168.250, 168.906, 169.555, 170.197, 170.831, 171.457, 172.075, 172.685,
	173.286,
]
const STAY_SLIDE_M := [
	0.00000, 0.00069, 0.00134, 0.00197, 0.00256, 0.00312, 0.00364, 0.00414, 0.00460, 0.00503, 0.00543, 0.00579, 0.00612, 0.00642, 0.00669,
	0.00692, 0.00711, 0.00728, 0.00741, 0.00750, 0.00756, 0.00759, 0.00758, 0.00754, 0.00747, 0.00736, 0.00721, 0.00703, 0.00682, 0.00657,
	0.00628, 0.00596, 0.00560, 0.00521, 0.00479, 0.00433, 0.00383, 0.00330, 0.00273, 0.00213, 0.00149, 0.00081, 0.00010, -0.00064, -0.00142,
	-0.00224, -0.00309, -0.00398, -0.00491, -0.00587, -0.00686, -0.00789, -0.00896, -0.01007, -0.01121, -0.01238, -0.01359, -0.01484, -0.01612, -0.01744,
	-0.01879, -0.02018, -0.02160, -0.02306, -0.02456, -0.02609, -0.02765, -0.02925, -0.03089, -0.03256, -0.03427, -0.03601, -0.03778, -0.03959, -0.04144,
	-0.04332, -0.04523, -0.04718, -0.04916, -0.05118, -0.05323, -0.05531, -0.05743, -0.05958, -0.06177, -0.06399, -0.06624, -0.06852, -0.07084, -0.07319,
	-0.07558, -0.07799, -0.08044, -0.08292, -0.08543, -0.08798, -0.09055, -0.09316, -0.09580, -0.09846, -0.10116, -0.10390, -0.10666, -0.10945, -0.11227,
	-0.11512, -0.11800, -0.12091, -0.12385, -0.12681, -0.12981, -0.13283, -0.13589, -0.13897, -0.14207, -0.14521, -0.14837, -0.15156, -0.15477, -0.15801,
	-0.16128, -0.16457, -0.16789, -0.17123, -0.17460, -0.17799, -0.18140, -0.18484, -0.18830, -0.19179, -0.19529, -0.19882, -0.20237, -0.20594, -0.20954,
	-0.21315, -0.21678, -0.22044, -0.22411, -0.22780, -0.23151, -0.23524, -0.23898, -0.24274, -0.24652, -0.25032, -0.25413, -0.25795, -0.26179, -0.26565,
	-0.26951, -0.27339, -0.27728, -0.28119, -0.28510, -0.28903, -0.29297, -0.29691, -0.30086, -0.30483, -0.30879, -0.31277, -0.31675, -0.32074, -0.32473,
	-0.32872, -0.33272, -0.33672, -0.34072, -0.34472, -0.34872, -0.35272, -0.35671, -0.36071, -0.36470, -0.36868, -0.37266, -0.37663, -0.38059, -0.38454,
	-0.38848, -0.39241, -0.39632, -0.40023, -0.40411, -0.40798, -0.41183, -0.41566, -0.41948, -0.42327, -0.42703, -0.43077, -0.43449, -0.43817, -0.44183,
	-0.44546, -0.44905, -0.45262, -0.45614, -0.45963, -0.46308, -0.46649, -0.46986, -0.47319, -0.47647, -0.47971, -0.48289, -0.48603, -0.48912, -0.49216,
	-0.49515,
]
const STAY_PLUNGER_M := [
	0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000,
	0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000,
	0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000,
	0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000,
	0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000,
	0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000,
	0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000,
	0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000,
	0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000,
	0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000,
	0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000,
	0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000,
	0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000,
	0.0000, 0.0000, -0.0085, -0.0085, -0.0085, -0.0085, -0.0085, -0.0085, -0.0085, -0.0085, -0.0085, -0.0085, -0.0085, -0.0085, -0.0085,
	0.0000,
]

var _root: Node3D
var _pearl: StandardMaterial3D
var _graphite: StandardMaterial3D
var _gun: StandardMaterial3D
var _alloy: StandardMaterial3D
var _seal: StandardMaterial3D
var _orange: StandardMaterial3D
var _floor_mat: StandardMaterial3D
var _wall_mat: StandardMaterial3D
var _glass: StandardMaterial3D
var _frit_tex: Texture2D
var _digit_cache: Texture2D
var _diamond_cache: Texture2D
var _notes: Array = []


static func build(parent: Node3D) -> Dictionary:
	var rig := DoorLabRig.new()
	return rig._build(parent)


func _build(parent: Node3D) -> Dictionary:
	_root = parent
	_make_materials()
	var profs := {}
	var max_r := 0.0
	for id in ["pocket", "bay3", "pair", "hatch", "floorhatch"]:
		var prof := load("res://resources/door_lab/%s.tres" % id) as MechDoorProfile
		prof.load_table()
		profs[id] = prof
		max_r = maxf(max_r, prof.trigger_radius(5.2))
	# Narrow proximity boxes (not spheres) so the four wall doors can sit a few
	# metres apart. The floor hatch is off to the side, outside those boxes.
	var spacing := 5.6
	var xs := {
		"pocket": -7.6,
		"bay3": -2.0,
		"pair": 3.6,
		"hatch": 7.6,
		"floorhatch": 12.8,
	}
	var depth := maxf(80.0, max_r + 40.0)
	_environment(xs["floorhatch"] - xs["pocket"], depth)
	_floor(xs["pocket"] - 20.0, xs["floorhatch"] + 8.0, depth, xs["floorhatch"])
	_room_shell(xs["pocket"] - 6.0, xs["floorhatch"] + 3.0)
	var doors := {}
	doors["pocket"] = _pocket(profs["pocket"], xs["pocket"])
	doors["bay3"] = _glb_door(profs["bay3"], xs["bay3"], "res://assets/models/tt_entrance_bay_3l.glb", ["Leaf_0", "Leaf_1", "Leaf_2"], true)
	doors["pair"] = _glb_door(profs["pair"], xs["pair"], "res://assets/models/tt_door_pair_18.glb", ["Leaf_L", "Leaf_R"], true)
	doors["hatch"] = _hatch(profs["hatch"], xs["hatch"])
	doors["floorhatch"] = _floor_hatch(profs["floorhatch"], xs["floorhatch"])
	_wings_for(doors)
	# Open shots look through the leaf into the clear color. A lit return gives
	# that cell a real surface. Visual only: the snag walk must still pass.
	_vestibules(doors)
	_reflection_cards(xs)
	var player := _player(xs["pocket"], -(max_r + 6.0))
	_lights(xs, depth)
	_mute_grid_shadows(_root)
	print("[door_lab] spacing=%.2f max_trigger=%.2f" % [spacing, max_r])
	for id in ["pocket", "bay3", "pair", "hatch", "floorhatch"]:
		var d: MechDoor = doors[id]
		print("[door_lab] %s trigger=%.2f open_s=%.3f close_s=%.3f walk_x=%.3f clear=%.3f" % [id, d.trigger_radius, d.profile.open_duration, d.profile.close_duration, float(d.get_meta("walk_x", 0.0)), float(d.get_meta("walk_clear", 0.0))])
	return {
		"spacing": spacing,
		"max_trigger": max_r,
		"radii": {
			"pocket": (profs["pocket"] as MechDoorProfile).trigger_radius(5.2),
			"bay3": (profs["bay3"] as MechDoorProfile).trigger_radius(5.2),
			"pair": (profs["pair"] as MechDoorProfile).trigger_radius(5.2),
			"hatch": 0.0,
			"floorhatch": 0.0,
		},
		"notes": _notes,
		"player": player,
		"doors": doors,
	}


func _make_materials() -> void:
	_pearl = _mat("TT_WhiteComposite_Lab", PEARL, 0.05, 0.48, TEX_WHITE, Color(0.93, 0.93, 0.93))
	# Broad specular on the pearl faces was crossing 235. Diffuse stays #D8DEE6.
	_pearl.roughness = 0.62
	_graphite = _mat("TT_CarbonSlate_Lab", GRAPHITE, 0.35, 0.62, "", Color.WHITE)
	_gun = _mat("TT_Gunmetal_Lab", GUN, 0.55, 0.42, TEX_GUN, Color(0.85, 0.85, 0.85))
	_gun.metallic = 0.55
	_gun.roughness = 0.42
	_alloy = _mat("TT_BrushedAlloy_Lab", ALLOY, 0.95, 0.35, TEX_STEEL, Color(0.80, 0.80, 0.80))
	_seal = _mat("TT_Seal_Lab", SEAL_C, 0.0, 0.85, "", Color.WHITE)
	_orange = _mat("Mat_Hub_OverrideOrange", ORANGE, 0.1, 0.45, "", Color.WHITE)
	_floor_mat = _mat("TT_CarbonSlate_Floor", Color(0.16, 0.17, 0.19), 0.15, 0.60, TEX_SLATE, Color(0.55, 0.55, 0.55))
	# Grazing views of this huge deck turn both the slate grain and the shaded
	# lighting into a 4 px screen stripe. An unshaded flat grey has nothing to beat.
	_floor_mat.albedo_texture = null
	_floor_mat.albedo_color = Color(0.36, 0.37, 0.40)
	_floor_mat.metallic = 0.0
	_floor_mat.roughness = 1.0
	_floor_mat.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	_wall_mat = _mat("TT_CarbonSlate", Color(0.24, 0.26, 0.30), 0.08, 0.70, TEX_SLATE, Color(0.70, 0.72, 0.76))
	_wall_mat.albedo_color = Color(2.19, 2.02, 1.91)
	_wall_mat.roughness = 0.7
	_wall_mat.metallic = 0.08
	_wall_mat.uv1_triplanar = true
	_wall_mat.uv1_scale = Vector3(0.5, 0.5, 0.5)
	_glass = StandardMaterial3D.new()
	_glass.resource_name = "TT_GlassScissor"
	# Alpha 0.35 so the lite reads as glass. Depth is written opaque so the
	# moving leaf does not sort inside itself.
	_glass.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
	# Pocket and bay3 lites. Alpha 0.25, not a scissor cut.
	_glass.albedo_color = Color(0.30, 0.36, 0.42, 0.25)
	_glass.roughness = 0.05
	_glass.metallic = 0.0
	_glass.cull_mode = BaseMaterial3D.CULL_DISABLED
	_glass.depth_draw_mode = BaseMaterial3D.DEPTH_DRAW_OPAQUE_ONLY


func _mat(name: String, albedo: Color, metal: float, rough: float, tex_path: String, tex_tint: Color) -> StandardMaterial3D:
	var m := StandardMaterial3D.new()
	m.resource_name = name
	m.albedo_color = albedo
	m.metallic = metal
	m.roughness = rough
	m.cull_mode = BaseMaterial3D.CULL_DISABLED
	if tex_path != "" and ResourceLoader.exists(tex_path):
		var tex := load(tex_path) as Texture2D
		if tex != null:
			m.albedo_texture = tex
			# Texture times this tint stays under the 0.90 cap. Pearl's own albedo_color is the approved #D8DEE6.
			if name != "TT_WhiteComposite_Lab":
				m.albedo_color = tex_tint
			else:
				m.albedo_color = albedo
	return m


func _environment(span: float, depth: float) -> void:
	var we := WorldEnvironment.new()
	we.name = "LabEnvironment"
	var env := Environment.new()
	env.background_mode = Environment.BG_COLOR
	env.background_color = Color("#1A1E24")
	env.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
	env.ambient_light_color = Color("#5A6470")
	env.ambient_light_energy = 0.35
	env.tonemap_mode = Environment.TONE_MAPPER_FILMIC
	env.tonemap_exposure = 1.05
	env.glow_enabled = false
	# Flat slate reflection when a probe cubemap is not applied.
	env.reflected_light_source = Environment.REFLECTION_SOURCE_BG
	# Compatibility renderer ignores these; set only the properties this build exposes.
	if "ssao_enabled" in env:
		env.ssao_enabled = false
	if "ssil_enabled" in env:
		env.ssil_enabled = false
	if "ssr_enabled" in env:
		env.ssr_enabled = false
	if "sdfgi_enabled" in env:
		env.sdfgi_enabled = false
	if "fog_enabled" in env:
		env.fog_enabled = false
	we.environment = env
	_root.add_child(we)
	var probe := ReflectionProbe.new()
	probe.name = "LabProbe"
	probe.update_mode = ReflectionProbe.UPDATE_ONCE
	probe.box_projection = true
	probe.size = Vector3(span + 50.0, 8.0, depth * 2.0)
	probe.position = Vector3(0.0, 2.0, 0.0)
	probe.max_distance = 80.0
	probe.interior = true
	probe.ambient_mode = ReflectionProbe.AMBIENT_COLOR
	probe.ambient_color = Color("#3A424C")
	# Godot #98382: on Windows the compatibility renderer adds a green light to
	# every mesh inside a ReflectionProbe. Keep the probe (Sloane §5) but do not
	# apply that cubemap. Metals fall back to the slate background reflection.
	if OS.get_name() == "Windows":
		probe.intensity = 0.0
		probe.ambient_mode = ReflectionProbe.AMBIENT_DISABLED
	_root.add_child(probe)


func _floor(x0: float, x1: float, depth: float, hole_x: float = INF) -> void:
	# The floor-hatch GLB brings its own 1.24 m flange. Four slabs leave that square open
	# so the flange and the lid are not fighting the lab floor. The walk collider (below) leaves the 0.90 opening open.
	var hole := 0.62
	var hz0 := 0.50 - hole
	var hz1 := 0.50 + hole
	var slabs: Array = [[x0, x1, -depth, hz0], [x0, x1, hz1, depth], [x0, hole_x - hole, hz0, hz1], [hole_x + hole, x1, hz0, hz1]]
	if hole_x == INF:
		slabs = [[x0, x1, -depth, depth]]
	for i in slabs.size():
		var sl: Array = slabs[i]
		var vis := MeshInstance3D.new()
		vis.name = "FloorVisual" if i == 0 else "FloorVisual%d" % i
		var bm := BoxMesh.new()
		bm.size = Vector3(float(sl[1]) - float(sl[0]), 0.02, float(sl[3]) - float(sl[2]))
		vis.mesh = bm
		vis.position = Vector3((float(sl[0]) + float(sl[1])) * 0.5, -0.01, (float(sl[2]) + float(sl[3])) * 0.5)
		vis.set_surface_override_material(0, _floor_mat)
		# The deck is the receiver. It must not also fill the shadow map.
		vis.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
		_root.add_child(vis)
	var body := StaticBody3D.new()
	body.name = "FloorBody"
	body.collision_layer = 1
	body.collision_mask = 1
	_root.add_child(body)
	# Top of the collision is y = 0.12. Body origin of a standing player rests at y = 0.
	# Rook pass E incr: with a floor hatch, the walk collider leaves the 0.90 x 0.90 clear opening open (4 boxes, same top),
	# so a capsule can drop into the well; the GLB brings the liner walls + well floor and the closed lid carries a walk skin.
	var cols: Array = [[x0, x1, -depth, depth]]
	if hole_x != INF:
		var oh := 0.45
		cols = [[x0, x1, -depth, 0.50 - oh], [x0, x1, 0.50 + oh, depth], [x0, hole_x - oh, 0.50 - oh, 0.50 + oh], [hole_x + oh, x1, 0.50 - oh, 0.50 + oh]]
	for j in cols.size():
		var cl: Array = cols[j]
		var cs := CollisionShape3D.new()
		cs.name = "FloorShape" if j == 0 else "FloorShape%d" % j
		var box := BoxShape3D.new()
		box.size = Vector3(float(cl[1]) - float(cl[0]), 0.24, float(cl[3]) - float(cl[2]))
		cs.shape = box
		cs.position = Vector3((float(cl[0]) + float(cl[1])) * 0.5, 0.0, (float(cl[2]) + float(cl[3])) * 0.5)
		body.add_child(cs)


func _wings_for(doors: Dictionary) -> void:
	# 40 mm of clear air between the GLB frame and the lab wall. The span is the
	# as-built mesh, so a skirt added on the door does not push the wall out.
	var prev := 0.0
	var first := true
	for id in ["pocket", "bay3", "pair", "hatch"]:
		var door: Node3D = doors[id]
		var host: Node = door.get_node_or_null("AsBuilt")
		if host == null:
			host = door
		var ab := _aabb_node(host)
		var x0 := ab.position.x - 0.040
		var x1 := ab.position.x + ab.size.x + 0.040
		if first:
			_static_box("Wing_Start", Vector3(8.0, 4.0, 0.16), Vector3(x0 - 4.0, 2.0, -0.02), _wall_mat)
			first = false
		else:
			var gap := x0 - prev
			if gap > 0.05:
				_static_box("Wing_%s" % id, Vector3(gap, 4.0, 0.16), Vector3((prev + x0) * 0.5, 2.0, -0.02), _wall_mat)
		prev = x1
	# The floor-hatch lid swings through the door plane. An 8 m Wing_End that
	# starts at the bulkhead hatch covers that arc. Stop short of the hatch.
	var limit := prev + 8.0
	if doors.has("floorhatch"):
		var fh: Node3D = doors["floorhatch"]
		limit = fh.global_position.x - 1.5
	var span := limit - prev
	if span > 0.05:
		_static_box("Wing_End", Vector3(span, 4.0, 0.16), Vector3(prev + span * 0.5, 2.0, -0.02), _wall_mat)


func _lights(xs: Dictionary, _depth: float) -> void:
	var key := DirectionalLight3D.new()
	key.name = "KeyLight"
	key.light_energy = 0.78
	key.shadow_enabled = true
	_root.add_child(key)
	# Approach faces look toward -Z. Pitch −35° and yaw 30° off that normal:
	# the key comes from the camera side. Euler (−35, 30, 0) aims the other way.
	var yaw := deg_to_rad(30.0)
	var pitch := deg_to_rad(35.0)
	var travel := Vector3(sin(yaw) * cos(pitch), -sin(pitch), cos(yaw) * cos(pitch))
	key.look_at(key.global_position + travel, Vector3.UP)
	# The bay canopy is a slat grid. Half-strength shadows keep the bevel read
	# without the diagonal streaks across the pair and bay3 leaves.
	key.shadow_opacity = 0.5
	# The lab floor is tens of metres. The default shadow distance turns that into
	# a 4 px grating on the grazing floor-hatch hero. Keep the map on the doors.
	key.directional_shadow_max_distance = 18.0
	key.shadow_bias = 0.05
	key.shadow_normal_bias = 2.0
	for id in xs.keys():
		var x: float = xs[id]
		# One omni per door, 3 m in front of the approach face and 2.2 m up.
		var fill := OmniLight3D.new()
		fill.name = "Fill_%s" % id
		fill.light_energy = 0.55
		fill.shadow_enabled = false
		fill.omni_range = 8.0
		fill.omni_attenuation = 1.0
		fill.position = Vector3(x, 2.2, -3.0)
		_root.add_child(fill)
		if id == "floorhatch":
			# The wing wall sits on z = 0, so the approach fill never reaches the plate.
			# Keep the +Z omni dim. A hotter one turned the graphite lid into a white sheet.
			var deck := OmniLight3D.new()
			deck.name = "DeckFill"
			deck.light_energy = 0.75
			deck.shadow_enabled = false
			deck.omni_range = 6.0
			deck.omni_attenuation = 1.0
			deck.position = Vector3(x, 1.65, 2.05)
			_root.add_child(deck)
			# Front-open looks at the standing lid from −Z. The +Z deck light is behind that face.
			var face := SpotLight3D.new()
			face.name = "FloorFaceFill"
			face.light_energy = 0.85
			face.shadow_enabled = false
			face.spot_angle = 38.0
			face.spot_range = 6.0
			face.position = Vector3(x, 1.45, -1.35)
			_root.add_child(face)
			face.look_at(Vector3(x, 0.75, 0.45), Vector3.UP)
			continue
		var rim := SpotLight3D.new()
		rim.name = "Rim_%s" % id
		rim.light_energy = 0.8
		rim.light_color = RIM_C
		rim.spot_angle = 28.0
		rim.shadow_enabled = false
		rim.position = Vector3(x, 1.6, 2.4)
		_root.add_child(rim)
		rim.look_at(Vector3(x, 1.2, 0.0), Vector3.UP)
	# Ceiling wash so the overview reads as a room, not a black plane.
	for i in 4:
		var wash := OmniLight3D.new()
		wash.name = "CeilingWash%d" % i
		wash.light_energy = 0.55
		wash.light_color = WARM
		wash.shadow_enabled = false
		wash.omni_range = 14.0
		wash.omni_attenuation = 1.0
		wash.position = Vector3(-6.0 + float(i) * 6.0, 3.7, -4.0)
		_root.add_child(wash)


func _vestibules(doors: Dictionary) -> void:
	var mat := _pearl.duplicate() as StandardMaterial3D
	mat.resource_name = "VestibuleReturn"
	mat.albedo_color = Color(0.24, 0.26, 0.30)
	mat.albedo_texture = null
	mat.metallic = 0.0
	mat.roughness = 0.74
	for id in ["pocket", "bay3", "pair", "hatch"]:
		var door: Node3D = doors[id]
		var ab := _aabb_node(door)
		# Inset from the frame so the 40 mm wall gap does not show this return.
		var width := maxf(ab.size.x - 0.9, 1.15)
		var height := 3.6
		var cx := ab.get_center().x
		var z := 3.5
		var energy := 1.4
		var vz := 2.15
		var vmat := mat
		if id == "hatch":
			# The open plug leaves a hole. A close, wide return keeps that hole from reading as a void.
			width = maxf(width, 2.6)
			z = 2.40
			energy = 1.4
			vz = 1.55
			vmat = mat.duplicate() as StandardMaterial3D
			vmat.albedo_color = Color(0.24, 0.26, 0.30)
		var mi := MeshInstance3D.new()
		mi.name = "Vestibule_%s" % id
		var bm := BoxMesh.new()
		bm.size = Vector3(width, height, 0.05)
		mi.mesh = bm
		mi.position = Vector3(cx, height * 0.5 + 0.02, z)
		mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
		mi.set_surface_override_material(0, vmat)
		_root.add_child(mi)
		var lamp := OmniLight3D.new()
		lamp.name = "VestibuleLight_%s" % id
		lamp.light_energy = energy
		lamp.light_color = WARM
		lamp.shadow_enabled = false
		lamp.omni_range = 5.5
		# Between the open leaf and the return, so the approach face stays on the key.
		lamp.position = Vector3(cx, 1.7, vz)
		_root.add_child(lamp)


func _player(x: float, z: float) -> CharacterBody3D:
	var body := CharacterBody3D.new()
	body.name = "PlayerBody"
	body.set_script(load("res://scripts/door_lab/door_lab_player.gd"))
	body.position = Vector3(x, 0.0, z)
	# Yaw 180: local -Z, which is walk-forward, points at world +Z (toward the doors).
	body.rotation.y = PI
	_root.add_child(body)
	return body


func _door(id: String, x: float) -> MechDoor:
	var d := MechDoor.new()
	d.position = Vector3(x, 0.0, 0.0)
	_root.add_child(d)
	return d


func _spec(prof: MechDoorProfile, nm: String) -> Dictionary:
	for item in prof.leaves:
		if str(item.get("name", "")) == nm:
			return item
	return {"name": nm, "sign": 1, "stagger_open": 0.0, "stagger_close": 0.0}


func _proximity(door: MechDoor) -> void:
	if door.profile.interact or door.trigger_radius <= 0.05:
		return
	var area := Area3D.new()
	area.name = "Proximity"
	area.monitoring = true
	area.monitorable = false
	area.collision_layer = 0
	area.collision_mask = 1
	var cs := CollisionShape3D.new()
	cs.name = "ProximityShape"
	# A box along the approach (−Z) only. A sphere of this radius would swallow the next door.
	var depth := door.trigger_radius
	var box := BoxShape3D.new()
	box.size = Vector3(3.2, 2.8, depth)
	cs.shape = box
	cs.position = Vector3(0.0, 1.3, -depth * 0.5)
	area.add_child(cs)
	door.add_child(area)
	door.attach_proximity(area)


func _lamp(door: MechDoor, pos: Vector3, along_x: bool = false) -> void:
	var root := Node3D.new()
	root.name = "StatusLamp"
	root.position = pos
	door.add_child(root)
	var base := StandardMaterial3D.new()
	base.resource_name = "Mat_Hub_StateGlow"
	base.emission_enabled = true
	base.emission = Color("#FF9500")
	base.emission_energy_multiplier = 0.6
	base.albedo_color = Color(0.10, 0.06, 0.0)
	base.roughness = 0.35
	base.metallic = 0.0
	# 10 × 300 mm strip. Vertical on a wall jamb, flat along X when the lamp
	# sits in a floor frame. MechDoor paints §3 colours onto this material.
	var bar := MeshInstance3D.new()
	bar.name = "LampBar"
	var bm := BoxMesh.new()
	bm.size = Vector3(0.300, 0.010, 0.008) if along_x else Vector3(0.010, 0.300, 0.010)
	bar.mesh = bm
	bar.set_surface_override_material(0, base)
	root.add_child(bar)
	var light := OmniLight3D.new()
	light.name = "LampSpill"
	light.omni_range = 0.6
	light.light_energy = 0.15
	light.shadow_enabled = false
	root.add_child(light)
	var segs: Array = []
	for i in 8:
		var mi := MeshInstance3D.new()
		mi.name = "LampSeg%d" % i
		var sm := BoxMesh.new()
		sm.size = Vector3(0.032, 0.008, 0.006) if along_x else Vector3(0.008, 0.032, 0.006)
		mi.mesh = sm
		mi.position = Vector3((float(i) - 3.5) * 0.036, 0.0, 0.002) if along_x else Vector3(0.0, (float(i) - 3.5) * 0.036, 0.002)
		var seg := base.duplicate() as StandardMaterial3D
		mi.set_surface_override_material(0, seg)
		root.add_child(mi)
		segs.append(mi)
	door.attach_lamp(base, light, segs)


func _downlight(parent: Node3D, pos: Vector3, look: Vector3) -> void:
	var s := SpotLight3D.new()
	s.name = "Downlight"
	s.light_energy = 0.70
	s.light_color = WARM
	s.spot_angle = 45.0
	s.spot_range = 5.0
	s.shadow_enabled = true
	s.position = pos
	parent.add_child(s)
	s.look_at(look, Vector3.UP)


func _reveal(parent: Node3D, name: String, size: Vector3, pos: Vector3) -> void:
	var m := StandardMaterial3D.new()
	m.resource_name = "TT_CyanLED"
	# Emission stays full cyan. Albedo stays under the 0.90 cap even if the strip texture is white.
	m.albedo_color = Color(0.02, 0.10, 0.12)
	m.emission_enabled = true
	m.emission = CYAN
	m.emission_energy_multiplier = 0.7
	m.roughness = 0.3
	if ResourceLoader.exists(TEX_CYAN):
		m.albedo_texture = load(TEX_CYAN)
	var mi := MeshInstance3D.new()
	mi.name = name
	var bm := BoxMesh.new()
	bm.size = size
	mi.mesh = bm
	mi.position = pos
	mi.set_surface_override_material(0, m)
	parent.add_child(mi)


func _mesh(parent: Node3D, name: String, size: Vector3, pos: Vector3, mat: Material, bevel: float) -> MeshInstance3D:
	var mi := MeshInstance3D.new()
	mi.name = name
	if bevel > 0.001 and size.x > bevel * 3.0 and size.y > bevel * 3.0 and size.z > bevel * 3.0:
		mi.mesh = _beveled(size, bevel)
	else:
		var bm := BoxMesh.new()
		bm.size = size
		mi.mesh = bm
	mi.position = pos
	if mat != null:
		mi.set_surface_override_material(0, mat)
	parent.add_child(mi)
	return mi


func _static_box(name: String, size: Vector3, pos: Vector3, mat: Material) -> StaticBody3D:
	var body := StaticBody3D.new()
	body.name = name
	body.collision_layer = 1
	body.collision_mask = 1
	body.position = pos
	_root.add_child(body)
	var mi := MeshInstance3D.new()
	mi.name = "Visual"
	var bm := BoxMesh.new()
	bm.size = size
	mi.mesh = bm
	if mat != null:
		mi.set_surface_override_material(0, mat)
	body.add_child(mi)
	var cs := CollisionShape3D.new()
	cs.name = "Shape"
	var box := BoxShape3D.new()
	box.size = size
	cs.shape = box
	body.add_child(cs)
	if String(name).begins_with("Wing"):
		_wing_seams(body, size)
	return body


func _body_shape(body: AnimatableBody3D, size: Vector3) -> void:
	var cs := CollisionShape3D.new()
	cs.name = "LeafShape"
	var box := BoxShape3D.new()
	box.size = size
	cs.shape = box
	body.add_child(cs)


func _new_body(parent: Node3D) -> AnimatableBody3D:
	var body := AnimatableBody3D.new()
	body.name = "TT_LeafBody"
	# sync_to_physics reverts scripted poses until the next physics tick, and
	# writing that reverted transform back cancels the motion. Script drives
	# the node, then copies it onto the physics server in the same call.
	body.sync_to_physics = false
	body.collision_layer = 1
	body.collision_mask = 1
	if "max_contacts_reported" in body:
		body.max_contacts_reported = 6
	parent.add_child(body)
	# Entering the tree reapplies the kinematic constructor mode. Set static
	# after that. Kinematic body_set_state waits for the next physics step, so
	# the server origin lags the mesh by one tick (~31 mm at the scaled peak).
	# Static mode applies the transform in the same call the mesh moves.
	PhysicsServer3D.body_set_mode(body.get_rid(), PhysicsServer3D.BODY_MODE_STATIC)
	body.add_to_group("door_lab_leaf")
	return body


func _beveled(size: Vector3, bevel: float) -> ArrayMesh:
	var b := minf(bevel, minf(size.x, minf(size.y, size.z)) * 0.2)
	var hx := size.x * 0.5
	var hy := size.y * 0.5
	var hz := size.z * 0.5
	var st := SurfaceTool.new()
	st.begin(Mesh.PRIMITIVE_TRIANGLES)
	_quad(st, Vector3(-(hx - b), hy, -(hz - b)), Vector3(hx - b, hy, -(hz - b)), Vector3(hx - b, hy, hz - b), Vector3(-(hx - b), hy, hz - b))
	_quad(st, Vector3(-(hx - b), -hy, hz - b), Vector3(hx - b, -hy, hz - b), Vector3(hx - b, -hy, -(hz - b)), Vector3(-(hx - b), -hy, -(hz - b)))
	_quad(st, Vector3(hx, -(hy - b), -(hz - b)), Vector3(hx, hy - b, -(hz - b)), Vector3(hx, hy - b, hz - b), Vector3(hx, -(hy - b), hz - b))
	_quad(st, Vector3(-hx, -(hy - b), hz - b), Vector3(-hx, hy - b, hz - b), Vector3(-hx, hy - b, -(hz - b)), Vector3(-hx, -(hy - b), -(hz - b)))
	_quad(st, Vector3(-(hx - b), -(hy - b), hz), Vector3(hx - b, -(hy - b), hz), Vector3(hx - b, hy - b, hz), Vector3(-(hx - b), hy - b, hz))
	_quad(st, Vector3(hx - b, -(hy - b), -hz), Vector3(-(hx - b), -(hy - b), -hz), Vector3(-(hx - b), hy - b, -hz), Vector3(hx - b, hy - b, -hz))
	# 45-degree edges. Corners stay open a few millimetres; the faces carry the highlight.
	_quad(st, Vector3(hx - b, hy, hz - b), Vector3(hx - b, hy, -(hz - b)), Vector3(hx, hy - b, -(hz - b)), Vector3(hx, hy - b, hz - b))
	_quad(st, Vector3(-(hx - b), hy, -(hz - b)), Vector3(-(hx - b), hy, hz - b), Vector3(-hx, hy - b, hz - b), Vector3(-hx, hy - b, -(hz - b)))
	_quad(st, Vector3(hx - b, -hy, -(hz - b)), Vector3(hx - b, -hy, hz - b), Vector3(hx, -(hy - b), hz - b), Vector3(hx, -(hy - b), -(hz - b)))
	_quad(st, Vector3(-(hx - b), -hy, hz - b), Vector3(-(hx - b), -hy, -(hz - b)), Vector3(-hx, -(hy - b), -(hz - b)), Vector3(-hx, -(hy - b), hz - b))
	_quad(st, Vector3(-(hx - b), hy, hz - b), Vector3(hx - b, hy, hz - b), Vector3(hx - b, hy - b, hz), Vector3(-(hx - b), hy - b, hz))
	_quad(st, Vector3(hx - b, hy, -(hz - b)), Vector3(-(hx - b), hy, -(hz - b)), Vector3(-(hx - b), hy - b, -hz), Vector3(hx - b, hy - b, -hz))
	_quad(st, Vector3(hx - b, -hy, hz - b), Vector3(-(hx - b), -hy, hz - b), Vector3(-(hx - b), -(hy - b), hz), Vector3(hx - b, -(hy - b), hz))
	_quad(st, Vector3(-(hx - b), -hy, -(hz - b)), Vector3(hx - b, -hy, -(hz - b)), Vector3(hx - b, -(hy - b), -hz), Vector3(-(hx - b), -(hy - b), -hz))
	_quad(st, Vector3(hx, hy - b, hz - b), Vector3(hx, -(hy - b), hz - b), Vector3(hx - b, -(hy - b), hz), Vector3(hx - b, hy - b, hz))
	_quad(st, Vector3(hx, -(hy - b), -(hz - b)), Vector3(hx, hy - b, -(hz - b)), Vector3(hx - b, hy - b, -hz), Vector3(hx - b, -(hy - b), -hz))
	_quad(st, Vector3(-hx, -(hy - b), hz - b), Vector3(-hx, hy - b, hz - b), Vector3(-(hx - b), hy - b, hz), Vector3(-(hx - b), -(hy - b), hz))
	_quad(st, Vector3(-hx, hy - b, -(hz - b)), Vector3(-hx, -(hy - b), -(hz - b)), Vector3(-(hx - b), -(hy - b), -hz), Vector3(-(hx - b), hy - b, -hz))
	st.generate_normals()
	return st.commit()


func _quad(st: SurfaceTool, a: Vector3, b: Vector3, c: Vector3, d: Vector3) -> void:
	st.set_uv(Vector2(0, 0))
	st.add_vertex(a)
	st.set_uv(Vector2(1, 0))
	st.add_vertex(b)
	st.set_uv(Vector2(1, 1))
	st.add_vertex(c)
	st.set_uv(Vector2(0, 0))
	st.add_vertex(a)
	st.set_uv(Vector2(1, 1))
	st.add_vertex(c)
	st.set_uv(Vector2(0, 1))
	st.add_vertex(d)


func _hw(parent: Node3D, name: String, size: Vector3, pos: Vector3, mat: Material) -> MeshInstance3D:
	var mi := _mesh(parent, name, size, pos, mat, 0.0)
	mi.set_meta("hw_id", name)
	return mi


func _wing_seams(body: StaticBody3D, size: Vector3) -> void:
	var seam := StandardMaterial3D.new()
	seam.resource_name = "PanelSeam"
	seam.albedo_color = Color(0.08, 0.09, 0.10)
	seam.roughness = 0.85
	seam.metallic = 0.0
	var z := -size.z * 0.5 - 0.004
	var x := -size.x * 0.5 + 0.55
	var i := 0
	while x < size.x * 0.5 - 0.15:
		var mi := MeshInstance3D.new()
		mi.name = "PanelSeam%d" % i
		var bm := BoxMesh.new()
		bm.size = Vector3(0.012, size.y * 0.92, 0.008)
		mi.mesh = bm
		mi.position = Vector3(x, 0.0, z)
		mi.set_surface_override_material(0, seam)
		body.add_child(mi)
		x += 1.15
		i += 1
	var rail := MeshInstance3D.new()
	rail.name = "PanelRail"
	var rm := BoxMesh.new()
	rm.size = Vector3(size.x * 0.98, 0.012, 0.008)
	rail.mesh = rm
	rail.position = Vector3(0.0, 0.15, z)
	rail.set_surface_override_material(0, seam)
	body.add_child(rail)
	var band := MeshInstance3D.new()
	band.name = "WallSkirting"
	var sb := BoxMesh.new()
	sb.size = Vector3(size.x * 0.998, 0.07, 0.010)
	band.mesh = sb
	band.position = Vector3(0.0, -size.y * 0.5 + 0.045, z)
	band.set_surface_override_material(0, _alloy)
	body.add_child(band)


func _seat_reveals(door: Node3D, leaves: Array) -> void:
	if leaves.is_empty():
		return
	var ab := AABB()
	var any := false
	for item in leaves:
		var body: Node = item["body"]
		var stack: Array[Node] = [body]
		while not stack.is_empty():
			var n: Node = stack.pop_back()
			for c in n.get_children():
				stack.append(c)
			if not (n is MeshInstance3D) or (n as MeshInstance3D).mesh == null:
				continue
			var nm := String(n.name).to_lower()
			if "colonly" in nm or "roller" in nm or "dog" in nm or "bolt" in nm or "piston" in nm or "wheel" in nm or "handle" in nm:
				continue
			if not (n as MeshInstance3D).visible:
				continue
			var world: AABB = (n as MeshInstance3D).global_transform * (n as MeshInstance3D).mesh.get_aabb()
			ab = world if not any else ab.merge(world)
			any = true
	if not any:
		return
	var origin := door.global_position
	var x0 := ab.position.x - origin.x
	var x1 := x0 + ab.size.x
	var y0 := ab.position.y - origin.y
	var y1 := y0 + ab.size.y
	# 15 mm behind the approach face (+Z), on the frame so the strip does not ride the leaf.
	var zf := ab.position.z - origin.z + 0.015
	var frame := _find(door, "frame", true)
	if frame == null:
		frame = _find(door, "Frame", true)
	var host: Node3D = door
	var into := func(p: Vector3) -> Vector3:
		if frame == null:
			return p
		var world := door.global_transform * p
		return frame.global_transform.affine_inverse() * world
	if frame != null:
		host = frame
	_reveal(host, "Reveal_Soffit", Vector3(maxf(0.2, x1 - x0), 0.015, 0.012), into.call(Vector3((x0 + x1) * 0.5, y1 + 0.016, zf)))
	_reveal(host, "Reveal_JambL", Vector3(0.015, maxf(0.2, y1 - y0), 0.012), into.call(Vector3(x0 - 0.020, (y0 + y1) * 0.5, zf)))
	_reveal(host, "Reveal_JambR", Vector3(0.015, maxf(0.2, y1 - y0), 0.012), into.call(Vector3(x1 + 0.020, (y0 + y1) * 0.5, zf)))


func _skirt(door: Node3D) -> void:
	var host: Node = door.get_node_or_null("AsBuilt")
	if host == null:
		host = door
	var frame := _find(host, "frame", true)
	var ab := _aabb_node(frame if frame != null else host)
	if ab.size == Vector3.ZERO:
		return
	var origin := door.global_position
	var x0 := ab.position.x - origin.x
	var x1 := x0 + ab.size.x
	var y0 := ab.position.y - origin.y
	var y1 := y0 + ab.size.y
	var z := ab.position.z - origin.z - 0.010
	var t := 0.028
	_mesh(door, "Skirting", Vector3(x1 - x0 + t * 2.0, t, 0.008), Vector3((x0 + x1) * 0.5, y0 + t * 0.5, z), _alloy, 0.0)
	_mesh(door, "HeadTrim", Vector3(x1 - x0 + t * 2.0, t, 0.008), Vector3((x0 + x1) * 0.5, y1 - t * 0.5, z), _alloy, 0.0)
	_mesh(door, "JambTrimL", Vector3(t, maxf(0.2, y1 - y0), 0.008), Vector3(x0 - t * 0.5, (y0 + y1) * 0.5, z), _alloy, 0.0)
	_mesh(door, "JambTrimR", Vector3(t, maxf(0.2, y1 - y0), 0.008), Vector3(x1 + t * 0.5, (y0 + y1) * 0.5, z), _alloy, 0.0)


func _alias(parent: Node3D, nm: String, pos: Vector3) -> Node3D:
	var n := Node3D.new()
	n.name = nm
	n.position = pos
	parent.add_child(n)
	return n


func _load_glb(door: MechDoor, path: String) -> Node3D:
	if not ResourceLoader.exists(path):
		push_error("door lab missing %s" % path)
		return null
	var packed := load(path) as PackedScene
	if packed == null:
		push_error("door lab missing %s" % path)
		return null
	var inst := packed.instantiate() as Node3D
	inst.name = "AsBuilt"
	door.add_child(inst)
	return inst


func _claim_slide_leaf(leaf: Node3D) -> AnimatableBody3D:
	var parent := leaf.get_parent() as Node3D
	var body := _new_body(parent)
	body.name = String(leaf.name) + "Body"
	body.transform = leaf.transform
	var grabbed: Array[Node] = []
	var stack: Array[Node] = [leaf]
	while not stack.is_empty():
		var n: Node = stack.pop_back()
		for c in n.get_children():
			stack.append(c)
		if n == leaf:
			continue
		if n is MeshInstance3D or n is CollisionShape3D:
			grabbed.append(n)
	for raw in grabbed:
		var node := raw as Node3D
		if node.get_parent() == null:
			continue
		if node is CollisionShape3D and not (node.get_parent() is CollisionObject3D):
			continue
		var xf := _xf_under(node, leaf)
		node.get_parent().remove_child(node)
		body.add_child(node)
		node.transform = xf
		if node is MeshInstance3D and "colonly" in String(node.name).to_lower():
			(node as MeshInstance3D).visible = false
	if not _has_shape(body):
		_shapes_from_col_meshes(body)
	_convexify(body)
	parent.remove_child(leaf)
	leaf.queue_free()
	return body


func _has_shape(body: Node) -> bool:
	for c in body.get_children():
		if c is CollisionShape3D and (c as CollisionShape3D).shape != null:
			return true
	return false


func _shapes_from_col_meshes(body: Node3D) -> void:
	for c in body.get_children():
		if not (c is MeshInstance3D):
			continue
		var mi := c as MeshInstance3D
		if mi.mesh == null or "colonly" not in String(mi.name).to_lower():
			continue
		var shape := mi.mesh.create_convex_shape()
		var cs := CollisionShape3D.new()
		cs.name = "LeafShape"
		cs.shape = shape
		cs.transform = mi.transform
		body.add_child(cs)
		mi.visible = false


func _tag_rollers(body: Node3D) -> void:
	var stack: Array[Node] = [body]
	while not stack.is_empty():
		var n: Node = stack.pop_back()
		for c in n.get_children():
			stack.append(c)
		var nm := String(n.name).to_lower()
		if "roller" in nm and n is Node3D:
			var node := n as Node3D
			node.set_meta("door_hw", "roller_z")
			if "antilift" in nm:
				node.set_meta("roller_r", 0.015)
				node.set_meta("roller_sign", -1.0)
			else:
				node.set_meta("roller_r", 0.030)
				node.set_meta("roller_sign", 1.0)


func _each_named(root: Node, needle: String) -> Array:
	var out: Array = []
	var want := needle.to_lower()
	var stack: Array[Node] = [root]
	while not stack.is_empty():
		var n: Node = stack.pop_back()
		for c in n.get_children():
			stack.append(c)
		if n != root and want in String(n.name).to_lower() and n is Node3D:
			out.append(n)
	return out


func _root_names(n: Node) -> String:
	var s := ""
	for c in n.get_children():
		s += "%s:%s " % [c.name, c.get_class()]
	return s


func _pocket(prof: MechDoorProfile, x: float) -> MechDoor:
	var door := _door("pocket", x)
	var path := "res://assets/models/door_lab/door_lab_biparting_slide.glb"
	var inst := _load_glb(door, path)
	if inst == null:
		return door
	print("[door_lab] pocket roots ", _root_names(inst))
	var leaves: Array = []
	for side in [["leaf_L", -1], ["leaf_R", 1]]:
		var nm := str(side[0])
		var spec := _spec(prof, nm)
		var leaf := _find(inst, nm, false)
		if leaf == null:
			push_error("door lab pivot missing %s" % nm)
			_dump(inst)
			continue
		var rest := leaf.position
		var body := _claim_slide_leaf(leaf)
		_tag_rollers(body)
		for seal in _each_named(body, "_seal"):
			_alias(seal as Node3D, "BulbSeal", Vector3.ZERO)
			# Right seal sits 3 mm forward so the meeting stile does not z-fight.
			# 4 mm moved the face-union centre onto the 2 mm shape-drift limit.
			if nm == "leaf_R":
				(seal as Node3D).position.z += 0.003
		_alias(body, "FloorGuide", Vector3(0.0, -2.36, -0.02))
		var meet := 0.42 if int(side[1]) < 0 else -0.42
		_hw(body, "ManualHandle", Vector3(0.018, 0.22, 0.016), Vector3(meet, -1.15, -0.036), _alloy)
		print("[door_lab] pocket %s rest=%s shapes=%s" % [nm, rest, _has_shape(body)])
		leaves.append({
			"name": nm,
			"sign": int(spec.get("sign", int(side[1]))),
			"stagger_open": float(spec.get("stagger_open", 0.0)),
			"stagger_close": float(spec.get("stagger_close", 0.0)),
			"body": body,
			"pivot": body,
			"rest": rest,
			"axis": Vector3(1, 0, 0),
		})
	# v1 ships with the access panel swung open. Close it for the hero.
	var panel := _find(inst, "slide_AccessPanel", false)
	if panel != null:
		panel.rotate_object_local(Vector3(1, 0, 0), deg_to_rad(-90.0))
	_retint(inst)
	_hide_exact(inst, "status_light")
	_hide_named_contains(inst, "reveal_strips")
	_hide_colonly_meshes(inst)
	_paint_surround(inst)
	for item in leaves:
		_vision_lite(item["body"])
		if str(item["name"]) == "leaf_R":
			_nudge_named_z(item["body"], 0.003)
	_pocket_tokens(door, inst)
	_skirt(door)
	_seat_reveals(door, leaves)
	# Camera sits on +X / −Z. The right jamb face is the one in the hero frame.
	_lamp(door, Vector3(1.10, 1.40, -0.125))
	_downlight(door, Vector3(0, 2.85, -0.45), Vector3(x, 1.4, 0))
	door.bind(prof, leaves, false)
	door.configure_sensor(Vector3(0, 1.15, 0), Vector3(1.85, 2.15, 0.50))
	door.set_approach(Vector3(0, 0, -1))
	_proximity(door)
	_mark_walk(door)
	door.set_meta("block_x", 0.0)
	door.set_meta("glb", path)
	return door


func _pocket_tokens(door: Node3D, inst: Node3D) -> void:
	var frame := _find(inst, "frame", true)
	var host: Node3D = frame if frame != null else door
	# HeadBox is not in the GLB. Radar is the only extra overlay. The rest are modeled.
	_alias(host, "HeadBox", Vector3(0.0, 2.55, -0.06))
	_hw(door, "Radar", Vector3(0.10, 0.032, 0.036), Vector3(0.0, 2.18, -0.14), _gun)


func _pocket_tokens_passb(door: Node3D, inst: Node3D) -> void:
	var frame := _find(inst, "frame", true)
	var host: Node3D = frame if frame != null else door
	_hw(door, "AccessPanel", Vector3(0.22, 0.06, 0.006), Vector3(0.0, 2.50, -0.090), _alloy)
	_alias(door, "Motor", Vector3(0.0, 2.58, -0.04))
	_alias(door, "TensionerL", Vector3(-1.99, 2.50, -0.02))
	_alias(door, "TensionerR", Vector3(1.99, 2.50, -0.02))
	_alias(door, "BumperL", Vector3(-2.05, 1.20, 0.0))
	_alias(door, "BumperR", Vector3(2.05, 1.20, 0.0))
	_hw(door, "Solenoid", Vector3(0.06, 0.028, 0.022), Vector3(-0.05, 2.38, -0.092), _alloy)
	_hw(door, "Keeper", Vector3(0.028, 0.022, 0.016), Vector3(0.04, 2.38, -0.092), _alloy)
	_hw(door, "HexRelease", Vector3(0.045, 0.055, 0.006), Vector3(-1.08, 1.15, -0.090), _alloy)
	for side in [-1, 1]:
		var sx := float(side)
		for i in 4:
			_hw(door, "LightCurtain%s%d" % [("L" if side < 0 else "R"), i], Vector3(0.012, 0.012, 0.008), Vector3(sx * 1.06, 0.48 + float(i) * 0.42, -0.090), _alloy)


func _hatch(prof: MechDoorProfile, x: float) -> MechDoor:
	var door := _door("hatch", x)
	var path := "res://assets/models/door_lab/door_lab_bulkhead_hatch.glb"
	var inst := _load_glb(door, path)
	if inst == null:
		return door
	print("[door_lab] hatch roots ", _root_names(inst))
	var spec := _spec(prof, "leaf")
	var pivot := _find(inst, "leaf", false)
	if pivot == null:
		push_error("door lab pivot missing leaf")
		_dump(inst)
		return door
	var body := _rig_pivot(pivot)
	_tag_hatch(inst)
	_retint(inst)
	_paint_status_green(inst)
	_hide_colonly_meshes(inst)
	_paint_hatch_leaf(inst)
	_paint_surround(inst)
	_clamp_rods(body)
	_hatch_tokens(door, inst, body)
	_clamp_rods(body)
	_indicator_bar(body)
	_stamp_readouts(inst)
	if body != null:
		var face_z := -0.162
		_wear_patch(body, "WearWheel", Vector3(-0.65, 1.27, face_z - 0.014), Vector3(0.15, 0.036, 0.010), _orange)
		_hatch_bevels(body, face_z)
		_wear_patch(body, "WearKick", Vector3(-0.65, 0.22, face_z - 0.003), Vector3(0.22, 0.14, 0.004), _graphite)
	_seat_reveals(door, [{"body": body}])
	_hatch_frame_reveal(door)
	_hatch_hazard_frame(door)
	_skirt(door)
	# On the camera-facing jamb, clear of the plug, centred at 1.4 m.
	_jamb_lamp(door)
	_downlight(door, Vector3(0, 2.90, -0.55), Vector3(x, 1.2, -0.1))
	# The plug face is recessed in the shell. A close fill is what makes graphite and the dogs read.
	var face_fill := OmniLight3D.new()
	face_fill.name = "HatchFaceFill"
	face_fill.light_energy = 0.72
	face_fill.shadow_enabled = false
	face_fill.omni_range = 3.4
	face_fill.omni_attenuation = 1.4
	face_fill.position = Vector3(0.08, 1.55, -0.95)
	door.add_child(face_fill)
	var leaves: Array = [{
		"name": "leaf",
		"sign": int(spec.get("sign", 1)),
		"stagger_open": float(spec.get("stagger_open", 0.0)),
		"stagger_close": float(spec.get("stagger_close", 0.0)),
		"body": body,
		"pivot": pivot,
		"rest": Vector3.ZERO,
		"axis": Vector3.ZERO,
	}]
	print("[door_lab] hatch hinge %s shapes=%s" % [pivot.position, _has_shape(body)])
	door.bind(prof, leaves, true)
	# Probe for the obstruction check stands on the approach side. The plug swings to +Z.
	door.configure_sensor(Vector3(0.0, 1.05, -0.55), Vector3(0.90, 1.90, 1.05))
	door.set_approach(Vector3(0, 0, -1))
	_mark_walk(door)
	door.set_meta("block_x", 0.0)
	door.set_meta("glb", path)
	return door


func _tag_hatch(inst: Node3D) -> void:
	# GLB dogs and linkages throw 25 mm on local +X. LockWheel is 90 deg. The orange handwheel is 12 turns.
	# "bulkhead_dog_0" (not "bulkhead_dog_"): the fixed bulkhead_dog_guides node must not slide with the dogs.
	for n in _each_named(inst, "bulkhead_dog_0") + _each_named(inst, "bulkhead_linkage_"):
		var bolt := n as Node3D
		bolt.set_meta("door_hw", "dog_x")
		bolt.set_meta("throw_m", 0.025)
	var wheel := _find(inst, "bulkhead_LockWheel", false)
	if wheel != null:
		wheel.set_meta("door_hw", "wheel_z")
	var hand := _find(inst, "bulkhead_OverrideOrange_Handwheel", false)
	if hand != null:
		hand.set_meta("door_hw", "wheel_z")
		hand.set_meta("wheel_deg", 4320.0)
	var seal := _find(inst, "bulkhead_InflatableSeal", false)
	if seal != null:
		seal.set_meta("door_hw", "seal_z")
		seal.set_meta("inflate_scale", 1.385)
	for n2 in _each_named(inst, "gauge_needle"):
		(n2 as Node3D).set_meta("door_hw", "needle_z")
	var rod := _find(inst, "bulkhead_DamperRod", false)
	var cyl := _find(inst, "bulkhead_Damper_body", false)
	if rod != null and cyl != null:
		rod.set_meta("door_hw", "piston")
		cyl.set_meta("door_hw", "piston")
		rod.set_meta("piston_partner", cyl)
		cyl.set_meta("piston_partner", rod)


func _hatch_tokens(door: Node3D, inst: Node3D, leaf_body: Node3D) -> void:
	# The GLB already has the hinge, davit, dogs, wheel, seal, and readout. Only the missing tokens are overlays.
	_hw(door, "HoldOpenCatch", Vector3(0.045, 0.028, 0.030), Vector3(0.78, 0.42, -0.10), _alloy)
	# Leaf hazard stripes stay off (pass E). The amber/graphite checker is the frame, not the plug.


func _hatch_tokens_passb(door: Node3D, inst: Node3D, leaf_body: Node3D) -> void:
	var hinge := _find(inst, "hinge_frame", false)
	if hinge != null:
		_alias(hinge, "HingeHeavy", Vector3(0.62, 0.55, -0.02))
		_alias(hinge, "Actuator", Vector3(0.62, 0.32, -0.04))
	var rams := _find(inst, "pushoff_rams", false)
	if rams != null:
		_alias(rams, "PushOffRam", Vector3(-0.50, 0.85, -0.02))
	_hw(door, "Davit", Vector3(0.028, 0.028, 0.36), Vector3(-0.10, 2.40, -0.18), _alloy)
	_hw(door, "EqualizePort", Vector3(0.07, 0.05, 0.010), Vector3(-0.62, 1.62, -0.18), _alloy)
	_hw(door, "HoldOpenCatch", Vector3(0.045, 0.028, 0.030), Vector3(0.78, 0.42, -0.10), _alloy)
	_hw(door, "EqualizeLever", Vector3(0.018, 0.12, 0.016), Vector3(-0.62, 1.02, -0.19), _orange)
	_hw(door, "EqualizeGrille", Vector3(0.10, 0.08, 0.008), Vector3(-0.62, 1.78, -0.16), _alloy)
	# The plug shell's approach face is local z = -0.14. Hardware behind that is hidden.
	if leaf_body != null:
		var face_z := -0.162
		_spoke_wheel(leaf_body, "OverrideOrange", Vector3(-0.65, 1.12, face_z), 0.15, 0.015, _orange)
		# 150 mm scuff along the top of the tube. A square behind the rim reads as a card.
		_wear_patch(leaf_body, "WearWheel", Vector3(-0.65, 1.27, face_z - 0.014), Vector3(0.15, 0.036, 0.010), _orange)
		_hatch_bevels(leaf_body, face_z)
		var dogs := [
			Vector2(-1.02, 0.72), Vector2(-1.02, 1.52),
			Vector2(-0.28, 0.78), Vector2(-0.28, 1.48),
			Vector2(-0.88, 1.88), Vector2(-0.42, 1.88),
			Vector2(-0.88, 0.36), Vector2(-0.42, 0.36),
		]
		for i in dogs.size():
			var d: Vector2 = dogs[i]
			var block := _mesh(leaf_body, "DogPivot%d" % i, Vector3(0.034, 0.034, 0.030), Vector3(d.x, d.y, face_z), _alloy, 0.003)
			_mesh(block, "DogPin", Vector3(0.014, 0.014, 0.022), Vector3(0.0, 0.0, -0.012), _gun, 0.0)
		var plate := _mesh(leaf_body, "IdPlate", Vector3(0.10, 0.055, 0.005), Vector3(-0.95, 1.72, face_z), _alloy, 0.001)
		_mesh(plate, "IdInset", Vector3(0.072, 0.032, 0.003), Vector3(0.0, 0.0, -0.002), _graphite, 0.0)
		_wear_patch(leaf_body, "WearKick", Vector3(-0.65, 0.22, face_z - 0.003), Vector3(0.22, 0.14, 0.004), _graphite)
		_readout(leaf_body, "DigitalReadout", Vector3(-0.95, 1.58, face_z))
	_readout(door, "DigitalReadoutBack", Vector3(0.28, 1.55, 0.22))
	_linkage_and_ribs(door, leaf_body)


func _wall_piece(body: StaticBody3D, size: Vector3, pos: Vector3) -> void:
	var cs := CollisionShape3D.new()
	var box := BoxShape3D.new()
	box.size = size
	cs.shape = box
	cs.position = pos
	body.add_child(cs)


func _gauge(parent: Node3D, name: String, pos: Vector3) -> void:
	var g := _hw(parent, name, Vector3(0.10, 0.10, 0.02), pos, _alloy)
	var needle := _mesh(g, "Needle", Vector3(0.004, 0.035, 0.004), Vector3(0, 0.01, -0.012), _orange, 0.0)
	needle.set_meta("door_hw", "needle")
	_hw(g, "DigitalReadout", Vector3(0.06, 0.02, 0.004), Vector3(0, -0.07, 0), _graphite)


func _glb_door(prof: MechDoorProfile, x: float, path: String, pivots: Array, hinge: bool) -> MechDoor:
	var door := _door(prof.door_id, x)
	var packed := load(path) as PackedScene
	if packed == null:
		push_error("door lab missing %s" % path)
		return door
	var inst := packed.instantiate() as Node3D
	inst.name = "AsBuilt"
	door.add_child(inst)
	_disable_named(inst, "Clear")
	_disable_named(inst, "DoorClear")
	var leaves: Array = []
	for nm in pivots:
		var spec := _spec(prof, str(nm))
		var pivot := _find(inst, str(nm), true)
		if pivot == null:
			push_error("door lab pivot missing %s in %s" % [nm, path])
			_dump(inst)
			continue
		var body := _rig_pivot(pivot)
		leaves.append({
			"name": str(nm),
			"sign": int(spec.get("sign", 1)),
			"stagger_open": float(spec.get("stagger_open", 0.0)),
			"stagger_close": float(spec.get("stagger_close", 0.0)),
			"body": body,
			"pivot": pivot,
			"rest": Vector3.ZERO,
			"axis": Vector3.ZERO,
		})
	if leaves.is_empty():
		push_error("door lab has no leaves in %s" % path)
		_dump(inst)
		return door
	_shift_to_plane(inst, leaves)
	_retint(inst)
	_hide_colonly_meshes(inst)
	_rename_glass(inst)
	if prof.door_id == "bay3":
		_hide_show_meshes(inst)
	_bay_pair_hw(door, inst, prof.door_id, leaves)
	_seat_reveals(door, leaves)
	var leaf_ab := _aabb_node(leaves[0]["body"])
	for item in leaves:
		leaf_ab = leaf_ab.merge(_aabb_node(item["body"]))
		_wear_leaf(item["body"], prof.door_id)
	var face_z := leaf_ab.position.z - door.global_position.z
	var top_y := leaf_ab.position.y + leaf_ab.size.y
	var leaf_x1 := leaf_ab.position.x + leaf_ab.size.x - door.global_position.x
	# Pair: 30 mm outboard of the leaf, 20 mm proud of the face, so the hero sees the strip.
	var jamb_x := leaf_x1 + 0.03
	var lamp_z := face_z - 0.02
	if prof.door_id == "bay3":
		# leaf_x1 − 0.35 m and 0.28 m proud put the moving cyan lamp on the left leaf.
		# The reveal is already on the frame, outside the glass. Step outboard of that.
		var jamb := _find(door, "Reveal_JambR", false)
		if jamb == null:
			jamb = _find(door, "Reveal_JambL", false)
		if jamb != null:
			var local := door.to_local(jamb.global_position)
			var out := 0.030 if local.x >= 0.0 else -0.030
			jamb_x = local.x + out
			lamp_z = local.z
	_lamp(door, Vector3(jamb_x, 1.40, lamp_z))
	_downlight(door, Vector3(0, top_y + 0.45, face_z - 0.40), Vector3(x, 1.3, 0))
	door.bind(prof, leaves, hinge)
	if prof.door_id == "bay3":
		door.configure_sensor(Vector3(0, 1.2, 0.75), Vector3(3.6, 2.3, 1.35))
		_bay_guards(door, leaves)
	else:
		door.configure_sensor(Vector3(0, 1.15, 0.6), Vector3(1.7, 2.2, 1.15))
		_pair_sweeps(leaves)
	door.set_approach(Vector3(0, 0, -1))
	_proximity(door)
	_mark_walk(door)
	door.set_meta("block_x", 0.0)
	door.set_meta("glb", path)
	_skirt(door)
	if prof.door_id == "pair":
		_trim_pair_frame(inst, leaves)
		_open_pair_meeting(leaves)
	return door


func _find(root: Node, nm: String, skip_collision: bool) -> Node3D:
	var stack: Array[Node] = [root]
	while not stack.is_empty():
		var n: Node = stack.pop_back()
		if n != root and String(n.name) == nm and n is Node3D:
			if skip_collision and n is CollisionObject3D:
				pass
			else:
				return n as Node3D
		for c in n.get_children():
			stack.append(c)
	return null


func _dump(root: Node) -> void:
	var stack: Array[Node] = [root]
	var shown := 0
	while not stack.is_empty() and shown < 60:
		var n: Node = stack.pop_back()
		print("[door_lab] node ", n.name, " ", n.get_class())
		shown += 1
		for c in n.get_children():
			stack.append(c)


func _rig_pivot(pivot: Node3D) -> AnimatableBody3D:
	var body := _new_body(pivot)
	body.transform = Transform3D.IDENTITY
	var pending: Array = []
	var stack: Array[Node] = [pivot]
	while not stack.is_empty():
		var n: Node = stack.pop_back()
		for c in n.get_children():
			if c == body:
				continue
			stack.append(c)
		if n == pivot or n == body:
			continue
		if n is MeshInstance3D or n is CollisionShape3D:
			pending.append(n)
	for n in pending:
		var node := n as Node3D
		var xf := _xf_under(node, pivot)
		var parent := node.get_parent()
		if node is CollisionShape3D and not (parent is CollisionObject3D):
			continue
		parent.remove_child(node)
		body.add_child(node)
		node.transform = xf
	var holders: Array = []
	var stack2: Array[Node] = [pivot]
	while not stack2.is_empty():
		var n2: Node = stack2.pop_back()
		for c2 in n2.get_children():
			if c2 == body:
				continue
			stack2.append(c2)
		if n2 is CollisionObject3D and n2 != body:
			holders.append(n2)
	for h in holders:
		var still := false
		for ch in (h as Node).get_children():
			if ch is CollisionShape3D:
				still = true
		if not still:
			(h as CollisionObject3D).collision_layer = 0
			(h as CollisionObject3D).collision_mask = 0
	_convexify(body)
	return body


func _decomp_settings() -> MeshConvexDecompositionSettings:
	# Tightest values Godot 4.7 accepts. max_convex_hulls caps at 32.
	var settings := MeshConvexDecompositionSettings.new()
	settings.max_convex_hulls = 32
	settings.max_concavity = 0.001
	settings.resolution = 100000
	settings.max_num_vertices_per_convex_hull = 64
	settings.convex_hull_approximation = false
	settings.plane_downsampling = 1
	settings.convex_hull_downsampling = 1
	settings.project_hull_vertices = true
	settings.min_volume_per_convex_hull = 0.0001
	return settings


func _hulls_from_mesh(mesh: Mesh, settings: MeshConvexDecompositionSettings) -> Array[ConvexPolygonShape3D]:
	# Mesh.convex_decompose is not bound in 4.7.2. The editor helper is.
	var out: Array[ConvexPolygonShape3D] = []
	var probe := MeshInstance3D.new()
	probe.mesh = mesh
	probe.create_multiple_convex_collisions(settings)
	var stack: Array[Node] = [probe]
	while not stack.is_empty():
		var n: Node = stack.pop_back()
		for c in n.get_children():
			stack.append(c)
		if n is CollisionShape3D:
			var shape := (n as CollisionShape3D).shape as ConvexPolygonShape3D
			if shape != null:
				out.append(shape)
	probe.free()
	return out


func _convexify(body: Node) -> void:
	# Convex-vs-convex is the clip test. One hull of a concave leaf fills the
	# dish and clips the frame once the leaf swings. Decompose the debug mesh
	# into tight hulls instead of keeping the concave shape.
	var settings := _decomp_settings()
	var targets: Array[CollisionShape3D] = []
	for c in body.get_children():
		if not (c is CollisionShape3D):
			continue
		if (c as CollisionShape3D).shape is ConcavePolygonShape3D:
			targets.append(c)
	for cs in targets:
		# get_debug_mesh() is a line gizmo. VHACD then returns one hull of the
		# vertices, which is the fat hull. Feed it the triangle faces instead.
		var faces: PackedVector3Array = (cs.shape as ConcavePolygonShape3D).data
		if faces.size() < 3:
			continue
		var arrays: Array = []
		arrays.resize(Mesh.ARRAY_MAX)
		arrays[Mesh.ARRAY_VERTEX] = faces
		var soup := ArrayMesh.new()
		soup.add_surface_from_arrays(Mesh.PRIMITIVE_TRIANGLES, arrays)
		var shapes := _hulls_from_mesh(soup, settings)
		# A single VHACD hull is the voxel box. The exact vertex hull is tighter.
		if shapes.size() <= 1:
			cs.shape = soup.create_convex_shape()
			print("[door_lab] convex %s -> exact" % cs.name)
			continue
		var parent := cs.get_parent()
		var xf := cs.transform
		var nm := String(cs.name)
		cs.shape = shapes[0]
		for i in range(1, shapes.size()):
			var extra := CollisionShape3D.new()
			extra.name = "%s_hull_%d" % [nm, i]
			extra.shape = shapes[i]
			extra.transform = xf
			parent.add_child(extra)
		print("[door_lab] convex %s -> %d hulls" % [nm, shapes.size()])


func _hinge_swing(body: Node3D) -> Vector2:
	# x = how far the collider reaches from the hinge on its thin axis.
	# y = that axis (0, 1, or 2). At 90° the +side enters the jamb.
	var pts: Array[Vector3] = []
	for ch in body.get_children():
		if not (ch is CollisionShape3D):
			continue
		var cs := ch as CollisionShape3D
		var poly := cs.shape as ConvexPolygonShape3D
		if poly == null:
			continue
		for p in poly.points:
			pts.append(cs.transform * p)
	if pts.is_empty():
		return Vector2(0.0, 2.0)
	var lo := pts[0]
	var hi := pts[0]
	for p in pts:
		lo = lo.min(p)
		hi = hi.max(p)
	var ext := hi - lo
	var axis := 0
	var thin := ext.x
	if ext.y < thin:
		axis = 1
		thin = ext.y
	if ext.z < thin:
		axis = 2
		thin = ext.z
	var past := 0.0
	var jamb := 0.0
	for p in pts:
		var c := p.x
		if axis == 1:
			c = p.y
		elif axis == 2:
			c = p.z
		past = maxf(past, absf(c))
		jamb = maxf(jamb, c)
	return Vector2(maxf(past, jamb), float(axis))


func _visual_jamb_past(body: Node3D, axis: int) -> float:
	var past := 0.0
	var stack: Array[Node] = [body]
	while not stack.is_empty():
		var n: Node = stack.pop_back()
		for c in n.get_children():
			stack.append(c)
		if not (n is MeshInstance3D):
			continue
		var mi := n as MeshInstance3D
		if mi.mesh == null or mi.mesh.get_surface_count() < 1:
			continue
		var arr: Array = mi.mesh.surface_get_arrays(0)
		var vs: PackedVector3Array = arr[Mesh.ARRAY_VERTEX]
		var xf := _xf_under(mi, body)
		for v in vs:
			var local: Vector3 = xf * v
			var c := local.x
			if axis == 1:
				c = local.y
			elif axis == 2:
				c = local.z
			past = maxf(past, c)
	return past


func _trim_pair_frame(inst: Node3D, leaves: Array) -> void:
	# The 50 mm slab is centred on the hinge, so at 90° it enters the jamb by
	# that half-extent. Pull only the jamb-cheek collision outboard of the
	# swing and leave the leaf collider full thickness, so both closed faces
	# still stop the capsule. The visual frame is unchanged.
	var frame := _find(inst, "Frame", false)
	if frame == null or leaves.is_empty():
		return
	var left_hinge := INF
	var right_hinge := -INF
	var past := 0.0
	var axis := 2
	for item in leaves:
		var body: Node3D = item["body"]
		var hx := body.global_position.x
		left_hinge = minf(left_hinge, hx)
		right_hinge = maxf(right_hinge, hx)
		var swing := _hinge_swing(body)
		axis = int(swing.y)
		past = maxf(past, swing.x)
		past = maxf(past, _visual_jamb_past(body, axis))
	if past <= 0.0:
		return
	var gap := 0.002
	var left_limit := left_hinge - past - gap
	var right_limit := right_hinge + past + gap
	var band := past + 0.04
	var stack: Array[Node] = [frame]
	var moved := 0
	while not stack.is_empty():
		var n: Node = stack.pop_back()
		for c in n.get_children():
			stack.append(c)
		if not (n is CollisionShape3D):
			continue
		var cs := n as CollisionShape3D
		var concave := cs.shape as ConcavePolygonShape3D
		if concave == null:
			continue
		var raw := concave.data
		var out := PackedVector3Array()
		out.resize(raw.size())
		var inv := cs.global_transform.affine_inverse()
		for i in raw.size():
			var world: Vector3 = cs.global_transform * raw[i]
			if world.x < left_hinge + band and world.x > left_limit:
				world.x = left_limit
				moved += 1
			elif world.x > right_hinge - band and world.x < right_limit:
				world.x = right_limit
				moved += 1
			out[i] = inv * world
		var copy := concave.duplicate() as ConcavePolygonShape3D
		copy.data = out
		cs.shape = copy
	print("[door_lab] pair frame cheek past %.4f left %.3f right %.3f moved %d" % [past, left_limit, right_limit, moved])


func _xf_under(node: Node3D, ancestor: Node) -> Transform3D:
	var xf := Transform3D.IDENTITY
	var n: Node = node
	while n != null and n != ancestor:
		if n is Node3D:
			xf = (n as Node3D).transform * xf
		n = n.get_parent()
	return xf


func _shift_to_plane(inst: Node3D, leaves: Array) -> void:
	if leaves.is_empty():
		return
	var ab := _aabb_node(leaves[0]["body"])
	for item in leaves:
		ab = ab.merge(_aabb_node(item["body"]))
	var cz := ab.position.z + ab.size.z * 0.5
	inst.position.z -= cz
	_notes.append("shifted %s by z %.3f so the closed leaf plane is at the door origin" % [inst.get_parent().name if false else "glb", -cz])


func _disable_named(root: Node, needle: String) -> void:
	var stack: Array[Node] = [root]
	while not stack.is_empty():
		var n: Node = stack.pop_back()
		for c in n.get_children():
			stack.append(c)
		if needle.to_lower() in String(n.name).to_lower() and n is CollisionObject3D:
			(n as CollisionObject3D).collision_layer = 0
			(n as CollisionObject3D).collision_mask = 0


func _retint(root: Node) -> void:
	var stack: Array[Node] = [root]
	var i := 0
	while not stack.is_empty():
		var n: Node = stack.pop_back()
		for c in n.get_children():
			stack.append(c)
		if n is MeshInstance3D:
			var mi := n as MeshInstance3D
			if mi.mesh == null:
				continue
			for s in mi.mesh.get_surface_count():
				var mat := mi.get_active_material(s)
				if mat == null:
					continue
				var label := "%s %s" % [mat.resource_name, mi.name]
				var low := label.to_lower()
				var mesh_low := String(mi.name).to_lower()
				if _retint_forced(mi, s, mesh_low, low):
					i += 1
					continue
				if not (mat is BaseMaterial3D):
					continue
				var dup := (mat as BaseMaterial3D).duplicate() as BaseMaterial3D
				if "push_bar" in mesh_low or "push_plate" in mesh_low:
					dup.albedo_color = AMBER_PLATE
					dup.albedo_texture = null
					dup.metallic = 0.15
					dup.roughness = 0.42
					if dup is StandardMaterial3D:
						var plate := dup as StandardMaterial3D
						plate.emission_enabled = false
						plate.emission_energy_multiplier = 0.0
					mi.set_surface_override_material(s, dup)
					i += 1
					continue
				if "door_scissor" in low or "side_scissor" in low or "upper_scissor" in low:
					# The GLB frit is a flat cyan (184, 219, 237) with the pattern in alpha.
					# Leaf bodies use a cool project grey. Cyan stays on the reveal strips.
					if dup is StandardMaterial3D:
						var frit := dup as StandardMaterial3D
						frit.albedo_texture = _neutral_frit(frit.albedo_texture)
						frit.emission_enabled = false
						# Pattern twice as large, anisotropic mips, so the header and the leaves do not moire.
						frit.texture_filter = BaseMaterial3D.TEXTURE_FILTER_LINEAR_WITH_MIPMAPS_ANISOTROPIC
						frit.uv1_scale = Vector3(0.5, 0.5, 0.5)
					dup.albedo_color = Color(0.80, 0.82, 0.84, 1.0)
					dup.roughness = 0.32
					dup.metallic = 0.10
					dup.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
					dup.alpha_antialiasing_mode = BaseMaterial3D.ALPHA_ANTIALIASING_ALPHA_TO_COVERAGE
					dup.alpha_scissor_threshold = 0.2
				elif "whitecomposite" in low or "white_composite" in low or "pearl" in low:
					# Blue stays at 0.900. #D8DEE6's 0.902 is only legal on the WhiteComposite name.
					dup.albedo_color = Color(0.847, 0.871, 0.900, dup.albedo_color.a)
					dup.albedo_texture = null
					dup.metallic = 0.1
					dup.roughness = 0.72
				elif "glass" in low or "vision" in low:
					var gid := _owner_id(mi)
					if gid == "pocket" or gid == "bay3" or gid == "":
						dup.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
						dup.albedo_color = Color(0.30, 0.36, 0.42, 0.25)
						dup.roughness = 0.05
						dup.metallic = 0.0
						if dup is StandardMaterial3D:
							(dup as StandardMaterial3D).emission_enabled = false
					else:
						dup.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA_SCISSOR
						dup.alpha_scissor_threshold = 0.2
						dup.albedo_color = Color(0.76, 0.86, 0.90, 1.0)
						dup.roughness = 0.05
						dup.metallic = 0.0
						if dup is StandardMaterial3D:
							(dup as StandardMaterial3D).emission_enabled = false
				elif "cyan" in low or "court_line" in low or ("led" in low and "amber" not in low) or ("scissor" in low and "glass" not in low):
					dup.albedo_color = Color(0.02, 0.10, 0.12, 1.0)
					if dup is StandardMaterial3D:
						var sd := dup as StandardMaterial3D
						sd.emission_enabled = true
						sd.emission = Color(0.0, 0.45, 0.52)
						sd.emission_energy_multiplier = 0.28
				elif "seal" in low or "rubber" in low:
					var c := dup.albedo_color
					dup.albedo_color = Color(minf(c.r, 0.90), minf(c.g, 0.90), minf(c.b, 0.90), c.a)
				else:
					var c2 := dup.albedo_color
					var hot := maxf(c2.r, maxf(c2.g, c2.b))
					if hot > 0.001 and hot < 0.16:
						var lift := 0.22 / hot
						dup.albedo_color = Color(minf(c2.r * lift, 0.90), minf(c2.g * lift, 0.90), minf(c2.b * lift, 0.90), c2.a)
					else:
						dup.albedo_color = Color(minf(c2.r, 0.90), minf(c2.g, 0.90), minf(c2.b, 0.90), c2.a)
				mi.set_surface_override_material(s, dup)
				i += 1


func _rename_glass(root: Node) -> void:
	var stack: Array[Node] = [root]
	var k := 0
	while not stack.is_empty():
		var n: Node = stack.pop_back()
		for c in n.get_children():
			stack.append(c)
		if "glass" in String(n.name).to_lower():
			n.name = "VisionPane%d" % k
			k += 1


func _bay_pair_hw(door: Node3D, _inst: Node3D, id: String, leaves: Array) -> void:
	_hw(door, "StatusLampMount", Vector3(0.4, 0.03, 0.03), Vector3(0, 2.32, -0.22), _alloy)
	if id == "bay3":
		_hw(door, "Transom", Vector3(3.6, 0.16, 0.20), Vector3(0, 2.48, -0.18), _gun)
		for item in leaves:
			var body: Node3D = item["body"]
			var box := _named_local_aabb(body, "stile")
			if box.size == Vector3.ZERO:
				continue
			var hinge_x := _near_edge(box)
			var meet_x := _far_edge(box)
			var inward := signf(meet_x - hinge_x)
			var mid_x := (hinge_x + meet_x) * 0.5
			var cy := box.get_center().y
			# Inboard of the stile edge so the pin does not fill the mullion or the finger gap.
			_hw(body, "PivotTop", Vector3(0.05, 0.03, 0.04), Vector3(hinge_x + inward * 0.04, box.position.y + box.size.y - 0.03, box.position.z + box.size.z + 0.02), _alloy)
			_hw(body, "PivotBottom", Vector3(0.05, 0.03, 0.04), Vector3(hinge_x + inward * 0.04, box.position.y + 0.04, box.position.z + box.size.z + 0.02), _alloy)
			_hw(body, "OperatorArm", Vector3(0.32, 0.02, 0.025), Vector3(hinge_x + inward * 0.22, box.position.y + box.size.y - 0.05, box.position.z - 0.02), _alloy)
			_hw(body, "PresenceBar", Vector3(minf(0.55, box.size.x * 0.55), 0.02, 0.018), Vector3(mid_x, cy, box.position.z + box.size.z + 0.012), _gun)
			_hw(body, "BrushSeal", Vector3(0.008, box.size.y * 0.90, 0.010), Vector3(meet_x - inward * 0.010, cy, box.position.z - 0.008), _seal)
		_hw(door, "ElectricStrike", Vector3(0.06, 0.08, 0.04), Vector3(0, 2.15, -0.12), _alloy)
		_hw(door, "FloorStop", Vector3(0.08, 0.02, 0.08), Vector3(0.4, 0.02, 0.7), _alloy)
		_hw(door, "Breakaway", Vector3(0.10, 0.04, 0.02), Vector3(-0.4, 1.05, -0.16), _orange)
	else:
		for item in leaves:
			var body2: Node3D = item["body"]
			var box2 := _named_local_aabb(body2, "panel")
			if box2.size == Vector3.ZERO:
				continue
			var hinge2 := _near_edge(box2)
			var meet2 := _far_edge(box2)
			var inward2 := signf(meet2 - hinge2)
			var outward2 := -inward2
			var cy2 := box2.get_center().y
			var cz2 := box2.get_center().z
			# Inner face sits 4.8 mm outboard. 5.0 mm sampled 5.01 and failed the closed band.
			var knuckle_x := hinge2 + outward2 * 0.0248
			for i in 3:
				_hw(body2, "HingeKnuckle%d" % i, Vector3(0.04, 0.10, 0.04), Vector3(knuckle_x, box2.position.y + 0.22 + float(i) * 0.95, cz2), _alloy)
			_hw(body2, "CloserArm", Vector3(0.28, 0.02, 0.03), Vector3(hinge2 + inward2 * 0.22, box2.position.y + box2.size.y - 0.08, box2.position.z - 0.03), _alloy)
			_hw(body2, "BrushSeal", Vector3(0.008, box2.size.y * 0.88, 0.008), Vector3(meet2 - inward2 * 0.008, cy2, cz2), _seal)
		_hw(door, "FloorStop", Vector3(0.06, 0.015, 0.06), Vector3(0.55, 0.02, 0.55), _alloy)


func _near_edge(box: AABB) -> float:
	var a := box.position.x
	var b := box.position.x + box.size.x
	return a if absf(a) <= absf(b) else b


func _far_edge(box: AABB) -> float:
	var a := box.position.x
	var b := box.position.x + box.size.x
	return b if absf(a) <= absf(b) else a


func _bay_guards(door: Node3D, leaves: Array) -> void:
	var stiles: Array = []
	for item in leaves:
		var body: Node3D = item["body"]
		var mi := _find_mesh_token(body, "stile")
		if mi == null:
			continue
		var wab := _mesh_world(mi)
		stiles.append({"name": str(item["name"]), "body": body, "ab": wab})
		var bottom := wab.position.y
		if bottom > 0.012:
			var sh := bottom - 0.008
			var centre := Vector3(wab.get_center().x, 0.008 + sh * 0.5, wab.get_center().z)
			_mesh(body, "FloorSweep", Vector3(wab.size.x * 0.98, sh, maxf(0.012, wab.size.z * 0.75)), body.to_local(centre), _seal, 0.0)
			_notes.append("bay3 %s floor sweep from y=%.3f down to 0.008, stile width" % [item["name"], bottom])
	var panels: Array = []
	var stack: Array[Node] = [door]
	while not stack.is_empty():
		var n: Node = stack.pop_back()
		for c in n.get_children():
			stack.append(c)
		if n is MeshInstance3D and "side_scissor" in String(n.name).to_lower():
			panels.append(_mesh_world(n as MeshInstance3D))
	for s in stiles:
		var sab: AABB = s["ab"]
		var best := 99.0
		var panel_edge := 0.0
		var stile_edge := 0.0
		for p in panels:
			var pb: AABB = p
			var gap_l := sab.position.x - (pb.position.x + pb.size.x)
			var gap_r := pb.position.x - (sab.position.x + sab.size.x)
			if gap_l > 0.02 and gap_l < best and gap_l < 0.08:
				best = gap_l
				panel_edge = pb.position.x + pb.size.x
				stile_edge = sab.position.x
			if gap_r > 0.02 and gap_r < best and gap_r < 0.08:
				best = gap_r
				panel_edge = pb.position.x
				stile_edge = sab.position.x + sab.size.x
		if best > 0.08:
			continue
		# 5 mm clear of the panel and of the stile. Plate sits on the approach face, clear of the swing arc.
		var x0 := minf(panel_edge, stile_edge) + 0.005
		var x1 := maxf(panel_edge, stile_edge) - 0.005
		var guard_centre := Vector3((x0 + x1) * 0.5, sab.get_center().y, sab.position.z - 0.012)
		_mesh(door, "FingerGuard", Vector3(x1 - x0, sab.size.y * 0.98, 0.010), door.to_local(guard_centre), _alloy, 0.002)
		_notes.append("bay3 %s finger guard %.0f mm in the %.0f mm hinge gap, 5 mm each side, approach face" % [s["name"], (x1 - x0) * 1000.0, best * 1000.0])
	_bay_mullions(door, stiles)
	_sink_mat(door)


func _bay_mullions(door: Node3D, stiles: Array) -> void:
	var edges: Array = []
	for s in stiles:
		var sab: AABB = s["ab"]
		edges.append({"x0": sab.position.x, "x1": sab.position.x + sab.size.x, "ab": sab})
	edges.sort_custom(func(a, b): return float(a["x0"]) < float(b["x0"]))
	for i in range(edges.size() - 1):
		var left: Dictionary = edges[i]
		var right: Dictionary = edges[i + 1]
		var gap := float(right["x0"]) - float(left["x1"])
		if gap < 0.09 or gap > 0.13:
			continue
		var x0 := float(left["x1"]) + 0.003
		var x1 := float(right["x0"]) - 0.003
		var ab: AABB = left["ab"]
		var y0 := 0.006
		var y1 := ab.position.y + ab.size.y
		var centre := Vector3((x0 + x1) * 0.5, (y0 + y1) * 0.5, ab.get_center().z)
		var size := Vector3(x1 - x0, y1 - y0, maxf(0.04, ab.size.z))
		_mesh(door, "Mullion", size, door.to_local(centre), _gun, 0.002)
		var post := StaticBody3D.new()
		post.name = "MullionBody"
		post.collision_layer = 1
		post.collision_mask = 1
		var cy0 := 0.14
		post.position = door.to_local(Vector3(centre.x, (cy0 + y1) * 0.5, centre.z))
		door.add_child(post)
		var cs := CollisionShape3D.new()
		var box := BoxShape3D.new()
		box.size = Vector3(size.x - 0.001, y1 - cy0, size.z * 0.8)
		cs.shape = box
		post.add_child(cs)
		_notes.append("bay3 mullion door-x %.3f..%.3f (3 mm each side of the %.0f mm stile gap); frame mesh had no post there" % [x0 - door.global_position.x, x1 - door.global_position.x, gap * 1000.0])


func _pair_sweeps(leaves: Array) -> void:
	for item in leaves:
		var body: Node3D = item["body"]
		var ab := _local_aabb(body)
		if ab.size == Vector3.ZERO:
			continue
		var bottom := ab.position.y
		if bottom > 0.014:
			var sh := bottom - 0.010
			_mesh(body, "FloorSweep", Vector3(ab.size.x * 0.96, sh, maxf(0.012, ab.size.z)), Vector3(ab.get_center().x, 0.010 + sh * 0.5, ab.get_center().z), _seal, 0.0)
			_notes.append("pair %s sweep from y=%.3f to 0.010" % [item["name"], bottom])
		else:
			_notes.append("pair %s leaf bottom y=%.3f already inside 8-12 mm" % [item["name"], bottom])


func _sink_mat(door: Node3D) -> void:
	var mat := _find_loose(door, "Threshold")
	if mat == null:
		_notes.append("bay3 threshold mat not found; sweep targets y=0.008")
		return
	var ab := _aabb_node(mat)
	var top := ab.position.y + ab.size.y
	if top > 0.004 and mat is Node3D:
		(mat as Node3D).position.y -= top - 0.004
		_notes.append("bay3 threshold mat shifted down %.3f m in the instance only so the sweep can sit at 8 mm" % (top - 0.004))
	if mat is CollisionObject3D:
		(mat as CollisionObject3D).collision_layer = 0
		(mat as CollisionObject3D).collision_mask = 0


func _find_loose(root: Node, needle: String) -> Node:
	var stack: Array[Node] = [root]
	while not stack.is_empty():
		var n: Node = stack.pop_back()
		if needle.to_lower() in String(n.name).to_lower():
			return n
		for c in n.get_children():
			stack.append(c)
	return null


func _mark_walk(door: MechDoor) -> void:
	if door.profile == null:
		return
	var door_x := door.global_position.x
	door.force_q(0.0)
	var closed: Array = []
	for item in door._leaves:
		closed.append(_xspan(_aabb_node(item["body"]), door_x))
	door.force_q(door.profile.travel)
	var opened: Array = []
	for item in door._leaves:
		opened.append(_xspan(_aabb_node(item["body"]), door_x))
	var posts := _bollard_spans(door)
	var gaps: Array = []
	if door.door_id == "hatch":
		# Clear hole is x -0.45..+0.45. The plug swings to +Z. Hardware on the body
		# (piston, dogs) must not count as blocking that hole.
		gaps.append([-0.45, 0.45])
		var cuts: Array = []
		for item in door._leaves:
			var shell := _token_world_aabb(item["body"], "shell")
			if shell.size.length() <= 0.001:
				shell = _aabb_node(item["body"])
			cuts.append(_xspan(shell, door_x))
		gaps = _subtract_many(gaps, cuts)
	elif door.profile.clear_model == "slide" or door.door_id == "pair":
		gaps = _interior_gaps(opened)
	else:
		for i in closed.size():
			gaps.append_array(_subtract_one(closed[i], opened[i]))
	gaps = _subtract_many(gaps, posts)
	var best_w := 0.0
	var best_c := 0.0
	for g in gaps:
		var w: float = float(g[1]) - float(g[0])
		var c: float = (float(g[0]) + float(g[1])) * 0.5
		if w > best_w + 0.005 or (absf(w - best_w) <= 0.005 and absf(c) < absf(best_c)):
			best_w = w
			best_c = c
	door.force_q(0.0)
	door.set_meta("walk_x", best_c)
	door.set_meta("walk_clear", best_w)
	if not posts.is_empty():
		print("[door_lab] %s bollard_spans=%d" % [door.door_id, posts.size()])


func _xspan(ab: AABB, door_x: float) -> Array:
	return [ab.position.x - door_x, ab.position.x + ab.size.x - door_x]


func _interior_gaps(spans: Array) -> Array:
	var ordered: Array = spans.duplicate()
	ordered.sort_custom(func(a, b): return float(a[0]) < float(b[0]))
	var out: Array = []
	for i in range(ordered.size() - 1):
		var a: float = float(ordered[i][1])
		var b: float = float(ordered[i + 1][0])
		if b - a > 0.05:
			out.append([a, b])
	return out


func _subtract_one(span: Array, cut: Array) -> Array:
	var a: float = float(span[0])
	var b: float = float(span[1])
	var c: float = float(cut[0])
	var d: float = float(cut[1])
	var out: Array = []
	if a < c - 0.001 and minf(b, c) - a > 0.02:
		out.append([a, minf(b, c)])
	if b > d + 0.001 and b - maxf(a, d) > 0.02:
		out.append([maxf(a, d), b])
	if c >= b or d <= a:
		if out.is_empty() and b - a > 0.02:
			out.append([a, b])
	return out


func _subtract_many(gaps: Array, cuts: Array) -> Array:
	var parts: Array = gaps.duplicate()
	for cut in cuts:
		var nxt: Array = []
		for p in parts:
			nxt.append_array(_subtract_one(p, cut))
		parts = nxt
	return parts


func _bollard_spans(door: MechDoor) -> Array:
	var inst := door.get_node_or_null("AsBuilt")
	if inst == null:
		return []
	var xs: Array = []
	var stack: Array[Node] = [inst]
	while not stack.is_empty():
		var n: Node = stack.pop_back()
		for c in n.get_children():
			stack.append(c)
		if not (n is MeshInstance3D) or "bollard" not in String(n.name).to_lower():
			continue
		var mi := n as MeshInstance3D
		if mi.mesh == null:
			continue
		var to_door := door.global_transform.affine_inverse() * mi.global_transform
		var faces := mi.mesh.get_faces()
		var step := maxi(1, int(faces.size() / 900))
		var i := 0
		while i < faces.size():
			xs.append((to_door * faces[i]).x)
			i += step
	if xs.is_empty():
		return []
	xs.sort()
	var spans: Array = []
	var a: float = float(xs[0])
	var b: float = a
	for raw in xs:
		var x: float = float(raw)
		if x - b > 0.12:
			spans.append([a - 0.02, b + 0.02])
			a = x
		b = x
	spans.append([a - 0.02, b + 0.02])
	return spans


func _token_world_aabb(root: Node, token: String) -> AABB:
	var ab := AABB()
	var any := false
	var needle := token.to_lower()
	var stack: Array[Node] = [root]
	while not stack.is_empty():
		var node: Node = stack.pop_back()
		for c in node.get_children():
			stack.append(c)
		if node is MeshInstance3D and needle in String(node.name).to_lower() and (node as MeshInstance3D).mesh != null:
			var mi := node as MeshInstance3D
			var world: AABB = mi.global_transform * mi.mesh.get_aabb()
			ab = world if not any else ab.merge(world)
			any = true
	return ab


func _aabb_node(n: Node) -> AABB:
	var ab := AABB()
	var any := false
	var stack: Array[Node] = [n]
	while not stack.is_empty():
		var node: Node = stack.pop_back()
		for c in node.get_children():
			stack.append(c)
		if node is MeshInstance3D and (node as MeshInstance3D).mesh != null:
			var mi := node as MeshInstance3D
			var world: AABB = mi.global_transform * mi.mesh.get_aabb()
			ab = world if not any else ab.merge(world)
			any = true
	return ab


func _named_local_aabb(body: Node3D, token: String) -> AABB:
	var ab := AABB()
	var any := false
	var needle := token.to_lower()
	var stack: Array[Node] = [body]
	while not stack.is_empty():
		var node: Node = stack.pop_back()
		for c in node.get_children():
			stack.append(c)
		if node is MeshInstance3D and needle in String(node.name).to_lower() and (node as MeshInstance3D).mesh != null:
			var mi := node as MeshInstance3D
			var local := body.global_transform.affine_inverse() * mi.global_transform
			var box: AABB = local * mi.mesh.get_aabb()
			ab = box if not any else ab.merge(box)
			any = true
	return ab


func _find_mesh_token(root: Node, token: String) -> MeshInstance3D:
	var needle := token.to_lower()
	var stack: Array[Node] = [root]
	while not stack.is_empty():
		var node: Node = stack.pop_back()
		for c in node.get_children():
			stack.append(c)
		if node is MeshInstance3D and needle in String(node.name).to_lower() and (node as MeshInstance3D).mesh != null:
			return node as MeshInstance3D
	return null


func _mesh_world(mi: MeshInstance3D) -> AABB:
	return mi.global_transform * mi.mesh.get_aabb()


func _local_aabb(body: Node3D) -> AABB:
	var ab := AABB()
	var any := false
	var stack: Array[Node] = [body]
	while not stack.is_empty():
		var node: Node = stack.pop_back()
		for c in node.get_children():
			stack.append(c)
		if node is MeshInstance3D and (node as MeshInstance3D).mesh != null and node != body:
			var mi := node as MeshInstance3D
			var local := body.global_transform.affine_inverse() * mi.global_transform
			var box: AABB = local * mi.mesh.get_aabb()
			ab = box if not any else ab.merge(box)
			any = true
	return ab


func _room_shell(x0: float, x1: float) -> void:
	var w := x1 - x0
	var cx := (x0 + x1) * 0.5
	var ceil := MeshInstance3D.new()
	ceil.name = "Ceiling"
	var bm := BoxMesh.new()
	bm.size = Vector3(w, 0.08, 18.0)
	ceil.mesh = bm
	ceil.position = Vector3(cx, 4.15, -2.0)
	ceil.set_surface_override_material(0, _wall_mat)
	_root.add_child(ceil)
	var deck := MeshInstance3D.new()
	deck.name = "HatchDeck"
	var dm := BoxMesh.new()
	dm.size = Vector3(3.2, 0.04, 3.2)
	deck.mesh = dm
	deck.position = Vector3(12.8, -0.02, 0.5)
	deck.set_surface_override_material(0, _floor_mat)
	_root.add_child(deck)


func _reflection_cards(xs: Dictionary) -> void:
	var mat := StandardMaterial3D.new()
	mat.resource_name = "ReflectionCard"
	# Shaded, not unshaded: an unshaded near-white card ignores emission and clips.
	mat.shading_mode = BaseMaterial3D.SHADING_MODE_PER_PIXEL
	mat.albedo_color = Color(0.45, 0.48, 0.52)
	mat.emission_enabled = true
	mat.emission = Color("#DDE6EE")
	mat.emission_energy_multiplier = 0.35
	mat.roughness = 0.85
	mat.metallic = 0.0
	var yaw := deg_to_rad(30.0)
	for id in xs.keys():
		var x: float = xs[id]
		var back := 3.55
		var mi := MeshInstance3D.new()
		mi.name = "ReflectCard_%s" % id
		var card := BoxMesh.new()
		card.size = Vector3(2.0, 4.0, 0.02)
		mi.mesh = card
		mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
		mi.position = Vector3(x + sin(yaw) * back, 2.0, -cos(yaw) * back)
		mi.set_surface_override_material(0, mat)
		_root.add_child(mi)


func _vision_lite(body: Node3D) -> void:
	var core := _named_local_aabb(body, "_core")
	if core.size == Vector3.ZERO:
		core = _local_aabb(body)
	if core.size == Vector3.ZERO:
		return
	# The GLB face is an opaque white skin and the core is graphite. Both sit in the
	# opening, so the lite never reads as glass until they are hidden. Stiles stay.
	_hide_pocket_skins(body)
	# Approach face is the min-Z side. Sit the panels in the recessed core, proud of the inset.
	var z := core.position.z - 0.004
	var x0 := core.position.x + core.size.x * 0.04
	var x1 := core.position.x + core.size.x * 0.96
	var y0 := core.position.y
	var h := core.size.y
	var w := x1 - x0
	var cx := (x0 + x1) * 0.5
	var glass_h := h * 0.34
	var gy := y0 + h - glass_h * 0.5 - h * 0.03
	var pearl_top := gy - glass_h * 0.5 + 0.012
	var lower_h := maxf(0.2, pearl_top - y0)
	_mesh(body, "PearlLower", Vector3(w, lower_h, 0.008), Vector3(cx, y0 + lower_h * 0.5, z), _pearl, 0.0)
	_mesh(body, "VisionLite", Vector3(w * 0.92, glass_h, 0.008), Vector3(cx, gy, z - 0.002), _glass, 0.0)
	var xa := _mesh(body, "VisionFritA", Vector3(w * 0.70, 0.006, 0.003), Vector3(cx, gy, z - 0.006), _alloy, 0.0)
	xa.rotation.z = deg_to_rad(58.0)
	var xb := _mesh(body, "VisionFritB", Vector3(w * 0.70, 0.006, 0.003), Vector3(cx, gy, z - 0.006), _alloy, 0.0)
	xb.rotation.z = deg_to_rad(-58.0)
	# Handle zone sits on the pearl, under the lite. Kick zone is the bottom of the leaf.
	_wear_patch(body, "WearHandle", Vector3(cx, y0 + lower_h * 0.72, z - 0.006), Vector3(0.15, 0.15, 0.003), _pearl)
	_wear_patch(body, "WearKick", Vector3(cx, y0 + 0.09, z - 0.006), Vector3(0.20, 0.14, 0.003), _pearl)


func _hide_exact(root: Node, nm: String) -> void:
	var stack: Array[Node] = [root]
	while not stack.is_empty():
		var n: Node = stack.pop_back()
		for c in n.get_children():
			stack.append(c)
		if String(n.name) == nm and n is MeshInstance3D:
			(n as MeshInstance3D).visible = false


func _neutral_frit(src: Texture2D) -> Texture2D:
	if _frit_tex != null:
		return _frit_tex
	if src == null:
		return null
	var img := src.get_image()
	if img == null or img.is_empty():
		return src
	img = img.duplicate()
	img.convert(Image.FORMAT_RGBA8)
	for y in img.get_height():
		for x in img.get_width():
			var c := img.get_pixel(x, y)
			img.set_pixel(x, y, Color(0.92, 0.93, 0.94, c.a))
	_frit_tex = ImageTexture.create_from_image(img)
	return _frit_tex


func _hide_show_meshes(root: Node) -> void:
	var stack: Array[Node] = [root]
	while not stack.is_empty():
		var n: Node = stack.pop_back()
		for c in n.get_children():
			stack.append(c)
		var low := String(n.name).to_lower()
		# Blade_Court_Stripe and Court_Line_LED sit at the scene root, so they
		# stay mid-leaf after the left leaf swings. They are the floating cyan.
		var hide := "bollard_ball" in low or "blade_ball" in low or "ball_finial" in low or "ball_bollard" in low or "blade_court" in low or "court_line_led" in low or "court_stripe" in low or "wayfinding" in low
		if not hide:
			continue
		# Hide the whole branch. The cyan line is a grandchild mesh, so hiding
		# only the direct MeshInstance children left it on the open leaf.
		if n is Node3D:
			(n as Node3D).visible = false
		if n is CollisionObject3D:
			(n as CollisionObject3D).collision_layer = 0
			(n as CollisionObject3D).collision_mask = 0


func _paint_hatch_leaf(root: Node) -> void:
	var face := _graphite.duplicate() as StandardMaterial3D
	face.metallic = 0.5
	face.roughness = 0.45
	face.albedo_texture = null
	face.albedo_color = GRAPHITE
	var stack: Array[Node] = [root]
	while not stack.is_empty():
		var n: Node = stack.pop_back()
		for c in n.get_children():
			stack.append(c)
		if not (n is MeshInstance3D):
			continue
		var low := String(n.name).to_lower()
		if "leaf_shell" in low or "leaf_panel" in low or "leaf_face" in low:
			var mi := n as MeshInstance3D
			if mi.mesh == null:
				continue
			for s in mi.mesh.get_surface_count():
				mi.set_surface_override_material(s, face)


func _readout(parent: Node3D, nm: String, pos: Vector3) -> void:
	var mat := _digit_mat()
	_mesh(parent, nm, Vector3(0.09, 0.035, 0.006), pos, mat, 0.0)
	_stamp_readouts(parent)


func _linkage_and_ribs(door: Node3D, leaf_body: Node3D) -> void:
	for i in 4:
		var y := 0.55 + float(i) * 0.32
		var side := -1.0 if i < 2 else 1.0
		var host: Node3D = leaf_body if leaf_body != null else door
		# Leaf-local bars beside the dogs. Door-local fallback keeps a frame door from dropping them.
		var pos := Vector3(-0.65 + side * 0.32, y, -0.160) if leaf_body != null else Vector3(side * 0.22, y, -0.12)
		_hw(host, "Linkage%d" % i, Vector3(0.014, 0.16, 0.012), pos, _alloy)
	if leaf_body == null:
		return
	var ab := _local_aabb(leaf_body)
	if ab.size == Vector3.ZERO:
		return
	var z := ab.position.z + ab.size.z + 0.008
	var cx := ab.get_center().x
	var y0 := ab.position.y + 0.25
	for i in 5:
		_hw(leaf_body, "Rib%d" % i, Vector3(ab.size.x * 0.72, 0.018, 0.012), Vector3(cx, y0 + float(i) * ab.size.y * 0.16, z), _gun)


func _surround_mat() -> StandardMaterial3D:
	var m := _mat("TT_Gunmetal_Surround", SURROUND, 0.5, 0.45, "", Color.WHITE)
	m.albedo_texture = null
	m.albedo_color = SURROUND
	m.metallic = 0.5
	m.roughness = 0.45
	return m


func _paint_surround(root: Node) -> void:
	var mat := _surround_mat()
	var stack: Array[Node] = [root]
	while not stack.is_empty():
		var n: Node = stack.pop_back()
		for c in n.get_children():
			stack.append(c)
		if not (n is MeshInstance3D):
			continue
		var low := String(n.name).to_lower()
		if "leaf" in low or "colonly" in low or "dog" in low or "hinge" in low or "seal" in low:
			continue
		if low == "frame" or low.begins_with("frame_") or "frame_collar" in low or "cladding" in low:
			var mi := n as MeshInstance3D
			if mi.mesh == null:
				continue
			for s in mi.mesh.get_surface_count():
				mi.set_surface_override_material(s, mat)


func _hide_colonly_meshes(root: Node) -> void:
	var stack: Array[Node] = [root]
	while not stack.is_empty():
		var n: Node = stack.pop_back()
		for c in n.get_children():
			stack.append(c)
		if n is MeshInstance3D and "colonly" in String(n.name).to_lower():
			(n as MeshInstance3D).visible = false


func _hide_named_contains(root: Node, needle: String) -> void:
	var want := needle.to_lower()
	var stack: Array[Node] = [root]
	while not stack.is_empty():
		var n: Node = stack.pop_back()
		for c in n.get_children():
			stack.append(c)
		if want in String(n.name).to_lower() and n is MeshInstance3D:
			(n as MeshInstance3D).visible = false


func _mute_grid_shadows(root: Node) -> void:
	var stack: Array[Node] = [root]
	while not stack.is_empty():
		var n: Node = stack.pop_back()
		for c in n.get_children():
			stack.append(c)
		var low := String(n.name).to_lower()
		var grid := "canopy" in low or "upper_scissor" in low or "slat" in low or "louver" in low or low.begins_with("grid")
		if grid and n is GeometryInstance3D:
			(n as GeometryInstance3D).cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF


func _wear_patch(parent: Node3D, nm: String, pos: Vector3, size: Vector3, base: StandardMaterial3D) -> void:
	var m := base.duplicate() as StandardMaterial3D
	m.resource_name = "Wear"
	m.emission_enabled = false
	var c := m.albedo_color
	var lift := 1.06
	m.albedo_color = Color(minf(c.r * lift, 0.90), minf(c.g * lift, 0.90), minf(c.b * lift, 0.90), 1.0)
	m.roughness = clampf(m.roughness - 0.15, 0.05, 1.0)
	m.metallic = minf(m.metallic, 0.95)
	_mesh(parent, nm, size, pos, m, 0.0)


func _wear_leaf(body: Node3D, id: String) -> void:
	var leaf_ab := _named_local_aabb(body, "panel")
	if leaf_ab.size == Vector3.ZERO:
		leaf_ab = _named_local_aabb(body, "scissor")
	if leaf_ab.size == Vector3.ZERO:
		leaf_ab = _local_aabb(body)
	if leaf_ab.size == Vector3.ZERO:
		return
	var z := leaf_ab.position.z - 0.003
	var bar := _named_local_aabb(body, "push")
	var raw_x := bar.get_center().x if bar.size != Vector3.ZERO else leaf_ab.get_center().x
	var cy := bar.get_center().y if bar.size != Vector3.ZERO else leaf_ab.get_center().y
	# Keep the scuff inside the leaf. A patch that crosses the meeting stile closes the pair gap.
	var cx := _inset_x(leaf_ab, raw_x, 0.075)
	var face := _override_mat(body, "scissor") if id == "bay3" else _pearl
	_wear_patch(body, "WearPush", Vector3(cx, cy, z), Vector3(0.15, 0.15, 0.004), face)
	if bar.size != Vector3.ZERO:
		var amber := _mat("PushPlateWear", AMBER_PLATE, 0.15, 0.32, "", Color.WHITE)
		amber.albedo_texture = null
		amber.albedo_color = AMBER_PLATE
		var bh := clampf(bar.size.y * 0.8, 0.012, 0.045)
		var bx := _inset_x(leaf_ab, bar.get_center().x, 0.075)
		_wear_patch(body, "WearBar", Vector3(bx, bar.get_center().y, bar.position.z - 0.002), Vector3(0.15, bh, 0.003), amber)
	var kick_y := leaf_ab.position.y + 0.08
	_wear_patch(body, "WearKick", Vector3(_inset_x(leaf_ab, cx, 0.09), kick_y, z), Vector3(0.18, 0.12, 0.004), _pearl)


func _inset_x(ab: AABB, x: float, half_w: float) -> float:
	var lo := ab.position.x + half_w + 0.006
	var hi := ab.position.x + ab.size.x - half_w - 0.006
	if hi < lo:
		return ab.get_center().x
	return clampf(x, lo, hi)


func _override_mat(body: Node3D, token: String) -> StandardMaterial3D:
	var needle := token.to_lower()
	var stack: Array[Node] = [body]
	while not stack.is_empty():
		var n: Node = stack.pop_back()
		for c in n.get_children():
			stack.append(c)
		if n is MeshInstance3D and needle in String(n.name).to_lower():
			var mi := n as MeshInstance3D
			var m := mi.get_surface_override_material(0)
			if m is StandardMaterial3D:
				return (m as StandardMaterial3D).duplicate() as StandardMaterial3D
	return _pearl


func _hide_pocket_skins(body: Node3D) -> void:
	var stack: Array[Node] = [body]
	while not stack.is_empty():
		var n: Node = stack.pop_back()
		for c in n.get_children():
			stack.append(c)
		var low := String(n.name).to_lower()
		if n is MeshInstance3D and (low.ends_with("_face") or low.ends_with("_core")):
			(n as MeshInstance3D).visible = false


func _jamb_lamp(door: Node3D) -> void:
	# Reveal depth is the approach face that already reads in the hero.
	# The gauge's X is that same surround, beside the disc so the strip is not inside it.
	var z := -0.22
	var x := 0.55
	var frame := _find(door, "frame", true)
	if frame != null:
		var ab := _aabb_node(frame)
		var origin := door.global_position
		z = ab.position.z - origin.z - 0.02
	var g := _find(door, "gauge_housing_front", false)
	if g != null:
		x = door.to_local(g.global_position).x - 0.14
	_lamp(door, Vector3(x, 1.40, z))


func _spoke_wheel(parent: Node3D, nm: String, center: Vector3, radius: float, tube_r: float, mat: Material) -> Node3D:
	var root := Node3D.new()
	root.name = nm
	root.position = center
	parent.add_child(root)
	var n := 18
	for i in n:
		var a := TAU * float(i) / float(n)
		var tangent := Vector3(-sin(a), cos(a), 0.0)
		var radial := Vector3(cos(a), sin(a), 0.0)
		var seg := MeshInstance3D.new()
		seg.name = "Rim%d" % i
		var cyl := CylinderMesh.new()
		cyl.top_radius = tube_r
		cyl.bottom_radius = tube_r
		cyl.height = radius * TAU / float(n) * 1.18
		seg.mesh = cyl
		seg.position = radial * radius
		var y_axis := tangent.normalized()
		var z_axis := Vector3(0.0, 0.0, 1.0)
		var x_axis := y_axis.cross(z_axis).normalized()
		seg.basis = Basis(x_axis, y_axis, z_axis)
		seg.set_surface_override_material(0, mat)
		root.add_child(seg)
	for k in 4:
		var a2 := TAU * float(k) / 4.0
		var spoke := MeshInstance3D.new()
		spoke.name = "Spoke%d" % k
		var sc := CylinderMesh.new()
		sc.top_radius = 0.008
		sc.bottom_radius = 0.008
		sc.height = radius - tube_r
		spoke.mesh = sc
		var dir := Vector3(cos(a2), sin(a2), 0.0)
		spoke.position = dir * (radius - tube_r) * 0.5
		var y2 := dir.normalized()
		var x2 := y2.cross(Vector3(0.0, 0.0, 1.0)).normalized()
		spoke.basis = Basis(x2, y2, Vector3(0.0, 0.0, 1.0))
		spoke.set_surface_override_material(0, mat)
		root.add_child(spoke)
	var hub := MeshInstance3D.new()
	hub.name = "Hub"
	var hc := CylinderMesh.new()
	hc.top_radius = 0.028
	hc.bottom_radius = 0.028
	hc.height = 0.022
	hub.mesh = hc
	hub.rotation.x = PI * 0.5
	hub.set_surface_override_material(0, _alloy)
	root.add_child(hub)
	return root


func _hatch_bevels(body: Node3D, face_z: float) -> void:
	var ab := _named_local_aabb(body, "leaf_shell")
	if ab.size == Vector3.ZERO:
		return
	var x0 := ab.position.x
	var x1 := x0 + ab.size.x
	var y0 := ab.position.y
	var y1 := y0 + ab.size.y
	# 3 mm thick, 14 mm deep toward the camera so the arris catches the key at hero distance.
	var z := face_z - 0.008
	var t := 0.003
	var depth := 0.014
	_mesh(body, "EdgeBevelT", Vector3(x1 - x0, t, depth), Vector3((x0 + x1) * 0.5, y1 - t, z), _alloy, 0.0)
	_mesh(body, "EdgeBevelB", Vector3(x1 - x0, t, depth), Vector3((x0 + x1) * 0.5, y0 + t, z), _alloy, 0.0)
	_mesh(body, "EdgeBevelL", Vector3(t, y1 - y0, depth), Vector3(x0 + t, (y0 + y1) * 0.5, z), _alloy, 0.0)
	_mesh(body, "EdgeBevelR", Vector3(t, y1 - y0, depth), Vector3(x1 - t, (y0 + y1) * 0.5, z), _alloy, 0.0)


func _hatch_frame_reveal(door: Node3D) -> void:
	var frame := _find(door, "frame", true)
	if frame == null:
		return
	var ab := _aabb_node(frame)
	if ab.size == Vector3.ZERO:
		return
	var origin := door.global_position
	var x0 := ab.position.x - origin.x
	var x1 := x0 + ab.size.x
	var y0 := ab.position.y - origin.y
	var y1 := y0 + ab.size.y
	# Proud of the approach face so the 15 mm strip is in the hero, not inside the collar.
	var z := ab.position.z - origin.z - 0.016
	var host: Node3D = frame
	var into := func(p: Vector3) -> Vector3:
		var world := door.global_transform * p
		return frame.global_transform.affine_inverse() * world
	_reveal(host, "Reveal_SoffitB", Vector3(maxf(0.2, x1 - x0), 0.015, 0.012), into.call(Vector3((x0 + x1) * 0.5, y1 - 0.02, z)))
	_reveal(host, "Reveal_SillB", Vector3(maxf(0.2, x1 - x0), 0.015, 0.012), into.call(Vector3((x0 + x1) * 0.5, y0 + 0.03, z)))
	_reveal(host, "Reveal_JambLB", Vector3(0.015, maxf(0.2, y1 - y0), 0.012), into.call(Vector3(x0 + 0.03, (y0 + y1) * 0.5, z)))
	_reveal(host, "Reveal_JambRB", Vector3(0.015, maxf(0.2, y1 - y0), 0.012), into.call(Vector3(x1 - 0.03, (y0 + y1) * 0.5, z)))


## Visual amber/graphite checker on the wall-hatch frame. The leaf stripe stays off.
func _hatch_hazard_frame(door: Node3D) -> void:
	# Exact "frame" misses bulkhead_frame. Skip the collar and the hinge bracket.
	var frame: Node3D = null
	for n in _each_named(door, "bulkhead_frame"):
		var node := n as Node3D
		var low := String(node.name).to_lower()
		if "collar" in low or "hinge" in low or "colonly" in low:
			continue
		if node is MeshInstance3D:
			frame = node
			break
	if frame == null:
		return
	var ab := _aabb_node(frame)
	if ab.size == Vector3.ZERO:
		return
	var origin := door.global_position
	var x0 := ab.position.x - origin.x
	var x1 := x0 + ab.size.x
	var y0 := ab.position.y - origin.y
	var y1 := y0 + ab.size.y
	var face_z := ab.position.z - origin.z - 0.024
	var haz := _orange.duplicate() as StandardMaterial3D
	haz.emission_enabled = false
	haz.albedo_color = AMBER_PLATE
	var blk := _graphite.duplicate() as StandardMaterial3D
	blk.albedo_texture = null
	blk.albedo_color = Color(0.05, 0.05, 0.05)
	blk.emission_enabled = false
	var band := 0.050
	var thick := 0.006
	_hazard_run(door, "T", x0, x1 - x0, y1 - band * 0.5, face_z, true, band, thick, haz, blk)
	_hazard_run(door, "B", x0, x1 - x0, y0 + band * 0.5, face_z, true, band, thick, haz, blk)
	_hazard_run(door, "L", y0, y1 - y0, x0 + band * 0.5, face_z, false, band, thick, haz, blk)
	_hazard_run(door, "R", y0, y1 - y0, x1 - band * 0.5, face_z, false, band, thick, haz, blk)
	# Last child, so the hardware walk hits this centre before a corner segment.
	var anchor := Node3D.new()
	anchor.name = "HazardBand"
	anchor.position = Vector3((x0 + x1) * 0.5, (y0 + y1) * 0.5, face_z)
	door.add_child(anchor)


func _hazard_run(parent: Node3D, tag: String, origin: float, length: float, cross: float, face_z: float, along_x: bool, band: float, thick: float, orange: Material, black: Material) -> void:
	var seg := 0.05
	var n := maxi(int(maxf(length, seg) / seg), 1)
	var step := length / float(n)
	for i in n:
		var mat: Material = orange if i % 2 == 0 else black
		var at := origin + (float(i) + 0.5) * step
		var pos := Vector3(at, cross, face_z) if along_x else Vector3(cross, at, face_z)
		var sz := Vector3(step, band, thick) if along_x else Vector3(band, step, thick)
		_mesh(parent, "HazardBand%s%d" % [tag, i], sz, pos, mat, 0.0)


func _floor_frame(door: Node3D) -> void:
	var mat := _surround_mat()
	var top := 0.001
	var depth := 0.05
	var yc := top - depth * 0.5
	var bar := 0.07
	# Lid is x −0.5..0.5, z 0..1. Inner clearance is 8 mm. Visual only: no extra collision.
	_mesh(door, "FloorFrameN", Vector3(1.0 + bar * 2.0, depth, bar), Vector3(0.0, yc, -0.008 - bar * 0.5), mat, 0.0)
	_mesh(door, "FloorFrameS", Vector3(1.0 + bar * 2.0, depth, bar), Vector3(0.0, yc, 1.008 + bar * 0.5), mat, 0.0)
	_mesh(door, "FloorFrameW", Vector3(bar, depth, 1.016), Vector3(-0.508 - bar * 0.5, yc, 0.50), mat, 0.0)
	_mesh(door, "FloorFrameE", Vector3(bar, depth, 1.016), Vector3(0.508 + bar * 0.5, yc, 0.50), mat, 0.0)
	var haz := _orange.duplicate() as StandardMaterial3D
	haz.emission_enabled = false
	haz.albedo_color = AMBER_PLATE
	var blk := _graphite.duplicate() as StandardMaterial3D
	blk.albedo_texture = null
	blk.albedo_color = Color(0.05, 0.05, 0.05)
	blk.emission_enabled = false
	var hy := 0.004
	var hw := 0.050
	# 50 mm band, alternating orange and black, sitting on the frame.
	_hazard_band(door, "N", Vector3(0.0, hy, -0.008 - hw * 0.5), Vector3(1.16, 0.004, hw), true, haz, blk)
	_hazard_band(door, "S", Vector3(0.0, hy, 1.008 + hw * 0.5), Vector3(1.16, 0.004, hw), true, haz, blk)
	_hazard_band(door, "W", Vector3(-0.508 - hw * 0.5, hy, 0.50), Vector3(hw, 0.004, 1.016), false, haz, blk)
	_hazard_band(door, "E", Vector3(0.508 + hw * 0.5, hy, 0.50), Vector3(hw, 0.004, 1.016), false, haz, blk)


func _hazard_band(door: Node3D, tag: String, center: Vector3, size: Vector3, along_x: bool, orange: Material, black: Material) -> void:
	var length := size.x if along_x else size.z
	var seg := 0.05
	var n := maxi(int(length / seg), 1)
	var used := float(n) * seg
	for i in n:
		var mat: Material = orange if i % 2 == 0 else black
		var shift := (float(i) + 0.5) * seg - used * 0.5
		var pos := center + (Vector3(shift, 0.0, 0.0) if along_x else Vector3(0.0, 0.0, shift))
		var sz := Vector3(seg, size.y, size.z) if along_x else Vector3(size.x, size.y, seg)
		_mesh(door, "HazardBorder%s%d" % [tag, i], sz, pos, mat, 0.0)


func _floor_hatch(prof: MechDoorProfile, x: float) -> MechDoor:
	var door := _door("floorhatch", x)
	door.hinge_axis = Vector3(1.0, 0.0, 0.0)
	# Finished floor is GLB y = 0.462. Shift down so the flange is flush, and centre the opening at z = 0.50.
	var path := "res://assets/models/door_lab/door_lab_floor_hatch.glb"
	var inst := _load_glb(door, path)
	if inst == null:
		return door
	inst.position = Vector3(0.0, -0.462, 0.50)
	var pivot := _find(inst, "hatch_leaf", false)
	if pivot == null:
		push_error("door lab pivot missing hatch_leaf")
		_dump(inst)
		return door
	var body := _rig_pivot(pivot)
	# "hatch_dog_0" (not "hatch_dog_"): the fixed hatch_dog_guides node must not slide with the dogs.
	for n in _each_named(inst, "hatch_dog_0") + _each_named(inst, "hatch_linkage_"):
		(n as Node3D).set_meta("door_hw", "dog_x")
		(n as Node3D).set_meta("throw_m", 0.025)
	var lw := _find(inst, "hatch_LockWheel", false)
	if lw != null:
		lw.set_meta("door_hw", "wheel_z")
		lw.set_meta("wheel_axis", Vector3(0, 1, 0))
	var hw := _find(inst, "hatch_OverrideOrange_Handwheel", false)
	if hw != null:
		hw.set_meta("door_hw", "wheel_z")
		hw.set_meta("wheel_axis", Vector3(0, 1, 0))
		hw.set_meta("wheel_deg", 4320.0)
	var seal := _find(inst, "hatch_InflatableSeal", false)
	if seal != null:
		seal.set_meta("door_hw", "seal_z")
		seal.set_meta("seal_axis", "y")
		seal.set_meta("inflate_scale", 1.208)
	# Rook pass C rev 2 (Vance): no gas struts. The 585 N m counterbalance is a torsion bar in the full-length hinge tube
	# (hatch_HingeTube rides on the leaf; hatch_TorsionBar, both hatch_TorsionAnchor_* clevises, hatch_HingeBearing_frame and
	# hatch_RotaryDamper are fixed on the axis, so they need no driver). Side-wall stay outside the 0.90 column, 0.5 deg tables 0..105:
	# hatch_stay_arm about local X (deg), hatch_stay_slider and hatch_stay_detent_plunger along local Z (m).
	var stay_nodes := {
		"hatch_stay_arm": ["stay_table", STAY_ARM_DEG],
		"hatch_stay_slider": ["stay_slide_table", STAY_SLIDE_M],
		"hatch_stay_detent_plunger": ["stay_slide_table", STAY_PLUNGER_M],
	}
	for nm in stay_nodes:
		var sn := _find(inst, nm, false)
		if sn == null:
			continue
		sn.set_meta("door_hw", "stay")
		sn.set_meta(str(stay_nodes[nm][0]), PackedFloat32Array(stay_nodes[nm][1]))
	_floor_walk_colliders(inst, body)
	_retint(inst)
	_dress_floor_lid(inst, body)
	_clamp_rods(body)
	# 300 × 10 mm strip lying in the camera-side frame member.
	_lamp(door, Vector3(0.0, 0.014, 1.055), true)
	_downlight(door, Vector3(0.0, 2.4, -0.6), Vector3(x, 0.1, 0.4))
	var top := OmniLight3D.new()
	top.name = "FloorHatchTop"
	top.light_energy = 0.85
	top.shadow_enabled = false
	top.omni_range = 3.2
	top.omni_attenuation = 1.0
	top.position = Vector3(0.15, 1.55, 0.85)
	door.add_child(top)
	var leaves: Array = [{
		"name": "leaf",
		"sign": -1,
		"stagger_open": 0.0,
		"stagger_close": 0.0,
		"body": body,
		"pivot": pivot,
		"rest": Vector3.ZERO,
		"axis": Vector3.ZERO,
	}]
	door.bind(prof, leaves, true)
	door.configure_sensor(Vector3(0.0, 0.45, 0.50), Vector3(0.70, 0.70, 0.70))
	door.set_approach(Vector3(0, 0, -1))
	door.set_meta("block_x", 0.0)
	door.set_meta("walk_x", 0.0)
	door.set_meta("walk_clear", 1.0)
	door.set_meta("glb", path)
	# Torque model inputs (mech_door._motion_advance reads these; its literals are the same numbers as fallbacks).
	door.set_meta("damper_open_dps", 77.8)
	door.set_meta("damper_close_dps", 33.3)
	door.set_meta("torque_model", {"weight_moment_Nm": 687.0, "torsion_bar_Nm": 585.0, "net_closing_Nm": 102.0, "actuator_max_Nm": 530.0, "inertia_kgm2": 46.7})
	_floor_frame(door)
	return door


func _floor_walk_colliders(inst: Node3D, leaf_body: AnimatableBody3D) -> void:
	# Lab walk colliders sit 0.12 m above the visual surface (FloorShape top y = 0.12, capsule bottom = body origin + 0.12).
	# The GLB colliders are true geometry, so match the convention where a capsule stands:
	#  - the well floor (hatch_well_floor-convcolonly) rises 0.12 so a capsule that drops in stands with its origin on the visual floor;
	#  - the closed lid gets a 0.12 m walk skin over the opening (lid-local, on the top face; it starts 46 mm in from the hinge edge
	#    so it stays clear of the frame ring through the 105 deg swing). Liner walls are vertical and stay where they are.
	# Found by shape, not name (the importer can rename collider bodies, e.g. the multi-box frame comes in as @StaticBody3D@n):
	# the static body whose collision top is more than 0.2 m below the finished floor. The liner walls reach the land (-0.106).
	var stack: Array[Node] = [inst]
	while not stack.is_empty():
		var n: Node = stack.pop_back()
		for c in n.get_children():
			stack.append(c)
		if not (n is StaticBody3D) or n == leaf_body:
			continue
		var top := -INF
		for ch in n.get_children():
			if ch is CollisionShape3D and (ch as CollisionShape3D).shape != null:
				var dbg := (ch as CollisionShape3D).shape.get_debug_mesh()
				if dbg != null:
					var xf := Transform3D.IDENTITY
					var k: Node = ch
					while k != inst and k is Node3D:
						xf = (k as Node3D).transform * xf
						k = k.get_parent()
					var ab: AABB = xf * dbg.get_aabb()
					top = maxf(top, ab.position.y + ab.size.y + inst.position.y)
		if top > -INF and top < -0.20:
			(n as Node3D).position.y += 0.12
			n.set_meta("walk_raise_m", 0.12)
	var skin := CollisionShape3D.new()
	skin.name = "LidWalkSkin"
	var sb := BoxShape3D.new()
	sb.size = Vector3(0.90, 0.12, 0.854)
	skin.shape = sb
	# Pivot-local (= hinge axis, GLB y 0.430 z -0.524): lid top y = +0.032; the opening spans pivot z 0.074..0.974, skin z 0.120..0.974.
	skin.position = Vector3(0.0, 0.032 + 0.06, 0.524 + (-0.404 + 0.45) * 0.5)
	leaf_body.add_child(skin)


func _owner_id(n: Node) -> String:
	var p: Node = n
	while p != null:
		if p is MechDoor:
			return (p as MechDoor).door_id
		p = p.get_parent()
	return ""


func _amber_std() -> StandardMaterial3D:
	var m := StandardMaterial3D.new()
	m.albedo_color = AMBER_PLATE
	m.albedo_texture = null
	m.metallic = 0.15
	m.roughness = 0.42
	m.emission_enabled = false
	m.emission_energy_multiplier = 0.0
	m.shading_mode = BaseMaterial3D.SHADING_MODE_PER_PIXEL
	m.vertex_color_use_as_albedo = false
	return m


func _gun_std() -> StandardMaterial3D:
	var m := _gun.duplicate() as StandardMaterial3D
	m.albedo_color = GUN
	m.albedo_texture = null
	m.metallic = 0.55
	m.roughness = 0.42
	m.emission_enabled = false
	m.shading_mode = BaseMaterial3D.SHADING_MODE_PER_PIXEL
	m.vertex_color_use_as_albedo = false
	return m


## Push bars, dog rods, and handwheels get a fresh material. A duplicated GLB
## material kept the emissive amber and the unshaded white rods.
func _retint_forced(mi: MeshInstance3D, surface: int, mesh_low: String, low: String) -> bool:
	if "push_bar" in mesh_low or "push_plate" in mesh_low or "push_bar" in low:
		mi.set_surface_override_material(surface, _amber_std())
		return true
	if ("handwheel" in mesh_low or "overrideorange" in mesh_low) and "lever" not in mesh_low:
		mi.set_surface_override_material(surface, _amber_std())
		return true
	if ("dog" in mesh_low or "linkage" in mesh_low) and "guide" not in mesh_low and "dogpivot" not in mesh_low and "dogpin" not in mesh_low:
		mi.set_surface_override_material(surface, _gun_std())
		return true
	if mesh_low == "status_light" or "status_light" in mesh_low:
		var g := StandardMaterial3D.new()
		g.albedo_color = Color(0.05, 0.35, 0.12)
		g.emission_enabled = true
		g.emission = Color(0.15, 0.85, 0.28)
		g.emission_energy_multiplier = 0.45
		g.roughness = 0.4
		g.shading_mode = BaseMaterial3D.SHADING_MODE_PER_PIXEL
		mi.set_surface_override_material(surface, g)
		return true
	return false


func _paint_status_green(root: Node) -> void:
	var stack: Array[Node] = [root]
	while not stack.is_empty():
		var n: Node = stack.pop_back()
		for c in n.get_children():
			stack.append(c)
		if n is MeshInstance3D and "status_light" in String(n.name).to_lower():
			(n as MeshInstance3D).visible = true


func _indicator_bar(leaf_body: Node3D) -> void:
	if leaf_body == null:
		return
	var mat := StandardMaterial3D.new()
	mat.resource_name = "IndicatorBar"
	mat.albedo_color = Color(0.05, 0.28, 0.10)
	mat.emission_enabled = true
	mat.emission = Color(0.2, 0.9, 0.35)
	mat.emission_energy_multiplier = 0.35
	mat.roughness = 0.45
	mat.shading_mode = BaseMaterial3D.SHADING_MODE_PER_PIXEL
	_mesh(leaf_body, "IndicatorBar", Vector3(0.16, 0.012, 0.006), Vector3(-0.78, 1.64, -0.168), mat, 0.0)


func _digit_mat() -> StandardMaterial3D:
	var mat := StandardMaterial3D.new()
	mat.resource_name = "DigitalReadout"
	mat.albedo_color = Color(0.05, 0.22, 0.10)
	mat.albedo_texture = _digit_tex()
	mat.emission_enabled = true
	mat.emission = Color(0.25, 0.85, 0.40)
	mat.emission_texture = _digit_tex()
	mat.emission_energy_multiplier = 0.70
	mat.roughness = 0.4
	mat.shading_mode = BaseMaterial3D.SHADING_MODE_PER_PIXEL
	return mat


func _digit_tex() -> Texture2D:
	if _digit_cache != null:
		return _digit_cache
	var img := Image.create(48, 16, false, Image.FORMAT_RGBA8)
	img.fill(Color(0.04, 0.28, 0.12, 1.0))
	var glyphs := {
		"1": "010010010010010",
		"0": "111101101101111",
	}
	var text := "100"
	var cursor := 4
	for i in text.length():
		var bits: String = glyphs[text.substr(i, 1)]
		for row in 5:
			for col in 3:
				if bits.substr(row * 3 + col, 1) == "1":
					var px := cursor + col * 2
					var py := 3 + row * 2
					img.set_pixel(px, py, Color(0.75, 1.0, 0.85, 1.0))
					img.set_pixel(px + 1, py, Color(0.75, 1.0, 0.85, 1.0))
					img.set_pixel(px, py + 1, Color(0.75, 1.0, 0.85, 1.0))
					img.set_pixel(px + 1, py + 1, Color(0.75, 1.0, 0.85, 1.0))
		cursor += 10
	_digit_cache = ImageTexture.create_from_image(img)
	return _digit_cache


func _stamp_readouts(root: Node) -> void:
	var mat := _digit_mat()
	var stack: Array[Node] = [root]
	while not stack.is_empty():
		var n: Node = stack.pop_back()
		for c in n.get_children():
			stack.append(c)
		if not (n is MeshInstance3D):
			continue
		if "digitalreadout" not in String(n.name).to_lower() and "readout" not in String(n.name).to_lower():
			continue
		var mi := n as MeshInstance3D
		if mi.mesh == null:
			continue
		# Box and quad readouts already span 0..1. The GLB screen's UVs collapse to one texel.
		if mi.mesh is BoxMesh or mi.mesh is QuadMesh:
			for s in mi.mesh.get_surface_count():
				mi.set_surface_override_material(s, mat)
			continue
		var ab := mi.mesh.get_aabb()
		var face := QuadMesh.new()
		face.size = Vector2(maxf(ab.size.x, 0.04), maxf(ab.size.y, 0.02))
		var quad := MeshInstance3D.new()
		quad.name = "DigitFace"
		quad.mesh = face
		quad.position = mi.position + ab.get_center() + mi.basis * Vector3(0.0, 0.0, ab.size.z * 0.5 + 0.003)
		quad.basis = mi.basis
		quad.set_surface_override_material(0, mat)
		var host := mi.get_parent()
		if host != null:
			host.add_child(quad)
		mi.visible = false


func _nudge_named_z(body: Node3D, dz: float) -> void:
	var stack: Array[Node] = [body]
	while not stack.is_empty():
		var n: Node = stack.pop_back()
		for c in n.get_children():
			stack.append(c)
		if not (n is MeshInstance3D) or n == body:
			continue
		var low := String(n.name).to_lower()
		if "pearl" in low or "vision" in low or "face" in low:
			(n as MeshInstance3D).position.z += dz
			(n as GeometryInstance3D).sorting_offset = 2.0


## Scale each pair leaf about the hinge so the meeting-stile AABB lands at 5 mm.
## Translating the whole leaf would push the hinge gap out of 3–5 mm.
func _open_pair_meeting(leaves: Array) -> void:
	if leaves.size() < 2:
		return
	var spans: Array = []
	for item in leaves:
		var ab := _aabb_node(item["body"])
		var origin := (item["body"] as Node3D).global_position
		spans.append([ab.position.x, ab.position.x + ab.size.x, origin])
	spans.sort_custom(func(a, b): return float(a[0]) < float(b[0]))
	var gap := float(spans[1][0]) - float(spans[0][1])
	var delta := (0.005 - gap) * 0.5
	if absf(delta) < 0.00015:
		return
	for item in leaves:
		var body: Node3D = item["body"]
		var local := _local_aabb(body)
		if local.size == Vector3.ZERO:
			continue
		# Scale about the hinge edge so the meeting stile moves and the hinge gap does not.
		var x_lo := local.position.x
		var x_hi := local.position.x + local.size.x
		var hinge_x := x_lo if absf(x_lo) <= absf(x_hi) else x_hi
		var far_x := x_hi if absf(x_lo) <= absf(x_hi) else x_lo
		var span := far_x - hinge_x
		if absf(span) < 0.05:
			continue
		var sign := 1.0 if far_x > hinge_x else -1.0
		var s := clampf((span - sign * delta) / span, 0.97, 1.03)
		for c in body.get_children():
			if c is Node3D:
				var node := c as Node3D
				node.position.x = hinge_x + (node.position.x - hinge_x) * s
				node.scale.x *= s


## Pull dog rods and linkages inside the leaf shell. Top rods were past the top edge.
func _clamp_rods(leaf_body: Node3D) -> void:
	if leaf_body == null:
		return
	var shell := _named_local_aabb(leaf_body, "leaf_shell")
	if shell.size == Vector3.ZERO:
		shell = _named_local_aabb(leaf_body, "shell")
	if shell.size == Vector3.ZERO:
		return
	var margin := 0.004
	var lo := shell.position + Vector3(margin, margin, margin)
	var hi := shell.position + shell.size - Vector3(margin, margin, margin)
	var center := shell.get_center()
	var stack: Array[Node] = [leaf_body]
	while not stack.is_empty():
		var n: Node = stack.pop_back()
		for c in n.get_children():
			stack.append(c)
		if not (n is MeshInstance3D) or n == leaf_body:
			continue
		var low := String(n.name).to_lower()
		if "guide" in low or "dogpivot" in low or "dogpin" in low:
			continue
		if "dog" not in low and "linkage" not in low:
			continue
		var mi := n as MeshInstance3D
		if mi.mesh == null:
			continue
		var box: AABB = leaf_body.global_transform.affine_inverse() * (mi.global_transform * mi.mesh.get_aabb())
		var factor := 1.0
		var corners: Array[Vector3] = [
			box.position,
			box.position + Vector3(box.size.x, 0, 0),
			box.position + Vector3(0, box.size.y, 0),
			box.position + Vector3(0, 0, box.size.z),
			box.position + Vector3(box.size.x, box.size.y, 0),
			box.position + Vector3(box.size.x, 0, box.size.z),
			box.position + Vector3(0, box.size.y, box.size.z),
			box.position + box.size,
		]
		for corner in corners:
			var v: Vector3 = corner - center
			if absf(v.x) > 1.0e-5:
				var limx := (hi.x - center.x) if v.x > 0.0 else (center.x - lo.x)
				factor = minf(factor, limx / absf(v.x))
			if absf(v.y) > 1.0e-5:
				var limy := (hi.y - center.y) if v.y > 0.0 else (center.y - lo.y)
				factor = minf(factor, limy / absf(v.y))
			if absf(v.z) > 1.0e-5:
				var limz := (hi.z - center.z) if v.z > 0.0 else (center.z - lo.z)
				factor = minf(factor, limz / absf(v.z))
		if factor >= 0.999:
			continue
		factor = maxf(factor, 0.25)
		var local_origin := leaf_body.global_transform.affine_inverse() * mi.global_position
		var new_local := center + (local_origin - center) * factor
		mi.global_position = leaf_body.global_transform * new_local
		mi.scale *= factor


func _diamond_normal() -> Texture2D:
	if _diamond_cache != null:
		return _diamond_cache
	var n := 64
	var img := Image.create(n, n, false, Image.FORMAT_RGBA8)
	var period := 16
	var heights: Array = []
	heights.resize(n * n)
	for y in n:
		for x in n:
			var dx := absf(float(x % period) - float(period) * 0.5) / (float(period) * 0.5)
			var dy := absf(float(y % period) - float(period) * 0.5) / (float(period) * 0.5)
			heights[y * n + x] = 1.0 - maxf(dx, dy)
	for y2 in n:
		for x2 in n:
			var hL: float = heights[y2 * n + ((x2 - 1 + n) % n)]
			var hR: float = heights[y2 * n + ((x2 + 1) % n)]
			var hD: float = heights[((y2 - 1 + n) % n) * n + x2]
			var hU: float = heights[((y2 + 1) % n) * n + x2]
			var nv := Vector3(hL - hR, hD - hU, 0.55).normalized()
			img.set_pixel(x2, y2, Color(nv.x * 0.5 + 0.5, nv.y * 0.5 + 0.5, nv.z * 0.5 + 0.5, 1.0))
	img.generate_mipmaps()
	_diamond_cache = ImageTexture.create_from_image(img)
	return _diamond_cache


func _lid_graphite() -> StandardMaterial3D:
	var m := StandardMaterial3D.new()
	m.resource_name = "FloorLidGraphite"
	# Lab graphite, not a light grey. The lighter albedo clipped to white under the deck lights.
	m.albedo_color = GRAPHITE
	m.metallic = 0.5
	m.roughness = 0.45
	m.metallic_specular = 0.18
	m.emission_enabled = false
	m.emission_energy_multiplier = 0.0
	m.normal_enabled = true
	m.normal_texture = _diamond_normal()
	m.normal_scale = 0.18
	m.texture_filter = BaseMaterial3D.TEXTURE_FILTER_LINEAR_WITH_MIPMAPS_ANISOTROPIC
	m.shading_mode = BaseMaterial3D.SHADING_MODE_PER_PIXEL
	m.vertex_color_use_as_albedo = false
	# Broad tread. 0.75 still broke into grazing specular waves on the hero.
	m.uv1_scale = Vector3(0.22, 0.22, 0.22)
	return m


func _dress_floor_lid(inst: Node3D, leaf_body: Node3D) -> void:
	var lid := _lid_graphite()
	var stack: Array[Node] = [inst]
	while not stack.is_empty():
		var n: Node = stack.pop_back()
		for c in n.get_children():
			stack.append(c)
		if not (n is MeshInstance3D):
			continue
		var mi := n as MeshInstance3D
		var low := String(mi.name).to_lower()
		if "colonly" in low or "dog" in low or "linkage" in low or "hinge" in low or "torsion" in low or "damper" in low or "stay" in low or "seal" in low or "wheel" in low or "hand" in low:
			continue
		if "shell" in low or "leaf" in low or "lid" in low or "tread" in low or "plate" in low or "disc" in low or "rect" in low:
			if mi.mesh == null:
				continue
			for s in mi.mesh.get_surface_count():
				mi.set_surface_override_material(s, lid)
		elif mi.mesh != null:
			for s2 in mi.mesh.get_surface_count():
				var mat := mi.get_active_material(s2)
				if mat is StandardMaterial3D:
					var sm := (mat as StandardMaterial3D).duplicate() as StandardMaterial3D
					sm.albedo_color = Color(minf(sm.albedo_color.r, 1.0), minf(sm.albedo_color.g, 1.0), minf(sm.albedo_color.b, 1.0), sm.albedo_color.a)
					if sm.emission_enabled and sm.emission.r > 0.8 and sm.emission.g > 0.8 and sm.emission.b > 0.8:
						sm.emission_enabled = false
						sm.emission_energy_multiplier = 0.0
					mi.set_surface_override_material(s2, sm)
	var handle := _find(inst, "hatch_Handle", false)
	if handle != null:
		handle.scale *= 2.0
	var gasket := StandardMaterial3D.new()
	gasket.albedo_color = Color(0.05, 0.05, 0.05)
	gasket.roughness = 0.9
	gasket.metallic = 0.0
	gasket.emission_enabled = false
	_mesh(leaf_body, "GasketLine", Vector3(0.96, 0.004, 0.90), Vector3(0.0, 0.028, 0.50), gasket, 0.0)
	var lamp_mat := _amber_std()
	lamp_mat.emission_enabled = true
	lamp_mat.emission = AMBER_PLATE
	lamp_mat.emission_energy_multiplier = 0.4
	_mesh(leaf_body, "CornerLampNE", Vector3(0.04, 0.008, 0.04), Vector3(0.42, 0.03, 0.88), lamp_mat, 0.0)
	_mesh(leaf_body, "CornerLampSW", Vector3(0.04, 0.008, 0.04), Vector3(-0.42, 0.03, 0.12), lamp_mat, 0.0)
