# Rook: box-side preview renderer for assemble_preview.py (loads GLBs at runtime, hides *colonly* nodes, renders shots).
extends SceneTree
var tagged := {}
func _hide_col(n: Node) -> void:
	for c in n.get_children():
		if "colonly" in String(c.name): c.visible = false
		_hide_col(c)
func _init() -> void:
	var job = JSON.parse_string(FileAccess.get_file_as_string("res://job.json"))
	var cache := {}
	var world := Node3D.new(); root.add_child(world)
	for p in job["placements"]:
		var path: String = p["glb"]
		if not cache.has(path):
			var doc := GLTFDocument.new(); var st := GLTFState.new()
			if doc.append_from_file(path, st) != OK: push_error("load " + path); continue
			var sc: Node = doc.generate_scene(st); _hide_col(sc); cache[path] = sc
		var inst: Node3D = cache[path].duplicate()
		inst.position = Vector3(p["p"][0], p["p"][1], p["p"][2]); inst.rotation_degrees = Vector3(0, p["yaw"], 0)
		world.add_child(inst)
		var t: String = p["tag"]
		if not tagged.has(t): tagged[t] = []
		tagged[t].append(inst)
	var env := WorldEnvironment.new(); var e := Environment.new()
	e.background_mode = Environment.BG_COLOR; e.background_color = Color(0.62, 0.70, 0.78)
	e.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR; e.ambient_light_color = Color(0.85, 0.88, 0.92); e.ambient_light_energy = 0.55
	e.tonemap_mode = Environment.TONE_MAPPER_FILMIC
	env.environment = e; root.add_child(env)
	var sun := DirectionalLight3D.new(); sun.rotation_degrees = Vector3(-55, -35, 0); sun.light_energy = 0.9; sun.shadow_enabled = true
	sun.directional_shadow_max_distance = 400.0; root.add_child(sun)
	var cam := Camera3D.new(); cam.far = 2000.0; cam.near = 0.1; root.add_child(cam); cam.current = true
	await process_frame
	await process_frame
	for s in job["shots"]:
		for t in tagged.keys():
			for n in tagged[t]: n.visible = not (t in s["hide"])
		e.ambient_light_energy = s.get("amb", 0.55)
		cam.fov = s["fov"]
		cam.look_at_from_position(Vector3(s["pos"][0], s["pos"][1], s["pos"][2]), Vector3(s["look"][0], s["look"][1], s["look"][2]), Vector3.UP)
		for i in range(6): await process_frame
		root.get_viewport().get_texture().get_image().save_png(s["out"]); print("shot ", s["name"])
	quit()
