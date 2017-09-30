# -*- encoding:utf-8 -*-

import engine

from utils import swallow
from utils import entity_utils

#class Server:
#	def __init__(self, owner):
#		self.owner = owner
#
#	def __getattr__(self, name):
#		owner = self.owner
#
#		def _fun(*args, **kwds):
#			protocol = owner.type_infos.server_service.get_protocol_by_name(name)
#			data = protocol.pack(*args, **kwds)
#			client = engine.client()
#			if protocol.has_return():
#				token = client.scheduler.gen_token()
#				engine.client().client.remote.entity_msg_with_return(token, data)
#
#				def _filter(data):
#					return protocol.unpack_return(data)
#
#				return client.scheduler.wait_for(token, _filter)
#			else:
#				engine.client().client.remote.entity_msg(data)
#
#		return _fun

class Server:
	def __init__(self, owner):
		self.owner = owner

	def __getattr__(self, name):
		owner = self.owner

		def _fun(*args):
			rpc_info = owner.type_info.get_rpc(name)

			data = rpc_info.pack_args(*args)

			engine.client().entity_msg(data)

		return _fun

class Entity(metaclass = entity_utils.EntityMeta):
	def __init__(self):
		pass

	def on_created(self):
		self.server = Server(self)

	def on_destroyed(self):
		self.__dict__.clear()

