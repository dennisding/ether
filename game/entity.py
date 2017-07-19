# -*- coding:utf-8 -*-

from . import clients
from . import entity_tools

from utils import swallow
from utils import entity_utils

class LocalEntity(metaclass = entity_utils.EntityMeta):
	gateid = None
	cid = None

	all_clients = swallow.swallow()
	own_client = swallow.swallow()
	other_clients = swallow.swallow()

	def __init__(self):
		pass

	def set_client(self, gateid, cid):
		print('set client!', gateid, cid)

		self.gateid = gateid
		self.cid = cid

		if not (self.gateid and self.cid):
			return
		# create the client entity
		entity_tools.create_player_client(self)

		# setup clients
		self.own_client = clients.OwnClient(self)
		self.all_clients = clients.AllClients(self)
		self.other_client = clients.OtherClients(self)

		# become player
		self.own_client.become_player()

class Entity(LocalEntity):
	def __init__(self):
		pass
