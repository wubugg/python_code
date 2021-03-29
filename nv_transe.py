#!/usr/bin/python3
import configparser

NV_PATH = 'mib-home-fap.nv'
SEC_BASE = 'FAP.0.ETHERNET_INTERFACE'

INTFSEC = [ SEC_BASE, '.']
print(INTFSEC)

#SEC_VLAN=

config = configparser.ConfigParser()
config.read(NV_PATH)
value = config['FAP.0.ETHERNET_INTERFACE/0']['INTERFACE_ENABLE/0']
#print(value)

value = config['FAP.0.ETHERNET_INTERFACE/0']['INTERFACE_MAC_ADDRESS/0']
#print(value)

#class AddressConfig:

str = 'FAP.0.ETHERNET_INTERFACE/0'
print(str.split('/')[-2])
#exit()

class InterfaceConfig:
	def __init__(self, index):
		self.index = index
		self.enable = '1'
		self.name = 'wangchao'
		self.maxbitrate = '250'
		self.duplexmode = ['Half', 'Full', 'Auto']


#		self.index = self.get_index
#		self.enable = 
#		self.name = 
#		self.status
	def get_from_nv(self):
		self.enable = '1'
		self.name = 'wangchao'
		self.maxbitrate = '250'
		self.duplexmode = ['Half', 'Full', 'Auto']

interface = list()
for index in range(10):
	interface.append(InterfaceConfig(index))
print(interface[8].name)

#index
#enable
#name
#status
#macaddress
#maxbitrate
#signtransmedia
#duplexmode
