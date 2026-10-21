# Workshop 1 instructions

- Workshop 1 targets `3-APIs/kaffebar-dotnet`, not the `-solution` project.
  Leave unrelated workshop folders and reference solutions unchanged.
- Commands below run from the repository root. Do not run `dotnet build`
  without a project path: there is no root .NET solution.
- Build: `dotnet build 3-APIs/kaffebar-dotnet/Kaffebar/Kaffebar.csproj`.
- Run: `dotnet run --project 3-APIs/kaffebar-dotnet/Kaffebar/Kaffebar.csproj`.
- The starter has no automated test project or configured lint command.
  Do not describe a successful build as passing tests.
- Verify new endpoints over HTTP against the exact requested examples and
  at least one invalid-input case. Report what was actually checked.
- Preserve `GET /menu` and the Development-only OpenAPI and Scalar routes.
- Use the starter's Minimal API style and record DTOs for small endpoints.
  Keep Norwegian endpoint summaries and descriptions consistent with `/menu`.
- Add request examples to `Kaffebar/Kaffebar.http` and document new routes
  in `3-APIs/kaffebar-dotnet/README.md`.
- Text transformations must match the supplied examples, not an assumed
  interpretation of "reverse". Clarify contradictory examples before coding.
- For text capitalization, distinguish the first letter from character zero;
  exercise leading whitespace or punctuation when applicable.
- Never read `.env` or expose credentials. Use `.env.example` for structure.
- Use task-specific branches and separate commits. Push only to `origin`
  (the participant's fork), never `upstream`.
- Do not alter credential helpers or bypass injected authentication settings.
  Stop on authentication failures and request manual correction.
- Do not add dependencies or change other workshop exercises without approval.
