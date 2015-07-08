#! /usr/bin/python
# -*- coding:utf-8 -*-

import nmap
import sys

__author__ = 'hgf'

scan_row=[]
input_data = raw_input("Please input hosts and ports:")
scan_row = input_data.split(' ')
if len(scan_row)!=2:
    print("input error, example input \"192.168.1.0/24 80,433-560\"")
    sys.exit(0)
hosts = scan_row[0]
ports = scan_row[1]

try:
    nm = nmap.PortScanner()
except nmap.PortScannerError:
    print("Nmap not found ", sys.exc_info()[0])
    sys.exit(0)
except:
    print("Unexcepted error!")
    sys.exit(0)

try:
    nm.scan(hosts = hosts, arguments='-v -sS -p'+ports)
except Exception,e:
    print("Scan error:"+ str(e))

for host in nm.all_hosts():
    print('----------------------------------------------------------------------------------------------------------')
    print('Host: %s (%s)'% (host, nm[hosts].hostname()))
    print('State: %s' % nm[host].state())
    for proto in nm[host].all_protocols():
        print('------------------------------------------------')
        print('Protocal: %s'% proto)

        iport = nm[host][proto].keys()
        iport.sort()
        for port in iport:
            print('Port: %s \tstate: %s' %(port, nm[host][proto][port]['state']))