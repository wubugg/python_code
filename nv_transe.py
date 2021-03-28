import configparser
config = configparser.ConfigParser()

NV_PATH = 'mib-home-fap.nv'

SEC_BASE = 'FAP.0.ETHERNET_INTERFACE'
SEC_INTERFACE = SEC_BASE + '.' + 'ETHERNET_INTERFACE'

SEC_VLAN=


config.read(NV_PATH)
value = config['FAP.0.ETHERNET_INTERFACE/0']['INTERFACE_ENABLE/0']
print(value)

value = config['FAP.0.ETHERNET_INTERFACE/0']['INTERFACE_MAC_ADDRESS/0']
print(value)


#for i in

#class AddressConfig:
#
#class InterfaceConfig:


