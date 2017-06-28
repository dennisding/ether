# -*- encoding:utf-8 -*-

from .protocol import protocol, pdef, pret

check_signature = protocol(
	pdef('Str', 'local_sign'),
	pdef('Str', 'remote_sign')
)

class BaseMsg:
	server_ready = protocol(
		pdef('Bool', 'is_ready')
	)