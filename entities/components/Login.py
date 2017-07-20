# -*- encoding:utf-8 -*-

class Login:
	def __init__(self):
		pass

	def login(self, name, password):

		return name == password

#		doc = db.find(name = 'dennis')
#
#		if doc:
#			self.login_reply(True)

def find(doc = {}, **kwds):
	doc = dict(doc)
	doc.update(kwds)

	dispatcher = engine.server().dispatcher

	# 1. send db request (need a token)
	# 2. switch out and wait db return(need current)

	token = dispatcher.gen_token()
	db_server.send_db_request(token, doc)

	return dispatcher.wait_for(token)

def on_db_return(token, doc):
	dispatcher.satisfy(token, doc)
