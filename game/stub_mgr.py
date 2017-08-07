# -*- coding:utf-8 -*-

import engine

from game import entity

class Proxy:
	def __init__(self, eid, name, gameid, type_infos):
		self.eid = eid
		self.name = name
		self.gameid = gameid
		self.type_infos = type_infos


	def __getattr__(self, name):
		def _fun(*args, **kwds):
			protocol = self.type_infos.server_service.get_protocol_by_name(name)
			data = self.type_infos.server_service.pack(name, *args, **kwds)

			game = engine.server().get_game(self.gameid)
			if protocol.has_return():
				scheduler = engine.scheduler()
				token = scheduler.gen_token()

				def _filter(data):
					return protocol.unpack_return(data)

				game.remote.entity_msg_with_return(self.eid, token, data)
				return scheduler.wait_for(token, _filter)
			else:
				game.remote.entity_msg(self.eid, data)

		return _fun

class StubMgr:
	def __init__(self):
		self.stubs = {} # {name: stub}

	def create_all_stubs(self):
		def _is_stub(Type):
			return issubclass(Type, entity.StubEntity)
		stubs = engine.entity_mgr().get_entity_type_list(_is_stub)

		game_stubs, gameids = self.gather_game_infos()
		all_stubs = list(filter(lambda a: a not in game_stubs, stubs))
		all_stubs.sort()
		gameids.sort()

		index = gameids.index(engine.config()['gid'])

		current_stubs = list(engine.config().get('stubs', ()))
		for i, stub in enumerate(all_stubs):
			if i % len(gameids) == index:
				current_stubs.append(stub)

		for stub in current_stubs:
			self.create_stub(stub)

	def gather_game_infos(self):
		stubs = set()
		gameids = set()

		for config in engine.config()['active_games']:
			for stub in config.get('stubs', ()):
				assert stub not in stubs
				stubs.add(stub)

			gameid = config['gid']
			assert gameid not in gameids
			gameids.add(gameid)

		return stubs, list(gameids)

	def create_proxy(self, eid, name, gameid):
		print('create stub proxy', eid, name, gameid)
		type_infos = engine.entity_mgr().get_type_infos(name)

		self.stubs[name] = Proxy(eid, name, gameid, type_infos)

	def create_stub(self, name):
		print('create stub', name)
		entity_mgr = engine.entity_mgr()

		eid = entity_mgr.create_entity(name)

		self.stubs[name] = entity_mgr.get_entity(eid)

	def __getattr__(self, name):
		if name not in self.stubs:
			raise AttributeError("'%s' object has no attribute '%s'"%(type(self), name))

		return self.stubs[name]