import requests
import time


# url = "http://127.0.0.1:6101/bestiaries-service/api/v1/bestiaries/12"
url = "http://217.71.129.139:4989/bestiaries-service/api/v1/bestiaries/14"
token = 'eyJhbGciOiJIUzI1NiJ9.eyJyb2xlIjoiUk9MRV9VU0VSIiwiaWQiOjMwLCJlbWFpbCI6InBhdmVscG9sa292bmlrb3YzMzRAZ21haWwuY29tIiwic3ViIjoicGF2ZWwiLCJpYXQiOjE3MzEyNTc3MDcsImV4cCI6MTczMTQwMTcwN30.-2UtZ2FXQvANCN8FgTfttRsrDQs1AKeZ4RDpG1yj16g'

headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json'
}


# TODO Сделать нормальные тесты

data = {
    "name": "Новое поколение драконов!",
    "src_icon": "/download/8.png",
    "description": "Это самый первый почти полноценный бестиарий или же справочник драконов с картинками и т.п. {Если вы видите этот текст, заначит бестиарий ещё не заполнен и просто красуется тут как пустышка)))}."
}
response = requests.get(url, json=data, headers=headers)
try:
    print(response.json())
except Exception:
    print(response)


timer = time.time()
response = requests.get('http://217.71.129.139:4989/bestiaries-service/api/v1/bestiaries/', headers=headers)
print(time.time() - timer)
try:
    print(response.json())
except Exception:
    print(response)


