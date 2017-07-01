# -*- encoding:utf-8 -*-

import engine
import random
import asyncio

from network import client
from network import service

from protocols import client_to_gate
from protocols import gate_to_client

class Connection:
	def __init__(self):
		pass

	def connection_made(self):
		print('connection made')

	def connection_lost(self):
		print('connection lost')

	def connection_ready(self):
		print('connection ready')

class Client:
	def __init__(self):
		pass

	def connect_to_gate(self):
		client_service = service.gen_service(gate_to_client.GateToClient())
		gate_service = service.gen_service(client_to_gate.ClientToGate())

		config = engine.config()
		self.client = client.Client(Connection(), \
						config['net_option'], gate_service, client_service)

		gate = random.choice(config['active_gates'])
		# connect to gate 1
		self.client.connect(gate['ip'], gate['cport'])

	def run_forever(self):
		loop = asyncio.get_event_loop()
		loop.run_forever()

	def start(self):
		self.connect_to_gate()
		self.run_forever()
