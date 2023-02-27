import random
import time

def generate_session_id():
	cnt = 0
	while True:
		cnt += 1
		t1 = time.time()
		t = random.randint(10**7, 10**9 - 1)		
		print(time.time()-t1)

generate_session_id()
