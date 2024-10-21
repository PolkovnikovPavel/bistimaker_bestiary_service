import requests
import time

url = "http://127.0.0.1:8000/bestiaries-service/api/v1/"
url = "http://217.71.129.139:4989/bestiaries-service/api/v1/"
author = 0

response = requests.get(url + 'bestiaries/', json={"author": author})
b_id = response.json()[-1]['id']
print('Для бестиария с id =', b_id)


response = requests.get(url + 'categories/', json={"author": author, "bestiaries_id": b_id})
print('все категории ДО:', response.json(), '\n')


data = {
    "author": author,
    "bestiaries_id": b_id,
    "name": "новая категория",
    "background_img": "#000000",
    "background_color": "#000000",
}
response = requests.post(url + 'categories/', json=data)
с_id = response.json()['id']
print('Новая категория с id =', с_id)


response = requests.get(url + 'categories/', json={"author": author, "bestiaries_id": b_id})
print('все категории ПОСЛЕ:', response.json(), '\n')


data = {
    "author": author,
    "bestiaries_id": b_id,
    "name": "КРУТАЯ КАТЕГОРИЯ!!!"
}
response = requests.put(url + f'categories/{с_id}', json=data)
if response.status_code != 200:
    raise Exception('Изменение не удалось')

response = requests.get(url + f'categories/{с_id}', json={"author": author, "bestiaries_id": b_id})
print('Новая категория ПОСЛЕ:', response.json(), '\n')


response = requests.delete(url + f'categories/{с_id}', json={"author": author, "bestiaries_id": b_id})
print('УДАЛЕНИЕ:', response.json(), '\n\n=====================================')


response = requests.get(url + 'categories/', json={"author": author, "bestiaries_id": b_id})
print('все категории в конце:', response.json())

