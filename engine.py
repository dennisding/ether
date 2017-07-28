# -*- encoding:utf-8 -*-

_args = None
_config = None
_game_config = None
_server = None
_client = None

def init():
	pass

def gid():
	return _config['gid']

def config():
	return _config

def game_config():
	return _game_config

def server():
	return _server

def client():
	return _client

def args():
	return _args

def defer(arg1 = None, arg2 = None):
	_server.defer(arg1, arg2)
