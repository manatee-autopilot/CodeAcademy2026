---
name: kvalitetsloop
description: Run a bounded implementer-reviewer quality loop for an explicitly approved Kaffebar feature or an explicitly scoped workshop harness exercise. Fix acceptance blockers and stop after at most three review rounds.
---

# Bounded quality loop

1. Require an approved feature plan, or an explicit harness exercise with
   permitted files and acceptance criteria. Do not use this skill to grant
   approval for application changes. Preserve all ordinary tool permissions.
2. Delegate the first implementation to `implementer`, with that scope and
   criteria. For an existing seeded exercise, give it the known initial
   files and the observed failing check rather than inventing a new defect.
3. Set the review counter to zero. Before each `reviewer` invocation, if the
   counter is already three, STOP. Otherwise increment it, then review.
   Every review attempt, including an error or incomplete result, consumes
   a round. Never reset the counter or nest another loop.
4. Give `reviewer` the exact criteria, changed file contents, and caller's
   actual check results or diff. It is read-only and cannot run checks.
   Classify BLOCKER findings as the workshop's red findings.
5. If no blockers remain, stop successfully only after the executable checks
   pass. Missing evidence, review errors, or blocked tools are not a clean
   review; report them and stop for help instead of declaring success.
6. If blockers remain and fewer than three reviews have run, delegate only
   the scoped repairs to `implementer`, rerun the checks, and return to step 3.
7. If review three still has blockers, do not launch another repair or review.
   Stop, list remaining findings and checks, and ask a human to decide.
8. Report the actual agents, review count, repair count, outcomes, and
   remaining limitations. No Git operations or dependency changes in workers.
