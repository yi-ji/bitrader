import brain
import leveldb
import config
from memory import Memory
from backtesting.testhand import Hand
from backtesting.pool import Pool

def main():
    price_db = leveldb.LevelDB(config.PRICE_DB)
    trade_db = leveldb.LevelDB(config.TRADE_DB)

    price_memory = Memory(price_db, trade_db)  # price data of latest period, multiple frequency and period length maybe
    pool = Pool(100000, 0)
    my_hand = Hand(pool)
    my_brain = brain.Brain(price_memory, my_hand)



