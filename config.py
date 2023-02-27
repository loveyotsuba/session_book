import os
import logging
from functools import lru_cache
from urllib.parse import quote_plus as urlquote

class BaseConfig(object):
	""" Public config """
	PROJECT_ROOT = os.path.realpath(os.path.dirname(__file__)) 
	DEBUG = True
	
	NO_KEEP_ALIVE = True

	INSTALL_HANDLERS = list()
	INSTALL_HANDLERS_NAME = dict()

	TOKEN_VERIFY_EXPIRE = True
	TOKEN_EXPIRE_DAYS = 30
	TOKEN_SECRET_KEY = 'my token secret'

	# APP
	LOG_PATH = 'logs'
	LOG_HANDLER = [
		logging.INFO,
		logging.WARNING,
		logging.ERROR
	]
	LOG_FORMAT = '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s'		


	ALLOW_ORIGIN = ['*']
	ALLOW_HEADERS = ['*']
	ALLOW_METHOD = ['POST', 'GET', 'OPTIONS']

	def from_dict(self, d):
		for key, val in d.items():
			setattr(self, key, val)	


class WorkConfig(object):	
	DEBUG = True

	# MySQL
	MYSQL_CONFIG = {
		'engine': None,
		'engine_url': f'mysql+mysqlconnector://root:{urlquote("123456")}@localhost:3306/session_book?charset=utf8',
		'engine_setting': {
			'echo': False,   # print url
			'echo_pool': False,
			'pool_recycle': 25200,
			'pool_size': 20,
			'max_overflow': 20,
		}
	}		

	# Celery
	CELERY_CONFIG = {
		'timezone': 'Asia/Shanghai',
		'enable_utc': False,
		'sqlalchemy_url': f'mysql+mysqlconnector://root:{urlquote("123456")}@localhost:3306/session_book?charset=utf8',
		'broker_url': 'redis://:@127.0.0.1:6379/0',
		'result_backend': 'redis://:@127.0.0.1:6379/0',
		'task_serializer': 'json',
		'result_serializer': 'json',
		'accept_content': ['json'],
		'include': [
			'run_celery.tasks.user',
			'run_celery.tasks.session',
		]
	}

#@lru_cache()
def load_base_config(env):
	config = BaseConfig()	
	config.from_dict(env)
	return config

@lru_cache()
def load_work_config():
	config = WorkConfig()
	return config
