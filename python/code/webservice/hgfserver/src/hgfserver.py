#! /usr/bin/python
#coding:utf-8

from optparse import OptionParser
import sys
import os
from os import sep
import pubutil
import logging
import socket
import time
from CGIHTTPServer import CGIHTTPRequestHandler
from  BaseHTTPServer import HTTPServer
from SocketServer import BaseServer
from configobj import ConfigObj
from OpenSSL import SSL
import cgi
from cStringIO import StringIO
import shutil
from SocketServer import ThreadingMixIn,ForkingMixIn

__author__ = 'hgf'

try:
    config_filename = os.path.join(os.path.dirname(os.path.abspath(os.path.dirname(os.path.curdir))),'conf/hgfserver.conf' )
    print(config_filename)
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
print(config['contentTypes'])
for m in config['contentTypes']:
    tmp=[]
    tmp.append(m)
    tmp.append(config['contentTypes'][m])
    contentTypes.append(tmp)
contentTypes = dict(contentTypes)

server_version = config['server_version']
bind_ip = config['bing_ip']
port = int(config['port'])
sys_version = config['sys_version']
protocol_version = config['protocol_version']
gzip = config['gzip']['gzip']
compresslevel = int(config['gzip']['compresslevel'])
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
    # for _path in os.path(cgi_path):
    #     if not pubutil.checkpath(pubutil.cur_file_dir()+'/'+_path):
    #         print "Error: cgi_path \""+pubutil.cur_file_dir()+'/'+_path+"\" No such file or directory."
    #         sys.exit()

# system log
try:
    logger = logging.getLogger()
    handler = logging.FileHandler(errorfile)
    logger.addHandler(handler)
    logger.setLevel(logging.NOTSET)
except IOError, e:
    print(str(e))

class SecureHTTPServer(HTTPServer):
    def __init__(self, server_address, HandlerClass):
        BaseServer.__init__(self, server_address, HandlerClass)
        ctx = SSL.Context(SSL.SSLv23_METHOD)        #定义一个ssl连接，ssl所采用的版本
        ctx.use_privatekey(privatekey)
        ctx.use_certificate(certificate)
        self.socket = SSL.Connection(ctx, socket.socket(self.address_family, self.socket_type))     #使用给定的OpenSSL.SSL.Content和Socket创建连接对象
        self.server_bind()
        self.server_activate()


class ServerHandler(CGIHTTPRequestHandler):
    # hgfserver info
    server_version = server_version
    sys_version = sys_version
    protocol_version = protocol_version
    CGIHTTPRequestHandler.cgi_directories = cgi_path

    def handle_on_request(self):
        try:
             self.raw_requestline = self.rfile.readline(65537)
             if len(self.raw_requestline) > 65536:
                 self.requestline = ''
                 self.request_version = ''
                 self.command = ''
                 self.send_error(414)
                 return
             if not self.raw_requestline:
                self.close_connection = 1
                return
             if not self.parse_request():
                return
             mname = "do_"+self.command
             if not hasattr(self, mname):
                 self.send_error(501, "Unsupported method (%r)" % self.command)
                 return
             method = getattr(self,mname)
             method()
             if not self.wfile.closed:
                self.wfile.flush() #actually send the response if not already done.
        except socket.timeout, e:
            logger.error(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+"-"+str(e))
            self.close_connection = 1
            return

    def setup(self):
        self.connection = self.request
        self.rfile = socket._fileobject(self.request, "rb", self.rbufsize)
        self.wfile = socket._fileobject(self.request, "wb", self.wbufsize)

    def do_GET(self):
        try:
            # go to default page
            if self.path.endswith("/"):
                if Indexes=="on":
                    self.send_response(200)
                    self.send_header("Content-type", "text/html")
                    self.end_headers()
                    f = self.list_directory(DocumentRoot+self.path)
                    self.copyfile(f, self.wfile)
                    f.close()
                    return
                elif indexpage != "":
                    self.send_response(302)
                    self.send_header("Location", indexpage)
                    self.end_headers()
                    return
                else:
                    self.send_response(404)
            if self.path=='/favicon.ico':
                return
            path_parts = self.path.split('.')
            try:
                content_type=contentTypes[path_parts[-1]]
            except:
                if page404=="":
                    self.send_response(404)
                else:
                    self.send_response(302)
                    self.send_header("Location", page404)
                self.end_headers()

            if cgi_moudle == "on" and self.path.endswith(cgi_extensions):
                return CGIHTTPRequestHandler.do_GET(self)
            else:
                #static content
                f = open(DocumentRoot+sep+self.path)
                fs = os.fstat(f.fileno())

                Expirestype = Expires[-1:]
                Expiresnum=Expires[:-1]

                expiration = pubutil.get_http_expiry(Expirestype, int(Expiresnum))

                CACHE_MAX_AGE = pubutil.secs_from_days(ExpiresTypes[Expirestype], int(Expiresnum))
                cache_control = 'public; max_age=%d' % (CACHE_MAX_AGE,)
                client_cache_cc = self.headers.getheader('Cache-Control')
                client_cache_p = self.headers.getheader('Pragma')
                ModifiedSince = self.headers.getheader('If-Modified-Since')

                if client_cache_cc=='no-cache' or client_cache_p == 'no-cache' or\
                        (client_cache_p == None and client_cache_cc == None and ModifiedSince == None):
                    client_modified = None
                else:
                    try:
                        client_modified = ModifiedSince.split(';')[0]
                    except:
                        client_modified = None
                file_last_modified = self.date_time_string(fs.st_mtime)

                if client_modified == file_last_modified:
                    self.send_response(304)
                    self.end_headers()
                else:
                    s = f.read()
                    if gzip == 'on':
                        compressed_content = pubutil.compressBuf(s, compresslevel)
                    else:
                        compressed_content = s
                    self.send_response(202)
                    self.send_header('Last-Modified', file_last_modified)
                    self.send_header('Cache-Control', cache_control)
                    self.send_header('Expires', expiration)
                    self.send_header('Content-type', content_type)
                    if gzip == 'on':
                        self.send_header('Content-Encoding','gzip')
                    self.send_header('Content-Length', str(len(compressed_content)))
                    self.end_headers()
                    self.wfile.write(compressed_content)
                f.close()
                return

            return
        except IOError, e:
            logger.error(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+"-"+str(e))

    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_POST(self):
        global rootnode
        try:
            ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
            if ctype == 'multipart/form-data':
                query=cgi.parse_multipart(self.rfile, pdict)
            self.send_response(200)
            self.end_headers()
            upfilecontent = query.get('upfile')
            print "filecontent", upfilecontent[0]
            self.wfile.write("<HTML>POST OK.<BR><BR>");
            self.wfile.write(upfilecontent[0]);

        except :
            pass
    def list_directory(self, path):

        try:
            list = os.listdir(path)
        except os.error:
            self.send_error(404, "No permission to list directory");
            return None
        list.sort(lambda a, b: cmp(a.lower(), b.lower()))
        f = StringIO()
        f.write("<h2>Directory listing for %s</h2>\n" % self.path)
        f.write("<hr>\n<ul>\n")
        f.write('<li><a href="%s">Parent Directory</a>\n' % (pubutil.parent_dir(self.path)))
        for name in list:
            fullname = os.path.join(path, name)
            displayname = name = cgi.escape(name)
            if os.path.islink(fullname):
                displayname = name + "@"
            elif os.path.isdir(fullname):
                displayname = name + "/"
                name = name + os.sep
            f.write('<li><a href="%s">%s</a>\n' % (name, displayname))
        f.write("</ul>\n<hr>\n")
        f.seek(0)
        return f

    def copyfile(self, source, outputfile):
        try:
            shutil.copyfileobj(source, outputfile)
        except KeyboardInterrupt,e:
            pass

    def log_message(self, format, *args):
        open(Logfile, "a").write("%s - - [%s] %s\n" %(self.address_string(),self.log_date_time_string(),format%args))

#mul-processsupport.
class ProcessHTTPServer(ForkingMixIn, HTTPServer):
    pass

#mul-thread support.
class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    pass

def main(HandlerClass = ServerHandler,ServerClass = SecureHTTPServer):
    try:
        try:
            if ssl=="on":
                server = (bind_ip, port)
                print("port:"+str(port))
            elif Multiprocess=="on":
                server = ProcessHTTPServer((bind_ip, port), ServerHandler)
                print("port:"+str(port))
            elif Multithreading=="on":
                server = ThreadedHTTPServer((bind_ip, port), ServerHandler)
                print("port:"+str(port))
            else:
                server = HTTPServer((bind_ip, port), ServerHandler)
                print("port:"+str(port))
            print 'Started hgfserver...[OK]'
        except Exception,e:
            print str(e)
            logger.error(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+"-"+str(e))
            return
        if ssl=="on":
            httpd = ServerClass(server, ServerHandler)
            httpd.serve_forever()
        else:
            server.serve_forever()
    except KeyboardInterrupt,e:
        print '^C received, shutting down server'
        if ssl=="on":
            httpd.socket.close()
        else:
            server.socket.close()

if __name__ == "__main__":
    MSG_USAGE = "hgfserver [-v] [-h]"
    parser = OptionParser(MSG_USAGE)
    parser.add_option("-v", "--version", action="store_true", dest="verbose", help="view hgfserver version info.")
    opts, args = parser.parse_args()

    if opts.verbose:
        print "hgfserver 0.1 beta."
        sys.exit();
    main()