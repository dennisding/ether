# -*- encoding:utf-8 -*-

import signal
import asyncio

from network import client
from network import service

from protocols import client_to_gate
from protocols import gate_to_client

class Client:
	def __init__(self):
		pass

	def connection_made(self):
		print('connection made')

	def connection_lost(self):
		print('connection lost')

	def connection_ready(self):
		print('connection ready')
		self.remote.login('dennis', 'dennis')

	def login(self, is_ok):
		print('is ok!!!', is_ok)

if __name__ == '__main__':
	signal.signal(signal.SIGINT, signal.SIG_DFL)

	client_service = service.Service(gate_to_client.GateToClient())
	client_service.build_protocols()

	gate_service = service.Service(client_to_gate.ClientToGate())
	gate_service.build_protocols()

	c = client.Client(Client(), 'zip pack big', gate_service, client_service)
	# connect to gate 1
	c.connect('127.0.0.1', 4000)

	loop = asyncio.get_event_loop()
	loop.run_forever()
