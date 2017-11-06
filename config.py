import math, time

PRICE_BUFFER_SIZE = 86400
PRICE_CACHE_SIZE = 300

RECORD_INTERVAL = 10 # second(s)
WATCH_INTERVAL = 2 # second(s)
THINK_INTERVAL = 5 # second(s)

MOMENTUM_LR_RANGE = [10, 30, 60, 180] # seconds

DEBUG = True

USERNAME = 'jiyi0327@gmail.com'
PASSWORD = 'no can tell'

PHANTOM_BIN = './phantom/phantomjs'
LEVEL_DB = './data/price-db'
PRICE_FILE = './data/ETH_JPY.json'

TRADE_RETRY_MAX = 5

INDICATERS = [(3600.0, 0.15),
			  (28*24*3600.0, 0.05)]
INDICATER_INETRVAL_INIT = 3600
INTERVAL_GROW_FACTOR = 2

# function: y = Ax^B

coef_B = math.log( INDICATERS[0][1]/INDICATERS[1][1], INDICATERS[0][0]/INDICATERS[1][0] )
coef_A = INDICATERS[0][1] / math.pow(INDICATERS[0][0], coef_B)

MIN_TRADE_AMOUNT = 40000

def threshold(timestamp):
	x = time.time() - int(timestamp)
	return coef_A * math.pow(x, coef_B)
