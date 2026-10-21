---
name: nytt-endepunkt
description: Add or change an HTTP endpoint in the C#/.NET Kaffebar starter at 3-APIs/kaffebar-dotnet. Use when a request asks for a new route, endpoint, query parameter, or endpoint validation in that starter; not for Java or reference solutions.
---

# Starter API endpoint

1. Read the repository instructions, the starter's `Kaffebar/Program.cs`,
   `Kaffebar/Kaffebar.http`, and README. Identify the requested method, route,
   request, response, and invalid-input behavior. Ask if examples conflict.
2. Follow the existing Minimal API style and record DTOs. Do not copy the
   `-solution` application or change unrelated endpoints. Reuse existing
   response shapes for related operations unless a change is requested.
3. Reject missing or blank required text with HTTP 400 and an explicit error,
   matching `/reverse`. Keep Norwegian summaries and descriptions.
4. Implement only the requested behavior. Keep pure text operations local;
   no translation services, network calls, or new packages are needed.
5. Add valid and invalid requests to `Kaffebar/Kaffebar.http` and describe the
   route and response shape in `3-APIs/kaffebar-dotnet/README.md`.
6. From the repository root, build with
   `dotnet build 3-APIs/kaffebar-dotnet/Kaffebar/Kaffebar.csproj`.
   Start a temporary local API on an unused loopback port, check readiness,
   and exercise exact output values, invalid input, and the existing `/menu`.
   Stop only the process you started. Use managed process tools or a numeric
   PID, not name-based kills or command substitutions in `kill`.
7. Run relevant automated tests if present; otherwise explicitly report that
   there is no test project and distinguish HTTP checks from a test suite.
   Report permission failures instead of claiming checks ran.
