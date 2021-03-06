# -*- encoding:utf-8 -*-

gate1 = {
	'ip' : '127.0.0.1',
	'cport' :4000,  # port for client connection
	'gport' : 5000, # port for game connection
	'gid' : 1,
}

gate2 = {
	'ip' : '127.0.0.1',
	'cport' : 4001,
	'gport' : 5001,
	'gid' : 2,
}

game1 = {
	'ip' : '127.0.0.1',
	'gport' : 6000,
	'gid' : 3,
	'stubs' : []
}

game2 = {
	'gport' : 6010,
	'gid' : 4,
}

client1 = {
}

dbmgr1 = {

}

common = {
	# 'name' : 'common', # set by setup_config
	'ip' : '127.0.0.1',
	'net_option' : 'zip pack big',
}

active_gates = [gate1]
active_games = [game1]
active_dbmgrs = []