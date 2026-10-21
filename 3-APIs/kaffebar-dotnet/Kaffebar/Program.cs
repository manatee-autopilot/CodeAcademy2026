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

// --- Snu tekst ------------------------------------------------------------
// Snur rekkefølgen på ordene og bokstavene i hvert ord. Mellomrom og tegnsetting
// beholder posisjonen sin. Første bokstav blir stor, resten små.
app.MapGet("/reverse", (string? text) =>
{
    if (string.IsNullOrWhiteSpace(text))
    {
        return Results.BadRequest(new { error = "Parameteren 'text' er påkrevd." });
    }

    var words = Regex.Matches(text, @"\p{L}+")
        .Select(m => new string(m.Value.Reverse().ToArray()))
        .Reverse()
        .ToArray();

    var index = 0;
    var result = Regex.Replace(text, @"\p{L}+", _ => words[index++]).ToLowerInvariant();

    // Første bokstav, ikke nødvendigvis første tegn (kan være mellomrom eller tegnsetting).
    var first = result.Select((c, i) => (c, i)).FirstOrDefault(x => char.IsLetter(x.c));
    if (char.IsLetter(first.c))
    {
        result = string.Concat(result.AsSpan(0, first.i), char.ToUpperInvariant(first.c).ToString(), result.AsSpan(first.i + 1));
    }

    return Results.Ok(new ReverseResult(result));
})
.WithName("ReverseText")
.WithSummary("Snu tekst")
.WithDescription("Snur rekkefølgen på ordene og bokstavene i hvert ord, beholder mellomrom og tegnsetting, og gir resultatet stor forbokstav.");

// --- Store bokstaver ------------------------------------------------------
app.MapGet("/uppercase", (string? text) =>
{
    if (string.IsNullOrWhiteSpace(text))
    {
        return Results.BadRequest(new { error = "Parameteren 'text' er påkrevd." });
    }

    return Results.Ok(new UppercaseResult(text.ToUpperInvariant()));
})
.WithName("UppercaseText")
.WithSummary("Gjør tekst om til store bokstaver")
.WithDescription("Returnerer teksten med store bokstaver (invariant kultur). Mangler eller er 'text' blank, gis HTTP 400.");

app.Run();

// DTO-er kan ligge i Program.cs når prosjektet er lite.
// Etter hvert er det ryddig å flytte dem til egne filer i en Models-mappe.
public record Coffee(Guid Id, string Name, decimal Price);

public record ReverseResult(string Result);

public record UppercaseResult(string Result);
