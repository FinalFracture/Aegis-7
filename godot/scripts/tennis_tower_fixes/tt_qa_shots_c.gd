extends Node
## --shot-ttfix-c. Windowed exit stills and per-room luminance.
## Room shots use shipped lighting only: no camera fill.

const OUT_DIR := "C:/Users/upchu/aegis_shots/ttfix_C"
const _TTRoomLights := preload("res://scripts/tennis_tower_fixes/tt_room_lighting.gd")

var ppa: PrefacePlayableArea
var _failures: int = 0


func _ready() -> void:
	_qa_run.call_deferred()


func _qa_run() -> void:
	var guard := 0
	var t0 := Time.get_ticks_msec()
	while (ppa == null or not ppa.has_meta("exterior_spawned") or ppa._player_body == null or ppa._tower == null) and guard < 6000:
		await get_tree().physics_frame
		guard += 1
	if ppa == null or ppa._player_body == null or ppa._tower == null or ppa._camera == null:
		print("[TT-SHOT-C] FAIL setup")
		get_tree().quit(1)
		return
	DirAccess.make_dir_recursive_absolute(OUT_DIR)
	if DisplayServer.get_name() != "headless":
		DisplayServer.window_set_mode(DisplayServer.WINDOW_MODE_WINDOWED)
		DisplayServer.window_set_size(Vector2i(1920, 1080))
	if ppa._hud != null:
		ppa._hud.visible = false
	ppa._third_person = false
	ppa._apply_view_mode()
	if ppa._flashlight != null:
		ppa._flashlight.visible = false
	_qa_show_body()
	await _qa_exit_still("C1_lap_pool_exits.png", Vector3(16.0, 6.2, 11.0), Vector3(28.0, 1.1, 11.0), Vector3(26.5, 0.5, 18.5), 62.0)
	await _qa_exit_still("C2_diving_tank_ladder.png", Vector3(22.0, 3.6, 23.0), Vector3(27.6, 0.6, 23.0), Vector3(24.0, 0.4, 23.0), 55.0)
	await _qa_exit_still("C3_river_exit.png", Vector3(18.0, 2.5, 45.6), Vector3(21.7, 0.55, 48.0), Vector3(21.7, 0.15, 47.6), 55.0)
	var body := ppa._player_body.get_node_or_null("TTShotBody")
	if body != null:
		body.visible = false
	var lines: PackedStringArray = PackedStringArray()
	for room: Dictionary in _TTRoomLights.rooms():
		var id := String(room["id"])
		var mean := await _qa_room(id, room["eye"], room["look"], "C_room_%s.png" % id)
		lines.append("%s %.1f" % [id, mean])
		if id == "f1_courts":
			await _qa_room(id + "_alias", room["eye"], room["look"], "C4_lit_court_hall_F1.png")
		elif id == "f2_rink":
			await _qa_room(id + "_alias", room["eye"], room["look"], "C5_lit_rink_F2.png")
		elif id == "f1_bowling":
			await _qa_room(id + "_alias", room["eye"], room["look"], "C6_lit_bowling_F1.png")
	var toddler := await _qa_room("f3_toddler", Vector3(134.0, 13.82, 54.0), Vector3(136.5, 13.4, 50.0), "C_room_f3_toddler.png")
	lines.append("f3_toddler %.1f" % toddler)
	var lobby := await _qa_room("lobby", Vector3(-9.0, 1.7, 44.0), Vector3(2.0, 1.4, 30.0), "C_room_lobby.png")
	lines.append("lobby %.1f" % lobby)
	if ppa._player_body != null:
		ppa._player_body.global_position = ppa._tower_xf * Vector3(-9.5, 0.3, 46.0)
	await ppa._qa_tower_draw_sample("lobby", ppa._tower_xf * Vector3(-9.0, 1.7, 44.0), ppa._tower_xf * Vector3(2.0, 1.4, 30.0), ppa._tower_up, "ttfix_c")
	var load_ms := Time.get_ticks_msec() - t0
	print("[TT-LUMA] load_ms=%d build_ms=%d" % [load_ms, int(ppa._tower_stats.get("ms", 0))])
	print("[TT-LUMA] table %s" % " | ".join(lines))
	print("[TT-SHOT-C] DONE failures=%d" % _failures)
	get_tree().quit(0 if _failures == 0 else 1)


func _qa_show_body() -> void:
	var host: CharacterBody3D = ppa._player_body
	if host.get_node_or_null("TTShotBody") != null:
		return
	var vis := MeshInstance3D.new()
	vis.name = "TTShotBody"
	var cap := CapsuleMesh.new()
	cap.radius = 0.35
	cap.height = 1.75
	vis.mesh = cap
	vis.position = Vector3(0.0, 0.995, 0.0)
	vis.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	var mat := StandardMaterial3D.new()
	mat.albedo_color = Color(0.92, 0.55, 0.18, 1.0)
	mat.roughness = 0.45
	vis.material_override = mat
	host.add_child(vis)


func _qa_exit_still(file_name: String, eye: Vector3, look: Vector3, stand: Vector3, fov: float) -> void:
	var feet := ppa._tower_xf * Vector3(stand.x, stand.y, stand.z)
	ppa._qa_tower_place(feet, ppa._tower_up, ppa._tower_xf * look)
	await ppa._qa_frames(8)
	await _qa_save(file_name, eye, look, fov)


func _qa_room(id: String, eye: Vector3, look: Vector3, file_name: String) -> float:
	var mean := await _qa_save(file_name, eye, look, 70.0)
	print("[TT-LUMA] room=%s mean=%.1f file=%s" % [id, mean, file_name])
	if not id.ends_with("_alias") and id != "lobby" and mean < 60.0:
		_failures += 1
		print("[TT-LUMA] LOW room=%s mean=%.1f" % [id, mean])
	return mean


func _qa_save(file_name: String, eye: Vector3, look: Vector3, fov: float) -> float:
	var xf: Transform3D = ppa._tower_xf
	ppa._qa_free_cam(xf * eye, xf * look, ppa._tower_up, fov)
	ppa._camera.current = true
	await ppa._qa_frames(6)
	var img: Image = await _qa_grab()
	var mean := 0.0
	if img == null or img.is_empty():
		_failures += 1
		print("[TT-SHOT-C] empty %s" % file_name)
		return 0.0
	var small: Image = img.duplicate() as Image
	small.resize(96, 54, Image.INTERPOLATE_BILINEAR)
	var acc := 0.0
	var w: int = small.get_width()
	var h: int = small.get_height()
	for y: int in range(h):
		for x: int in range(w):
			var c: Color = small.get_pixel(x, y)
			acc += 0.2126 * c.r + 0.7152 * c.g + 0.0722 * c.b
	mean = acc / float(w * h) * 255.0
	var path := OUT_DIR + "/" + file_name
	var err := img.save_png(path)
	if err != OK:
		_failures += 1
		print("[TT-SHOT-C] save fail %s err=%s" % [path, str(err)])
	else:
		print("[TT-SHOT-C] saved %s" % path)
	return mean


func _qa_grab() -> Image:
	await get_tree().process_frame
	await RenderingServer.frame_post_draw
	var tex: ViewportTexture = ppa.get_viewport().get_texture()
	if tex == null:
		return null
	return tex.get_image()
