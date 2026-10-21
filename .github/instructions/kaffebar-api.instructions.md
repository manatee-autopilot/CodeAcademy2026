---
applyTo: '3-APIs/kaffebar-dotnet/Kaffebar/**/*.cs'
---

# Starter C# API

- Preserve `GET /menu` and the Development-only OpenAPI and Scalar routes.
- Use Minimal APIs and record DTOs for these small endpoints, with Norwegian
  summaries and descriptions consistent with `/menu`.
- Preserve `{"result":"..."}` for the related text endpoints. Missing or blank
  required text returns HTTP 400 and an explicit error.
- Declare success and error response metadata so the generated OpenAPI
  describes the actual responses.
- Capitalize the first letter, not necessarily character zero. Check leading
  whitespace and punctuation.
- Commands run from the repository root; there is no root .NET solution.
- Build: `dotnet build 3-APIs/kaffebar-dotnet/Kaffebar/Kaffebar.csproj`.
- Run: `dotnet run --project 3-APIs/kaffebar-dotnet/Kaffebar/Kaffebar.csproj`.
- The starter has no automated .NET test project or configured lint command.
  A successful build is not passing tests.
- Verify exact HTTP outputs, invalid input, and `/menu`. Check readiness first,
  and stop only the server process you started using managed process tools.
