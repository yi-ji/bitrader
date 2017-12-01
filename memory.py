import collections
import time
import sys
import config, utils
from utils import logger


class Memory:
    def __init__(self, _price_db, _trade_db, timestamp):
        self.price_db = _price_db
        self.trade_db = _trade_db
        self.buffer = collections.deque([], config.PRICE_BUFFER_SIZE)
        self.cache = collections.deque([], config.PRICE_CACHE_SIZE)
        self.first_order = collections.deque([], config.PRICE_CACHE_SIZE)
        self.mid = None
        self.ask = None
        self.bid = None
        self.balance_eth = None
        self.balance_jpy = None
        self.record_timestamp = None
        self.retrospect_price(config.DAY0_TIMESTAMP, timestamp)
        self.history_trade_avg = self.retrospect_trade(config.DAY0_TIMESTAMP, timestamp)

    def print_state(self):
        buffer_state = 'buffer: '+str(len(self.buffer))+'/'+str(config.PRICE_BUFFER_SIZE)
        cache_state = 'cache: '+str(len(self.cache))+'/'+str(config.PRICE_CACHE_SIZE)
        first_order_state = 'first_order: '+str(len(self.first_order))+'/'+str(config.PRICE_CACHE_SIZE)
        logger.debug(', '.join([buffer_state, cache_state, first_order_state]))

    def update(self, ask_price, bid_price, balance_eth, balance_jpy, timestamp):
        self.balance_jpy, self.balance_eth = int(balance_jpy), float(balance_eth)
        self.ask, self.bid = int(ask_price), int(bid_price)
        self.mid = (self.ask + self.bid) / 2
        if self.cache:
            self.first_order.appendleft(self.mid - self.cache[0])
        self.cache.appendleft(self.mid)
        if self.record_timestamp is None or timestamp - self.record_timestamp > config.RECORD_INTERVAL:
            self.record_timestamp = timestamp
            self.price_db.Put(str(timestamp), str(self.ask) + '|' + str(self.bid))
            self.buffer.appendleft((str(timestamp), str(self.ask) + '|' + str(self.bid)))
        self.print_state()

    def retrospect_trade(self, time_from, time_to):
        history_trade = list(self.trade_db.RangeIter(key_from=str(time_from), key_to=str(time_to)))
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

    def memorize_trade(self, price, amount, timestamp):
        self.trade_db.Put(str(timestamp), str(int(price)) + '|' + str(int(amount)))
        self.history_trade_avg = self.retrospect_trade(config.DAY0_TIMESTAMP, timestamp)

    def retrospect_price(self, time_from, time_to): # time_from -> time_to = past -> now
        interval = 36000
        while True:
            timestamp = time_to - interval
            interval *= 2
            #if timestamp < time_from:
            #    logger.error('not enough history data to prefill the buffer, exit')
            #    sys.exit(0)
            logger.debug('try to prefill data from timestamp ' + str(timestamp) + ' to ' + str(time_to))
            past_data = list(self.price_db.RangeIter(key_from=str(timestamp), key_to=str(time_to)))
            if len(past_data) >= config.PRICE_BUFFER_SIZE or timestamp < time_from:
                for ele in past_data[len(past_data) - config.PRICE_BUFFER_SIZE:]:
                    if ele[1] != 'CLOSED|CLOSED':
                        self.buffer.appendleft(ele)
                        ele_mid = utils.kv2mid(ele)
                        if self.cache:
                            self.first_order.appendleft(ele_mid - self.cache[0])
                        self.cache.appendleft(ele_mid)
                break
        logger.debug('price buffer prefilled with past data')
