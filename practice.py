import requests
import csv

url = "https://api.tenderbot.kz/api/lots"

keyword = "компьютер"
payload = {
    "search_tags": [{"text": keyword, "tiClasses": ["ti-valid"]}],
    "searchstr": keyword
} # "search_tags" и "searchstr" c запроса в network

response = requests.post(url, json=payload)
data = response.json()

lots = data['aData']['lots']['data'] # записываю нужные данные из всего ответа

with open("practice1.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["id", "name_ru"])

    for lot in lots:
        writer.writerow([
            lot.get("id"),
            lot.get("name_ru")
        ])  # записываю id и name_ru для файла

print("Ответ с id и name_ru записан в файл practice1.csv")
