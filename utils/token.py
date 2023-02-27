import logging
import jwt
from datetime import datetime, timedelta

jwt_log = logging.getLogger("JWT")

def jwt_encode(data, secret_key, expires=7):
	"""
	生成token
	:param data: 用户数据
	:param secret_key: 加密串
	:param expires: 过期时间, 天
	:return:
	"""
	payload = {
		'data': data,
		'exp': datetime.now() + timedelta(days=expires), # 过期时间
		'issue_time': datetime.now().strftime("%H-%m-%d %H:%M:%S"),
	}
	try:
		token = jwt.encode(
			payload,
			secret_key,
			algorithm = 'HS256',
		)
	except Exception as e:
		print(e)
		jwt_log.error(e)
		return None
	return token

def jwt_decode(token, secret_key, **options):
	"""
	解析token
	:param token:
	:param secret_key:
	:param options
	:return:
	"""
	try:
		payload = jwt.decode(token, secret_key, algorithms='HS256', options=options)
	except Exception as e:
		jwt_log.error(e)
		return None
	return payload
	
