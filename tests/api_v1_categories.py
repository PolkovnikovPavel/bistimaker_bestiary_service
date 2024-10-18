import requests
import time

url = "http://127.0.0.1:8000//api/v1/categories/2"
url = "http://217.71.129.139:4989//api/v1/categories/2"


data = {
    "author": 0,
    "bestiaries_id": 38
}
timer = time.time()
response = requests.get(url, json=data)
print(time.time() - timer, response.json())


data = {
    "author": 0,
    "bestiaries_id": 38,
    "name": "монстры 2"
}
response = requests.put(url, json=data)
print(response.json())
