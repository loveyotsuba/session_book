from pytz import timezone, utc
from datetime import datetime

from api.base import BaseHandler, jwt_auth
from api.status import Code, Message
from run_celery.tasks.session import SessionService

class SessionBookHandler(BaseHandler):
	@jwt_auth
	async def post(self):
		start_time = self.get_arg('start_time')
		end_time = self.get_arg('end_time')
		num = self.get_arg('num')
		expressions = [['&', ['<', 'start_time', end_time, '>', 'end_time', start_time]]] + [['==', 'applicant', self.current_user]]
		session = SessionService.query(['id'], expressions)
		if session:
			self.write_fail(Code.Session.PRIOD_EXIST, Message.Session.PRIOD_EXIST)	
		else:
			session_id = SessionService.generate_session_id()
			session = {
				'session_id': session_id,
				'created_at': datetime.now(),
				'applicant': self.current_user,
				'start_time': start_time,
				'end_time': end_time,
				'status': 0,
				'num': num,
			}
			SessionService.create(session)	
			eta = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S").astimezone(timezone('Asia/Shanghai'))
			print(eta, eta.tzinfo)
			SessionService.end_session.apply_async((session_id, ), eta=eta, utc=False)
			self.write_success()
			
