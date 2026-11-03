# Self-Rotation Rule (Jared, 2026-11-03)

Every bot keeps this rule and passes it on to its successor word for word.

1. At **500 messages** in your own conversation, do a memory transfer before you take on new work.
2. Write `context/<name>-handoff-v<N>.md` and a mirror `<name>-handoff.md`. Keep the **Predecessor Purpose & Mandatory Reference Files Manifest** at the top, followed by current state, open tasks and standing rules.
3. Create the replacement bot with CreateAgent. Give it the same name and the same purpose, and tell it to read the handoff first. Its description must include this rule: "At 500 messages, self-rotate per context/ROTATION_RULE.md."
4. Rename yourself to `delete-<name>` with UpdateAgent.
5. Update your entry in `roster.json`: the new id, `previous_id`, and the handoff file. Commit only those files to main, push, and leave `git status` clean.
6. Send Atlas the new id with priority false. Scribe audits this and doesn't do it for you.
