__author__ = 'hgf'
# -*- coding:utf-8 -*-
# !/usr/bin/python

import datetime
import gzip
import cStringIO
import os
import sys

 #return Expires
def get_http_expiry(_Expirestype,_num):
    """
    Adds the given number of days on to the current date and returns the future
    date as a string, in the format: "Mon, 18 Jan 2010 17:10:02 GMT"
    """
    if _Expirestype == 'd':
        expire_date = datetime.datetime.now() + datetime.timedelta(days=_num)
    elif _Expirestype == 'h':
        expire_date = datetime.datetime.now() + datetime.timedelta(hours=_num)
    else:
        expire_date = datetime.datetime.now() + datetime.timedelta(minutes=_num)
    return expire_date.strftime('%a, %d %b %Y %H:%M:%S GMT')    #格式化时间为Expire时间格式：Tue, 22 Jul 2015 12:12:12 GMT

 #return max-age
def secs_from_days(_seconds,_num):
    """
    Returns the number of seconds that are in the given number of days.
    (i.e. 1 returns 86400)
    """
    return _seconds * _num

#通过内容和压缩比压缩文件
def compressBuf(buf,_compresslevel):
    zbuf = cStringIO.StringIO()     #创建内存对象

    zfile = gzip.GzipFile(mode='wb', compresslevel=_compresslevel,fileobj=zbuf)
    zfile.write(buf)
    zfile.close()
    return zbuf.getvalue()

# 返回当前的文件夹路径
def cur_file_dir():
     path = sys.path[0]
     if os.path.isdir(path):
         return path
     elif os.path.isfile(path):
         return os.path.dirname(path)

#check file
def checkfile(_path):
    return os.path.isfile(_path)

#check path
def checkpath(_path):
    return os.path.exists(_path)

#get parent dir
def parent_dir(_path):
    return os.path.dirname(_path)
'''
    parent_dir_string=""
    if _path=="/":
        return parent_dir_string

    dir_list=_path.split("/")
    if len(dir_list)==2:
        return parent_dir_string
    else:
        for i in range(0,len(dir_list)-2):
            parent_dir_string+=dir_list[i]+"/"
    return parent_dir_string
'''