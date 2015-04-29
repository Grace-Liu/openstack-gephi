Openstack-Gephi
=====
A tool to export openstack network topology, node information into Gephi

Gephi Configuration
===================
1. Install Gephi and Graph Streaming plugin.
   - http://gephi.github.io/users/download/
   - https://marketplace.gephi.org/plugin/graph-streaming/
2. Create a new project in Gephi
3. Open Streaming tab and Start Master Server 
4. Open Layout tab and choose YifanHu's Multilevel or DAG Layout(need to install), click Run

Openstack Configuration 
=======================
1. Change ip address and port in openstack-gephi.py to match machine information running Gephi Server 
   ( gephi_server and gephi_port)
2. Run program: python openstack-gephi.py

Gephi Graph 
=======================
You can view detailed graph information by modifying Label text settings.
In current version, the following information can be shown in the graph
- node id
- node name
- node type
- ip address
- physical host
- resource infomation: cpu, mem, disk
- utilization information: cpu
