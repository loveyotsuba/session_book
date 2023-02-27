import sys
from base import make_app


if __name__ == '__main__':
	options = {}
	if len(sys.argv) > 1:
		if sys.argv[1] == 'upgradedb':
			from alembic.config import main
			main('upgrade head'.split(' '), 'alembic')
	
			exit(0)
		for arg in sys.argv[1:]:
			k, v = arg.strip('--').split('=', 1)
			options[k] = v
	app = make_app(options)
	app.run()
