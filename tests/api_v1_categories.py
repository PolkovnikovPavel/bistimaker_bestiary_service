import requests
import time

# url = "http://127.0.0.1:6101/bestiaries-service/api/v1/"
url = "http://217.71.129.139:4989/bestiaries-service/api/v1/"
token = 'eyJhbGciOiJIUzI1NiJ9.eyJyb2xlIjoiUk9MRV9VU0VSIiwiaWQiOjMwLCJlbWFpbCI6InBhdmVscG9sa292bmlrb3YzMzRAZ21haWwuY29tIiwic3ViIjoicGF2ZWwiLCJpYXQiOjE3MzE3NDc4NjUsImV4cCI6MTczMTg5MTg2NX0.7TMHRBqx7_lmIQWUK48AAnBMhSnXvRwbxYTRn6Q4Ve4'

headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json'
}


response = requests.get(url + 'bestiaries/', headers=headers)
b_id = response.json()[-1]['id']
print('Для бестиария с id =', b_id)


response = requests.get(url + 'categories/', json={"bestiaries_id": b_id}, headers=headers)
print('все категории ДО:', response.json(), '\n')


data = {
    "bestiaries_id": b_id,
    "name": "новая категория",
    "background_img": "#000000",
    "background_color": "#000000",
}
response = requests.post(url + 'categories/', json=data, headers=headers)
с_id = response.json()['id']
print('Новая категория с id =', с_id)


response = requests.get(url + 'categories/', json={"bestiaries_id": b_id}, headers=headers)
print('все категории ПОСЛЕ:', response.json(), '\n')


data = {
    "bestiaries_id": b_id,
    "name": "КРУТАЯ КАТЕГОРИЯ!!!"
}
response = requests.put(url + f'categories/{с_id}', json=data, headers=headers)
if response.status_code != 200:
    raise Exception('Изменение не удалось')

response = requests.get(url + f'categories/{с_id}', json={"bestiaries_id": b_id}, headers=headers)
print('Новая категория ПОСЛЕ:', response.json(), '\n')


response = requests.delete(url + f'categories/{с_id}', json={"bestiaries_id": b_id}, headers=headers)
print('УДАЛЕНИЕ:', response.json(), '\n\n=====================================')


response = requests.get(url + 'categories/', json={"bestiaries_id": b_id}, headers=headers)
print('все категории в конце:', response.json())

