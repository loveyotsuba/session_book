import requests

param = {'name': 'test3', 'password': '123456', 'phone': 'phone3'}
url = 'http://localhost:8000/login'

res = requests.post(url, params=param)
print(res.cookies.get_dict())
print(res, res.text)
