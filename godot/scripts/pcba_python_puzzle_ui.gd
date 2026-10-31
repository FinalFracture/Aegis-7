class_name PcbaPythonPuzzleUI
extends CanvasLayer
## Interactive Full-Screen "I Spy" PCBA (`RESET` Pin) + Readable Python Firmware Terminal UI
## Attached to `preface_playable_area.tscn` / `preface_playable_residential_sector.tscn`.
## - Left Panel ("I Spy" PCBA View): FR4 Circuit Board (`AEGIS-7 FIELD EMITTER PCBA [REV 4.2]`),
##   central `IC1: AEGIS-DRV-04`, 4-pin header (`GND`, `LOCK_HOLD`, `RESET`, `AUX_BUZZ`),
##   loose glowing Super Wire jumper lead from `#04` Neural Smart-Sleeve plugged onto `RESET`,
##   and `+5A Battery Charge` Aux Slot.
## - Right Panel (Readable Python Firmware Editor `field_control.py`):
##   `supply_amperage = 7` -> `12` (or `>` -> `<`) in `def enable_field(amperage): if amperage > 10: return True else: return False`.

signal door_unlocked(final_amperage: int)

const TEX_DIRS := [
	"res://assets/textures/preface",
	"res://assets/textures/residential",
	"res://assets/textures"
]

var _root_control: Control
var _pcba_tex_rect: TextureRect
var _python_tex_rect: TextureRect
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


func _resolve_asset_path(res_path: String) -> String:
	if res_path.begins_with("res://"):
		var global_p: String = ProjectSettings.globalize_path(res_path).simplify_path()
		if FileAccess.file_exists(global_p):
			return global_p
	if FileAccess.file_exists(res_path):
		return res_path
	return ""


func _load_tex(fname: String) -> Texture2D:
	for d: String in TEX_DIRS:
		var res_p: String = d + "/" + fname
		var abs_p: String = _resolve_asset_path(res_p)
		if abs_p != "":
			var img: Image = Image.new()
			if img.load(abs_p) == OK and not img.is_empty():
				return ImageTexture.create_from_image(img)
		if ResourceLoader.exists(res_p):
			var r: Resource = ResourceLoader.load(res_p)
			if r is Texture2D:
				return r as Texture2D
	return null


func set_Overlay_visible(vis: bool) -> void:
	visible = vis
	if _root_control != null:
		_root_control.visible = vis


func _build_ui() -> void:
	_root_control = Control.new()
	_root_control.name = "DiagnosticConsoleRoot"
	_root_control.set_anchors_preset(Control.PRESET_FULL_RECT)
	add_child(_root_control)

	# Translucent peripheral vignette so the 3D residential vestibule, force field & Hammerhead bot remain visible around the console!
	var backdrop_dim: ColorRect = ColorRect.new()
	backdrop_dim.color = Color(0.03, 0.06, 0.10, 0.42)
	backdrop_dim.set_anchors_preset(Control.PRESET_FULL_RECT)
	_root_control.add_child(backdrop_dim)

	# Main 84% Diegetic Field Diagnostic Console Frame (centered 1612 x 908 on 1920 x 1080)
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

	# Top Diegetic Header Bar
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
	title_lbl.position = Vector2(22, 10)
	title_lbl.text = "AEGIS-7 FIELD DIAGNOSTIC CONSOLE // SECTOR-04 FIELD EMITTER [WRIST RIG #04 NEURAL SLEEVE COUPLED]"
	title_lbl.add_theme_font_size_override("font_size", 21)
	title_lbl.add_theme_color_override("font_color", Color("#F0F6FF"))
	header_bg.add_child(title_lbl)

	var sub_lbl: Label = Label.new()
	sub_lbl.position = Vector2(22, 38)
	sub_lbl.text = "STAGE 1 (LEFT): 'I SPY' PCBA — PLUG SUPER WIRE INTO [RESET] PIN & SEAT +5A BATTERY   |   STAGE 2 (RIGHT): PYTHON FIRMWARE — def enable_field(amperage)"
	sub_lbl.add_theme_font_size_override("font_size", 14)
	sub_lbl.add_theme_color_override("font_color", Color("#FFD166"))
	header_bg.add_child(sub_lbl)

	_close_button = Button.new()
	_close_button.position = Vector2(1430, 12)
	_close_button.size = Vector2(144, 42)
	_close_button.text = "[P / ESC] CLOSE"
	_close_button.pressed.connect(func() -> void: set_Overlay_visible(false))
	header_bg.add_child(_close_button)

	# ==========================================================================
	# LEFT PANEL: STAGE 1 — "I SPY" PCBA CIRCUIT BOARD (`ui_pcba_circuit_board_panel.png`)
	# ==========================================================================
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

	_pcba_tex_rect = TextureRect.new()
	_pcba_tex_rect.position = Vector2(14, 12)
	_pcba_tex_rect.size = Vector2(748, 596)
	_pcba_tex_rect.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	_pcba_tex_rect.stretch_mode = TextureRect.STRETCH_SCALE
	var pcba_tex: Texture2D = _load_tex("ui_pcba_circuit_board_panel.png")
	if pcba_tex != null:
		_pcba_tex_rect.texture = pcba_tex
	left_panel.add_child(_pcba_tex_rect)

	var j4_label: Label = Label.new()
	j4_label.position = Vector2(18, 616)
	j4_label.text = "INTERACTIVE J4 HEADER PINOUT (CLICK PIN TO SEAT #04 WRIST SUPER WIRE LEAD):"
	j4_label.add_theme_font_size_override("font_size", 15)
	j4_label.add_theme_color_override("font_color", Color("#A8F0D8"))
	left_panel.add_child(j4_label)

	var pin_names := ["GND", "LOCK_HOLD", "RESET", "AUX_BUZZ"]
	for i: int in range(pin_names.size()):
		var pname: String = pin_names[i]
		var btn: Button = Button.new()
		btn.position = Vector2(18 + i * 188, 646)
		btn.size = Vector2(176, 72)
		btn.text = "[PIN %d: %s]\n%s" % [i + 1, pname, "SUPER WIRE SEATED" if pname == "RESET" else "UNCOUPLED"]
		btn.add_theme_font_size_override("font_size", 15)
		btn.pressed.connect(_on_pin_pressed.bind(pname))
		left_panel.add_child(btn)
		_pin_buttons[pname] = btn

	# ==========================================================================
	# RIGHT PANEL: STAGE 2 — READABLE PYTHON FIRMWARE TERMINAL (`ui_python_code_editor_panel.png`)
	# ==========================================================================
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

	_python_tex_rect = TextureRect.new()
	_python_tex_rect.position = Vector2(14, 12)
	_python_tex_rect.size = Vector2(748, 596)
	_python_tex_rect.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	_python_tex_rect.stretch_mode = TextureRect.STRETCH_SCALE
	var py_tex: Texture2D = _load_tex("ui_python_code_editor_panel.png")
	if py_tex != null:
		_python_tex_rect.texture = py_tex
	right_panel.add_child(_python_tex_rect)

	var py_ctrl_lbl: Label = Label.new()
	py_ctrl_lbl.position = Vector2(18, 616)
	py_ctrl_lbl.text = "INTERACTIVE PYTHON OVERRIDE — def enable_field(amperage): if amperage > 10: return True"
	py_ctrl_lbl.add_theme_font_size_override("font_size", 15)
	py_ctrl_lbl.add_theme_color_override("font_color", Color("#88E8FF"))
	right_panel.add_child(py_ctrl_lbl)

	_amp_button = Button.new()
	_amp_button.position = Vector2(18, 646)
	_amp_button.size = Vector2(368, 72)
	_amp_button.add_theme_font_size_override("font_size", 16)
	_amp_button.pressed.connect(_on_toggle_amperage)
	right_panel.add_child(_amp_button)

	_run_button = Button.new()
	_run_button.position = Vector2(404, 646)
	_run_button.size = Vector2(354, 72)
	_run_button.add_theme_font_size_override("font_size", 16)
	_run_button.pressed.connect(_on_execute_field_script)
	right_panel.add_child(_run_button)

	# ==========================================================================
	# BOTTOM LIVE EVALUATION STATUS BAR
	# ==========================================================================
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
		var is_reset_active: bool = (pname == "RESET" and reset_pin_connected)
		btn.text = "[PIN: %s]\n%s" % [pname, ">> SUPER WIRE ON RESET <<" if is_reset_active else "OPEN / UNCOUPLED"]
		btn.add_theme_color_override("font_color", Color("#00E676") if is_reset_active else Color("#B0C4D8"))

	if _amp_button != null:
		_amp_button.text = "supply_amperage = %d  (%s)\n[CLICK TO TOGGLE 7A <-> 12A +5A CELL]" % [
			supply_amperage,
			"12A BOOSTED" if supply_amperage > 10 else "7A DEFAULT"
		]
		_amp_button.add_theme_color_override("font_color", Color("#FFD166"))

	var is_open: bool = evaluate_enable_field(supply_amperage) and reset_pin_connected
	if _run_button != null:
		_run_button.text = "EXECUTE: enable_field(%d) ==> %s\n%s" % [
			supply_amperage,
			"True" if is_open else "False",
			"[FIELD RELEASED]" if is_open else "[FIELD STALLED AT 40%]"
		]
		_run_button.add_theme_color_override("font_color", Color("#00E676") if is_open else Color("#FF5544"))

	if _status_banner != null:
		if is_open:
			_status_banner.text = "LIVE TELEMETRY: J4 [RESET] PIN COUPLED VIA SUPER WIRE  •  supply_amperage = 12  •  enable_field(12) -> return True  [FIELD RELEASED]"
			_status_banner.add_theme_color_override("font_color", Color("#00E676"))
		else:
			_status_banner.text = "LIVE TELEMETRY: J4 [RESET] PIN / AMPERAGE FAULT  •  supply_amperage = %d  •  enable_field(%d) -> return False  [FIELD LOCKED]" % [supply_amperage, supply_amperage]
			_status_banner.add_theme_color_override("font_color", Color("#FF9500"))
