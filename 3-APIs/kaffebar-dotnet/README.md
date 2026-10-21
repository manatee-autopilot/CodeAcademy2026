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
