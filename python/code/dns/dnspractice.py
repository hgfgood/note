#! /usr/bin/python
import dns.resolver
import os
import httplib

iplist=[]
domain = "www.google.com"

def getIpList(domain=""):
	try:
		A = dns.resolver.query(domain,'A')
	except Exception,e:
		print "dns resolver error:"+str(e)
		return
	for x in A.response.answer:
		for i in x.items:
			iplist.append(i.address)
	return True

def checkIp(ip):
	checkurl = ip + ":80"
	getcontent = ""
	httplib.socket.setdefaulttimeout(5)
	conn = httplib.HTTPConnection(checkurl)

	try:
		conn.request("GET","/",headers={"Host":domain})
		r = conn.getresponse()
		getcontent = r.read(15)
	finally:
		if getcontent == "<!doctype html>":
			print ip+"[OK]"
		else:
			print ip+"[Error]"
			print getcontent+"\n"

if __name__ =="__main__":
	if(getIpList(domain) and len(iplist)>0):
		for ip in iplist:
			checkIp(ip)
	else:
		print "dns resolver error."
