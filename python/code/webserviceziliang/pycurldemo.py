#! /usr/bin/python
# coding:utf-8

import pycurl


__author__ = 'hgf'


c = pycurl.Curl()
c.setopt(pycurl.URL, "http://www.baidu.com")
c.setopt(pycurl.NOPROGRESS, 0)
c.setopt(pycurl.FORBID_REUSE, 1)
f = open("a.txt",'wb')
c.setopt(pycurl.WRITEHEADER, f)
c.setopt(pycurl.WRITEDATA, f)
c.setopt(pycurl.DNS_CACHE_TIMEOUT, 30)

c.perform()
c.close()
