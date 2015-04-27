# openstack-gephi
Gephi Configuration
1. Install Gephi and Graph Streaming plugin.
2. Create a new project in Gephi
3. Open Streaming tab and Start Master Server 
4. Open Layout tab and choose YifanHu's Multilevel, click Run

Openstack configuration 
1. Change ip address and port in openstack-gephi.py to the machine running Gephi Server 
   ( graph = pygephi.GephiClient('http://161.253.66.62:8080/workspace0', autoflush=True) )
2. Run program: python openstack-gephi.py
