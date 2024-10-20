import requests


url = "http://127.0.0.1:8000/api/v1/entities/3"
url = "http://217.71.129.139:4989/api/v1/entities/3"

# TODO Сделать нормальные тесты

data = {
    "author": 0,
    "bestiaries_id": 39
}
response = requests.get(url, json=data)
print(response.json())


data = {
    "author": 0,
    "bestiaries_id": 39,
    "name": "дракон 2",
}
response = requests.put(url, json=data)
print(response.json())
