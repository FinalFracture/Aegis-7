extends CharacterBody3D
## Preface player model, flat lab, up = +Y.
## Forward is -basis.z, read from this body's basis (the same basis WASD uses).
## Yaw 180 faces world +Z. Swept substeps keep a 63 m/s tick under 0.40 m.

const WALK_SPEED := 5.2
const SPRINT_SPEED := 63.0
const JUMP_VELOCITY := 4.8
const GRAVITY := 9.8
const GROUND_ACCEL := 45.0
const SPRINT_GROUND_ACCEL := 63.0
const GROUND_FRICTION := 35.0
const AIR_ACCEL := 8.0
const SWEEP_STEP := 0.40

var gravity_scale: float = 1.0
var drive_enabled: bool = true


func _ready() -> void:
	floor_max_angle = deg_to_rad(50.0)
	floor_snap_length = 0.35
	floor_stop_on_slope = true
	collision_layer = 1
	collision_mask = 1
	add_to_group("door_lab_actor")
	var cs := CollisionShape3D.new()
	cs.name = "PlayerCapsule"
	var cap := CapsuleShape3D.new()
	cap.radius = 0.35
	cap.height = 1.75
	cs.shape = cap
	# Bottom of the capsule sits 0.12 m above the body origin.
	cs.position = Vector3(0.0, 0.875 + 0.12, 0.0)
	add_child(cs)
	var pivot := Node3D.new()
	pivot.name = "CameraPivot"
	pivot.position = Vector3(0.0, 1.50 + 0.12, 0.0)
	add_child(pivot)
	var cam := Camera3D.new()
	cam.name = "PlayerCamera"
	cam.fov = 70.0
	cam.near = 0.05
	cam.far = 200.0
	cam.current = true
	pivot.add_child(cam)


func _physics_process(delta: float) -> void:
	var input_dir := Vector2.ZERO
	var sprint := false
	var jump := false
	if drive_enabled:
		input_dir = Input.get_vector("move_left", "move_right", "move_forward", "move_back")
		sprint = Input.is_action_pressed("sprint")
		jump = Input.is_action_just_pressed("jump")
	var basis := global_transform.basis
	var dir := basis.x * input_dir.x + basis.z * input_dir.y
	dir.y = 0.0
	if dir.length_squared() > 0.0001:
		dir = dir.normalized()
	var speed := SPRINT_SPEED if sprint else WALK_SPEED
	var v_up := velocity.y
	if not is_on_floor():
		v_up -= GRAVITY * gravity_scale * delta
	elif jump:
		v_up = JUMP_VELOCITY
	elif v_up > 0.0 and v_up < JUMP_VELOCITY * 0.5:
		v_up = 0.0
	var h := Vector3(velocity.x, 0.0, velocity.z)
	var target := dir * speed
	if is_on_floor():
		if dir != Vector3.ZERO:
			var accel := SPRINT_GROUND_ACCEL if sprint else GROUND_ACCEL
			h = h.move_toward(target, accel * delta)
		else:
			h = h.move_toward(Vector3.ZERO, GROUND_FRICTION * delta)
	elif dir != Vector3.ZERO:
		h = h.move_toward(target, AIR_ACCEL * delta)
	velocity = Vector3(h.x, v_up, h.z)
	_move_swept(delta)


func _move_swept(delta: float) -> void:
	# Each move_and_slide uses the full physics delta, so velocity is split
	# across n calls and the chord of each call stays <= 0.40 m.
	var dist := velocity.length() * delta
	var n := clampi(int(ceil(dist / SWEEP_STEP)), 1, 16)
	if n == 1:
		floor_snap_length = 0.35
		safe_margin = 0.001
		move_and_slide()
		return
	floor_snap_length = 0.35
	safe_margin = 0.03
	var true_vel := velocity
	for _i in n:
		velocity = true_vel / float(n)
		move_and_slide()
		true_vel = velocity * float(n)
		if is_on_floor() and true_vel.y < 0.0:
			true_vel.y = 0.0
		if true_vel.length_squared() < 0.0004:
			true_vel = Vector3.ZERO
			break
	velocity = true_vel
