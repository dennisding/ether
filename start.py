# -*- encoding:utf-8 -*-

import sys

from utils import init_server

def start_game_mgr():
	from servers import game_mgr

	mgr = game_mgr.GameMgr()

	mgr.start()

def start_gate():
	from servers import gate

	gate_server = gate.Gate()

	gate_server.start()

if __name__ == '__main__':
	server, config_file = sys.argv[1], sys.argv[2]

	init_server.init_server(config_file)

	if server == 'game_mgr':
		start_game_mgr()
	elif server = 'gate':
		start_gate()