import math
# from modules.verify_company import verify_companies  # slått av midlertidig

def risk_score(company):
    ansatte = company.get("antall_ansatte", 0)
    bransje = company.get("næringskode", "").lower()

    base = min(ansatte / 1000, 1.0)
    risk = base

    risikobransjer = [
        "bygg", "anlegg", "renhold", "bemanning",
        "transport", "produksjon", "varehandel",
        "helse", "omsorg", "næringsmiddel"
    ]
    if any(word in bransje for word in risikobransjer):
        risk += 0.3

    if ansatte < 10:
        risk -= 0.2

    return round(max(0.0, min(risk, 1.0)), 2)

def filter_companies(companies):
    print("🔍 Filtrerer selskaper på regioner og årsverk ...")

    # Kun Oslo, Akershus, Østfold
    filtered = [c for c in companies if c.get("kommune", "").upper() in ["OSLO", "AKERSHUS", "ØSTFOLD"]]

    # Kun selskaper med minst 30 årsverk
    filtered = [c for c in filtered if c.get("antall_ansatte", 0) >= 30]
    print(f"✅ {len(filtered)} selskaper har minst 30 årsverk i Oslo, Akershus eller Østfold.")

    # Beregn risikoanalyse
    for c in filtered:
        c["risikoanalyse_score"] = risk_score(c)

    print(f"📊 {len(filtered)} selskaper inkluderes i eksport (CSV + Google Sheets).")

    # --- midlertidig slått av Proff-verifisering ---
    # verified = verify_companies(filtered)
    # return verified

    return filtered



