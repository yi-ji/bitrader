import config
import json, leveldb, time

class Logger:
	def __init__(self):
		pass

	def log(self, msg):
		print(msg)

	def time_header(self):
		return time.strftime("%d %b %Y %H:%M:%S", time.localtime())

	def debug(self, msg):
		if config.DEBUG:
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

def json2leveldb():
	with open(config.PRICE_FILE) as price_data:
		price_json = json.loads(price_data.read())
		db = leveldb.LevelDB(config.LEVEL_DB)
		for time_price_pair in price_json:
			timestamp = str(int(time_price_pair[0])/1000)
			price = str(time_price_pair[1])
			db.Put(timestamp, price)

