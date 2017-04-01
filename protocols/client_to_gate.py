# -*- encoding:utf-8 -*-

from ..network.protocol import Service, protocol, pdef, pret

class ClientToGate(Service):
	check = protocols(
		pdef('Str', 'local_sign'),
		pdef('Str', 'remote_sign')
	)

	login = protocol(
		pdef('Str', 'name'),
		pdef('Str', 'password')
	)
