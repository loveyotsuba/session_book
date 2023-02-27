"""
First step: celery beat -A celery.server --loglevel=info

Second step: celery worker -A celery.server --loglevel=info
"""

import importlib
import redis
from celery import Celery

from config import WorkConfig
from model.db_models import db

#CELERY_ACCEPT_CONTENT = ['pickle']
#CELERY_TASK_SERIALIZER = 'pickle'

app = Celery('session_book', set_as_current=False) # 不设置实例为全局当前应用

beat_schedule = dict()
for cron in WorkConfig.CELERY_CONFIG['include']:
	module = importlib.import_module(cron)
	if hasattr(module, 'beat_schedule'):
		beat_schedule.update(getattr(module, 'beat_schedule'))

app.config_from_object(WorkConfig.CELERY_CONFIG)
app.conf.project_conf = WorkConfig
app.conf.beat_schedule = beat_schedule
app.conf.update(
	mysql_database = db,
	cache_redis = redis.StrictRedis(host='localhost', port=6379, db=1)
)
