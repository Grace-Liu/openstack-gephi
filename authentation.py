import os
from neutronclient.v2_0 import client as neutron
from novaclient import client as nova
from ceilometerclient import client as ceilometer

os_username = os.getenv("OS_USERNAME")
os_password = os.getenv("OS_PASSWORD")
os_tenant_name = os.getenv("OS_TENANT_NAME")
os_auth_url = os.getenv("OS_AUTH_URL")

neutron_credentials = {
	"username": os_username,
	"password": os_password,
	"tenant_name": os_tenant_name,
	"auth_url": os_auth_url
}

nova_credentials = {
	"username": os_username,
	"api_key": os_password,
	"project_id": os_tenant_name,
	"auth_url": os_auth_url
}

ceilometer_credentials = {
	"os_username": os_username,
	"os_password": os_password,
	"os_tenant_name": os_tenant_name,
	"os_auth_url": os_auth_url
}

def create_neutron_client():
	neutron_client = neutron.Client(**neutron_credentials)
	return neutron_client

def create_nova_client():
	nova_client = nova.Client("2", **nova_credentials)
	return nova_client

def create_ceilo_client():	
	ceilo_client = ceilometer.get_client("2", **ceilometer_credentials)
	return ceilo_client
