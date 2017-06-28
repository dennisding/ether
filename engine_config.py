# -*- encoding:utf-8 -*-

gate1 = {
	'cport' :4000,  # port for client connection
	'gport' : 5000, # port for game connection
	'gid' : 1,
}

gate2 = {
	'cport' : 4001,
	'gport' : 5001,
	'gid' : 2,
}

game1 = {
	'gport' : 6000,
	'gid' : 3,
}

common = {
	# 'name' : 'common', # set by setup_config
	'net_option' : 'zip pack big',
}

active_gates = [gate1, gate2]
active_games = [game1]
active_dbmgrs = []