import requests
import csv

base_url = "https://api.tenderbot.kz/api/lots"
keyword = "компьютер"
page = 1

payload = {
    "search_tags": [{"text": keyword, "tiClasses": ["ti-valid"]}],
    "searchstr": keyword
}

with open("practice1.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["id", "name_ru"])

    while True:
        params = {"page": page}
        response = requests.post(base_url, params=params, json=payload)
        data = response.json()

        lots = data['aData']['lots']['data']

        for lot in lots:
            writer.writerow([
                lot.get("id"),
                lot.get("name_ru")
            ])

        next_page_url = data['aData']['lots'].get('next_page_url')

        if next_page_url is None:
            break
        page += 1

print("All lots with id and name_ru are saved in the practice1.csv file")




