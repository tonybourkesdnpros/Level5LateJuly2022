#!/usr/bin/python3

import pyeapi

connect = pyeapi.connect_to('leaf4-DC1')

result = connect.api("ipinterfaces").get('Ethernet3')

print(result['address'])