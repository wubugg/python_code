#!/usr/bin/python3
'''
#mib-home-fap.nv
[FAP.0.ETHERNET_INTERFACE/0]
INTERFACE_DUPLEX_MODE/0 = Full
INTERFACE_ENABLE/0 = 0
INTERFACE_MAC_ADDRESS/0 = 11:11:11:11:11:11
INTERFACE_MAX_BIT_RATE/0 = 1000
INTERFACE_NAME/0 = eth0
INTERFACE_SIGN_TRANS_MEDIA/0 = TP
INTERFACE_STATUS/0 = NoLink

[FAP.0.ETHERNET_INTERFACE/1]
INTERFACE_DUPLEX_MODE/0 = Full
INTERFACE_ENABLE/0 = 1
INTERFACE_MAC_ADDRESS/0 = 22:22:22:22:22:22
INTERFACE_MAX_BIT_RATE/0 = 1000
INTERFACE_NAME/0 = eth2
INTERFACE_SIGN_TRANS_MEDIA/0 = TP
INTERFACE_STATUS/0 = NoLink

[FAP.0.ETHERNET_INTERFACE.0.VLAN_INTERFACE/0]
VLAN_INTERFACE_ENABLE/0 = 0
VLAN_INTERFACE_ID/0 = 0
VLAN_INTERFACE_NAME/0 = valn0

[FAP.0.ETHERNET_INTERFACE.0.VLAN_INTERFACE.0.VLAN_IPV4_ADDRESS/0]
IPV4_ADDRESSING_TYPE/0 = static
IPV4_DEFAULT_GATEWAY/0 = 0.0.0.0
IPV4_IP_ADDRESS/0 = 0.0.0.0
IPV4_PORT_TYPE/0 = Ng
IPV4_SUBNET_MASK/0 = 255.255.255.0

[FAP.0.ETHERNET_INTERFACE.0.VLAN_INTERFACE.0.VLAN_IPV6_ADDRESS/0]
IPV6_ADDRESSING_TYPE/0 = static
IPV6_DEFAULT_GATEWAY/0 = 0
IPV6_IP_ADDRESS/0 = 0:0:0:0::
IPV6_PORT_TYPE/0 = Ng
IPV6_SUBNET_MASK/0 = 255.255.255.0

[FAP.0.ETHERNET_INTERFACE.0.IPV4_ADDRESS/0]
IPV4_ADDRESSING_TYPE/0 = static
IPV4_DEFAULT_GATEWAY/0 = 0.0.0.0
IPV4_IP_ADDRESS/0 = 0.0.0.0
IPV4_PORT_TYPE/0 = Ng
IPV4_SUBNET_MASK/0 = 255.255.255.0

[FAP.0.ETHERNET_INTERFACE.0.IPV6_ADDRESS/0]
IPV6_ADDRESSING_TYPE/0 = static
IPV6_DEFAULT_GATEWAY/0 = 0
IPV6_IP_ADDRESS/0 = 0:0:0:0::
IPV6_PORT_TYPE/0 = Ng
IPV6_SUBNET_MASK/0 = 255.255.255.0

#data module
(W)	Device.Ethernet.Interface.{i}.Enable
	Device.Ethernet.Interface.{i}.Name
	Device.Ethernet.Interface.{i}.Status
	Device.Ethernet.Interface.{i}.MACAddress
(W) Device.Ethernet.Interface.{i}.MaxBitRate
	Device.Ethernet.Interface.{i}.SignTransMedia
(W)	Device.Ethernet.Interface.{i}.DuplexMode

(W)	Device.Ethernet.Interface.{i}.IPv4Address.{i}.IPAddress
(W) Device.Ethernet.Interface.{i}.IPv4Address.{i}.DefaultGateway
(W) Device.Ethernet.Interface.{i}.IPv4Address.{i}.SubnetMask
(W) Device.Ethernet.Interface.{i}.IPv4Address.{i}.AddressingType
	Device.Ethernet.Interface.{i}.IPv4Address.{i}.PortType
(W) Device.Ethernet.Interface.{i}.IPv6Address.{i}.IPAddress
(W) Device.Ethernet.Interface.{i}.IPv6Address.{i}.DefaultGateway
(W) Device.Ethernet.Interface.{i}.IPv6Address.{i}.SubnetMask
(W) Device.Ethernet.Interface.{i}.IPv6Address.{i}.AddressingType
    Device.Ethernet.Interface.{i}.IPv6Address.{i}.PortType

(W) Device.Ethernet.Interface.{i}.VlanInterface.{i}.Name
(W) Device.Ethernet.Interface.{i}.VlanInterface.{i}.Id
(W) Device.Ethernet.Interface.{i}.VlanInterface.{i}.Enable
(W) Device.Ethernet.Interface.{i}.VlanInterface.{i}.IPv4Address.{i}.IPAddress
(W) Device.Ethernet.Interface.{i}.VlanInterface.{i}.IPv4Address.{i}.SubnetMask
(W) Device.Ethernet.Interface.{i}.VlanInterface.{i}.IPv4Address.{i}.AddressingType
(W) Device.Ethernet.Interface.{i}.VlanInterface.{i}.IPv4Address.{i}.DefaultGateway
    Device.Ethernet.Interface.{i}.VlanInterface.{i}.IPv4Address.{i}.PortType
(W) Device.Ethernet.Interface.{i}.VlanInterface.{i}.IPv6Address.{i}.IPAddress
(W) Device.Ethernet.Interface.{i}.VlanInterface.{i}.IPv6Address.{i}.SubnetMask
(W) Device.Ethernet.Interface.{i}.VlanInterface.{i}.IPv6Address.{i}.AddressingType
(W) Device.Ethernet.Interface.{i}.VlanInterface.{i}.IPv6Address.{i}.DefaultGateway
    Device.Ethernet.Interface.{i}.VlanInterface.{i}.IPv6Address.{i}.PortType
'''

import configparser
import pprint
import os
import sys
import json
import re

NV_PATH = 'mib-home-fap.nv'

NV_SEC_BASE = 'FAP\.0\.ETHERNET_INTERFACE'
NV_SEC_VLAN = 'VLAN_INTERFACE'
NV_SEC_IPV4 = 'IPV4_ADDRESS'
NV_SEC_IPV6 = 'IPV6_ADDRESS'

#options need to write to system
NV_enbale = 'INTERFACE_ENABLE/0 = 0'



re_interface		   = re.compile(r'(%s)/(\d)'%NV_SEC_BASE)
re_interface_sub	   = re.compile(r'(%s)\.(\d)'%NV_SEC_BASE)
re_interafce_ipv4	   = re.compile(r'(%s)\.(\d)\.(%s)/(\d)'%(NV_SEC_BASE, NV_SEC_IPV4))
re_interafce_ipv6	   = re.compile(r'(%s)\.(\d)\.(%s)/(\d)'%(NV_SEC_BASE, NV_SEC_IPV6))
re_interface_vlan	   = re.compile(r'(%s)\.(\d)\.(%s)/(\d)'%(NV_SEC_BASE, NV_SEC_VLAN))
re_interface_vlan_sub  = re.compile(r'(%s)\.(\d)\.(%s)\.(\d)'%(NV_SEC_BASE, NV_SEC_VLAN))
re_interface_vlan_ipv4 = re.compile(r'(%s)\.(\d)\.(%s)\.(\d)\.(VLAN_%s)/(\d)'%(NV_SEC_BASE, NV_SEC_VLAN, NV_SEC_IPV4))
re_interface_vlan_ipv6 = re.compile(r'(%s)\.(\d)\.(%s)\.(\d)\.(VLAN_%s)/(\d)'%(NV_SEC_BASE, NV_SEC_VLAN, NV_SEC_IPV6))

class Vividict(dict):
	def __missing__(self, key):
		value = self[key] = type(self)()
		return value

nv_cfg = configparser.ConfigParser()
nv_cfg.optionxform = str
nv_cfg.read(NV_PATH)

nv_dict = Vividict()
#Level 1
for sec in nv_cfg.sections():
	m = re_interface.match(sec)
	if m != None:
		nv_dict['interface.'+m.group(2)] = dict()
		print(nv_cfg.options(sec))
#for opt in nv_cfg.options(sec):
		#print(nv_cfg[][])

pprint.pprint(nv_dict, width=40)


class networkMangager:
	def __init__():
		pass
	def nv_to_dict():
		pass
	def nv_to_system():
		pass
	def system_to_dict():
		pass
	def dict_to_systemdcfg():
		pass
	def show_running_config():
		pass
	def	oam_get(): 
		pass
# pprint.pprint(netcfg)
#	print(re_interface.match(sec))
#	print(m.group())
#	m = re.match(r'(FAP.0.ETHERNET_INTERFACE/)(\d)',sec)
   # if m == None:
   # 	continue
   # print('interface.'+m.group(2))
   # netcfg['interface.'+m.group(2)] = dict()
#	print(m.group(1)+m.group(2))
#	if m == None:
#		continue
#	print(m.group(2))
#	print(nvcfg.sections()[0])

#print(nvcfg['FAP.0.ETHERNET_INTERFACE/0']['INTERFACE_MAC_ADDRESS/0'])
#pprint.pprint(interface['interface.0'], width=40, depth=None)
exit(0)

netcfg['interface.0']['enable'] = '1'
netcfg['interface.0']['ipv4address.0']['ipaddress'] = '1.1.1.1'
netcfg['interface.0']['ipv4address.0']['ipaddress.2'] = '1.1.1.1'
netcfg['interface.0']['ipv4address.1']['ipaddress']= '2.2.2.2'

pprint.pprint(interface['interface.0'], width=40, depth=None)

#print(interface['ipv4address.0']['ipaddress'])
#print(interface['ipv4address.1']['ipaddress'])

#pprint.pprint(interface['interface.0'], width=40, depth=1)
#pprint.pprint(interface['interface.0'], width=40, depth=None, indent=1)
#print(interface)


#fd = os.open('a.txt', os.O_CREAT|os.O_WRONLY)


#def get_interface():
#	for index in range(100):
#		sec_name = NV_BASE+'/'+str(index)
#		if config.has_section(sec_name):
			#interface[str(index)].['abcd'] = 'asdfasdf'
			#print(interface[str(index)].['abcd'])
			#config.sections() 
#interface = list()
#for index in range(10):
#	tmp = NV_BASE+'/'+str(index)
#	if tmp in config.sections():
#		interface.append(dict())
#print(interface[0])
		#for key in config[NV_BASE+'/'+str(index)]:
		#interface[str(index)] = i
	#print(config.options[NV_BASE+'/'+str(index)])
	#interface[str(index)] = (NV_BASE+'/'+str(index))
	

#get_from_nv()



'''
for sec in nvcfg.sections():
	m = re_interface_vlan_ipv4.match(sec)
	if m != None:
		print(m.group(0))
	#	print(m.group(1), m.group(2), m.group(3), m.group(4))
exit(0)

class InterfaceConfig:
	def __init__(nv_config):
		self.conf = nv_config

def get_from_nv():
	print(1111111111)

NV_PATH = 'mib-home-fap.nv'
SEC_BASE = 'FAP.0.ETHERNET_INTERFACE'

INTFSEC = [ SEC_BASE, '.']
print(INTFSEC)

config = configparser.ConfigParser()
config.read(NV_PATH)
#value = config['FAP.0.ETHERNET_INTERFACE/0']['INTERFACE_ENABLE/0']
#value = config['FAP.0.ETHERNET_INTERFACE/0']['INTERFACE_MAC_ADDRESS/0']
#class AddressConfig:
#str = 'FAP.0.ETHERNET_INTERFACE/0'
#print(str.split('/')[-2])
class AddressConfig:
	def __init__(self, index):
		self.index = index
		self.ipaddr = '1.1.1.1'


	
class InterfaceConfig:
#	index = -1
	def __init__(self, index):
		self.index = index
		self.enable = '1'
		self.name = 'wangchao'
		self.maxbitrate = '250'
		self.duplexmode = ['None', 'Half', 'Full', 'Auto']
		self.AddressConfig = dict()
		for i in range(10):
			self.AddressConfig[i] = AddressConfig(i)

#		self.index = self.get_index
#		self.enable = 
#		self.name = 
#		self.status
	def get_from_nv(self):
		self.enable = '1'
		self.name = 'wangchao'
		self.maxbitrate = '250'
		self.duplexmode = ['Half', 'Full', 'Auto']



value = InterfaceConfig(14)
print(value.AddressConfig.ipaddr)


#interface = list()
#for index in range(10):
#	interface.append(InterfaceConfig(index))
#print(interface[8].name)

#index
#enable
#name
#status
#macaddress
#maxbitrate
#signtransmedia
#duplexmode

def get_from_system
def set_to_system
def set_to_networkd

interface = dict()
interface['0'] = dict()
interface['0']['enable'] = '1'
interface['0']['name'] = 'ens33'

print(interface['0']['name'] )
'''
