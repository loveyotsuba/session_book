import requests

def login():
	param = {'name': 'test1', 'password': '123456', 'phone': 'phone1'}
	url = 'http://localhost:8000/login/'
	res = requests.post(url, params=param)
	cookies = res.cookies
	cookie = requests.utils.dict_from_cookiejar(cookies)
	print("登录成功！")
	return cookie

def book(cookie):
	url = 'http://localhost:8000/session/book'
	start_time = "2023-02-27 17:28:00"
	end_time = "2023-02-27 17:28:30"
	num = 3
	param = {'start_time': start_time, 'end_time': end_time}
	res = requests.post(url, params=param, cookies=cookie)
	print(res.text)


if __name__ == "__main__":
	cookie = login()
	book(cookie)
