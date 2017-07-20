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
			protocol = owner.type_infos.server_service.get_protocol_by_name(name)
			data = protocol.pack(*args, **kwds)
			client = engine.client()
			if protocol.has_return():
				token = client.scheduler.gen_token()
				engine.client().client.remote.entity_msg_with_return(token, data )

				return client.scheduler.wait_for(owner.eid, token)
			else:
				engine.client().client.remote.entity_msg(data)

		return _fun

class Entity(metaclass = entity_utils.EntityMeta):
	def __init__(self):
		pass

	def _setup_server(self):
		self.server = Server(self)