# -*- encoding:utf-8 -*-

import greenlet

class Scheduler:
	def __init__(self):
		self.waiting = {} # {token:greenlet}
		self.active_tasks = {} # {eid:set(greenlet)}
		self.current_eid = None

		self.last_token = 0

	def gen_token(self):
		self.last_token = self.last_token + 1
		return self.last_token

	def clear_tasks(self, eid):
		self.active_tasks.pop(eid, None)

	def has_task(self, eid):
		return bool(self.active_tasks.get(eid))

	def schedule(self, eid, task, args = ()):
		self.current_eid = eid or self.current_eid

		g = greenlet.greenlet(task)

		g.switch(*args)

	def wait_for(self, token, filter = None):
		filter = filter or (lambda data:data)
		g = greenlet.getcurrent()
		self.waiting[token] = g, self.current_eid, filter

		if self.current_eid in self.active_tasks:
			tasks = self.active_tasks[self.current_eid]
		else:
			tasks = set()

		tasks.add(g)
		self.active_tasks[self.current_eid] = tasks

		return g.parent.switch()

	def satisfy(self, token, data):
		info = self.waiting.pop(token, None)
		if not info: # entity task has been clear, ignore it
			return

		g, eid, filter = info

		self.current_eid = eid

		if eid in self.active_tasks:
			self.active_tasks[eid].discard(g)

		g.switch(filter(data))
