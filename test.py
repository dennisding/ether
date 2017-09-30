# -*- coding:utf-8 -*-

from common import attr
from common import gtypes

class Package(gtypes.Attribute):
	size = attr(gtypes.Int)
	max_size = attr(gtypes.Int)

class Avatar:
	_components = ()

	def __init__(self):
		super().__init__()

a = Avatar()
a.hp = 1000

a2 = Avatar()
