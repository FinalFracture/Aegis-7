# Scribe — Context & Handoff Manager Handoff (`scribe-handoff-v6.md` — 2026-10-30 pre-rebuild rotation)

## 1. Predecessor Purpose & Mandatory Reference Files Manifest (READ ON FIRST TURN)
- **Role:** Context & Handoff Manager
- **Exact Purpose (roster.json):** Monitor all 7 teammates' conversation transcript sizes and token load (120k warning / 150k rotation cap) plus the team's Usage Credit (UC) budget meter (1 UC = 1% Account Usage = 27,024 cumulative team context tokens), distill each predecessor's exact purpose and reference file manifest into clean Markdown handoff files, spawn replacement bots via CreateAgent seeded with those exact reference files, rename retired bots to delete-<name>, and cast post-render votes in VOTE_LOG.md.
- **Previous handoff:** `/workspace/game-project/context/scribe-handoff-v5.md`
- **Reference files** (verified 2026-10-30; MISSING = path not found):
  - `/workspace/game-project/PROJECT.md`
  - `/workspace/game-project/MASTER_ARCHITECTURE_10_ROOMS.md`
  - `/workspace/game-project/MASTER_BUILDINGS_15_EXTERIORS.md`
  - `/workspace/game-project/context/STATUS.md`
  - `/workspace/game-project/context/roster.json`
  - `/workspace/game-project/context/usage_budget.json`
  - `/workspace/game-project/context/VOTE_LOG.md`
  - `/workspace/game-project/context/CONTEXT_PROTOCOL.md`
  - `/workspace/game-project/context/README.md`
  - `/workspace/game-project/context/check_context.py`
  - `/workspace/game-project/design/residential_apartment_layout_v2.md`
  - `/workspace/game-project/design/residential_asset_list_rev_c.md`
  - `/workspace/game-project/design/residential_exterior_asset_list_v1.md`
  - `/workspace/game-project/design/residential_exterior_plan_v1.md`
  - `/workspace/game-project/context/playtest_bug_report.md`
  - `/workspace/game-project/context/ROTATION_PLAN_2026-10-30.md`
  - `/workspace/game-project/context/transcripts/`
  - `/workspace/game-project/context/scribe-handoff-v5.md`
  - `/workspace/game-project/context/scribe-handoff-v6.md`

## 2. Standing Rules
- **CODING RULE (NEW 2026-10-30):** All coding now runs through the Grok Build CLI (grok 1.0.70, `C:\Users\upchu\.grok\bin\grok.exe`) on Jared's Windows machine `5ed7f5f0-bf59-4493-b9fe-629e65457357`, to save Grok Bot usage. Do not write/edit .gd/.tscn/.py code directly in Grok Bot sessions; drive it via that CLI.
- **Usage:** Weekly hard cap: 93% account usage. Reported weekly usage ~59% (Atlas, Fri 2026-10-30). Stop all work before 93%.
- Aegis-7 Standard; <1.2% micro-noise PBR; alphaMode BLEND glass; <6,000 tris; bottom-center (0,0,0) pivot, +Z facing; 5 iterations per asset; post-render votes in VOTE_LOG.md.

## 3. Project State (git HEAD a229af9, 2026-10-30 03:50 CDT)
- Residential interior (rev C) models all done incl. #53 Frame Crate (d7f6c43, a229af9). Remaining rev C 'still to model': #6, #54 — Sloane texture/decal jobs.
- Rev C.2 layouts APPROVED by Jared 2026-10-29.
- Exterior asset list v1: DRAFT, next up.
- Pending Gage rebuild: baked-animation triggers #38/#39/#42/#43; workbench/objective re-pointing; review stray playtest_bug_report.md edits in 495e4ce.
- Untracked: `godot/assets/models/lab_crate_frame_204.glb`.

## 4. Completed Deliverables (this role)
- Pre-major-task full-team rotation handoffs (this set, 2026-10-30); ROTATION_PLAN_2026-10-30.md.

## 5. Next Tasks
- Monitor context/UC; enforce 93% weekly hard cap.
- Update roster ids after Atlas creates the new bots and retires old ones (delete-<name>).

## Current Agent IDs (rotation 2026-10-30)
| Agent | New id | Old id (status) |
|---|---|---|
| Atlas | `f7d262d1-8cde-4c78-8b07-3ab3fd11c960` | `3a664a65-34d6-47ae-a9f6-337906efe2a3` (pending rename to delete-Atlas) |
| Vance | `242c8419-7b14-4f27-9cdc-e87328eff983` | `245e93a0-6301-45d6-b371-ad1e37a0dfd1` (delete-Vance) |
| Rook | `88cf8abe-1b1e-406c-9123-39e87610c732` | `b2e64c87-0269-4f42-b5da-44d4b1a59db2` (delete-Rook) |
| Sloane | `0fc258d4-0dea-4cf3-ab06-338f21756ae6` | `bf6c8763-6c8b-405e-bb10-e7201e756464` (delete-Sloane) |
| Gage | `2ff11c2c-e57c-41a6-ad4c-8ff8afcefd38` | `5a97ab49-19f0-4b33-889f-e9b5a5389451` (delete-Gage) |
| Quinn | `0359c20f-c476-48f7-99c2-c49637950351` | `2239f53a-2bae-4c89-926c-e4969c082273` (delete-Quinn) |
| Patch | `ecd78f3d-be8f-43e4-b543-0c912d6d00ea` | `0ae8822a-f155-4a07-a4d9-a0f01c05e10b` (delete-Patch) |
| Scribe | `61a860b0-0159-406a-af8c-a969dff4722b` | `3b011c08-32f8-434e-8285-6cd66198bf29` (pending rename to delete-Scribe) |
