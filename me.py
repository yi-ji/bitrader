import eye, brain, hand, config
from utils import logger
import time, sys, signal, leveldb
from selenium import webdriver
from memory import Memory


def signal_handler(signal, frame):
    print('Terminating PhantomJS before exit')
    driver.quit()
    sys.exit(0)


def init_web_driver(driver):
    signal.signal(signal.SIGINT, signal_handler)
    driver.set_window_size(1280, 1024)
    logger.debug('opening login page')
    driver.get('https://bitflyer.jp/en-jp/ex/EthPrice')
    # driver.save_screenshot('phantom/screen1.png')
    email = driver.find_element_by_id('MainContent_email')
    email.send_keys(config.USERNAME)
    passwd = driver.find_element_by_id('MainContent_password')
    passwd.send_keys(config.PASSWORD)
    login = driver.find_element_by_id('MainContent_Button1')
    logger.debug('ready for login')
    login.click()
    # time.sleep(3)
    # driver.save_screenshot('phantom/screen2.png')
    driver.get('https://bitflyer.jp/en-jp/ex/EthPrice')
    logger.debug('go to eth price page')
    time.sleep(3)


# driver.save_screenshot('phantom/screen3.png')

driver = webdriver.PhantomJS(executable_path=config.PHANTOM_BIN)


def main():
    price_db = leveldb.LevelDB(config.PRICE_DB)
    trade_db = leveldb.LevelDB(config.TRADE_DB)

    price_memory = Memory(price_db, trade_db, int(time.time()))  # price data of latest period, multiple frequency and period length maybe

    my_hand = hand.Hand(driver)
    my_eye = eye.Eye(price_memory, driver)
    my_brain = brain.Brain(price_memory, my_hand)

    init_web_driver(driver)

    my_eye.start_watching()  # thread. collect data from website, put into (i) leveldb for future use; (ii) into buffer for brain to think about.
    my_brain.start_thinking()  # read price data from buffer, send trading commands to hand.

main()

