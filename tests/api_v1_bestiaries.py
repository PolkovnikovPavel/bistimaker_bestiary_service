import requests


url = "http://127.0.0.1:6101/bestiaries-service/api/v1/bestiaries/"
url = "http://217.71.129.139:4989/bestiaries-service/api/v1/bestiaries/"

# TODO Сделать нормальные тесты

data = {
    "author": 0
}
response = requests.get(url, json=data)
print(response.json())

# data = {
#     "author": 1,
#     "name": 'бомжи 3',
#     "is_star": False
# }
# response = requests.put(url, json=data)
# print(response.json())

