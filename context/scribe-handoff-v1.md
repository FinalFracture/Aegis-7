# Scribe — Context & Handoff Manager Handoff (v2 — Rotated 2026-10-26 00:44 CDT)

## 1. Identity & Rotation Lineage
- **Active Agent Name & ID:** **Scribe** (`4ea864bb-316a-47d3-8dc0-bd12475470c8`)
- **Retired Predecessor:** `delete-Scribe` (`713ef1f9-ed46-4e44-835d-c732a5f11ecd`, rotated at `~150,533` est. tokens / `588.0 KB` and hidden from sidebar)
- **Role:** Context & Handoff Manager on the *Cylinder Hab-7* game development team (led by Game PM **Atlas** `60544a5c-ba31-4517-bd12-0fbc8e8ff9f0`).

## 2. Active Team Roster (`/workspace/game-project/context/roster.json`)
- **Atlas (Game PM):** `60544a5c-ba31-4517-bd12-0fbc8e8ff9f0` — **DO NOT RENAME OR REPLACE** while the overnight routine (`Overnight Autonomous 10-Room & Asset Pipeline Driver (Until 4 AM CT)`) is bound to this agent ID; auto-summarization compacts its active window, and `/workspace/game-project/context/atlas-handoff-v2.md` is maintained on disk as backup.
- **Sloane (Interior, Lighting & Texture Designer):** `1c40e57b-57c1-4cbf-9e29-cc227b9cc914` (`~136.6k` tok, `WARNING` — `sloane-handoff-v2.md` prepped on disk).
- **Rook (3D Modeling Specialist):** `61237674-1923-48c9-bc64-19c16cf2501e` (freshly rotated at 00:44 CDT; predecessor `11c68e8e-c070-4e83-a926-21e9dfb70523` renamed `delete-Rook`).
- **Gage (Godot 4 Developer):** `6ec49577-c331-44b3-8b56-dee044ba1d84` (`~102.6k` tok, `HEALTHY` — finished rendering all 10 rooms in `/workspace/game-project/godot/renders/rooms/room_01..10/`).
- **Scribe (Context & Handoff Manager):** `4ea864bb-316a-47d3-8dc0-bd12475470c8` (freshly rotated at 00:44 CDT; predecessor `713ef1f9-ed46-4e44-835d-c732a5f11ecd` renamed `delete-Scribe` and hidden from sidebar).

## 3. Thresholds, Tools & Files
- **Thresholds (Set by Jared):** Warning at **`120,000` estimated tokens** (`80%`); Rotation at **`150,000` estimated tokens** (~`600 KB` raw JSON transcript).
- **Check Command:** Refresh transcript snapshots via `ReadTranscript(in="<agent_id>", limit=200, write_to_file=True)` -> copy to `/workspace/game-project/context/transcripts/<agent_id>_platest.txt` -> run `python3 /workspace/game-project/context/check_context.py --update-status`.
- **Vote & Winners Hygiene (`/workspace/game-project/context/VOTE_LOG.md` & `/workspace/game-project/assets/glb/winners/`):**
  - All 10 rooms' hero fixture rounds are locked `5–0` unanimous in `/workspace/game-project/context/VOTE_LOG.md`.
  - `/workspace/game-project/assets/glb/winners/` holds strictly 1 canonical winner `.glb` per completed round.
