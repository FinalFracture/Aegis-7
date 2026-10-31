class_name PcbBoardView
extends Control
## Hatch Field Emitter board. Pad, trace, and gap coordinates come only from
## res://data/troubleshoot_simple_final_board_geom.json (5 nets, 12 pads).
## gap_pressed fires on a click along the open span. The host decides what that does.

signal gap_pressed

const GEOM_PATH := "res://data/troubleshoot_simple_final_board_geom.json"
const COLOR_PCB := Color("#1E4D3A")
const COLOR_SILK := Color("#F3F0E6")
const COLOR_NEON := Color("#3EC8FF")
const COLOR_PAD := Color("#C5CCD2")
const COLOR_PAD_EDGE := Color("#7A848C")
## Visual pad radius at the design's 40 px/grid (electrical r in the geom is the clearance disk).
const PAD_VIS_R := 15.0 / 40.0
## Silkscreen stroke centerline sits this far from a near-edge pad center (15 px pad + 7.5 px gap + 1.5 px half-stroke).
const SILK_OFF := 0.6
const SILK_W := 3.0 / 40.0
const VIEW_MIN := Vector2(1.0, 0.35)
const VIEW_MAX := Vector2(30.2, 12.45)

## Hosts set this when the open span has been bridged. Drawing reads it.
var break_repaired: bool = false

var _geom: Dictionary = {}
var _pad_xy: Dictionary = {}
var _origin: Vector2 = Vector2.ZERO
var _px: float = 1.0


func _ready() -> void:
	_load_geom()
	queue_redraw()


func pad_pos(id: String) -> Vector2:
	if _pad_xy.has(id):
		return _pad_xy[id] as Vector2
	return Vector2.ZERO


func pad_ids() -> Array:
	return _pad_xy.keys()


func trace_list() -> Array:
	return _geom.get("traces", []) as Array


func gap_grid() -> PackedVector2Array:
	var out := PackedVector2Array()
	var opens: Array = _geom.get("expected_open", []) as Array
	if not opens.is_empty() and opens[0] is Dictionary:
		var gap: Array = (opens[0] as Dictionary).get("gap", []) as Array
		for item in gap:
			if item is Array and (item as Array).size() >= 2:
				var xy: Array = item
				out.append(Vector2(float(xy[0]), float(xy[1])))
	if out.size() < 2:
		out = PackedVector2Array([Vector2(17.6, 7.0), Vector2(19.4, 7.0)])
	return out


func _load_geom() -> void:
	var f := FileAccess.open(GEOM_PATH, FileAccess.READ)
	if f == null:
		push_error("PcbBoardView: missing " + GEOM_PATH)
		return
	var parsed: Variant = JSON.parse_string(f.get_as_text())
	f.close()
	if not (parsed is Dictionary):
		push_error("PcbBoardView: bad geom json")
		return
	_geom = parsed
	_pad_xy.clear()
	for item in (_geom.get("pads", []) as Array):
		if not (item is Dictionary):
			continue
		var pad: Dictionary = item
		_pad_xy[String(pad.get("id", ""))] = Vector2(float(pad.get("x", 0.0)), float(pad.get("y", 0.0)))


func _gui_input(event: InputEvent) -> void:
	if not (event is InputEventMouseButton):
		return
	var mb := event as InputEventMouseButton
	if mb.pressed and mb.button_index == MOUSE_BUTTON_LEFT and _hits_gap(mb.position):
		gap_pressed.emit()
		accept_event()


func _draw() -> void:
	if not _prepare_map():
		return
	_pcb()
	_silk_boxes()
	var out3 := PackedVector2Array()
	var out3_w := 0.5
	for item in trace_list():
		if not (item is Dictionary):
			continue
		var tr: Dictionary = item
		var net := String(tr.get("net", ""))
		var grid := PackedVector2Array()
		for p in (tr.get("pts", []) as Array):
			if p is Array and (p as Array).size() >= 2:
				var xy: Array = p
				grid.append(Vector2(float(xy[0]), float(xy[1])))
		if break_repaired and net == "OUT3":
			out3_w = float(tr.get("w", out3_w))
			for g in grid:
				if out3.is_empty() or out3[out3.size() - 1].distance_to(g) > 0.001:
					out3.append(g)
			continue
		_neon(grid, float(tr.get("w", 0.5)))
	if break_repaired and out3.size() >= 2:
		_neon(out3, out3_w)
	elif not break_repaired:
		var gap := gap_grid()
		if gap.size() >= 2:
			_burn(gap[0], gap[1])
	_pads()
	_silk_labels()


func _prepare_map() -> bool:
	if size.x < 8.0 or size.y < 8.0:
		return false
	var margin := 6.0
	var area := Rect2(margin, margin, size.x - margin * 2.0, size.y - margin * 2.0)
	var span := VIEW_MAX - VIEW_MIN
	_px = minf(area.size.x / span.x, area.size.y / span.y)
	var used := span * _px
	_origin = area.position + (area.size - used) * 0.5
	return _px > 0.0


func _map(g: Vector2) -> Vector2:
	return _origin + (g - VIEW_MIN) * _px


func _hits_gap(local: Vector2) -> bool:
	if not _prepare_map():
		return false
	var gap := gap_grid()
	if gap.size() < 2:
		return false
	return _dist_seg(local, _map(gap[0]), _map(gap[1])) <= maxf(14.0, _px * 0.7)


func _dist_seg(p: Vector2, a: Vector2, b: Vector2) -> float:
	var ab := b - a
	var den := ab.length_squared()
	if den < 0.001:
		return p.distance_to(a)
	var t := clampf((p - a).dot(ab) / den, 0.0, 1.0)
	return p.distance_to(a + ab * t)


func _pcb() -> void:
	var sb := StyleBoxFlat.new()
	sb.bg_color = COLOR_PCB
	sb.set_corner_radius_all(int(clampf(minf(size.x, size.y) * 0.035, 8.0, 26.0)))
	draw_style_box(sb, Rect2(Vector2(1, 1), size - Vector2(2, 2)))
	var y := 4.0
	var shade := Color(0, 0, 0, 0.14)
	while y < size.y:
		draw_line(Vector2(6.0, y), Vector2(size.x - 6.0, y), shade, 1.0, false)
		y += 3.0
	var hole := maxf(2.0, _px * 0.09)
	var inset := hole + 8.0
	var hole_c := Color("#0E2E24")
	for c in [Vector2(inset, inset), Vector2(size.x - inset, inset), Vector2(inset, size.y - inset), Vector2(size.x - inset, size.y - inset)]:
		draw_circle(c, hole, hole_c)


func _neon(grid: PackedVector2Array, width_grid: float) -> void:
	if grid.size() < 2:
		return
	var pts := PackedVector2Array()
	for g in grid:
		pts.append(_map(g))
	var w := maxf(1.0, width_grid * _px)
	var glow := Color(COLOR_NEON.r, COLOR_NEON.g, COLOR_NEON.b, 0.18)
	draw_polyline(pts, glow, w * 1.85, true)
	draw_polyline(pts, COLOR_NEON, w, true)


func _burn(a: Vector2, b: Vector2) -> void:
	var d := b - a
	var length := d.length()
	if length < 0.05:
		return
	var dir := d / length
	var n := Vector2(-dir.y, dir.x)
	if n.y > 0.0:
		n = -n
	var inset := length * 0.10
	var a2 := a + dir * inset
	var b2 := b - dir * inset
	for i in 6:
		var t := float(i) / 5.0
		var wobble := n * (0.05 if i % 2 == 0 else -0.04)
		var rad := _px * (0.20 + 0.04 * float(i % 3))
		draw_circle(_map(a2.lerp(b2, t) + wobble), rad, Color("#120C09"))
		draw_circle(_map(a2.lerp(b2, t) + wobble * 0.4), rad * 0.62, Color("#3A2418"))
	var flecks: Array[Vector2] = [
		Vector2(0.16, -0.14), Vector2(0.33, 0.12), Vector2(0.47, -0.08),
		Vector2(0.62, 0.16), Vector2(0.76, -0.13), Vector2(0.40, 0.20),
	]
	var cols: Array[Color] = [Color("#8A5A32"), Color("#C48A52"), Color("#6E4428"), Color("#A56B3C")]
	var pix_dir := (_map(a + dir) - _map(a)).normalized()
	var pix_n := (_map(a + n) - _map(a)).normalized()
	for i in flecks.size():
		var f: Vector2 = flecks[i]
		var p := _map(a2.lerp(b2, f.x) + n * f.y)
		var tip := pix_dir * _px * 0.09 + pix_n * _px * (0.035 if i % 2 == 0 else -0.03)
		draw_line(p - tip, p + tip, cols[i % cols.size()], maxf(1.0, _px * 0.04), true)
	_curl(a, dir, n)
	_curl(b, -dir, n)


func _curl(end: Vector2, away: Vector2, up: Vector2) -> void:
	var tip := _map(end + away * 0.22 + up * 0.18)
	var root := _map(end)
	var pix_up := (_map(end + up) - _map(end)).normalized()
	draw_line(root, tip + pix_up * _px * 0.03, Color("#3A2416"), maxf(1.4, _px * 0.09), true)
	draw_line(root, tip, Color("#B8733A"), maxf(1.1, _px * 0.065), true)


func _pads() -> void:
	for id in pad_ids():
		_pad_ring(pad_pos(String(id)))


func _pad_ring(g: Vector2) -> void:
	var c := _map(g)
	var r := PAD_VIS_R * _px
	draw_circle(c, r, COLOR_PAD)
	draw_circle(c, r * 0.80, COLOR_PAD_EDGE)
	draw_circle(c, r * 0.50, COLOR_PCB)
	draw_arc(c, r, 0.0, TAU, 28, Color("#5E676E"), maxf(1.0, _px * 0.03), true)


func _rect_grid(left: float, top: float, right: float, bottom: float, col: Color, width: float) -> void:
	var a := _map(Vector2(left, top))
	var b := _map(Vector2(right, bottom))
	draw_rect(Rect2(a, b - a), col, false, width, true)


func _silk_boxes() -> void:
	var sw := maxf(1.0, SILK_W * _px)
	var jp := pad_pos("J1.+")
	var jm := pad_pos("J1.-")
	_rect_grid(jp.x - 1.55, jp.y - SILK_OFF, jp.x + 1.55, jm.y + SILK_OFF, COLOR_SILK, sw)
	var vin := pad_pos("U1.VIN")
	var pr := pad_pos("U1.P1")
	var ug := pad_pos("U1.GND")
	_rect_grid(vin.x - 1.25, vin.y - SILK_OFF, pr.x + SILK_OFF, ug.y + SILK_OFF, COLOR_SILK, sw)
	var inn := pad_pos("FE1.IN")
	_rect_grid(inn.x - SILK_OFF, inn.y - 2.15, inn.x + 3.15, inn.y + 1.85, COLOR_SILK, sw)


func _silk_labels() -> void:
	var col := COLOR_SILK
	var jp := pad_pos("J1.+")
	var jm := pad_pos("J1.-")
	var vin := pad_pos("U1.VIN")
	var p1 := pad_pos("U1.P1")
	var p2 := pad_pos("U1.P2")
	var p3 := pad_pos("U1.P3")
	var ug := pad_pos("U1.GND")
	var inn := pad_pos("FE1.IN")
	var g1 := pad_pos("GND1")
	var g2 := pad_pos("GND2")
	var g3 := pad_pos("GND3")
	_text(Vector2(jp.x, jp.y - SILK_OFF - 0.38), "J1", 0.40, col, HORIZONTAL_ALIGNMENT_CENTER)
	var u_cx := (vin.x - 1.25 + p1.x + SILK_OFF) * 0.5
	_text(Vector2(u_cx, vin.y - SILK_OFF - 0.38), "U1", 0.40, col, HORIZONTAL_ALIGNMENT_CENTER)
	_text(Vector2(inn.x - SILK_OFF, inn.y - 2.15 - 0.36), "FE1", 0.40, col, HORIZONTAL_ALIGNMENT_LEFT)
	_text(Vector2(jp.x, jp.y - 0.50), "+", 0.28, col, HORIZONTAL_ALIGNMENT_CENTER)
	_text(Vector2(jm.x - 0.62, jm.y), "−", 0.30, col, HORIZONTAL_ALIGNMENT_CENTER)
	_text(Vector2(jp.x, (jp.y + jm.y) * 0.5 - 0.28), "GRID", 0.36, col, HORIZONTAL_ALIGNMENT_CENTER)
	_text(Vector2(jp.x, (jp.y + jm.y) * 0.5 + 0.28), "POWER", 0.36, col, HORIZONTAL_ALIGNMENT_CENTER)
	_text(Vector2(vin.x, vin.y + 0.62), "VIN", 0.32, col, HORIZONTAL_ALIGNMENT_CENTER)
	_text(Vector2(p1.x - 0.78, p1.y), "1", 0.32, col, HORIZONTAL_ALIGNMENT_CENTER)
	_text(Vector2(p2.x - 0.78, p2.y), "2", 0.32, col, HORIZONTAL_ALIGNMENT_CENTER)
	_text(Vector2(p3.x - 0.78, p3.y), "3", 0.32, col, HORIZONTAL_ALIGNMENT_CENTER)
	_text(Vector2(ug.x + 0.78, ug.y), "GND", 0.30, col, HORIZONTAL_ALIGNMENT_LEFT)
	var ctrl := Vector2((vin.x - 0.4 + p1.x - 0.9) * 0.5, (p1.y + p3.y) * 0.5)
	_text(ctrl, "CONTROLLER", 0.34, col, HORIZONTAL_ALIGNMENT_CENTER)
	_text(Vector2(inn.x + 0.72, inn.y), "IN", 0.32, col, HORIZONTAL_ALIGNMENT_LEFT)
	var glyph := _map(Vector2(inn.x + 2.15, inn.y))
	var gw := maxf(1.1, _px * 0.055)
	for i in 3:
		draw_arc(glyph, _px * (0.22 + float(i) * 0.20), -0.95, 0.95, 16, col, gw, true)
	draw_circle(_map(vin + Vector2(-0.78, 0.0)), maxf(1.4, _px * 0.065), col)
	_text(Vector2(29.45, inn.y + 2.55), "FIELD EMITTER", 0.40, col, HORIZONTAL_ALIGNMENT_RIGHT)
	_ground(g1, col)
	_ground(g2, col)
	_ground(g3, col)
	_text(Vector2((g2.x + g3.x) * 0.5, g2.y + 1.35), "D-204 REV C", 0.32, col, HORIZONTAL_ALIGNMENT_CENTER)


func _ground(g: Vector2, col: Color) -> void:
	var c := _map(g)
	var w := maxf(1.0, _px * 0.055)
	var y0 := c.y + PAD_VIS_R * _px + _px * 0.08
	var widths: Array[float] = [0.62, 0.40, 0.20]
	for i in 3:
		var y := y0 + float(i) * _px * 0.15
		var hw := _px * widths[i] * 0.5
		draw_line(Vector2(c.x - hw, y), Vector2(c.x + hw, y), col, w, true)


func _text(g: Vector2, text: String, fs_grid: float, col: Color, h_align: int) -> void:
	var font := ThemeDB.fallback_font
	var fs := int(maxf(8.0, fs_grid * _px))
	var sz := font.get_string_size(text, HORIZONTAL_ALIGNMENT_LEFT, -1, fs)
	var baseline := _map(g).y + (font.get_ascent(fs) - font.get_descent(fs)) * 0.5
	var x := _map(g).x
	if h_align == HORIZONTAL_ALIGNMENT_CENTER:
		x -= sz.x * 0.5
	elif h_align == HORIZONTAL_ALIGNMENT_RIGHT:
		x -= sz.x
	draw_string(font, Vector2(x, baseline), text, HORIZONTAL_ALIGNMENT_LEFT, -1, fs, col)
