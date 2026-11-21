# Door lab pass G

Self-scores in this file are Gage's read of the shots. They are not Sloane's official scores.

Main is `b5308471aa0a2d77a526bb1965ef3b3737d14cbc` plus the pass G working tree. Nothing was committed or pushed. The Rook patch applied cleanly: anti-lift roller radius 0.020, and the shot script opens `slide_AccessPanel` by exact name, +90 degrees local X, meta shot `head_closed`.

The functional harness at 60, 20, and 15 Hz, and the windowed OpenGL shot pass, all leave the same seven failing rows. `qa/door_lab/runG/summary.json` says verdict FAIL, functional FAIL, visual FAIL, fails_count 7:

- hatch: F-CLIP-HW 0.086 m, F-CLIP-ALLOW, R7
- floorhatch: F-CLIP-LEAF 0.0152 m, F-CLIP-HW 0.070 m, F-CLIP-ALLOW, R7

The summary visual flag is FAIL because the shot rewrite counts every failing metric row, and those seven rows are functional clip rows. Each door's own visual field is PASS. Every V-* gate in `runG/*/metrics.json` passes. Pocket, bay3, and pair are functionally clean.

20 Hz and 15 Hz summaries list the same seven ids. Their visual field stays PENDING because shots write only into `runG`.

## Stamp

`qa/door_lab/runG/meta.json` was rewritten after the glass, hatch face fill, floor hazard, and shot-script edits. The hashes are write-tree results of that final tree, taken on a temporary index. The real index was left as it was: staged and unstaged copies of `godot/scripts/door_lab/door_lab_rig.gd` and `godot/tools/qa/door_lab_shots.gd`.

| field | value |
| --- | --- |
| commit | `b5308471aa0a2d77a526bb1965ef3b3737d14cbc` |
| dirty | true |
| tree | `03382c6a1d0d523619432f4d28ecdc2f82f20839` |
| godot_tree | `88ce84e4b22c5d74e4c8b9e46e5615269ade9ac3` |
| head_godot | `731a9e8e3131f82ea2ac355b77d3eb5d0043e9ce` |
| gpu | Intel UHD Graphics 605 |
| updated | 2026-11-21 13:02 CT |

`godot_tree` is a write-tree of the `godot/` worktree. Compare it to `head_godot`. Tree `932f8ec` is not an object on origin.

## Checks outside the door harness

First-pass with `GODOT_BIN` set to the Godot 4.7.2 console binary: SUMMARY 25 PASS, 15 WARN, 0 FAIL, exit 0. The probe ran on `res://scenes/test/door_lab.tscn`: 39 static bodies, 699 meshes. An earlier run without `GODOT_BIN` skipped the probe. That run is not the result.

Placement assert: `PLACEMENT_ASSERT: interiors_loaded=true`, then `PLACEMENT_ASSERT: 26 pass, 0 fail`, `SEAM_AUDIT: 336 pass, 0 fail`, exit 0.

## Timing

Published game-tempo totals stayed: pocket 1.08/2.40, bay3 1.54/2.85 (last leaf adds the stagger), pair 1.21/2.05 (lead; trail +60 ms), hatch 4.64/7.80, floor hatch 4.09/6.39. K_TRAVEL 0.45 and K_MECH 0.60 stayed. The bulkhead close stayed 7.800 s. M-114 stayed held: pair open section7 windows are request 0.00–0.05, latch retract 0.05–0.12, lurch 0.12–0.20, accel 0.200–0.521, cruise 0.521–0.550, decel 0.550–0.871, backcheck 0.871–1.051, settle 1.051–1.271. F-TIME at ±10% of 1.21 still covers settle end 1.271.

F-TIME and R2 pass on all five doors at all three rates. Measured open/close seconds, with the profile duration in parentheses:

| door | 60 Hz | 20 Hz | 15 Hz | profile |
| --- | --- | --- | --- | --- |
| pocket | 1.100 / 2.417 | 1.100 / 2.450 | 1.133 / 2.467 | 1.084 / 2.400 |
| bay3 | 1.683 / 2.983 | 1.700 / 3.000 | 1.733 / 3.000 | 1.551 / 2.850 |
| pair | 1.333 / 2.117 | 1.350 / 2.150 | 1.333 / 2.133 | 1.271 / 2.050 |
| hatch | 4.633 / 7.800 | 4.650 / 7.800 | 4.667 / 7.800 | 4.629 / 7.799 |
| floor | 4.100 / 6.400 | 4.100 / 6.400 | 4.133 / 6.400 | 4.091 / 6.390 |

Bay3 spec adds the 0.120 s last-leaf stagger (1.540+0.120 / 2.850+0.120). Pair spec adds the 0.060 s trail (1.210+0.060 / 2.050+0.060).

The first 60 Hz run of this pass failed bay3 and pair F-TIME/R2 on phase labels only. Totals were already inside ±10%. Bay3 said "close prewarn missing from motion rows". Pair said "close accel missing from motion rows". The missing test was treating a real span as missing. The 20 Hz run then failed pair open request: the 0.00–0.05 s window is one tick at 20 Hz and never received a Leaf_L sample. A leading short phase is now accepted when the next phase starts by the end of that window plus tolerance. The 50 ms window was left as published. Lead leaf was left as published. After that fix, F-TIME passes at 60, 20, and 15 Hz.

Close peaks from R3 at 60 Hz: pocket 0.640 m/s, bay3 50.00 °/s (reference 50), pair 66.67 °/s (reference 66.67), hatch 19.40 °/s, floor hatch 33.33 °/s. The obstruction trace's own peak, used for the 2% stop, is 46.914 °/s on bay3 and 62.821 °/s on pair at 60 Hz.

F-OBS-STOP at 60 Hz, first tick at or under 2% of peak, no extra tick: pocket 0.100 s vs 0.13, bay3 0.150 vs 0.15, pair 0.100 vs 0.10, hatch 0.483 vs 0.6, floor 0.317 vs 0.6. All pass. 15 Hz also passes: pocket 0.067, bay3 0.133, pair 0.067, hatch 0.533, floor 0.333. 20 Hz is absent from the fail list. `stop_s` was not edited.

R3 passes. Worst raw ratio is about 0.91, with the logged phase-entry exceptions. The one-tick seal-contact exclusion stays.

F-LAMP-FADE passes on all five doors: measured 0.075 s. The 50% crossing is 0.0750 s at 60 Hz, 0.0750 s at 20 Hz, and 0.0767 s at 15 Hz.

## Mesh clip

The allowlist is `godot/resources/door_lab/contact_allowlist.json`. Each entry is an exact part pair with its own max depth. No entry is above 0.030 m. Leaf skin versus visible frame skin stays at 0.010 m. A listed part that disappears fails the gate. Seals have a compression limit. Depth is containment on the welded meshes, all triangles, at 0/25/50/75/100% open and at mid-close. The spatial hash is only the pre-pass. Early-out inside a pair is 0.120 m, so the depths below are the true maxima, not a truncated first hit.

Before, the first 60 Hz run failed F-CLIP-LEAF, F-CLIP-HW, F-CLIP-ALLOW, and R7 on all five doors, plus F-CLIP-POCKET on the pocket. Those depths were prism hits: pocket leaf 0.168 m and hardware 0.1125 m, bay3 leaf 0.7734 m and hardware 1.0871 m, pair leaf 0.3550 m and hardware 0.8472 m, hatch leaf 0.3136 m and hardware 0.4648 m, floor leaf 0.0349 m and hardware 0.9440 m.

After the poke-or-slab depth, at 60 Hz:

| door | leaf m | hw m | allow over-limit pairs | R7 |
| --- | --- | --- | --- | --- |
| pocket | 0.0025 pass | 0.0100 pass | 0 | pass |
| bay3 | 0.0092 pass | 0.0050 pass | 0 | pass |
| pair | 0.0025 pass | 0.0048 pass | 0 | pass |
| hatch | 0.0060 pass | 0.0860 fail | 4 pairs, every pose | fail |
| floor | 0.0152 fail | 0.0700 fail | 3 pairs | fail |

The missing-part list is empty on every door. The allow note begins `missing ;` and then the JSON array.

Hatch pairs over the 0.010 m skin cap, same depth at every sampled pose:

- `bulkhead_HingeHeavy_frame` vs `frame_skin` 0.086 m
- `bulkhead_damper_mount` vs `frame_skin` 0.076 m
- `bulkhead_HingeHeavy_leaf` vs `leaf_skin` 0.0697 m
- `bulkhead_leaf_damper_mount` vs `leaf_skin` 0.0597 m

Those four also fail F-CLIP-HW, whose cap is 0.030 m even when a pair is listed. They were left failing. No allowlist row was added above 0.030 m, and no leaf-versus-frame row was raised above 0.010 m.

Floor pairs:

- `hatch_HingeBearing_frame` vs `frame_skin` 0.070 m at every pose
- `hatch_RotaryDamper` vs `frame_skin` 0.0358 m at every pose
- `leaf_skin` vs `frame_skin` 0.0115 m at q=0, 0.0113 m at q=26.25, 0.0152 m at q=105

The floor leaf-versus-frame cap stays 0.010 m. The perimeter gap is still 6.00 mm. Moving the leaf to clear 15.2 mm would break that gap. The bearing and the rotary damper sit in the frame skin deeper than both the 0.010 m skin cap and the 0.030 m hardware cap.

Gaps that do pass: hatch deflated leaf-to-opening 6.00 mm, inflated seal compression 8.00 mm. Floor hatch W/E/S 6.00 mm (N is the open hinge channel), inflated compression 8.00 mm. Pair meet 5.00 mm, hinge 4.79 mm, floor 10.00 mm. Pocket meet 0.00, bolt 3.10, jamb 6.00, floor 8.00, soffit 10.00, lap 24.95. R8 passes on all five.

F-CLIP-SWEEP on bay3 is a clearance, measured 0.527 m against a minimum of 0.300 m. It passes. The other doors record 0.300 m as not applicable and pass.

## Rendered clip, luma, amber, strip, readout

Leaf-rect clip is the percent of pixels with any channel at or above 250, limit 5%. The first windowed shot pass failed these. The second reshoot is the table below. Limits were not loosened.

| door | before | after worst | hero | jamb | detail |
| --- | --- | --- | --- | --- | --- |
| pocket | detail 16.43%; luma 0.6668; strip 0 | 0.00% | 0.00 including hero_final | 0.00 | 0.00 |
| bay3 | strip 0.00011; amber err 0.4353 rgb 109,112,116 (3 samples) | 0.00% | 0.00 | 0.00 | 0.00 |
| pair | detail 27.43%; amber err 0.4157 rgb 113,114,111 (2 samples); strip 0.00110 | 0.0146% | hero_closed 0.01 | jamb_closed 0.01 | 0.00 |
| hatch | luma 0.0929; strip 0; clip already 1.99 | 1.99% | hero_closed 0.29, hero_final 0.29 | jamb_closed 0.34 | detail_closed 1.99 |
| floor | jamb 6.60% at rgb 255,145,7; strip 0.00032 | 0.00% | 0.00 | 0.00 | 0.00 |

Pocket also clips 0.00% on `head_closed` and `pocket_end_open`.

V-LUMA after: pocket 0.2041 (limit 0.25, lower half of hero_final and jamb_closed; leaf mean 0.137, floor 0.10), bay3 0.1747, pair 0.2648, hatch 0.1143, floor 0.2368. The non-pocket limit is a leaf-face mean of at least 0.10.

V-STRIP minimum consecutive frame difference, limit 0.004: pocket 0.0149, bay3 0.0471, pair 0.0177, hatch 0.0150, floor 0.0152. The first reshoot still had hatch strip 0.00000 because frames 5, 6, and 7 were byte-identical on the approach camera. The back camera, with the vestibule meshes hidden for those eight frames and then restored, cleared it.

V-AMBER-PX versus Color8(217, 115, 5). Error is the max channel delta. Limit is 12/255 = 0.0471.

| door | samples | rgb | error | result |
| --- | --- | --- | --- | --- |
| pocket | 0 | none | −1 | pass, no plate in frame |
| bay3 | 3 | 217, 115, 0 | 0.0196 | pass |
| pair | 2 | 217, 115, 0 | 0.0196 | pass |
| hatch | 1 | 217, 115, 0 | 0.0196 | pass |
| floor | 24 | 217, 115, 0 | 0.0196 | pass |

The unshaded handwheel material is Color8(217, 115, 5). The rendered pixel is 217, 115, 0. LampBar was left alone.

V-READOUT, crop standard deviation, blank if under 0.02: hatch 0.1630 pass. Pocket, bay3, pair, and floor measure −1 (no digit plate in that crop) and pass. Both hatch faces are DigitFace and read "100".

V-ALBEDO hottest channel, limit 0.90: pocket `slide_AntiLiftRoller_R1` 0.900, bay3 WearBar 0.900, pair WearBar 0.900, hatch `bulkhead_Beacon` 0.900, floor `hatch_stay_detent_knob` 0.900. All pass. The earlier hatch fail was 1.0 on `@MeshInstance3D@17`, a duplicate digit face. Digit faces are now albedo 0.90, glyph (0.75, 0.90, 0.85), unique name DigitFace.

V-PLATE: bay3 Leaf_2_Push_Bar distance 0.0014, emission off. Pair Leaf_R_Push_Bar distance 0.0014, emission off.

V-ZFIGHT-FLICKER measures 0.0 on all five (limit 0.00784). V-SHADOW measures 0.0.

Audio: V-AUDIO and R11 pass at 60, 20, and 15 Hz, missing cues 0. Worst error at 60 Hz is 0.0167 s (one tick) on pocket, pair, hatch, and floor. Bay3 is 0.0133 s. At 20 Hz the tolerance is 0.050 s: pocket, pair, hatch, and floor are 0.0500 s, and bay3 is 0.0400 s. At 15 Hz the tolerance is 0.0667 s: pocket, pair, hatch, and floor are 0.0667 s, and bay3 is 0.0633 s.

## M-98 through M-122

M-98. Before: target tables lived in the harness, and a phase could pass without a motion span. After: F-TRES-SRC passes on all five doors. Each row names the `.tres`, the sibling json, and `section7=true`. F-TIME uses the motion samples. See the timing table. No section 7 table was copied back into the harness.

M-99. Before: hinge, knuckle, damper, seal, sweep, and brush names were dropped from the hardware set, and the first mesh test reported the prism depths above. After: those parts are back in the test through the allowlist file, with a per-pair cap. Pocket, bay3, and pair are clean (leaf 2.5 mm, 9.2 mm, 2.5 mm). Hatch and floor stay open at the depths in the clip table. Listed parts are still in the test.

M-100. Closed in pass C and still closed here. The leaf is moving when it stops. At 60 Hz the reopen speed is pocket 0.60 m/s (cap 0.60), bay3 39.99 °/s (cap 40), pair 59.76 °/s (cap 60), hatch 19.99 °/s (cap 20), floor 20.00 °/s (cap 20). Stop distance is pocket 0.041 m, bay3 8.0, pair 6.0, hatch 12.0, floor 8.0. The stop-time slack is M-112, and that gate now passes without the extra tick.

M-101. Closed in pass C. This pass did not retune the walk. F-WALK-CLEAR passes at 60 Hz: pocket 1.486 m, bay3 0.877 m, pair 1.406 m, hatch 1.039 m, floor 0.923 m.

M-102. V-JUMP passes at 60 Hz under the 4.0 mm flat: pocket 3.98 mm, bay3 3.95 mm, pair 3.99 mm, hatch 1.72 mm, floor 0.87 mm. The cut accel and lurch tables stay held under M-114.

M-103. Lurch and settle stay at real duration (`lurch_scale` 1.0, `settle_scale` 1.0 on every profile). This pass did not scale them. R4 passes: pocket hump 0.0019 m, bay3 0.799°, pair 0.997°, hatch 0.300°, floor 0.000°.

M-104. Pocket flicker stays closed. V-ZFIGHT-FLICKER is 0.0 on Intel UHD 605 for all five doors.

M-105. Before this pass the rendered plates and bars were gold, around (255, 222, 9) and (255, 189–230, ~10). The first shot pass of this pass still sampled grey: bay3 err 0.4353 rgb 109,112,116 on 3 pixels, pair err 0.4157 rgb 113,114,111 on 2 pixels. After: bay3, pair, hatch, and floor sample 217,115,0, error 0.0196, under 12/255. The handwheel material is Color8(217, 115, 5). V-HW and R6 pass with empty missing lists. Hatch back face, wheel, and both "100" readouts are in `back_open.png`.

M-106. Lamp fade stays measured. F-LAMP-FADE is 0.075 s on every door, crossings above. Cue streams are assigned. R11 passes.

M-107. Shots completed and wrote metrics. The mirror path is the `--qa-door-lab-mirror` argument. `meta.json` records the GPU name.

M-108. `timing_authority` is `section_7`. `door_profiles` lists all five doors with mass, inertia, and the scales read from the resources. F-TRES-SRC passes.

M-109. Bay3 settle was the old 15 Hz failure. R4 on bay3 now passes at 60 Hz (0.799°). This pass did not retune settle.

M-110. F-LAT-MECH passes at 60 Hz: pocket 0.067 s (tol ±0.017), bay3 0.067 s, pair 0.050 s, hatch 0.133 s from the E hold, floor 0.133 s from the E hold. The extra tick of slack stays out.

M-111. R5 passes at 60 Hz. First-motion error is numerical dust: pocket 2.2e-8 s, bay3 4.5e-8 s, pair 2.3e-8 s, hatch 1.1e-7 s, floor 4.6e-8 s. The 1 ms slack stays out.

M-112. Before: stop time was not what the gate measured, and pair at 60 Hz had been 0.117 s against 0.10 s with a tick of slack. After: F-OBS-STOP uses the first tick at or under 2% of peak and compares it to `stop_s` with no added tick. 60 Hz numbers are in the timing section. All five pass. Inflated seal compression measures 8.00 mm on the bulkhead and on the floor hatch. The one-tick stop at seal contact stays excluded from R3. `stop_s` was not changed. Cue tolerance has no added 1 ms. Worst audio error at 60 Hz is 0.0167 s, which is one tick.

M-113. R11 passes against the section 7 cue times at 60, 20, and 15 Hz. Missing count is 0. Worst 60 Hz error is 0.0167 s.

M-114. Held. Pair and bay3 lurch tables were not restored and were not retuned. Pair open windows are the ones quoted in the timing section, including settle ending at 1.271 s. V-JUMP still passes at the 4 mm flat.

M-115. The floor hatch runs the same gate set as the other doors, including F-CLIP, F-OBS, V-LUMA, V-CLIP, and V-AMBER. It has a shots folder. The open rows are the three clip rows above, not missing coverage.

M-116. Top cameras are part of the shot set that was copied. This pass did not reopen a blank-top failure. New framing work is G-V2 and G-V3.

M-117. Phase spans now come from motion, and F-TIME fails when a published window is missing. Hatch close is 7.800 s at 60 and 20 Hz and 7.800 s at 15 Hz. Floor close is 6.400 s at all three rates (spec 6.39, profile 6.390). The stretch that had pushed hatch close to 7.983 s and floor close to 6.633 s is gone. Pocket, bay3, and pair phase checks pass at all three rates after the short-window fill described under timing.

M-118. Floor V-GAP-HATCH passes: W/E/S 6.00 mm, inflated compression 8.00 mm. V-HW passes with an empty missing list (hinge tube, torsion anchor, rotary damper are present). The white pit and the stripe moiré are gone from the clip numbers: V-CLIP is 0.00%. The remaining floor failures are mesh embed, not the gap.

M-119. Before, on the first shot pass of this pass: pocket detail clip 16.43% and luma 0.6668, pair detail clip 27.43%, bay3 strip frozen at 0.00011, hatch strip 0 and luma 0.0929, floor jamb clip 6.60%, hatch front readout had been a blank grey in the prior re-test. After the second reshoot every V-CLIP, V-LUMA, V-STRIP, and V-READOUT row passes. Numbers are in the render table. The detail-fill light is energy 0.08 with specular 0. The floor hazard squares are unshaded Color8 amber, so they no longer render (255, 145, 7). Hatch face fill is local energy 0.60. Global ambient stayed 0.18 and exposure stayed 1.0.

M-120. Pair V-GAP-PAIR passes: meet 5.00 mm, hinge 4.79 mm, floor 10.00 mm. The 5 mm meet is still the runtime leaf scale in M-122 (0.9973 on each TT_LeafBody, gap delta 0.00250 m). Summary `fails` matches the seven metric rows. The git stamp is the write-tree pair above, and it records `dirty: true`.

M-121. Floor hatch cues are four open clunks at 1.456, 1.474, 1.492, 1.510 s and four close clunks at 5.346, 5.364, 5.382, 5.400 s in `floorhatch.json`. The bulkhead still has eight. R11 and V-AUDIO pass at 60, 20, and 15 Hz with missing 0. Worst floor error at 60 Hz is 0.0167 s.

M-122. Pending Rook bake. The runtime edits are still in the rig and are logged. No new GLB edit was added. Pocket and bay3 log "no runtime mesh edit recorded on this door; pending Rook bake".

Pair, three rows:

- Frame: rewrote 112 concave collision vertices, left_x 2.643, right_x 4.557. Visual frame unchanged.
- TT_LeafBody: x-scale 0.9973 about the hinge, gap delta 0.00250 m, so the meeting gap is 5 mm.
- TT_LeafBody: the same scale on the other leaf.

Hatch, 17 rows: dogs 01–08 pulled in by factor 0.683, linkages 01–08 pulled in by factor 0.538, and TT_LeafBody factor 1 because the rods are already inside.

Floor hatch, 8 rows: dogs 01–04 factor 0.418, linkages 01–04 factor 0.489.

R14 still passes on pivot names ("glb files not edited"). That is the known hole: the lab is not testing the unmodified GLB.

## Vance G-V

G-V1. Floor hatch plays four dog clunks at the section 7 times above. Phase windows were not moved. Open dogs stay 1.02–1.50 s (0.48 s). Close dogs stay 4.92–5.40 s (0.48 s). The bulkhead keeps eight clunks. Audio passes as in M-121.

G-V2. `head_closed.png` shows both leaves from the approach side, the header track, and the head mechanism, with a dark surround. `pocket_end_open.png` fills the frame with the open right leaf and a vertical green status strip. `detail_open` is the access-panel pose: exact node `slide_AccessPanel`, +90 degrees. `pocket_wear_closeup.png` is a dark leaf face with a faint horizontal scuff and the green strip at the frame. It is no longer a flat grey card. The wear mark is small. Rook's reference renders under `/workspace/renders/doorlab_passG/` are not on this PC.

G-V3. `back_open.png` shows the plug swung open, the handwheel, both "100" readouts on the near jamb, and the far wall through the opening. `latch_edge_19.png` is a tight view of one dog-rod tip and a slice of the orange wheel at t=1.9 s. The pushoff rams were nudged −0.012 m on Z for that shot only and then restored. The crop is readable. It is a close-up of the rod tip, not a wide shot of every ram.

G-V4. Both hatch digit faces read "100". V-READOUT standard deviation is 0.1630 against a blank floor of 0.02. The other doors have no digit plate in the approach crop and measure −1, which passes.

G-V5. Pocket lower panels are the #84 glass: albedo (0.30, 0.36, 0.42), alpha 0.25, roughness 0.05, with a graphite backer so the unshaded floor does not show through. V-LUMA lower-half max is 0.2041 against 0.25. Leaf mean is 0.137. Clip on hero_final and jamb_closed is 0.00%, under 5%. Roughness was not raised.

G-V6. `godot_tree` and the origin note are in the stamp section. Rendered amber on bay3, pair, hatch, and floor is 217,115,0 against the Color8(217, 115, 5) swatch, error 0.0196. Pocket has no plate.

G-V7. The shot pass copied the run tree to `C:\Users\upchu\aegis_shots\doorlab_G`, including the back, closeup, jamb, threshold, and top shots. At that copy the two trees had the same 284 file names and the same 260 png names. This report and the repaired `meta.json` are copied in after the fact. Shots were not run again.

## Sloane S1–S5

Official #86 scores were pocket 3.63 (Mat), bay3 3.38 (Artifact 2), pair 3.50 (Mat, Wear 2), hatch 3.75 (Motion 3), floor hatch 3.25 (Mat, Wear 2). The bar is average at least 4, nothing under 3, and Mat, Status, and Motion each at least 4.

S1. Lower pocket panels use the #84 glass and a graphite LowerBacker. WearHandle and WearKick stay pearl. Walls are graphite (0.157, 0.180, 0.220), roughness 0.85, not the old HDR 2.19 albedo. `head_closed` shows both leaves, the header, the frit X, and small pearl wear squares. The upper-left white disc is gone. A cyan status lamp remains on the left jamb. Glass roughness stays 0.05.

S2. Bay3 frit is (0.42, 0.45, 0.48) with alpha-to-coverage, and the shots use MSAA 4x. Key shadow opacity is 0.35 and shadow blur is 1.5. V-CLIP is 0.00% on hero, jamb, and detail. Amber samples are 217,115,0.

S3. Pair leaves are pearl (0.78, 0.80, 0.80), roughness 0.35, metallic specular 0.20, cladding texture cleared. Wear stays albedo times 1.06 and roughness minus 0.15. The jamb lamp stays state-driven. LampBar was not painted amber. V-CLIP worst is 0.0146%. Amber samples are 217,115,0 on 2 pixels.

S4. Hatch open dogs in section7 are 1.02–1.50 s (0.48 s). Close dogs are 6.33–6.81 s (0.48 s). `dwell_s` is 0.15. Both sit inside the 0.5 s and 0.2 s asks, and both are the published windows. Shortening either one would miss those windows and fail R2. The 7.8 s close was not touched. Measured close is 7.800 s at 60, 20, and 15 Hz. The readout is legible at hero distance (std 0.163, both faces "100"). The wheel samples 217,115,0 on 1 pixel.

S5. Floor dogs already sit in 0.48 s windows (open 1.02–1.50, close 4.92–5.40), which is inside 0.5 s. The same R2 limit applies: those windows were not tightened. The lid normal is off. WearLid is a patch at (0.16, 0.040, 0.62), size (0.18, 0.006, 0.12). Corner lamps are 40 mm cubes (0.04, 0.032, 0.04) at y 0.048, unshaded Color8 amber. The hazard checker is unshaded amber, so the old (255, 145, 7) clip is gone. V-CLIP is 0.00%. V-ALBEDO hottest is 0.900. The 0.90 limit was not raised.

## Self-scores, not official

Scale is the #86 set: Materials, Artifact, Wear, Status, Motion. Wear stays at 3 on every door. The wear that exists is a small pearl square, a wear-bar albedo at the 0.90 cap, or a 180 by 120 mm lid patch. `pocket_wear_closeup.png` shows a faint scuff on a very dark leaf. That is not a 4.

| door | Mat | Artifact | Wear | Status | Motion | average |
| --- | --- | --- | --- | --- | --- | --- |
| pocket | 4 | 4 | 3 | 4 | 4 | 3.8 |
| bay3 | 4 | 4 | 3 | 4 | 4 | 3.8 |
| pair | 4 | 4 | 3 | 4 | 4 | 3.8 |
| hatch | 4 | 4 | 3 | 4 | 4 | 3.8 |
| floor | 4 | 4 | 3 | 4 | 4 | 3.8 |

Mat, Status, and Motion are 4. Nothing is under 3. The average is under 4 because wear is still small. These numbers are not a vote.

## Still open

- M-122 pending Rook bake. The three families of runtime mesh edits above stay until the GLBs absorb them.
- Hatch hinge and damper embeds: 86 mm, 76 mm, 69.7 mm, and 59.7 mm. They miss both the 0.010 m skin cap and the 0.030 m hardware cap.
- Floor hinge bearing versus frame 70 mm, rotary damper versus frame 35.8 mm, leaf versus frame 15.2 mm at full open (11.5 mm closed). The 6 mm perimeter gap and the 0.010 m leaf-frame cap both stay.
- Hatch and floor dog phases and the hatch dwell are already inside 0.5 s and 0.2 s. They are the published section 7 windows. Tightening them would fail R2. The 7.8 s close stays.
- Tree `932f8ec` is not an object on origin. Use the write-tree hashes in the stamp section.
- `summary.json` verdict stays FAIL for the seven clip rows. The visual FAIL flag on that file counts those same rows.

Other functional rows checked at 60 Hz and passing: R1, R3, R8, F-SCALAR (pocket max |k−spec| 0.049, others 0), F-KE, F-STALL-OPEN, F-CYCLE 50, F-CLIP-COPLANAR 0, V-EASE-SCURVE, V-HW, R6, R14.
