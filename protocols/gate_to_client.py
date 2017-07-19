# -*- encoding:utf-8 -*-

from network.protocol import protocol, pdef, pret

class GateToClient:
	create_player_client = protocol(
		pdef('Eid', 'eid'),
		pdef('Str', 'name'),
	)

	client_msg = protocol(
		pdef('Eid', 'eid'),
		pdef('Bytes', 'data'),
	)

	# test code
	login = protocol(
		pdef('Bool', 'is_ok'),
	)

	show_info = protocol(
		pdef('Str', 'name'),
		pdef('Str', 'info')
	)
