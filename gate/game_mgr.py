# -*- coding:utf-8 -*-

import random
import engine

from network import server
from network import service

from protocols import gate_to_game
from protocols import game_to_gate

class Connection:
	def __init__(self):
		pass

	def connection_made(self):
		print('game connection made')

	def connection_lost(self):
		print('game connection lost')

	def connection_ready(self):
		print('game connection ready')

class GameMgr:
	def __init__(self):
		self.games = {} # {gid: cid}

	def serve(self):
		gate_service = service.gen_service(game_to_gate.GameToGate())
		game_service = service.gen_service(gate_to_game.GateToGame())

		config = engine.config()
		self.server = server.Server(Connection, config['net_option'], \
								game_service, gate_service)

		self.server.start(config['gport'])

	def get_free_game(self):
		games = list(self.server.connections.values())
		return random.choice(games)

	def get_game(self, gid):
		cid = self.games[gid]

		return self.server.get_connection(cid)
