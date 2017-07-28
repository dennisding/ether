# -*- coding:utf-8 -*-

from . import clients
from . import entity_tools

from utils import swallow
from utils import entity_utils

class Stub:
	def __init__(self, gateid = 0, cid = 0, gameid = 0):
		self.gateid = gateid
		self.cid = cid
		self.gameid = gameid

	def set_client(self, gateid = 0, cid = 0):
		self.gateid = gateid
		self.cid = cid

	def set_game(self, gameid = 0):
		self.gameid = gameid

class LocalEntity(metaclass = entity_utils.EntityMeta):
	stub = Stub()

	all_clients = swallow.swallow()
	own_client = swallow.swallow()
	other_clients = swallow.swallow()

	def __init__(self):
		pass

	def set_client(self, gateid, cid):
		if not (gateid and cid):
			self.stub.set_client()
			return

		self.stub.set_client(gateid, cid)
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

class Stub(LocalEntity):
	def __init__(self):
		pass
