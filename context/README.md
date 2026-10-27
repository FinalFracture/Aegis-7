# Context & Handoff Protocol (Managed by Scribe)

This directory holds living Markdown handoff documents, reference file manifests, and context snapshots for all 6 members of the *Cylinder Hab-7* ("Aegis-7 Standard") game development team:

- **Atlas** (`e744c2d9-fd3b-4916-a082-3cedfae0b695`) — Game Project Manager (`atlas-handoff-v3.md` / `atlas-handoff.md`)
- **Vance** (`0724beeb-94b9-43fa-a9cf-27117c5d4aa6`) — Sci-Fi Architect, Movie Prop & Set Design Specialist (`vance-handoff-v1.md` / `vance-handoff.md`)
- **Sloane** (`ec8a7e65-dd93-415c-9240-465e61fb2bcb`) — Interior, Lighting & Texture Designer (`sloane-handoff-v2.md` / `sloane-handoff.md`)
- **Rook** (`61237674-1923-48c9-bc64-19c16cf2501e`) — 3D Modeling Specialist (`rook-handoff-v2.md` / `rook-handoff.md`)
- **Gage** (`5c9c9f64-e799-4958-97ab-f8cbf4f6ff90`) — Godot 4 Developer (`gage-handoff-v2.md` / `gage-handoff.md`)
- **Scribe** (`49521640-e6fc-4f8f-b873-726f3f599220`) — Context & Handoff Manager (`scribe-handoff-v3.md` / `scribe-handoff.md`)

## Predecessor Purpose & Reference File Continuity Rule
Every replacement bot spawned during a memory transfer **must follow the exact same purpose as its predecessor** and **must know every file, spec, script, and asset directory its predecessor was referencing**. Each bot's `purpose` and `reference_files` list are stored in:
1. `/workspace/game-project/context/roster.json` (`purpose` and `reference_files` fields)
2. `/workspace/game-project/context/<agent>-handoff-v<N>.md` (and `<agent>-handoff.md`) under **"Predecessor Purpose & Mandatory Reference Files Manifest"**
3. The replacement bot's `CreateAgent` profile description on spawn.
