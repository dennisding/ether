# -*- coding:utf-8 -*-

from network.protocol import protocol, pdef, pret

class Account:
	become_player = protocol()

	# server methods
	login = protocol( 'server',
		pdef('Str', 'name'),
		pdef('Str', 'password'),
	)

	# client methods
	login_reply = protocol( 'client',
		pdef('Bool', 'is_ok'),
	)