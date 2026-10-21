using System.Text.RegularExpressions;
using Scalar.AspNetCore;

var builder = WebApplication.CreateBuilder(args);

// Registrer OpenAPI-tjenestene. Disse genererer spesifikasjonen
// automatisk basert på endepunktene og typene i prosjektet (code-first).
builder.Services.AddOpenApi();

var app = builder.Build();

if (app.Environment.IsDevelopment())
{
    // Eksponerer den genererte spesifikasjonen på /openapi/v1.json
    app.MapOpenApi();

    // Scalar gir et moderne, interaktivt UI på /scalar/v1
    // for å utforske og teste API-et.
    app.MapScalarApiReference();
}

// --- Hello Coffee --------------------------------------------------------
// Et minimal API-endepunkt som returnerer en hardkodet kaffemeny.
// Dette er utgangspunktet for workshopen. Bygg videre herfra!
app.MapGet("/menu", () => new[]
{
    new Coffee(Guid.NewGuid(), "Kaffe Latte", 48.50m),
    new Coffee(Guid.NewGuid(), "Cappuccino", 45.00m),
    new Coffee(Guid.NewGuid(), "Espresso", 35.00m)
})
.WithName("GetMenu")
.WithSummary("Hent kaffemeny")
.WithDescription("Returnerer en liste over alle tilgjengelige kaffedrikker i kaffebaren.");

// --- Reverse -------------------------------------------------------------
// Snur rekkefølgen på ordene og bokstavene i hvert ord. Mellomrom og tegnsetting
// beholder posisjonen sin. Resultatet får stor forbokstav og resten små bokstaver.
app.MapGet("/reverse", (string text) => new ReverseResult(text, ReverseText(text)))
.WithName("ReverseText")
.WithSummary("Snu tekst")
.WithDescription("Snur ordrekkefølgen og bokstavene i hvert ord. Eksempel: 'Hello, Andrew' gir 'Werdna, olleh'.");

app.Run();

static string ReverseText(string text)
{
    var words = Regex.Matches(text, @"\w+").Select(m => m.Value).Reverse().ToArray();
    var i = 0;
    var result = Regex.Replace(text, @"\w+", _ => new string(words[i++].Reverse().ToArray())).ToLowerInvariant();
    return result.Length == 0 ? result : char.ToUpperInvariant(result[0]) + result[1..];
}

// DTO-er kan ligge i Program.cs når prosjektet er lite.
// Etter hvert er det ryddig å flytte dem til egne filer i en Models-mappe.
public record Coffee(Guid Id, string Name, decimal Price);

public record ReverseResult(string Original, string Reversed);
