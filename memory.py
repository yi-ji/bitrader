import collections, time
import config
from utils import logger

class Memory:
	def __init__(self, db):
		self.db = db
		self.buffer = collections.deque([], config.PRICE_BUFFER_SIZE)
		self.cache = collections.deque([], config.PRICE_CACHE_SIZE)
		self.first_order = collections.deque([], config.PRICE_CACHE_SIZE)
		self.mid = None
		self.ask = None
		self.bid = None
		self.record_timestamp = None
		self.retrospect()

	def update(self, ask_price, bid_price):
		self.ask = int(ask_price)
		self.bid = int(bid_price)
		self.mid = (self.ask+self.bid)/2
		if self.cache:
			self.first_order.appendleft(self.mid - self.cache[0])
		self.cache.appendleft(self.mid)
		timestamp = int(time.time())
		if self.record_timestamp is None or timestamp - self.record_timestamp > config.RECORD_INTERVAL:
			self.record_timestamp = timestamp
			self.db.Put(str(timestamp), str(self.ask)+'|'+str(self.bid))
			self.buffer.appendleft((str(timestamp), str(self.ask)+'|'+str(self.bid)))

	def retrospect(self):
		now_time = int(time.time())
		interval = 3600
		while True:
			few_time_ago = now_time - interval
			interval *= 2
			if few_time_ago < 1451606400:
				logger.error('not enough history data to prefill the buffer, exit')
				sys.exit(0)
			logger.debug('try to prefill data from timestamp '+str(few_time_ago)+' to '+str(now_time))
			past_data = list(self.db.RangeIter(key_from = str(few_time_ago), key_to = str(now_time)))
			if len(past_data) >= config.PRICE_BUFFER_SIZE/5:
				for ele in past_data[len(past_data)-config.PRICE_BUFFER_SIZE:]:
					if ele[1] != 'CLOSED|CLOSED':
						self.buffer.appendleft(ele)
				break
		logger.info('price buffer prefilled with past data')

