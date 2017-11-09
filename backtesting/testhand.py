from utils import logger
from backtesting.pool import Pool


class Hand:

    def __init__(self, pool):
        self.pool = pool  # type: Pool

    def buy(self, price, jpy, time):
        detail = ' price: ' + str(price) + ', ' + str(jpy) + ' JPY '
        logger.info('buying with' + detail)
        eth_count = float(jpy) / float(price)
        self.pool.operate(jpy=-jpy, eth=eth_count, time=time)

    def sell(self, price, jpy, time):
        detail = ' price: ' + str(price) + ', ' + str(jpy) + ' JPY '
        logger.info('selling with' + detail)
        eth_count = float(jpy) / float(price)
        self.pool.operate(jpy=jpy, eth=-eth_count, time=time)

