#! /usr/bin/python
# coding:utf-8

import getpass
import pxssh

__author__ = 'hgf'

try:
    s = pxssh.pxssh()
    hostname=raw_input("hostname:")
    username = raw_input("username:")
    password = getpass.getpass('Please input password:')
    s.login(hostname,username,password)
    s.sendline('ls -al')
    s.prompt()
    print(s.before)
    print(s.after)
    s.sendline('df')
    s.prompt()
    print(s.before)
    s.close()
except Exception, e:
    print("pxssh failed in login")
    print str(e)