# -*- coding:utf-8 -*-

from network.protocol import protocol, pdef, pret

from common.attr import attr
from common import gtypes

class Package(gtypes.Attribute):
	count = attr(gtypes.Int)

class Property(gtypes.EntityAttribute):
	hp = attr(gtypes.Int)

	package = attr(Package)

#	hp = attr('Int', 'all_clients', default)
#	mp = attr('Int', 'all_clients', default)
#	models = attr('List', 'all_clients')
#
#	equips = attr('List(Int)', 'own_client')
#	tasks = attr('Map(Int, TaskInfo)', 'own_client')

class Client:
	become_player = protocol()

class Server:
	pass
