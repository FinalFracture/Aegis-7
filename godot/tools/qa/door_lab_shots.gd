extends Node
## Windowed opengl3 captures for the door lab. Not headless.
## Rewrites V-LUMA, V-SHADOW, and V-ZFIGHT-FLICKER from the pixels it saves.

const IDS := ["pocket", "bay3", "pair", "hatch"]
const QA_CAMS := ["front", "oblique45", "jamb", "top", "player"]
const STATES := ["closed", "025", "050", "open", "closing"]

var _lab: Node3D
var _player: CharacterBody3D
var _doors: Dictionary = {}
var _out: String = ""
var _cam: Camera3D
var _vis_fail: int = 0
var _pixel: Dictionary = {}


func start(lab: Node3D) -> void:
	_lab = lab
	var info: Dictionary = lab.get_meta("lab_info")
	_player = info["player"]
	_doors = info["doors"]
	_out = _read_out()
	Engine.max_physics_steps_per_frame = 1
	Engine.physics_ticks_per_second = 60
	_setup_window()
	_player.drive_enabled = false
	_player.velocity = Vector3.ZERO
	_player.global_position = Vector3(0.0, 0.0, -200.0)
	var pcam: Camera3D = _player.find_child("PlayerCamera", true, false) as Camera3D
	if pcam != null:
		pcam.current = false
	_cam = Camera3D.new()
	_cam.name = "ShotCam"
	_cam.near = 0.05
	_cam.far = 200.0
	_lab.add_child(_cam)
	_cam.current = true
	for id in IDS:
		var door: MechDoor = _doors[id]
		door.set_physics_process(false)
		door.reset_closed()
		_pixel[id] = {"luma": 1.0, "shadow": 0.0, "shadow_hot": 0, "flicker": 0.0, "flicker_hot": 0}
	await _shoot_all()
	_rewrite_metrics()
	_call_sheet()
	_mirror_pngs()
	print("DONE --qa-door-lab-shots fails=%d" % _vis_fail)
	get_tree().quit(0 if _vis_fail == 0 else 1)


func _setup_window() -> void:
	DisplayServer.window_set_mode(DisplayServer.WINDOW_MODE_WINDOWED)
	DisplayServer.window_set_size(Vector2i(1920, 1080))
	get_tree().root.size = Vector2i(1920, 1080)


func _read_out() -> String:
	var rel := "user://door_lab_run"
	var args := OS.get_cmdline_user_args()
	for i in args.size():
		if args[i] == "--qa-door-lab-out" and i + 1 < args.size():
			rel = str(args[i + 1])
	if rel.begins_with("res://") or rel.begins_with("user://"):
		return ProjectSettings.globalize_path(rel)
	if rel.begins_with("/") or (rel.length() > 2 and rel[1] == ":"):
		return rel
	var base := ProjectSettings.globalize_path("res://")
	return base.path_join(rel).simplify_path()


func _shoot_all() -> void:
	for id in IDS:
		var door: MechDoor = _doors[id]
		print("[door_lab] shots %s" % id)
		door.reset_closed()
		for state in STATES:
			_pose(door, state)
			for cam_name in QA_CAMS:
				_place(door, cam_name)
				var burst: bool = state == "closed" and (cam_name == "front" or cam_name == "jamb")
				var frames: Array = await _grab_frames(8 if burst else 1)
				_save(frames[0], "%s/shots/%s_%s.png" % [id, cam_name, state])
				if cam_name == "front" and (state == "closed" or state == "open"):
					_note_luma(id, frames[0])
				if state == "closed" and cam_name == "front":
					_note_shadow(id, frames)
					_note_flicker(id, frames, _seam_rect(frames[0]))
				elif state == "closed" and cam_name == "jamb":
					_note_flicker(id, frames, _seam_rect(frames[0]))
		_place(door, "hero")
		for state in STATES:
			_pose(door, state)
			_place(door, "hero")
			var hero_n: int = 8 if state == "closed" else 1
			var hero_frames: Array = await _grab_frames(hero_n)
			_save(hero_frames[0], "%s/shots/hero_%s.png" % [id, state])
			if state == "closed" or state == "open":
				_note_luma(id, hero_frames[0])
			if state == "closed":
				_note_shadow(id, hero_frames)
		_pose(door, "closed")
		_place(door, "square")
		_save(await _one_frame(), "%s/shots/square_closed.png" % id)
		_place(door, "detail")
		_save(await _one_frame(), "%s/shots/detail_closed.png" % id)
		_pose(door, "open")
		_place(door, "detail")
		_save(await _one_frame(), "%s/shots/detail_open.png" % id)
		_pose(door, "050")
		_place(door, "player_sloane")
		_save(await _one_frame(), "%s/shots/player_sloane_050.png" % id)
		_pose(door, "open")
		_place(door, "threshold")
		_save(await _one_frame(), "%s/shots/threshold_open.png" % id)
		await _open_strip(door, id)
		door.set_physics_process(false)
		door.reset_closed()


func _open_strip(door: MechDoor, id: String) -> void:
	door.reset_closed()
	door.set_physics_process(true)
	_place(door, "hero")
	door.command_open()
	for i in 8:
		if i > 0:
			var waited := 0.0
			while waited < (1.0 / 24.0) - 0.0001:
				await get_tree().physics_frame
				waited += 1.0 / 60.0
		else:
			await get_tree().physics_frame
		var img: Image = await _shot_image()
		_save(img, "%s/shots/hero_openstrip_%d.png" % [id, i])
	door.set_physics_process(false)


func _pose(door: MechDoor, state: String) -> void:
	door.force_q(_q_for(door, state))


func _q_for(door: MechDoor, state: String) -> float:
	var travel := door.profile.travel
	if state == "025":
		return travel * 0.25
	if state == "050":
		return travel * 0.5
	if state == "open":
		return travel
	if state == "closing":
		return _half_close_q(door)
	return 0.0


func _half_close_q(door: MechDoor) -> float:
	var lo := 0.0
	var hi := door.profile.close_duration
	for _i in 20:
		var mid := (lo + hi) * 0.5
		var q := float(door.profile.sample("close", mid)["q"])
		if q > door.profile.travel * 0.5:
			lo = mid
		else:
			hi = mid
	return float(door.profile.sample("close", (lo + hi) * 0.5)["q"])


func _place(door: MechDoor, cam_name: String) -> void:
	var spec: Dictionary = _cam_spec(door, cam_name)
	_cam.fov = float(spec["fov"])
	_cam.global_position = spec["at"]
	var up: Vector3 = spec["up"]
	_cam.look_at(spec["look"], up)


func _cam_spec(door: MechDoor, cam_name: String) -> Dictionary:
	var origin := door.global_position
	var cx := origin.x + float(door.get_meta("walk_x", 0.0))
	var dz := origin.z
	var look_y: float = 1.05 if door.door_id == "hatch" else 1.15
	var look := Vector3(cx, look_y, dz)
	var half := 1.05
	if door.door_id == "bay3":
		half = 1.65
	elif door.door_id == "pair":
		half = 0.95
	elif door.door_id == "hatch":
		half = 0.50
	var jamb := Vector3(cx - half, 1.1, dz)
	var ang45 := deg_to_rad(45.0)
	var ang30 := deg_to_rad(30.0)
	var at := Vector3(cx, 1.62, dz - 4.0)
	var fov := 40.0
	var up := Vector3.UP
	match cam_name:
		"front", "square":
			at = Vector3(cx, 1.62 if cam_name == "front" else 1.5, dz - 4.0)
			fov = 40.0
		"oblique45":
			at = Vector3(cx + sin(ang45) * 3.2, 1.62, dz - cos(ang45) * 3.2)
			fov = 50.0
		"jamb", "detail":
			at = jamb + Vector3(-sin(ang45) * 0.9, 0.0, -cos(ang45) * 0.9)
			look = jamb
			fov = 35.0
		"top":
			at = Vector3(cx, look_y + 4.0, dz)
			fov = 40.0
			up = Vector3(0.0, 0.0, 1.0)
		"player":
			at = Vector3(cx, 1.62, dz - 1.8)
			fov = 70.0
		"hero":
			at = Vector3(cx + sin(ang30) * 3.2, 1.6, dz - cos(ang30) * 3.2)
			fov = 50.0
		"player_sloane":
			at = Vector3(cx, 1.65, dz - 1.8)
			fov = 75.0
		"threshold":
			at = Vector3(cx, 0.35, dz - 1.2)
			look = Vector3(cx, 0.35 + tan(deg_to_rad(10.0)) * 1.2, dz)
			fov = 45.0
	return {"at": at, "look": look, "fov": fov, "up": up}


func _one_frame() -> Image:
	var frames: Array = await _grab_frames(1)
	return frames[0]


func _grab_frames(n: int) -> Array:
	var out: Array = []
	for _i in n:
		out.append(await _shot_image())
	return out


func _shot_image() -> Image:
	await get_tree().process_frame
	await RenderingServer.frame_post_draw
	var img := get_viewport().get_texture().get_image()
	if img == null:
		return Image.create(16, 16, false, Image.FORMAT_RGBA8)
	if img.get_format() != Image.FORMAT_RGBA8:
		img.convert(Image.FORMAT_RGBA8)
	return img


func _save(img: Image, rel: String) -> void:
	var path := _out.path_join(rel)
	DirAccess.make_dir_recursive_absolute(path.get_base_dir())
	img.save_png(path)


func _seam_rect(img: Image) -> Rect2i:
	var w := img.get_width()
	var h := img.get_height()
	var x := int(w / 2) - 8
	var y0 := int(h * 0.22)
	var y1 := int(h * 0.78)
	return Rect2i(x, y0, 16, maxi(y1 - y0, 16))


func _leaf_rect(img: Image) -> Rect2i:
	var w := img.get_width()
	var h := img.get_height()
	return Rect2i(int(w * 0.32), int(h * 0.28), int(w * 0.36), int(h * 0.44))


func _note_luma(id: String, img: Image) -> void:
	var score := _best_cell_luma(img)
	var slot: Dictionary = _pixel[id]
	slot["luma"] = minf(float(slot["luma"]), score)
	_pixel[id] = slot


func _best_cell_luma(img: Image) -> float:
	var w := img.get_width()
	var h := img.get_height()
	var best := 0.0
	for gy in 2:
		for gx in 3:
			var rect := Rect2i(int(w * (0.12 + gx * 0.25)), int(h * (0.22 + gy * 0.28)), int(w * 0.22), int(h * 0.24))
			best = maxf(best, _mean_luma(img, rect))
	return best


func _note_shadow(id: String, frames: Array) -> void:
	if frames.size() < 2:
		return
	var stat := _flicker_stat(frames, _leaf_rect(frames[0]))
	var slot: Dictionary = _pixel[id]
	slot["shadow"] = maxf(float(slot["shadow"]), float(stat["mean"]))
	slot["shadow_hot"] = maxi(int(slot["shadow_hot"]), int(stat["hot"]))
	_pixel[id] = slot


func _note_flicker(id: String, frames: Array, rect: Rect2i) -> void:
	if frames.size() < 2:
		return
	var stat := _flicker_stat(frames, rect)
	var slot: Dictionary = _pixel[id]
	slot["flicker"] = maxf(float(slot["flicker"]), float(stat["mean"]))
	slot["flicker_hot"] = maxi(int(slot["flicker_hot"]), int(stat["hot"]))
	_pixel[id] = slot


func _flicker_stat(frames: Array, rect: Rect2i) -> Dictionary:
	var mean_acc := 0.0
	var pairs := 0
	var hot_count := {}
	var base: Image = frames[0]
	for fi in range(1, frames.size()):
		var img: Image = frames[fi]
		var step := 2
		var y := rect.position.y
		while y < rect.position.y + rect.size.y:
			var x := rect.position.x
			while x < rect.position.x + rect.size.x:
				if x >= 0 and y >= 0 and x < img.get_width() and y < img.get_height():
					var d := absf(_luma_at(img, x, y) - _luma_at(base, x, y))
					mean_acc += d
					pairs += 1
					if d > 8.0 / 255.0:
						var key := "%d,%d" % [x, y]
						hot_count[key] = int(hot_count.get(key, 0)) + 1
				x += step
			y += step
		base = img
	var hot := 0
	for k in hot_count.keys():
		if int(hot_count[k]) >= 3:
			hot += 1
	var mean := mean_acc / float(maxi(pairs, 1))
	return {"mean": mean, "hot": hot}


func _mean_luma(img: Image, rect: Rect2i) -> float:
	var acc := 0.0
	var n := 0
	var y := rect.position.y
	while y < rect.position.y + rect.size.y:
		var x := rect.position.x
		while x < rect.position.x + rect.size.x:
			if x >= 0 and y >= 0 and x < img.get_width() and y < img.get_height():
				acc += _luma_at(img, x, y)
				n += 1
			x += 4
		y += 4
	if n == 0:
		return 0.0
	return acc / float(n)


func _luma_at(img: Image, x: int, y: int) -> float:
	var c := img.get_pixel(x, y)
	return 0.2126 * c.r + 0.7152 * c.g + 0.0722 * c.b


func _rewrite_metrics() -> void:
	var vis_ids := {}
	for id in IDS:
		var slot: Dictionary = _pixel[id]
		var luma := float(slot["luma"])
		var shadow := float(slot["shadow"])
		var shadow_hot := int(slot["shadow_hot"])
		var flicker := float(slot["flicker"])
		var flicker_hot := int(slot["flicker_hot"])
		var luma_ok: bool = luma >= 0.10
		var shadow_ok: bool = shadow <= (2.0 / 255.0) + 1.0e-5 and shadow_hot == 0
		var flicker_ok: bool = flicker <= (2.0 / 255.0) + 1.0e-5 and flicker_hot == 0
		print("[door_lab] %s V-LUMA %s measured=%.4f limit=0.10" % [id, "PASS" if luma_ok else "FAIL", luma])
		print("[door_lab] %s V-SHADOW %s measured=%.5f hot=%d limit=0.00784" % [id, "PASS" if shadow_ok else "FAIL", shadow, shadow_hot])
		print("[door_lab] %s V-ZFIGHT-FLICKER %s measured=%.5f hot=%d limit=0.00784" % [id, "PASS" if flicker_ok else "FAIL", flicker, flicker_hot])
		var path := _out.path_join(id).path_join("metrics.json")
		var metrics: Array = _load_array(path)
		_upsert(metrics, "V-LUMA", luma_ok, luma, 0.10, "1", "best cell, Sloane A and front, closed and open")
		_upsert(metrics, "V-SHADOW", shadow_ok, shadow, 2.0 / 255.0, "1", "leaf-face mean |d| hot %d" % shadow_hot)
		_upsert(metrics, "V-ZFIGHT-FLICKER", flicker_ok, flicker, 2.0 / 255.0, "1", "seam band mean |d| hot %d" % flicker_hot)
		_store(path, metrics)
		if not luma_ok or not shadow_ok or not flicker_ok:
			_vis_fail += 1
		vis_ids[id] = luma_ok and shadow_ok and flicker_ok and _rest_visual_ok(metrics)
	_rewrite_summary(vis_ids)


func _rest_visual_ok(metrics: Array) -> bool:
	for item in metrics:
		if typeof(item) != TYPE_DICTIONARY:
			continue
		var cid := str(item["id"])
		var visual: bool = cid.begins_with("V-") or cid == "R6" or cid == "R8" or cid == "R11" or cid == "R12"
		if visual and not bool(item["pass"]):
			return false
	return true


func _rewrite_summary(vis_ids: Dictionary) -> void:
	var path := _out.path_join("summary.json")
	var parsed: Variant = JSON.parse_string(FileAccess.get_file_as_string(path))
	var summary: Dictionary = parsed if typeof(parsed) == TYPE_DICTIONARY else {}
	var doors: Dictionary = summary.get("doors", {})
	var any_fail := false
	for id in IDS:
		var door_row: Dictionary = doors.get(id, {})
		var vok: bool = bool(vis_ids.get(id, false))
		door_row["visual"] = "PASS" if vok else "FAIL"
		if not vok:
			any_fail = true
		if str(door_row.get("functional", "PASS")) == "FAIL":
			any_fail = true
		doors[id] = door_row
	summary["doors"] = doors
	summary["functional"] = summary.get("functional", "PASS")
	summary["sloane"] = "PENDING"
	summary["vance"] = "PENDING"
	summary["hooks_missing"] = []
	if any_fail or str(summary["functional"]) != "PASS":
		summary["visual"] = "FAIL"
		summary["verdict"] = "FAIL"
	else:
		summary["visual"] = "PASS"
		summary["verdict"] = "CONDITIONAL"
	_store(path, summary)
	_touch_meta()


func _touch_meta() -> void:
	var path := _out.path_join("meta.json")
	var parsed: Variant = JSON.parse_string(FileAccess.get_file_as_string(path))
	if typeof(parsed) != TYPE_DICTIONARY:
		return
	var meta: Dictionary = parsed
	meta["gpu"] = RenderingServer.get_video_adapter_name()
	meta["renderer"] = "gl_compatibility/opengl3"
	var vp := get_viewport().get_texture().get_image()
	if vp != null:
		meta["resolution"] = [vp.get_width(), vp.get_height()]
	var now := Time.get_datetime_dict_from_system()
	meta["updated"] = "%04d-%02d-%02d %02d:%02d CT" % [int(now["year"]), int(now["month"]), int(now["day"]), int(now["hour"]), int(now["minute"])]
	_store(path, meta)


func _load_array(path: String) -> Array:
	var parsed: Variant = JSON.parse_string(FileAccess.get_file_as_string(path))
	if typeof(parsed) != TYPE_ARRAY:
		return []
	return parsed


func _upsert(metrics: Array, cid: String, ok: bool, measured: float, limit: float, unit: String, note: String) -> void:
	var row := {"id": cid, "pass": ok, "measured": measured, "limit": limit, "unit": unit, "note": note}
	for i in metrics.size():
		var item: Variant = metrics[i]
		if typeof(item) == TYPE_DICTIONARY and str(item["id"]) == cid:
			metrics[i] = row
			return
	metrics.append(row)


func _store(path: String, data) -> void:
	DirAccess.make_dir_recursive_absolute(path.get_base_dir())
	var f := FileAccess.open(path, FileAccess.WRITE)
	if f == null:
		push_error("door lab shots cannot write %s" % path)
		return
	f.store_string(JSON.stringify(data, "\t"))
	f.close()


func _call_sheet() -> void:
	var script := ProjectSettings.globalize_path("res://").path_join("../tools/door_lab_contact_sheet.py").simplify_path()
	var output: Array = []
	var code := OS.execute("python", PackedStringArray([script, _out]), output, true)
	print("[door_lab] contact_sheet exit=%d %s" % [code, str(output)])


func _mirror_pngs() -> void:
	var dest := "C:/Users/upchu/aegis_shots/doorlab_A"
	_mirror_dir(_out, dest)


func _mirror_dir(src: String, dest: String) -> void:
	var dir := DirAccess.open(src)
	if dir == null:
		return
	DirAccess.make_dir_recursive_absolute(dest)
	for name in dir.get_files():
		if String(name).ends_with(".png"):
			DirAccess.copy_absolute(src.path_join(name), dest.path_join(name))
	for sub in dir.get_directories():
		_mirror_dir(src.path_join(sub), dest.path_join(sub))
