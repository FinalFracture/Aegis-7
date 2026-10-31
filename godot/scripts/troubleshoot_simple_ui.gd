class_name TroubleshootSimpleUI
extends Control
## Simple-tier troubleshoot holo for Hatch Field Emitter D-204.
## Board art is PcbBoardView (res://data/troubleshoot_simple_final_board_geom.json).
## FIELD_PIN commits on Enter or focus-out. There is no RUN button.
## The window closes only from EXIT.

signal field_released(device_id: String)
signal exited

const REF := Vector2(1024.0, 576.0)
const COLOR_BG := Color("#06080E")
const COLOR_CYAN := Color("#2EE6FF")
const COLOR_AMBER := Color("#FFB000")

var device_id: String = "D-204"

var _mono: Font
var _selected: String = ""
var _counts: Dictionary = {"batt": 3, "wire": 6, "jelly": 2}
var _break_repaired: bool = false
var _committed_pin: int = 1
var _won: bool = false
var _release_sent: bool = false
var _closing: bool = false

var _title: Label
var _exit: Button
var _icon: Control
var _caption: Label
var _board_frame: Control
var _board: PcbBoardView
var _cons_frame: Control
var _rows: Array = []
var _code_frame: Control
var _num_labels: Array[Label] = []
var _code_labels: Array[Label] = []
var _pin_prefix: Label
var _pin_edit: LineEdit
var _status: Label
var _footer: Control


func _ready() -> void:
	mouse_filter = Control.MOUSE_FILTER_STOP
	set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	_make_font()
	_build()
	_layout()
	call_deferred("_layout")


func _notification(what: int) -> void:
	if what == NOTIFICATION_RESIZED:
		_layout()


func is_won() -> bool:
	return _won


func is_break_repaired() -> bool:
	return _break_repaired


func status_text() -> String:
	return _status.text if _status != null else ""


func selected_kind() -> String:
	return _selected


func consumable_count(kind: String) -> int:
	return int(_counts.get(kind, 0))


func pad_pos(id: String) -> Vector2:
	if _board != null:
		return _board.pad_pos(id)
	return Vector2.ZERO


func pad_ids() -> Array:
	if _board != null:
		return _board.pad_ids()
	return []


func trace_list() -> Array:
	if _board != null:
		return _board.trace_list()
	return []


func gap_grid() -> PackedVector2Array:
	if _board != null:
		return _board.gap_grid()
	return PackedVector2Array([Vector2(17.6, 7.0), Vector2(19.4, 7.0)])


func select_consumable(kind: String) -> void:
	_selected = kind
	for row in _rows:
		(row as Control).queue_redraw()


func try_repair_from_board() -> void:
	if _selected != "wire" or _break_repaired:
		return
	if consumable_count("wire") <= 0:
		return
	repair_break()


func repair_break() -> void:
	if _break_repaired:
		return
	_break_repaired = true
	var n := consumable_count("wire")
	if n > 0:
		_counts["wire"] = n - 1
	if _board != null:
		_board.break_repaired = true
		_board.queue_redraw()
	for row in _rows:
		(row as Control).queue_redraw()


func commit_pin(text: String) -> void:
	var t := text.strip_edges()
	if _pin_edit != null and _pin_edit.text != t:
		_pin_edit.text = t
	_committed_pin = int(t) if t.is_valid_int() else -1
	_apply_pin()


func press_exit() -> void:
	if _closing:
		return
	_closing = true
	if _pin_edit != null:
		commit_pin(_pin_edit.text)
	exited.emit()
	hide()
	queue_free()


func _apply_pin() -> void:
	if _won:
		return
	if _break_repaired and _committed_pin == 3:
		_won = true
		_set_status("[FIELD RELEASED]", Color("#8CFFC6"))
		if not _release_sent:
			_release_sent = true
			field_released.emit(device_id)
		return
	if _break_repaired:
		_set_status("[FIELD STALLED AT 40%]", COLOR_AMBER)
	else:
		_set_status("", COLOR_AMBER)


func _set_status(text: String, col: Color) -> void:
	if _status == null:
		return
	_status.text = text
	_status.add_theme_color_override("font_color", col)
	_status.visible = text != ""


func _make_font() -> void:
	var sf := SystemFont.new()
	sf.font_names = PackedStringArray(["Consolas", "Cascadia Mono", "Courier New", "DejaVu Sans Mono", "monospace"])
	sf.antialiasing = TextServer.FONT_ANTIALIASING_GRAY
	_mono = sf


func _code_font() -> Font:
	if _mono != null:
		return _mono
	return ThemeDB.fallback_font


func _build() -> void:
	_icon = GlyphIcon.new()
	_icon.name = "DeviceIcon"
	_icon.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(_icon)

	_title = Label.new()
	_title.name = "Title"
	_title.text = "DEVICE: Hatch Field Emitter D-204"
	_title.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	_title.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_title.add_theme_color_override("font_color", Color("#F4F7FB"))
	add_child(_title)

	_exit = Button.new()
	_exit.name = "ExitButton"
	_exit.text = "× EXIT"
	_exit.focus_mode = Control.FOCUS_NONE
	_exit.mouse_default_cursor_shape = Control.CURSOR_POINTING_HAND
	_exit.add_theme_color_override("font_color", Color("#F4F7FB"))
	_exit.add_theme_color_override("font_hover_color", Color("#FFFFFF"))
	_exit.add_theme_color_override("font_pressed_color", Color("#FFFFFF"))
	_exit.pressed.connect(press_exit)
	add_child(_exit)

	_board_frame = HoloFrame.new()
	_board_frame.name = "BoardFrame"
	(_board_frame as HoloFrame).stroke = COLOR_CYAN
	(_board_frame as HoloFrame).bracket = true
	(_board_frame as HoloFrame).bracket_mask = 15
	_board_frame.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(_board_frame)

	var board := PcbBoardView.new()
	board.name = "BoardView"
	board.mouse_filter = Control.MOUSE_FILTER_STOP
	board.gap_pressed.connect(try_repair_from_board)
	_board_frame.add_child(board)
	_board = board

	_caption = Label.new()
	_caption.name = "HoloCaption"
	_caption.text = "HOLO-LINK // SLEEVE 04"
	_caption.horizontal_alignment = HORIZONTAL_ALIGNMENT_RIGHT
	_caption.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	_caption.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_caption.add_theme_color_override("font_color", COLOR_CYAN)
	add_child(_caption)

	_cons_frame = HoloFrame.new()
	_cons_frame.name = "ConsumablesFrame"
	(_cons_frame as HoloFrame).stroke = COLOR_CYAN
	(_cons_frame as HoloFrame).bracket = false
	_cons_frame.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(_cons_frame)
	var kinds: Array[String] = ["batt", "wire", "jelly"]
	for kind in kinds:
		var row := ConsumableRow.new()
		row.kind = kind
		row.host = self
		row.name = "Row_" + kind
		_cons_frame.add_child(row)
		_rows.append(row)

	_code_frame = HoloFrame.new()
	_code_frame.name = "CodeFrame"
	(_code_frame as HoloFrame).stroke = COLOR_AMBER
	(_code_frame as HoloFrame).fill = Color("#120E0A")
	(_code_frame as HoloFrame).scanlines = true
	(_code_frame as HoloFrame).bracket = true
	(_code_frame as HoloFrame).bracket_mask = 12
	(_code_frame as HoloFrame).bracket_color = COLOR_CYAN
	_code_frame.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(_code_frame)

	var sources: PackedStringArray = PackedStringArray([
		"# hatch field emitter D-204 / door controller",
		"FIELD_PIN = ",
		"",
		"def on_power():",
		"    controller.output(FIELD_PIN)",
	])
	for i in 5:
		var num := Label.new()
		num.text = str(i + 1)
		num.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
		num.horizontal_alignment = HORIZONTAL_ALIGNMENT_RIGHT
		num.mouse_filter = Control.MOUSE_FILTER_IGNORE
		num.add_theme_color_override("font_color", Color("#C6A36A"))
		_code_frame.add_child(num)
		_num_labels.append(num)
		if i == 1:
			continue
		var line := Label.new()
		line.text = sources[i]
		line.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
		line.mouse_filter = Control.MOUSE_FILTER_IGNORE
		var col := Color("#A8B5A4") if i == 0 else Color("#E6EDF2")
		line.add_theme_color_override("font_color", col)
		_code_frame.add_child(line)
		_code_labels.append(line)

	_pin_prefix = Label.new()
	_pin_prefix.text = "FIELD_PIN = "
	_pin_prefix.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	_pin_prefix.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_pin_prefix.add_theme_color_override("font_color", Color("#E6EDF2"))
	_code_frame.add_child(_pin_prefix)

	_pin_edit = LineEdit.new()
	_pin_edit.name = "FieldPinEdit"
	_pin_edit.text = "1"
	_pin_edit.alignment = HORIZONTAL_ALIGNMENT_CENTER
	_pin_edit.max_length = 4
	_pin_edit.context_menu_enabled = false
	_pin_edit.select_all_on_focus = true
	_pin_edit.caret_blink = false
	_pin_edit.add_theme_color_override("font_color", Color("#FFE6C2"))
	_pin_edit.add_theme_color_override("font_selected_color", Color("#1A1208"))
	_pin_edit.add_theme_color_override("selection_color", COLOR_AMBER)
	_pin_edit.add_theme_color_override("caret_color", COLOR_AMBER)
	_pin_edit.text_submitted.connect(_on_pin_submitted)
	_pin_edit.focus_exited.connect(_on_pin_focus_exited)
	_code_frame.add_child(_pin_edit)

	_status = Label.new()
	_status.name = "StatusLine"
	_status.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	_status.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_status.visible = false
	_code_frame.add_child(_status)

	_footer = FooterPill.new()
	_footer.name = "NeuralSleeveTab"
	_footer.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(_footer)


func _on_pin_submitted(text: String) -> void:
	commit_pin(text)


func _on_pin_focus_exited() -> void:
	if _closing or _pin_edit == null:
		return
	commit_pin(_pin_edit.text)


func _scale() -> float:
	if size.x < 8.0 or size.y < 8.0:
		return 1.0
	return minf(size.x / REF.x, size.y / REF.y)


func _origin() -> Vector2:
	var s := _scale()
	return Vector2((size.x - REF.x * s) * 0.5, (size.y - REF.y * s) * 0.5)


func _place(node: Control, pos: Vector2, sz: Vector2) -> void:
	node.position = pos
	node.size = sz


func _layout() -> void:
	if _board_frame == null or size.x < 32.0 or size.y < 32.0:
		return
	var s := _scale()
	var o := _origin()
	var font := _code_font()

	_place(_icon, o + Vector2(24, 14) * s, Vector2(32, 32) * s)
	_place(_title, o + Vector2(66, 12) * s, Vector2(760, 36) * s)
	_title.add_theme_font_size_override("font_size", int(maxf(12.0, 22.0 * s)))
	_place(_exit, o + Vector2(888, 13) * s, Vector2(112, 34) * s)
	_exit.add_theme_font_override("font", font)
	_exit.add_theme_font_size_override("font_size", int(maxf(11.0, 15.0 * s)))
	_style_exit(s)

	var board_pos := o + Vector2(20, 58) * s
	var board_sz := Vector2(712, 292) * s
	_place(_board_frame, board_pos, board_sz)
	var bf := _board_frame as HoloFrame
	bf.border_px = maxf(1.5, 2.0 * s)
	bf.radius_px = int(maxf(8.0, 16.0 * s))
	bf.queue_redraw()
	var pad := bf.content_pad()
	_place(_board, Vector2(pad, pad), board_sz - Vector2(pad, pad) * 2.0)

	_place(_caption, o + Vector2(20, 350) * s, Vector2(712, 20) * s)
	_caption.add_theme_font_override("font", font)
	_caption.add_theme_font_size_override("font_size", int(maxf(9.0, 12.0 * s)))

	var cons_pos := o + Vector2(748, 58) * s
	var cons_sz := Vector2(256, 292) * s
	_place(_cons_frame, cons_pos, cons_sz)
	var cf := _cons_frame as HoloFrame
	cf.border_px = maxf(1.5, 2.0 * s)
	cf.radius_px = int(maxf(8.0, 18.0 * s))
	cf.queue_redraw()
	var cpad := cf.content_pad()
	var inner_h := cons_sz.y - cpad * 2.0
	var row_h := inner_h / 3.0
	for i in _rows.size():
		var row := _rows[i] as Control
		_place(row, Vector2(cpad, cpad + row_h * float(i)), Vector2(cons_sz.x - cpad * 2.0, row_h))
		row.queue_redraw()

	var code_pos := o + Vector2(20, 374) * s
	var code_sz := Vector2(712, 158) * s
	_place(_code_frame, code_pos, code_sz)
	var kf := _code_frame as HoloFrame
	kf.border_px = maxf(1.5, 2.0 * s)
	kf.radius_px = int(maxf(8.0, 14.0 * s))
	kf.queue_redraw()
	_layout_code(kf, s, font)

	_place(_footer, o + Vector2(397, 528) * s, Vector2(230, 34) * s)
	_footer.queue_redraw()
	queue_redraw()


func _layout_code(frame: HoloFrame, s: float, font: Font) -> void:
	var inset := frame.content_pad()
	var inner := Rect2(Vector2(inset, inset), frame.size - Vector2(inset, inset) * 2.0)
	if inner.size.y < 8.0:
		return
	var lh := inner.size.y / 6.2
	var fs := int(maxf(10.0, lh * 0.62))
	var num_w := maxf(18.0, 32.0 * s)
	var text_x := inner.position.x + num_w + 8.0 * s
	for i in _num_labels.size():
		var num := _num_labels[i]
		_place(num, Vector2(inner.position.x, inner.position.y + lh * float(i)), Vector2(num_w, lh))
		num.add_theme_font_override("font", font)
		num.add_theme_font_size_override("font_size", fs)
	var code_i := 0
	for i in 5:
		if i == 1:
			continue
		if code_i >= _code_labels.size():
			break
		var line := _code_labels[code_i]
		code_i += 1
		_place(line, Vector2(text_x, inner.position.y + lh * float(i)), Vector2(inner.size.x - num_w - 12.0 * s, lh))
		line.add_theme_font_override("font", font)
		line.add_theme_font_size_override("font_size", fs)
	var prefix_w := font.get_string_size("FIELD_PIN = ", HORIZONTAL_ALIGNMENT_LEFT, -1, fs).x
	_place(_pin_prefix, Vector2(text_x, inner.position.y + lh), Vector2(prefix_w + 2.0, lh))
	_pin_prefix.add_theme_font_override("font", font)
	_pin_prefix.add_theme_font_size_override("font_size", fs)
	var edit_h := lh * 0.78
	var edit_w := maxf(28.0 * s, fs * 1.7)
	_place(_pin_edit, Vector2(text_x + prefix_w, inner.position.y + lh + (lh - edit_h) * 0.5), Vector2(edit_w, edit_h))
	_pin_edit.add_theme_font_override("font", font)
	_pin_edit.add_theme_font_size_override("font_size", fs)
	_style_pin(s)
	_place(_status, Vector2(text_x, inner.position.y + lh * 5.05), Vector2(inner.size.x - num_w - 12.0 * s, lh))
	_status.add_theme_font_override("font", font)
	_status.add_theme_font_size_override("font_size", fs)


func _style_exit(s: float) -> void:
	var normal := _exit_box(s, Color("#D5DCE6"), Color(0.06, 0.08, 0.12, 0.94))
	var hover := _exit_box(s, Color("#FFFFFF"), Color(0.10, 0.13, 0.18, 0.96))
	var pressed := _exit_box(s, COLOR_CYAN, Color(0.05, 0.10, 0.14, 0.96))
	_exit.add_theme_stylebox_override("normal", normal)
	_exit.add_theme_stylebox_override("hover", hover)
	_exit.add_theme_stylebox_override("pressed", pressed)
	_exit.add_theme_stylebox_override("focus", normal)
	_exit.add_theme_stylebox_override("disabled", normal)


func _exit_box(s: float, border: Color, bg: Color) -> StyleBoxFlat:
	var sb := StyleBoxFlat.new()
	sb.bg_color = bg
	sb.border_color = border
	sb.set_border_width_all(maxi(1, int(s + 0.5)))
	sb.set_corner_radius_all(maxi(4, int(8.0 * s)))
	sb.content_margin_left = 8.0 * s
	sb.content_margin_right = 8.0 * s
	return sb


func _style_pin(s: float) -> void:
	var normal := _pin_box(s, false)
	var hot := _pin_box(s, true)
	_pin_edit.add_theme_stylebox_override("normal", normal)
	_pin_edit.add_theme_stylebox_override("focus", hot)
	_pin_edit.add_theme_stylebox_override("read_only", normal)


func _pin_box(s: float, hot: bool) -> StyleBoxFlat:
	var sb := StyleBoxFlat.new()
	sb.bg_color = Color("#2A1C08")
	sb.border_color = Color("#FFD56A") if hot else COLOR_AMBER
	sb.set_border_width_all(maxi(1, int(maxf(1.0, 2.0 * s))))
	sb.set_corner_radius_all(maxi(2, int(3.0 * s)))
	sb.content_margin_left = 2.0
	sb.content_margin_right = 2.0
	sb.content_margin_top = 0.0
	sb.content_margin_bottom = 0.0
	return sb


func _draw() -> void:
	draw_rect(Rect2(Vector2.ZERO, size), COLOR_BG, true)
	var s := _scale()
	var band_h := 40.0 * s
	draw_rect(Rect2(0.0, size.y - band_h, size.x, band_h), Color("#241C16"), true)


class HoloFrame extends Control:
	var stroke: Color = Color("#2EE6FF")
	var fill: Color = Color(0, 0, 0, 0)
	var border_px: float = 2.0
	var radius_px: int = 14
	var bracket: bool = true
	var bracket_mask: int = 15
	var bracket_color: Color = Color("#2EE6FF")
	var scanlines: bool = false

	func _arm() -> float:
		return clampf(minf(size.x, size.y) * 0.055, 8.0, 20.0)

	func content_pad() -> float:
		var inset := _arm() * 0.55 if bracket else 2.0
		return inset + border_px + 6.0

	func _draw() -> void:
		if size.x < 8.0 or size.y < 8.0:
			return
		var arm := _arm()
		var inset := arm * 0.55 if bracket else 2.0
		var inner := Rect2(Vector2(inset, inset), size - Vector2(inset, inset) * 2.0)
		if inner.size.x < 4.0 or inner.size.y < 4.0:
			return
		var sb := StyleBoxFlat.new()
		sb.bg_color = fill
		sb.border_color = stroke
		sb.set_border_width_all(maxi(1, int(border_px + 0.5)))
		sb.set_corner_radius_all(maxi(2, radius_px))
		sb.anti_aliasing = true
		draw_style_box(sb, inner)
		if scanlines and fill.a > 0.01:
			var y := inner.position.y + 4.0
			var line_c := Color(1, 0.9, 0.7, 0.045)
			while y < inner.end.y:
				draw_line(Vector2(inner.position.x + 8.0, y), Vector2(inner.end.x - 8.0, y), line_c, 1.0, false)
				y += 4.0
		if not bracket:
			return
		var w := maxf(1.5, border_px)
		var col := bracket_color
		if bracket_mask & 1:
			draw_polyline(PackedVector2Array([Vector2(1, arm), Vector2(1, 1), Vector2(arm, 1)]), col, w, true)
		if bracket_mask & 2:
			draw_polyline(PackedVector2Array([Vector2(size.x - arm, 1), Vector2(size.x - 1, 1), Vector2(size.x - 1, arm)]), col, w, true)
		if bracket_mask & 4:
			draw_polyline(PackedVector2Array([Vector2(1, size.y - arm), Vector2(1, size.y - 1), Vector2(arm, size.y - 1)]), col, w, true)
		if bracket_mask & 8:
			draw_polyline(PackedVector2Array([Vector2(size.x - arm, size.y - 1), Vector2(size.x - 1, size.y - 1), Vector2(size.x - 1, size.y - arm)]), col, w, true)


class GlyphIcon extends Control:
	func _draw() -> void:
		if size.x < 4.0 or size.y < 4.0:
			return
		var col := TroubleshootSimpleUI.COLOR_CYAN
		var sb := StyleBoxFlat.new()
		sb.bg_color = Color(0, 0, 0, 0)
		sb.border_color = col
		sb.set_border_width_all(maxi(1, int(size.y * 0.08)))
		sb.set_corner_radius_all(maxi(2, int(size.y * 0.22)))
		draw_style_box(sb, Rect2(Vector2(1, 1), size - Vector2(2, 2)))
		var bw := size.x * 0.11
		var bh := size.y * 0.40
		var y := (size.y - bh) * 0.5
		var gap := size.x * 0.10
		var x0 := size.x * 0.5 - gap * 0.5 - bw
		draw_rect(Rect2(x0, y, bw, bh), col, true)
		draw_rect(Rect2(x0 + bw + gap, y, bw, bh), col, true)


class FooterPill extends Control:
	func _draw() -> void:
		if size.y < 4.0:
			return
		var sb := StyleBoxFlat.new()
		sb.bg_color = Color(0.08, 0.12, 0.16, 0.94)
		sb.border_color = Color(0.18, 0.78, 0.88, 0.45)
		sb.set_border_width_all(1)
		sb.set_corner_radius_all(int(size.y * 0.5))
		draw_style_box(sb, Rect2(Vector2.ZERO, size))
		var font := ThemeDB.fallback_font
		var fs := int(maxf(10.0, size.y * 0.40))
		var text := "#04 NEURAL SLEEVE"
		var sz := font.get_string_size(text, HORIZONTAL_ALIGNMENT_LEFT, -1, fs)
		var pos := Vector2((size.x - sz.x) * 0.5, (size.y + font.get_ascent(fs) - font.get_descent(fs)) * 0.5)
		draw_string(font, pos, text, HORIZONTAL_ALIGNMENT_LEFT, -1, fs, TroubleshootSimpleUI.COLOR_CYAN)


class ConsumableRow extends Control:
	var kind: String = "wire"
	var host: TroubleshootSimpleUI

	func _ready() -> void:
		mouse_filter = Control.MOUSE_FILTER_STOP
		mouse_default_cursor_shape = Control.CURSOR_POINTING_HAND

	func _gui_input(event: InputEvent) -> void:
		if host == null or not (event is InputEventMouseButton):
			return
		var mb := event as InputEventMouseButton
		if mb.pressed and mb.button_index == MOUSE_BUTTON_LEFT:
			host.select_consumable(kind)
			accept_event()

	func _draw() -> void:
		if host == null or size.y < 8.0:
			return
		if host.selected_kind() == kind:
			var hi := StyleBoxFlat.new()
			hi.bg_color = Color(0.18, 0.85, 1.0, 0.12)
			hi.border_color = TroubleshootSimpleUI.COLOR_CYAN
			hi.set_border_width_all(maxi(1, int(size.y * 0.04)))
			hi.set_corner_radius_all(int(size.y * 0.18))
			var m := size.y * 0.08
			draw_style_box(hi, Rect2(Vector2(m, m), size - Vector2(m, m) * 2.0))
		var col := Color("#E7EBF0")
		var ih := size.y * 0.36
		var ic := Vector2(size.y * 0.62, size.y * 0.50)
		if kind == "batt":
			_battery(ic, ih, col)
		elif kind == "wire":
			_coil(ic, ih, col)
		else:
			_drop(ic, ih, col)
		var font := ThemeDB.fallback_font
		var fs := int(maxf(12.0, size.y * 0.32))
		var text := "×%d" % host.consumable_count(kind)
		var baseline := size.y * 0.5 + (font.get_ascent(fs) - font.get_descent(fs)) * 0.5
		draw_string(font, Vector2(size.y * 1.25, baseline), text, HORIZONTAL_ALIGNMENT_LEFT, -1, fs, col)

	func _battery(c: Vector2, h: float, col: Color) -> void:
		var body := Rect2(c.x - h * 0.95, c.y - h * 0.42, h * 1.55, h * 0.84)
		var sb := StyleBoxFlat.new()
		sb.bg_color = Color(0, 0, 0, 0)
		sb.border_color = col
		sb.set_border_width_all(maxi(1, int(h * 0.12)))
		sb.set_corner_radius_all(maxi(2, int(h * 0.18)))
		draw_style_box(sb, body)
		var nub_h := h * 0.30
		var nub := Rect2(body.end.x + h * 0.04, c.y - nub_h * 0.5, h * 0.18, nub_h)
		draw_rect(nub, col, true)

	func _coil(c: Vector2, h: float, col: Color) -> void:
		var r := h * 0.30
		var w := maxf(1.25, h * 0.10)
		var x0 := c.x - r * 1.55
		var y := c.y + r * 0.02
		for i in 3:
			draw_arc(Vector2(x0 + float(i) * r * 1.45, y), r, PI, TAU, 14, col, w, true)
		draw_line(Vector2(x0 - r * 0.15, y), Vector2(x0 + r * 2.95, y), col, w, true)

	func _drop(c: Vector2, h: float, col: Color) -> void:
		var shape: Array[Vector2] = [
			Vector2(0, -0.52), Vector2(0.16, -0.28), Vector2(0.32, -0.02),
			Vector2(0.30, 0.20), Vector2(0.14, 0.38), Vector2(0, 0.46),
			Vector2(-0.14, 0.38), Vector2(-0.30, 0.20), Vector2(-0.32, -0.02),
			Vector2(-0.16, -0.28), Vector2(0, -0.52),
		]
		var pts := PackedVector2Array()
		for v in shape:
			pts.append(c + v * h)
		draw_polyline(pts, col, maxf(1.25, h * 0.10), true)
