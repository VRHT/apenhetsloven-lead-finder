def upload_to_sheets(data):
    # Foreløpig bare skriv ut til terminalen
    print("Sender følgende selskaper til Sheets:")
    for c in data:
        print(f"- {c['navn']}")
