###author: Spurthi Amba Hombaiah
###Queue implementation using lists

class Queue:
	def __init__(self, lang):
		self.queue = []
		self.size = 0
		self.lang = lang

	def add_element(self, val):
		self.queue.append(val)
		self.size += 1

	def pop_element(self):
		if self.size > 0:
			self.size -= 1
			ele = self.queue.pop(0)
			return ele
		return