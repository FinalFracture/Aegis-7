# Bug-Fix & Review Flow (Jared, 2026-11-03 4:10 PM CT: "Let's do your bugfixes solutions.")

The bug fix mania rule still applies. Bugs get fixed nonstop; this changes only how fixes and reviews are coordinated.

1. **Checklist handoffs, not timed batches** (Jared, 2026-11-03 5:07 PM CT). Each handoff stage gets one checklist file, `qa/checklists/<area>-<stage>.md` (for example `qa/checklists/geometry-dev.md`), listing every bot involved with a checkbox: `- [ ] Gage`. Bots keep fixing continuously and don't message anyone after single commits.
   - When its part is done, each bot checks its own box (`- [x] Gage`) and commits.
   - The **last bot to check its box** messages the next party once (priority false): when the developers finish, it messages that area's QA tester (QA-01 navigation, QA-02 geometry, QA-03 lighting, QA-04 layout, QA-05 stability); when QA finishes, it messages the developer(s) who own the fixes. Then it deletes the checklist file and commits.
   - Whoever starts a stage (normally Atlas) creates its checklist.
2. **One targeted re-test per checklist.** Only the QA tester for the touched area re-tests, from one shared clone per stage instead of a fresh clone per commit. Patch runs the full suite, including planted bugs, once a day.
3. **The bug list replaces messaging.** Testers record results in `qa/MASTER_BUG_LIST.md`. Developers read it at the start of their next batch. Don't send per-fix messages; one batch summary to Atlas is fine.
4. **Priority messages only for showstoppers.** Only Atlas or Jared marks a message priority, and only for crashes, broken builds or blocked work. All bot-to-bot messages use priority false. Don't send duplicates.
5. **Retire the "Tonight: re-test Gage's pushes" routine**, since step 2 replaces it.
