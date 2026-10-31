# DEPRECATED (5DB-01): replaced by scenes/ui/troubleshoot_simple.tscn; not referenced by any scene.
class_name PcbaPythonPuzzleUI
extends CanvasLayer
## Field diagnostic console. The board is PcbBoardView (netlist geom).
## Pin seating, supply_amperage, and EXECUTE keep the existing rules.
## door_unlocked fires from execute when evaluate_enable_field passes and the reset pin is seated.
## Labels name the device, EXIT, and the live control state. They do not name a solving pin, amperage, or part.

signal door_unlocked(final_amperage: int)

var _root_control: Control
var _status_banner: Label
var _pin_buttons: Dictionary = {}
var _amp_button: Button
var _run_button: Button
var _close_button: Button

var reset_pin_connected: bool = true
var supply_amperage: int = 12
var comparator_gt: bool = true


func _ready() -> void:
	layer = 10
	_build_ui()
	_refresh_ui_state()


func set_Overlay_visible(vis: bool) -> void:
	visible = vis
	if _root_control != null:
		_root_control.visible = vis


func _pin_caption(pname: String) -> String:
	var seated := pname == "RESET" and reset_pin_connected
	return "[PIN: %s]\n%s" % [pname, "SEATED" if seated else "OPEN"]


func _build_ui() -> void:
	_root_control = Control.new()
	_root_control.name = "DiagnosticConsoleRoot"
	_root_control.set_anchors_preset(Control.PRESET_FULL_RECT)
	add_child(_root_control)

	var backdrop_dim: ColorRect = ColorRect.new()
	backdrop_dim.color = Color(0.03, 0.06, 0.10, 0.42)
	backdrop_dim.set_anchors_preset(Control.PRESET_FULL_RECT)
	_root_control.add_child(backdrop_dim)

	var frame: Panel = Panel.new()
	frame.name = "ConsoleMainFrame"
	frame.position = Vector2(154, 86)
	frame.size = Vector2(1612, 908)
	var fstyle: StyleBoxFlat = StyleBoxFlat.new()
	fstyle.bg_color = Color(0.06, 0.09, 0.13, 0.95)
	fstyle.border_color = Color("#00E5FF")
	fstyle.set_border_width_all(3)
	fstyle.set_corner_radius_all(12)
	frame.add_theme_stylebox_override("panel", fstyle)
	_root_control.add_child(frame)

	var header_bg: Panel = Panel.new()
	header_bg.position = Vector2(12, 12)
	header_bg.size = Vector2(1588, 66)
	var hstyle: StyleBoxFlat = StyleBoxFlat.new()
	hstyle.bg_color = Color(0.09, 0.14, 0.20, 1.0)
	hstyle.border_color = Color("#FFB703")
	hstyle.border_width_bottom = 3
	hstyle.set_corner_radius_all(8)
	header_bg.add_theme_stylebox_override("panel", hstyle)
	frame.add_child(header_bg)

	var title_lbl: Label = Label.new()
	title_lbl.name = "Title"
	title_lbl.position = Vector2(22, 10)
	title_lbl.text = "AEGIS-7 FIELD DIAGNOSTIC CONSOLE // SECTOR-04 FIELD EMITTER [WRIST RIG #04 NEURAL SLEEVE COUPLED]"
	title_lbl.add_theme_font_size_override("font_size", 21)
	title_lbl.add_theme_color_override("font_color", Color("#F0F6FF"))
	header_bg.add_child(title_lbl)

	_close_button = Button.new()
	_close_button.name = "ExitButton"
	_close_button.position = Vector2(1430, 12)
	_close_button.size = Vector2(144, 42)
	_close_button.text = "EXIT"
	_close_button.pressed.connect(func() -> void: set_Overlay_visible(false))
	header_bg.add_child(_close_button)

	var left_panel: Panel = Panel.new()
	left_panel.name = "LeftPcbaPanel"
	left_panel.position = Vector2(20, 92)
	left_panel.size = Vector2(776, 736)
	var lstyle: StyleBoxFlat = StyleBoxFlat.new()
	lstyle.bg_color = Color(0.05, 0.18, 0.14, 1.0)
	lstyle.border_color = Color("#00E676")
	lstyle.set_border_width_all(2)
	lstyle.set_corner_radius_all(8)
	left_panel.add_theme_stylebox_override("panel", lstyle)
	frame.add_child(left_panel)

	var board := PcbBoardView.new()
	board.name = "BoardView"
	board.position = Vector2(14, 12)
	board.size = Vector2(748, 596)
	board.mouse_filter = Control.MOUSE_FILTER_IGNORE
	left_panel.add_child(board)

	var j4_label: Label = Label.new()
	j4_label.name = "J4Label"
	j4_label.position = Vector2(18, 616)
	j4_label.text = "J4"
	j4_label.add_theme_font_size_override("font_size", 15)
	j4_label.add_theme_color_override("font_color", Color("#A8F0D8"))
	left_panel.add_child(j4_label)

	var pin_names := ["GND", "LOCK_HOLD", "RESET", "AUX_BUZZ"]
	for i: int in range(pin_names.size()):
		var pname: String = pin_names[i]
		var btn: Button = Button.new()
		btn.name = "Pin_" + pname
		btn.position = Vector2(18 + i * 188, 646)
		btn.size = Vector2(176, 72)
		btn.text = _pin_caption(pname)
		btn.add_theme_font_size_override("font_size", 15)
		btn.pressed.connect(_on_pin_pressed.bind(pname))
		left_panel.add_child(btn)
		_pin_buttons[pname] = btn

	var right_panel: Panel = Panel.new()
	right_panel.name = "RightPythonPanel"
	right_panel.position = Vector2(816, 92)
	right_panel.size = Vector2(776, 736)
	var rstyle: StyleBoxFlat = StyleBoxFlat.new()
	rstyle.bg_color = Color(0.05, 0.08, 0.13, 1.0)
	rstyle.border_color = Color("#00E5FF")
	rstyle.set_border_width_all(2)
	rstyle.set_corner_radius_all(8)
	right_panel.add_theme_stylebox_override("panel", rstyle)
	frame.add_child(right_panel)

	# ui_python_code_editor_panel.png stays on disk. It prints the winning pin, part, and amperage, so it is not shown.
	var py_ctrl_lbl: Label = Label.new()
	py_ctrl_lbl.name = "FirmwareLabel"
	py_ctrl_lbl.position = Vector2(18, 616)
	py_ctrl_lbl.text = "field_control.py"
	py_ctrl_lbl.add_theme_font_size_override("font_size", 15)
	py_ctrl_lbl.add_theme_color_override("font_color", Color("#88E8FF"))
	right_panel.add_child(py_ctrl_lbl)

	_amp_button = Button.new()
	_amp_button.name = "AmperageButton"
	_amp_button.position = Vector2(18, 646)
	_amp_button.size = Vector2(368, 72)
	_amp_button.add_theme_font_size_override("font_size", 16)
	_amp_button.pressed.connect(_on_toggle_amperage)
	right_panel.add_child(_amp_button)

	_run_button = Button.new()
	_run_button.name = "ExecuteButton"
	_run_button.position = Vector2(404, 646)
	_run_button.size = Vector2(354, 72)
	_run_button.text = "EXECUTE"
	_run_button.add_theme_font_size_override("font_size", 16)
	_run_button.add_theme_color_override("font_color", Color("#F0F6FF"))
	_run_button.pressed.connect(_on_execute_field_script)
	right_panel.add_child(_run_button)

	var footer_panel: Panel = Panel.new()
	footer_panel.position = Vector2(20, 838)
	footer_panel.size = Vector2(1572, 56)
	var foot_style: StyleBoxFlat = StyleBoxFlat.new()
	foot_style.bg_color = Color(0.04, 0.14, 0.12, 1.0)
	foot_style.border_color = Color("#00E676")
	foot_style.set_border_width_all(2)
	foot_style.set_corner_radius_all(8)
	footer_panel.add_theme_stylebox_override("panel", foot_style)
	frame.add_child(footer_panel)

	_status_banner = Label.new()
	_status_banner.name = "StatusBanner"
	_status_banner.position = Vector2(20, 14)
	_status_banner.add_theme_font_size_override("font_size", 19)
	_status_banner.add_theme_color_override("font_color", Color("#00E676"))
	footer_panel.add_child(_status_banner)


func _on_pin_pressed(pname: String) -> void:
	reset_pin_connected = (pname == "RESET")
	_refresh_ui_state()


func _on_toggle_amperage() -> void:
	supply_amperage = 12 if supply_amperage <= 10 else 7
	_refresh_ui_state()


func _on_execute_field_script() -> void:
	var result: bool = evaluate_enable_field(supply_amperage) and reset_pin_connected
	if result:
		emit_signal("door_unlocked", supply_amperage)
	_refresh_ui_state()


func evaluate_enable_field(amperage: int) -> bool:
	if comparator_gt:
		if amperage > 10:
			return true
		else:
			return false
	else:
		if amperage < 10:
			return true
		else:
			return false


func _refresh_ui_state() -> void:
	for pname: String in _pin_buttons.keys():
		var btn: Button = _pin_buttons[pname] as Button
		var seated: bool = pname == "RESET" and reset_pin_connected
		btn.text = _pin_caption(pname)
		btn.add_theme_color_override("font_color", Color("#00E676") if seated else Color("#B0C4D8"))

	if _amp_button != null:
		_amp_button.text = "supply_amperage = %d" % supply_amperage
		_amp_button.add_theme_color_override("font_color", Color("#FFD166"))

	var is_open: bool = evaluate_enable_field(supply_amperage) and reset_pin_connected
	if _status_banner != null:
		if is_open:
			_status_banner.text = "[FIELD RELEASED]"
			_status_banner.add_theme_color_override("font_color", Color("#00E676"))
		else:
			_status_banner.text = "[FIELD STALLED AT 40%]"
			_status_banner.add_theme_color_override("font_color", Color("#FF9500"))
