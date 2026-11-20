extends Node3D
## Door lab root. Builds the rig for every launch, including the placement probe.
## The long QA and the shot pass run only when their flags are on the command line.

func _ready() -> void:
	var info: Dictionary = DoorLabRig.build(self)
	set_meta("lab_info", info)
	var user := OS.get_cmdline_user_args()
	if _flag(user, "--qa-door-lab-shots"):
		var shots: Node = load("res://tools/qa/door_lab_shots.gd").new()
		shots.name = "ShotPass"
		add_child(shots)
		shots.call("start", self)
	elif _flag(user, "--qa-door-lab"):
		var qa: Node = load("res://tools/qa/door_lab_qa.gd").new()
		qa.name = "LabPass"
		add_child(qa)
		qa.call("start", self)
	elif _flag(user, "--qa-door-lab-build"):
		print("[door_lab] build-ok")
		get_tree().quit(0)


func _flag(args: PackedStringArray, name: String) -> bool:
	return args.has(name)
