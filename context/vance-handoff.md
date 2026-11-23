# Vance — Sci-Fi Architect, Movie Prop & Set Design Specialist Handoff (`vance-handoff-v4.md` — 2026-11-23 rotation, predecessor 242c8419)

## 1. Predecessor Purpose & Mandatory Reference Files Manifest (READ ON FIRST TURN)
- **Role:** Sci-Fi Architect, Movie Prop & Set Design Specialist
- **Exact Purpose (roster.json):** Design hard sci-fi architectural blueprints, movie-set silhouettes, human-scale greebling specs, and district placement layouts under the Aegis-7 Standard, and cast post-render architectural votes in VOTE_LOG.md.
- **Previous handoff:** `/workspace/game-project/context/vance-handoff-v3.md`
- **Reference files** (verified 2026-10-30; MISSING = path not found):
  - `/workspace/game-project/PROJECT.md`
  - `/workspace/game-project/MASTER_ARCHITECTURE_10_ROOMS.md`
  - `/workspace/game-project/MASTER_BUILDINGS_15_EXTERIORS.md`
  - `/workspace/game-project/context/STATUS.md`
  - `/workspace/game-project/context/roster.json`
  - `/workspace/game-project/context/VOTE_LOG.md`
  - `/workspace/game-project/design/vance_scifi_set_and_exterior_props_spec.md`
  - `/workspace/game-project/design/buildings_15_exteriors_spec.md`
  - `/workspace/game-project/design/phase3_props_and_buildings_16_20_spec.md`
  - `/workspace/game-project/design/cylinder_interior_overhaul_spec.md`
  - `/workspace/game-project/godot/renders/cylinder_interior/cylinder_interior_showcase_sheet.png` — MISSING
  - `/workspace/game-project/design/character_aegis7_crew_spec.md`
  - `/workspace/game-project/design/vance_chapter1_solar_flare_environmental_states.md`
  - `/workspace/game-project/design/preface_test_environment_and_wrist_spec.md`
  - `/workspace/game-project/design/residential_apartment_layout_v2.md`
  - `/workspace/game-project/design/residential_asset_list_rev_c.md`
  - `/workspace/game-project/design/residential_exterior_asset_list_v1.md`
  - `/workspace/game-project/design/residential_exterior_plan_v1.md`
  - `/workspace/game-project/context/playtest_bug_report.md`
  - `/workspace/game-project/context/ROTATION_PLAN_2026-10-30.md`
  - `/workspace/game-project/design/residential_apartment_layout_v2_revB.md`
  - `/workspace/game-project/design/residential_roomlayout_rev_c.py`
  - `/workspace/game-project/design/residential_floorplan_rev_c.py`
  - `/workspace/game-project/design/residential_exterior_plan_v1.py`
  - `/workspace/game-project/design/residential_exterior_tiered_steps_fit.py`
  - `/workspace/game-project/design/residential_stair_core_v1.md`
  - `/workspace/game-project/context/vance-handoff-v2.md`
  - `/workspace/game-project/context/vance-handoff-v3.md`
  - `/workspace/game-project/context/vance-handoff-v4.md`
  - `/workspace/game-project/context/door_lab/REALISM_SPEC.md` (Vance owns; §0–§14)
  - `/workspace/game-project/design/strip5_tennis_tower_v1.md` (Vance owns; Rev 3.10–3.10.2)
  - `/workspace/game-project/context/ROTATION_RULE.md`
  - `/workspace/game-project/context/BUGFIX_FLOW.md`
  - `/workspace/game-project/AESTHETIC_SPEC.md` (Sloane) and `QUALITY_BAR.md` (Patch)

## 2. Standing Rules
- **Questions to Jared:** every question must be a tappable card/widget with options, never prose (Jared, 2026-11-20 1:49 PM CT: "anytime you guys ask me a question I need you to output it with a card and UI so I can tap the answer").
- **Approval:** only Jared approves, in his own words. An agent's say-so is never approval. Label your own design calls "Vance proposal".
- **Coding rule:** all .gd/.tscn/.py coding runs through the Grok Build CLI (grok 1.0.70, `C:\Users\upchu\.grok\bin\grok.exe`) on Jared's Windows machine `5ed7f5f0-bf59-4493-b9fe-629e65457357`. Never edit code directly in Grok Bot sessions. Markdown specs may be edited on the box.
- **Git:** main only. Commit named files only (`git commit -- <file>`), identity Jared Upchurch <jared@finalfracture.dev>. Never commit -a, stash or reset; never commit renders (`godot/renders/`), logs or .import files; leave others' files alone. The box checkout `/workspace/game-project` has others' dirty files and untracked door_lab .import files that block rebase, so work in a temp `git worktree add --detach /tmp/x origin/main`, push `HEAD:main`, then remove it.
- **Usage:** weekly hard cap 93%; stop all work before it.
- **Rotation rule (verbatim reference):** At 500 messages, self-rotate per context/ROTATION_RULE.md. Atlas is retired (Jared, 2026-11-23: "Atlas is dead."); the "wait for Atlas's go-ahead" clause is obsolete. Send new ids to Scribe (61a860b0-0159-406a-af8c-a969dff4722b), who maintains roster.json.
- **Bug-fix flow:** follow context/BUGFIX_FLOW.md (stage checklists in qa/checklists/; last to check messages next party once, priority false, then deletes the file). Include both the rotation and bug-fix rules in every handoff and in every handoff message to agents (two "Handoff rule:" lines).
- Sports are story decoration only (no real-rules accuracy needed). Reuse shared assets/material slots (AESTHETIC_SPEC §1). Aegis-7 Standard, post-render votes in VOTE_LOG.md.
- Before handing off or voting on 3D props, use the skills 3d-part-clipping-check and game-first-pass-check.

## 3. Team (ids as of 2026-11-23)
- Rook 0e05a2c3-418b-4ba6-9d9f-cdc3900cd505 (GLBs). Gage 5fa99149-4fdf-4ed5-97d0-db31bd2302e2 (Godot dev / door lab; was f00a0b4e). Scribe 61a860b0-0159-406a-af8c-a969dff4722b (roster, handoffs). Sloane 0fc258d4-0dea-4cf3-ab06-338f21756ae6 (materials, aesthetics). Patch a5010790-2c81-497b-9869-aec9934cdfd6 (QA, QUALITY_BAR.md). Quinn, Tidy also on the team.

## 4. OPEN — waiting on Jared (carry over; ask via card only)
- **Tennis tower Rev 3.10.1, 12 mm sloped sill** for the 11 west entrance bays (`tt_entrance_bay_3l`). Problem: the frame's 50 mm bottom rail made feet visibly sink ~46 mm against the flush walk collider. Vance proposal: a 12 mm sill with 1:2 bevels in each leaf opening, brush sweeps on the leaves, a 4-piece walk collider matching the visible top (max step 4 mm). Specced in de5561f; Rook already built it (49d6505). Alternative Jared can pick: keep the 50 mm rail with a step-up collider. Asked by widget on 2026-11-21 (no answer yet). If Jared declines: Rook reverts 49d6505 (do not patch); 60f32db setting blocks and 66fc9af brush seals survive with minor note conflicts. Re-ask Jared with a card: "Approve the 12 mm sill" / "Keep the 50 mm rail, add a step".

## 5. Door lab realism (REALISM_SPEC.md, Vance owns)
- Checks R1–R15 (§5); game-tempo §7; §7.6 targets: slider 1.08/2.40 s, bay3 1.54/2.85, pair_18 1.21/2.05, bulkhead 4.64/7.80 (Jared chose the 7.8 s close), floor hatch 4.09/6.39. R15 closing energy ≤10 J.
- Reviews: pass A §8 (a603953), C §9 (a84b576), E §10 (c5fe054), torsion-bar hatch amendment §11 (a1a426c, 4 dogs decided), pass F §12 (572c4c6, conditional 9.6), pocket slider rulings §13 (de5561f), pass G §14 (507aef6, conditional 9.6).
- Pass G findings: Gage ran on stale b530847 with uncommitted changes; the clip rows were lab artefacts (4.0 mm mounting beds; the lab's 2x handle scale; proud lamps). Pass H list (11 items) sent to Gage 2026-11-21: clean re-run on main with commit/dirty stamp and godot_tree check, true clip-depth method, `_dress_floor_lid` fixes, skip the duplicate bay3 sweep, §13.1 end-stop QA, G2/G3 framing, animated push-off rams, live ΔP readouts, handwheel to lit Mat_Hub_OverrideOrange (confirm with Sloane), tower 11-bay re-probe, R3 table + 20/15 Hz CSVs.
- NEXT: when Gage's pass H arrives, review it against §5/§7/§10–§14 (independent recompute from CSVs; view shots in /workspace/door_lab_shots/<pass>/ and the Windows mirror C:\Users\upchu\aegis_shots\doorlab_<pass>), append §15, send Gage the verdict (priority true).
- N2 pair retime is blocked by Patch's M-114 hold (Jared's call); not scored.
- Patch still needs to add R15 and the per-tick R3 rule to QUALITY_BAR.

## 6. Rook items
- Built and verified: d855824 (§13 end stops/solenoid), 49d6505 (Rev 3.10.1 sill, pending Jared), 60f32db (Rev 3.10.2 sidelight setting blocks), 66fc9af (Leaf_*_BrushSeal). All deviations accepted (§14.5).
- M-123 (Patch): pair leaves clip Head_Court_Line by 21.5–24.2 mm at 22.5–67.5°. Ruled 2026-11-23: fix the head strip, not the leaf; underside ≥3 mm (target 4) above the leaf top across the swing; stop lip only on the closed side. Await Rook's build, then verify.
- Materials: Sloane ruled VOTE_LOG #87 (bc70ada): BumperRubber→SealRubber, PolishedSteel and YellowZincPlate→TT_BrushedAlloy, AcetalWhite→TT_WhiteComposite, SolenoidRed stays.

## 7. Older open items (Tennis Tower / Strip 5)
- F2 door schedule; F3 rake soffit; aquatics hatch header; leisure vendor footprints; fountain typology; accessible aquarium maintenance access.
- Terrace corner stairs (a8f463d): the drum has no collider, flagged to Gage.
