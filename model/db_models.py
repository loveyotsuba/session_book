from datetime import datetime
from sqlalchemy import create_engine, and_, or_
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import WorkConfig

DbBase = declarative_base()

def db_pool_init():
	engine_config = WorkConfig.MYSQL_CONFIG['engine_url']
	engine = create_engine(engine_config, **WorkConfig.MYSQL_CONFIG['engine_setting'])
	db_pool = sessionmaker(bind=engine)
	return db_pool()

db = db_pool_init()

class DbInit(object):
	created_at = Column(DateTime, default=datetime.now)

	def to_dict(self):
		return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}

	@classmethod
	def get_query(cls, db_session, queries, expressions, all):
		print("开始查表")
		if isinstance(queries, list):
			queries = [hasattr(cls, field) for field in queries]
			query = db_session.query(*queries)
		else:	
			query = db_session.query(queries)
		if expressions is None:
			return query
		query = query.filter(cls.get_expression(expressions))
		if all:
			return query.all().to_dict()
		else:
			return query.first().to_dict()

	@classmethod		
	def get_expression(cls, expressions, is_join=None):
		stack = []
		index = 0
		while (index < len(expressions)):
			if expressions[index] in ('|', '&'):
				stack.append(cls.get_expression(expressions[index + 1], is_join=expressions[index]))
				index += 2
			else:
				field = getattr(cls, expressions[index + 1], None)
				val = expressions[index + 2]
				if expressions[index] == '==':
					stack.append(field == val)
				index += 3
		if is_join is None:
			return stack[0]
		elif is_join == '|':
			return or_(*stack)
		else:
			return and_(*stack)

				
			
			
			



class User(DbBase, DbInit):
	__tablename__ = 'user'
	id = Column(Integer, primary_key=True)
	name = Column(String(64), unique=True, index=True)
	password = Column(String(128))
	phone = Column(String(64), unique=True, index=True)

