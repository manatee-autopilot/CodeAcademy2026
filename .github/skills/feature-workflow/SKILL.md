---
name: feature-workflow
description: Plan and implement a new feature or behavior change in the .NET Kaffebar starter at 3-APIs/kaffebar-dotnet, with human plan approval, test-first implementation, and verification. Use for feature requests in that starter, including new HTTP endpoints. Not for documentation-only edits or other workshop projects.
---

# Feature workflow

1. **Understand:** read relevant code and applicable instructions. Resolve
   conflicting examples or unclear behavior before choosing an implementation.
2. **Plan and STOP:** list affected files, behavior, failing test cases, and
   verification commands. Ask the user to approve this specific plan. Do not
   write tests, edit application code, or run mutating commands before approval.
   Earlier permission to work on the workshop is not approval of this plan.
   If no interactive answer is available, return the plan and stop.
3. **Test first:** after approval, add an executable regression check for the
   required behavior. Run it against the old behavior and observe the intended
   failure. A connection error, missing dependency, or failed build is not a
   valid red test. Use existing tooling; ask before adding dependencies.
4. **Implement:** make the smallest change that turns the failing check green.
   For new endpoints, use the `nytt-endepunkt` skill. Do not re-enter planning
   when using that implementation skill after this plan has been approved.
5. **Verify:** run relevant tests and the explicit project build command.
   Run a configured lint command if one exists; otherwise say there is none.
   Check the existing endpoints too. Read [the checklist](sjekkliste.md) now,
   rather than loading it into every planning request.
6. **Summarize:** report the change, red/green evidence, checks actually run,
   remaining warnings, and what a reviewer should inspect. Keep task changes
   in their own commit and task branch. Do not claim a push succeeded without
   its success output; publish only to the participant's `origin` fork.
