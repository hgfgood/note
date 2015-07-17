#! /usr/bin/python
# coding: utf-8
import configobj
import os

__author__ = 'hgf'

app_path = raw_input("hgfserver app path [default path is:'/usr/local/hgfserver']:")
if len(app_path) == 0:
    app_path = 'hgfserver'
    os.mkdir(app_path)
    os.mkdir(app_path+"/conf")
    os.mkdir(app_path+"/logs")
    os.mkdir(app_path+"/key")

conf_ini = app_path + "/conf/hgfserver.conf"
config = configobj.ConfigObj(conf_ini, encoding='UTF-8')
config['server_version'] = "hgfserver 0.1"
config['app_path'] = app_path
config['bing_ip'] = '0.0.0.0'
config['port'] = '80'
config['sys_version'] = ""
config['protocol_version'] = "HTTP/1.0"
config['Expires'] = "7d"
config['Multiprocess'] = "off"
config['Multithreading'] = "on"
config['DocumentRoot'] = "/home/hgf/www"
config['page404'] = "/404.html"
config['Indexes'] = "off"
config['indexpage'] = "/index.html"
config['Logfile'] = app_path + "/logs/access.log"
config['errorfile'] = app_path + "/logs/error.log"

config['gzip'] = {}
config['gzip']['gzip'] = "on"
config['gzip']['compresslevel'] = "1"

config['ssl'] = {}
config['ssl']['ssl'] = "off"
config['ssl']['privatekey'] = app_path + "/key/private.key"
config['ssl']['certificate'] = app_path + "/key/server.crt"

config['cgim'] = {}
config['cgim']['cgi_moudle'] = "on"
config['cgim']['cgi_path'] = "/cgi-bin"
config['cgim']['cgi_extensions'] = "('.cgi', '.py', '.pl', '.php' )"

config['contentTypes'] = {}
config['contentTypes']['css'] = "text/css"
config['contentTypes']['doc'] = "application/msdoc"
config['contentTypes']['gif'] = "image/gif"
config['contentTypes']['gz'] = "application/x-gzip"
config['contentTypes']['html'] = "text/html"
config['contentTypes']['htm'] = "text/html"
config['contentTypes']['esp'] = "text/html"
config['contentTypes']['ics'] = "text/calendar"
config['contentTypes']['jpeg'] = "image/jpeg"
config['contentTypes']['jpg'] = "image/jpeg"
config['contentTypes']['js'] = "text/javascript"
config['contentTypes']['pdf'] = "application/pdf"
config['contentTypes']['png'] = "image/png"
config['contentTypes']['rtf'] = "application/rtf"
config['contentTypes']['txt'] = "text/plain"
config['contentTypes']['zip'] = "application/zip"
config['contentTypes']['cgi'] = "text/html"
config['contentTypes']['py'] = "text/html"
config['contentTypes']['pl'] = "text/html"
config['contentTypes']['php'] = "text/html"

config.write()