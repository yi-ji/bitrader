from utils import logger
import time
import config
from selenium.common.exceptions import ElementNotVisibleException, TimeoutException
from datetime import datetime
from selenium.webdriver.common.by import By
import selenium.webdriver.support.expected_conditions as EC
import selenium.webdriver.support.ui as ui

class Hand:
	def __init__(self, _driver):
		self.driver = _driver

	def buy(self, price, eth=None, jpy=None):
		detail = ' price: '+str(price)+', amount '+str(eth)+' ether or '+str(jpy)+' JPY '
		logger.info('buying with'+detail)
		if eth is not None:
			self.buy_by_eth(eth)
		elif jpy is not None:
			self.buy_by_eth(float(jpy)/float(price))
		else:
			logger.warn('buying failed, eth and jpy both empty.')
			return
		if self.check_trade_record():
			logger.info('bought with'+detail)
		else:
			logger.warn('buying failed!'+detail)

	def check_trade_record(self):
		records = self.driver.find_elements_by_xpath("//td[@data-prop='exec_date']")
		now_time = int(time.time())
		for record in records:
			if len(record.text) < 2:
				continue
			timestamp = int(time.mktime(datetime.strptime(record.text, '%b %d, %Y %H:%M:%S').timetuple()))
			if now_time - timestamp < 10:
				return True
		return False 

	def buy_by_eth(self, eth):
		eth_input = self.driver.find_element_by_id('MainContent_TextBox1')
		eth_input.send_keys(str(eth))
		eth_buy = self.driver.find_element_by_id('buttonBUY')
		eth_buy.click()
		try:
			eth_buy_confirm = self.driver.find_element_by_id('doExecBuy')
			ui.WebDriverWait(self.driver, 6).until(EC.visibility_of(eth_buy_confirm))
			eth_buy_confirm.click()
			time.sleep(5)
		except TimeoutException:
			logger.debug('waiting for click buy confirm button timeout')

	def sell(self, price, eth=None, jpy=None):
		detail = ' price: '+str(price)+', amount '+str(eth)+' ether or '+str(jpy)+' JPY '
		logger.info('selling with'+detail)
		if eth is not None:
			self.sell_by_eth(eth)
		elif jpy is not None:
			self.sell_by_eth(float(jpy)/float(price))
		else:
			logger.warn('selling failed, eth and jpy both empty.')
			return
		if self.check_trade_record():
			logger.info('sold with'+detail)
		else:
			logger.warn('selling failed!'+detail)

	def sell_by_eth(self, eth):
		eth_input = self.driver.find_element_by_id('MainContent_TextBox1')
		eth_input.send_keys(str(eth))
		eth_sell = self.driver.find_element_by_id('buttonSELL')
		eth_sell.click()
		try:
			eth_sell_confirm = self.driver.find_element_by_id('doExecSell')
			ui.WebDriverWait(self.driver, 6).until(EC.visibility_of(eth_sell_confirm))
			eth_sell_confirm.click()
			time.sleep(5)
		except TimeoutException:
			logger.debug('waiting for click sell confirm button timeout')