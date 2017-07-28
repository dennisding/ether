# -*- coding:utf-8 -*-

import engine

class ClientBase:
	def __init__(self, owner):
		self.owner = owner

	def __getattr__(self, name):
		def _fun(*args, **kwds):
			data = self.owner.type_infos.client_service.pack(name, *args, **kwds)
			self._do_send(data)

		return _fun

	def _do_send(self, data):
		raise NotImplemented('client _do_send not implemented')

class OwnClient(ClientBase):
	def __init__(self, owner):
		super().__init__(owner)

	def _do_send(self, data):
		owner = self.owner
		gate = engine.server().get_gate(owner.stub.gateid)

		gate.remote.client_msg(owner.stub.cid, owner.eid, data)

class AllClients(ClientBase):
	def __init__(self, owner):
		super().__init__(owner)

	def _do_send(self, data):
		pass

class OtherClients(ClientBase):
	def __init__(self, owner):
		super().__init__(owner)

	def _do_send(self, data):
		pass