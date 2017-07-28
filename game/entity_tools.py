# -*- coding:utf-8 -*-

import engine

def create_player_client(entity):
	gate = engine.server().get_gate(entity.stub.gateid)
	type_infos = entity.type_infos

	gate.remote.create_player_client(entity.stub.cid, entity.eid, type_infos.name)

