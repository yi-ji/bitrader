import config
import time, itertools
from utils import logger
from sklearn.linear_model import LinearRegression as LR
import numpy as np

class Brain:
	def __init__(self, _memory, _my_hand):
		self.memory = _memory
		self.hand = _my_hand

	def get_trend(self):
		trend = []

		interval = config.INDICATER_INETRVAL_INIT
		time_point = int(time.time()) - interval
		price_sum = 0

		buffer_len = len(self.memory.buffer)
		for buffer_iter in range(0, buffer_len-1):
			item = self.memory.buffer[buffer_iter]
			timestamp = int(item[0])
			mid = [float(price) for price in item[1].split('|')]
			mid = (mid[0]+mid[1])/2 if len(mid) > 1 else mid[0]
			#print item, timestamp, mid, time_point
			if timestamp <= time_point:
				average = float(price_sum)/float(buffer_iter)
				trend.append((time_point, (self.memory.mid-average)/float(average)))
				#print int(time.time())-time_point, average, '|', self.buffer.mid
				interval *= config.INTERVAL_GROW_FACTOR
				time_point -= interval
			price_sum += mid

		logger.debug(str([(int(time.time()-a), b) for (a, b) in trend]))

	def get_momentum(self):
		if len(self.memory.first_order) < max(config.MOMENTUM_LR_RANGE):
			logger.debug('first_order array ('+str(len(self.memory.first_order))+'/'+str(max(config.MOMENTUM_LR_RANGE))+') not ready yet, later')
			return None
		momentum = []
		for lr_range in config.MOMENTUM_LR_RANGE:
			lr_range = lr_range/config.WATCH_INTERVAL
			y = list(itertools.islice(self.memory.first_order, 0, lr_range))
			x = range(1, lr_range+1)
			x = np.asarray(x).reshape(-1,1)
			y = np.asarray(y).reshape(-1,1)
			lr = LR()
			lr.fit(x,y)
			momentum.append(lr.predict(0)[0][0])
		logger.debug('momentums: '+str(momentum))
		return sum(momentum)/float(len(momentum))

	def decide_buy(self, trend, momentum):
		return -1

	def decide_sell(self, trend):
		return -1

	def start_thinking(self):
		while True:
			time.sleep(config.THINK_INTERVAL)
			trend = self.get_trend()
			momentum = self.get_momentum()

			buy_amount = self.decide_buy(trend, momentum)
			if buy_amount > config.MIN_TRADE_AMOUNT:
				self.hand.buy(self.buffer.ask, jpy=buy_amount)

			sell_amount = self.decide_sell(trend)
			if sell_amount > config.MIN_TRADE_AMOUNT:
				self.hand.sell(self.buffer.bid, jpy=sell_amount)
