import math
import time

PRICE_BUFFER_SIZE = 200000
PRICE_CACHE_SIZE = 300

RECORD_INTERVAL = 10  # second(s)
WATCH_INTERVAL = 2  # second(s)
THINK_INTERVAL = 5  # second(s)

MOMENTUM_LR_RANGE = [10, 20, 30, 40, 60, 180]  # seconds

DAY0_TIMESTAMP = 1451606400

DEBUG = True

USERNAME = 'jiyi0327@gmail.com'
PASSWORD = 'Never put your password here!!'

PHANTOM_BIN = './phantom/phantomjs'
PRICE_DB = './data/price-db'
TRADE_DB = './data/trade-db'
PRICE_FILE = './data/ETH_JPY.json'

TRADE_RETRY_MAX = 5

INDICATERS = [(3600.0, 0.15),
              (28 * 24 * 3600.0, 0.05)]
INDICATER_INETRVAL_INIT = 60
INTERVAL_GROW_FACTOR = 4

EMAIL = ['jiyi0327@gmail.com']

# function: y = Ax^B

coef_B = math.log(INDICATERS[0][1] / INDICATERS[1][1], INDICATERS[0][0] / INDICATERS[1][0])
coef_A = INDICATERS[0][1] / math.pow(INDICATERS[0][0], coef_B)

MIN_TRADE_AMOUNT = 35000
TRADE_AMOUNT_BASE = 350000
DAMP_COEF = 1000

TREND_LEN = 8

def threshold(timestamp):
    x = time.time() - int(timestamp)
    return coef_A * math.pow(x, coef_B)
