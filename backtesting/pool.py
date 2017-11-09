from utils import logger


class Pool:

    def __init__(self, jpy, eth):
        self.jpy = jpy  # type: double
        self.eth = eth  # type: double

    def operate(self, jpy, eth, time):
        logger.info('operating: '
                    + 'jpy ' + self.jpy + ' -> ' + (self.jpy + jpy) + '(' + jpy + ')\t'
                    + 'eth ' + self.eth + ' -> ' + (self.eth + eth) + '(' + eth + ')\t'
                    + time.strftime('%b %d, %Y %H:%M:%S'))
        self.jpy += jpy
        self.eth += eth
