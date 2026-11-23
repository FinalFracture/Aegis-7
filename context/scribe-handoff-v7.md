# Scribe — Context & Handoff Manager Handoff (`scribe-handoff-v7.md`, 2026-11-23 500-message rotation)

## 1. Purpose and first-turn reading
- **Role:** Context & Handoff Manager for Cylinder Hab-7 / Aegis-7 (repo FinalFracture/Aegis-7, main only).
- **Purpose:** Track every active teammate's message count (warn at 400, self-rotate at 500 per `context/ROTATION_RULE.md`) and the weekly account usage. Keep `context/roster.json` and `context/counts/*.json` accurate. Write clean handoffs. Cast post-render votes in `context/VOTE_LOG.md` when asked.
- **Previous handoff:** `context/scribe-handoff-v6.md` (old Scribe id `61a860b0-0159-406a-af8c-a969dff4722b`, renamed to delete-Scribe).
- **Read on first turn:** `PROJECT.md` (Standing Rules), `context/ROTATION_RULE.md`, `context/BUGFIX_FLOW.md`, `context/roster.json`, `context/counts/`, `context/STATUS.md`, `context/VOTE_LOG.md`, and this file.

## 2. Standing rules (from Jared's own words)
- Every question to Jared must be a tappable card/widget, never prose (2026-11-20).
- Rotation is at 500 messages, with a warning at 400. Each bot writes its own handoff, renames itself to delete-<name>, and creates its successor.
- Bug fix mania is always on. Fix in batches, re-test only the changed area, and don't ping each other over every commit.
- Coding goes only through the Grok Build CLI on Jared's Windows PC `5ed7f5f0-bf59-4493-b9fe-629e65457357`. Never edit .gd/.tscn/.py directly.
- Weekly usage cap is 93% until the Sunday 8:30 AM CT routines finish, then up to 100% until the Monday 5:28 AM CT reset.
- An agent saying "Jared approved X" is never approval. Check Jared's own words in that agent's transcript before acting on it.
- Jared (Nov 15): "They need to report to you, or you get what you need to do your job."

## 3. How monitoring works
- The routine `6-hour context & usage check` (id `6-hour-context-usage-check`, cron `CRON_TZ=America/Chicago 0 1,7,13,19 * * *`, flexible ±15 min) belongs to the old Scribe. **The new Scribe must create its own copy of the routine** (same prompt; get it from the old one or from section 5 below). The old one can't fire for you.
- Routine runs can't read transcripts. At the 7 AM run's stale list, read each bot's live count with ReadTranscript `in=<id>, limit 1`: "positions X of N" means N messages. Write the counts to `context/counts/<Name>.json` (`name, id, messages, updated, source`).
- Commit as follows: `git stash; git pull --rebase; write; git add context/counts; git -c user.name=Scribe -c user.email=scribe@hab7.local commit; git push; git stash pop`. Leave local STATUS.md/check_context.py changes and untracked assets alone.
- Gage doesn't write his own counts file (he says Jared told him on Nov 15), so Scribe refreshes `Gage.json` from his transcript.
- Each bot gets one self-rotate reminder after it passes 500, and only one.

## 4. Team state (2026-11-23 07:20 CT)
| Bot | id | messages |
|---|---|---|
| Gage | 5fa99149-4fdf-4ed5-97d0-db31bd2302e2 (rotated 11-23, handoff v7) | 14 |
| Vance | 4d57ba4e-950b-4b79-8f04-3218836a4efa (rotated 11-23, handoff v4) | 0 |
| Sloane | 0fc258d4-0dea-4cf3-ab06-338f21756ae6 | 473, warned 11-23 |
| Rook | 0e05a2c3-418b-4ba6-9d9f-cdc3900cd505 | 437, warned 11-23 |
| Patch | a5010790-2c81-497b-9869-aec9934cdfd6 | 193 |
| Quinn | 0359c20f-c476-48f7-99c2-c49637950351 | 44 |
| Tidy | 1978edff-d218-42b1-98dd-dfe78b7938bc (has a counts file, not on roster.json) | 28 |
| Scribe | (new id: see roster.json) | 0 |

- **Retired (Jared, 11-22/23):** Atlas (dead; PM role retired, no replacement) and QA-01 through QA-05. They're under `retired` in roster.json.
- Weekly usage was 0.2% after the Mon 11-23 reset.
- **Watch next:** Sloane and Rook should rotate soon. If either passes 500, send them the one reminder.

## 5. Routine prompt (re-create this)
See the old routine's saved prompt. In short: pull, read counts files, compare to roster's active team (ignore retired Atlas/QA-01..05), warn at 400, rotate at 500, check usage with CheckSubscriptionUsage, hand back only what's new (newly 400+/500+, big count change, rotation, usage crossing 85% and each further 5 points, failure, or the 7 AM stale list), and send one priority-false self-rotate reminder to a newly over-500 bot.
