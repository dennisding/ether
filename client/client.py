# -*- encoding:utf-8 -*-

import sys
import engine
import random
import pathlib
import asyncio

from . import entity

from utils import entity_mgr

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

	def create_client_entity(self, eid, name):
		print('create client entity', eid, name)

		entity_mgr = engine.client().entity_mgr
		entity_mgr.create_entity(name, eid = eid)

class Client:
	def __init__(self):
		engine._client = self
		self.prepare_environment()
		self.setup_entity_mgr()

	def prepare_environment(self):
		path = pathlib.Path(engine.game_config()['client_entity_path'])
		sys.path.insert(0, str(path.resolve()))

	def setup_entity_mgr(self):
		self.entity_mgr = entity_mgr.EntityMgr()

		entity_path = engine.game_config()['client_entity_path']
		self.entity_mgr.load_entities(entity_path, entity.Entity)

	def connect_to_gate(self):
		client_service = service.gen_service(gate_to_client.GateToClient())
		gate_service = service.gen_service(client_to_gate.ClientToGate())

		config = engine.config()
		self.client = client.Client(Connection(), \
						config['net_option'], gate_service, client_service)

		gate = random.choice(config['active_gates'])
		# connect to gate 1
		self.client.connect(gate['ip'], gate['cport'])

	def start(self):
		self.connect_to_gate()

		loop = asyncio.get_event_loop()
		loop.run_forever()
