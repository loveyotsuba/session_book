from celery.result import AsyncResult
from datetime import datetime

from .base import BaseHandler, jwt_auth
from run_celery.server import app
from run_celery.tasks.user import UserService
from .status import Code, Message
from utils.token import jwt_encode

class HomeHandler(BaseHandler):
	@jwt_auth
	async def get(self):
		return self.write_success(msg=f'欢迎回来, 用户{self.current_user}!')

class RegisterHandler(BaseHandler):
	async def post(self):
		phone = self.get_arg('phone')
		name = self.get_arg('name')
		password = self.get_arg('password')
		if (UserService.query_redis(name) or UserService.query_redis(phone)):
			self.write_fail(Code.User.USER_IS_EXIST, Message.User.USER_IS_EXIST)
			self.finish()
		else:
			user = {
				'phone': phone,
				'name': name,
				'password': password,
				'created_at': datetime.now(),
			}
			UserService.createUser.apply_async((user, ))
			self.write_success()
		
			
			

class LoginHandler(BaseHandler):
	async def post(self):
		phone = self.get_arg('phone')
		name = self.get_arg('name')
		password = self.get_arg('password')
		if (UserService.query_redis(name) != password or UserService.query_redis(phone) != password):
			self.write_fail(Code.User.USER_INVALID, Message.User.USER_INVALID)
			self.finish()
		else:
			data = {
				'name': name,
				'login_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
			}
			token = jwt_encode(data, self.application.config.TOKEN_SECRET_KEY,
					   expires=self.application.config.TOKEN_EXPIRE_DAYS)
			self.set_secure_cookie('token', token)
			self.write_success(msg="登录成功!")
	
