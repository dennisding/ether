# -*- encoding:utf-8 -*-

event_loop = None

_config = None
_server = None
_event_loop = None

def init():
	pass

def config():
	return _config

def server():
	return _server

def event_loop():
	return _event_loop