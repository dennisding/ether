# -*- encoding:utf-8 -*-

import engine

class Login:
#	def __init__(self):
#		pass

	def login(self, name, password):

#		avatar = self.create_avatar(name)

		if engine.stubs.OnlineStub.is_online(name):
			print('login is online!')
			return False

#		avatar = self.create_avatar(name)

		if name == password:
			engine.stubs.OnlineStub.set_online(name)
			return True
		else:
			return False

	def transfer_client_to(self, entity):
		if not self._has_client():
			return

#		doc = db.find(name = 'dennis')
#
#		if doc:
#			self.login_reply(True)

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
