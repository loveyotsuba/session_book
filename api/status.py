class Code:
	class System:
		SUCCESS = 0
		ERROR = -1

	class User:
		USER_INVALID = 110001
		TOKEN_INVALID = 110003
		USER_IS_EXIST = 110004

class Message:
	class System:
		SUCCESS = "成功"
		ERROR = "系统繁忙"

	class User:
		USER_INVALID = "用户名，手机号，或者密码错误!"
		TOKEN_INVALID = "Token无效!"	
		USER_IS_EXIST = "该用户已存在，请直接登录!"
