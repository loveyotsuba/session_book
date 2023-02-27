import importlib

from config import WorkConfig
from api.home import HomeHandler, LoginHandler, RegisterHandler


def import_string(dotted_path):
	"""
	"""
	try:
		module_path, class_name = dotted_path.rsplit('.', 1)
	except ValueError:
		msg = f"{dotted_path} doesn't look loke a module path"
		raise ImportError(msg)

	module = importlib.import_module(module_path)		
	
	try:
		return getattr(module, class_name)
	except AttributeError:
		msg = f'Module "{module_path}" does not define a "{class_name}" attribute/class'
		raise ImportError(msg)

class _RouterMetaclass(type):
	"""
	A singleton metaclass.
	"""
	_instances = None

	def __call__(self, *args, **kwargs):
		if self._instances is None:
			self._instances = super(_RouterMetaclass, self).__call__(*args, **kwargs)
		return self._instances

class Router(metaclass=_RouterMetaclass):	
	def _get_handlers(self):
		"""
		return a list of URL patterns, given the registered handlers.
		"""
		handlers_map = {}
		if WorkConfig.DEBUG:
			handlers_map[r'/?'] = HomeHandler
			handlers_map[r'/login/?'] = LoginHandler
			handlers_map[r'/register/?'] = RegisterHandler
		
		#for handler in WorkConfig.INSTALL_HANDERLS:
		#	import_string(handler)

		return [(rgex, handler) for rgex, handler in handlers_map.items()]
	
	@property
	def handlers(self):
		if not hasattr(self, '_handlers'):
			self._handlers = self._get_handlers()
		return self._handlers

route = Router()
