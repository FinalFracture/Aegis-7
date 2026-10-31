extends Node3D
## Preface service-call force-field door. Self-contained: does not use PrefacePlayableArea.
## Lockout on ready. Call run_scan_cycle(1|2|3) for the calibration sequence.

const GLB_PATH := "res://assets/models/rfid_forcefield_door.glb"
const SHADER_PATH := "res://shaders/forcefield_door.gdshader"
const TEX_DIR := "res://assets/textures/force_field/"
const FRAME_W := 2.40
const FRAME_H := 2.60
const MODEL_FRAME_W := 1.82
const MODEL_FRAME_H := 2.61
const OPEN_W := 1.50
const OPEN_H := 2.45
const DEFAULT_OPACITY := 0.45
const STALL_STRENGTH := 0.40
const STALL_TIME := 2.0
const DISSOLVE_TIME := 0.8
const FIELD_COLOR := Color(0.72, 0.35, 1.0, 1.0)
const HUB_AMBER := Color(1.0, 0.584, 0.0)
const READY_CYAN := Color("#00E5FF")
const PHASE_ORANGE := Color("#D95B26")
const BASE_STATIC := 0.35
const BASE_JITTER := 0.004
const BASE_ARC := 0.8

const FALLBACK_SHADER := """shader_type spatial;
render_mode unshaded, blend_mix, cull_disabled, depth_draw_never, shadows_disabled;
uniform vec4 field_color : source_color = vec4(0.72, 0.35, 1.0, 1.0);
uniform float opacity : hint_range(0.0, 1.0) = 0.45;
uniform float dissolve : hint_range(0.0, 1.0) = 0.0;
uniform float static_strength : hint_range(0.0, 1.0) = 0.35;
uniform float jitter_strength : hint_range(0.0, 0.02) = 0.004;
uniform float arc_strength : hint_range(0.0, 2.0) = 0.8;
uniform float stall_amount : hint_range(0.0, 1.0) = 0.0;
uniform float split_seam : hint_range(0.0, 1.0) = 0.0;
uniform sampler2D state_albedo : hint_default_white, repeat_enable, filter_linear;
uniform sampler2D state_emission : hint_default_black, repeat_enable, filter_linear;
uniform sampler2D stall_noise_mask : hint_default_black, repeat_enable, filter_linear;
uniform sampler2D split_seam_albedo : hint_default_black, repeat_enable, filter_linear;
uniform sampler2D split_seam_emission : hint_default_black, repeat_enable, filter_linear;
void fragment() {
	vec3 col = field_color.rgb * texture(state_albedo, UV).rgb;
	col += texture(state_emission, UV).rgb;
	float a = opacity * (1.0 - dissolve);
	a = mix(a, max(a, 0.15), stall_amount);
	ALBEDO = col;
	ALPHA = clamp(a, 0.0, 1.0);
}
"""

var _built: bool = false
var _model: Node3D
var _mat_a: ShaderMaterial
var _mat_b: ShaderMaterial
var _col_a: CollisionShape3D
var _col_b: CollisionShape3D
var _status_mat: StandardMaterial3D
var _threshold_mat: StandardMaterial3D
var _coil_mats: Array[StandardMaterial3D] = []
var _calib_mats: Array[StandardMaterial3D] = []
var _calib_cells: Array[int] = []
var _tex_cache: Dictionary = {}
var _half_a_on: bool = true
var _half_b_on: bool = true
var _split_synced: bool = false
var _open: bool = false
var _ff_state: String = "locked"
var _stall_t: float = 0.0
var _opacity: float = DEFAULT_OPACITY
var _time: float = 0.0
var _frame: int = 0
var _seq: int = 0
var _tween: Tween
var _surge_tween: Tween


func _ready() -> void:
	var container: Node3D = get_node_or_null("DoorContainer") as Node3D
	if container == null:
		container = self
	_build(container)


func _process(delta: float) -> void:
	_time += delta
	_frame += 1
	if not _built:
		return
	if _ff_state == "stall":
		_tick_stall(delta)


## 1-based calibration pass. Values below 1 run cycle 1; values above 3 run cycle 3.
## Cycle 1: A drops to a 40% stall, B holds, both colliders stay on, then both surge to 100%.
## Cycle 2: B drops, A returns, then the field drops and re-raises (coils end in phase).
## Cycle 3: hold A, sync both halves, then collapse (dissolve 0.8 s, colliders off).
func run_scan_cycle(i: int) -> void:
	if not _built or not is_inside_tree():
		return
	_seq += 1
	var token: int = _seq
	var n: int = clampi(i, 1, 3)
	if n == 1:
		_begin_cycle_1()
		return
	if n == 2:
		await _run_cycle_2(token)
		return
	await _run_cycle_3(token)


func _build(container: Node3D) -> void:
	var shader: Shader = _load_shader()
	_model = _instance_glb(GLB_PATH)
	if _model == null:
		_model = _placeholder_model()
	_model.name = "ForceFieldDoorModel"
	_model.scale = Vector3(FRAME_W / MODEL_FRAME_W, FRAME_H / MODEL_FRAME_H, 1.0)
	container.add_child(_model)
	var base: ShaderMaterial = _new_field_material(shader)
	var plane: MeshInstance3D = _find_mi(_model, "FieldPlane")
	if plane != null:
		plane.material_override = base
		plane.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	_enable_split(plane, base)
	_bind_emitters(container, false)
	_threshold_mat = _bind_threshold(false)
	_bind_status(HUB_AMBER)
	_make_calib(container)
	_make_pedestal(container)
	_make_transom(container)
	_apply_lockout_visuals()
	_apply_colliders(true)
	_built = true
	print("[SERVICE-DOOR] ready frame=%.2fx%.2f split=true calib=%d" % [FRAME_W, FRAME_H, _calib_mats.size()])


func _begin_cycle_1() -> void:
	_kill_motion()
	_open = false
	_half_a_on = true
	_half_b_on = true
	_split_synced = false
	_ff_state = "stall"
	_stall_t = STALL_TIME
	_set_calib(0, 2)
	_set_calib(1, 1)
	_set_calib(2, 1)
	_set_coil_phase(false)
	_set_seam(1.0)
	_set_threshold(false)
	_bind_state(_mat_a, true)
	_bind_state(_mat_b, true)
	_write_half(_mat_b, 0.0, _opacity, BASE_STATIC, BASE_JITTER, BASE_ARC, 0.0)
	_set_status(HUB_AMBER, 2.0)
	_apply_colliders(true)
	_tick_stall(0.0)


func _run_cycle_2(token: int) -> void:
	_kill_motion()
	_ff_state = "locked"
	_stall_t = 0.0
	_open = false
	_half_a_on = true
	_half_b_on = true
	_split_synced = false
	_set_calib(1, 2)
	_set_coil_phase(false)
	_set_seam(1.0)
	_set_threshold(false)
	_bind_state(_mat_a, true)
	_bind_state(_mat_b, true)
	_write_half(_mat_a, 0.0, _opacity, BASE_STATIC, BASE_JITTER, BASE_ARC, 0.0)
	_apply_colliders(false)
	# B drops while A returns. Colliders stay up until each sheet is actually gone.
	if not await _tween_halves(0.0, 1.0, 0.45, token):
		return
	_half_b_on = false
	_apply_colliders(false)
	# Full drop, then a clear aperture, then re-raise. Not the final collapse.
	if not await _tween_halves(1.0, 1.0, 0.40, token):
		return
	_half_a_on = false
	_apply_colliders(false)
	if not await _wait_sec(0.35, token):
		return
	_half_a_on = true
	_half_b_on = true
	_apply_colliders(false)
	if not await _tween_halves(0.0, 0.0, 0.45, token):
		return
	_write_half(_mat_a, 0.0, _opacity, BASE_STATIC, BASE_JITTER, BASE_ARC, 0.0)
	_write_half(_mat_b, 0.0, _opacity, BASE_STATIC, BASE_JITTER, BASE_ARC, 0.0)
	_set_coil_phase(true)
	_set_calib(2, 2)
	_set_status(HUB_AMBER, 2.0)
	_apply_colliders(false)


func _run_cycle_3(token: int) -> void:
	_kill_motion()
	_ff_state = "locked"
	_stall_t = 0.0
	_open = false
	_split_synced = false
	# Hold A. Do not release yet.
	_half_a_on = true
	_bind_state(_mat_a, true)
	_write_half(_mat_a, 0.0, _opacity, BASE_STATIC, BASE_JITTER, BASE_ARC, 0.0)
	_set_seam(1.0)
	_apply_colliders(false)
	if not await _wait_sec(0.40, token):
		return
	# Sync both halves, then the field is allowed to collapse.
	_half_b_on = true
	_split_synced = true
	_bind_state(_mat_a, false)
	_bind_state(_mat_b, false)
	_write_half(_mat_a, 0.0, _opacity, BASE_STATIC, BASE_JITTER, BASE_ARC, 0.0)
	_write_half(_mat_b, 0.0, _opacity, BASE_STATIC, BASE_JITTER, BASE_ARC, 0.0)
	_set_seam(0.0)
	_set_coil_phase(true)
	_set_calib(0, 2)
	_set_calib(1, 2)
	_set_calib(2, 2)
	_set_threshold(true)
	_set_status(READY_CYAN, 2.0)
	_apply_colliders(false)
	if not _split_synced or not _half_a_on or not _half_b_on:
		return
	if not await _wait_sec(0.20, token):
		return
	_ff_state = "open"
	if not await _tween_halves(1.0, 1.0, DISSOLVE_TIME, token):
		return
	_open = true
	_half_a_on = false
	_half_b_on = false
	_apply_colliders(false)


func _tick_stall(delta: float) -> void:
	if delta > 0.0:
		_stall_t -= delta
	if delta > 0.0 and _stall_t <= 0.0:
		_surge_from_stall()
		return
	var n0: float = _noise(1.7)
	var n1: float = _noise(4.2)
	var n2: float = _noise(8.9)
	var n3: float = _noise(12.4)
	var base_op: float = _opacity * STALL_STRENGTH
	var op: float = clampf(base_op * lerpf(0.72, 1.28, n0), 0.08, base_op * 1.35)
	# A flickers at ~40%. B holds full strength. Both colliders stay on.
	_write_half(_mat_a, 0.0, op, lerpf(0.62, 0.98, n1), lerpf(0.008, 0.016, n2), lerpf(0.45, 1.35, n3), lerpf(0.85, 1.0, n0))
	_write_half(_mat_b, 0.0, _opacity, BASE_STATIC, BASE_JITTER, BASE_ARC, 0.0)
	_apply_colliders(true)
	_pulse_calib_stall()
	if _status_mat != null:
		_status_mat.emission = HUB_AMBER
		_status_mat.albedo_color = HUB_AMBER
		_status_mat.emission_energy_multiplier = 2.0 * (0.85 + 0.15 * sin(_time * TAU))


func _surge_from_stall() -> void:
	_ff_state = "locked"
	_stall_t = 0.0
	_open = false
	_half_a_on = true
	_half_b_on = true
	_write_half(_mat_a, 0.0, _opacity, BASE_STATIC, BASE_JITTER, BASE_ARC, 0.0)
	_write_half(_mat_b, 0.0, _opacity, BASE_STATIC, BASE_JITTER, BASE_ARC, 0.0)
	_bind_state(_mat_a, true)
	_bind_state(_mat_b, true)
	_apply_colliders(true)
	_set_status(HUB_AMBER, 2.0)
	_pulse_calib_stall()
	if _status_mat != null and is_inside_tree():
		var tw: Tween = create_tween()
		tw.tween_property(_status_mat, "emission_energy_multiplier", 4.2, 0.08)
		tw.tween_property(_status_mat, "emission_energy_multiplier", 2.0, 0.22)
		_surge_tween = tw


func _apply_lockout_visuals() -> void:
	_half_a_on = true
	_half_b_on = true
	_split_synced = false
	_open = false
	_ff_state = "locked"
	_bind_state(_mat_a, true)
	_bind_state(_mat_b, true)
	_write_half(_mat_a, 0.0, _opacity, BASE_STATIC, BASE_JITTER, BASE_ARC, 0.0)
	_write_half(_mat_b, 0.0, _opacity, BASE_STATIC, BASE_JITTER, BASE_ARC, 0.0)
	_set_seam(1.0)
	_set_coil_phase(false)
	_set_threshold(false)
	_set_status(HUB_AMBER, 2.0)
	for i: int in range(_calib_mats.size()):
		_set_calib(i, 1)


func _enable_split(plane: MeshInstance3D, base: ShaderMaterial) -> void:
	_mat_a = base.duplicate() as ShaderMaterial
	_mat_b = base.duplicate() as ShaderMaterial
	var parent: Node = _model
	var xform: Transform3D = Transform3D.IDENTITY
	if plane != null:
		parent = plane.get_parent()
		xform = plane.transform
		plane.visible = false
		plane.set_meta("replaced_by_split", true)
	var a: MeshInstance3D = MeshInstance3D.new()
	a.name = "FieldPlane_A"
	a.mesh = _half_mesh(true)
	a.transform = xform
	a.material_override = _mat_a
	a.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	var b: MeshInstance3D = MeshInstance3D.new()
	b.name = "FieldPlane_B"
	b.mesh = _half_mesh(false)
	b.transform = xform
	b.material_override = _mat_b
	b.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	parent.add_child(a)
	parent.add_child(b)
	_col_a = _static_box(_model, "FieldCollider_A", Vector3(OPEN_W * 0.5, OPEN_H, 0.20), Vector3(-OPEN_W * 0.25, OPEN_H * 0.5, 0.0))
	_col_b = _static_box(_model, "FieldCollider_B", Vector3(OPEN_W * 0.5, OPEN_H, 0.20), Vector3(OPEN_W * 0.25, OPEN_H * 0.5, 0.0))


func _apply_colliders(force_both_on: bool) -> void:
	var a_on: bool = true
	var b_on: bool = true
	if force_both_on:
		a_on = true
		b_on = true
	elif _open:
		a_on = false
		b_on = false
	else:
		a_on = _half_a_on
		b_on = _half_b_on
	_set_cs(_col_a, a_on)
	_set_cs(_col_b, b_on)


func _set_cs(cs: CollisionShape3D, enabled: bool) -> void:
	if cs != null and is_instance_valid(cs):
		cs.set_deferred("disabled", not enabled)


func _write_half(mat: ShaderMaterial, dissolve_v: float, opacity: float, static_s: float, jitter: float, arc: float, stall_amount: float) -> void:
	if mat == null:
		return
	mat.set_shader_parameter("dissolve", dissolve_v)
	mat.set_shader_parameter("opacity", opacity)
	mat.set_shader_parameter("static_strength", static_s)
	mat.set_shader_parameter("jitter_strength", jitter)
	mat.set_shader_parameter("arc_strength", arc)
	mat.set_shader_parameter("stall_amount", stall_amount)


func _bind_state(mat: ShaderMaterial, amber: bool) -> void:
	if mat == null:
		return
	var alb: Texture2D = _tex("ff_field_lockout_amber_albedo.png" if amber else "ff_field_ready_cyan_albedo.png")
	var emi: Texture2D = _tex("ff_field_lockout_amber_emission.png" if amber else "ff_field_ready_cyan_emission.png")
	if alb != null:
		mat.set_shader_parameter("state_albedo", alb)
	if emi != null:
		mat.set_shader_parameter("state_emission", emi)


func _set_seam(amount: float) -> void:
	if _mat_a != null:
		_mat_a.set_shader_parameter("split_seam", amount)
	if _mat_b != null:
		_mat_b.set_shader_parameter("split_seam", amount)


func _new_field_material(shader: Shader) -> ShaderMaterial:
	var mat: ShaderMaterial = ShaderMaterial.new()
	mat.shader = shader
	mat.set_shader_parameter("field_color", FIELD_COLOR)
	mat.set_shader_parameter("opacity", DEFAULT_OPACITY)
	mat.set_shader_parameter("dissolve", 0.0)
	mat.set_shader_parameter("static_strength", BASE_STATIC)
	mat.set_shader_parameter("jitter_strength", BASE_JITTER)
	mat.set_shader_parameter("arc_strength", BASE_ARC)
	mat.set_shader_parameter("stall_amount", 0.0)
	mat.set_shader_parameter("split_seam", 0.0)
	var stall_mask: Texture2D = _tex("ff_field_stall_noise_mask.png")
	var seam_a: Texture2D = _tex("ff_split_seam_albedo.png")
	var seam_e: Texture2D = _tex("ff_split_seam_emission.png")
	if stall_mask != null:
		mat.set_shader_parameter("stall_noise_mask", stall_mask)
	if seam_a != null:
		mat.set_shader_parameter("split_seam_albedo", seam_a)
	if seam_e != null:
		mat.set_shader_parameter("split_seam_emission", seam_e)
	return mat


func _bind_emitters(container: Node3D, in_phase: bool) -> void:
	_coil_mats.clear()
	var strip: MeshInstance3D = _find_mi(_model, "EmitterStrip")
	if strip != null:
		var sm: StandardMaterial3D = _coil_material(in_phase, 2.5)
		strip.material_override = sm
		_coil_mats.append(sm)
	var found_coil: bool = false
	for nm: String in ["Emitter_Coil_A", "Emitter_Coil_B", "EmitterCoil_A", "EmitterCoil_B"]:
		var mi: MeshInstance3D = _find_mi(_model, nm)
		if mi == null:
			continue
		found_coil = true
		var cm: StandardMaterial3D = _coil_material(in_phase, 2.0)
		mi.material_override = cm
		_coil_mats.append(cm)
	if not found_coil:
		# Header phase bars sit behind the inspection transom (world metres, not the scaled frame).
		_add_phase_bar(container, "Emitter_Coil_A", -0.34, in_phase)
		_add_phase_bar(container, "Emitter_Coil_B", 0.34, in_phase)


func _add_phase_bar(parent: Node3D, nm: String, x: float, in_phase: bool) -> void:
	var mi: MeshInstance3D = MeshInstance3D.new()
	mi.name = nm
	var bm: BoxMesh = BoxMesh.new()
	bm.size = Vector3(0.36, 0.08, 0.02)
	mi.mesh = bm
	mi.position = Vector3(x, FRAME_H + 0.28, 0.05)
	var cm: StandardMaterial3D = _coil_material(in_phase, 2.0)
	mi.material_override = cm
	parent.add_child(mi)
	_coil_mats.append(cm)


func _coil_material(in_phase: bool, energy: float) -> StandardMaterial3D:
	var mat: StandardMaterial3D = StandardMaterial3D.new()
	mat.emission_enabled = true
	mat.emission_energy_multiplier = energy
	_apply_coil_textures(mat, in_phase)
	return mat


func _apply_coil_textures(mat: StandardMaterial3D, in_phase: bool) -> void:
	if mat == null:
		return
	var alb: Texture2D = _tex("ff_emitter_coil_albedo.png")
	var orm: Texture2D = _tex("ff_emitter_coil_orm.png")
	var emi_name: String = "ff_emitter_coil_emission_inphase.png" if in_phase else "ff_emitter_coil_emission_outphase.png"
	var emi: Texture2D = _tex(emi_name)
	if emi == null and not in_phase:
		emi = _tex("ff_emitter_coil_emission_inphase.png")
	if alb != null:
		mat.albedo_texture = alb
		mat.albedo_color = Color.WHITE
	else:
		mat.albedo_color = Color("#88929E")
	if orm != null:
		mat.ao_enabled = true
		mat.ao_texture = orm
		mat.ao_texture_channel = BaseMaterial3D.TEXTURE_CHANNEL_RED
		mat.roughness_texture = orm
		mat.roughness_texture_channel = BaseMaterial3D.TEXTURE_CHANNEL_GREEN
		mat.metallic_texture = orm
		mat.metallic_texture_channel = BaseMaterial3D.TEXTURE_CHANNEL_BLUE
	else:
		mat.roughness = 0.35
		mat.metallic = 1.0
	mat.emission_enabled = true
	if emi != null:
		mat.emission = Color.WHITE
		mat.emission_texture = emi
	else:
		mat.emission = READY_CYAN if in_phase else PHASE_ORANGE


func _set_coil_phase(in_phase: bool) -> void:
	for mat: StandardMaterial3D in _coil_mats:
		var energy: float = mat.emission_energy_multiplier
		_apply_coil_textures(mat, in_phase)
		mat.emission_energy_multiplier = energy


func _bind_threshold(ready_state: bool) -> StandardMaterial3D:
	var mi: MeshInstance3D = _find_threshold_mi(_model)
	if mi == null:
		mi = MeshInstance3D.new()
		mi.name = "Threshold"
		var bm: BoxMesh = BoxMesh.new()
		bm.size = Vector3(OPEN_W, 0.025, 0.10)
		mi.mesh = bm
		mi.position = Vector3(0.0, 0.02, 0.06)
		_model.add_child(mi)
	var m: StandardMaterial3D = StandardMaterial3D.new()
	_apply_threshold(m, ready_state)
	mi.material_override = m
	return m


func _apply_threshold(mat: StandardMaterial3D, ready_state: bool) -> void:
	if mat == null:
		return
	var alb: Texture2D = _tex("ff_threshold_strip_albedo.png")
	var emi: Texture2D = _tex("ff_threshold_strip_cyan_emission.png" if ready_state else "ff_threshold_strip_amber_emission.png")
	if alb != null:
		mat.albedo_texture = alb
	mat.emission_enabled = true
	mat.emission = READY_CYAN if ready_state else HUB_AMBER
	mat.emission_energy_multiplier = 1.8
	mat.roughness = 0.6
	mat.metallic = 0.0
	if emi != null:
		mat.emission_texture = emi


func _set_threshold(ready_state: bool) -> void:
	_apply_threshold(_threshold_mat, ready_state)


func _bind_status(col: Color) -> void:
	var mi: MeshInstance3D = _find_mi(_model, "StatusLight")
	if mi == null:
		return
	var m: StandardMaterial3D = StandardMaterial3D.new()
	m.emission_enabled = true
	m.albedo_color = col
	m.emission = col
	m.emission_energy_multiplier = 2.0
	mi.material_override = m
	mi.visible = true
	_status_mat = m


func _set_status(col: Color, energy: float) -> void:
	if _status_mat == null:
		return
	_status_mat.albedo_color = col
	_status_mat.emission = col
	_status_mat.emission_energy_multiplier = energy


func _make_calib(container: Node3D) -> void:
	var alb: Texture2D = _tex("ff_calib_node_albedo.png")
	var emi: Texture2D = _tex("ff_calib_node_emission_states.png")
	var xs: Array[float] = [-0.36, 0.0, 0.36]
	for i: int in range(3):
		var mi: MeshInstance3D = MeshInstance3D.new()
		mi.name = "Node_Calib_%02d" % (i + 1)
		var bm: BoxMesh = BoxMesh.new()
		bm.size = Vector3(0.10, 0.08, 0.06)
		mi.mesh = bm
		mi.position = Vector3(xs[i], FRAME_H - 0.12, 0.16)
		var m: StandardMaterial3D = StandardMaterial3D.new()
		m.emission_enabled = true
		m.emission = HUB_AMBER
		m.emission_energy_multiplier = 2.5
		if alb != null:
			m.albedo_texture = alb
		if emi != null:
			m.emission_texture = emi
		m.uv1_scale = Vector3(1.0 / 3.0, 1.0, 1.0)
		m.uv1_offset = Vector3(1.0 / 3.0, 0.0, 0.0)
		mi.material_override = m
		container.add_child(mi)
		_calib_mats.append(m)
		_calib_cells.append(1)


func _set_calib(index: int, cell: int) -> void:
	if index < 0 or index >= _calib_mats.size():
		return
	_calib_cells[index] = cell
	var m: StandardMaterial3D = _calib_mats[index]
	m.uv1_offset = Vector3(float(cell) / 3.0, 0.0, 0.0)
	m.emission_energy_multiplier = 2.5 if cell > 0 else 0.0
	if cell == 2:
		m.emission = READY_CYAN
	elif cell == 1:
		m.emission = HUB_AMBER
	else:
		m.emission = Color(0.05, 0.05, 0.05, 1.0)


func _pulse_calib_stall() -> void:
	for i: int in range(_calib_mats.size()):
		if i >= _calib_cells.size():
			continue
		if _calib_cells[i] != 1:
			continue
		_calib_mats[i].emission_energy_multiplier = 2.5 * (0.85 + 0.15 * sin(_time * TAU))


func _make_pedestal(container: Node3D) -> void:
	var root: Node3D = Node3D.new()
	root.name = "Pedestal_RFID_Main"
	root.position = Vector3(1.55, 0.0, 0.55)
	container.add_child(root)
	var steel: StandardMaterial3D = StandardMaterial3D.new()
	steel.albedo_color = Color("#88929E")
	steel.metallic = 0.85
	steel.roughness = 0.38
	var column: MeshInstance3D = MeshInstance3D.new()
	column.name = "PedestalColumn"
	var cm: BoxMesh = BoxMesh.new()
	cm.size = Vector3(0.22, 1.15, 0.22)
	column.mesh = cm
	column.position = Vector3(0.0, 0.575, 0.0)
	column.material_override = steel
	root.add_child(column)
	var cap: MeshInstance3D = MeshInstance3D.new()
	cap.name = "PedestalCap"
	var cap_m: BoxMesh = BoxMesh.new()
	cap_m.size = Vector3(0.36, 0.04, 0.36)
	cap.mesh = cap_m
	cap.position = Vector3(0.0, 1.15, 0.0)
	cap.material_override = steel
	root.add_child(cap)
	var halo: MeshInstance3D = MeshInstance3D.new()
	halo.name = "PedestalHalo"
	var hm: CylinderMesh = CylinderMesh.new()
	hm.top_radius = 0.14
	hm.bottom_radius = 0.14
	hm.height = 0.02
	halo.mesh = hm
	halo.position = Vector3(0.0, 1.18, 0.0)
	var glow: StandardMaterial3D = StandardMaterial3D.new()
	glow.albedo_color = HUB_AMBER
	glow.emission_enabled = true
	glow.emission = HUB_AMBER
	glow.emission_energy_multiplier = 2.0
	halo.material_override = glow
	root.add_child(halo)


func _make_transom(container: Node3D) -> void:
	var mi: MeshInstance3D = MeshInstance3D.new()
	mi.name = "Transom_Glass"
	mi.mesh = _centered_quad(FRAME_W, 0.85)
	mi.position = Vector3(0.0, FRAME_H + 0.425, 0.18)
	mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	var mat: StandardMaterial3D = StandardMaterial3D.new()
	mat.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
	mat.cull_mode = BaseMaterial3D.CULL_DISABLED
	mat.metallic = 0.0
	mat.roughness = 0.12
	mat.metallic_specular = 0.5
	var alb: Texture2D = _tex("ff_transom_glass_albedo.png")
	var orm: Texture2D = _tex("ff_transom_glass_orm.png")
	if alb != null:
		mat.albedo_texture = alb
		mat.albedo_color = Color(1.0, 1.0, 1.0, 1.0)
	else:
		mat.albedo_color = Color(0.75, 0.86, 0.92, 0.32)
	if orm != null:
		mat.ao_enabled = true
		mat.ao_texture = orm
		mat.ao_texture_channel = BaseMaterial3D.TEXTURE_CHANNEL_RED
		mat.roughness_texture = orm
		mat.roughness_texture_channel = BaseMaterial3D.TEXTURE_CHANNEL_GREEN
	mi.material_override = mat
	container.add_child(mi)


func _placeholder_model() -> Node3D:
	var root: Node3D = Node3D.new()
	var steel: StandardMaterial3D = StandardMaterial3D.new()
	steel.albedo_color = Color("#1A1E24")
	steel.metallic = 0.7
	steel.roughness = 0.4
	var plane: MeshInstance3D = MeshInstance3D.new()
	plane.name = "FieldPlane"
	plane.mesh = _opening_quad(OPEN_W, OPEN_H)
	root.add_child(plane)
	_add_box(root, "FrameL", Vector3(0.16, MODEL_FRAME_H, 0.12), Vector3(-MODEL_FRAME_W * 0.5 + 0.08, MODEL_FRAME_H * 0.5, 0.0), steel)
	_add_box(root, "FrameR", Vector3(0.16, MODEL_FRAME_H, 0.12), Vector3(MODEL_FRAME_W * 0.5 - 0.08, MODEL_FRAME_H * 0.5, 0.0), steel)
	_add_box(root, "FrameHead", Vector3(MODEL_FRAME_W, 0.16, 0.12), Vector3(0.0, MODEL_FRAME_H - 0.08, 0.0), steel)
	var strip: MeshInstance3D = MeshInstance3D.new()
	strip.name = "EmitterStrip"
	var sm: BoxMesh = BoxMesh.new()
	sm.size = Vector3(OPEN_W, 0.05, 0.03)
	strip.mesh = sm
	strip.position = Vector3(0.0, OPEN_H + 0.03, 0.04)
	root.add_child(strip)
	return root


func _add_box(parent: Node3D, nm: String, sz: Vector3, pos: Vector3, mat: Material) -> void:
	var mi: MeshInstance3D = MeshInstance3D.new()
	mi.name = nm
	var bm: BoxMesh = BoxMesh.new()
	bm.size = sz
	mi.mesh = bm
	mi.position = pos
	mi.material_override = mat
	parent.add_child(mi)


func _half_mesh(negative_x: bool) -> ArrayMesh:
	var hw: float = OPEN_W * 0.5
	var x0: float = -hw if negative_x else 0.0
	var x1: float = 0.0 if negative_x else hw
	var u0: float = 0.0 if negative_x else 0.5
	var u1: float = 0.5 if negative_x else 1.0
	var st: SurfaceTool = SurfaceTool.new()
	st.begin(Mesh.PRIMITIVE_TRIANGLES)
	var nrm: Vector3 = Vector3(0.0, 0.0, 1.0)
	var verts: Array[Vector3] = [Vector3(x0, 0.0, 0.0), Vector3(x1, 0.0, 0.0), Vector3(x1, OPEN_H, 0.0), Vector3(x0, 0.0, 0.0), Vector3(x1, OPEN_H, 0.0), Vector3(x0, OPEN_H, 0.0)]
	var uvs: Array[Vector2] = [Vector2(u0, 1.0), Vector2(u1, 1.0), Vector2(u1, 0.0), Vector2(u0, 1.0), Vector2(u1, 0.0), Vector2(u0, 0.0)]
	for i: int in range(verts.size()):
		st.set_normal(nrm)
		st.set_uv(uvs[i])
		st.add_vertex(verts[i])
	return st.commit()


func _opening_quad(w: float, h: float) -> ArrayMesh:
	var st: SurfaceTool = SurfaceTool.new()
	st.begin(Mesh.PRIMITIVE_TRIANGLES)
	var nrm: Vector3 = Vector3(0.0, 0.0, 1.0)
	var hw: float = w * 0.5
	var verts: Array[Vector3] = [Vector3(-hw, 0.0, 0.0), Vector3(hw, 0.0, 0.0), Vector3(hw, h, 0.0), Vector3(-hw, 0.0, 0.0), Vector3(hw, h, 0.0), Vector3(-hw, h, 0.0)]
	var uvs: Array[Vector2] = [Vector2(0.0, 1.0), Vector2(1.0, 1.0), Vector2(1.0, 0.0), Vector2(0.0, 1.0), Vector2(1.0, 0.0), Vector2(0.0, 0.0)]
	for i: int in range(verts.size()):
		st.set_normal(nrm)
		st.set_uv(uvs[i])
		st.add_vertex(verts[i])
	return st.commit()


func _centered_quad(w: float, h: float) -> ArrayMesh:
	var st: SurfaceTool = SurfaceTool.new()
	st.begin(Mesh.PRIMITIVE_TRIANGLES)
	var nrm: Vector3 = Vector3(0.0, 0.0, 1.0)
	var hw: float = w * 0.5
	var hh: float = h * 0.5
	var verts: Array[Vector3] = [Vector3(-hw, -hh, 0.0), Vector3(hw, -hh, 0.0), Vector3(hw, hh, 0.0), Vector3(-hw, -hh, 0.0), Vector3(hw, hh, 0.0), Vector3(-hw, hh, 0.0)]
	var uvs: Array[Vector2] = [Vector2(0.0, 1.0), Vector2(1.0, 1.0), Vector2(1.0, 0.0), Vector2(0.0, 1.0), Vector2(1.0, 0.0), Vector2(0.0, 0.0)]
	for i: int in range(verts.size()):
		st.set_normal(nrm)
		st.set_uv(uvs[i])
		st.add_vertex(verts[i])
	return st.commit()


func _static_box(parent: Node3D, nm: String, sz: Vector3, pos: Vector3) -> CollisionShape3D:
	var body: StaticBody3D = StaticBody3D.new()
	body.name = nm
	body.position = pos
	parent.add_child(body)
	var cs: CollisionShape3D = CollisionShape3D.new()
	cs.name = nm + "_Shape"
	var bs: BoxShape3D = BoxShape3D.new()
	bs.size = sz
	cs.shape = bs
	body.add_child(cs)
	return cs


func _tween_halves(a_to: float, b_to: float, dur: float, token: int) -> bool:
	if token != _seq or not is_inside_tree():
		return false
	if _tween != null and _tween.is_valid():
		_tween.kill()
	var tw: Tween = create_tween().set_parallel(true)
	var span: float = maxf(dur, 0.001)
	if _mat_a != null:
		tw.tween_property(_mat_a, "shader_parameter/dissolve", a_to, span)
	if _mat_b != null:
		tw.tween_property(_mat_b, "shader_parameter/dissolve", b_to, span)
	_tween = tw
	return await _wait_sec(span + 0.02, token)


func _wait_sec(sec: float, token: int) -> bool:
	if token != _seq or not is_inside_tree():
		return false
	await get_tree().create_timer(maxf(sec, 0.001)).timeout
	return token == _seq and is_inside_tree()


func _kill_motion() -> void:
	if _tween != null and _tween.is_valid():
		_tween.kill()
	_tween = null
	if _surge_tween != null and _surge_tween.is_valid():
		_surge_tween.kill()
	_surge_tween = null


func _noise(salt: float) -> float:
	var s: float = sin(_time * 17.13 + salt * 1.37 + float(_frame) * 0.41) * 43758.5453
	return s - floor(s)


func _load_shader() -> Shader:
	if ResourceLoader.exists(SHADER_PATH):
		var res: Resource = ResourceLoader.load(SHADER_PATH)
		if res is Shader:
			return res as Shader
	var abs_p: String = ProjectSettings.globalize_path(SHADER_PATH)
	if FileAccess.file_exists(abs_p):
		var code: String = FileAccess.get_file_as_string(abs_p)
		if code != "":
			var sh: Shader = Shader.new()
			sh.code = code
			return sh
	push_warning("[SERVICE-DOOR] shader missing, using fallback: " + SHADER_PATH)
	var fb: Shader = Shader.new()
	fb.code = FALLBACK_SHADER
	return fb


func _tex(fname: String) -> Texture2D:
	if _tex_cache.has(fname):
		return _tex_cache[fname] as Texture2D
	var res_p: String = TEX_DIR + fname
	var tex: Texture2D = null
	if ResourceLoader.exists(res_p):
		var loaded: Resource = ResourceLoader.load(res_p)
		if loaded is Texture2D:
			tex = loaded as Texture2D
	if tex == null:
		var abs_p: String = ProjectSettings.globalize_path(res_p)
		if FileAccess.file_exists(abs_p):
			var img: Image = Image.new()
			if img.load(abs_p) == OK and not img.is_empty():
				tex = ImageTexture.create_from_image(img)
	_tex_cache[fname] = tex
	return tex


func _instance_glb(path: String) -> Node3D:
	if ResourceLoader.exists(path):
		var res: Resource = ResourceLoader.load(path)
		if res is PackedScene:
			var inst: Node = (res as PackedScene).instantiate()
			if inst is Node3D:
				_convert_importer_meshes(inst)
				return inst as Node3D
			if inst != null:
				inst.free()
	var abs_p: String = ProjectSettings.globalize_path(path)
	if not FileAccess.file_exists(abs_p):
		push_warning("[SERVICE-DOOR] glb missing, using placeholder frame: " + path)
		return null
	var doc: GLTFDocument = GLTFDocument.new()
	var st: GLTFState = GLTFState.new()
	if doc.append_from_file(abs_p, st) != OK:
		push_warning("[SERVICE-DOOR] glb load failed, using placeholder frame: " + abs_p)
		return null
	var root: Node = doc.generate_scene(st)
	if not (root is Node3D):
		if root != null:
			root.free()
		return null
	_convert_importer_meshes(root)
	return root as Node3D


func _convert_importer_meshes(root: Node) -> void:
	var stack: Array[Node] = [root]
	var imps: Array[ImporterMeshInstance3D] = []
	while not stack.is_empty():
		var c: Node = stack.pop_back()
		if c is ImporterMeshInstance3D:
			imps.append(c as ImporterMeshInstance3D)
		for ch: Node in c.get_children():
			stack.append(ch)
	for imp: ImporterMeshInstance3D in imps:
		var mi: MeshInstance3D = MeshInstance3D.new()
		mi.transform = imp.transform
		mi.mesh = imp.mesh.get_mesh() if imp.mesh != null else null
		var p: Node = imp.get_parent()
		var nm: String = String(imp.name)
		var idx: int = imp.get_index()
		p.remove_child(imp)
		imp.free()
		mi.name = nm
		p.add_child(mi)
		p.move_child(mi, idx)


func _find_mi(root: Node, want: String) -> MeshInstance3D:
	if root == null:
		return null
	var exact: Node = root.find_child(want, true, false)
	if exact is MeshInstance3D:
		return exact as MeshInstance3D
	var stack: Array[Node] = [root]
	var low: String = want.to_lower()
	while not stack.is_empty():
		var c: Node = stack.pop_back()
		var nm: String = String(c.name).to_lower()
		if c is MeshInstance3D and (nm == low or nm.begins_with(low)):
			return c as MeshInstance3D
		for ch: Node in c.get_children():
			stack.append(ch)
	return null


func _find_threshold_mi(root: Node) -> MeshInstance3D:
	if root == null:
		return null
	var stack: Array[Node] = [root]
	while not stack.is_empty():
		var c: Node = stack.pop_back()
		if c is MeshInstance3D and String(c.name).to_lower().contains("threshold"):
			return c as MeshInstance3D
		for ch: Node in c.get_children():
			stack.append(ch)
	return null
