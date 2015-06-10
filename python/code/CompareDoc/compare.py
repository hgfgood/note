#!/usr/bin/python
#coding:utf-8

import difflib
import sys

try:
	firstfile = sys.argv[1]#python 的参数是从一开始的
	secondfile = sys.argv[2]
except Exception,e:
	print ("Error:"+ str(e))
	print ("Usage: compare.py file1 file2")
	sys.exit()

def readfile(path):
	try:
		filehandle = open(path,'r')
		text = filehandle.read().splitlines()
		filehandle.close()
		return text
	except IOError as error:
		print ("Read file error:" + str(error))
		print ("Usage: compare.py file1 file2")
		sys.exit()

if(firstfile =="" or secondfile ==""):
	print ("Usage: compare.py file1 file2")
	sys.exit()

file1lines = readfile(firstfile)
file2lines = readfile(secondfile)

diff = difflib.HtmlDiff()
print diff.make_file(file1lines,file2lines)		
