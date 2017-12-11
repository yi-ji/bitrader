import config
from utils import logger
import time, threading, sys, signal
from selenium.common.exceptions import NoSuchElementException


class Eye:
    def __init__(self, _memory, _driver):
        self.memory = _memory
        self.driver = _driver
        self.closed_retry = 0

    def refresh_driver(self):
        logger.debug('opening login page')
        self.driver.get('https://bitflyer.jp/login')
        email = self.driver.find_element_by_id('MainContent_email')
        email.send_keys(config.USERNAME)
        passwd = self.driver.find_element_by_id('MainContent_password')
        passwd.send_keys(config.PASSWORD)
        login = self.driver.find_element_by_id('MainContent_Button1')
        logger.debug('ready for login')
        login.click()
        self.driver.get('https://bitflyer.jp/en-jp/ex/EthPrice')
        logger.debug('go to eth price page')
        time.sleep(5)

    def init_driver(self):
        def signal_handler(signal, frame):
            logger.debug('Terminating PhantomJS before exit')
            self.driver.quit()
            sys.exit(0)
        signal.signal(signal.SIGINT, signal_handler)
        self.driver.set_window_size(1280, 1024)
        self.refresh_driver()

    def get_eth_price(self, Ask_or_Bid):
        return self.driver.find_element_by_css_selector('strong.bfPrice' + Ask_or_Bid).text.replace(',', '')

    def get_balance_jpy(self):
        return self.driver.find_element_by_id('JPYAmount').text.split(' ')[0].replace(',', '')

    def get_balance_eth(self):
        return self.driver.find_element_by_id('ETHAmount_pw').text

    def start_watching(self):
        self.init_driver()
        time.sleep(5)
        threading.Thread(target=self.watch).start()

    def watch(self):
        while True:
            try:
                ask_price = self.get_eth_price('Ask')
                bid_price = self.get_eth_price('Bid')
                if ask_price == 'CLOSED' or bid_price == 'CLOSED':
                    logger.debug('showing CLOSED')
                    self.closed_retry += 1
                    if self.closed_retry > 10:
                        self.driver.save_screenshot('closed.png')
                        logger.info('showing CLOSED, refresh web driver')
                        self.refresh_driver()
                        self.closed_retry = 0
                    time.sleep(1)
                    continue
                balance_eth = self.get_balance_eth()
                balance_jpy = self.get_balance_jpy()
                self.memory.update(ask_price, bid_price, balance_eth, balance_jpy, int(time.time()))
                time.sleep(config.WATCH_INTERVAL)
                logger.debug('Ask: ' + ask_price + ' Bid: ' + bid_price + ' ETH: ' + balance_eth + ' JPY: ' + balance_jpy)
            except NoSuchElementException:
                self.driver.save_screenshot('NoSuchElementException.png')
                logger.error('NoSuchElementException, refresh web driver')
                self.refresh_driver()
