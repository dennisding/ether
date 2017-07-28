# -*- coding:utf-8 -*-

import engine

from network import client
from network import service

from protocols import gate_to_game
from protocols import game_to_gate

class Connection:
	def __init__(self, gate_mgr, gid):
		self.gate_mgr = gate_mgr
		self.gid = gid

	def connection_made(self):
		print(self.gid, 'gate connection made')

	def connection_lost(self):
		print(self.gid, 'gate connection lost')

	def connection_ready(self):
		print(self.gid, 'gate connection ready')
		self.gate_mgr.gate_ready(self.gid)

		self.remote.game_server_ready(self.gid)

	def client_connected(self, gateid, cid):
		# 1. create entity
		# 2. bind the entity to client
		print('client connected!!!', gateid, cid)
		entity_mgr = engine.server().entity_mgr

		connect_entity = engine.game_config()['connect_entity']
		eid = entity_mgr.create_entity(connect_entity)

		entity = entity_mgr.get_entity(eid)
		entity.set_client(gateid, cid)

	def entity_msg(self, eid, data):
		server = engine.server()
		entity_mgr = server.entity_mgr

		entity = entity_mgr.get_entity(eid)
		name, args = entity.type_infos.server_service.unpack(data)

		server.scheduler.schedule(eid, getattr(entity, name), args)

	def entity_msg_with_return(self, eid, token, data):
		server = engine.server()
		entity_mgr = server.entity_mgr

		entity = entity_mgr.get_entity(eid)
		name, args = entity.type_infos.server_service.unpack(data)

		def _task():
			# pack the return
			entity = entity_mgr.get_entity(eid)
			if not entity:
				return

			result = getattr(entity, name)(*args)

			data = entity.type_infos.server_service.pack_return(name, result)

			gate = engine.server().get_gate(entity.stub.gateid)
			gate.remote.entity_msg_return(entity.stub.cid, eid, token, data)

		server.scheduler.schedule(eid, _task)

class GateMgr:
	def __init__(self):
		self.clients = {} # { gid: connection }
		self.connecting = {} # {gid : client}

	def gate_ready(self, gid):
		client = self.connecting.pop(gid)
		self.clients[gid] = client

	def get_gate(self, gid):
		return self.clients[gid]

	def connect_gates(self):
		gate_service = service.gen_service(game_to_gate.GameToGate())
		game_service = service.gen_service(gate_to_game.GateToGame())

		config = engine.config()

		for gate in config['active_gates']:
			c = client.Client(Connection(self, gate['gid']), \
								config['net_option'], gate_service, game_service)

			self.connecting[gate['gid']] = c
			c.connect(gate['ip'], gate['gport'])
