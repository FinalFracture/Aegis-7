# Tennis Tower: texture needs for Sloane (Rook, Nov 4 2026)
Not sent. Kept as a file per Jared. Materials currently use flat colours (untextured) unless listed as mapped.

## Already mapped (no action needed unless restyling)
TT_Gunmetal, TT_BrushedSteel, TT_CarbonSlate, Glass, TT_WhiteComposite, TT_BrushedAlloy, TT_StairGunmetal (existing facade/qa03/stair PBR textures).

## Needed
- TT_Leaf / TT_LeafLight: leaf crests, foliage, vines and leaf relief (ridge crown #73, playground, benches). Tileable leaf-green albedo/normal.
- TT_Soil: soil/berm mounds (playground).
- TT_BallYellow: tennis-ball holds/finials, felt look (climbing #60, bar #62, fence #71).
- TT_AmberLED / TT_CyanLED: emissive court-line strips (bar, climbing, fence).
- TT_StairSlate: stair finish (check it matches the Rev C stair PBR).
- TT_AccentViolet / TT_StatusGreen: status accents (emissive).
- Cabana (#61): TT_CabanaCanvas_White, TT_Upholstery_FabricSlate (tileable, matches atlas UV_FABRIC_SLATE), TT_Cushion_Button (optional).
- Playground (#63-#72): TT_PlayRubber_Moss, poured EPDM (green base, blue river, grey stones, tan pads), HDPE_Leaf / HDPE_Sand (slides, slats), and yellow HDPE slide plastic.
- Restrooms (#58): bath-pod white/mirror/cyan albedo exceeds 0.9 (first-pass warning). Needs a tuned albedo.
- Ridge crown (#73): slate roof facet texture (TT_CarbonSlate scale at 20 m), weathered gunmetal ridge/glazing caps.
- Roof bay / curtain wall (#52/#55): roof glass tint consistency across the Glass Box (single BLEND layer).
