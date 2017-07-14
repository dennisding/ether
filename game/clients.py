# -*- coding:utf-8 -*-

class ClientBase:
	def __init__(self, owner):
		self.owner = owner

	def __getattr__(self, name):
		def _fun(self, *args, **kwds):
			data = self.type_infos.protocol.pack(name, *args, **kwds)
			self._do_send(data)

		return _fun

	def _do_send(self, data):
		raise NotImplemented('client _do_send not implemented')

class OwnClient:
	def __init__(self, owner):
		super().__init__(owner)

	def _do_send(self, data):
		pass

class AllClients:
	def __init__(self, owner):
		super().__init__(owner)

	def _do_send(self, data):
		pass

class OtherClients:
	def __init__(self, owner):
		super().__init__(owner)

	def _do_send(self, data):
		pass