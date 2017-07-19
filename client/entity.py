# -*- encoding:utf-8 -*-

import engine

from utils import swallow
from utils import entity_utils

class Server:
	def __init__(self, owner):
		self.owner = owner

	def __getattr__(self, name):
		owner = self.owner

		def _fun(*args, **kwds):
			data = owner.type_infos.server_service.pack(name, *args, **kwds)

			engine.client().client.remote.entity_msg(data)

		return _fun

class Entity(metaclass = entity_utils.EntityMeta):
	def __init__(self):
		pass

	def _setup_server(self):
		self.server = Server(self)