from cvplibrary import CVPGlobalVariables, GlobalVariableNames
import yaml
from cvplibrary import RestClient
import ssl

stuff = CVPGlobalVariables.getValue(GlobalVariableNames.CVP_SYSTEM_LABELS)

for item in stuff:
  key, value = item.split(':', 1)
  if key == 'hostname':
    hostname = value


ssl._create_default_https_context = ssl._create_unverified_context

configlet = 'underlay_yaml'

cvp_url = 'https://192.168.0.5/cvpservice/configlet/getConfigletByName.do?name='

client = RestClient(cvp_url+configlet, 'GET')


if client.connect():
  result = client.getResponse()

underlay_raw = yaml.safe_load(result)

underlay_string = underlay_raw['config']

underlay = yaml.safe_load(underlay_string)


lo_route_map = """
ip prefix-list LOOPBACK
    seq 10 permit 192.168.101.0/24 eq 32
    seq 11 permit 192.168.102.0/24 eq 32
    seq 12 permit 192.168.201.0/24 eq 32
    seq 13 permit 192.168.202.0/24 eq 32
    seq 14 permit 192.168.253.0/24 eq 32


route-map LOOPBACK permit 10
  match ip address prefix-list LOOPBACK
"""

peer_range = """
peer-filter LEAF-AS-RANGE
10 match as-range 65000-65535 result accept
"""

def gen_spine_bgp():
  print(loopback)
  print(peer_range)
  ASN = underlay[hostname]['BGP']['ASN']
  loopback0 = underlay[hostname]['interfaces']['loopback0']['ipv4']
  print("router bgp %s") % ASN  
  
  print("  router-id %s ") % loopback0
  print("  no bgp default ipv4-unicast")
  print("  maximum-paths 3")
  print("  distance bgp 20 200 200")


  range = "192.168.103.0/24"

    
  print("  bgp listen range %s peer-group LEAF_Underlay peer-filter LEAF-AS-RANGE") % range
      
  print(" neighbor LEAF_Underlay peer group")
  print(" neighbor LEAF_Underlay send-community")
  print(" neighbor LEAF_Underlay maximum-routes 12000") 

  

  print("  neighbor EVPN peer group") 

  evpn_range = "192.168.101.0/24"

  print("  bgp listen range %s peer-group EVPN peer-filter LEAF-AS-RANGE") % evpn_range
      
  
  print("  neighbor EVPN update-source Loopback0")
  print("  neighbor EVPN ebgp-multihop 3")
  print("  neighbor EVPN send-community extended")
  print("  neighbor EVPN maximum-routes 0")

  print("  address-family evpn")
  print("    neighbor EVPN activate")
  print("  address-family ipv4")
  print("    neighbor LEAF_Underlay activate")
  print("    redistribute connected route-map LOOPBACK")
  





def gen_leaf_BGP():
  print(lo_route_map)
  ASN = underlay['devices'][hostname]['BGP']['ASN']
  loopback0 = underlay['devices'][hostname]['interfaces']['loopback0']['ipv4']
  print("router bgp %s") % ASN  
  
  print("  router-id %s ") % loopback0
  print("  no bgp default ipv4-unicast")
  print("  maximum-paths 3")
  print("  distance bgp 20 200 200")

  spine_ASN = underlay['global']['DC1']['spine_ASN']
 

  print("  neighbor SPINE_Underlay peer group")
  print("  neighbor SPINE_Underlay remote-as %s") % spine_ASN
  print("  neighbor SPINE_Underlay send-community")
  print("  neighbor SPINE_Underlay maximum-routes 12000") 


  print("  neighbor LEAF_Peer peer group")
  print("  neighbor LEAF_Peer remote-as %s") % ASN
  print("  neighbor LEAF_Peer next-hop-self")
  print("  neighbor LEAF_Peer maximum-routes 12000")

  for neighbor in underlay['devices'][hostname]['BGP']['spine-peers']:
    print("  neighbor %s peer group SPINE_Underlay") % neighbor
  
  print("  address-family ipv4")
  print("  neighbor SPINE_Underlay activate")
  print("     redistribute connected route-map LOOPBACK")

def gen_spine_bgp():
  print(lo_route_map)
  print(peer_range)
  ASN = underlay['devices'][hostname]['BGP']['ASN']
  loopback0 = underlay['devices'][hostname]['interfaces']['loopback0']['ipv4']
  print("router bgp %s") % ASN  
  
  print("  router-id %s ") % loopback0
  print("  no bgp default ipv4-unicast")
  print("  maximum-paths 3")
  print("  distance bgp 20 200 200")


  range = "192.168.103.0/24"

    
  print("  bgp listen range %s peer-group LEAF_Underlay peer-filter LEAF-AS-RANGE") % range
      
  print(" neighbor LEAF_Underlay peer group")
  print(" neighbor LEAF_Underlay send-community")
  print(" neighbor LEAF_Underlay maximum-routes 12000") 

  

  print("  neighbor EVPN peer group") 

  evpn_range = "192.168.101.0/24"

  print("  bgp listen range %s peer-group EVPN peer-filter LEAF-AS-RANGE") % evpn_range
      
  
  print("  neighbor EVPN update-source Loopback0")
  print("  neighbor EVPN ebgp-multihop 3")
  print("  neighbor EVPN send-community extended")
  print("  neighbor EVPN maximum-routes 0")

  print("  address-family evpn")
  print("    neighbor EVPN activate")
  print("  address-family ipv4")
  print("    neighbor LEAF_Underlay activate")
  print("    redistribute connected route-map LOOPBACK")
  
def gen_interfaces():  
  for iface in underlay['devices'][hostname]['interfaces']:
    ip = underlay['devices'][hostname]['interfaces'][iface]['ipv4']
    mask = underlay['devices'][hostname]['interfaces'][iface]['mask']
    print("interface %s") % iface
    print("  ip address %s/%s") % (ip, mask) 
    if 'thernet' in iface:
      print("  no switchport")


if ('leaf' in hostname) or ('spine' in hostname):
  gen_interfaces()
  
if 'leaf' in hostname:
  gen_leaf_BGP()
  
if 'spine' in hostname:
  gen_spine_bgp()


