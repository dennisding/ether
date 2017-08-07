# -*- encoding:utf-8 -*-

import sys
import engine
import random
import pathlib
import asyncio

from . import entity

from utils import entity_mgr
from utils import scheduler

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

	def create_player_client(self, eid, name):
		print('create client entity', eid, name)

		entity_mgr = engine.client().entity_mgr
		entity_mgr.create_entity(name, eid = eid)

	def client_msg(self, eid, data):
		client = engine.client()
		entity_mgr = client.entity_mgr

		entity = entity_mgr.get_entity(eid)

		name, args = entity.type_infos.client_service.unpack(data)
#		getattr(entity, name)(*args)

		client.scheduler.schedule(eid, getattr(entity, name), args)

	def entity_msg_return(self, eid, token, data):
		client = engine.client()
		client.scheduler.satisfy(token, data)

class Client:
	def __init__(self):
		engine._client = self
		self.prepare_environment()
		self.setup_entity_mgr()

		self.scheduler = scheduler.Scheduler()

	def prepare_environment(self):
		path = pathlib.Path(engine.game_config()['client_entity_path'])
		sys.path.insert(0, str(path.resolve()))

	def setup_entity_mgr(self):
		self.entity_mgr = entity_mgr.EntityMgr()

		game_config = engine.game_config()
		def_path = game_config['entity_def_path']
		entity_path = game_config['client_entity_path']

		self.entity_mgr.prepare_entities(def_path, entity_path, entity.Entity)

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
