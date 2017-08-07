# -*- encoding:utf-8 -*-

from network.protocol import protocol, pdef, pret

class GameToGame:
	create_stub_proxy = protocol(
		pdef('Eid', 'eid'),
		pdef('Str', 'name'),
		pdef('Int', 'gameid'),
	)

	entity_msg = protocol(
		pdef('Eid', 'eid'),
		pdef('Bytes', 'data'),
	)

	entity_msg_with_return = protocol(
		pdef('Eid', 'eid'),
		pdef('Token', 'token'),
		pdef('Bytes', 'data')
	)

	entity_msg_return = protocol(
		pdef('Token', 'token'),
		pdef('Bytes', 'data'),
	)
