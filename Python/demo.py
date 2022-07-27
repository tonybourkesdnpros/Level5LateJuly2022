#!/usr/bin/python3

import yaml 

# variables (simple, complex), for loops

# Simple variables (integers, strings, Booleans)

## Integers
i = 1
p = 3

e = p + i

## Strings

greeting_1 = "Hello, "
greeting_2 = "world!"
# print(greeting_1, greeting_2)

# Complex variables (lists, dictionaries)
## Lists
planets = ['Mercury', 'Venus', 'Earth', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune']

# for planet in planets:
#    print(planet, "is a planet")

spines = ['192.168.101.101', '192.168.101.102', '192.168.101.103']

# for neighbor in spines:
#     print("neighbor", neighbor, "peer group EVPN")

## Dictionaries

file = open('underlay.yml', 'r')

underlay = yaml.safe_load(file)

for switch in underlay['devices']:
    print('Syntax for:', switch)
    for iface in underlay['devices'][switch]['interfaces']:
        ip = underlay['devices'][switch]['interfaces'][iface]
        print('interface', iface)
        print('  ip address', ip)
        if 'Ethernet' in iface:
            print('  no switchport')