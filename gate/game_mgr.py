# -*- coding:utf-8 -*-

import random
import engine

from network import server
from network import service

from protocols import gate_to_game
from protocols import game_to_gate

class Connection:
	def __init__(self):
		self.gameid = None

	def connection_made(self):
		print('game connection made')

	def connection_lost(self):
		print('game connection lost')

	def connection_ready(self):
		print('game connection ready')

	def game_server_ready(self, gameid):
		self.gameid = gameid
		engine.server().game_mgr.game_ready(gameid, self.cid)

	def create_player_client(self, cid, eid, name):
		print('create client entity', cid, eid, name, self.gameid)

		client = engine.server().get_client(cid)
		client.remote.create_player_client(eid, name)

		engine.server().on_entity_created(eid, cid, self.gameid)

	def client_msg(self, cid, eid, data):
		client = engine.server().get_client(cid)
		client.remote.client_msg(eid, data)

	def entity_msg_return(self, cid, eid, token, data):
		client = engine.server().get_client(cid)

		client.remote.entity_msg_return(eid, token, data)

class GameMgr:
	def __init__(self):
		self.games = {} # {gid: cid}

	def game_ready(self, gameid, cid):
		self.games[gameid] = cid

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

	def get_game(self, gameid):
		cid = self.games[gameid]

		return self.server.get_connection(cid)
