extends Node
## --shot-ttfix-d. Opened 3l bay and the F1/F2 Z15 links.

const OUT_DIR := "C:/Users/upchu/aegis_shots/ttfix_D"

var ppa: PrefacePlayableArea
var _failures: int = 0


func _ready() -> void:
	_qa_run.call_deferred()


func _qa_run() -> void:
	var guard := 0
	while (ppa == null or not ppa.has_meta("exterior_spawned") or ppa._player_body == null or ppa._tower == null) and guard < 6000:
		await get_tree().physics_frame
		guard += 1
	if ppa == null or ppa._player_body == null or ppa._tower == null or ppa._camera == null:
		print("[TT-SHOT-D] FAIL setup")
		get_tree().quit(1)
		return
	DirAccess.make_dir_recursive_absolute(OUT_DIR)
	if DisplayServer.get_name() != "headless":
		DisplayServer.window_set_mode(DisplayServer.WINDOW_MODE_WINDOWED)
		DisplayServer.window_set_size(Vector2i(1920, 1080))
	if ppa._hud != null:
		ppa._hud.visible = false
	if ppa._reticle_box != null:
		ppa._reticle_box.visible = false
	ppa._third_person = false
	ppa._apply_view_mode()
	var bay_z: float = ppa._qa_tower_bay_lane_z(39.0)
	await _still("D1_bay3_open.png", Vector3(-18.0, 1.7, bay_z + 3.2), Vector3(-12.2, 1.3, bay_z), Vector3(-16.0, 0.2, bay_z))
	_print_leaves("bay", "tt_entrance_bay_3l", bay_z)
	await _still("D2_f1_z15_cut.png", Vector3(64.2, 1.7, 17.8), Vector3(65.1, 1.3, 14.2), Vector3(65.25, 0.2, 14.6))
	await _still("D3_f2_z15_cut.png", Vector3(64.2, 7.8, 17.8), Vector3(65.1, 7.3, 14.2), Vector3(65.25, 6.3, 14.6))
	# Hall gap is X 90.58..92.41. x=90.2 sits inside the stand.
	await _still("D4_f2_pair18_open.png", Vector3(91.5, 7.7, 18.2), Vector3(91.5, 7.1, 14.85), Vector3(91.5, 6.3, 13.9))
	_print_leaves("pair", "tt_door_pair_18", 14.85)
	print("[TT-SHOT-D] DONE failures=%d" % _failures)
	get_tree().quit(0 if _failures == 0 else 1)


func _still(file_name: String, eye: Vector3, look: Vector3, stand: Vector3) -> void:
	var xf: Transform3D = ppa._tower_xf
	ppa._qa_tower_place(xf * stand, ppa._tower_up, xf * look)
	await ppa._qa_frames(50)
	ppa._qa_free_cam(xf * eye, xf * look, ppa._tower_up, 55.0)
	ppa._camera.current = true
	await ppa._qa_frames(8)
	if not await ppa._shot_curve_save(OUT_DIR + "/" + file_name):
		_failures += 1
		print("[TT-SHOT-D] save fail %s" % file_name)


func _print_leaves(tag: String, prefix: String, want_z: float) -> void:
	var best: Node3D = null
	var best_d: float = INF
	var stack: Array[Node] = [ppa._tower]
	while not stack.is_empty():
		var n: Node = stack.pop_back()
		for ch: Node in n.get_children():
			stack.append(ch)
		if n is Node3D and String(n.name).begins_with(prefix):
			var qz: float = (ppa._tower_inv * (n as Node3D).global_position).z
			var d: float = absf(qz - want_z)
			if d < best_d:
				best_d = d
				best = n as Node3D
	if best == null:
		print("[TT-SHOT-D] %s missing" % tag)
		return
	var shown := 0
	var hidden := 0
	var yaw := ""
	var walk: Array[Node] = [best]
	while not walk.is_empty():
		var node: Node = walk.pop_back()
		for ch2: Node in node.get_children():
			walk.append(ch2)
		if node is MeshInstance3D:
			if (node as MeshInstance3D).visible:
				shown += 1
			else:
				hidden += 1
		if node is Node3D and (String(node.name).begins_with("Leaf_") or String(node.name).begins_with("Leaf")):
			yaw += " %s=%.0f vis=%s" % [String(node.name), rad_to_deg((node as Node3D).rotation.y), str((node as Node3D).visible)]
	print("[TT-SHOT-D] %s %s meshes_visible=%d hidden=%d%s" % [tag, String(best.name), shown, hidden, yaw])
