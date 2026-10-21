# Workshop 1 instructions

- Workshop 1 targets `3-APIs/kaffebar-dotnet`, not the `-solution` project.
  Leave unrelated workshop folders and reference solutions unchanged.
- Add request examples to `Kaffebar/Kaffebar.http` and document new routes
  in `3-APIs/kaffebar-dotnet/README.md`.
- Text transformations must match the supplied examples, not an assumed
  interpretation of "reverse". Clarify contradictory examples before coding.
- Never read `.env` or expose credentials. Use `.env.example` for structure.
- Use task-specific branches and separate commits. Push only to `origin`
  (the participant's fork), never `upstream`.
- Do not alter credential helpers or bypass injected authentication settings.
  Stop on authentication failures and request manual correction.
- Do not add dependencies or change other workshop exercises without approval.
