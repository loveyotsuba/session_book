import concurrent
import tornado.gen
import tornado.web
import types
from functools import lru_cache

from base.log import TornadoLogger
from config import load_base_config
from model.db_models import db

# 全局变量
app = None
config = None

settings = {
	'cookie_secret': 'my_cookie_secret'
}

class Application(tornado.web.Application):
	def __init__(self, handlers, config, **settings):
		super(Application, self).__init__(handlers, **settings)
		self.config = config
		self.db_pool = db
		
		self.loop = tornado.ioloop.IOLoop.current()

		logger = TornadoLogger(self.config.PROJECT_ROOT, self.config.LOG_PATH, self.config.LOG_HANDLER, 
                                            self.config.LOG_FORMAT, self.config.DEBUG).logger
		self.logger = logger
		"""	
		def _run_callback(self, callback) -> None:
			try:
				ret = callback()
				print(ret)
				if ret is not None:
					try:
						# 生成的对象转为future
						ret = tornado.gen.convet_yielded(ret)
					except tornado.gen.BadYieldError:
						pass
				else:
					self.add_future(ret, self._discard_future_result)
			except concurrent.futures.CancelledError:
				pass
			except Exception:
				logger.error(f"Exception in callback {callback}", exc_info=True)	

		# _run_callback函数绑定到loop上作为loop的回调函数
		self.loop._run_callback = types.MethodType(_run_callback, self.loop)
		"""
	def run(self, port=8000, host='localhost'):
		self.listen(port, host)
		self.loop.start()



def make_app(env):
	global app, config
	print(env)	
	config = load_base_config(env)

	from docs import route

	app = Application(route.handlers, config, **settings)
		
	return app

