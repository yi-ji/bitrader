import eye, brain, hand, config
from utils import logger
import time, leveldb
from selenium import webdriver
from memory import Memory

driver = webdriver.PhantomJS(executable_path=config.PHANTOM_BIN)

def main():
    price_db = leveldb.LevelDB(config.PRICE_DB)
    trade_db = leveldb.LevelDB(config.TRADE_DB)

    price_memory = Memory(price_db, trade_db, int(time.time()))  # price data of latest period, multiple frequency and period length maybe

    my_hand = hand.Hand(driver)
    my_eye = eye.Eye(price_memory, driver)
    my_brain = brain.Brain(price_memory, my_hand)

    my_eye.start_watching()  # thread. collect data from website, put into (i) leveldb for future use; (ii) into buffer for brain to think about.
    my_brain.start_thinking()  # read price data from buffer, send trading commands to hand.

main()

