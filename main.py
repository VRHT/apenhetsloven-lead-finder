from modules.fetch_data import fetch_company_data
from modules.filter_companies import filter_companies
# from modules.verify_company import verify_companies  # slått av midlertidig
from modules.sheets_sync import upload_to_sheets

def main():
    print("=== Åpenhetsloven Lead Finder starter ===")

    companies = fetch_company_data()
    filtered = filter_companies(companies)

    # --- slå av Proff-verifisering inntil videre ---
    # verified = verify_companies(filtered)
    # upload_to_sheets(verified)

    upload_to_sheets(filtered)

    print("=== Ferdig ===")

if __name__ == "__main__":
    main()


