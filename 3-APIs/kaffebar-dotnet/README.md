# Kaffebar – .NET 10 starter

Utgangspunktet for workshopen. Se [`oppgave.md`](./oppgave.md) for oppgavebeskrivelsen.

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
| `http://localhost:5035/reverse?text=Hello, Andrew` | Snur ordrekkefølgen og bokstavene i hvert ord, beholder tegnsetting, og gir stor forbokstav. Svar: `{"result":"Werdna, olleh"}`. Mangler `text`, får du `400`. |
| `http://localhost:5035/uppercase?text=Hello, Andrew` | Gjør teksten om til store bokstaver (invariant kultur). Svar: `{"result":"HELLO, ANDREW"}`. Mangler `text` eller er den blank, får du `400`. |
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
`{"original":"Hello","reversed":"Olleh"}` to `{"result":"Olleh"}`; the prompt
left that shape open, so this is a comparison result, not a guaranteed contract.
The CLI could edit files but its shell checks lacked approval in prompt mode.
Build and HTTP verification were therefore performed separately; no automated
.NET test suite exists in the starter.
