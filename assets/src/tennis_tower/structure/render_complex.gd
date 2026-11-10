# Rook: box-side preview renderer for assemble_complex.py.
# Brighter sky + hemisphere fill + interior omni grid so metals and interiors read.
# Hides *colonly* nodes. Loads job.json (placements, shots, lights).
extends SceneTree
var tagged := {}

func _hide_col(n: Node) -> void:
	for c in n.get_children():
		if "colonly" in String(c.name):
			c.visible = false
		_hide_col(c)

func _make_omni(p: Vector3, energy: float, rng: float, color: Color) -> OmniLight3D:
	var o := OmniLight3D.new()
	o.position = p
	o.light_energy = energy
	o.light_color = color
	o.omni_range = rng
	o.omni_attenuation = 1.4
	o.shadow_enabled = false
	return o

func _init() -> void:
	var job = JSON.parse_string(FileAccess.get_file_as_string("res://job.json"))
	var cache := {}
	var world := Node3D.new()
	root.add_child(world)
	for p in job["placements"]:
		var path: String = p["glb"]
		if not cache.has(path):
			if not FileAccess.file_exists(path):
				push_error("missing " + path)
				continue
			var doc := GLTFDocument.new()
			var st := GLTFState.new()
			if doc.append_from_file(path, st) != OK:
				push_error("load " + path)
				continue
			var sc: Node = doc.generate_scene(st)
			_hide_col(sc)
			cache[path] = sc
		var inst: Node3D = cache[path].duplicate()
		inst.position = Vector3(p["p"][0], p["p"][1], p["p"][2])
		inst.rotation_degrees = Vector3(0, p["yaw"], 0)
		world.add_child(inst)
		var t: String = p["tag"]
		if not tagged.has(t):
			tagged[t] = []
		tagged[t].append(inst)
	print("loaded ", job["placements"].size(), " instances, ", cache.size(), " unique glbs")

	var env := WorldEnvironment.new()
	var e := Environment.new()
	var sky := Sky.new()
	var sm := ProceduralSkyMaterial.new()
	sm.sky_top_color = Color(0.48, 0.64, 0.86)
	sm.sky_horizon_color = Color(0.82, 0.86, 0.90)
	sm.ground_horizon_color = Color(0.70, 0.73, 0.70)
	sm.ground_bottom_color = Color(0.50, 0.54, 0.50)
	sm.sky_energy_multiplier = 1.35
	sm.ground_energy_multiplier = 0.85
	sky.sky_material = sm
	e.background_mode = Environment.BG_SKY
	e.sky = sky
	e.ambient_light_source = Environment.AMBIENT_SOURCE_SKY
	e.ambient_light_color = Color(0.92, 0.94, 0.98)
	e.ambient_light_energy = 1.6
	e.tonemap_mode = Environment.TONE_MAPPER_FILMIC
	e.tonemap_exposure = 1.2
	if e.has_method("set_reflected_light_source"):
		e.reflected_light_source = Environment.REFLECTION_SOURCE_SKY
	env.environment = e
	root.add_child(env)

	var sun := DirectionalLight3D.new()
	sun.rotation_degrees = Vector3(-52, -38, 0)
	sun.light_energy = 1.15
	sun.light_color = Color(1.0, 0.97, 0.92)
	sun.shadow_enabled = true
	sun.directional_shadow_max_distance = 400.0
	root.add_child(sun)

	# Cool sky fill (hemisphere opposite the sun); no shadows.
	var fill := DirectionalLight3D.new()
	fill.rotation_degrees = Vector3(55, 140, 0)
	fill.light_energy = 0.55
	fill.light_color = Color(0.72, 0.82, 1.0)
	fill.shadow_enabled = false
	root.add_child(fill)

	var fill2 := DirectionalLight3D.new()
	fill2.rotation_degrees = Vector3(-20, 130, 0)
	fill2.light_energy = 0.32
	fill2.light_color = Color(0.95, 0.96, 1.0)
	fill2.shadow_enabled = false
	root.add_child(fill2)

	var omnis: Array[OmniLight3D] = []
	var warm := Color(1.0, 0.96, 0.90)
	# Interior point grid on each occupied floor, plus a few tall-hall extras.
	for y in [3.0, 9.0, 15.4]:
		var x := -4.0
		while x <= 140.0:
			var z := 8.0
			while z <= 74.0:
				var o := _make_omni(Vector3(x, y, z), 1.7, 24.0, warm)
				root.add_child(o)
				omnis.append(o)
				z += 20.0
			x += 20.0
	# Foyer, pool hall, leisure water, arcade — slightly stronger local lamps.
	for p2 in [
		Vector3(-6, 3.0, 26), Vector3(-6, 3.0, 40), Vector3(-6, 3.0, 53),
		Vector3(16, 4.5, 14), Vector3(16, 4.5, 28), Vector3(16, 8.0, 20),
		Vector3(16, 4.5, 58), Vector3(22, 8.5, 56),
		Vector3(128, 3.0, 40), Vector3(128, 9.0, 40),
		Vector3(70, 3.0, 72), Vector3(72, 9.0, 40), Vector3(72, 15.5, 40),
		Vector3(-6, 15.5, 40), Vector3(134, 15.5, 40)
	]:
		var o2 := _make_omni(p2, 2.4, 22.0, warm)
		root.add_child(o2)
		omnis.append(o2)
	print("lights omni=", omnis.size())

	var cam := Camera3D.new()
	cam.far = 2000.0
	cam.near = 0.1
	root.add_child(cam)
	cam.current = true

	await process_frame
	await process_frame

	for s in job["shots"]:
		for t in tagged.keys():
			for n in tagged[t]:
				n.visible = not (t in s["hide"])
		e.ambient_light_energy = s.get("amb", 1.6)
		e.tonemap_exposure = s.get("exposure", 1.2)
		var omni_mul: float = s.get("omni", 1.0)
		for o in omnis:
			if not o.has_meta("base_e"):
				o.set_meta("base_e", o.light_energy)
			o.light_energy = float(o.get_meta("base_e")) * omni_mul
		cam.fov = s["fov"]
		cam.look_at_from_position(
			Vector3(s["pos"][0], s["pos"][1], s["pos"][2]),
			Vector3(s["look"][0], s["look"][1], s["look"][2]),
			Vector3.UP
		)
		for i in range(6):
			await process_frame
		root.get_viewport().get_texture().get_image().save_png(s["out"])
		print("shot ", s["name"])
	quit()
