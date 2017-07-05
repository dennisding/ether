# -*- coding:utf-8 -*-

import engine

def create_client_entity(entity):
	gate = engine.server().get_gate(entity.gateid)
	type_infos = entity.type_infos

	gate.remote.create_client_entity(entity.cid, entity.eid, type_infos.name)

