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

	def login(self, name, password):
		print('login:name = %s, password = %s'%(name, password), name == password)

		self.remote.login(name == password)

class ClientService:
	def __init__(self):
		pass

	def serve(self):
		client_service = service.Service(gate_to_client.GateToClient())
		client_service.build_protocols()

		gate_service = service.Service(client_to_gate.ClientToGate())
		gate_service.build_protocols()

		config = engine.config()
		self.server = server.Server(Connection, config['net_option'], \
							client_service, gate_service)

		self.server.start(config['cport'])
