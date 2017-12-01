import eye, brain, hand, memory, config
from utils import logger
import time, leveldb
from selenium import webdriver

driver = webdriver.PhantomJS(executable_path=config.PHANTOM_BIN)

def me():
    price_db = leveldb.LevelDB(config.PRICE_DB)
    trade_db = leveldb.LevelDB(config.TRADE_DB)

    my_memory = memory.Memory(price_db, trade_db, int(time.time()))  # price data of latest period, multiple frequency and period length maybe

    my_hand = hand.Hand(driver)
    my_eye = eye.Eye(my_memory, driver)
    my_brain = brain.Brain(my_memory, my_hand)

    my_eye.start_watching()  # thread. collect data from website, put into (i) leveldb for future use; (ii) into buffer for brain to think about.
    my_brain.start_thinking()  # read price data from buffer, send trading commands to hand.

me()
