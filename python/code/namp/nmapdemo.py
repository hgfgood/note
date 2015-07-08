#! /usr/bin/python
# -*- coding:utf-8 -*-

import nmap
import sys

__author__ = 'hgf'

def detailinfo(hosts, ports):
    '''
    使用nmap测试hosts中的所有的ports，并输出详细的信息
    :param hosts: 所有主机
    :param ports:所有端口号
    :return:
    '''
    try:
        nm.scan(hosts = hosts, arguments='-v -sS -p'+ports)
    except Exception,e:
        print("Scan error:"+ str(e))

    for host in nm.all_hosts():
        print('-------------------------------------------------------------------------------------------------------')
        print('Host: %s (%s)'% (host, nm[hosts].hostname()))
        print('State: %s' % nm[host].state())
        for proto in nm[host].all_protocols():
            print('------------------------------------------------')
            print('Protocal: %s'% proto)

            iport = nm[host][proto].keys()
            iport.sort()
            for port in iport:
                print('Port: %s \tstate: %s' %(port, nm[host][proto][port]['state']))

def printcsv(nm):
    '''
    将nmap的结果以excel表的格式输出
    :param nm: namp实例
    :return:
    '''
    print('-----------------------------------------------------------------------------------------------------------')
    print('print result as csv')
    print(nm.csv())

def pingsweep(hosts,ports):
    '''
    根据ports端口，查询网段内存活主机
    :param hosts:网段
    :param ports:端口
    :return:
    '''
    nm.scan(hosts=hosts, arguments='-n -sP -PE -PA'+ports)
    host_list=[(x,nm[x]['status']['state']) for x in nm.all_hosts()]
    for host, state in host_list:
        print('{0}:{1}'.format(host,state))

def call_back(host, scan_result):
    print("----------------------------------")
    print host, scan_result
def arsynNmap(hosts):
    '''
    异步Nmap
    :param hosts:
    :return:
    '''
    nma = nmap.PortScannerAsync()
    nma.scan(hosts=hosts, arguments='-sP', callback=call_back)
    while nma.still_scanning():
        print('wait')
        nma.wait(2)
        # do some other things

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

arsynNmap(hosts)