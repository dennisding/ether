# -*- coding:utf-8 -*-

from game import entity

class OnlineStub(entity.StubEntity):
	_components = (
		'stubs.Online.Online',
	)
	def __init__(self):
		print('OnlineStub create!')
