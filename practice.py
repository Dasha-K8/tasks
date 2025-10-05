import requests
import csv

base_url = "https://api.tenderbot.kz/api/lots"
keyword = "компьютер"
page = 1

with open("practice1.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["id", "name_ru"])

    while True:

        payload = {
            "methods": [],
            "tags": [],
            "search_tags": [
                {
                    "text": keyword,
                    "tiClasses": [
                        "ti-valid"
                    ]
                }
            ],
            "rate_id": 1,
            "rate_name": "KZT",
            "subject": [],
            "sort_col": "lots.created_at",
            "sort_type": "asc",
            "excluded": [],
            "partners": [],
            "searchstr": keyword,
            "types": [],
            "summ": [],
            "send_lots": "",
            "send_mail": "",
            "today": [],
            "hasitogt2": 0,
            "exactMatch": 0,
            "publicate": [],
            "closed": [],
            "search_type": [],
            "export_xls": "",
            "link": "lots.list",
            "bot_id": "",
            "bot_name": "",
            "max_amount": "",
            "markPko": 0,
            "markTph": 0,
            "markInvalid": 0,
            "markMedicine": 0,
            "cstatus": [],
            "customers": [],
            "kato_id": [],
            "page": page

        }
        response = requests.post(base_url, json=payload)
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











































