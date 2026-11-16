extends Node
## Windowed QA stills for the tower safety pass. Shipped lighting plus one
## unshadowed fill OmniLight parented to the camera.

const GUARD_JSON := "res://scripts/tennis_tower_fixes/tt_guard_rails.json"
const OUT_DIR := "C:/Users/upchu/aegis_shots/ttfix_A"

var ppa: PrefacePlayableArea
var _failures: int = 0


func _ready() -> void:
	_run.call_deferred()


func _run() -> void:
	var guard: int = 0
	while (ppa == null or not ppa.has_meta("exterior_spawned")) and guard < 4000:
		await get_tree().physics_frame
		guard += 1
	if ppa == null or ppa._player_body == null or ppa._tower == null or ppa._camera == null:
		print("[TT-SHOT] FAIL setup")
		get_tree().quit(1)
		return
	if DisplayServer.get_name() != "headless":
		DisplayServer.window_set_mode(DisplayServer.WINDOW_MODE_WINDOWED)
		DisplayServer.window_set_size(Vector2i(1280, 720))
	if ppa._hud != null:
		ppa._hud.visible = false
	ppa._third_person = false
	ppa._apply_view_mode()
	_show_player()
	var fill: OmniLight3D = OmniLight3D.new()
	fill.name = "TTShotFill"
	fill.shadow_enabled = false
	fill.light_energy = 1.2
	fill.light_color = Color(0.85, 0.9, 1.0)
	fill.omni_range = 28.0
	ppa._camera.add_child(fill)
	var segs: Array = _segs()
	await _still("A1_lift_landing_sealed_F2.png", Vector3(64.2, 7.5, 17.6), Vector3(68.5, 7.05, 14.6))
	await _still("A2_guardrail_track_stairwell_F3.png", Vector3(57.2, 14.0, 11.5), Vector3(61.0, 12.9, 6.0))
	var slab: Dictionary = _longest(segs, "slab_opening")
	if slab.is_empty():
		await _still("A3_guardrail_slab_opening_F2.png", Vector3(64.0, 7.6, 17.5), Vector3(68.5, 6.8, 14.2))
	else:
		await _rail_still("A3_guardrail_slab_opening_F2.png", slab)
	# Gallery rails sit on the west edge of the F2 north opening (x=-10.75, z=70..71.6).
	await _still("A4_guardrail_gallery_edge_F2.png", Vector3(-8.2, 7.6, 70.8), Vector3(-10.75, 6.7, 70.8))
	await _court()
	await _open_door("A7_court_door_open.png", "tt_court_partition_door_closed", Vector3(0.45, 0.1, 1.6), Vector3(2.4, 1.55, 1.3), Vector3(0.4, 1.05, 0.15))
	await _open_door("A8_pair_door_open.png", "tt_door_pair_18", Vector3(0.0, 0.1, -2.0), Vector3(-1.8, 1.6, -1.6), Vector3(0.0, 1.15, 0.2))
	var stair: Dictionary = _longest(segs, "stair_landing")
	if stair.is_empty():
		await _still("A6_stair_core_guard.png", Vector3(36.5, 2.4, 22.2), Vector3(35.2, 1.3, 17.8))
	else:
		await _rail_still("A6_stair_core_guard.png", stair)
	print("[TT-SHOT] DONE failures=%d" % _failures)
	get_tree().quit(0 if _failures == 0 else 1)


func _show_player() -> void:
	var body: CharacterBody3D = ppa._player_body
	if body.get_node_or_null("TTShotBody") != null:
		return
	var vis: MeshInstance3D = MeshInstance3D.new()
	vis.name = "TTShotBody"
	var cap: CapsuleMesh = CapsuleMesh.new()
	cap.radius = 0.35
	cap.height = 1.75
	vis.mesh = cap
	vis.position = Vector3(0.0, 0.995, 0.0)
	vis.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	var mat: StandardMaterial3D = StandardMaterial3D.new()
	mat.albedo_color = Color(0.92, 0.55, 0.18, 1.0)
	mat.roughness = 0.45
	vis.material_override = mat
	body.add_child(vis)


func _court() -> void:
	var a: Vector3 = Vector3(61.5, 0.08, 24.8)
	var b: Vector3 = Vector3(61.5, 0.0, 30.5)
	var xf: Transform3D = ppa._tower_xf
	ppa._qa_tower_place(xf * a, ppa._tower_up, xf * b)
	await ppa._qa_frames(12)
	await ppa._qa_tower_walk_leg("shot_court", b, 160)
	await ppa._qa_frames(8)
	var q: Vector3 = ppa._tower_inv * ppa._player_body.global_position
	var eye: Vector3 = Vector3(q.x + 2.4, q.y + 1.35, q.z - 1.6)
	var at: Vector3 = Vector3(q.x, q.y + 1.0, q.z + 1.2)
	await _still("A5_court_glass_blocked.png", eye, at)
	print("[TT-SHOT] court stop q=(%.2f,%.2f,%.2f)" % [q.x, q.y, q.z])


func _open_door(file_name: String, prefix: String, stand_local: Vector3, eye_local: Vector3, at_local: Vector3) -> void:
	var door: Node3D = null
	var stack: Array[Node] = [ppa._tower]
	while not stack.is_empty():
		var n: Node = stack.pop_back()
		for ch: Node in n.get_children():
			stack.append(ch)
		if n is Node3D and String(n.name).begins_with(prefix):
			door = n as Node3D
			break
	if door == null:
		print("[TT-SHOT] %s missing %s" % [file_name, prefix])
		_failures += 1
		return
	var feet: Vector3 = door.global_transform * stand_local
	ppa._qa_tower_place(feet, ppa._tower_up, door.global_transform * at_local)
	await ppa._qa_frames(50)
	var eye: Vector3 = door.global_transform * eye_local
	var at: Vector3 = door.global_transform * at_local
	await _still_world(file_name, eye, at)


func _rail_still(file_name: String, s: Dictionary) -> void:
	var y: float = float(s["y"])
	var mid: Vector3 = Vector3((float(s["x0"]) + float(s["x1"])) * 0.5, y, (float(s["z0"]) + float(s["z1"])) * 0.5)
	var nrm: Vector3 = Vector3(float(s["nx"]), 0.0, float(s["nz"])).normalized()
	var stand: Vector3 = mid + nrm * 2.2 + Vector3(0.0, 1.55, 0.0)
	var look: Vector3 = mid + Vector3(0.0, 0.7, 0.0)
	ppa._player_body.global_position = ppa._tower_xf * (mid + nrm * 0.85 + Vector3(0.0, 0.15, 0.0))
	await _still(file_name, stand, look)


func _still(file_name: String, eye_q: Vector3, at_q: Vector3) -> void:
	var xf: Transform3D = ppa._tower_xf
	await _still_world(file_name, xf * eye_q, xf * at_q)


func _still_world(file_name: String, eye: Vector3, at: Vector3) -> void:
	ppa._qa_free_cam(eye, at, ppa._tower_up, 55.0)
	await ppa._qa_frames(12)
	var path: String = OUT_DIR + "/" + file_name
	if not await ppa._shot_curve_save(path):
		_failures += 1


func _segs() -> Array:
	if not FileAccess.file_exists(GUARD_JSON):
		return []
	var parsed: Variant = JSON.parse_string(FileAccess.get_file_as_string(GUARD_JSON))
	if typeof(parsed) != TYPE_DICTIONARY:
		return []
	var segs: Variant = (parsed as Dictionary).get("segments", [])
	return segs if segs is Array else []


func _longest(segs: Array, reason: String) -> Dictionary:
	var best: Dictionary = {}
	var best_l: float = -1.0
	for s_v in segs:
		var s: Dictionary = s_v
		if String(s.get("reason", "")) != reason:
			continue
		var l: float = Vector2(float(s["x1"]) - float(s["x0"]), float(s["z1"]) - float(s["z0"])).length()
		if l > best_l:
			best_l = l
			best = s
	return best
