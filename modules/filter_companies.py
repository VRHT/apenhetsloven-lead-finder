import math

def risk_score(company):
    ansatte = company.get("antall_ansatte", 0)
    bransje = company.get("naeringskode", "").lower()

    base = min(ansatte / 1000, 1.0)  # skaler ansatte 0–1
    risk = base

    # Øk score for typiske risikoutsatte bransjer
    risikobransjer = [
        "bygg", "anlegg", "renhold", "bemanning",
        "transport", "produksjon", "varehandel",
        "helse", "omsorg", "næringsmiddel"
    ]

    if any(word in bransje for word in risikobransjer):
        risk += 0.3

    # juster ned hvis veldig små virksomheter
    if ansatte < 10:
        risk -= 0.2

    # klem verdien mellom 0 og 1
    return round(max(0.0, min(risk, 1.0)), 2)


def filter_companies(companies):
    result = []
    for c in companies:
        ansatte = c.get("antall_ansatte", 0)
        if ansatte and ansatte > 50:
            c["risikoanalyse_score"] = risk_score(c)
            result.append(c)

    print(f"Fant {len(result)} selskaper med mer enn 50 ansatte.")
    return result


