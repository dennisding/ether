# -*- coding:utf-8 -*-

from network.protocol import protocol, pdef, pret

class Property:
	pass

class Client:
	become_player = protocol()

	login_reply = protocol(
		pdef('Bool', 'is_ok'),
	)


class Server:
	login = protocol(
		pdef('Str', 'name'),
		pdef('Str', 'password'),
	)
