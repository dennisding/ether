# -*- coding:utf-8 -*-

from network.protocol import protocol, pdef, pret

class Property:
	hp = protocol( 'all_clients')
	money = protocol('own_client')

class Client:
	become_player = protocol()

class Server:
	login = protocol(
		pret('Int', 'login_ok'),
		pdef('Str', 'name'),
		pdef('Str', 'password'),
	)
