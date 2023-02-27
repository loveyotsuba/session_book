import inspect
import json
import tornado.web

from .status import Code, Message 
from utils.token import jwt_decode

class BaseHandler(tornado.web.RequestHandler):
	current_user_id = None
	
	before_request_funcs = []
	after_request_funcs = []

	def __init__(self, *args, **kwargs):
		super(BaseHandler, self).__init__(*args, **kwargs)
	
	@property
	def user_id(self):
		return self.current_user_id	

	async def prepare(self):
		if self.before_request_funcs:
			await tornado.gen.multi(self.before_request_funcs)
	def add_callback(self, callback, *args, **kwargs):
		self.application.loop.add_callback(call_back, *args, **kwargs)

	def get_current_user(self):
		token = self.get_secure_cookie('token')
		print("token", token)
		if not token:
			return None
		payload = jwt_decode(token, self.application.config.TOKEN_SECRET_KEY,
				     verify_exp=self.application.config.TOKEN_VERIFY_EXPIRE)	
		if not payload or not payload.get('data'):
			return None
		return payload['data']['name']
	
	def on_finish(self):
		#async
		for func in self.after_request_funcs:
			func_args = inspect.getfullargspec(func).args

	def set_default_headers(self):
		allow_origin = ','.join(self.application.config.ALLOW_ORIGIN)
		allow_headers = ','.join(self.application.config.ALLOW_HEADERS)
		allow_method = ','.join(self.application.config.ALLOW_METHOD)

		self.set_header("Access-Control-Allow-Origin", allow_origin)
		self.set_header("Access-Control-Allow-Headers", allow_headers)
		self.set_header("Access-Control-Allow-Method", allow_method)


	def write_fail(self, code=Code.System.ERROR, msg=Message.System.ERROR, data={}, ensure_ascii=False):
		"""
		Reuqest Fail. Return fail message.
		"""
		return self.write(json.dumps({'return_code': code, 'return_data': data, 'return_msg': msg}, ensure_ascii=ensure_ascii))
	
	def write_success(self, code=Code.System.SUCCESS, msg=Message.System.SUCCESS, data={}, ensure_ascii=False):
		"""
		Request Success. Return success message.
		"""
		return self.write(json.dumps({'return_code': code, 'return_data': data, 'return_msg': msg}, ensure_ascii=ensure_ascii))
	
	# async def before_request(self) -> Awaitable
	
	# def after_request(self) -> Awaitable

	# def _get_argument(self, name, default=None, strip=True)

	# def get_headers(self, name, default=None, strip=True)

	def get_arg(self, name, default=None, strip=True):
		argument = self.get_argument(name, default=default, strip=strip) or default
		return argument
	# def _log(self):

	#def log_request(self):

def jwt_auth(method):
	async def wrapper(self, *args, **kwargs):
		self.current_user = self.get_current_user()
		if not self.current_user:
			return self.write_fail(Code.User.TOKEN_INVALID, Message.User.TOKEN_INVALID)

		return await method(self, *args, **kwargs)
	return wrapper

