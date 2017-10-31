import eye, brain, hand, config
from config import logger
import collections, time
from selenium import webdriver

class PriceBuffer:
	def __init__(self):
		self.buffer = collections.deque(config.PRICE_BUFFER_SIZE*[], config.PRICE_BUFFER_SIZE)

def init_web_driver(driver):
	driver.set_window_size(1280, 1024)
	logger.debug('opening login page')
	driver.get('https://bitflyer.jp/en-jp/ex/EthPrice')
	#driver.save_screenshot('phantom/screen1.png')
	email = driver.find_element_by_id('MainContent_email')
	email.send_keys(config.USERNAME)
	passwd = driver.find_element_by_id('MainContent_password')
	passwd.send_keys(config.PASSWORD)
	login = driver.find_element_by_id('MainContent_Button1')
	logger.debug('ready for login')
	login.click()
	#time.sleep(3)
	#driver.save_screenshot('phantom/screen2.png')
	driver.get('https://bitflyer.jp/en-jp/ex/EthPrice')
	logger.debug('go to eth price page')
	time.sleep(3)
	#driver.save_screenshot('phantom/screen3.png')


price_buffer = PriceBuffer() # price data of latest period, multiple frequency and period length maybe

driver = webdriver.PhantomJS(executable_path=config.PHANTOM_BIN)
init_web_driver(driver)

my_hand = hand.Hand(driver)
my_eye = eye.Eye(price_buffer, driver)
my_brain = brain.Brain(price_buffer, my_hand)

my_eye.start_watching() # thread. collect data from website, put into (i) leveldb for future use; (ii) into buffer for brain to think about.
my_brain.start_thinking() # read price data from buffer, send trading commands to hand.

