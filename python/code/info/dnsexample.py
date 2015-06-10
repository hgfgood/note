#!/usr/bin/env python
import dns.resolver

domain = raw_input('Please input a domain:')
A = dns.resolver.query(domain,'A')
for i in A.response.answer:
	for j in i.items:
		print j
