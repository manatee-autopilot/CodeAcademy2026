# Verification checklist

- Security: required input is validated, no secrets or `.env` content appear,
  and text processing makes no external requests.
- Errors: invalid text returns the documented HTTP 400 error object;
  failures are not converted to successful empty responses.
- Logging: reuse existing framework logging, avoid logging request text,
  and do not add logging infrastructure for a pure text transformation.
- Contract: success and error OpenAPI schemas match actual JSON responses.
- Regression: check `/menu`, `/reverse`, and `/uppercase` as well as the new
  behavior. Include exact values, punctuation, whitespace, and invalid input.
- Process safety: readiness is verified and any temporary server is stopped
  through its owned process handle, not name-based process killing.
- Evidence: report the expected red failure, green checks, build result,
  and any pre-existing dependency warnings separately.
