# -*- encoding:utf-8 -*-

_args = None
_config = None
_game_config = None
_server = None
_client = None

def init():
	pass

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
