import requests
import csv

base_url = "https://api.tenderbot.kz/api/lots?page="
last_page = 15

keyword = "компьютер"
payload = {
    "search_tags": [{"text": keyword, "tiClasses": ["ti-valid"]}],
    "searchstr": keyword
}

with open("practice1.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["id", "name_ru"])

    for page in range(1, last_page + 1):
        url = f"{base_url}{page}"
        response = requests.post(url, json=payload)
        data = response.json()

        lots = data['aData']['lots']['data']

        for lot in lots:
            writer.writerow([
                lot.get("id"),
                lot.get("name_ru")
            ])

print("All lots with id and name_ru are saved in the practice1.csv file")
