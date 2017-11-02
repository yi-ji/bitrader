import leveldb
import config
from utils import logger
import time, threading, sys
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

class Eye:
	def __init__(self, _price_buffer, _driver):
		self.buffer = _price_buffer
		self.driver = _driver
		self.db = leveldb.LevelDB(config.LEVEL_DB)

	def get_eth_price(self, Ask_or_Bid):
		return self.driver.find_element_by_css_selector('strong.bfPrice'+Ask_or_Bid).text.replace(',', '')

	def get_balance(self):
		return self.driver.find_element_by_id('JPYAmount').text.split(' ')[0].replace(',', '')

	def prefill(self):
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
						self.buffer.buffer.appendleft(ele)
				break
		logger.info('price buffer prefilled with past data')

	def update(self, ask, bid):
		self.buffer.ask = int(ask)
		self.buffer.bid = int(bid)
		self.buffer.mid = (self.buffer.ask+self.buffer.bid)/2

	def start_watching(self):
		threading.Thread(target=self.watch).start()

	def watch(self):
		time.sleep(3)
		while True:
			ask_price = self.get_eth_price('Ask')
			bid_price = self.get_eth_price('Bid')
			if ask_price == 'CLOSED' or bid_price == 'CLOSED':
				time.sleep(1)
				continue
			self.update(ask_price, bid_price)
			timestamp = str(int(time.time()))
			logger.debug('Ask: ' + ask_price + ' Bid: ' + bid_price)
			self.db.Put(timestamp, str(ask_price)+'|'+str(bid_price))
			self.buffer.buffer.appendleft((timestamp, str(ask_price)+'|'+str(bid_price)))
			time.sleep(config.WATCH_INTERVAL)
