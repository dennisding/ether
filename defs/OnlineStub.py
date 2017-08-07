# -*- coding:utf-8 -*-

from network.protocol import protocol, pdef, pret

class Property:
	hp = protocol( 'all_clients')
	money = protocol('own_client')

class Server:
	is_online = protocol(
		pret('Bool', 'is_online'),
		pdef('Str', 'name'),
	)

	set_online = protocol(
		pdef('Str', 'name'),
	)
