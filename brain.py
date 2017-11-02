import config
import time
from utils import logger

class Brain:
	def __init__(self, _price_buffer, _my_hand):
		self.buffer = _price_buffer
		self.hand = _my_hand

	def get_trend(self):
		trend = []

		interval = config.INDICATER_INETRVAL_INIT
		time_point = int(time.time()) - interval
		price_sum = 0

		buffer_len = len(self.buffer.buffer)
		for buffer_iter in range(0, buffer_len-1):
			item = self.buffer.buffer[buffer_iter]
			timestamp = int(item[0])
			mid = [float(price) for price in item[1].split('|')]
			mid = (mid[0]+mid[1])/2 if len(mid) > 1 else mid[0]
			#print item, timestamp, mid, time_point
			if timestamp <= time_point:
				average = float(price_sum)/float(buffer_iter)
				trend.append((time_point, (self.buffer.mid-average)/float(average)))
				#print int(time.time())-time_point, average, '|', self.buffer.mid
				interval *= config.INTERVAL_GROW_FACTOR
				time_point -= interval
			price_sum += mid

		logger.debug(str([(int(time.time()-a), b) for (a, b) in trend]))

	def decide_buy(self, trend):
		return -1

	def decide_sell(self, trend):
		return -1

	def start_thinking(self):
		while True:
			time.sleep(config.THINK_INTERVAL)
			trend = self.get_trend()

			buy_amount = self.decide_buy(trend)
			if buy_amount > config.MIN_TRADE_AMOUNT:
				self.hand.buy(self.buffer.ask, jpy=buy_amount)

			sell_amount = self.decide_sell(trend)
			if sell_amount > config.MIN_TRADE_AMOUNT:
				self.hand.sell(self.buffer.bid, jpy=sell_amount)
