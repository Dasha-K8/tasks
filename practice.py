import requests
from pymongo import MongoClient

client = MongoClient(host='mongo_db', port=27017)
db_practice = client['db_practice']

lots_collection = db_practice['lots_collection']
documents = []


base_url = "https://api.tenderbot.kz/api/lots"
keyword = "компьютер"
page = 1

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
    "kato_id": []

}
response = requests.post(base_url, json=payload)
data = response.json()


lots = data['aData']['lots']['data']

for lot in lots:
    documents.append({
        "id": lot.get("id"),
        "name_ru": lot.get("name_ru")
    })
lots_collection.insert_many(documents)

print("All lots have been recorded in the MongoDB database.")