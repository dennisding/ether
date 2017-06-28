# -*- encoding:utf-8 -*-

gate1 = {
	'port' :4000,
	'name' : 'gate1',
	'gid' : 1,
}

gate2 = {
	'port' : 4001,
	'name' : 'gate2',
	'gid' : 2,
}

game1 = {
	'port_for_gate': 5000,
	'port_for_game' : 6000,
	'name' : 'game1',
	'gid' : 3,
}

common = {

}

active_gates = [gate1, gate2]
active_games = [game1]
active_dbmgrs = []