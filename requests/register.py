import requests
from threading import Thread

def register(i):
	param = {'name': f'test{i}', 'password': '123456', 'phone': f'phone{i}'}
	url = 'http://localhost:8000/register'

	res = requests.post(url, params=param)
	print(res, res.text)

if __name__ == "__main__":
	thread_list = []
	for i in range(4, 10001):
		t = Thread(target=register, args=(i, ))
		thread_list.append(t)
	for t in thread_list:
		t.start()
		t.join()
