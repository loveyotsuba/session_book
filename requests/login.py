import requests
import time
from threading import Thread

def login(i):
	param = {'name': f'test{i}', 'password': '123456', 'phone': f'phone{i}'}
	url = 'http://localhost:8000/login'
	print(f"第{i}个发送时间: ", time.time())
	res = requests.post(url, params=param)
	print(res, res.text)
	print(f"第{i}个接受时间: {time.time()}")


if __name__ == "__main__":
	for i in range( 1, 10001):
		t = Thread(target=login, args=(i,))
		t.start()
