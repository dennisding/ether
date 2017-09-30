# -*- coding:utf-8 -*-

_factory = None

class Factory:
	def create(self, name, attrs):
		pass

def set_factory(factory):
	global _factory
	_factory = factory

