# -*- encoding:utf-8 -*-

from ..network.protocol import Service, protocol, pdef, pret

class GameMgrServices(Services):
	gate_started = protocol(
		pdef('Int', 'gate_id'),
		pdef('Str', 'ip'),
		pdef('Int', 'port')
	)

	game_started = protocol()