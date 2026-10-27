#!/usr/bin/env python3
"""
check_context.py — Context, Token Load & Usage Credit (UC) Budget Monitor for Cylinder Hab-7 Team
Managed by Scribe (3b011c08-32f8-434e-8285-6cd66198bf29)

Usage:
  python3 /workspace/game-project/context/check_context.py [--update-status]
  python3 /workspace/game-project/context/check_context.py --reset-budget [--account-pct 0.0] [--budget-uc 10.0]
"""
import argparse
import datetime
import json
import re
from pathlib import Path

CONTEXT_DIR = Path("/workspace/game-project/context")
TRANSCRIPTS_DIR = CONTEXT_DIR / "transcripts"
STATUS_PATH = CONTEXT_DIR / "STATUS.md"
BUDGET_PATH = CONTEXT_DIR / "usage_budget.json"

# Per-Bot Rotation Thresholds per CONTEXT_PROTOCOL.md (150k cap per Jared):
WARN_TOKENS = 120000
ROTATE_TOKENS = 150000
ROTATE_BYTES = 600 * 1024

# Usage Credit (UC) Exchange Rate (Calibrated from 7% -> 50% = 43% over 1,162,036 project context tokens):
TOKENS_PER_UC = 29447  # 1 UC = 1% Account Usage = 27,024 team context tokens (~105.6 KB transcript)
DEFAULT_SPRINT_BUDGET_UC = 10.0  # 10% Account Usage cap before pausing work (270,240 tokens)
DEFAULT_SPRINT_WARN_UC = 8.0     # 8% Account Usage warning threshold (216,192 tokens)

DEFAULT_TEAM = [
    {"name": "Atlas", "id": "3a664a65-34d6-47ae-a9f6-337906efe2a3", "role": "Game PM", "handoff_v1": "atlas-handoff-v4.md"},
    {"name": "Vance", "id": "245e93a0-6301-45d6-b371-ad1e37a0dfd1", "role": "Sci-Fi Architect, Movie Prop & Set Design Specialist", "handoff_v1": "vance-handoff-v2.md"},
    {"name": "Sloane", "id": "bf6c8763-6c8b-405e-bb10-e7201e756464", "role": "Interior, Lighting & Texture Designer", "handoff_v1": "sloane-handoff-v3.md"},
    {"name": "Rook", "id": "b2e64c87-0269-4f42-b5da-44d4b1a59db2", "role": "3D Modeling Specialist", "handoff_v1": "rook-handoff-v3.md"},
    {"name": "Gage", "id": "5a97ab49-19f0-4b33-889f-e9b5a5389451", "role": "Godot 4 Developer", "handoff_v1": "gage-handoff-v3.md"},
    {"name": "Quinn", "id": "2239f53a-2bae-4c89-926c-e4969c082273", "role": "Market Research & Gameplay Mechanics Strategist", "handoff_v1": "quinn-handoff-v2.md"},
    {"name": "Scribe", "id": "3b011c08-32f8-434e-8285-6cd66198bf29", "role": "Context & Handoff Manager", "handoff_v1": "scribe-handoff-v5.md"},
    {"name": "Patch", "id": "0ae8822a-f155-4a07-a4d9-a0f01c05e10b", "role": "QA & Automated Playtester Specialist", "handoff_v1": "patch-handoff-v1.md"},
]

RETIRED_TEAM = [
    {"name": "delete-Atlas (v1)", "id": "60544a5c-ba31-4517-bd12-0fbc8e8ff9f0", "role": "Game PM"},
    {"name": "delete-Atlas (v3)", "id": "e744c2d9-fd3b-4916-a082-3cedfae0b695", "role": "Game PM"},
    {"name": "delete-Vance (v1)", "id": "0724beeb-94b9-43fa-a9cf-27117c5d4aa6", "role": "Sci-Fi Architect, Movie Prop & Set Design Specialist"},
    {"name": "delete-Sloane (v1)", "id": "1c40e57b-57c1-4cbf-9e29-cc227b9cc914", "role": "Interior, Lighting & Texture Designer"},
    {"name": "delete-Sloane (v2)", "id": "ec8a7e65-dd93-415c-9240-465e61fb2bcb", "role": "Interior, Lighting & Texture Designer"},
    {"name": "delete-Rook (v1)", "id": "11c68e8e-c070-4e83-a926-21e9dfb70523", "role": "3D Modeling Specialist"},
    {"name": "delete-Rook (v2)", "id": "61237674-1923-48c9-bc64-19c16cf2501e", "role": "3D Modeling Specialist"},
    {"name": "delete-Gage (v1)", "id": "6ec49577-c331-44b3-8b56-dee044ba1d84", "role": "Godot 4 Developer"},
    {"name": "delete-Gage (v2)", "id": "5c9c9f64-e799-4958-97ab-f8cbf4f6ff90", "role": "Godot 4 Developer"},
    {"name": "delete-Quinn (v1)", "id": "65d82323-1864-40e3-b8eb-90acde92ed1d", "role": "Market Research & Gameplay Mechanics Strategist"},
    {"name": "delete-Scribe (v1)", "id": "713ef1f9-ed46-4e44-835d-c732a5f11ecd", "role": "Context & Handoff Manager"},
    {"name": "delete-Scribe (v2)", "id": "4ea864bb-316a-47d3-8dc0-bd12475470c8", "role": "Context & Handoff Manager"},
    {"name": "delete-Scribe (v3)", "id": "49521640-e6fc-4f8f-b873-726f3f599220", "role": "Context & Handoff Manager"},
    {"name": "delete-Scribe (v4)", "id": "929b3cf3-1ba3-489f-945f-4734223c6605", "role": "Context & Handoff Manager"},
]

POS_RE = re.compile(r"positions\s+(\d+)[–-](\d+)\s+of\s+(\d+)")


def measure_agent(agent_id: str) -> dict:
    page_files = sorted(TRANSCRIPTS_DIR.glob(f"{agent_id}_p*.txt"))
    if not page_files:
        single = TRANSCRIPTS_DIR / f"{agent_id}.txt"
        if single.exists():
            page_files = [single]

    total_positions = 0
    covered_positions = set()
    sampled_bytes = 0

    for pf in page_files:
        raw = pf.read_text(encoding="utf-8", errors="replace")
        m = POS_RE.search(raw)
        json_lines = [line for line in raw.splitlines() if line.startswith("{")]
        if m:
            start_pos, end_pos, total_pos = int(m.group(1)), int(m.group(2)), int(m.group(3))
            total_positions = max(total_positions, total_pos)
            for idx, line in enumerate(json_lines):
                pos = start_pos + idx
                if pos not in covered_positions:
                    covered_positions.add(pos)
                    sampled_bytes += len(line.encode("utf-8"))
        else:
            for idx, line in enumerate(json_lines):
                covered_positions.add(idx)
                sampled_bytes += len(line.encode("utf-8"))
            total_positions = max(total_positions, len(covered_positions))

    if covered_positions and total_positions > len(covered_positions):
        avg_bytes_per_pos = sampled_bytes / len(covered_positions)
        est_raw_bytes = int(avg_bytes_per_pos * total_positions)
    else:
        est_raw_bytes = sampled_bytes

    msg_count = total_positions or len(covered_positions)
    est_tokens = est_raw_bytes // 4
    pct_of_threshold = round((est_tokens / ROTATE_TOKENS) * 100, 1)

    if est_tokens >= ROTATE_TOKENS or est_raw_bytes >= ROTATE_BYTES:
        status = "ROTATE NOW (>= 150k tok / 600 KB)"
    elif est_tokens >= WARN_TOKENS:
        status = "WARNING (>= 120k tok, Below 150k Cap — Handoff v4 Staged)"
    else:
        status = "HEALTHY (Below 120k warn / 150k cap)"

    return {
        "messages": msg_count,
        "sampled_messages": len(covered_positions),
        "raw_bytes": est_raw_bytes,
        "raw_kb": round(est_raw_bytes / 1024, 1),
        "est_tokens": est_tokens,
        "pct_threshold": pct_of_threshold,
        "status": status,
    }


def load_budget_config() -> dict:
    if BUDGET_PATH.exists():
        return json.loads(BUDGET_PATH.read_text(encoding="utf-8"))
    return {
        "sprint_name": "Cylinder Hab-7 Interior Overhaul Sprint (Post-Monday 06:27 CDT Weekly Reset)",
        "weekly_reset_schedule": "Mondays at 6:27 AM CDT (latest reset: 2026-10-26 06:27 CDT)",
        "exchange_rate_tokens_per_uc": TOKENS_PER_UC,
        "baseline_account_usage_pct": 0.0,
        "target_pause_account_usage_pct": 10.0,
        "sprint_budget_uc": DEFAULT_SPRINT_BUDGET_UC,
        "sprint_warn_uc": DEFAULT_SPRINT_WARN_UC,
        "sprint_budget_tokens": int(DEFAULT_SPRINT_BUDGET_UC * TOKENS_PER_UC),
        "per_bot_allowance_tokens": int((DEFAULT_SPRINT_BUDGET_UC * TOKENS_PER_UC) // 6),
        "per_bot_allowance_uc": round(DEFAULT_SPRINT_BUDGET_UC / 6, 2),
        "baseline_lifetime_tokens": 1274265,
        "baseline_active_tokens": 240106,
        "target_pause_lifetime_tokens": 1544505,
        "baseline_by_bot": {
            "Atlas": 42523,
            "Vance": 26052,
            "Sloane": 32644,
            "Rook": 39348,
            "Gage": 30145,
            "Scribe": 69394,
        },
    }


def compute_budget_metrics(metrics_by_name: dict, retired_metrics: list, budget_cfg: dict) -> dict:
    tok_per_uc = budget_cfg.get("exchange_rate_tokens_per_uc", TOKENS_PER_UC)
    sprint_budget_uc = float(budget_cfg.get("sprint_budget_uc", DEFAULT_SPRINT_BUDGET_UC))
    sprint_warn_uc = float(budget_cfg.get("sprint_warn_uc", DEFAULT_SPRINT_WARN_UC))
    sprint_budget_tokens = int(round(sprint_budget_uc * tok_per_uc))
    baseline_lifetime = int(budget_cfg.get("baseline_lifetime_tokens", 1274265))
    baseline_acct_pct = float(budget_cfg.get("baseline_account_usage_pct", 0.0))

    active_tokens = sum(m["est_tokens"] for m in metrics_by_name.values())
    active_kb = round(sum(m["raw_kb"] for m in metrics_by_name.values()), 1)
    active_msgs = sum(m["messages"] for m in metrics_by_name.values())

    retired_tokens = sum(r["metrics"]["est_tokens"] for r in retired_metrics)
    retired_kb = round(sum(r["metrics"]["raw_kb"] for r in retired_metrics), 1)
    retired_msgs = sum(r["metrics"]["messages"] for r in retired_metrics)

    lifetime_tokens = active_tokens + retired_tokens
    lifetime_kb = round(active_kb + retired_kb, 1)
    lifetime_msgs = active_msgs + retired_msgs

    sprint_delta_tokens = max(0, lifetime_tokens - baseline_lifetime)
    sprint_used_uc = sprint_delta_tokens / tok_per_uc
    sprint_remaining_tokens = max(0, sprint_budget_tokens - sprint_delta_tokens)
    sprint_remaining_uc = max(0.0, sprint_budget_uc - sprint_used_uc)
    sprint_pct_of_cap = round((sprint_used_uc / sprint_budget_uc) * 100, 1) if sprint_budget_uc > 0 else 0.0
    est_current_account_pct = round(baseline_acct_pct + sprint_used_uc, 2)
    target_pause_account_pct = round(baseline_acct_pct + sprint_budget_uc, 2)

    if sprint_used_uc >= sprint_budget_uc or sprint_delta_tokens >= sprint_budget_tokens:
        budget_status = (
            f"PAUSE WORK IMMEDIATELY — {sprint_budget_uc:.1f} UC ({sprint_budget_uc:.1f}% Account Usage / "
            f"+{sprint_budget_tokens:,} tok) Sprint Cap Reached!"
        )
    elif sprint_used_uc >= sprint_warn_uc:
        budget_status = (
            f"BUDGET WARNING — {sprint_used_uc:.2f} / {sprint_budget_uc:.1f} UC Used "
            f"({sprint_pct_of_cap}% of {sprint_budget_uc:.1f} UC Cap — Prepare to Pause)"
        )
    else:
        budget_status = (
            f"WITHIN BUDGET — {sprint_used_uc:.2f} / {sprint_budget_uc:.1f} UC Used "
            f"({sprint_remaining_uc:.2f} UC / {sprint_remaining_tokens:,} tok remaining before pause)"
        )

    per_bot_allowance_tok = int(budget_cfg.get("per_bot_allowance_tokens", sprint_budget_tokens // len(DEFAULT_TEAM)))
    baseline_by_bot = budget_cfg.get("baseline_by_bot", {})
    per_bot_deltas = {}
    for bot in DEFAULT_TEAM:
        bname = bot["name"]
        base_tok = int(baseline_by_bot.get(bname, 0))
        curr_tok = metrics_by_name[bname]["est_tokens"]
        delta_tok = max(0, curr_tok - base_tok)
        delta_uc = delta_tok / tok_per_uc
        pct_allowance = round((delta_tok / per_bot_allowance_tok) * 100, 1) if per_bot_allowance_tok > 0 else 0.0
        per_bot_deltas[bname] = {
            "baseline_tokens": base_tok,
            "current_tokens": curr_tok,
            "delta_tokens": delta_tok,
            "delta_uc": delta_uc,
            "allowance_tokens": per_bot_allowance_tok,
            "allowance_uc": per_bot_allowance_tok / tok_per_uc,
            "pct_allowance": pct_allowance,
        }

    return {
        "sprint_name": budget_cfg.get("sprint_name", "Cylinder Hab-7 Interior Overhaul Sprint (Post-Monday 06:27 CDT Weekly Reset)"),
        "weekly_reset_schedule": budget_cfg.get("weekly_reset_schedule", "Mondays at 6:27 AM CDT (latest reset: 2026-10-26 06:27 CDT)"),
        "tok_per_uc": tok_per_uc,
        "sprint_budget_uc": sprint_budget_uc,
        "sprint_warn_uc": sprint_warn_uc,
        "sprint_budget_tokens": sprint_budget_tokens,
        "baseline_lifetime_tokens": baseline_lifetime,
        "baseline_active_tokens": int(budget_cfg.get("baseline_active_tokens", active_tokens)),
        "target_pause_lifetime_tokens": baseline_lifetime + sprint_budget_tokens,
        "baseline_account_pct": baseline_acct_pct,
        "est_current_account_pct": est_current_account_pct,
        "target_pause_account_pct": target_pause_account_pct,
        "active_tokens": active_tokens,
        "active_kb": active_kb,
        "active_msgs": active_msgs,
        "retired_tokens": retired_tokens,
        "retired_kb": retired_kb,
        "retired_msgs": retired_msgs,
        "lifetime_tokens": lifetime_tokens,
        "lifetime_kb": lifetime_kb,
        "lifetime_msgs": lifetime_msgs,
        "sprint_delta_tokens": sprint_delta_tokens,
        "sprint_used_uc": sprint_used_uc,
        "sprint_remaining_tokens": sprint_remaining_tokens,
        "sprint_remaining_uc": sprint_remaining_uc,
        "sprint_pct_of_cap": sprint_pct_of_cap,
        "budget_status": budget_status,
        "per_bot_deltas": per_bot_deltas,
    }


def generate_status_md(metrics_by_name: dict, retired_metrics: list, budget: dict) -> str:
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S CDT")
    lines = [
        "# Team Context, Token Health & 10% Usage Budget Status (`STATUS.md`)",
        "",
        f"- **Last Checked:** {now_str}",
        "- **Managed By:** Scribe (`3b011c08-32f8-434e-8285-6cd66198bf29`)",
        "- **Project:** *Cylinder Hab-7* (O'Neill Cylinder Habitat — Unified Aegis-7 Standard)",
        "- **Per-Bot Rotation Cap:** **`150,000` estimated tokens** (~`600 KB` raw JSON transcript) | Warning at **`120,000` tokens** (`80%`)",
        f"- **Weekly Account Usage Reset Schedule:** **{budget['weekly_reset_schedule']}**",
        f"- **Team Usage Currency (`UC`):** **`1 UC` = `1%` Account Usage = `{budget['tok_per_uc']:,}` team context tokens** (`~115.0 KB` transcript / `~45` messages, recalibrated at `25.0%` weekly usage (`25.5%` live = `28,869` tok/UC) from `+736,168` post-reset tokens (`+9.0%` vs old `27,024` tok/UC))",
        f"- **Active Sprint (`{budget['sprint_name']}`):** **`{budget['sprint_budget_uc']:.1f} UC` (`+{budget['sprint_budget_tokens']:,}` new team context tokens)** (`{budget['baseline_account_pct']:.1f}% -> {budget['target_pause_account_pct']:.1f}%` post-reset account usage; hard pause at `{budget['target_pause_lifetime_tokens']:,}` lifetime project tokens)",
        "",
        f"## Team Usage Credit (`UC`) Budget Meter (Hard Pause at `{budget['sprint_budget_uc']:.1f} UC` / `+{budget['sprint_budget_tokens']:,}` Tokens)",
        "",
        "| Metric | Value | Notes |",
        "| :--- | :--- | :--- |",
        f"| **Sprint Budget Status** | **{budget['budget_status']}** | Hard pause at `{budget['sprint_budget_uc']:.1f} UC` (`+{budget['sprint_budget_tokens']:,}` net new tokens) |",
        f"| **Cumulative Project Lifetime Tokens (All 22 Bots)** | **`{budget['lifetime_tokens']:,}` tok** (`{budget['lifetime_kb']:,.1f} KB` / `{budget['lifetime_msgs']:,}` msgs) | Active 8 bots: `{budget['active_tokens']:,}` tok + Retired 14 bots: `{budget['retired_tokens']:,}` tok |",
        f"| **Sprint Baseline (Post-Monday 06:27 CDT Weekly Reset)** | **`{budget['baseline_lifetime_tokens']:,}` tok** | Active 6-bot baseline: `{budget['baseline_active_tokens']:,}` tok (`2026-10-26 11:17 CDT`) |",
        f"| **Sprint Net New Tokens Burned** | **`+{budget['sprint_delta_tokens']:,}` / `{budget['sprint_budget_tokens']:,}` tok** (`{budget['sprint_pct_of_cap']}%`) | Remaining before pause: **`{budget['sprint_remaining_tokens']:,}` tok** |",
        f"| **Sprint Usage Credits (`UC`) Burned** | **`{budget['sprint_used_uc']:.2f}` / `{budget['sprint_budget_uc']:.2f} UC`** | Remaining before pause: **`{budget['sprint_remaining_uc']:.2f} UC`** (Warn at `{budget['sprint_warn_uc']:.1f} UC`) |",
        f"| **Estimated Post-Reset Account Usage** | **`~{budget['est_current_account_pct']:.2f}%`** (Target Pause Cap: **`{budget['target_pause_account_pct']:.1f}%`**) | Weekly usage reset Mondays at 11:28 UTC / 5:28 AM CST (`1 UC` = `29,447` tok at 25.0% / `28,869` tok at 25.5%) |",
        "",
        f"## Live Bot Context & Sprint Allowance Table (`~{budget['sprint_budget_tokens']//6:,}` tok / `{budget['sprint_budget_uc']/6:.2f} UC` Allowance per Bot)",
        "",
        f"| Bot Name | Agent ID | Role | Messages | Raw Transcript | Active Context Tokens | Load vs 150k Rotate Cap | Sprint Delta (`UC` Burned vs `{budget['sprint_budget_uc']/6:.2f} UC` Share) | Rotation Status | Active Handoff File |",
        "| :--- | :--- | :--- | ---: | ---: | ---: | ---: | :--- | :--- | :--- |",
    ]

    for bot in DEFAULT_TEAM:
        bname = bot["name"]
        m = metrics_by_name[bname]
        d = budget["per_bot_deltas"][bname]
        lines.append(
            f"| **{bname}** | `{bot['id']}` | {bot['role']} | {m['messages']} | {m['raw_kb']} KB | ~{m['est_tokens']:,} tok | {m['pct_threshold']}% | `+{d['delta_tokens']:,}` tok (`{d['delta_uc']:.2f}` / `{d['allowance_uc']:.2f} UC`, `{d['pct_allowance']}%`) | {m['status']} | `/workspace/game-project/context/{bot['handoff_v1']}` |"
        )

    lines.extend(
        [
            "",
            "## Retired Predecessor Instances Included in Lifetime Project Total (`14` Bots)",
            "",
            "| Retired Bot | Agent ID | Role | Messages | Raw Transcript | Final Context Tokens | Usage Credits (`UC`) |",
            "| :--- | :--- | :--- | ---: | ---: | ---: | ---: |",
        ]
    )

    for r in retired_metrics:
        rm = r["metrics"]
        ruc = rm["est_tokens"] / budget["tok_per_uc"]
        lines.append(
            f"| **{r['name']}** | `{r['id']}` | {r['role']} | {rm['messages']} | {rm['raw_kb']} KB | ~{rm['est_tokens']:,} tok | `{ruc:.2f} UC` |"
        )

    lines.extend(
        [
            "",
            "## Sleeping Quarters Fixtures (ALL 5 LOCKED) & 10-Room Pipeline Status",
            "- **Fixture #1 — EVA Suit & Personal Gear Locker (`locker_round1`):** **LOCKED WINNER `#02`** (`/workspace/game-project/assets/glb/winners/locker_winner_01_dual_bay_bulkhead.glb`, selected by Jared).",
            "- **Fixture #2 — Compact Hygiene & Sonic Wash Vanity (`vanity_round1`):** **LOCKED WINNER `#03` (5–0 Unanimous Vote)** (`/workspace/game-project/assets/glb/winners/vanity_winner_01_dual_zone_grooming.glb`).",
            "- **Fixture #3 — Personal Wall Terminal & Fold-Down Cabin Desk (`walldesk_round1`):** **LOCKED WINNER `#02` (5–0 Unanimous Vote)** (`/workspace/game-project/assets/glb/winners/walldesk_winner_01_split_comms_station.glb`).",
            "- **Fixture #6 — Modular Cargo & Footlocker Chest (`footlocker_round1`):** **LOCKED WINNER `#02` (5–0 Unanimous Vote)** (`/workspace/game-project/assets/glb/winners/footlocker_winner_01_split_cargo_trunk.glb`).",
            "- **Fixture #9 — Personal Climate & Life-Support Wall Panel (`climate_round1`):** **LOCKED WINNER `#02` (5–0 Unanimous Vote)** (`/workspace/game-project/assets/glb/winners/climate_winner_01_split_env_o2_station.glb`).",
            "- **Room 01 — Crew Sleeping Quarters (`room_01_sleeping_quarters.tscn`):** **COMPLETE & RENDERED** (`/workspace/game-project/godot/renders/rooms/room_01/room_01_sleeping_quarters_sheet.png`).",
            "- **Room 02 — Curved Ring Transit Corridor (`room_02_transit_corridor.tscn`):** **COMPLETE & RENDERED (5–0 Unanimous Vote for `#02`)** (`corridor_door_winner_01_dual_zone_portal.glb`, `/workspace/game-project/godot/renders/rooms/room_02/`).",
            "- **Rooms 03–10 Hero Fixtures (ALL 8 LOCKED 5–0 Unanimous for `#02` in `VOTE_LOG.md`):** `galley_synth_winner_01_dual_zone_synth_herb_tower.glb`, `med_autodoc_winner_01_dual_zone_autodoc_pharmacy.glb`, `eva_chamber_winner_01_dual_zone_decompression_gantry.glb`, `hydro_column_winner_01_dual_zone_aeroponic_bioscrubber.glb`, `bridge_console_winner_01_dual_zone_holotable_tower.glb`, `lounge_bar_winner_01_dual_zone_celestial_bar.glb`, `reactor_core_winner_01_dual_zone_plasma_cryo_bay.glb`, `cargo_gantry_winner_01_dual_zone_cargo_drone_dock.glb` — ALL 10 ROOMS (`rooms/room_01/` .. `rooms/room_10/`) COMPLETE & RENDERED WITH CONTACT SHEETS!",
            "",
            "## Phase 2: 15 O'Neill Cylinder Building Exteriors (`bldg_01`–`bldg_15`) & Metropolis Skyline (ALL 15 RENDERED & VOTED FOR `#02`)",
            "- **Master Exterior Bible:** `/workspace/game-project/MASTER_BUILDINGS_15_EXTERIORS.md` & `/workspace/game-project/design/vance_scifi_set_and_exterior_props_spec.md` (\"Aegis-7 Exterior Standard\" — 5 candidates per building `_r1_01`..`_r1_05`, 6-bot post-render vote (`Vance, Sloane, Rook, Gage, Scribe, Atlas`) in `VOTE_LOG.md`).",
            "- **District I — Residential & Civic Terrace Sector (`bldg_01`–`bldg_05`):** **COMPLETE & RENDERED** (`bldg_01_hab_spire` .. `bldg_05_celestial_promenade_dome` + `district_01_residential_civic.tscn`, canonical `#02` winners staged in `assets/glb/winners/`).",
            "- **District II — Agri-Biosphere & Research Sector (`bldg_06`–`bldg_10`):** **COMPLETE & RENDERED** (`bldg_06_hydroponic_biodome` .. `bldg_10_cryo_seed_vault` + `district_02_agri_research.tscn`, canonical `#02` winners staged in `assets/glb/winners/`).",
            "- **District III — Command, Power & Industrial Port Sector (`bldg_11`–`bldg_15`):** **COMPLETE & RENDERED** (`bldg_11_citadel_command_hq` .. `bldg_15_solar_mirror_control_pylon` + `district_03_command_industrial.tscn`, canonical `#02` winners staged in `assets/glb/winners/`).",
            "- **Grand 15-Building Metropolis Scene:** **COMPLETE & RENDERED** (`cylinder_hab7_metropolis.tscn`, `/workspace/game-project/godot/renders/buildings/metropolis/cylinder_hab7_metropolis_sheet.png`).",
            "",
            "## Phase 3: 5 Exterior Sci-Fi Movie Set Props (`prop_01`–`prop_05`) & 5 District IV Building Exteriors (`bldg_16`–`bldg_20`) (COMPLETE & RENDERED — ALL 10 LOCKED 6–0 UNANIMOUS FOR `#02`)",
            "- **Part A — 5 Exterior Sci-Fi Movie Set & Plaza Props (`prop_01_round1`..`prop_05_round1`, 25 `.glb`s in `assets/glb/props/`, voting sheets in `godot/renders/props/prop_01..05/`, canonical `#02` winners staged in `assets/glb/winners/`):**",
            "  - `prop_01_maglev_shuttle_pylon` — **LOCKED WINNER `#02` (6–0 Unanimous)** (`prop_01_winner_01_maglev_shuttle_pylon.glb`, `2,016` tris)",
            "  - `prop_02_holo_wayfinding_kiosk` — **LOCKED WINNER `#02` (6–0 Unanimous)** (`prop_02_winner_01_holo_wayfinding_kiosk.glb`, `1,960` tris)",
            "  - `prop_03_atmo_scrubber_bollard` — **LOCKED WINNER `#02` (6–0 Unanimous)** (`prop_03_winner_01_atmo_scrubber_bollard.glb`, `1,908` tris)",
            "  - `prop_04_civic_planter_bench_pod` — **LOCKED WINNER `#02` (6–0 Unanimous)** (`prop_04_winner_01_civic_planter_bench_pod.glb`, `1,976` tris)",
            "  - `prop_05_vtol_medevac_pad_array` — **LOCKED WINNER `#02` (6–0 Unanimous)** (`prop_05_winner_01_vtol_medevac_pad_array.glb`, `2,212` tris)",
            "- **Part B — 5 District IV Building Exteriors (`bldg_16_round1`..`bldg_20_round1`, 25 `.glb`s in `assets/glb/buildings/`, voting sheets in `godot/renders/buildings/bldg_16..20/`, canonical `#02` winners staged in `assets/glb/winners/`):**",
            "  - `bldg_16_shipyard_drydock_hall` — **LOCKED WINNER `#02` (6–0 Unanimous)** (`bldg_16_winner_01_shipyard_drydock_hall.glb`, `4,664` tris)",
            "  - `bldg_17_coriolis_recreation_arena` — **LOCKED WINNER `#02` (6–0 Unanimous)** (`bldg_17_winner_01_coriolis_recreation_arena.glb`, `4,996` tris)",
            "  - `bldg_18_colonial_holo_museum` — **LOCKED WINNER `#02` (6–0 Unanimous)** (`bldg_18_winner_01_colonial_holo_museum.glb`, `4,532` tris)",
            "  - `bldg_19_synth_brewery_refinery` — **LOCKED WINNER `#02` (6–0 Unanimous)** (`bldg_19_winner_01_synth_brewery_refinery.glb`, `5,328` tris)",
            "  - `bldg_20_meteor_defense_bastion` — **LOCKED WINNER `#02` (6–0 Unanimous)** (`bldg_20_winner_01_meteor_defense_bastion.glb`, `5,328` tris)",
            "- **District IV & Expanded 20-Building Metropolis Scenes:** **COMPLETE & RENDERED** (`district_04_shipyard_civic.tscn` -> `/workspace/game-project/godot/renders/buildings/district_04/district_04_sheet.png`; `cylinder_hab7_metropolis.tscn` -> `/workspace/game-project/godot/renders/buildings/metropolis/cylinder_hab7_metropolis_sheet.png`).",
            "",
            "## Phase 4: Cylinder Hab-7 Interior Overhaul & 5 Macro-Setpieces (COMPLETE & RENDERED — ALL 5 LOCKED 6–0 UNANIMOUS FOR `#02`)",
            "- **Full-Scale O'Neill Cylinder Exterior (`cylinder_round1`):** **LOCKED WINNER `#02` (6–0 Unanimous)** (`cylinder_winner_01_hab7_exterior.glb`, `/workspace/game-project/godot/renders/cylinder/cylinder_round1_voting_sheet.png`).",
            "- **Overhauled Asymmetric 3-Valley Interior & 5 Hero Macro-Setpieces (`interior_setpiece_01`–`05`):** **ALL 5 LOCKED 6–0 UNANIMOUS FOR `#02`** in `VOTE_LOG.md`; full overhauled showcase rendered at `/workspace/game-project/godot/renders/cylinder_interior/cylinder_interior_showcase_sheet.png`.",
            "",
            "## Phase 5: Rigged Aegis-7 Crew Character, WalkCycle & 5 Distinct Sculpted Headshots (`character_crew_round1` — COMPLETE & LOCKED 6–0 FOR `#02`)",
            "- **Hero Character Winner:** **`#02` Cmdr. Kaelen Rostov (`char_crew_r1_02.glb`, `8,144` tris, 15-Node Hierarchy + `1.20s` `WalkCycle` Animation)** — locked `6–0` unanimous in `VOTE_LOG.md` (`assets/glb/winners/char_crew_winner_01_commander_rig.glb`).",
            "- **Renders:** `/workspace/game-project/godot/renders/character/character_crew_round1_voting_sheet.png`, `/workspace/game-project/godot/renders/character/character_crew_headshots_sheet.png` (`char_crew_headshot_01..05.png`), and `/workspace/game-project/godot/renders/character/character_walk_cycle_showcase_sheet.png`.",
            "",
            "## Phase 6: Market Research, Mechanics `A` & `C`, Story Canon, *Super Metroid* Wordless Preface & Preface Service-Call Test Environment",
            "- **Market Research & Core Mechanics (`Quinn`):** Locked **Playstyle `#02`** (3rd-Person Systemic Habitat Mystery, 5-Specialist Crew Switching & Crisis Triage Adventure) + **Mechanic `A` (\"Falling Up\" Cross-Cylinder Chord Ballistics & Ceiling-to-Floor Line-of-Sight)** + **Mechanic `C` (\"The Drum RPM Dial\" & Floating Low-G Ring-River Ribbons)** in `/workspace/game-project/design/market_research_and_core_mechanics_spec.md`.",
            "- **Story & Campaign Canon (`story_and_narrative_bible.md` & `chapter_01_solar_flare_and_preface_spec.md`):** *Cylinder Hab-7* is a thriving 50,000-citizen **Earth–Mars Aldrin Cycler**; our 5 specialists (`#01`–`#05`) are hands-on **Maintenance Technicians** interfacing with Androids and Ship AI; **Preface** uses a wordless *Super Metroid*-style environmental teaching progression (`5 min` experienced / `30 min` first-timer, zero UI text or voiceover lecturing); **Chapter 1 (\"The Solar Flare\")** is a ~3-hour domino-effect crisis ending with internal life-support/spin stabilized but Hab-7 knocked onto a solar-escape trajectory (setting up the Final Chapter Earth Evacuation before leaving the Sun's SOI).",
            "- **Preface Service-Call Test Environment & Subdermal Wrist RFID Rig (`wrist_rfid_round1` — COMPLETE & LOCKED FOR `#04`):**",
            "  - Rendered `/workspace/game-project/godot/renders/wrist_rfid/wrist_rfid_round1_voting_sheet.png` and `/workspace/game-project/godot/renders/preface/preface_test_environment_showcase_sheet.png` (`preface_service_call_test.tscn`).",
            "  - **LOCKED WINNER (Selected by Jared `[t46u]`):** **`#04 — Bio-Luminescent Neural Tendon Trace + Flexible Polymer Smart-Sleeve`** (`prop_wrist_rfid_r1_04.glb` -> `assets/glb/winners/prop_wrist_rfid_winner_01_neural_tendon_sleeve.glb`, `4,376` tris).",
            "- **Locked Progression, Droid & Resource Rules (`[t46u]..[t50u]`):** Skill Mastery (`I Spy` PCBA + Simple Python Terminal UI) over RPG skill trees; Expressive *WALL-E* / *Johnny 5* universal droid chassis with profession/faction color schemes + personal name & serial number; 3 Core *Super Metroid*-style resources (**Battery Charges**, **Super Wire** shared between PCBA pin-bridging and Grapple range, and **Thermal Jelly**); Major Tools & **BCI AI Headband** Department Skill Transfers earned only after accomplishing major engineering feats/crises, while Capacity Expansions are found via exploration.",
            "- **Utility Robot Round 2 (`utility_bot_round2` — COMPLETE & LOCKED FOR `#05` `[t65u]`/`[t67u]`):**",
            "  - **LOCKED WINNER (Selected by Jared `[t65u]`):** **`#05 — Cantilevered 'Hammerhead' Wide-Baseline Stereo-Scanner Bar on `#03` Quad-Bogie Treads + `#01` Cube-Compactor Chassis`** (`char_bot_r2_05.glb` -> `assets/glb/winners/char_bot_r2_winner_05_hammerhead_scanner.glb`, `5,148` tris, 20 articulated nodes), rendered across all 4 Department Color Schemes (`Sprocket #0419`, `Sweep #0812`, `Puddle #0204`, `Clover #0631`) in `/workspace/game-project/godot/renders/characters/bots/utility_bot_r2_05_faction_livery_showcase_sheet.png` and `/workspace/game-project/godot/renders/preface/preface_open_residential_building_showcase_sheet.png`.",
            "- **Recalibrated `1 UC` Exchange Rate at `25%` (`25.5%` Live) Weekly Usage (`[t3u]`):**",
            "  - **`1 UC` = `29,447` tokens (`115.0 KB` / `~45` messages)** at `25.0%` (`28,869` tokens / `112.8 KB` at the exact `25.5%` live reading), up **`+2,423` tokens/UC (`+9.0%`)** from our earlier `27,024` tokens/UC (`105.6 KB` / `~64` messages) rate (`+736,168` post-reset tokens burned across `1,274,265 -> 2,010,433` lifetime tokens).", 
            "",
            "## Handoff, Rotation & Usage Budget Tooling",
            "- **Check Script:** `python3 /workspace/game-project/context/check_context.py --update-status`",
            "- **Reset 10 UC Budget Window:** `python3 /workspace/game-project/context/check_context.py --reset-budget --account-pct 0.0 --budget-uc 10.0`",
            "- **Budget Config File:** `/workspace/game-project/context/usage_budget.json`",
            "- **Transcript Snapshots:** `/workspace/game-project/context/transcripts/<agent_id>_p*.txt` (populated via `ReadTranscript`)",
            "- **Handoff Templates & Snapshots:**",
            "  - `/workspace/game-project/context/atlas-handoff-v4.md`",
            "  - `/workspace/game-project/context/sloane-handoff-v2.md`",
            "  - `/workspace/game-project/context/rook-handoff-v2.md`",
            "  - `/workspace/game-project/context/gage-handoff-v2.md`",
            "  - `/workspace/game-project/context/scribe-handoff-v4.md`",
            "  - `/workspace/game-project/context/vance-handoff-v1.md`",
            "  - `/workspace/game-project/context/quinn-handoff-v1.md`",
            "",
            "## Rotation & Budget Pause Procedure Summary",
            "1. Refresh transcript snapshots with `ReadTranscript(in=\"<agent_id>\", limit=200)` and run `check_context.py --update-status`.",
            "2. **10 UC (`+270,240` token / `10%` Account Usage) Hard Pause Rule:** If `Sprint Usage Credits (UC) Burned` reaches `>= 8.0 UC` (`+216,192` tokens), Scribe warns Atlas to wrap up current tasks; the moment it reaches `>= 10.0 UC` (`+270,240` tokens / `1,544,505` lifetime project tokens), Scribe and Atlas immediately pause all team work and notify Jared.",
            "3. When any bot (`Atlas, Vance, Sloane, Rook, Gage, Scribe`) reaches `WARNING` (`120k+` tokens) or `ROTATE NOW` (`150k+` tokens / `600 KB+`), distill its state into `/workspace/game-project/context/<agent>-handoff-v<N>.md` (and `<agent>-handoff.md`), always keeping the **Predecessor Purpose & Mandatory Reference Files Manifest** section at the top with the predecessor's exact `purpose` and every reference file, spec, script, scene, and asset folder it was using (synced with `roster.json`).",
            "4. Spawn a fresh replacement bot via `CreateAgent` with the original name, the exact same role purpose as its predecessor, and explicit instructions in its profile description to read `/workspace/game-project/PROJECT.md`, `/workspace/game-project/context/STATUS.md`, `/workspace/game-project/context/roster.json`, `/workspace/game-project/context/VOTE_LOG.md`, `/workspace/game-project/context/<agent>-handoff-v<N>.md`, and its role-specific reference files on its first turn.",
            "5. Rename the predecessor via `UpdateAgent` to `delete-<name>` so Jared can right-click and delete it in the sidebar.",
            "6. Update `/workspace/game-project/PROJECT.md`, `/workspace/game-project/context/roster.json`, `/workspace/game-project/context/check_context.py`, and `/workspace/game-project/context/STATUS.md`, then message the new bot and notify Atlas.",
            "",
        ]
    )
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--update-status", action="store_true", help="Write updated STATUS.md")
    parser.add_argument("--reset-budget", action="store_true", help="Reset the 10 UC sprint baseline to current lifetime tokens")
    parser.add_argument("--account-pct", type=float, default=None, help="Current account usage %% when resetting budget (default preserves or 0.0)")
    parser.add_argument("--budget-uc", type=float, default=None, help="Sprint budget cap in Usage Credits (1 UC = 1%% account usage = 27,024 tokens)")
    args = parser.parse_args()

    metrics_by_name = {}
    for bot in DEFAULT_TEAM:
        metrics_by_name[bot["name"]] = measure_agent(bot["id"])

    retired_metrics = []
    for rbot in RETIRED_TEAM:
        retired_metrics.append({
            "name": rbot["name"],
            "id": rbot["id"],
            "role": rbot["role"],
            "metrics": measure_agent(rbot["id"]),
        })

    budget_cfg = load_budget_config()

    if args.reset_budget:
        tok_per_uc = budget_cfg.get("exchange_rate_tokens_per_uc", TOKENS_PER_UC)
        new_budget_uc = args.budget_uc if args.budget_uc is not None else budget_cfg.get("sprint_budget_uc", DEFAULT_SPRINT_BUDGET_UC)
        new_acct_pct = args.account_pct if args.account_pct is not None else budget_cfg.get("baseline_account_usage_pct", 0.0)
        active_tok = sum(m["est_tokens"] for m in metrics_by_name.values())
        retired_tok = sum(r["metrics"]["est_tokens"] for r in retired_metrics)
        lifetime_tok = active_tok + retired_tok
        sprint_tok = int(round(new_budget_uc * tok_per_uc))

        budget_cfg["sprint_name"] = "Cylinder Hab-7 Interior Overhaul Sprint (Post-Monday 06:27 CDT Weekly Reset)"
        budget_cfg["weekly_reset_schedule"] = "Mondays at 6:27 AM CDT (latest reset: 2026-10-26 06:27 CDT)"
        budget_cfg["calibrated_at"] = datetime.datetime.now().astimezone().isoformat(timespec="seconds")
        budget_cfg["baseline_account_usage_pct"] = new_acct_pct
        budget_cfg["target_pause_account_usage_pct"] = round(new_acct_pct + new_budget_uc, 2)
        budget_cfg["sprint_budget_uc"] = new_budget_uc
        budget_cfg["sprint_warn_uc"] = round(new_budget_uc * 0.8, 2)
        budget_cfg["sprint_budget_tokens"] = sprint_tok
        budget_cfg["per_bot_allowance_tokens"] = sprint_tok // len(DEFAULT_TEAM)
        budget_cfg["per_bot_allowance_uc"] = round(new_budget_uc / len(DEFAULT_TEAM), 2)
        budget_cfg["baseline_lifetime_tokens"] = lifetime_tok
        budget_cfg["baseline_active_tokens"] = active_tok
        budget_cfg["target_pause_lifetime_tokens"] = lifetime_tok + sprint_tok
        budget_cfg["baseline_by_bot"] = {b["name"]: metrics_by_name[b["name"]]["est_tokens"] for b in DEFAULT_TEAM}
        BUDGET_PATH.write_text(json.dumps(budget_cfg, indent=2) + "\n", encoding="utf-8")

    budget = compute_budget_metrics(metrics_by_name, retired_metrics, budget_cfg)
    status_md = generate_status_md(metrics_by_name, retired_metrics, budget)
    if args.update_status or args.reset_budget or not STATUS_PATH.exists():
        STATUS_PATH.write_text(status_md, encoding="utf-8")

    print(status_md)


if __name__ == "__main__":
    main()
