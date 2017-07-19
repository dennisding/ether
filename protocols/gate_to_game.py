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