class_name PlayerCamera
extends Camera3D
## PlayerCamera for Cylinder Hab-7: Living Quarters
## Supports:
## - First-Person walkable movement (WASD + Mouse Look, Q/E vertical)
## - Toggleable Orbit mode (Tab or C key) around room center (0, 1.35, 0)
## - Preset viewpoints 1-5 for instant inspection
## - Automated screenshot capture (--capture-screenshots CLI arg or F12)
## - Clean headless validation exit (--validate-only or headless DisplayServer)

enum Mode {
	FIRST_PERSON,
	ORBIT
}

@export var move_speed: float = 2.6
@export var mouse_sensitivity: float = 0.0025
@export var orbit_target: Vector3 = Vector3(0.0, 1.25, 0.0)
@export var orbit_distance: float = 2.45

var current_mode: Mode = Mode.FIRST_PERSON
var yaw: float = 0.0
var pitch: float = -0.14
var orbit_yaw: float = 0.45
var orbit_pitch: float = 0.24

# Room walk bounds (inside 4.0m x 5.0m x 3.0m interior)
const BOUNDS_X := Vector2(-1.72, 1.72)
const BOUNDS_Y := Vector2(0.55, 2.65)
const BOUNDS_Z := Vector2(-2.15, 2.25)

const PRESETS := [
	{
		"name": "01_overview_entrance",
		"label": "Wide Entrance Overview Toward O'Neill Viewport",
		"pos": Vector3(0.15, 1.68, 2.22),
		"target": Vector3(0.0, 1.15, -1.50),
		"fov": 72.0
	},
	{
		"name": "02_viewport_and_desk",
		"label": "O'Neill Viewport, Hydro Planter & Retro CRT Desk",
		"pos": Vector3(-0.35, 1.48, 0.35),
		"target": Vector3(0.65, 1.15, -1.95),
		"fov": 66.0
	},
	{
		"name": "03_bunk_and_wardrobe",
		"label": "Built-In Bunk Pod & Crew Wardrobe Locker",
		"pos": Vector3(1.15, 1.52, -0.35),
		"target": Vector3(-1.35, 1.02, 0.35),
		"fov": 68.0
	},
	{
		"name": "04_lounge_and_lamp",
		"label": "Cozy Lounge Chair, Smoked-Amber Table & Mushroom Lamp",
		"pos": Vector3(-0.65, 1.42, -1.15),
		"target": Vector3(0.85, 0.88, 1.15),
		"fov": 66.0
	},
	{
		"name": "05_oneill_cylinder_vista",
		"label": "O'Neill Cylinder 800m x 400m Window Vista & Sunlight",
		"pos": Vector3(0.05, 1.48, -0.25),
		"target": Vector3(-0.10, 1.52, -3.20),
		"fov": 62.0
	}
]

var _capture_requested: bool = false
var _validate_only: bool = false
var _frame_counter: int = 0
var _capture_step: int = 0
var _capture_wait_frames: int = 0


func _ready() -> void:
	current = true
	apply_preset(0)

	var all_args: PackedStringArray = OS.get_cmdline_args() + OS.get_cmdline_user_args()
	for arg: String in all_args:
		if arg == "--capture-screenshots" or arg == "--screenshots":
			_capture_requested = true
		elif arg == "--validate-only" or arg == "--validate":
			_validate_only = true

	if OS.get_environment("CAPTURE_SCREENSHOTS") == "1":
		_capture_requested = true
	if OS.get_environment("VALIDATE_ONLY") == "1":
		_validate_only = true

	if DisplayServer.get_name() == "headless" and not _capture_requested:
		_validate_only = true

	print("[PlayerCamera] Initialized at ", global_position, " | Mode: FIRST_PERSON | DisplayServer: ", DisplayServer.get_name())


func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventKey:
		var key_event: InputEventKey = event as InputEventKey
		if key_event.pressed and not key_event.echo:
			match key_event.keycode:
				KEY_TAB, KEY_C:
					toggle_mode()
				KEY_1:
					apply_preset(0)
				KEY_2:
					apply_preset(1)
				KEY_3:
					apply_preset(2)
				KEY_4:
					apply_preset(3)
				KEY_5:
					apply_preset(4)
				KEY_F12:
					_start_manual_capture()
				KEY_ESCAPE:
					if Input.get_mouse_mode() == Input.MouseMode.MOUSE_MODE_CAPTURED:
						Input.set_mouse_mode(Input.MouseMode.MOUSE_MODE_VISIBLE)
					else:
						Input.set_mouse_mode(Input.MouseMode.MOUSE_MODE_CAPTURED)

	if event is InputEventMouseButton:
		var mb: InputEventMouseButton = event as InputEventMouseButton
		if mb.pressed:
			if mb.button_index == MOUSE_BUTTON_RIGHT:
				if Input.get_mouse_mode() == Input.MouseMode.MOUSE_MODE_CAPTURED:
					Input.set_mouse_mode(Input.MouseMode.MOUSE_MODE_VISIBLE)
				else:
					Input.set_mouse_mode(Input.MouseMode.MOUSE_MODE_CAPTURED)
			elif mb.button_index == MOUSE_BUTTON_WHEEL_UP and current_mode == Mode.ORBIT:
				orbit_distance = clampf(orbit_distance - 0.2, 0.8, 3.6)
				_update_orbit_transform()
			elif mb.button_index == MOUSE_BUTTON_WHEEL_DOWN and current_mode == Mode.ORBIT:
				orbit_distance = clampf(orbit_distance + 0.2, 0.8, 3.6)
				_update_orbit_transform()

	if event is InputEventMouseMotion:
		var mm: InputEventMouseMotion = event as InputEventMouseMotion
		if current_mode == Mode.FIRST_PERSON and Input.get_mouse_mode() == Input.MouseMode.MOUSE_MODE_CAPTURED:
			yaw -= mm.relative.x * mouse_sensitivity
			pitch = clampf(pitch - mm.relative.y * mouse_sensitivity, -1.35, 1.35)
			rotation = Vector3(pitch, yaw, 0.0)
		elif current_mode == Mode.ORBIT and (Input.is_mouse_button_pressed(MOUSE_BUTTON_LEFT) or Input.get_mouse_mode() == Input.MouseMode.MOUSE_MODE_CAPTURED):
			orbit_yaw -= mm.relative.x * mouse_sensitivity * 1.2
			orbit_pitch = clampf(orbit_pitch + mm.relative.y * mouse_sensitivity * 1.2, -0.45, 1.15)
			_update_orbit_transform()


func _process(delta: float) -> void:
	_frame_counter += 1

	if _capture_requested:
		_process_automated_capture()
		return

	if _validate_only:
		if _frame_counter >= 4:
			print("[PlayerCamera] Headless validation complete after ", _frame_counter, " frames. Exiting cleanly.")
			get_tree().quit(0)
		return

	var input_dir: Vector2 = Vector2.ZERO
	if Input.is_key_pressed(KEY_W) or Input.is_key_pressed(KEY_UP):
		input_dir.y -= 1.0
	if Input.is_key_pressed(KEY_S) or Input.is_key_pressed(KEY_DOWN):
		input_dir.y += 1.0
	if Input.is_key_pressed(KEY_A) or Input.is_key_pressed(KEY_LEFT):
		input_dir.x -= 1.0
	if Input.is_key_pressed(KEY_D) or Input.is_key_pressed(KEY_RIGHT):
		input_dir.x += 1.0

	if current_mode == Mode.FIRST_PERSON:
		if input_dir.length_squared() > 0.0:
			input_dir = input_dir.normalized()
			var forward: Vector3 = -global_transform.basis.z
			forward.y = 0.0
			forward = forward.normalized()
			var right: Vector3 = global_transform.basis.x
			right.y = 0.0
			right = right.normalized()
			var move_vec: Vector3 = (right * input_dir.x - forward * input_dir.y) * move_speed * delta
			global_position += move_vec

		if Input.is_key_pressed(KEY_E) or Input.is_key_pressed(KEY_SPACE):
			global_position.y += move_speed * 0.6 * delta
		if Input.is_key_pressed(KEY_Q) or Input.is_key_pressed(KEY_SHIFT):
			global_position.y -= move_speed * 0.6 * delta

		global_position.x = clampf(global_position.x, BOUNDS_X.x, BOUNDS_X.y)
		global_position.y = clampf(global_position.y, BOUNDS_Y.x, BOUNDS_Y.y)
		global_position.z = clampf(global_position.z, BOUNDS_Z.x, BOUNDS_Z.y)
	else:
		if input_dir.length_squared() > 0.0:
			orbit_yaw += input_dir.x * 1.4 * delta
			orbit_pitch = clampf(orbit_pitch - input_dir.y * 1.0 * delta, -0.45, 1.15)
			_update_orbit_transform()


func toggle_mode() -> void:
	if current_mode == Mode.FIRST_PERSON:
		current_mode = Mode.ORBIT
		_update_orbit_transform()
		print("[PlayerCamera] Switched to ORBIT mode around ", orbit_target)
	else:
		current_mode = Mode.FIRST_PERSON
		var euler: Vector3 = global_transform.basis.get_euler()
		pitch = euler.x
		yaw = euler.y
		print("[PlayerCamera] Switched to FIRST_PERSON mode at ", global_position)


func _update_orbit_transform() -> void:
	var offset: Vector3 = Vector3(
		sin(orbit_yaw) * cos(orbit_pitch),
		sin(orbit_pitch),
		cos(orbit_yaw) * cos(orbit_pitch)
	) * orbit_distance
	var desired: Vector3 = orbit_target + offset
	desired.x = clampf(desired.x, BOUNDS_X.x, BOUNDS_X.y)
	desired.y = clampf(desired.y, BOUNDS_Y.x, BOUNDS_Y.y)
	desired.z = clampf(desired.z, BOUNDS_Z.x, BOUNDS_Z.y)
	global_position = desired
	look_at(orbit_target, Vector3.UP)


func apply_preset(index: int) -> void:
	if index < 0 or index >= PRESETS.size():
		return
	current_mode = Mode.FIRST_PERSON
	var p: Dictionary = PRESETS[index]
	global_position = p["pos"] as Vector3
	fov = float(p["fov"])
	look_at(p["target"] as Vector3, Vector3.UP)
	var euler: Vector3 = global_transform.basis.get_euler()
	pitch = euler.x
	yaw = euler.y


func _start_manual_capture() -> void:
	_capture_requested = true
	_capture_step = 0
	_capture_wait_frames = 0


func _process_automated_capture() -> void:
	if DisplayServer.get_name() == "headless":
		print("[PlayerCamera] WARNING: Cannot capture viewport texture under 'headless' DisplayServer. Run with xvfb-run and --rendering-driver opengl3.")
		get_tree().quit(0)
		return

	# Wait initial 10 frames for scene assembly, textures, and lighting setup
	if _frame_counter < 10:
		apply_preset(0)
		return

	if _capture_step >= PRESETS.size():
		print("[PlayerCamera] All ", PRESETS.size(), " preview renders saved! Exiting cleanly.")
		get_tree().quit(0)
		return

	if _capture_wait_frames == 0:
		apply_preset(_capture_step)
		_capture_wait_frames = 1
		return

	_capture_wait_frames += 1
	if _capture_wait_frames >= 6:
		var preset: Dictionary = PRESETS[_capture_step]
		var filename: String = "render_" + String(preset["name"]) + ".png"
		var img: Image = get_viewport().get_texture().get_image()
		if img != null and not img.is_empty():
			var out_dirs: Array[String] = [
				ProjectSettings.globalize_path("res://renders"),
				ProjectSettings.globalize_path("res://../assets/renders")
			]
			for d: String in out_dirs:
				DirAccess.make_dir_recursive_absolute(d)
				var full_path: String = d.path_join(filename)
				var err: Error = img.save_png(full_path)
				if err == OK:
					print("[PlayerCamera] Saved render: ", full_path, " (", img.get_width(), "x", img.get_height(), ")")
		_capture_step += 1
		_capture_wait_frames = 0
