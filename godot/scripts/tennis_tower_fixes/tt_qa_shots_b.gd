extends Node
## Windowed stills for the drum-entry pass. Shipped lighting plus one
## unshadowed camera fill OmniLight (TTShotFill).

const OUT_DIR := "C:/Users/upchu/aegis_shots/ttfix_B"

var ppa: PrefacePlayableArea
var _failures: int = 0


func _ready() -> void:
	_run.call_deferred()


func _run() -> void:
	var guard := 0
	while (ppa == null or not ppa.has_meta("exterior_spawned")) and guard < 4000:
		await get_tree().physics_frame
		guard += 1
	if ppa == null or ppa._player_body == null or ppa._tower == null or ppa._camera == null:
		print("[TT-SHOT-B] FAIL setup")
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
	var fill := OmniLight3D.new()
	fill.name = "TTShotFill"
	fill.shadow_enabled = false
	fill.light_energy = 0.9
	fill.light_color = Color(0.85, 0.90, 1.0)
	fill.omni_range = 22.0
	fill.omni_attenuation = 1.2
	ppa._camera.add_child(fill)
	# West of the switchback, above the drum, looking east along the ramp.
	# The old eye sat under the terrace skirt and framed the black soffit.
	await _stand_drum("B1_SW_ramp_from_drum.png", Vector2(-46.0, 1.5), Vector3(-34.0, -0.4, 10.2), Vector3(-64.0, 7.0, -4.0))
	await _stand_drum("B2_W_grand_stair_from_drum.png", Vector2(-78.0, 34.0), Vector3(-66.0, -2.0, 39.5), Vector3(-82.0, 2.4, 28.0))
	await _stand_drum("B3_E_plaza_access.png", Vector2(186.0, 32.0), Vector3(168.0, -1.5, 38.0), Vector3(190.0, 2.6, 24.0))
	await _stand_drum("B4_S_door_wayfinding.png", Vector2(72.0, -10.0), Vector3(72.0, 2.2, -1.0), Vector3(66.0, 1.7, -14.0))
	await _stand_drum("B5_N_door_wayfinding.png", Vector2(72.0, 90.0), Vector3(72.0, 2.2, 80.0), Vector3(66.0, 1.8, 96.0))
	await _aerial()
	print("[TT-SHOT-B] DONE failures=%d" % _failures)
	get_tree().quit(0 if _failures == 0 else 1)


func _drum_y(z: float) -> float:
	return 195.9592 - sqrt(maxf(0.0, 40000.0 - (z - 40.0) * (z - 40.0)))


func _show_player() -> void:
	var body: CharacterBody3D = ppa._player_body
	if body.get_node_or_null("TTShotBody") != null:
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
	body.add_child(vis)


func _stand_drum(file_name: String, stand_xz: Vector2, look_q: Vector3, eye_q: Vector3) -> void:
	var feet: Vector3 = ppa._tt_floor_feet(Vector3(stand_xz.x, 0.0, stand_xz.y))
	ppa._qa_tower_place(feet, ppa._drum_up_at(feet), ppa._tower_xf * look_q)
	await ppa._qa_frames(12)
	var eye := Vector3(eye_q.x, _drum_y(eye_q.z) + eye_q.y, eye_q.z)
	await _still(file_name, eye, look_q)


func _aerial() -> void:
	var feet: Vector3 = ppa._tt_floor_feet(Vector3(-62.0, 0.0, 4.0))
	ppa._qa_tower_place(feet, ppa._drum_up_at(feet), ppa._tower_xf * Vector3(-40.0, 0.0, 12.0))
	await ppa._qa_frames(8)
	# Southwest, looking north along the west edge so the switchbacks
	# read in plan. A due-west eye saw only the stair end-on.
	await _still("B6_W_aerial_access.png", Vector3(-58.0, 14.0, -16.0), Vector3(-46.0, -0.3, 42.0), 58.0)


func _still(file_name: String, eye_q: Vector3, at_q: Vector3, fov: float = 55.0) -> void:
	var xf: Transform3D = ppa._tower_xf
	ppa._qa_free_cam(xf * eye_q, xf * at_q, ppa._tower_up, fov)
	await ppa._qa_frames(16)
	var path := OUT_DIR + "/" + file_name
	if not await ppa._shot_curve_save(path):
		_failures += 1
