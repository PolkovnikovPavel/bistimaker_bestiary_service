import requests


url = "http://127.0.0.1:8000/api/debug/bestiaries/"
url = "http://217.71.129.139:4989/api/debug/bestiaries/"


# response = requests.delete("http://127.0.0.1:8000/api/debug/bestiaries")
# print(response.json())


response = requests.get(url)
print(response.json())


data = {
    "name": "бомжи 1",
    "author": 0
}
response = requests.post(url, json=data)
print(response.json())


data = {
    "name": "бомжи 2",
    "author": 0
}
response = requests.post(url, json=data)
print(response.json())


data = {
    "name": "бомжи 3",
    "author": 1
}
response = requests.post(url, json=data)
print(response.json())


response = requests.get(url)
print('После добавления (1, 2, 3)\t\t' + response.text)
last_id = response.json()[-1]['id']


response = requests.delete(url + str(last_id))
print(f'Удаление 3 ({last_id})\t\t' + response.text)


response = requests.get(url)
print('После удаления 3\t\t' + response.text)

print('\n==============================================================\n')

