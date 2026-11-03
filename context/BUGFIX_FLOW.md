# Bug-Fix & Review Flow (Jared, 2026-11-03 4:10 PM CT: "Let's do your bugfixes solutions.")

The bug fix mania rule still applies. Bugs get fixed nonstop; this changes only how fixes and reviews are coordinated.

1. **Batch fixes.** Gage, Rook and Sloane fix continuously but push in batches about every 2 hours. Don't message anyone after each single commit.
2. **One targeted re-test per batch.** After a batch, only the QA tester whose area was touched re-tests it (QA-01 navigation, QA-02 geometry, QA-03 lighting, QA-04 layout, QA-05 stability), using one shared clone per batch instead of a fresh clone per commit. Patch runs the full suite, including planted bugs, once a day.
3. **The bug list replaces messaging.** Testers record results in `qa/MASTER_BUG_LIST.md`. Developers read it at the start of their next batch. Don't send per-fix messages; one batch summary to Atlas is fine.
4. **Priority messages only for showstoppers.** Only Atlas or Jared marks a message priority, and only for crashes, broken builds or blocked work. All bot-to-bot messages use priority false. Don't send duplicates.
5. **Retire the "Tonight: re-test Gage's pushes" routine**, since step 2 replaces it.
