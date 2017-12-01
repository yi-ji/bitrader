import config, utils
import time, math
import itertools
from utils import logger
from sklearn.linear_model import LinearRegression as LR
import numpy as np


class Brain:
    def __init__(self, _memory, _my_hand):
        self.memory = _memory
        self.hand = _my_hand

    def get_trend(self, now_time):
        trend = []

        interval = config.INDICATER_INETRVAL_INIT
        time_point = now_time - interval
        price_sum = 0

        buffer_len = len(self.memory.buffer)
        for buffer_iter in range(0, buffer_len):
            item = self.memory.buffer[buffer_iter]
            timestamp = int(item[0])
            mid = utils.kv2mid(item)
            # print item, timestamp, mid, time_point
            if timestamp <= time_point:
                average = float(price_sum) / float(buffer_iter)
                trend.append((time_point, (self.memory.mid - average) / float(average)))
                # print now_time-time_point, average, '|', self.buffer.mid
                interval *= config.INTERVAL_GROW_FACTOR
                time_point -= interval
            price_sum += mid
        logger.debug('trend: ' + str([(int(now_time - a), b) for (a, b) in trend]))
        return trend

    def get_momentum(self):
        if len(self.memory.first_order) < max(config.MOMENTUM_LR_RANGE):
            logger.debug('first_order array (' + str(len(self.memory.first_order)) + '/' + str(
                max(config.MOMENTUM_LR_RANGE)) + ') not ready yet, later')
            return None
        momentum = []
        for lr_range in config.MOMENTUM_LR_RANGE:
            lr_range = lr_range / config.WATCH_INTERVAL
            y = list(itertools.islice(self.memory.first_order, 0, lr_range))
            x = range(1, lr_range + 1)
            x = np.asarray(x).reshape(-1, 1)
            y = np.asarray(y).reshape(-1, 1)
            lr = LR()
            lr.fit(x, y)
            momentum.append(lr.predict(0)[0][0])
        logger.debug('momentums: ' + str(momentum))
        return momentum

    def decide_trade(self, trend, momentum):
        trend_avg = sum([float(b) for (a, b) in trend]) / float(len(trend))
        momentum_avg = float(sum(momentum)) / float(len(momentum))
        trade_amount = config.TRADE_AMOUNT_BASE * (-trend_avg)
        delta = min(abs(trade_amount), config.DAMP_COEF * momentum_avg * momentum_avg)
        trade_amount = trade_amount - delta if trade_amount >= 0 else trade_amount + delta
        if trade_amount > 0:
            trade_amount *= min(1, math.sqrt(float(self.memory.balance_jpy)/float(self.memory.balance_eth*self.memory.ask)))
        else:
            trade_amount *= min(1, math.sqrt(float(self.memory.balance_eth*self.memory.bid)/float(self.memory.balance_jpy)))
        logger.debug('proposed trading amount: ' + str(int(trade_amount)))
        return int(trade_amount)

    def think(self, timestamp):
        trend = self.get_trend(timestamp)
        momentum = self.get_momentum()

        if len(trend) >= config.MIN_TREND_LEN and len(momentum) >= len(config.MOMENTUM_LR_RANGE):
            history_buy_avg, history_sell_avg = self.memory.history_trade_avg
            trade_amount = self.decide_trade(trend, momentum)
            if trade_amount > config.MIN_TRADE_AMOUNT and self.memory.ask < history_sell_avg:
                logger.debug('history_sell_avg: '+str(history_sell_avg))
                if self.hand.buy(self.memory.ask, jpy=trade_amount):
                    self.memory.memorize_trade(self.memory.ask, trade_amount, timestamp)
            if trade_amount < -config.MIN_TRADE_AMOUNT and self.memory.bid > history_buy_avg:
                logger.debug('history_buy_avg: '+str(history_buy_avg))
                if self.hand.sell(self.memory.bid, jpy=-trade_amount):
                    self.memory.memorize_trade(self.memory.bid, trade_amount, timestamp)

    def start_thinking(self):
        while True:
            time.sleep(config.THINK_INTERVAL)
            self.think(int(time.time()))
