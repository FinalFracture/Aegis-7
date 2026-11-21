"""Rook door_lab QA for the bulkhead + floor hatch (pass C): thin wrapper over door_lab_passC.py (clip at key poses, motion sweeps,
flush / clear-opening checks, tri budget, renders to /workspace/renders/doorlab_passC/). The pass B checks used the old node names."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import door_lab_passC as pc
if __name__ == "__main__":
    pc.main(["bulkhead_hatch", "floor_hatch"], "--no-render" not in sys.argv)
