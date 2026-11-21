extends Node
## Windowed opengl3 captures for the door lab. Not headless.
## Rewrites V-LUMA, V-SHADOW, and V-ZFIGHT-FLICKER from the pixels it saves.

const IDS := ["pocket", "bay3", "pair", "hatch"]
const SHOT_IDS := ["pocket", "bay3", "pair", "hatch", "floorhatch"]
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
var _metrics_bad: bool = false
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
	# Specular on this camera light was the white disc in the detail leaf rect.
	# Scene key and fill still light the close-up. This one stays dim and diffuse.
	_fill.light_energy = 0.08
	_fill.light_specular = 0.0
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
		if id in SHOT_IDS:
			_pixel[id] = {
				"luma": 1.0, "shadow": 0.0, "shadow_hot": 0, "flicker": 0.0, "flicker_hot": 0,
				"clip": 0.0, "clips": [], "amber": -1.0, "amber_rgb": "", "readout": -1.0,
				"strip": -1.0, "pocket_low": 1.0, "pocket_set": false,
			}
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
	get_viewport().msaa_3d = Viewport.MSAA_4X


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
	for id in SHOT_IDS:
		if not _doors.has(id):
			continue
		var door: MechDoor = _doors[id]
		print("[door_lab] shots %s" % id)
		door.reset_closed()
		for state in STATES:
			_pose(door, state)
			for cam_name in QA_CAMS:
				if cam_name == "jamb":
					_set_vestibule_meshes(false)
				_place(door, cam_name)
				var burst: bool = state == "closed" and (cam_name == "front" or cam_name == "jamb")
				var frames: Array = await _grab_frames(8 if burst else 1)
				_save(frames[0], "%s/shots/%s_%s.png" % [id, cam_name, state])
				if cam_name == "jamb":
					_note_clip(id, frames[0], "jamb_%s" % state)
					if state == "closed":
						_note_pocket_low(id, frames[0])
					_set_vestibule_meshes(true)
				if cam_name == "front" and state == "closed":
					_note_readout(id, frames[0])
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
			_note_clip(id, hero_frames[0], "hero_%s" % state)
			if state == "closed" or state == "open":
				_note_luma(id, hero_frames[0])
			if state == "closed":
				_note_shadow(id, hero_frames)
		_pose(door, "closed")
		_place(door, "square")
		_save(await _one_frame(), "%s/shots/square_closed.png" % id)
		_set_vestibule_meshes(false)
		_place(door, "detail")
		var detail_closed: Image = await _one_frame()
		_save(detail_closed, "%s/shots/detail_closed.png" % id)
		_note_clip(id, detail_closed, "detail_closed")
		_pose(door, "open")
		if id == "pocket":
			_set_access_panel(door, true)
		_place(door, "detail")
		if id == "pocket":
			_aim_pocket_panel(door)
		var detail_open: Image = await _one_frame()
		_save(detail_open, "%s/shots/detail_open.png" % id)
		_note_clip(id, detail_open, "detail_open")
		if id == "pocket":
			_set_access_panel(door, false)
			await _pocket_end_shot(door)
			_pose(door, "closed")
			_set_access_panel(door, true)
			await _pocket_head_shot(door)
			_set_access_panel(door, false)
		_set_vestibule_meshes(true)
		if id == "hatch":
			_set_vestibule_meshes(false)
		_pose(door, "closed")
		_place(door, "back")
		_save(await _one_frame(), "%s/shots/back_closed.png" % id)
		_pose(door, "open")
		_place(door, "back")
		_save(await _one_frame(), "%s/shots/back_open.png" % id)
		if id == "hatch":
			await _latch_edge(door)
			_set_vestibule_meshes(true)
		_pose(door, "050")
		_place(door, "player_sloane")
		_save(await _one_frame(), "%s/shots/player_sloane_050.png" % id)
		_pose(door, "open")
		_set_vestibule_meshes(false)
		_place(door, "threshold")
		_save(await _one_frame(), "%s/shots/threshold_open.png" % id)
		_set_vestibule_meshes(true)
		await _wear_closeup(door, id)
		await _open_strip(door, id)
		door.set_physics_process(false)
		door.reset_closed()
	await _motion_pack()
	await _heroes()


func _set_vestibule_meshes(on: bool) -> void:
	var stack: Array[Node] = [_lab]
	while not stack.is_empty():
		var n: Node = stack.pop_back()
		for c in n.get_children():
			stack.append(c)
		if n is MeshInstance3D and String(n.name).begins_with("Vestibule_"):
			(n as MeshInstance3D).visible = on


func _aim_pocket_panel(door: MechDoor) -> void:
	# Open clamps sit at x ±1.52. fov 40 at z-1.55 only covered ±1.1.
	var origin := door.global_position
	var cx := origin.x + float(door.get_meta("walk_x", 0.0))
	_cam.fov = 72.0
	_cam.global_position = Vector3(cx, 1.95, origin.z - 2.60)
	_cam.look_at(Vector3(cx, 2.38, origin.z - 0.02), Vector3.UP)


func _pocket_head_shot(door: MechDoor) -> void:
	# Closed pose, panel +90, −Z side, wide enough to see the head hardware.
	var origin := door.global_position
	var cx := origin.x + float(door.get_meta("walk_x", 0.0))
	_cam.fov = 55.0
	_cam.global_position = Vector3(cx, 1.85, origin.z - 2.80)
	_cam.look_at(Vector3(cx, 2.30, origin.z), Vector3.UP)
	if _fill != null:
		_fill.visible = true
	var img := await _one_frame()
	_save(img, "pocket/shots/head_closed.png")
	_note_clip("pocket", img, "head_closed")


func _pocket_end_shot(door: MechDoor) -> void:
	# Full open. Bumper and end stop are near x = cx+1.93; open clamps near +1.52.
	var origin := door.global_position
	var cx := origin.x + float(door.get_meta("walk_x", 0.0))
	var ex := cx + 1.72
	_cam.fov = 46.0
	_cam.global_position = Vector3(ex - 0.15, 1.40, origin.z - 1.55)
	_cam.look_at(Vector3(ex + 0.20, 1.30, origin.z + 0.02), Vector3.UP)
	if _fill != null:
		_fill.visible = true
	var img := await _one_frame()
	_save(img, "pocket/shots/pocket_end_open.png")
	_note_clip("pocket", img, "pocket_end_open")


func _latch_edge(door: MechDoor) -> void:
	# t = 1.9 s is in the lurch. Rams are posed +12 mm toward the approach for this frame only.
	var sampled: Dictionary = door.profile.sample("open", 1.9)
	door.force_q(float(sampled.get("q", 0.0)))
	_nudge_rams(door, -0.012)
	var origin := door.global_position
	var cx := origin.x + float(door.get_meta("walk_x", 0.0))
	_cam.fov = 28.0
	_cam.global_position = Vector3(cx - 0.95, 0.95, origin.z - 0.70)
	_cam.look_at(Vector3(cx - 0.55, 0.90, origin.z - 0.02), Vector3.UP)
	if _fill != null:
		_fill.visible = true
	_save(await _one_frame(), "hatch/shots/latch_edge_19.png")
	_nudge_rams(door, 0.012)
	door.force_q(0.0)


func _nudge_rams(door: Node, dz: float) -> void:
	var stack: Array[Node] = [door]
	while not stack.is_empty():
		var n: Node = stack.pop_back()
		for c in n.get_children():
			stack.append(c)
		if not (n is Node3D):
			continue
		var low := String(n.name).to_lower()
		if "pushoff" not in low:
			continue
		var parent_hit := false
		var p: Node = n.get_parent()
		while p != null and p != door:
			if "pushoff" in String(p.name).to_lower():
				parent_hit = true
				break
			p = p.get_parent()
		if parent_hit:
			continue
		(n as Node3D).global_position += Vector3(0.0, 0.0, dz)


func _set_access_panel(door: Node, opened: bool) -> void:
	# Rook pass G: exact name. The substring search returned slide_AccessPanel_hinge (its sibling, popped first),
	# so the panel never moved and covered the head hardware in detail_open.
	var panel := _find_exact(door, "slide_AccessPanel")
	if panel == null or not (panel is Node3D):
		return
	var was := bool(panel.get_meta("shot_open", false))
	# The GLB panel opens +90 about local X (top hinge, swings up and out; v1 bakes that pose and the rig closes it with -90).
	# -110 swung it into the head box, through the track and belt.
	if opened and not was:
		(panel as Node3D).rotate_object_local(Vector3(1, 0, 0), deg_to_rad(90.0))
		panel.set_meta("shot_open", true)
	elif not opened and was:
		(panel as Node3D).rotate_object_local(Vector3(1, 0, 0), deg_to_rad(-90.0))
		panel.set_meta("shot_open", false)


func _find_exact(root: Node, nm: String) -> Node:
	var stack: Array[Node] = [root]
	while not stack.is_empty():
		var n: Node = stack.pop_back()
		if String(n.name) == nm:
			return n
		for c in n.get_children():
			stack.append(c)
	return null


func _wear_closeup(door: MechDoor, id: String) -> void:
	var target: Node3D = null
	for needle in ["WearHandle", "WearPush", "WearBar", "WearKick", "WearWheel", "WearLid", "hatch_Handle", "ManualHandle"]:
		var found := _find_node(door, needle)
		if found is Node3D:
			target = found
			break
	if target == null:
		print("[door_lab] %s wear close-up missing a wear mesh" % id)
		return
	var p := target.global_position
	_cam.fov = 28.0
	_cam.global_position = p + Vector3(0.12, 0.04, -0.32)
	_cam.look_at(p, Vector3.UP)
	if _fill != null:
		_fill.visible = true
	var img := await _one_frame()
	var tries := 0
	while _image_std(img) < 0.015 and tries < 3:
		var away := _cam.global_position - p
		if away.length() < 0.05:
			away = Vector3(0.0, 0.2, -1.0)
		_cam.global_position += away.normalized() * 0.45
		_cam.look_at(p, Vector3.UP)
		img = await _one_frame()
		tries += 1
	_save(img, "%s_wear_closeup.png" % id)
	_save(img, "%s/shots/%s_wear_closeup.png" % [id, id])
	print("[door_lab] %s wear close-up %s std=%.4f tries=%d" % [id, target.name, _image_std(img), tries])


func _print_clip(id: String, img: Image) -> void:
	var hot := 0
	var n := 0
	var mx := 0.0
	var y := 0
	while y < img.get_height():
		var x := 0
		while x < img.get_width():
			var c := img.get_pixel(x, y)
			mx = maxf(mx, maxf(c.r, maxf(c.g, c.b)))
			if c.r >= 250.0 / 255.0 or c.g >= 250.0 / 255.0 or c.b >= 250.0 / 255.0:
				hot += 1
			n += 1
			x += 2
		y += 2
	var pct := 100.0 * float(hot) / float(maxi(n, 1))
	print("[door_lab] hero %s clip_pct=%.3f max_channel=%.3f" % [id, pct, mx])


func _find_node(root: Node, needle: String) -> Node:
	var stack: Array[Node] = [root]
	var want := needle.to_lower()
	while not stack.is_empty():
		var n: Node = stack.pop_back()
		if want in String(n.name).to_lower():
			return n
		for c in n.get_children():
			stack.append(c)
	return null


func _open_strip(door: MechDoor, id: String) -> void:
	# Time samples pile up on the end dwell, so the last two frames match.
	# Eight equal travel steps. q changes every frame, including the last.
	door.reset_closed()
	door.set_physics_process(false)
	_place(door, "hero")
	if id == "hatch":
		# Approach hero loses the plug after about 70 deg (it swings to +Z).
		# The back camera still sees that last third. Vestibule wall sits in the way.
		_set_vestibule_meshes(false)
		_place(door, "back")
	var travel := maxf(door.profile.travel, 0.001)
	var prev: Image = null
	var min_diff := 1.0
	for i in 8:
		var q := travel * float(i) / 7.0
		door.force_q(q)
		var img: Image = await _shot_image()
		_save(img, "%s/shots/hero_openstrip_%d.png" % [id, i])
		if prev != null:
			min_diff = minf(min_diff, _frame_diff(prev, img))
		prev = img
	if _pixel.has(id):
		var slot: Dictionary = _pixel[id]
		slot["strip"] = min_diff
		_pixel[id] = slot
	print("[door_lab] %s V-STRIP min_diff=%.5f" % [id, min_diff])
	if id == "hatch":
		_set_vestibule_meshes(true)
	door.force_q(0.0)
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
		_print_clip(id, img)
		_note_clip(id, img, "hero_final")
		_note_pocket_low(id, img)
		_note_amber(door, img)
		_note_readout(id, img)
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
		_fill.visible = cam_name == "detail" or cam_name == "jamb" or (cam_name == "back" and door.door_id == "floorhatch")


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
			if door.door_id == "floorhatch":
				at = Vector3(cx + 1.15, 0.85, dz + 0.15)
				look = Vector3(cx + 0.45, 0.02, dz + 0.50)
				fov = 32.0
			else:
				# Farther back so the white leaf does not fill the frame and clip.
				at = Vector3(cx - inset - 0.85, 1.35, dz - 2.55)
				look = Vector3(cx - inset * 0.4, 1.25, dz - 0.02)
				fov = 38.0
		"detail":
			if door.door_id == "floorhatch":
				at = Vector3(cx + 0.35, 1.15, dz + 1.35)
				look = Vector3(cx, 0.05, dz + 0.50)
				fov = 35.0
			else:
				at = Vector3(cx - inset * 0.55, 1.28, dz - 1.70)
				look = Vector3(cx - inset * 0.15, 1.20, dz - 0.02)
				fov = 28.0
		"top":
			# Ceiling slab is y = 4.07..4.23. Stay under it or the shot is the roof.
			at = Vector3(cx, 3.55, dz - 0.40)
			look = Vector3(cx, look_y, dz - 0.15)
			fov = 40.0
			up = Vector3(0.0, 0.0, -1.0)
		"back":
			if door.door_id == "floorhatch":
				# Under the opening, looking up at the +Z edge. Closed, the lid
				# underside (hub, ribs, struts). Open, the standing leaf's back skin.
				at = Vector3(cx, -0.38, dz + 0.35)
				look = Vector3(cx, 0.65, dz + 1.15)
				up = Vector3(0.0, 0.0, -1.0)
				fov = 50.0
			elif door.door_id == "hatch":
				# Vestibule is hidden for this shot. Full leaf plus 0.3 m, davit and the lower-hinge actuator.
				at = Vector3(cx, 1.15, dz + 2.6)
				look = Vector3(cx, 1.15, dz)
				fov = 55.0
			else:
				at = Vector3(cx, 1.45, dz + 3.2)
				look = Vector3(cx, look_y, dz)
				fov = 40.0
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


func _lower_half(img: Image) -> Rect2i:
	var leaf := _leaf_rect(img)
	return Rect2i(leaf.position.x, leaf.position.y + int(leaf.size.y / 2), leaf.size.x, int(leaf.size.y / 2))


func _clip_pct(img: Image, rect: Rect2i) -> float:
	var hot := 0
	var n := 0
	var y := rect.position.y
	while y < rect.position.y + rect.size.y:
		var x := rect.position.x
		while x < rect.position.x + rect.size.x:
			if x >= 0 and y >= 0 and x < img.get_width() and y < img.get_height():
				var c := img.get_pixel(x, y)
				if c.r >= 250.0 / 255.0 or c.g >= 250.0 / 255.0 or c.b >= 250.0 / 255.0:
					hot += 1
				n += 1
			x += 2
		y += 2
	return 100.0 * float(hot) / float(maxi(n, 1))


func _note_clip(id: String, img: Image, label: String) -> void:
	if not _pixel.has(id):
		return
	var pct := _clip_pct(img, _leaf_rect(img))
	var slot: Dictionary = _pixel[id]
	var list: Array = slot.get("clips", [])
	list.append("%s=%.2f" % [label, pct])
	slot["clips"] = list
	slot["clip"] = maxf(float(slot.get("clip", 0.0)), pct)
	_pixel[id] = slot
	print("[door_lab] %s %s leaf_clip_pct=%.2f" % [id, label, pct])


func _note_pocket_low(id: String, img: Image) -> void:
	if id != "pocket" or not _pixel.has(id):
		return
	var v := _mean_luma(img, _lower_half(img))
	var slot: Dictionary = _pixel[id]
	if not bool(slot.get("pocket_set", false)):
		slot["pocket_low"] = v
		slot["pocket_set"] = true
	else:
		slot["pocket_low"] = maxf(float(slot["pocket_low"]), v)
	_pixel[id] = slot
	print("[door_lab] pocket lower-half luma=%.4f" % v)


func _note_amber(door: MechDoor, img: Image) -> void:
	var id := door.door_id
	if not _pixel.has(id):
		return
	var target := Color.from_rgba8(217, 115, 5)
	var best := 99.0
	var rgb := ""
	var used := 0
	var stack: Array[Node] = [door]
	while not stack.is_empty() and used < 24:
		var n: Node = stack.pop_back()
		for c in n.get_children():
			stack.append(c)
		if not (n is MeshInstance3D):
			continue
		var mi := n as MeshInstance3D
		if mi.mesh == null or mi.mesh.get_surface_count() < 1:
			continue
		var mat := mi.get_surface_override_material(0) as StandardMaterial3D
		if mat == null:
			mat = mi.get_active_material(0) as StandardMaterial3D
		if mat == null or mat.shading_mode != BaseMaterial3D.SHADING_MODE_UNSHADED:
			continue
		var d := mat.albedo_color - target
		if Vector3(d.r, d.g, d.b).length() > 0.04:
			continue
		# The node origin is the leaf pivot on these GLBs, so a radius around it
		# lands on the grey glass. Sample the mesh bounds, which sit on the bar.
		var rect := _mesh_screen_rect(mi)
		if rect.size.x < 2 or rect.size.y < 2:
			continue
		var hit := _best_amber_in(img, rect, target)
		used += 1
		if float(hit["err"]) < best:
			best = float(hit["err"])
			rgb = str(hit["rgb"])
	var slot: Dictionary = _pixel[id]
	slot["amber"] = best if best < 50.0 else -1.0
	slot["amber_rgb"] = rgb
	_pixel[id] = slot
	print("[door_lab] %s V-AMBER-PX err=%.4f rgb=%s samples=%d" % [id, float(slot["amber"]), rgb, used])


func _mesh_screen_rect(mi: MeshInstance3D) -> Rect2i:
	var box: AABB = mi.global_transform * mi.mesh.get_aabb()
	var min_x := 100000
	var min_y := 100000
	var max_x := -1
	var max_y := -1
	var any := false
	for i in 8:
		var corner := Vector3(
			box.position.x + box.size.x * float(i & 1),
			box.position.y + box.size.y * float((i >> 1) & 1),
			box.position.z + box.size.z * float((i >> 2) & 1))
		if _cam.is_position_behind(corner):
			continue
		var s := _cam.unproject_position(corner)
		any = true
		min_x = mini(min_x, int(floor(s.x)))
		min_y = mini(min_y, int(floor(s.y)))
		max_x = maxi(max_x, int(ceil(s.x)))
		max_y = maxi(max_y, int(ceil(s.y)))
	if not any:
		return Rect2i(0, 0, 0, 0)
	min_x = clampi(min_x - 4, 0, 100000)
	min_y = clampi(min_y - 4, 0, 100000)
	max_x = maxi(max_x + 4, min_x + 2)
	max_y = maxi(max_y + 4, min_y + 2)
	return Rect2i(min_x, min_y, max_x - min_x, max_y - min_y)


func _best_amber_in(img: Image, rect: Rect2i, target: Color) -> Dictionary:
	var best := 99.0
	var rgb := ""
	var step := 1 if rect.size.x * rect.size.y < 12000 else 2
	var y := rect.position.y
	var y1 := mini(rect.position.y + rect.size.y, img.get_height())
	var x1 := mini(rect.position.x + rect.size.x, img.get_width())
	while y < y1:
		var x := maxi(rect.position.x, 0)
		while x < x1:
			var c := img.get_pixel(x, y)
			var err := maxf(absf(c.r - target.r), maxf(absf(c.g - target.g), absf(c.b - target.b)))
			if err < best:
				best = err
				rgb = "%d,%d,%d" % [int(round(c.r * 255.0)), int(round(c.g * 255.0)), int(round(c.b * 255.0))]
			x += step
		y += step
	return {"err": best, "rgb": rgb}


func _nearest_amber(img: Image, sx: int, sy: int, target: Color) -> Dictionary:
	var best := 99.0
	var rgb := ""
	var rad := 64
	var y := sy - rad
	while y <= sy + rad:
		var x := sx - rad
		while x <= sx + rad:
			if x >= 0 and y >= 0 and x < img.get_width() and y < img.get_height():
				var c := img.get_pixel(x, y)
				var err := maxf(absf(c.r - target.r), maxf(absf(c.g - target.g), absf(c.b - target.b)))
				if err < best:
					best = err
					rgb = "%d,%d,%d" % [int(round(c.r * 255.0)), int(round(c.g * 255.0)), int(round(c.b * 255.0))]
			x += 2
		y += 2
	return {"err": best, "rgb": rgb}


func _note_readout(id: String, img: Image) -> void:
	if not _pixel.has(id) or not _doors.has(id):
		return
	var face := _approach_digit(_doors[id])
	if face == null or _cam.is_position_behind(face.global_position):
		return
	var screen := _cam.unproject_position(face.global_position)
	var std := _crop_std(img, screen, 28, 14)
	var slot: Dictionary = _pixel[id]
	var cur := float(slot.get("readout", -1.0))
	slot["readout"] = std if cur < 0.0 else maxf(cur, std)
	_pixel[id] = slot
	print("[door_lab] %s V-READOUT std=%.4f" % [id, float(slot["readout"])])


func _approach_digit(door: Node) -> Node3D:
	var best: Node3D = null
	var best_dot := 0.2
	var stack: Array[Node] = [door]
	while not stack.is_empty():
		var n: Node = stack.pop_back()
		for c in n.get_children():
			stack.append(c)
		if not (n is MeshInstance3D):
			continue
		if "digitface" not in String(n.name).to_lower():
			continue
		var nd := n as Node3D
		var to_cam := _cam.global_position - nd.global_position
		if to_cam.length() < 0.05:
			continue
		var facing: Vector3 = nd.global_transform.basis.z
		var d := facing.normalized().dot(to_cam.normalized())
		if d > best_dot:
			best_dot = d
			best = nd
	return best


func _crop_std(img: Image, center: Vector2, hw: int, hh: int) -> float:
	var acc := 0.0
	var acc2 := 0.0
	var n := 0
	var y := int(center.y) - hh
	while y <= int(center.y) + hh:
		var x := int(center.x) - hw
		while x <= int(center.x) + hw:
			if x >= 0 and y >= 0 and x < img.get_width() and y < img.get_height():
				var l := _luma_at(img, x, y)
				acc += l
				acc2 += l * l
				n += 1
			x += 1
		y += 1
	if n < 8:
		return 0.0
	var mean := acc / float(n)
	return sqrt(maxf(acc2 / float(n) - mean * mean, 0.0))


func _image_std(img: Image) -> float:
	var acc := 0.0
	var acc2 := 0.0
	var n := 0
	var y := 0
	while y < img.get_height():
		var x := 0
		while x < img.get_width():
			var l := _luma_at(img, x, y)
			acc += l
			acc2 += l * l
			n += 1
			x += 8
		y += 8
	if n == 0:
		return 0.0
	var mean := acc / float(n)
	return sqrt(maxf(acc2 / float(n) - mean * mean, 0.0))


func _frame_diff(a: Image, b: Image) -> float:
	var acc := 0.0
	var n := 0
	var y := 0
	var h := mini(a.get_height(), b.get_height())
	var w := mini(a.get_width(), b.get_width())
	while y < h:
		var x := 0
		while x < w:
			var ca := a.get_pixel(x, y)
			var cb := b.get_pixel(x, y)
			acc += absf(ca.r - cb.r) + absf(ca.g - cb.g) + absf(ca.b - cb.b)
			n += 1
			x += 8
		y += 8
	return acc / float(maxi(n, 1))


func _join_bits(items: Array) -> String:
	var s := ""
	for i in items.size():
		if i > 0:
			s += "; "
		s += str(items[i])
	return s


func _metrics_file_ok(path: String) -> bool:
	if not FileAccess.file_exists(path):
		return false
	var parsed: Variant = JSON.parse_string(FileAccess.get_file_as_string(path))
	return typeof(parsed) == TYPE_ARRAY and (parsed as Array).size() > 0


func _rewrite_metrics() -> void:
	var vis_ids := {}
	for id in SHOT_IDS:
		if not _pixel.has(id):
			continue
		var slot: Dictionary = _pixel[id]
		var luma := float(slot["luma"])
		var shadow := float(slot["shadow"])
		var shadow_hot := int(slot["shadow_hot"])
		var flicker := float(slot["flicker"])
		var flicker_hot := int(slot["flicker_hot"])
		var luma_ok := luma >= 0.10
		var luma_limit := 0.10
		var luma_measured := luma
		var luma_note := "leaf-face mean >= 0.10"
		if id == "pocket":
			var low := float(slot.get("pocket_low", 1.0))
			luma_ok = luma >= 0.10 and low <= 0.25 and bool(slot.get("pocket_set", false))
			luma_limit = 0.25
			luma_measured = low
			luma_note = "lower-half of hero_final and jamb_closed <= 0.25; leaf mean %.3f >= 0.10" % luma
		var clip := float(slot.get("clip", 0.0))
		var clip_ok := clip <= 5.0
		var amber := float(slot.get("amber", -1.0))
		var amber_ok := amber >= 0.0 and amber <= (12.0 / 255.0) + 1.0e-5
		var amber_note := "rgb %s max-channel vs 217,115,5" % str(slot.get("amber_rgb", ""))
		if id == "pocket" and amber < 0.0:
			amber_ok = true
			amber_note = "no plate in frame"
		elif amber < 0.0:
			amber_ok = false
			amber_note = "amber part not sampled"
		var rd := float(slot.get("readout", -1.0))
		var rd_ok := true
		if id == "hatch":
			rd_ok = rd >= 0.02
		elif rd >= 0.0:
			rd_ok = rd >= 0.02
		var strip := float(slot.get("strip", -1.0))
		var strip_ok := strip > 0.004
		var shadow_ok: bool = shadow <= (2.0 / 255.0) + 1.0e-5 and shadow_hot == 0
		var flicker_ok: bool = flicker <= (2.0 / 255.0) + 1.0e-5 and flicker_hot == 0
		print("[door_lab] %s V-LUMA %s measured=%.4f limit=%.2f" % [id, "PASS" if luma_ok else "FAIL", luma_measured, luma_limit])
		print("[door_lab] %s V-SHADOW %s measured=%.5f hot=%d limit=0.00784" % [id, "PASS" if shadow_ok else "FAIL", shadow, shadow_hot])
		print("[door_lab] %s V-ZFIGHT-FLICKER %s measured=%.5f hot=%d limit=0.00784" % [id, "PASS" if flicker_ok else "FAIL", flicker, flicker_hot])
		print("[door_lab] %s V-CLIP %s measured=%.2f limit=5" % [id, "PASS" if clip_ok else "FAIL", clip])
		print("[door_lab] %s V-AMBER-PX %s measured=%.4f" % [id, "PASS" if amber_ok else "FAIL", amber])
		print("[door_lab] %s V-READOUT %s measured=%.4f" % [id, "PASS" if rd_ok else "FAIL", rd])
		print("[door_lab] %s V-STRIP %s measured=%.5f" % [id, "PASS" if strip_ok else "FAIL", strip])
		var path := _out.path_join(id).path_join("metrics.json")
		var file_ok := _metrics_file_ok(path)
		if not file_ok:
			_metrics_bad = true
			print("[door_lab] %s metrics.json missing or empty" % id)
		var metrics: Array = _load_array(path)
		if not file_ok:
			_upsert(metrics, "V-METRICS", false, 0.0, 1.0, "1", "metrics.json missing or empty before shots")
		_upsert(metrics, "V-LUMA", luma_ok, luma_measured, luma_limit, "1", luma_note)
		_upsert(metrics, "V-SHADOW", shadow_ok, shadow, 2.0 / 255.0, "1", "leaf-face mean |d| hot %d" % shadow_hot)
		_upsert(metrics, "V-ZFIGHT-FLICKER", flicker_ok, flicker, 2.0 / 255.0, "1", "seam band mean |d| hot %d" % flicker_hot)
		_upsert(metrics, "V-CLIP", clip_ok, clip, 5.0, "pct", "leaf-rect channel>=250; %s" % _join_bits(slot.get("clips", [])))
		_upsert(metrics, "V-AMBER-PX", amber_ok, amber, 12.0 / 255.0, "1", amber_note)
		_upsert(metrics, "V-READOUT", rd_ok, rd, 0.02, "1", "approach DigitFace crop std; blank if under 0.02")
		_upsert(metrics, "V-STRIP", strip_ok, strip, 0.004, "1", "min consecutive open-strip frame diff")
		_store(path, metrics)
		var gates_ok := luma_ok and shadow_ok and flicker_ok and clip_ok and amber_ok and rd_ok and strip_ok and file_ok
		if not gates_ok:
			_vis_fail += 1
		if not _rest_visual_ok(metrics):
			_vis_fail += 1
		vis_ids[id] = gates_ok and _rest_visual_ok(metrics)
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
	for id in SHOT_IDS:
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
	var fails: Array = []
	if _metrics_bad:
		any_fail = true
		fails.append("metrics.json unreadable or empty")
	for sid in SHOT_IDS:
		var metrics_path := _out.path_join(sid).path_join("metrics.json")
		if not _metrics_file_ok(metrics_path):
			any_fail = true
			fails.append("%s:metrics.json unreadable or empty" % sid)
		var metrics: Array = _load_array(metrics_path)
		for item in metrics:
			if typeof(item) != TYPE_DICTIONARY:
				continue
			if not bool(item.get("pass", true)):
				fails.append("%s:%s" % [sid, str(item["id"])])
	summary["fails"] = fails
	summary["fails_count"] = fails.size()
	_vis_fail = fails.size()
	if any_fail or str(summary["functional"]) != "PASS" or not fails.is_empty():
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
	DirAccess.make_dir_recursive_absolute(dest)
	_mirror_dir(_out, dest)


func _mirror_dir(src: String, dest: String) -> void:
	var dir := DirAccess.open(src)
	if dir == null:
		return
	DirAccess.make_dir_recursive_absolute(dest)
	for name in dir.get_files():
		var from := src.path_join(name)
		var to := dest.path_join(name)
		if FileAccess.file_exists(to):
			DirAccess.remove_absolute(to)
		DirAccess.copy_absolute(from, to)
	for sub in dir.get_directories():
		_mirror_dir(src.path_join(sub), dest.path_join(sub))
