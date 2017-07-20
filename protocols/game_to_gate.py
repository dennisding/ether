# -*- encoding:utf-8 -*-

from network.protocol import protocol, pdef, pret

class GameToGate:
	game_server_ready = protocol(
		pdef('Int', 'gameid'),
	)

	create_player_client = protocol(
		pdef('Eid', 'eid'),
		pdef('Int', 'cid'),
		pdef('Str', 'name'),
	)

	client_msg = protocol(
		pdef('Int', 'cid'),
		pdef('Eid', 'eid'),
		pdef('Bytes', 'data'),
	)

	entity_msg_return = protocol(
		pdef('Int', 'cid'),
		pdef('Eid', 'eid'),
		pdef('Token', 'token'),
		pdef('Bytes', 'data'),
	)
