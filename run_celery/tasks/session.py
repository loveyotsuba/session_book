import random
import time
from sqlalchemy import or_

from run_celery.server import app
from model.db_models import db, Session


class SessionService(object):
	@staticmethod
	@app.task
	def query(queries=None, expressions=None, all=False):
		if queries is None:
			queries = Session
		return Session.get_query(db, queries, expressions, all)

	@staticmethod
	@app.task
	def create(session):
		session_obj = Session(**session)
		db.add(session_obj)
		db.commit()

	
	@staticmethod
	@app.task
	def generate_session_id():
		session_id = random.randint(10**7, 10**9)
		bf = app.conf.bloom_filter
		while bf.is_exist(session_id):
			session_id = random.randint(10**6, 10**9)
		bf.add(session_id)
		return session_id
		
	@staticmethod
	@app.task
	def end_session(session_id):
		print("结束会议")
		db.query(Session).where(Session.session_id == session_id).update({"status": 1})
		db.commit()
		

