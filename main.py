from modules.fetch_data import fetch_company_data
from modules.filter_companies import filter_companies
from modules.sheets_sync import upload_to_sheets

def main():
    print("=== Åpenhetsloven Lead Finder starter ===")

    companies = fetch_company_data()
    filtered = filter_companies(companies)
    upload_to_sheets(filtered)

    print("=== Ferdig ===")

if __name__ == "__main__":
    main()

