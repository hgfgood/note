#! /usr/bin/python
import dns.resolver

domain= "baidu.com"
NC = dns.resolver.query(domain,'Ns')
for x in NC.response.answer:
	for i in x.items:
		print i.to_text()
