import requests


url = "http://127.0.0.1:6102/bestiaries-service/api/v1/bestiaries/6"
url = "http://217.71.129.139:4989/bestiaries-service/api/v1/bestiaries/6"

# TODO Сделать нормальные тесты

data = {
    "author": 1
}
response = requests.get(url, json=data)
try:
    print(response.json())
except Exception:
    print(response)



# data = {
#     "author": 1,
#     "name": 'бомжи 3',
#     "is_star": False
# }
# response = requests.put(url, json=data)
# print(response.json())

