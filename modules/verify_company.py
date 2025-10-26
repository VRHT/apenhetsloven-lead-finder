import requests
from bs4 import BeautifulSoup
import re
import csv
import os
import time

CACHE_FILE = "data/verified_cache.csv"

def read_cache():
    """Leser tidligere verifiserte selskaper fra cache."""
    if not os.path.exists(CACHE_FILE):
        return {}
    with open(CACHE_FILE, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return {row["organisasjonsnummer"]: row for row in reader}

def write_cache(cache):
    """Lagrer cache til fil."""
    with open(CACHE_FILE, "w", newline='', encoding='utf-8') as f:
        fieldnames = ["organisasjonsnummer", "antall_ansatte", "omsetning", "balanse"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for orgnr, data in cache.items():
            writer.writerow(data)

def extract_number(text):
    """Trekker ut tall og fjerner mellomrom."""
    numbers = re.findall(r"\d+", text.replace(" ", ""))
    return int("".join(numbers)) if numbers else 0

def get_company_details(orgnr):
    """Henter selskapsdata fra Proff basert på organisasjonsnummer."""
    url = f"https://www.proff.no/selskap/{orgnr}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"⚠️  Feil ved henting av {orgnr}: {response.status_code}")
        return None

    soup = BeautifulSoup(response.text, "html.parser")

    try:
        omsetning_elem = soup.find(text=re.compile("Omsetning"))
        balanse_elem = soup.find(text=re.compile("Sum eiendeler"))
        ansatte_elem = soup.find(text=re.compile("Antall ansatte"))

        omsetning = extract_number(omsetning_elem.find_next("td").get_text()) if omsetning_elem else 0
        balanse = extract_number(balanse_elem.find_next("td").get_text()) if balanse_elem else 0
        ansatte = extract_number(ansatte_elem.find_next("td").get_text()) if ansatte_elem else 0

        return {
            "organisasjonsnummer": orgnr,
            "antall_ansatte": ansatte,
            "omsetning": omsetning,
            "balanse": balanse,
        }
    except Exception as e:
        print(f"⚠️  Parsing-feil for {orgnr}: {e}")
        return None

def qualifies_for_openhetsloven(company):
    """Returnerer True hvis selskapet oppfyller minst ett kriterium."""
    return (
        int(company.get("antall_ansatte", 0)) >= 50 or
        int(company.get("omsetning", 0)) >= 70_000_000 or
        int(company.get("balanse", 0)) >= 35_000_000
    )

def verify_companies(companies):
    """Verifiserer alle selskaper mot Proff, med caching og feilhåndtering."""
    cache = read_cache()
    verified = []

    for c in companies:
        orgnr = str(c["organisasjonsnummer"])
        if orgnr in cache:
            data = cache[orgnr]
        else:
            print(f"🔎 Henter data fra Proff for {orgnr} ...")
            data = get_company_details(orgnr)
            time.sleep(2.5)  # Unngå rate limiting
            if data:
                cache[orgnr] = data
                write_cache(cache)

        if data:
            if qualifies_for_openhetsloven(data):
                c.update(data)
                c["kvalifiserer"] = True
                verified.append(c)

    return verified
