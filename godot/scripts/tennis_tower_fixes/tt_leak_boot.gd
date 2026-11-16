extends SceneTree
## Headless leak recount on the standalone tower after the collider fallback.
##   godot --headless --path godot -s res://scripts/tennis_tower_fixes/tt_leak_boot.gd


func _initialize() -> void:
	var n: Node = Node.new()
	n.set_script(load("res://scripts/tennis_tower_fixes/tt_leak_run.gd"))
	root.add_child(n)
