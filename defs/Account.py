# -*- coding:utf-8 -*-

from network.protocol import protocol, pdef, pret

from common import attr
from common import gtypes

class Package(gtypes.Attribute):
	count = attr.attr(gtypes.Int)

class Property(gtypes.EntityAttribute):
	hp = attr.attr(gtypes.Int)
	package = attr.attr(Package)

class Client:
	become_player = protocol()

class Server:
	login = protocol(
		pret('Int', 'login_ok'),
		pdef('Str', 'name'),
		pdef('Str', 'password'),
	)
