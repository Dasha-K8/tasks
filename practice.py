import requests
import csv

url = "https://api.tenderbot.kz/api/lots"

payload = {"q": "компьютер"}


response = requests.post(url, json=payload)
data = response.json()

with open("../autotests-api/practice1.csv", "w") as file:
    writer = csv.DictWriter(file, fieldnames=data)
    writer.writerow(data)

print("Ответ записан в файл practice1.csv")