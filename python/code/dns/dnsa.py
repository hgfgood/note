#! /usr/bin/python
import dns.resolver

domain="www.google.com"
A=dns.resolver.query(domain,'A')
for x in A.response.answer:
	for i in x:
		print (i.address)
