#!/usr/bin/python3

import json

file = open('response.txt', 'r')

response = json.load(file)

print(response['result'][0]['output'])