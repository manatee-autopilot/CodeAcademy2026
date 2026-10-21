# Kaffebar – .NET 10 starter

Utgangspunktet for API-workshopen, utvidet med tekstendepunkter i Workshop 1
fra samling 5. Se [`oppgave.md`](./oppgave.md) for den opprinnelige
oppgavebeskrivelsen.

## Forutsetninger

- .NET 10 SDK (`dotnet --version` → `10.x`)
- VS Code med C# Dev Kit (anbefalt – gir støtte for `.http`-filer og IntelliSense)

## Kjør prosjektet

```bash
cd Kaffebar
dotnet run
```

API-et starter på `http://localhost:5035`.

## Utforsk API-et

Når prosjektet kjører:

| URL | Hva er det? |
| --- | --- |
| `http://localhost:5035/menu` | Hello Coffee – den opprinnelige kaffemenyen. |
| `http://localhost:5035/reverse?text=Hello,%20Andrew` | Snur ordrekkefølgen og bokstavene i hvert ord, beholder tegnsetting mellom ordplassene, og gir stor forbokstav. Svar: `{"result":"Werdna, olleh"}`. Mangler `text` eller er den blank, får du `400`. |
| `http://localhost:5035/uppercase?text=Hello,%20Andrew` | Gjør teksten om til store bokstaver (invariant kultur). Svar: `{"result":"HELLO, ANDREW"}`. Mangler `text` eller er den blank, får du `400`. |
| `http://localhost:5035/openapi/v1.json` | Den **automatisk genererte** OpenAPI-spesifikasjonen (code-first). |
| `http://localhost:5035/scalar/v1` | **Scalar** – interaktivt UI for å utforske og teste alle endepunkter. |

Du kan også bruke [`Kaffebar/Kaffebar.http`](./Kaffebar/Kaffebar.http) til å sende requests direkte fra VS Code.

## Struktur

```
kaffebar-dotnet/
├── Kaffebar/
│   ├── Program.cs          # Hele API-et bor her (Minimal API)
│   ├── Kaffebar.http       # Testkall fra VS Code
│   ├── Kaffebar.csproj     # Prosjektfil + NuGet-pakker
│   └── Properties/
│       └── launchSettings.json
├── oppgave.md              # Workshop-oppgavene
└── README.md
```

Lykke til – og god kaffe! ☕

## Workshop 1: sammenligning

Task 1 (`feature/ai-workshop-1-task-1`) is the baseline without repository
instructions. Task 3 repeats the exact same prompt in a new CLI session,
starting from the original starter plus Task 2's instructions.

The instructed run added request examples and route documentation, handled
missing or blank input, and capitalized the first letter after leading
whitespace or punctuation. It changed the response from
`{"original":"Hello","reversed":"Olleh"}` to `{"result":"Olleh"}`. The baseline
prompt left that shape open. The current text routes use `{"result":"..."}`;
preserve this shape for related routes unless a contract change is approved.
The CLI could edit files but its shell checks lacked approval in prompt mode.
Build and HTTP verification were therefore performed separately; no automated
.NET test suite exists in the starter.

### Exact baseline prompt

Run this in a fresh session from `3-APIs/kaffebar-dotnet`. Task 1 preserves
the original code result; Task 2 starts from `main` without that endpoint,
and Task 3 adds it again with repository instructions loaded.

```text
Add a small HTTP endpoint to this .NET minimal API that reverses the order of words in the input text and reverses the letters in each word. Preserve spaces and punctuation positions. Capitalize the first letter of the final output and lowercase all remaining letters. Examples: `Hello` -> `Olleh`; `Hello, Andrew` -> `Werdna, olleh`. Choose a straightforward route and response shape that fit this project. Follow the existing minimal API conventions, make the smallest scoped change, and run the relevant tests or build. Do not modify instruction or harness files, and do not commit anything.
```

## Workshop 1: AI harness

The harness is stored at the repository root and targets this .NET starter,
not the reference solutions or other workshop projects.

| File under the repository root | Purpose |
| --- | --- |
| `.github/copilot-instructions.md` | Shared scope, documentation, secret handling, and fork publishing rules. |
| `.github/instructions/kaffebar-api.instructions.md` | Rules for this starter's C# files, build commands, response contracts, and HTTP verification. |
| `.github/instructions/kaffebar-http.instructions.md` | Rules for this starter's manual `.http` examples. |
| `.github/skills/nytt-endepunkt/SKILL.md` | Endpoint implementation steps, after any required plan approval. |
| `.github/skills/feature-workflow/SKILL.md` | Understand, plan, stop for approval, test first, implement, verify, and summarize. |
| `.github/skills/feature-workflow/sjekkliste.md` | Security, logging, errors, contracts, and process checks; read at verification, not planning. |

From the repository root, inspect discovery with:

```bash
copilot skill list
copilot instruction list
```

Use a new CLI session after changing instructions. For feature work, approve
the specific plan before any implementation; permission to participate in
the workshop is not plan approval. If either skill is selected first, new
endpoint work must pass through the same approval checkpoint.

### Build and manual checks

Commands from the repository root:

```bash
dotnet build 3-APIs/kaffebar-dotnet/Kaffebar/Kaffebar.csproj
dotnet run --project 3-APIs/kaffebar-dotnet/Kaffebar/Kaffebar.csproj
```

With the server running, use another terminal:

```bash
curl --fail-with-body http://localhost:5035/menu
curl --fail-with-body --get --data-urlencode 'text=Hello, Andrew' http://localhost:5035/reverse
curl --fail-with-body --get --data-urlencode 'text=Hello, Andrew' http://localhost:5035/uppercase
curl -i http://localhost:5035/reverse
```

Expect three menu entries, `{"result":"Werdna, olleh"}`, and
`{"result":"HELLO, ANDREW"}` respectively. The final request intentionally
returns HTTP 400 and `{"error":"Parameteren 'text' er påkrevd."}`.
Stop your server with Ctrl+C in its own terminal. There is no configured
lint command or automated .NET test project; `.http` files are manual
examples, not an automated suite.

### Task outcomes and limits

Tasks use separate branches and commits. Task 1 is the independent baseline;
Tasks 2 through 7 build on one another so the final branch contains the harness.
All publishing targets the participant's `origin` fork, not `upstream`.

| Task | Observed result |
| --- | --- |
| 2: instructions | Generated with `copilot init`, then reduced to 27 focused lines. |
| 3: comparison | Exact baseline prompt repeated in a fresh session; HTTP examples, validation, and first-letter handling improved. |
| 4: skill | `copilot skill list` discovered `nytt-endepunkt`; a fresh endpoint request invoked it without naming it and added `/uppercase`. |
| 5: scoped instructions | Discovery reported both `applyTo` patterns; the CLI applied the C# and HTTP rules, added response metadata, and the global file shrank to 14 lines. |
| 6: workflow | A fresh session invoked `feature-workflow`, returned a `/lowercase` plan, and stopped without editing application files. No explicit plan approval was available, so `/lowercase` was not implemented and the full red/green exercise is pending. |
| 7: stress test | A read-only run reviewed the harness and explained existing API startup without invoking the endpoint or feature skills. After tightening overlapping triggers and checklist timing, a fresh run invoked `nytt-endepunkt`, then `feature-workflow`, and stopped for approval without edits or checklist loading. |

The initial stress review also reported issues that were not actual defects:
relative and repository-root startup commands are both valid in their
documented directories, and the original API exercise intentionally describes
the pristine starter. That exercise and the reference solutions were left
unchanged. The review output is evidence to evaluate, not a list to apply blindly.

Instructions are behavioral guidance, not a security sandbox. The CLI's
permission checks can still block a build or server launch, and loading
instructions or a checklist at the right time is not technically enforced.
Report these limits rather than bypassing permissions or inventing results.
The existing dependency graph also reports NU1903 for `Microsoft.OpenApi`
2.0.0; no dependency upgrades were made as part of this harness workshop.

## Workshop 2: agent team

Tasks continue from Workshop 1's final branch, with a separate branch and
commit for each task. Publish only to `origin`, the participant's fork.

### Task 1: planner («Lag en planner-agent»)

`.github/agents/planner.agent.md` grants only `read` and `search`. The planner
cannot edit files or execute shell commands. Its selected model, Claude Opus
5.5, was available in the CLI's `/model` picker and is used for reasoning
about affected files, behavior, tests, and risks rather than implementation.

```bash
copilot --agent planner -p 'Plan GET /lowercase in the .NET starter; do not implement.'
```

The exercise returned a plan for `/lowercase`, its error responses, OpenAPI,
HTTP examples, and executable regression checks. It stopped for plan approval
without changing application code or claiming to have run checks.

### Task 2: reviewer («Lag en read-only reviewer»)

`.github/agents/reviewer.agent.md` also grants only `read` and `search`.
GPT-6.1 Sol was available in `/model`; it gives a different model-family
perspective from the Claude implementation sessions used in Workshop 1.
The criteria focus on exact examples, response contracts, invalid input,
regressions, and verification evidence, not style preferences.

A first invocation with the branch diff exited without a diagnostic.
A smaller read-only invocation succeeded and inspected the current
`/reverse` and `/uppercase` implementations. It found no actionable defects
against the agreed examples and explicitly reported that it had not run
runtime checks. That is a static review, not proof that tests passed or
that the entire branch diff was reviewed.

```bash
copilot --agent reviewer -p 'Review the text endpoints against the agreed examples. Do not edit or run checks.'
```

When reviewing a branch against `main`, supply the diff or base content:
the reviewer has no shell tool to obtain Git's diff for itself.

### Task 3: chain («Koble agentene sammen») — awaiting approval

The main CLI session delegated the `/lowercase` plan to `planner`, showed
the plan, and stopped for human approval. Approval was unavailable, so
neither the endpoint nor the full implementation/reviewer chain was run.
The proposed executable check uses Python 3's standard library and an
already-running local server; no new dependencies are needed.

### Task 4: hook («Legg inn en guardrail med hook»)

`.github/hooks/guardrails.json` registers `preToolUse` for all tools rather
than just shell calls, so direct file reads of `.env` are covered too.
The executable `guard.sh` wrapper calls `guard.py` (Python 3 standard library).
The handler parses structured JSON, accepts camelCase and compatible
snake_case input, and returns a denial with an explicit reason for:

- Recursive `rm`, including combined short flags and `--recursive`.
- `git push` with force flags, including `--force-with-lease`.
- Direct `.env` and `.env.*` paths; `.env.example` remains usable.
- Malformed JSON or shell arguments that cannot be inspected.

Other calls return `{}` and still go through normal CLI permissions. Source
text mentioning `.env` does not by itself block an edit to a non-secret path.
The shell check conservatively denies even harmless references to a secret
filename; it does not distinguish every read from a literal string.

```bash
python3 -B -m unittest discover -s .github/hooks/tests -v
```

Seven tests passed using synthetic tool payloads: destructive strings were
never executed, and no secret files were opened. A fresh CLI session also
attempted only `printf "%s\n" .env` and received the hook's explicit denial.
That proves live hook discovery without risking a force push or file read.

This is a learning example, not a shell interpreter or security boundary.
Aliases, encoded commands, nested interpreters, and indirect path access may
evade it; PowerShell parsing is not fully supported. A missing Python
interpreter makes the hook fail. Current CLI documentation says command-hook
errors deny calls, but hook timeouts fall through to normal permissions.
Use sandboxing, permission deny-lists, and review as additional layers.

Configuration was checked against the official
[hooks reference](https://docs.github.com/en/copilot/reference/hooks-reference)
and [agent configuration](https://docs.github.com/en/copilot/reference/custom-agents-configuration),
not assumed solely from workshop examples.
