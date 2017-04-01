# -*- encoding:utf-8 -*-

from ..network.protocol import Service, protocol, pdef, pret

class GateToClient(Service):
	login = protocol(
		pdef('Bool'),
	)