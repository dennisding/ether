# -*- coding:utf-8 -*-

import greenlet

class Dispatcher:
	def __init__(self):
		self.tasks = []

	def dispatch(self, entity, name, args):
		method = getattr(entity, name)

		g = greenlet.greenlet(method)

		g.switch(*args)

