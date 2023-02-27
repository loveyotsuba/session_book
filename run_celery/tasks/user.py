import time
from sqlalchemy import or_

from run_celery.server import app
from model.db_models import db, User


class UserService(object):
	@staticmethod
	@app.task
	def query_redis(key):
		cache = app.conf.cache_redis
		load = cache.set('load_user', 'loading', nx=True)
		if load:
			users = UserService.query(all = True)
			for user in users:
				cache.set(user.name, user.password)
				cache.set(user.phone, user.password)
			cache.set('load_user', 'loaded')
		load = cache.get('load_user')
		while (load.decode() != 'loaded'):
			time.sleep(30)
			load = cache.get('load_user')
		print(key)
		password = cache.get(key)
		if password:
			return cache.get(key).decode()
		else:	
			return None
			

	@staticmethod
	@app.task
	def query(queries=None, expressions=None, all=False):
		if queries is None:
			queries = User
		return User.get_query(db, queries, expressions, all)

	@staticmethod
	@app.task
	def createUser(user):
		user_obj = User(**user)
		db.add(user_obj)
		db.commit()
		cache = app.conf.cache_redis
		cache.set(user['name'], user['password'])
		cache.set(user['phone'], user['password'])
		

