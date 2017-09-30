# -*- coding:utf-8 -*-

import os
from . import assemble

class EntityMeta(type):
	def __new__(cls, name, bases, namespace, **kwds):
		namespace = assemble.assemble_components(namespace)

		new_type = type.__new__(cls, name, bases, namespace)

		type_info.gen_type_info(new_type)
		return new_type

def gen_eid():
	# the length from mongodb's objectid
	return os.urandom(12)
