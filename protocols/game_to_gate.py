# -*- encoding:utf-8 -*-

from network.protocol import protocol, pdef, pret

class GameToGate:
	create_client_entity = protocol(
		pdef('Eid', 'eid'),
		pdef('Int', 'cid'),
		pdef('Str', 'name'),
	)