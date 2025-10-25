def filter_companies(companies):
    result = []
    for c in companies:
        # Hent antall ansatte
        ansatte = c.get("antall_ansatte", 0)

        # Foreløpig filtrering basert på antall ansatte
        # (senere kan vi utvide med økonomidata fra Proff.no eller regnskaps-API)
        if ansatte and ansatte > 50:
            result.append(c)

    print(f"Fant {len(result)} selskaper med mer enn 50 ansatte.")
    return result

