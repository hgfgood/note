#! /usr/bin/python
import paramiko

__author__ = 'hgf'

username = "root"
password = "1qaz2wsx"
hostname = "10.109.33.163"
port = 22
paramiko.util.log_to_file('log.txt')
try:
    t = paramiko.Transport((hostname, port))
    t.connect(username=username, password=password)
    sftp = paramiko.SFTPClient.from_transport(t)
    sftp.put('/home/hgf/authorized_keys', '/root/aaaaa',)
    sftp.get('/root/install.log', './server.log')
    sftp.mkdir('/root/test', '700')
    print(sftp.stat('/root/install.log'))
    sftp.rmdir('/root/a')
    print(sftp.listdir('/home'))
    t.close()
except Exception, e:
    print "Error!"
    print(str(e))