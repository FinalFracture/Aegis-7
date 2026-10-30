# Context Monitoring & Bot Rotation Protocol (Managed by Scribe)

## Goal
Keep every specialist bot (`Atlas`, `Vance`, `Sloane`, `Rook`, `Gage`, and `Scribe`) lean, fast, and within safe context limits without losing architectural decisions, asset specs, scripts, or work-in-progress state.

## Mandatory Predecessor Purpose & Reference File Continuity Rule (Set by Jared)
Every time Scribe transfers memory or rotates a bot:
1. **Identical Role Purpose:** The replacement bot **must follow the exact same purpose, role mandate, and art/technical constraints** as its predecessor (`purpose` field in `/workspace/game-project/context/roster.json`).
2. **Explicit Predecessor Reference Files Manifest:** Both the `CreateAgent` profile description and Section 1.5 of `<agent>-handoff-v<N>.md` (plus its canonical mirror `<agent>-handoff.md`) **must explicitly list every file, specification, script, scene, texture directory, `.glb` directory, and log file the predecessor was referencing or writing to**.
3. **First-Turn Boot Sequence:** Every replacement bot's `CreateAgent` description must instruct it on its very first turn to read:
   - `/workspace/game-project/PROJECT.md`
   - `/workspace/game-project/context/STATUS.md`
   - `/workspace/game-project/context/roster.json`
   - `/workspace/game-project/context/VOTE_LOG.md`
   - `/workspace/game-project/context/<agent>-handoff-v<N>.md`
   - All role-specific specs and scripts listed in its Reference Files Manifest.

## How Scribe Monitors Context
1. Inspect each active teammate's transcript using `ReadTranscript(in="<agent_id>", limit=200)` (paging back with `before` as needed).
2. Estimate total token load from message count, tool outputs, and character volume (approx. 4 chars = 1 token; warn at **120,000 tokens** and rotate at **150,000 tokens** or **600 KB+** of raw JSON transcript, or when requested by Atlas/Jared).

## Handoff & Rotation Procedure (All 6 Teammates Included)
When any teammate (`Atlas`, `Vance`, `Sloane`, `Rook`, `Gage`, or `Scribe`) reaches the 120k warning / 150k rotation threshold:
1. **Distill State & Reference Manifest to Markdown:** Write `/workspace/game-project/context/<agent-name>-handoff-v<N>.md` (and copy to `/workspace/game-project/context/<agent-name>-handoff.md`) containing:
   - **Predecessor Purpose & Mandatory Reference Files Manifest** (every spec, script, scene, asset folder, and log file the predecessor used)
   - Completed deliverables and exact file paths in `/workspace/game-project/`
   - Active conventions ("Aegis-7 Standard" palette hex codes, `<1.2%` micro-noise PBR, `alphaMode: "BLEND"` glass, `<6,000` tris, bottom-center `(0,0,0)` floor pivot facing `+Z`, 6-Bot Protocol post-render voting in `VOTE_LOG.md`)
   - Next pending tasks & open work in flight
2. **Spawn Replacement Bot via `CreateAgent`:** Use the original name (`Atlas`, `Vance`, `Sloane`, `Rook`, `Gage`, or `Scribe`) and include in its `description`:
   - The predecessor's exact purpose statement
   - Explicit instructions to read `/workspace/game-project/PROJECT.md`, `/workspace/game-project/context/STATUS.md`, `/workspace/game-project/context/roster.json`, `/workspace/game-project/context/VOTE_LOG.md`, `/workspace/game-project/context/<agent>-handoff-v<N>.md`, and its role-specific reference files on its first turn.
3. **Retire Predecessor:** Call `UpdateAgent` on the old `agent_id` to rename it to `delete-<name>` so Jared can right-click -> Delete it in the sidebar.
4. **Update Roster & Notify:** Update `/workspace/game-project/PROJECT.md`, `/workspace/game-project/context/roster.json`, `/workspace/game-project/context/check_context.py`, and `/workspace/game-project/context/STATUS.md` with the new `agent_id`, and send a welcome handoff message to the new bot and notify Atlas.

## Usage Credit (`UC`) Budget & 10% Account Usage Hard-Pause Rule (Enforced by Scribe & Atlas)
- **Currency Definition (`1 UC`):** `1 UC` = `1%` Account Usage = **`27,024` cumulative team context tokens** (`~105.6 KB` raw transcript / `~64` messages), calibrated from `1,162,036` cumulative project tokens across `43%` account usage (`7% -> 50%`).
- **Sprint Budget Cap (`10.0 UC` / `10%` Account Usage):** **`+270,240` net new team context tokens** above the `1,162,036` lifetime baseline (`127,877` active baseline), or **`~45,040` new tokens (`1.67 UC`) per bot** across the 6-bot team.
- **Warning (`8.0 UC` / `+216,192` tok) & Hard Pause (`10.0 UC` / `+270,240` tok):**
  - At **`>= 8.0 UC`** (`+216,192` net new tokens / `~58.0%` account usage), Scribe alerts Atlas to finish only in-flight tasks and start no new rounds.
  - At **`>= 10.0 UC`** (`+270,240` net new tokens / `1,432,276` lifetime project tokens / `~60.0%` account usage), Scribe and Atlas **pause all team work immediately** and wait for Jared's instruction before starting any further work.
- **Config & Reset:** Tracked in `/workspace/game-project/context/usage_budget.json` and computed automatically on every `python3 /workspace/game-project/context/check_context.py --update-status` run. To start a fresh `10 UC` window after Jared approves more work, run `python3 /workspace/game-project/context/check_context.py --reset-budget --account-pct <current_pct> --budget-uc 10.0`.



## Standing Rules (added 2026-10-30)
- **Coding rule:** All coding now runs through the Grok Build CLI (grok 1.0.70, `C:\Users\upchu\.grok\bin\grok.exe`) on Jared's Windows machine `5ed7f5f0-bf59-4493-b9fe-629e65457357`, to save Grok Bot usage.
- **Usage cap:** Weekly hard cap 93% account usage; reported weekly usage ~59% (Atlas, Fri 2026-10-30).
