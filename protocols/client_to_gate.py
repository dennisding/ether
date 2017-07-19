# -*- encoding:utf-8 -*-

from network.protocol import protocol, pdef, pret

class ClientToGate:
	entity_msg = protocol(
		pdef('Bytes', 'data'),
	)

	# test code
	check = protocol(
		pdef('Str', 'name'),
		pdef('Str', 'password')
	)

	login = protocol(
		pdef('Str', 'name'),
		pdef('Str', 'password')
	)

	msg_to_game = protocol(
		pdef('Str', 'eid'),
		pdef('Bool', 'data')
	)
