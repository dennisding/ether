# -*- coding:utf-8 -*-

from network.protocol import protocol, pdef, pret

from common import attr
from common import gtypes

class Property(gtypes.EntityAttribute):
	pass

class Server:
	is_online = protocol(
		pret('Bool', 'is_online'),
		pdef('Str', 'name'),
	)

	set_online = protocol(
		pdef('Str', 'name'),
	)

	try_set_online = protocol(
		pret('Bool', 'is_online'),
		pdef('Str', 'name')
	)
