extends Node
## Windowed opengl3 captures for the door lab. Not headless.
## Rewrites V-LUMA, V-SHADOW, and V-ZFIGHT-FLICKER from the pixels it saves.

const IDS := ["pocket", "bay3", "pair", "hatch"]
const HEROES := ["pocket", "bay3", "pair", "hatch", "floorhatch"]
const QA_CAMS := ["front", "oblique45", "jamb", "top", "player"]
const STATES := ["closed", "025", "050", "open", "closing"]

var _lab: Node3D
var _player: CharacterBody3D
var _doors: Dictionary = {}
var _out: String = ""
var _cam: Camera3D
var _fill: OmniLight3D
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
	_fill = OmniLight3D.new()
	_fill.name = "DetailFill"
	_fill.light_energy = 1.1
	_fill.shadow_enabled = false
	_fill.omni_range = 3.0
	_fill.visible = false
	_cam.add_child(_fill)
	_cam.far = 200.0
	_lab.add_child(_cam)
	_cam.current = true
	for id in _doors.keys():
		var door: MechDoor = _doors[id]
		door.set_physics_process(false)
		door.reset_closed()
		if id in IDS:
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
	await _motion_pack()
	await _heroes()


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


func _heroes() -> void:
	for id in HEROES:
		if not _doors.has(id):
			continue
		var door: MechDoor = _doors[id]
		for other in _doors.keys():
			(_doors[other] as MechDoor).reset_closed()
		if id == "hatch":
			# Closed plug so the graphite face, dogs and approach wheel fill the hero.
			_pose(door, "closed")
		elif id == "floorhatch":
			# Closed, so the lid reads seated in the frame. The strip shows the swing.
			_pose(door, "closed")
		else:
			_pose(door, "050")
		_place(door, "hero")
		var img := await _one_frame()
		_save(img, "hero_final_%s.png" % id)
		if id == "floorhatch":
			print("[door_lab] floorhatch V-LUMA measured=%.4f" % _mean_luma(img, _leaf_rect(img)))
		door.reset_closed()
	(_doors["pocket"] as MechDoor).set_locked(true)
	(_doors["pocket"] as MechDoor).reset_closed()
	_pose(_doors["bay3"], "050")
	_pose(_doors["pair"], "open")
	(_doors["hatch"] as MechDoor).present_fault()
	if _doors.has("floorhatch"):
		_pose(_doors["floorhatch"], "050")
	var a: MechDoor = _doors["pocket"]
	var b: MechDoor = _doors["hatch"]
	var mid_x := (a.global_position.x + b.global_position.x) * 0.5
	# The reflection cards sit in this frustum and read as white slabs. Heroes keep them.
	_set_reflect_cards(false)
	_cam.fov = 76.0
	_cam.global_position = Vector3(mid_x, 3.7, -12.0)
	_cam.look_at(Vector3(mid_x, 1.35, 0.15), Vector3.UP)
	_fill.visible = false
	_save(await _one_frame(), "overview.png")
	_set_reflect_cards(true)
	(_doors["pocket"] as MechDoor).set_locked(false)
	for id2 in _doors.keys():
		(_doors[id2] as MechDoor).reset_closed()


func _pose(door: MechDoor, state: String) -> void:
	door.force_q(_q_for(door, state))
	var mode := "closed"
	if state == "open":
		mode = "open"
	elif state == "025" or state == "050" or state == "closing":
		mode = "moving"
	door._set_lamp(mode, true)


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


func _motion_pack() -> void:
	for id in HEROES:
		if not _doors.has(id):
			continue
		var door: MechDoor = _doors[id]
		for other in _doors.keys():
			(_doors[other] as MechDoor).reset_closed()
		await _motion_strip(door, id)
		_curve_png(door, id)
		door.reset_closed()


func _motion_strip(door: MechDoor, id: String) -> void:
	var marks: Array = _strip_marks(door)
	_place(door, "hero")
	var cells: Array = []
	for mark in marks:
		var row: Dictionary = mark
		door.force_q(float(row["q"]))
		door._set_lamp(str(row["lamp"]), true)
		cells.append(await _one_frame())
	var cell_w := 480
	var cell_h := 270
	var strip := Image.create(cell_w * cells.size(), cell_h + 16, false, Image.FORMAT_RGBA8)
	strip.fill(Color(0.07, 0.08, 0.09))
	for i in cells.size():
		var src: Image = cells[i]
		var scaled := src.duplicate()
		scaled.resize(cell_w, cell_h, Image.INTERPOLATE_LANCZOS)
		strip.blit_rect(scaled, Rect2i(0, 0, cell_w, cell_h), Vector2i(i * cell_w, 0))
		_stamp(strip, str(marks[i]["label"]), i * cell_w + 6, cell_h + 3, Color(0.92, 0.93, 0.94))
	_save(strip, "%s_motion_strip.png" % id)


func _strip_marks(door: MechDoor) -> Array:
	var prof := door.profile
	var lurch := prof.phase_span("open", "lurch")
	var lurch_t := (lurch.x + lurch.y) * 0.5 if lurch.x >= 0.0 else 0.02
	var settle := prof.phase_span("close", "settle")
	var settle_t := (settle.x + settle.y) * 0.5 if settle.x >= 0.0 else prof.close_duration
	return [
		{"label": "closed", "q": float(prof.sample("open", 0.0)["q"]), "lamp": "closed"},
		{"label": "lurch", "q": float(prof.sample("open", lurch_t)["q"]), "lamp": "moving"},
		{"label": "25%", "q": _q_at_frac(prof, "open", 0.25), "lamp": "moving"},
		{"label": "50%", "q": _q_at_frac(prof, "open", 0.50), "lamp": "moving"},
		{"label": "75%", "q": _q_at_frac(prof, "open", 0.75), "lamp": "moving"},
		{"label": "open", "q": float(prof.sample("open", prof.open_duration)["q"]), "lamp": "open"},
		{"label": "close", "q": _q_at_frac(prof, "close", 0.50), "lamp": "moving"},
		{"label": "settle", "q": float(prof.sample("close", settle_t)["q"]), "lamp": "closed"},
	]


func _q_at_frac(prof: MechDoorProfile, direction: String, frac: float) -> float:
	var target := prof.travel * frac
	if direction == "close":
		target = prof.travel * (1.0 - frac)
	var dur := prof.duration(direction)
	var best_t := 0.0
	var best_d := 1.0e9
	var steps := 80
	for i in steps + 1:
		var t := dur * float(i) / float(steps)
		var q := float(prof.sample(direction, t)["q"])
		var d := absf(q - target)
		if d < best_d:
			best_d = d
			best_t = t
	return float(prof.sample(direction, best_t)["q"])


func _curve_png(door: MechDoor, id: String) -> void:
	var prof := door.profile
	var open_d := prof.open_duration
	var close_d := prof.close_duration
	var total := maxf(open_d + close_d, 0.1)
	var pts: Array = []
	var phases: Array = []
	var prev := ""
	var q_min := 0.0
	var q_max := 0.001
	var v_min := 0.0
	var v_max := 0.001
	var steps := 240
	for i in steps + 1:
		var t := total * float(i) / float(steps)
		var direction := "open" if t <= open_d else "close"
		var local_t := t if direction == "open" else t - open_d
		var s: Dictionary = prof.sample(direction, local_t)
		var q := float(s["q"])
		var v := float(s["vel"])
		var phase := str(s["phase"])
		pts.append({"t": t, "q": q, "v": v})
		q_min = minf(q_min, q)
		q_max = maxf(q_max, q)
		v_min = minf(v_min, v)
		v_max = maxf(v_max, v)
		if phase != prev:
			phases.append({"t": t, "name": phase})
			prev = phase
	if absf(q_max - q_min) < 1.0e-4:
		q_max = q_min + 1.0
	if absf(v_max - v_min) < 1.0e-4:
		v_max = v_min + 1.0
	var unit := "m" if door.profile.clear_model == "slide" else "deg"
	var img := Image.create(960, 520, false, Image.FORMAT_RGBA8)
	img.fill(Color(0.96, 0.95, 0.93))
	_plot_band(img, pts, phases, "q", q_min, q_max, 72, 36, 940, 230, Color(0.10, 0.35, 0.55))
	_plot_band(img, pts, phases, "v", v_min, v_max, 72, 280, 940, 490, Color(0.62, 0.28, 0.08))
	_stamp(img, "%s pos (%s)" % [id, unit], 72, 8, Color(0.1, 0.2, 0.3), 2)
	_stamp(img, "%s vel (%s/s)" % [id, unit], 72, 252, Color(0.35, 0.15, 0.05), 2)
	_save(img, "%s_curve.png" % id)


func _plot_band(img: Image, pts: Array, phases: Array, key: String, lo: float, hi: float, left: int, top: int, right: int, bottom: int, color: Color) -> void:
	var span := maxf(hi - lo, 1.0e-6)
	var t_max := float(pts[pts.size() - 1]["t"])
	_rect(img, left, top, right, bottom, Color(0.15, 0.15, 0.16))
	for tick in 5:
		var u := float(tick) / 4.0
		var x := int(lerpf(float(left), float(right), u))
		var y := int(lerpf(float(bottom), float(top), u))
		_rect(img, x, bottom, x + 1, bottom + 4, Color(0.15, 0.15, 0.16))
		_rect(img, left - 4, y, left, y + 1, Color(0.15, 0.15, 0.16))
		_stamp(img, "%.2f" % (u * t_max), x - 12, bottom + 6, Color(0.2, 0.2, 0.2), 2)
		_stamp(img, "%.2f" % (lo + u * span), 4, y - 6, Color(0.2, 0.2, 0.2), 2)
	var last_x := -100
	for ph in phases:
		var row: Dictionary = ph
		var x := int(lerpf(float(left), float(right), float(row["t"]) / t_max))
		_rect(img, x, top, x + 1, bottom, Color(0.75, 0.68, 0.55))
		if x - last_x < 44:
			continue
		last_x = x
		_stamp(img, str(row["name"]).substr(0, 6), x + 2, top + 2, Color(0.35, 0.28, 0.16), 2)
	var prev := Vector2i(left, bottom)
	var any := false
	for p in pts:
		var row2: Dictionary = p
		var x2 := int(lerpf(float(left), float(right), float(row2["t"]) / t_max))
		var y2 := int(lerpf(float(bottom), float(top), (float(row2[key]) - lo) / span))
		var here := Vector2i(x2, y2)
		if any:
			_line(img, prev, here, color)
		prev = here
		any = true


func _rect(img: Image, x0: int, y0: int, x1: int, y1: int, color: Color) -> void:
	var xa := mini(x0, x1)
	var xb := maxi(x0, x1)
	var ya := mini(y0, y1)
	var yb := maxi(y0, y1)
	xa = clampi(xa, 0, img.get_width() - 1)
	xb = clampi(xb, 0, img.get_width())
	ya = clampi(ya, 0, img.get_height() - 1)
	yb = clampi(yb, 0, img.get_height())
	if xb <= xa or yb <= ya:
		return
	img.fill_rect(Rect2i(xa, ya, xb - xa, maxi(yb - ya, 1)), color)


func _line(img: Image, a: Vector2i, b: Vector2i, color: Color) -> void:
	var steps := maxi(absi(b.x - a.x), absi(b.y - a.y))
	steps = maxi(steps, 1)
	for i in steps + 1:
		var u := float(i) / float(steps)
		var x := int(lerpf(float(a.x), float(b.x), u))
		var y := int(lerpf(float(a.y), float(b.y), u))
		if x >= 0 and y >= 0 and x < img.get_width() and y < img.get_height():
			img.set_pixel(x, y, color)
			if x + 1 < img.get_width():
				img.set_pixel(x + 1, y, color)


func _stamp(img: Image, text: String, x: int, y: int, color: Color, scale: int = 1) -> void:
	var glyphs := {
		"0": "111101101101111", "1": "010010010010010", "2": "111001111100111",
		"3": "111001111001111", "4": "101101111001001", "5": "111100111001111",
		"6": "111100111101111", "7": "111001001001001", "8": "111101111101111",
		"9": "111101111001111", ".": "000000000000010", "-": "000000111000000",
		"a": "000111101111101", "b": "110110111110110", "c": "011100100100011",
		"d": "110101101101110", "e": "111100111100111", "f": "111100111100100",
		"g": "011100101101011", "h": "101101111101101", "i": "111010010010111",
		"k": "101101110101101", "l": "100100100100111", "m": "000110111101101",
		"n": "000110101101101", "o": "000111101101111", "p": "111101111100100",
		"q": "011101101011001", "r": "000110100100100", "s": "011100010001110",
		"t": "111010010010010", "u": "000101101101011", "v": "000101101101010",
		"w": "000101101111010", "y": "101101011001001", " ": "000000000000000",
		"%": "101000010001101", "/": "001001010100100", "(": "001010100100001",
		")": "100001001001100",
	}
	var cursor := x
	for i in text.length():
		var ch := text.substr(i, 1).to_lower()
		var bits: String = glyphs.get(ch, "000000000000000")
		for row in 5:
			for col in 3:
				if bits.substr(row * 3 + col, 1) == "1":
					var px := cursor + col * scale
					var py := y + row * scale
					for sy in scale:
						for sx in scale:
							var qx := px + sx
							var qy := py + sy
							if qx >= 0 and qy >= 0 and qx < img.get_width() and qy < img.get_height():
								img.set_pixel(qx, qy, color)
		cursor += 4 * scale


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
	if _fill != null:
		_fill.visible = cam_name == "detail" or cam_name == "jamb"


func _cam_spec(door: MechDoor, cam_name: String) -> Dictionary:
	var origin := door.global_position
	var cx := origin.x + float(door.get_meta("walk_x", 0.0))
	var dz := origin.z
	var look_y: float = 1.05 if door.door_id == "hatch" else 1.15
	if door.door_id == "floorhatch":
		look_y = 0.15
	var look := Vector3(cx, look_y, dz + (0.45 if door.door_id == "floorhatch" else 0.0))
	var inset := 0.55
	if door.door_id == "bay3":
		inset = 0.90
	elif door.door_id == "pair":
		inset = 0.42
	elif door.door_id == "hatch":
		inset = 0.28
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
		"jamb":
			# Outside the frame. Bay3's canopy swallows a camera at z = -1.15.
			at = Vector3(cx - inset - 0.55, 1.22, dz - 1.75)
			look = Vector3(cx - inset, 1.15, dz - 0.04)
			fov = 32.0
		"detail":
			at = Vector3(cx - inset * 0.55, 1.28, dz - 1.70)
			look = Vector3(cx - inset * 0.15, 1.20, dz - 0.02)
			fov = 28.0
		"top":
			at = Vector3(cx, look_y + 4.0, dz - 0.40)
			look = Vector3(cx, look_y, dz - 0.15)
			fov = 40.0
			up = Vector3(0.0, 0.0, -1.0)
		"player":
			at = Vector3(cx, 1.62, dz - 1.8)
			fov = 70.0
		"hero":
			if door.door_id == "floorhatch":
				# The plate sits on +Z. High enough to see the whole rim without a grazing angle.
				at = Vector3(cx + 0.15, 2.55, dz + 2.35)
				look = Vector3(cx, 0.06, dz + 0.48)
				fov = 42.0
			elif door.door_id == "hatch":
				at = Vector3(cx + sin(ang30) * 2.35, 1.32, dz - cos(ang30) * 2.35)
				look = Vector3(cx - 0.05, 1.12, dz + 0.02)
				fov = 40.0
			else:
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


func _set_reflect_cards(on: bool) -> void:
	var stack: Array[Node] = [_lab]
	while not stack.is_empty():
		var n: Node = stack.pop_back()
		for c in n.get_children():
			stack.append(c)
		if String(n.name).begins_with("ReflectCard") and n is MeshInstance3D:
			(n as MeshInstance3D).visible = on


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
	var score := _mean_luma(img, _leaf_rect(img))
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
		var luma_ok: bool = luma >= 0.25
		var shadow_ok: bool = shadow <= (2.0 / 255.0) + 1.0e-5 and shadow_hot == 0
		var flicker_ok: bool = flicker <= (2.0 / 255.0) + 1.0e-5 and flicker_hot == 0
		print("[door_lab] %s V-LUMA %s measured=%.4f limit=0.25" % [id, "PASS" if luma_ok else "FAIL", luma])
		print("[door_lab] %s V-SHADOW %s measured=%.5f hot=%d limit=0.00784" % [id, "PASS" if shadow_ok else "FAIL", shadow, shadow_hot])
		print("[door_lab] %s V-ZFIGHT-FLICKER %s measured=%.5f hot=%d limit=0.00784" % [id, "PASS" if flicker_ok else "FAIL", flicker, flicker_hot])
		var path := _out.path_join(id).path_join("metrics.json")
		var metrics: Array = _load_array(path)
		_upsert(metrics, "V-LUMA", luma_ok, luma, 0.25, "1", "leaf-face mean, Sloane A and front, closed and open")
		_upsert(metrics, "V-SHADOW", shadow_ok, shadow, 2.0 / 255.0, "1", "leaf-face mean |d| hot %d" % shadow_hot)
		_upsert(metrics, "V-ZFIGHT-FLICKER", flicker_ok, flicker, 2.0 / 255.0, "1", "seam band mean |d| hot %d" % flicker_hot)
		_store(path, metrics)
		if not luma_ok or not shadow_ok or not flicker_ok:
			_vis_fail += 1
		if not _rest_visual_ok(metrics):
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
	var bin := _python_bin()
	var code := OS.execute(bin, PackedStringArray([script, _out]), output, true)
	print("[door_lab] contact_sheet %s exit=%d %s" % [bin, code, str(output)])


func _python_bin() -> String:
	for bin in ["python3", "python"]:
		var output: Array = []
		var code := OS.execute(bin, PackedStringArray(["-c", "import sys"]), output, true)
		if code == 0:
			return bin
	return "python3"


func _mirror_pngs() -> void:
	var dest := ""
	var args := OS.get_cmdline_user_args()
	for i in args.size():
		if args[i] == "--qa-door-lab-mirror" and i + 1 < args.size():
			dest = str(args[i + 1])
	if dest == "":
		return
	if not DirAccess.dir_exists_absolute(dest):
		print("[door_lab] mirror skip, absent %s" % dest)
		return
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
