class_name DoorLabRig
extends RefCounted
## Isolated mechanical-door lab. Procedural pocket and hatch. bay3 and pair
## instance the existing GLBs and do not modify those files.

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
	_wings(xs, spacing)
	var doors := {}
	doors["pocket"] = _pocket(profs["pocket"], xs["pocket"])
	doors["bay3"] = _glb_door(profs["bay3"], xs["bay3"], "res://assets/models/tt_entrance_bay_3l.glb", ["Leaf_0", "Leaf_1", "Leaf_2"], true)
	doors["pair"] = _glb_door(profs["pair"], xs["pair"], "res://assets/models/tt_door_pair_18.glb", ["Leaf_L", "Leaf_R"], true)
	doors["hatch"] = _hatch(profs["hatch"], xs["hatch"])
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


func _wings(xs: Dictionary, spacing: float) -> void:
	var ids := ["pocket", "bay3", "pair", "hatch"]
	var half := {"pocket": 2.45, "bay3": 2.7, "pair": 1.4, "hatch": 1.3}
	var prev: float = float(xs["pocket"]) - float(half["pocket"]) - 8.0
	for id in ids:
		var x: float = float(xs[id])
		var hx: float = float(half[id])
		_static_box("Wing_%s" % id, Vector3(x - hx - prev, 4.0, 0.16), Vector3((prev + x - hx) * 0.5, 2.0, -0.02), _gun)
		prev = x + hx
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
	var fill := OmniLight3D.new()
	fill.name = "FillLight"
	fill.light_energy = 0.2
	fill.shadow_enabled = false
	fill.position = Vector3(0.0, 3.4, -8.0)
	# Outer doors sit ~42 m off the origin. Energy stays 0.2; the range has to reach them.
	fill.omni_range = 120.0
	_root.add_child(fill)
	for id in xs.keys():
		var x: float = xs[id]
		var rim := SpotLight3D.new()
		rim.name = "Rim_%s" % id
		rim.light_energy = 0.4
		rim.light_color = RIM_C
		rim.spot_angle = 28.0
		rim.shadow_enabled = false
		rim.position = Vector3(x, 1.6, 2.4)
		_root.add_child(rim)
		rim.look_at(Vector3(x, 1.2, 0.0), Vector3.UP)


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
	bm.size = Vector3(0.72, 0.018, 0.012)
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
		sm.size = Vector3(0.07, 0.012, 0.010)
		mi.mesh = sm
		mi.position = Vector3((float(i) - 3.5) * 0.082, 0.0, -0.008)
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


func _pocket(prof: MechDoorProfile, x: float) -> MechDoor:
	var door := _door("pocket", x)
	var y := 1.204
	var size := Vector3(1.05, 2.392, 0.05)
	var leaves: Array = []
	for side in [["leaf_L", -1, -0.528], ["leaf_R", 1, 0.528]]:
		var spec := _spec(prof, str(side[0]))
		var pivot := Node3D.new()
		pivot.name = str(side[0]) + "Pivot"
		door.add_child(pivot)
		var body := _new_body(pivot)
		_mesh(body, "LeafFace", size, Vector3.ZERO, _pearl, 0.003)
		_mesh(body, "Inset", Vector3(0.86, 1.7, 0.008), Vector3(0, 0.05, -0.031), _graphite, 0.0)
		var edge := 0.525 if int(side[1]) < 0 else -0.525
		var stile_x := edge - 0.006 * signf(edge)
		_mesh(body, "MeetingStile", Vector3(0.012, 2.30, 0.012), Vector3(stile_x, 0, -0.02), _alloy, 0.002)
		var seal_x := 0.5265 if int(side[1]) < 0 else -0.5265
		_mesh(body, "BulbSeal", Vector3(0.003, 2.28, 0.008), Vector3(seal_x, 0, 0), _seal, 0.0)
		# Kick and handle wear: roughness down, albedo up a few percent. Not grime.
		var wear := _pearl.duplicate() as StandardMaterial3D
		wear.roughness = maxf(0.05, _pearl.roughness - 0.12)
		wear.albedo_color = Color(minf(0.90, PEARL.r * 1.04), minf(0.90, PEARL.g * 1.04), minf(0.902, PEARL.b * 1.03))
		_mesh(body, "KickWear", Vector3(0.70, 0.12, 0.004), Vector3(0, -1.10, -0.029), wear, 0.0)
		_mesh(body, "HandleWear", Vector3(0.16, 0.22, 0.004), Vector3(edge * 0.7, -0.1, -0.029), wear, 0.0)
		_body_shape(body, size)
		_pocket_leaf_hw(body, int(side[1]))
		leaves.append({
			"name": str(side[0]),
			"sign": int(side[1]),
			"stagger_open": float(spec.get("stagger_open", 0.0)),
			"stagger_close": float(spec.get("stagger_close", 0.0)),
			"body": body,
			"pivot": body,
			"rest": Vector3(float(side[2]), y, 0.0),
			"axis": Vector3(1, 0, 0),
		})
	_pocket_frame(door)
	_lamp(door, Vector3(-1.15, 1.4, -0.08))
	_reveal(door, "Reveal_Soffit", Vector3(1.90, 0.010, 0.010), Vector3(0, 2.395, -0.08))
	_reveal(door, "Reveal_JambL", Vector3(0.010, 2.20, 0.010), Vector3(-1.02, 1.15, -0.08))
	_reveal(door, "Reveal_JambR", Vector3(0.010, 2.20, 0.010), Vector3(1.02, 1.15, -0.08))
	_downlight(door, Vector3(0, 2.7, -0.4), Vector3(x, 1.3, 0))
	door.bind(prof, leaves, false)
	door.configure_sensor(Vector3(0, 1.15, 0), Vector3(1.85, 2.15, 0.50))
	door.set_approach(Vector3(0, 0, -1))
	_proximity(door)
	_mark_walk(door)
	door.set_meta("block_x", 0.0)
	return door


func _pocket_leaf_hw(body: Node3D, sign: int) -> void:
	var inward := 0.42 * sign
	for i in 2:
		var zc := -0.2 + float(i) * 0.45
		var car := _hw(body, "Carriage%d" % i, Vector3(0.12, 0.04, 0.06), Vector3(inward, 1.16, zc), _alloy)
		for r in 2:
			var roller := _mesh(car, "Roller%d" % r, Vector3(0.06, 0.06, 0.02), Vector3(-0.03 + float(r) * 0.06, 0.04, 0), _alloy, 0.0)
			roller.set_meta("door_hw", "roller")
			roller.set_meta("roller_r", 0.03)
		_hw(car, "AntiLift", Vector3(0.04, 0.02, 0.04), Vector3(0, 0.07, 0), _alloy)
	_hw(body, "BeltClamp", Vector3(0.06, 0.03, 0.03), Vector3(inward, 1.22, 0), _alloy)
	_hw(body, "FloorGuide", Vector3(0.04, 0.02, 0.03), Vector3(0, -1.18, 0), _alloy)
	_hw(body, "ManualHandle", Vector3(0.02, 0.28, 0.03), Vector3(0.48 * sign, -0.05, -0.04), _alloy)


func _pocket_frame(door: Node3D) -> void:
	_mesh(door, "HeadBox", Vector3(4.4, 0.12, 0.15), Vector3(0, 2.55, 0), _gun, 0.003)
	_hw(door, "AccessPanel", Vector3(0.28, 0.08, 0.004), Vector3(0, 2.55, -0.08), _alloy)
	_hw(door, "Track", Vector3(4.2, 0.02, 0.03), Vector3(0, 2.46, 0), _alloy)
	_hw(door, "Motor", Vector3(0.22, 0.08, 0.10), Vector3(0, 2.62, 0), _gun)
	_hw(door, "TensionerL", Vector3(0.06, 0.06, 0.04), Vector3(-2.05, 2.48, 0), _alloy)
	_hw(door, "TensionerR", Vector3(0.06, 0.06, 0.04), Vector3(2.05, 2.48, 0), _alloy)
	_hw(door, "Belt", Vector3(4.1, 0.004, 0.012), Vector3(0, 2.44, 0.02), _seal)
	_mesh(door, "Soffit", Vector3(2.05, 0.02, 0.16), Vector3(0, 2.42, 0), _gun, 0.0)
	_hw(door, "Solenoid", Vector3(0.08, 0.04, 0.04), Vector3(0, 2.36, -0.06), _alloy)
	_hw(door, "Keeper", Vector3(0.04, 0.03, 0.03), Vector3(0.06, 2.36, -0.06), _alloy)
	_hw(door, "Radar", Vector3(0.12, 0.04, 0.06), Vector3(0, 2.48, -0.22), _gun)
	_hw(door, "HexRelease", Vector3(0.06, 0.08, 0.004), Vector3(-1.12, 1.05, -0.09), _alloy)
	for side in [-1, 1]:
		var sx := float(side)
		_mesh(door, "Fascia%s" % ("L" if side < 0 else "R"), Vector3(1.40, 2.50, 0.02), Vector3(sx * 1.678, 1.25, -0.055), _gun, 0.0)
		_mesh(door, "FasciaBack%s" % ("L" if side < 0 else "R"), Vector3(1.40, 2.50, 0.02), Vector3(sx * 1.678, 1.25, 0.055), _gun, 0.0)
		_mesh(door, "PocketFace%s" % ("L" if side < 0 else "R"), Vector3(0.008, 2.35, 0.08), Vector3(sx * 1.063, 1.20, 0.0), _gun, 0.0)
		_hw(door, "Bumper%s" % side, Vector3(0.02, 0.08, 0.03), Vector3(sx * 2.08, 1.2, 0), _seal)
		_hw(door, "FloorChannel%s" % side, Vector3(1.1, 0.004, 0.014), Vector3(sx * 1.4, 0.004, 0), _seal)
		for i in 4:
			_hw(door, "LightCurtain%s%d" % [("L" if side < 0 else "R"), i], Vector3(0.012, 0.012, 0.008), Vector3(sx * 1.04, 0.45 + float(i) * 0.48, -0.07), _alloy)
	# Fascia collision so the pocket cavity is not a shortcut. Separated from the leaf in Z.
	for side in [-1.0, 1.0]:
		var fb := StaticBody3D.new()
		fb.name = "FasciaBody%s" % side
		door.add_child(fb)
		var cs := CollisionShape3D.new()
		var box := BoxShape3D.new()
		box.size = Vector3(1.40, 2.50, 0.02)
		cs.shape = box
		cs.position = Vector3(side * 1.678, 1.25, -0.055)
		fb.add_child(cs)


func _hatch(prof: MechDoorProfile, x: float) -> MechDoor:
	var door := _door("hatch", x)
	var spec := _spec(prof, "leaf")
	var pivot := Node3D.new()
	pivot.name = "HatchHinge"
	pivot.position = Vector3(-0.55, 0.0, -0.064)
	door.add_child(pivot)
	var body := _new_body(pivot)
	var plug := Vector3(1.10, 2.10, 0.12)
	# Body origin is the hinge. Plug center sits 0.55 m toward +X.
	# +0.038 m in Z puts the closed plug's corridor face 6 mm off the wall (wall starts at z=0.04).
	_mesh(body, "LeafFace", plug, Vector3(0.55, 1.056, 0.038), _gun, 0.003)
	_mesh(body, "Inset", Vector3(0.78, 1.35, 0.008), Vector3(0.55, 1.10, -0.028), _graphite, 0.0)
	_body_shape(body, plug)
	# Shape follows the visual center, not the hinge.
	var shape := body.get_node("LeafShape") as CollisionShape3D
	shape.position = Vector3(0.55, 1.056, 0.038)
	_hatch_hw(door, body)
	var leaves: Array = [{
		"name": "leaf",
		"sign": int(spec.get("sign", -1)),
		"stagger_open": float(spec.get("stagger_open", 0.0)),
		"stagger_close": float(spec.get("stagger_close", 0.0)),
		"body": body,
		"pivot": pivot,
		"rest": Vector3.ZERO,
		"axis": Vector3.ZERO,
	}]
	_lamp(door, Vector3(0.72, 1.55, -0.16))
	_reveal(door, "Reveal_Soffit", Vector3(0.84, 0.010, 0.010), Vector3(0, 1.95, -0.10))
	_reveal(door, "Reveal_JambL", Vector3(0.010, 1.70, 0.010), Vector3(-0.48, 1.0, -0.10))
	_reveal(door, "Reveal_JambR", Vector3(0.010, 1.70, 0.010), Vector3(0.48, 1.0, -0.10))
	_downlight(door, Vector3(0, 2.35, -0.45), Vector3(x, 1.1, -0.1))
	door.bind(prof, leaves, true)
	# Plug is wider than the clear hole, so it swings to the approach side (-Z).
	door.configure_sensor(Vector3(0.0, 1.05, -0.55), Vector3(0.80, 1.85, 1.05))
	door.set_approach(Vector3(0, 0, -1))
	_mark_walk(door)
	door.set_meta("block_x", 0.0)
	return door


func _hatch_hw(door: Node3D, body: Node3D) -> void:
	var wall := StaticBody3D.new()
	wall.name = "HatchWallBody"
	door.add_child(wall)
	# Frame around the 0.90 x 1.90 clear hole. Four boxes.
	_wall_piece(wall, Vector3(2.6, 1.20, 0.16), Vector3(0, 2.55, 0.12))
	_wall_piece(wall, Vector3(0.85, 1.90, 0.16), Vector3(-0.875, 0.95, 0.12))
	_wall_piece(wall, Vector3(0.85, 1.90, 0.16), Vector3(0.875, 0.95, 0.12))
	_mesh(door, "HatchHead", Vector3(2.6, 1.20, 0.16), Vector3(0, 2.55, 0.12), _gun, 0.003)
	_mesh(door, "HatchJambL", Vector3(0.85, 1.90, 0.16), Vector3(-0.875, 0.95, 0.12), _gun, 0.003)
	_mesh(door, "HatchJambR", Vector3(0.85, 1.90, 0.16), Vector3(0.875, 0.95, 0.12), _gun, 0.003)
	_hw(door, "HingeHeavy0", Vector3(0.08, 0.22, 0.08), Vector3(-0.62, 0.35, -0.06), _alloy)
	_hw(door, "HingeHeavy1", Vector3(0.08, 0.22, 0.08), Vector3(-0.62, 1.70, -0.06), _alloy)
	_hw(door, "Davit", Vector3(0.04, 0.04, 0.55), Vector3(-0.35, 2.20, 0.15), _alloy)
	_hw(door, "Actuator", Vector3(0.14, 0.16, 0.14), Vector3(-0.62, 0.22, -0.02), _gun)
	var rod := Node3D.new()
	rod.name = "DamperRod"
	rod.set_meta("door_hw", "rod")
	door.add_child(rod)
	var mesh := MeshInstance3D.new()
	mesh.name = "Mesh"
	var bm := BoxMesh.new()
	bm.size = Vector3(0.03, 0.03, 1.0)
	mesh.mesh = bm
	mesh.set_surface_override_material(0, _alloy)
	rod.add_child(mesh)
	var aa := Node3D.new()
	aa.name = "AnchorA"
	aa.position = Vector3(-0.62, 0.55, -0.02)
	door.add_child(aa)
	var ab := Node3D.new()
	ab.name = "AnchorB"
	ab.position = Vector3(0.15, 1.15, 0.0)
	body.add_child(ab)
	rod.set_meta("anchor_a", aa)
	rod.set_meta("anchor_b", ab)
	var dog_pos := [
		Vector2(-0.02, 0.25), Vector2(-0.02, 1.70),
		Vector2(1.02, 0.25), Vector2(1.02, 1.70),
		Vector2(0.25, 0.08), Vector2(0.80, 0.08),
		Vector2(0.25, 1.95), Vector2(0.80, 1.95),
	]
	for i in dog_pos.size():
		var p: Vector2 = dog_pos[i]
		var dog := _mesh(body, "Dog%d" % (i + 1), Vector3(0.04, 0.08, 0.06), Vector3(p.x, p.y, 0.04), _alloy, 0.002)
		dog.set_meta("door_hw", "dog")
		dog.set_meta("rest", dog.position)
		dog.set_meta("retract", Vector3(0, 0, -0.025))
		dog.set_meta("stagger", float(i) * 0.0375)
		dog.set_meta("hw_id", "Dog")
		_hw(door, "DogKeeper%d" % (i + 1), Vector3(0.05, 0.06, 0.03), Vector3(-0.55 + p.x, p.y, 0.02), _gun)
	_hw(body, "Linkage", Vector3(0.70, 0.02, 0.02), Vector3(0.55, 1.05, -0.05), _alloy)
	var wheel := _mesh(body, "LockWheel", Vector3(0.28, 0.28, 0.03), Vector3(0.55, 1.05, -0.08), _alloy, 0.0)
	wheel.set_meta("door_hw", "wheel")
	_mesh(door, "InflatableSeal", Vector3(1.14, 2.14, 0.012), Vector3(0, 1.056, -0.012), _seal, 0.0)
	var seal := door.get_node("InflatableSeal") as Node3D
	seal.set_meta("door_hw", "seal")
	_hw(body, "PushOffRam0", Vector3(0.04, 0.04, 0.10), Vector3(0.95, 0.55, 0.02), _alloy)
	_hw(body, "PushOffRam1", Vector3(0.04, 0.04, 0.10), Vector3(0.95, 1.55, 0.02), _alloy)
	_gauge(door, "GaugeApproach", Vector3(0.72, 1.55, -0.14))
	_gauge(door, "GaugeFar", Vector3(0.72, 1.55, 0.22))
	_hw(door, "EqualizePort", Vector3(0.10, 0.08, 0.02), Vector3(0.35, 1.85, -0.02), _alloy)
	_hw(door, "HoldOpenCatch", Vector3(0.06, 0.04, 0.08), Vector3(0.55, 0.12, 0.20), _alloy)
	_hw(body, "HubLamp", Vector3(0.10, 0.10, 0.02), Vector3(0.55, 1.05, -0.10), _alloy)
	_hw(door, "Beacon", Vector3(0.06, 0.06, 0.06), Vector3(0.85, 2.15, -0.10), _orange)
	var hand := _hw(door, "Handwheel", Vector3(0.16, 0.16, 0.03), Vector3(0.85, 1.15, -0.16), _orange)
	hand.set_meta("door_hw", "wheel")
	_hw(door, "EqualizeLever", Vector3(0.03, 0.16, 0.03), Vector3(0.85, 0.85, -0.14), _orange)
	var band := _mesh(door, "HazardBand", Vector3(0.90, 0.06, 0.004), Vector3(0, 0.04, -0.02), _orange, 0.0)
	var band_mat := band.get_surface_override_material(0).duplicate() as StandardMaterial3D
	band_mat.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
	band_mat.albedo_color.a = 0.9
	band.set_surface_override_material(0, band_mat)
	band.position.z = -0.004


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
	_shift_to_plane(inst, leaves)
	_retint(inst)
	_rename_glass(inst)
	_bay_pair_hw(door, inst, prof.door_id, leaves)
	_lamp(door, Vector3(0, 2.35, -0.25))
	_reveal(door, "Reveal_Soffit", Vector3(1.6, 0.010, 0.010), Vector3(0, 2.45, -0.2))
	_reveal(door, "Reveal_JambL", Vector3(0.010, 2.0, 0.010), Vector3(-0.95, 1.2, -0.2))
	_reveal(door, "Reveal_JambR", Vector3(0.010, 2.0, 0.010), Vector3(0.95, 1.2, -0.2))
	_downlight(door, Vector3(0, 2.9, -0.55), Vector3(x, 1.4, 0))
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
				if "whitecomposite" in low or "white_composite" in low:
					dup.albedo_color = PEARL
					dup.albedo_texture = null
				elif "glass" in low:
					dup.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA_SCISSOR
					dup.albedo_color = Color(0.70, 0.84, 0.89)
					dup.roughness = 0.08
					dup.metallic = 0.0
				else:
					var c := dup.albedo_color
					dup.albedo_color = Color(minf(c.r, 0.90), minf(c.g, 0.90), minf(c.b, 0.90), c.a)
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
		# Clear hole is x -0.45..+0.45. The plug swings out to -Z and is not the opening.
		gaps.append([-0.45, 0.45])
		gaps = _subtract_many(gaps, opened)
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
