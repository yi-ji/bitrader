from utils import logger

class Hand:
	def __init__(self, _driver):
		self.driver = _driver

	def buy(self, price, eth=None, jpy=None):
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
		eth_buy_confirm = self.driver.find_element_by_id('doExecBuy')
		eth_buy_confirm.click()

	def sell(self, price, eth=None, jpy=None):
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
		eth_sell_confirm = self.driver.find_element_by_id('doExecSell')
		eth_sell_confirm.click()