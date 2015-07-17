#! /usr/bin/python
#coding:utf-8

from optparse import OptionParser
import sys
import os
import pubutil
import logging
from  BaseHTTPServer import HTTPServer
from SocketServer import BaseServer
from configobj import ConfigObj

__author__ = 'hgf'

try:
    config_filename = os.path.join('/conf/hgfserver.conf', os.path.dirname(os.path.abspath(os.path.dirname(os.path.curdir))))
    config = ConfigObj(config_filename, encoding="UTF-8")
except Exception, e:
    print("Read hgfserver config file ERROR: "+str(e))
    sys.exit(-1)

#defind Expires type
ExpiresTypes = {
    "d"	: 86400,
    "h"	: 3600,
    "m"	: 60,
}

#mime types
contentTypes=[]
for m in config['contentTypes']:
    tmp=[]
    tmp.append(m)
    tmp.append(config['contentTypes'][m])
    contentTypes.append(tmp)
contentTypes = dict(contentTypes)

server_version = config['server_version']
bind_ip = config['bing_ip']
port = config['port']
sys_version = config['sys_version']
protocol_version = config['protocol_version']
gzip = config['gzip']['gzip']
compresslevel = config['gzip']['compresslevel']
ssl = config['ssl']['ssl']
privatekey = config['ssl']['privatekey']
certificate = config['ssl']['certificate']
Expires = config['Expires']
Multiprocess = config['Multiprocess']
Multithreading = config['Multithreading']
DocumentRoot = config['DocumentRoot']
page404 = config['page404']
Indexes = config['Indexes']
indexpage = config['indexpage']
Logfile = config['Logfile']
errorfile = config['errorfile']

cgi_moudle = config['cgim']['cgi_moudle']
cgi_path = config['cgim']['cgi_path']
cgi_extensions = config['cgim']['cgi_extensions']

if ssl == 'on':
    if not pubutil.checkfile(privatekey):
        print("Error: privatekey \""+privatekey+"\" No such file or directory.")
        sys.exit()
    if not pubutil.checkfile(certificate):
        print("Error: certificate \""+certificate+"\" No such file or directory.")
        sys.exit()

if not pubutil.checkpath(DocumentRoot):
    print "Error: DocumentRoot \""+DocumentRoot+"\" No such file or directory."
    sys.exit()

if not pubutil.checkfile(Logfile):
    print "Error: Logfile \""+Logfile+"\" No such file or directory."
    sys.exit()

if not pubutil.checkfile(errorfile):
    print "Error: Errorfile \""+errorfile+"\" No such file or directory."
    sys.exit()

if cgi_moudle == 'on':
    if len(cgi_path) == 0:
        print "Error: cgi_path is null? please set."
        sys.exit()
    for _path in cgi_path:
        if not pubutil.checkpath(pubutil.cur_file_dir()+'/'+_path):
            print "Error: cgi_path \""+pubutil.cur_file_dir()+'/'+_path+"\" No such file or directory."
            sys.exit()

# system log
try:
    logger = logging.getLogger()
    handler = logging.FileHandler(errorfile)
    logger.addHandler(handler)
    logger.setLevel(logging.NOTSET)
except IOError, e:
    print(str(e))

class SecureHTTPServer(HTTPServer):
    pass


if __name__ == "__main__":
    MSG_USAGE = "hgfserver [-v] [-h]"
    parser = OptionParser(MSG_USAGE)
    parser.add_option("-v", "--version", action="store_true", dest="verbose", help="view hgfserver version info.")
    opts, args = parser.parse_args()

    if opts.verbose:
        print "hgfserver 0.1 beta."
        sys.exit();