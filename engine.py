# -*- encoding:utf-8 -*-

_args = None
_config = None
_game_config = None
_server = None
_client = None

stubs = None #  StubMgr
all_games = None

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

def entity_mgr():
	return _server.entity_mgr

def client():
	return _client

def args():
	return _args

def callback(arg1 = None, arg2 = None):
	_server.callback(arg1, arg2)

def get_entity(eid):
	return _server.entity_mgr.get_entity(eid)

def del_entity(eid):
	_server.entity_mgr.del_entity(eid)

def create_entity(*args, **kwds):
	return _server.entity_mgr.create_entity(*args, **kwds)

def scheduler():
	return _server.scheduler
