


class BaseConfig(dict):
	"""Project base settings"""
	#PROJECT_ROOT = os.path.realpath(os.path.dirname(__file__))
	#INSTALL_HANDLERS = list()
	#INSTALL_HANDLERS_NAME = dict()
	
	############
	# Tornado Docs #
	DOCS_USERNAME = 'super'
	DOCS_PASSWORD = '123456'
	#DOCS_GLOBAL_PARAMS = []
	#DOCS_GLOBAL_HEADERS = []
	DOCS_TOKEN_VERIFY_EXPIRE = True
	DOCS_TOKEN_EXPIRE_DAYS = 7
	DOCS_TOKEN_SECRET_KEY = "my token secret"

	# APP

	DEBUG = True

	REQUEST_ALLOW_ORIGIN = ['*']
	REQUEST_ALLOW_HEADERS = ['*']

	
