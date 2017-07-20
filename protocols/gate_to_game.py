# -*- encoding:utf-8 -*-

from network.protocol import protocol, pdef, pret

class GateToGame:
	client_connected = protocol(
		pdef('Int', 'gateid'),
		pdef('Int', 'cid')
	)

	entity_msg = protocol(
		pdef('Eid', 'eid'),
		pdef('Bytes', 'data'),
	)

	entity_msg_with_return = protocol(
		pdef('Eid', 'eid'),
		pdef('Token', 'token'),
		pdef('Bytes', 'data'),
	)

	entity_msg_return = protocol(
		pdef('Eid', 'eid'),
		pdef('Token', 'token'),
		pdef('Bytes', 'data'),
	)