import leveldb
from config import logger
import time
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

class Eye:
	def __init__(self, _price_buffer, _driver):
		self.buffer = _price_buffer
		self.driver = _driver

	def get_eth_price(self, Ask_or_Bid):
		return self.driver.find_element_by_css_selector('strong.bfPrice'+Ask_or_Bid).text.replace(',','')

	def start_watching(self):
		while True:
			time.sleep(1)
			logger.debug('Ask: ' + self.get_eth_price('Ask') + ' Bid: ' + self.get_eth_price('Bid'))
