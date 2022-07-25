#!/usr/bin/python3

import json

file = open('response.json', 'r')

response = json.load(file)

for iface in response['result'][0]['interfaces']:
    print(iface, response['result'][0]['interfaces'][iface]['interfaceAddress']['ipAddr']['address'])