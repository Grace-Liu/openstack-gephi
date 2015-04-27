def list_vms(nova_client):
	''' 
		query nova, list all virtual machines	
	'''
	vms = nova_client.servers.list(True)
	return vms
	
def list_routers(neutron_client):
	'''
		query neutron, list all routers
	'''
	routers = neutron_client.list_routers()
	return routers

def list_ports(neutron_client):
	'''
		query neutron, list all ports
		create PortList [ port1, port2... ]
	'''
	PortList = []
	PortList = neutron_client.list_ports()
	return PortList

def list_subnets(neutron_client):	
	'''
		query neutron, list all subents
		create NetList [ subnet1, subnet2... ]
	'''
	subnets = []
	sub = neutron_client.list_subnets()
	for s in sub['subnets']:
		subnets.append(s['id'])
	return subnets

def list_extnets(neutron_client):
	'''
		query neutron, list all external networks
		create ExternalNet [ net1, net2... ]
	'''
	ExternalNet = []
	net = neutron_client.list_networks()
	for n in net['networks']:
		if str(n['router:external']) == "True":
			ExternalNet.append(n['id'])

	subnet = neutron_client.list_subnets()
	for s in subnet['subnets']:
		if s['network_id'] in ExternalNet:
			ExternalNet.append(s['id'])
	return ExternalNet

def create_vm_table(VMList):
	'''
		query ceilometer, list resource for each virtual machine
		create VMTable { id: name, cpu, mem, disk } and add resource info 
	'''
	VMTable = {}

	for v in VMList:
		v = v.to_dict()
		VMTable[v['id']] = { "name": v['name'], 
							 "cpu":  None, 
							 "mem":  None, 
							 "disk": None }
	return VMTable

def update_vm_table(VMTable, ceilo_client):
	for v in VMTable:
		res = ceilo_client.resources.get(v);
		res = res.to_dict()
		#print res['metadata']['display_name']
		VMTable[v]["cpu"] = res['metadata']['vcpus']
		VMTable[v]["mem"] = res['metadata']['memory_mb']
		VMTable[v]["disk"] = res['metadata']['disk_gb']

def create_router_table(RouterList):
	'''
		create RouterTable { id: name, host, subnet:[] }
	'''
	RouterTable = {}
	for r in RouterList['routers']:
		RouterTable[r['id']] = { "name": r['name'],  
								 "host": None, \
								 "subnet": [] }
	return RouterTable

def update_router_table(RouterTable, PortList):
	'''
		Update router table: { id: name, host, subnet:[] }
		Add host and subnet information
	'''
	for port in PortList['ports']:
		router_id = port['device_id']
		if router_id in RouterTable:
			if RouterTable[router_id]["host"] == None:
				RouterTable[router_id]["host"] = port["binding:host_id"].split('.')[0]
			for net in port['fixed_ips']:
				net_id = net['subnet_id']
				if net_id not in RouterTable[router_id]["subnet"]:
						RouterTable[router_id]["subnet"].append(net_id)

def create_net_table(NetList, PortList, VMTable):
	'''
		Create NetTable { subnet_id: name, type, host, ip, resource }
	'''
	NetTable = { n:{} for n in NetList }
	for port in PortList['ports']:
		if str(port["device_owner"]) == "compute:nova":
			vmname = VMTable[port["device_id"]]['name']
			resource = "cpu:" + VMTable[port["device_id"]]['cpu']  \
				 	 + " mem:" + VMTable[port["device_id"]]['mem'] \
				 	 + " disk:" + VMTable[port["device_id"]]['disk']  
			for net in port['fixed_ips']:
				host = port["binding:host_id"].split('.')[0]
				NetTable[net['subnet_id']][port['id']] = { "name":vmname, \
														   "type":port["device_owner"], \
														   "host":host, \
														   "ip":net['ip_address'], \
														   "resource":resource }
	return NetTable
