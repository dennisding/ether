# -*- encoding:utf-8 -*-

import greenlet

class Scheduler:
	def __init__(self):
		self.waiting = {} # {token:greenlet}
		self.active_tasks = {} # {eid:set(greenlet)}

		self.last_token = 0

	def gen_token(self):
		self.last_token = self.last_token + 1
		return self.last_token

	def clear(self, eid):
		self.active_tasks.pop(eid, None)

	def schedule(self, eid, task, args = ()):
		g = greenlet.greenlet(task)

		g.switch(*args)

		if not g.dead:
			self.add_active_task(eid, g)

	def wait_for(self, eid, token):
		g = greenlet.getcurrent()
		self.waiting[token] = g, eid

		return g.parent.switch()

	def add_active_task(self, eid, g):
		tasks = self.active_tasks.get(eid)
		if tasks:
			tasks.add(g)
		else:
			self.active_tasks[eid] = {g}

	def satisfy(self, token, data):
		info = self.waiting.pop(token, None)
		if not info: # entity task has been clear, ignore it
			return

		g, eid = info

		g.switch(data)

		if not g.dead:
			self.add_active_task(eid, g)
		else:
			self.active_tasks[eid].remove(g)
