import collections
import time
import sys
import config
from utils import logger


class Memory:
    def __init__(self, _price_db, _trade_db):
        self.price_db = _price_db
        self.trade_db = _trade_db
        self.buffer = collections.deque([], config.PRICE_BUFFER_SIZE)
        self.cache = collections.deque([], config.PRICE_CACHE_SIZE)
        self.first_order = collections.deque([], config.PRICE_CACHE_SIZE)
        self.mid = None
        self.ask = None
        self.bid = None
        self.record_timestamp = None
        self.retrospect_price()
        self.history_trade_avg = self.retrospect_trade()

    def update(self, ask_price, bid_price):
        self.ask = int(ask_price)
        self.bid = int(bid_price)
        self.mid = (self.ask + self.bid) / 2
        if self.cache:
            self.first_order.appendleft(self.mid - self.cache[0])
        self.cache.appendleft(self.mid)
        timestamp = int(time.time())
        if self.record_timestamp is None or timestamp - self.record_timestamp > config.RECORD_INTERVAL:
            self.record_timestamp = timestamp
            self.price_db.Put(str(timestamp), str(self.ask) + '|' + str(self.bid))
            self.buffer.appendleft((str(timestamp), str(self.ask) + '|' + str(self.bid)))

    def retrospect_trade(self):
        history_trade = list(self.trade_db.RangeIter(key_from=str(config.DAY0_TIMESTAMP), key_to=str(int(time.time()))))
        buy_avg, sell_avg, buy_amount, sell_amount = 0, 0, 0, 0
        for trade in history_trade:
            trade = trade[1].split('|')
            price, amount = int(trade[0]), int(trade[1])
            if amount >= 0:
                buy_avg += price * amount
                buy_amount += amount
            else:
                sell_avg += price * amount
                sell_amount += amount
        buy_avg /= buy_amount
        sell_avg /= sell_amount
        return (buy_avg, sell_avg)

    def memorize_trade(self, price, amount):
        self.trade_db.Put(str(int(time.time())), str(int(price)) + '|' + str(int(amount)))
        self.retrospect_trade()

    def retrospect_price(self):
        now_time = int(time.time())
        interval = 3600
        while True:
            few_time_ago = now_time - interval
            interval *= 2
            if few_time_ago < config.DAY0_TIMESTAMP:
                logger.error('not enough history data to prefill the buffer, exit')
                sys.exit(0)
            logger.debug('try to prefill data from timestamp ' + str(few_time_ago) + ' to ' + str(now_time))
            past_data = list(self.price_db.RangeIter(key_from=str(few_time_ago), key_to=str(now_time)))
            if len(past_data) >= config.PRICE_BUFFER_SIZE / 5:
                for ele in past_data[len(past_data) - config.PRICE_BUFFER_SIZE:]:
                    if ele[1] != 'CLOSED|CLOSED':
                        self.buffer.appendleft(ele)
                break
        logger.debug('price buffer prefilled with past data')
