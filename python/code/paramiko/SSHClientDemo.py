#/usr/bin/python
# coding:utf-8
import paramiko
import sys

__author__='hgf'

try:
    data =  raw_input("Please input hostname username and password:").split()
    if len(data)!=3:
        print("input error! make sure your input like \"192.168.1.1 root 123456\"")
        sys.exit(0)
except Exception,e:
    print("Exception occourred!")
    print (str(e))
hostname = data[0]
username = data[1]
password = data[2]

paramiko.util.log_to_file('sys.log')

ssh = paramiko.SSHClient()
ssh.load_system_host_keys()

ssh.connect(hostname = hostname, username = username, password = password)
stdin, stdout, stderr = ssh.exec_command('free -m')
print stdout.read()
ssh.close()
