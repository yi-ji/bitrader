import config
from utils import logger
import time
import threading


class Eye:
    def __init__(self, _memory, _driver):
        self.memory = _memory
        self.driver = _driver

    def get_eth_price(self, Ask_or_Bid):
        return self.driver.find_element_by_css_selector('strong.bfPrice' + Ask_or_Bid).text.replace(',', '')

    def get_balance_jpy(self):
        return self.driver.find_element_by_id('JPYAmount').text.split(' ')[0].replace(',', '')

    def get_balance_eth(self):
        return self.driver.find_element_by_id('ETHAmount_pw').text

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
            balance_eth = self.get_balance_eth()
            balance_jpy = self.get_balance_jpy()
            self.memory.update(ask_price, bid_price, balance_eth, balance_jpy, int(time.time()))
            time.sleep(config.WATCH_INTERVAL)
            logger.debug('Ask: ' + ask_price + ' Bid: ' + bid_price + ' ETH: ' + balance_eth + ' JPY: ' + balance_jpy)
