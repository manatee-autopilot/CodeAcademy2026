---
applyTo: '3-APIs/kaffebar-dotnet/Kaffebar/*.http'
---

# Starter HTTP checks

- Keep `@host` configurable and separate requests with `###`.
- Use Norwegian request labels. Add expected HTTP status and JSON as comments
  for new cases; never put explanatory text in the HTTP request itself.
- Encode whitespace and query delimiters in parameter values.
- Cover an exact successful example and missing, empty, and whitespace-only
  required input. For capitalization, also cover leading punctuation.
- Keep `/menu` checks so adding text endpoints does not hide regressions.
- A `.http` file is a set of manual requests, not an automated test suite.
  Run the requests before claiming they pass and report permission failures.
