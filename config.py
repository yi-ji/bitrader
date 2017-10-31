import time

PRICE_BUFFER_SIZE = 100

WATCH_INTERVAL = 5 # second(s)
THINK_INTERVAL = 5 # second(s)

DEBUG = True

USERNAME = 'jiyi0327@gmail.com'
PASSWORD = 'himitsu desu.'

PHANTOM_BIN = './phantom/phantomjs'
LEVEL_DB = './data/price-db'

class Logger:
	def __init__(self):
		pass

	def log(self, msg):
		print(msg)

	def time_header(self):
		return time.strftime("%d %b %Y %H:%M:%S", time.localtime())

	def debug(self, msg):
		if DEBUG:
			msg = self.time_header() + ' [DEBUG]: ' + msg
			self.log(msg)

	def info(self, msg):
		msg = self.time_header() + ' [INFO]: ' + msg
		self.log(msg)

	def warn(self, msg):
		msg = self.time_header() + ' [WARN]: ' + msg
		self.log(msg)

	def error(self, msg):
		msg = self.time_header() + ' [ERROR]: ' + msg
		self.log(msg)

logger = Logger()