# -*- coding:utf-8 -*-

class Online:
	def __init__(self):
		self.onlines = set()

	def is_online(self, name):
		print('online stubs is online', name, self.onlines)
		return name in self.onlines

	def set_online(self, name):
		print('online stub set online', name)
		self.onlines.add(name)

	def try_set_online(self, name):
		if name in self.onlines:
			return False

		self.onlines.add(name)
		return True
