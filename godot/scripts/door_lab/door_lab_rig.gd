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

const TEX_WHITE := "res://assets/textures/facade_aerospace_white_cladding.png"
const TEX_GUN := "res://assets/textures/facade_titanium_gunmetal_hull.png"
const TEX_STEEL := "res://assets/textures/facade_brushed_steel_gantry.png"
const TEX_SLATE := "res://assets/models/char_bot_r2_05_livery_01_sprocket_facade_carbon_slate_spandrel.png"
const TEX_CYAN := "res://assets/textures/led_cyan_strip.png"

var _root: Node3D
var _pearl: StandardMaterial3D
var _graphite: StandardMaterial3D
var _gun: StandardMaterial3D
var _alloy: StandardMaterial3D
var _seal: StandardMaterial3D
var _orange: StandardMaterial3D
var _floor_mat: StandardMaterial3D
var _notes: Array = []


static func build(parent: Node3D) -> Dictionary:
	var rig := DoorLabRig.new()
	return rig._build(parent)


func _build(parent: Node3D) -> Dictionary:
	_root = parent
	_make_materials()
	var profs := {}
	var max_r := 0.0
	for id in ["pocket", "bay3", "pair", "hatch"]:
		var prof := load("res://resources/door_lab/%s.tres" % id) as MechDoorProfile
		prof.load_table()
		profs[id] = prof
		max_r = maxf(max_r, prof.trigger_radius(5.2))
	var spacing := maxf(28.0, 2.0 * max_r + 6.0)
	var xs := {
		"pocket": -1.5 * spacing,
		"bay3": -0.5 * spacing,
		"pair": 0.5 * spacing,
		"hatch": 1.5 * spacing,
	}
	var depth := maxf(80.0, max_r + 40.0)
	_environment(xs["hatch"] - xs["pocket"], depth)
	_floor(xs["pocket"] - 20.0, xs["hatch"] + 20.0, depth)
	var doors := {}
	doors["pocket"] = _pocket(profs["pocket"], xs["pocket"])
	doors["bay3"] = _glb_door(profs["bay3"], xs["bay3"], "res://assets/models/tt_entrance_bay_3l.glb", ["Leaf_0", "Leaf_1", "Leaf_2"], true)
	doors["pair"] = _glb_door(profs["pair"], xs["pair"], "res://assets/models/tt_door_pair_18.glb", ["Leaf_L", "Leaf_R"], true)
	doors["hatch"] = _hatch(profs["hatch"], xs["hatch"])
	_wings_for(doors)
	# Open shots look through the leaf into the clear color. A lit return gives
	# that cell a real surface. Visual only: the snag walk must still pass.
	_vestibules(doors)
	var player := _player(xs["pocket"], -(max_r + 6.0))
	_lights(xs, depth)
	print("[door_lab] spacing=%.2f max_trigger=%.2f" % [spacing, max_r])
	for id in ["pocket", "bay3", "pair", "hatch"]:
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
		},
		"notes": _notes,
		"player": player,
		"doors": doors,
	}


func _make_materials() -> void:
	_pearl = _mat("TT_WhiteComposite_Lab", PEARL, 0.05, 0.48, TEX_WHITE, Color(0.93, 0.93, 0.93))
	_graphite = _mat("TT_CarbonSlate_Lab", GRAPHITE, 0.35, 0.62, "", Color.WHITE)
	_gun = _mat("TT_Gunmetal_Lab", GUN, 0.72, 0.50, TEX_GUN, Color(0.85, 0.85, 0.85))
	_alloy = _mat("TT_BrushedAlloy_Lab", ALLOY, 0.95, 0.35, TEX_STEEL, Color(0.80, 0.80, 0.80))
	_seal = _mat("TT_Seal_Lab", SEAL_C, 0.0, 0.85, "", Color.WHITE)
	_orange = _mat("Mat_Hub_OverrideOrange", ORANGE, 0.1, 0.45, "", Color.WHITE)
	_floor_mat = _mat("TT_CarbonSlate_Floor", Color(0.16, 0.17, 0.19), 0.15, 0.60, TEX_SLATE, Color(0.55, 0.55, 0.55))


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
	env.ambient_light_color = Color("#1A1E24")
	env.ambient_light_energy = 0.15
	env.tonemap_mode = Environment.TONE_MAPPER_FILMIC
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
	probe.ambient_color = Color("#1A1E24")
	# Godot #98382: on Windows the compatibility renderer adds a green light to
	# every mesh inside a ReflectionProbe. Keep the probe (Sloane §5) but do not
	# apply that cubemap. Metals fall back to the slate background reflection.
	if OS.get_name() == "Windows":
		probe.intensity = 0.0
		probe.ambient_mode = ReflectionProbe.AMBIENT_DISABLED
	_root.add_child(probe)


func _floor(x0: float, x1: float, depth: float) -> void:
	var w := x1 - x0
	var cx := (x0 + x1) * 0.5
	var vis := MeshInstance3D.new()
	vis.name = "FloorVisual"
	var bm := BoxMesh.new()
	bm.size = Vector3(w, 0.02, depth * 2.0)
	vis.mesh = bm
	vis.position = Vector3(cx, -0.01, 0.0)
	vis.set_surface_override_material(0, _floor_mat)
	_root.add_child(vis)
	var body := StaticBody3D.new()
	body.name = "FloorBody"
	body.collision_layer = 1
	body.collision_mask = 1
	_root.add_child(body)
	var cs := CollisionShape3D.new()
	cs.name = "FloorShape"
	var box := BoxShape3D.new()
	box.size = Vector3(w, 0.24, depth * 2.0)
	cs.shape = box
	# Top of the collision is y = 0.12. Body origin of a standing player rests at y = 0.
	cs.position = Vector3(cx, 0.0, 0.0)
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
			_static_box("Wing_Start", Vector3(8.0, 4.0, 0.16), Vector3(x0 - 4.0, 2.0, -0.02), _gun)
			first = false
		else:
			var gap := x0 - prev
			if gap > 0.05:
				_static_box("Wing_%s" % id, Vector3(gap, 4.0, 0.16), Vector3((prev + x0) * 0.5, 2.0, -0.02), _gun)
		prev = x1
	_static_box("Wing_End", Vector3(8.0, 4.0, 0.16), Vector3(prev + 4.0, 2.0, -0.02), _gun)


func _lights(xs: Dictionary, _depth: float) -> void:
	var key := DirectionalLight3D.new()
	key.name = "KeyLight"
	key.light_energy = 0.5
	key.shadow_enabled = true
	_root.add_child(key)
	# Approach faces look toward -Z. Pitch −35° and yaw 30° off that normal:
	# the key comes from the camera side. Euler (−35, 30, 0) aims at world −Z
	# and leaves the leaf faces in shadow.
	var yaw := deg_to_rad(30.0)
	var pitch := deg_to_rad(35.0)
	var travel := Vector3(sin(yaw) * cos(pitch), -sin(pitch), cos(yaw) * cos(pitch))
	key.look_at(key.global_position + travel, Vector3.UP)
	for id in xs.keys():
		var x: float = xs[id]
		# One fill on the approach side of each door. Energy stays at Sloane's 0.2.
		# Closer than the first rig: at z=-2.2 the hatch plug was still near black.
		var fill := OmniLight3D.new()
		fill.name = "Fill_%s" % id
		fill.light_energy = 0.2
		fill.shadow_enabled = false
		fill.omni_range = 8.0
		fill.position = Vector3(x, 1.95, -1.7)
		_root.add_child(fill)
		var rim := SpotLight3D.new()
		rim.name = "Rim_%s" % id
		rim.light_energy = 0.4
		rim.light_color = RIM_C
		rim.spot_angle = 28.0
		rim.shadow_enabled = false
		rim.position = Vector3(x, 1.6, 2.4)
		_root.add_child(rim)
		rim.look_at(Vector3(x, 1.2, 0.0), Vector3.UP)
		# Pair is already near white under the key. A wash there only clips it.
		if id != "pair":
			var wash := SpotLight3D.new()
			wash.name = "ApproachWash_%s" % id
			wash.light_color = Color(1.0, 0.96, 0.92)
			wash.shadow_enabled = false
			wash.spot_range = 5.0
			# The plug is dark metal. The same key that lifts a white stile to 0.34
			# leaves this face near 0.04, so the hatch wash has to be the stronger one.
			if id == "hatch":
				# Frontal cone covers the plug. A second spot sits on the mirror line of
				# the hero camera (+X), so that 3/4 view gets a broad highlight too.
				wash.light_energy = 4.0
				wash.spot_angle = 68.0
				wash.spot_range = 6.5
				wash.position = Vector3(x, 1.25, -2.35)
			else:
				wash.light_energy = 0.9
				wash.spot_angle = 48.0
				wash.position = Vector3(x, 1.7, -2.1)
			_root.add_child(wash)
			wash.look_at(Vector3(x, 1.10, 0.02), Vector3.UP)
			if id == "hatch":
				var side := SpotLight3D.new()
				side.name = "ApproachWash_hatch_side"
				side.light_energy = 4.5
				side.light_color = Color(1.0, 0.96, 0.92)
				side.shadow_enabled = false
				side.spot_angle = 58.0
				side.spot_range = 6.0
				side.position = Vector3(x - 1.05, 1.15, -2.05)
				_root.add_child(side)
				side.look_at(Vector3(x, 1.05, 0.02), Vector3.UP)


func _vestibules(doors: Dictionary) -> void:
	var mat := _pearl.duplicate() as StandardMaterial3D
	mat.resource_name = "VestibuleReturn"
	mat.albedo_color = Color(0.72, 0.74, 0.76)
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
		var mi := MeshInstance3D.new()
		mi.name = "Vestibule_%s" % id
		var bm := BoxMesh.new()
		bm.size = Vector3(width, height, 0.05)
		mi.mesh = bm
		mi.position = Vector3(cx, height * 0.5 + 0.02, z)
		mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
		mi.set_surface_override_material(0, mat)
		_root.add_child(mi)
		var lamp := OmniLight3D.new()
		lamp.name = "VestibuleLight_%s" % id
		lamp.light_energy = 1.4
		lamp.light_color = WARM
		lamp.shadow_enabled = false
		lamp.omni_range = 5.5
		# Between the open leaf and the return, so the approach face stays on the key.
		lamp.position = Vector3(cx, 1.7, 2.15)
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
	var sph := SphereShape3D.new()
	sph.radius = door.trigger_radius
	cs.shape = sph
	area.add_child(cs)
	door.add_child(area)
	door.attach_proximity(area)


func _lamp(door: MechDoor, pos: Vector3) -> void:
	var root := Node3D.new()
	root.name = "StatusLamp"
	root.position = pos
	door.add_child(root)
	var base := StandardMaterial3D.new()
	base.resource_name = "Mat_Hub_StateGlow"
	base.emission_enabled = true
	base.emission = Color("#FF9500")
	base.emission_energy_multiplier = 0.6
	base.albedo_color = Color(0.90, 0.52, 0.0)
	base.roughness = 0.3
	base.metallic = 0.0
	var bar := MeshInstance3D.new()
	bar.name = "LampBar"
	var bm := BoxMesh.new()
	bm.size = Vector3(0.16, 0.012, 0.008)
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
		sm.size = Vector3(0.016, 0.008, 0.006)
		mi.mesh = sm
		mi.position = Vector3((float(i) - 3.5) * 0.020, 0.0, -0.005)
		var seg := base.duplicate() as StandardMaterial3D
		mi.set_surface_override_material(0, seg)
		root.add_child(mi)
		segs.append(mi)
	door.attach_lamp(base, light, segs)


func _downlight(parent: Node3D, pos: Vector3, look: Vector3) -> void:
	var s := SpotLight3D.new()
	s.name = "Downlight"
	s.light_energy = 0.6
	s.light_color = WARM
	s.spot_angle = 35.0
	s.shadow_enabled = true
	s.position = pos
	parent.add_child(s)
	s.look_at(look, Vector3.UP)


func _reveal(parent: Node3D, name: String, size: Vector3, pos: Vector3) -> void:
	var m := StandardMaterial3D.new()
	m.resource_name = "TT_CyanLED"
	# Emission stays full cyan. Albedo stays under the 0.90 cap even if the strip texture is white.
	m.albedo_color = Color(0.0, 0.80, 0.85)
	m.emission_enabled = true
	m.emission = CYAN
	m.emission_energy_multiplier = 0.5
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
	var seam := _graphite.duplicate() as StandardMaterial3D
	seam.roughness = minf(0.92, _graphite.roughness + 0.08)
	var z := -size.z * 0.5 - 0.004
	var x := -size.x * 0.5 + 0.55
	var i := 0
	while x < size.x * 0.5 - 0.15:
		var mi := MeshInstance3D.new()
		mi.name = "PanelSeam%d" % i
		var bm := BoxMesh.new()
		bm.size = Vector3(0.008, size.y * 0.90, 0.006)
		mi.mesh = bm
		mi.position = Vector3(x, 0.0, z)
		mi.set_surface_override_material(0, seam)
		body.add_child(mi)
		x += 1.15
		i += 1
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
	var zf := ab.position.z - origin.z
	_reveal(door, "Reveal_Soffit", Vector3(maxf(0.2, x1 - x0), 0.010, 0.010), Vector3((x0 + x1) * 0.5, y1 + 0.014, zf))
	_reveal(door, "Reveal_JambL", Vector3(0.010, maxf(0.2, y1 - y0), 0.010), Vector3(x0 - 0.018, (y0 + y1) * 0.5, zf))
	_reveal(door, "Reveal_JambR", Vector3(0.010, maxf(0.2, y1 - y0), 0.010), Vector3(x1 + 0.018, (y0 + y1) * 0.5, zf))


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
	_retint(inst)
	_pocket_tokens(door, inst)
	_skirt(door)
	_lamp(door, Vector3(-0.85, 2.46, -0.09))
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
	_alias(host, "HeadBox", Vector3(0.0, 2.55, -0.06))
	_hw(door, "AccessPanel", Vector3(0.22, 0.06, 0.006), Vector3(0.0, 2.50, -0.090), _alloy)
	_alias(door, "Motor", Vector3(0.0, 2.58, -0.04))
	_alias(door, "TensionerL", Vector3(-1.99, 2.50, -0.02))
	_alias(door, "TensionerR", Vector3(1.99, 2.50, -0.02))
	_alias(door, "BumperL", Vector3(-2.05, 1.20, 0.0))
	_alias(door, "BumperR", Vector3(2.05, 1.20, 0.0))
	_hw(door, "Solenoid", Vector3(0.06, 0.028, 0.022), Vector3(-0.05, 2.38, -0.092), _alloy)
	_hw(door, "Keeper", Vector3(0.028, 0.022, 0.016), Vector3(0.04, 2.38, -0.092), _alloy)
	_hw(door, "Radar", Vector3(0.10, 0.032, 0.036), Vector3(0.0, 2.18, -0.14), _gun)
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
	_hatch_tokens(door, inst)
	_seat_reveals(door, [{"body": body}])
	_skirt(door)
	_lamp(door, Vector3(0.0, 2.52, -0.20))
	_downlight(door, Vector3(0, 2.90, -0.55), Vector3(x, 1.2, -0.1))
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
	for n in _each_named(inst, "latch_bolt"):
		var bolt := n as Node3D
		bolt.set_meta("door_hw", "dog_x")
		bolt.set_meta("throw_m", 0.025)
	var wheel := _find(inst, "dog_handwheel", false)
	if wheel != null:
		wheel.set_meta("door_hw", "wheel_z")
		_alias(wheel, "LockWheel", Vector3.ZERO)
	var seal := _find(inst, "seal", false)
	if seal != null:
		seal.set_meta("door_hw", "seal_z")
		_alias(seal, "InflatableSeal", Vector3.ZERO)
	for n2 in _each_named(inst, "gauge_needle"):
		(n2 as Node3D).set_meta("door_hw", "needle_z")
	var rod := _find(inst, "piston_rod", false)
	var cyl := _find(inst, "piston_body", false)
	if rod != null and cyl != null:
		rod.set_meta("door_hw", "piston")
		cyl.set_meta("door_hw", "piston")
		rod.set_meta("piston_partner", cyl)
		cyl.set_meta("piston_partner", rod)
		_alias(rod, "DamperRod", Vector3.ZERO)


func _hatch_tokens(door: Node3D, inst: Node3D) -> void:
	var hinge := _find(inst, "hinge_frame", false)
	if hinge != null:
		_alias(hinge, "HingeHeavy", Vector3(0.62, 0.55, -0.02))
		_alias(hinge, "Actuator", Vector3(0.62, 0.32, -0.04))
	var rams := _find(inst, "pushoff_rams", false)
	if rams != null:
		_alias(rams, "PushOffRam", Vector3(-0.50, 0.85, -0.02))
	_hw(door, "Davit", Vector3(0.028, 0.028, 0.36), Vector3(-0.10, 2.40, -0.18), _alloy)
	_hw(door, "EqualizePort", Vector3(0.07, 0.05, 0.010), Vector3(-0.62, 1.62, -0.18), _alloy)
	_hw(door, "HoldOpenCatch", Vector3(0.045, 0.028, 0.030), Vector3(0.28, 0.38, -0.18), _alloy)
	_hw(door, "EqualizeLever", Vector3(0.018, 0.12, 0.016), Vector3(-0.62, 1.02, -0.19), _orange)
	var band := _mesh(door, "HazardBand", Vector3(0.62, 0.040, 0.006), Vector3(0.0, 0.24, -0.18), _orange, 0.0)
	var band_mat := band.get_surface_override_material(0)
	if band_mat is StandardMaterial3D:
		var dup := (band_mat as StandardMaterial3D).duplicate() as StandardMaterial3D
		dup.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
		dup.albedo_color.a = 0.9
		band.set_surface_override_material(0, dup)


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
	_rename_glass(inst)
	_bay_pair_hw(door, inst, prof.door_id, leaves)
	_seat_reveals(door, leaves)
	var leaf_ab := _aabb_node(leaves[0]["body"])
	for item in leaves:
		leaf_ab = leaf_ab.merge(_aabb_node(item["body"]))
	var face_z := leaf_ab.position.z - door.global_position.z
	var top_y := leaf_ab.position.y + leaf_ab.size.y
	_lamp(door, Vector3(leaf_ab.get_center().x - door.global_position.x, top_y + 0.04, face_z - 0.012))
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
	return body


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
				if not (mat is BaseMaterial3D):
					continue
				var dup := (mat as BaseMaterial3D).duplicate() as BaseMaterial3D
				var low := label.to_lower()
				if "whitecomposite" in low or "white_composite" in low or "pearl" in low:
					# Blue stays at 0.900. #D8DEE6's 0.902 is only legal on the WhiteComposite name.
					dup.albedo_color = Color(0.847, 0.871, 0.900, dup.albedo_color.a)
					dup.albedo_texture = null
					dup.metallic = 0.1
					dup.roughness = 0.48
				elif "glass" in low:
					dup.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA_SCISSOR
					dup.albedo_color = Color(0.70, 0.84, 0.89)
					dup.roughness = 0.08
					dup.metallic = 0.0
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
			# Inner face of the knuckle sits 5 mm outboard of the panel edge (Vance 3–5 mm).
			var knuckle_x := hinge2 + outward2 * 0.025
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
