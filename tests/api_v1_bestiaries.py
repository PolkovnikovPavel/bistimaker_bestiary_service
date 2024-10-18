import requests


url = "http://127.0.0.1:8000/api/v1/bestiaries/35"
url = "http://217.71.129.139:4989/api/v1/bestiaries/35"


data = {
    "author": 1
}
response = requests.get(url, json=data)
print(response.json())

data = {
    "author": 1,
    "name": 'бомжи 3',
    "is_star": False
}
response = requests.put(url, json=data)
print(response.json())

