# -*- coding:utf-8 -*-

import engine

from network import server
from network import service

from protocols import client_to_gate
from protocols import gate_to_client

class Connection:
	def __init__(self):
		pass

	def connection_made(self):
		print('client connectin made')

	def connection_lost(self):
		print('client connection lost')

	def connection_ready(self):
		print('client connection ready')
		# 1. pick a free game
		# 2. send client connected msg
		server = engine.server()

		game = server.game_mgr.get_free_game()
		game.remote.client_connected(server.gid, self.cid)

	def create_client_entity(self, eid, name):
		print('create client entity', eid)

class ClientMgr:
	def __init__(self):
		pass

	def serve(self):
		client_service = service.gen_service(gate_to_client.GateToClient())
		gate_service = service.gen_service(client_to_gate.ClientToGate())

		config = engine.config()
		self.server = server.Server(Connection, \
							config['net_option'], client_service, gate_service)

		self.server.start(config['cport'])

	def get_client(self, cid):
		return self.server.get_connection(cid)
