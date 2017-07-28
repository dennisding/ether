# -*- coding:utf-8 -*-

import engine

from network import server
from network import client
from network import service

from protocols import game_to_game

class Connection:
	def __init__(self):
		pass

	def connection_made(self):
		pass

	def connection_lost(self):
		pass

	def connection_ready(self):
		pass

class GameMgr:
	def __init__(self):
		self.games = {} # {gameid:game}

	def start_game_service(self):
		game_service = service.gen_service(game_to_game.GameToGame())

		config = engine.config()

		self.server = server.Server(Connection, \
							config['net_option'], game_service, game_service)

		self.server.start(config['gport'])

	def get_game(self, gid):
		return self.games[gid]

	def connect_games(self):
		configs = engine.config()

		self_gid = engine.gid()

		for config in configs['active_games']:
			if config['gid'] == self_gid:
				continue

			self.connect(config, configs['net_option'])

	def connect(self, config, net_option):
		game_service = service.gen_service(game_to_game.GameToGame())

		c = client.Client(Connection(), \
							net_option, game_service, game_service)

		c.connect(config['ip'], config['gport'])

		self.clients[config['gid']] = c
