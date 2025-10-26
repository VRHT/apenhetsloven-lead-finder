from datetime import datetime
import pandas as pd
from modules.fetch_data import fetch_company_data
from modules.filter_companies import filter_companies
from modules.sheets_sync import upload_to_sheets

def main():
    print("=== Åpenhetsloven Lead Finder starter ===")

    # 1. Hent data
    companies = fetch_company_data()
    print(f"Hentet {len(companies)} selskaper.")

    # 2. Filtrer selskaper
    filtered = filter_companies(companies)
    print(f"Etter filtrering: {len(filtered)} selskaper igjen.")

    # 3. Legg til/oppdater 'last_updated' kolonne
    filtered["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 4. Lagre til CSV
    csv_path = "data/companies.csv"
    filtered.to_csv(csv_path, index=False)
    print(f"✅ Lagret oppdatert CSV med timestamp: {csv_path}")

    # 5. Last opp til Google Sheets
    upload_to_sheets(filtered)
    print("📤 Data lastet opp til Google Sheets.")

    print("=== Ferdig! ===")

if __name__ == "__main__":
    main()

