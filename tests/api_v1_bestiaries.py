import requests


url = "http://127.0.0.1:6101/bestiaries-service/api/v1/bestiaries/12"
# url = "http://217.71.129.139:4989/bestiaries-service/api/v1/bestiaries/"

# TODO Сделать нормальные тесты

# data = {
#     "token": 'eyJhbGciOiJIUzI1NiJ9.eyJyb2xlIjoiUk9MRV9VU0VSIiwiaWQiOjI2LCJlbWFpbCI6InBhdmVscG9sa292bmlrb3YzMzQuMkBnbWFpbC5jb20iLCJzdWIiOiJhZG1pbjIiLCJpYXQiOjE3MzA5MDY4MjgsImV4cCI6MTczMTA1MDgyOH0.jRqORPKxiUugOnI635ECdyco5th9OpHHmRwapmJjn6g',
#     "name": 'dragons2',
# }
#
# response = requests.put(url, json=data)
# try:
#     print(response.json())
# except Exception:
#     print(response)
#

data = {
    "token": 'eyJhbGciOiJIUzI1NiJ9.eyJyb2xlIjoiUk9MRV9VU0VSIiwiaWQiOjI2LCJlbWFpbCI6InBhdmVscG9sa292bmlrb3YzMzQuMkBnbWFpbC5jb20iLCJzdWIiOiJhZG1pbjIiLCJpYXQiOjE3MzA5MDY4MjgsImV4cCI6MTczMTA1MDgyOH0.jRqORPKxiUugOnI635ECdyco5th9OpHHmRwapmJjn6g'
}
response = requests.get(url, json=data)
try:
    print(response.json())
except Exception:
    print(response)


