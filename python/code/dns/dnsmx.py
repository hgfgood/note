#! /usr/bin/python
import dns.resolver

domain="163.com"
MX = dns.resolver.query(domain,'MX')
for i in MX:
	print i.preference, i.exchange
