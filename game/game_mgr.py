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
		print('game connection made')

	def connection_lost(self):
		print('game connection lost')

	def connection_ready(self):
		print('game connection ready')

	def create_stub_proxy(self, eid, name, gameid):
		engine.stubs.create_proxy(eid, name, gameid)

	def entity_msg(self, eid, data):
		entity = engine.get_entity(eid)
		assert entity != None

		name, args = entity.type_infos.server_service.unpack(data)

		engine.scheduler().schedule(eid, getattr(entity, name), args)

	def entity_msg_with_return(self, eid, token, data):
		entity = engine.get_entity(eid)

		assert entity != None

		name, args = entity.type_infos.server_service.unpack(data)
		protocol = entity.type_infos.server_service.get_protocol_by_name(name)

		def _task():
			value = getattr(entity, name)(*args)

			data = protocol.pack_return(value)
			self.remote.entity_msg_return(token, data)

		engine.scheduler().schedule(eid, _task)

	def entity_msg_return(self, token, data):
		engine.server().scheduler.satisfy(token, data)

class AllGame:
	def __init__(self, game_mgr):
		self.game_mgr = game_mgr

	def __getattr__(self, name):
		def _fun(*args, **kwds):
			self.game_mgr.send_to_all_game(name, *args, **kwds)

		return _fun

class GameMgr:
	def __init__(self):
		self.games = {} # {gameid:game}

	def gen_all_game(self):
		return AllGame(self)

	def start_game_service(self):
		self.game_service = service.gen_service(game_to_game.GameToGame())

		config = engine.config()

		self.server = server.Server(Connection, \
							config['net_option'], self.game_service, self.game_service)

		self.server.start(config['gport'])

	def get_game(self, gid):
		return self.games[gid]

	def connect_games(self):
		configs = engine.config()

		self_gid = engine.gid()
		active_games = configs['active_games']

		for config in active_games:
			if config['gid'] == self_gid:
				continue

			self.connect(config)

		if len(active_games) == 1:
			self.all_game_connected()

	def connect(self, config):
		game_service = service.gen_service(game_to_game.GameToGame())

		c = client.Client(Connection(), \
							config['net_option'], game_service, game_service)

		def _connect_callback(connected):
			gid = config['gid']
			if not connected:
				print('connect game failed!, gid[%d]', gid)
				return

			self.games[gid] = c

			# exclude self
			if len(self.games) + 1 == len(engine.config()['active_games']):
				self.all_game_connected()


		c.connect(config['ip'], config['gport'], _connect_callback)

	def all_game_connected(self):
		print('all games connected!')
		# create all stubs
		engine.stubs.create_all_stubs()

	def create_stubs(self):
		engine.stubs.create_all_stubs()

	def send_to_all_game(self, name, *args, **kwds):
		data = self.game_service.pack(name, *args, **kwds)
		for game in self.games.values():
			game.raw_send(data)
