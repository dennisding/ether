# -*- encoding:utf-8 -*-

from network.protocol import protocol, pdef, pret

class GateToClient:
	create_client_entity = protocol(
		pdef('Eid', 'eid'),
		pdef('Str', 'name')
	)

	login = protocol(
		pdef('Bool', 'is_ok'),
	)

	show_info = protocol(
		pdef('Str', 'name'),
		pdef('Str', 'info')
	)
