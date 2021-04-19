#!/bin/python3
import os
process = os.popen("mysql -e 'show grants for master';")
output = process.read()
findbycode = output.find('ALL PRIVILEGES ON `test`.* TO `master`@`%`')
if findbycode > 0:
    print('User-has')
else:
    print('unvalidated')
#print(output)
