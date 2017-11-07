from utils import logger
import time
import config
from selenium.common.exceptions import ElementNotVisibleException

class Hand:
	def __init__(self, _driver):
		self.driver = _driver

	def buy(self, price, eth=None, jpy=None):
		logger.info('buying with price: '+str(price)+', amount '+str(eth)+' ether or '+str(jpy)+' JPY')
		if eth is not None:
			self.buy_by_eth(eth)
		elif jpy is not None:
			self.buy_by_eth(float(jpy)/float(price))
		else:
			logger.warn('eth or jpy amount cannot be both empty when buying')
			return

	def buy_by_eth(self, eth):
		eth_input = self.driver.find_element_by_id('MainContent_TextBox1')
		eth_input.send_keys(str(eth))
		eth_buy = self.driver.find_element_by_id('buttonBUY')
		eth_buy.click()
		retry = 1
		while True:
			try:
				time.sleep(1)
				eth_buy_confirm = self.driver.find_element_by_id('doExecBuy')
				eth_buy_confirm.click()
				break
			except ElementNotVisibleException:
				if retry > config.TRADE_RETRY_MAX:
					logger.warn('buying failed too many times, abort')
					return
				logger.debug('buying failed, retry')
				retry += 1
		time.sleep(5)
		logger.info('bought '+str(eth)+' ether')

	def sell(self, price, eth=None, jpy=None):
		logger.info('selling with price: '+str(price)+', amount '+str(eth)+' ether or '+str(jpy)+' JPY')
		if eth is not None:
			self.sell_by_eth(eth)
		elif jpy is not None:
			self.sell_by_eth(float(jpy)/float(price))
		else:
			logger.warn('eth or jpy amount cannot be both empty when selling')
			return

	def sell_by_eth(self, eth):
		eth_input = self.driver.find_element_by_id('MainContent_TextBox1')
		eth_input.send_keys(str(eth))
		eth_sell = self.driver.find_element_by_id('buttonSELL')
		eth_sell.click()
		retry = 1
		while True:
			try:
				time.sleep(1)
				eth_sell_confirm = self.driver.find_element_by_id('buttonSELL')
				eth_sell_confirm.click()
				break
			except ElementNotVisibleException:
				if retry > config.TRADE_RETRY_MAX:
					logger.warn('selling failed too many times, abort')
					return
				logger.debug('selling failed, retry')
				retry += 1
		time.sleep(5)
		logger.info('sold '+str(eth)+' ether')