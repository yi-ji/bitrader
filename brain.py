import config
import time

class Brain:
	def __init__(self, _price_buffer, _my_hand):
		self.buffer = _price_buffer
		self.hand = _my_hand

	def start_thinking(self):
		while True:
			time.sleep(config.THINK_INTERVAL)
			ele = self.buffer.buffer.pop()
			print(ele)
