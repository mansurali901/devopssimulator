#!/bin/python
import os 
os.system("mysql -uroot -e 'show engines' |grep DEFAULT")