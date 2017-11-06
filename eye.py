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
	def __init__(self, _memory, _driver):
		self.memory = _memory
		self.driver = _driver

	def get_eth_price(self, Ask_or_Bid):
		return self.driver.find_element_by_css_selector('strong.bfPrice'+Ask_or_Bid).text.replace(',', '')

	def get_balance(self):
		return self.driver.find_element_by_id('JPYAmount').text.split(' ')[0].replace(',', '')

	def start_watching(self):
		time.sleep(5)
		threading.Thread(target=self.watch).start()
			
	def watch(self):
		while True:
			ask_price = self.get_eth_price('Ask')
			bid_price = self.get_eth_price('Bid')
			if ask_price == 'CLOSED' or bid_price == 'CLOSED':
				time.sleep(1)
				continue
			self.memory.update(ask_price, bid_price)
			time.sleep(config.WATCH_INTERVAL)
			logger.debug('Ask: ' + ask_price + ' Bid: ' + bid_price)
