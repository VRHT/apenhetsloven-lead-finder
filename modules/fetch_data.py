import requests
import time

def fetch_company_data():
    base_url = "https://data.brreg.no/enhetsregisteret/api/enheter"
    all_companies = []
    size = 100  # antall selskaper per side

    # Kommunenummer for Oslo, Akershus og Østfold
    kommune_liste = [
        # Oslo
        "0301",
        # Akershus (nye kommuner etter 2024-struktur)
        "3024", "3025", "3026", "3027", "3028", "3029", "3030", "3031", "3032", "3033", "3034",
        # Østfold (gamle Østfold-kommuner)
        "3001", "3002", "3003", "3004", "3005", "3006", "3011", "3012", "3013", "3014"
    ]

    for kommunenr in kommune_liste:
        page = 0
        while True:
            params = {
                "page": page,
                "size": size,
                "kommunenummer": kommunenr
            }

            response = requests.get(base_url, params=params)
            response.raise_for_status()
            data = response.json()
            companies = data.get("_embedded", {}).get("enheter", [])

            if not companies:
                break

            for item in companies:
                all_companies.append({
                    "navn": item.get("navn"),
                    "organisasjonsnummer": item.get("organisasjonsnummer"),
                    "antall_ansatte": item.get("antallAnsatte", 0),
                    "kommune": item.get("forretningsadresse", {}).get("kommune", ""),
                    "naeringskode": item.get("naeringskode1", {}).get("beskrivelse", "")
                })

            print(f"Hentet {len(companies)} selskaper fra kommune {kommunenr}, side {page + 1}")
            page += 1
            time.sleep(0.4)

            # Begrens testkjøring for å unngå tusenvis av treff
            if page >= 3:
                break

    print(f"Totalt hentet {len(all_companies)} selskaper fra Oslo, Akershus og Østfold.")
import pandas as pd
import os
import requests
import time

def fetch_company_data():
    base_url = "https://data.brreg.no/enhetsregisteret/api/enheter"
    all_companies = []
    size = 100

    kommune_liste = [
        "0301",  # Oslo
        # Akershus (nye kommuner)
        "3024", "3025", "3026", "3027", "3028", "3029", "3030", "3031", "3032", "3033", "3034",
        # Østfold
        "3001", "3002", "3003", "3004", "3005", "3006", "3011", "3012", "3013", "3014"
    ]

    for kommunenr in kommune_liste:
        page = 0
        while True:
            params = {
                "page": page,
                "size": size,
                "kommunenummer": kommunenr
            }

            response = requests.get(base_url, params=params)
            response.raise_for_status()
            data = response.json()
            companies = data.get("_embedded", {}).get("enheter", [])

            if not companies:
                break

            for item in companies:
                all_companies.append({
                    "navn": item.get("navn"),
                    "organisasjonsnummer": item.get("organisasjonsnummer"),
                    "antall_ansatte": item.get("antallAnsatte", 0),
                    "kommune": item.get("forretningsadresse", {}).get("kommune", ""),
                    "naeringskode": item.get("naeringskode1", {}).get("beskrivelse", "")
                })

            print(f"Hentet {len(companies)} selskaper fra kommune {kommunenr}, side {page + 1}")
            page += 1
            time.sleep(0.4)

            if page >= 3:
                break

    print(f"Totalt hentet {len(all_companies)} selskaper fra Oslo, Akershus og Østfold.")

    # Lagre til CSV
    df = pd.DataFrame(all_companies)
    os.makedirs("data", exist_ok=True)
    csv_path = os.path.join("data", "companies.csv")
    df.to_csv(csv_path, index=False, encoding="utf-8-sig")

    print(f"Lagret {len(all_companies)} selskaper til {csv_path}")
    return all_companies



