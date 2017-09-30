# -*- encoding:utf-8 -*-

import engine

from common import attr
from common import gtypes

class Package(gtypes.Attribute):
	count = attr.attr(gtypes.Int)

class Login:
	hp = attr.attr(gtypes.Int)
	package = attr.attr(Package)

	def __init__(self):
		self.name = ''

	@rpc.rpc('Int, Int', 'Return', 'options')
	def test3(self, name_id, arg):
		return 0.1

	def login(self, name, password):
		# test code

		if name != password:
			return False

		if not engine.stubs.online.try_set_online(name):
			return False

		return True

	def transfer_client_to(self, entity):
		if not self._has_client():
			return

def find(doc = {}, **kwds):
	doc = dict(doc)
	doc.update(kwds)

	scheduler = engine.server().scheduler

	# 1. send db request (need a token)
	# 2. switch out and wait db return(need current task)

	token = scheduler.gen_token()
	db_server.send_db_request(token, doc)

	return scheduler.wait_for(token)

def on_db_return(token, doc):
	dispatcher.satisfy(token, doc)
