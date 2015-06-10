#!/usr/bin/env python
import difflib

def readfile(filepath):
	content=[]
	f=open(filepath,'r')
	for line in f.readlines():
		content.append(line.strip().splitlines())
	return content

def dif(text1,text2,toHTML):
	print "begin"
	if(toHTML):
		d = difflib.HtmlDiff()
		print d.make_file(text1,text2)
	else:
		d=difflib.Differ()
		diff_message = d.compare(text1,text2)
		print "\n".join(list(diff_message))

if __name__=='__main__':
	print '''please input the file path name of two text documents.'''
	test1path=raw_input("the first text file path:")
	test2path=raw_input("the seconf text file path:")
#	tohtml=raw_input("to html file?('yes' or 'no'):")
	tohtml="no"
	text1 = open(test1path,'r').readlines()
	text2 = open(test2path,'r').readlines()
	print text2
	print text1

	print type(text2)
	print "**********************************************"


	if('yes' == tohtml):
		dif(text1,text2,True)
	else:
		dif(text1,text2,False)
	'''
	d=difflib.Differ()
	diff_message = d.compare(text1,text2)
	print "\n".join(list(diff_message))
	'''