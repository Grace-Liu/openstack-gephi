#!/usr/bin/env python
# openstack_gephi.py - a plugin to show network topology in Gephi

# Copyright(c) 2015 Grace Liu 

# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import gephi_client as pygephi
from authentation import *
from create_db import *

def create_graph(graph, RouterTable, NetTable, ExtNetList):
	'''
		Create a Gephi graph:
		nodes: router, net, vm
		edge: link between router-net and net-vm
	'''
	link_attributes = {}
	external_attributes = { "size":50, 'r':1.0, 'g':1.0, 'b':0.0, 'x':1, "label":"External_Net" }
	router_attributes = { "size":30, 'r':1.0, 'g':0.0, 'b':0.0, 'x':1, "label":None, "host":None } 
	subnet_attributes = { "size":20, 'r':0.0, 'g':1.0, 'b':0.0, 'x':1 }
	port_attributes = { "size":10, 'r':0.0, 'g':0.0, 'b':1.0, 'x':1, \
						"label":None, "type":None, "host":None, "ip":None, "resource":None, "util":None }

	for router in RouterTable:
		router_attributes['label'] = RouterTable[router]['name']
		router_attributes['host'] = RouterTable[router]['host']
		graph.add_node(str(router), **router_attributes)
		for net in RouterTable[router]['subnet']: 
			if net in ExtNetList:
				graph.add_node(str(net), **external_attributes)
				graph.add_edge(router+net, str(router), str(net), False)
			else:
				graph.add_node(str(net), **subnet_attributes)
				graph.add_edge(router+net, str(router), str(net), False)
				for port in NetTable[net]: 
					port_attributes['label'] = NetTable[net][port]['name']
					port_attributes['type'] = NetTable[net][port]['type']
					port_attributes['host'] = NetTable[net][port]['host']
					port_attributes['ip'] = NetTable[net][port]['ip']
					port_attributes['resource'] = NetTable[net][port]['resource']
					port_attributes['util'] = NetTable[net][port]['util']
					graph.add_node(str(port), **port_attributes)
					graph.add_edge(net+port, str(net), str(port), False)

def main():
	'''Create neutron, nova and ceilo client for retrieving topology information'''
	neutron_client = create_neutron_client()
	nova_client = create_nova_client()
	ceilo_client = create_ceilo_client()

	'''Create resource list by querying openstack client'''
	ExtNetList = list_extnets(neutron_client)
	RouterList = list_routers(neutron_client)
	VMList = list_vms(nova_client)
	PortList =list_ports(neutron_client)
	NetList = list_subnets(neutron_client)
	
	'''Create VMTable, RouterTable and NetTable'''
	VMTable = create_vm_table(VMList)
	update_vm_table_resource(VMTable, ceilo_client)
	update_vm_table_util(VMTable, ceilo_client)
	RouterTable = create_router_table(RouterList)
	update_router_table(RouterTable, PortList)
	NetTable = create_net_table(NetList, PortList, VMTable)

	'''Create gephi graph'''
	graph = pygephi.GephiClient('http://161.253.66.62:8080/workspace0', autoflush=True)
	graph.clean()
	create_graph(graph, RouterTable, NetTable, ExtNetList)

if __name__ == "__main__":
	main()
