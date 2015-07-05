#! /usr/bin/python
# coding:utf-8

import pexpect
import sys
import copy

__author__ = 'hgf'

class Host:
    def __init__(self):
        self.ip=''
        self.user=''
        self.userpass=''
    def __init__(self,ip,user,password):
        self.ip=ip
        self.user=user
        self.userpass=password

class AutoPassword:
    # 一个一个输入，实现初始化,server 为Host的一个对象，slaves时Host对象列表,all表示是否只能服务器免密钥访问slaves
    def __init__(self,server, slaves, all):
        self.sever=server
        self.slaves=slaves
        self.all = all
        self.child=pexpect.spawn()
        self.uncheckedto=copy.deepcopy(self.slaves)# uncheckto记录所有没有检查主机：从server ssh 到slaves
        if self.all==True:
            self.uncheckedfrom=copy.deepcopy(self.slaves)# uncheckto记录所有没有检查主机：从slaves ssh 到server
        fout = file('log.txt','w')
        self.child.logfile=fout
    # 文件初始化server和slave,文件的格式IP:username:password。其中username和password中不能出现:号，默认第一行是server，其余为slaves;all同上
    def __init__(self,filenamepath,all):
        self.all = all
        self.slaves=[]
        self.child=pexpect.spawn()
        fout = file('log.txt','w')
        self.child.logfile=fout
        fhandle = open(filenamepath,'r')
        first = True
        for line in fhandle.readlines():
            info = line.split(":")
            host = Host(info[0], info[1], info[2])
            if(first == True):
                self.server = host
                first=False
            else:
                self.slaves.append(host)
        self.uncheckedto=copy.deepcopy(self.slaves)# uncheckto记录所有没有检查主机：从server ssh 到slaves
        if self.all==True:
            self.uncheckedfrom=copy.deepcopy(self.slaves)# uncheckto记录所有没有检查主机：从slaves ssh 到server

    def check_hosts_files(self):
        pass
    # 传送文件
    def scp_files(self, filenamepath, hostfrom, hostto):
        pass
    # 产生密钥文件
    def generate_rsa(self):
        pass
    def sshremote(self,hostto):
        index=self.child.expect(['#',pexpect.EOF])
        if index!=0 and index!=1:
            print "error encountered before ssh to "+ hostto.ip
            sys.exit(-1)
        self.child.sendline( str( 'ssh %s@%s' % (hostto.user, hostto.ip) ) )
        index = self.child.expect(['(?i)are you', '(?i)password', '(?i)continue connecting (yes/no)?','(?i)Last login', pexpect.EOF, pexpect.TIMEOUT])
        if index==0:# 以前从未登录过这个IP
            pass
        elif index==1:
            pass
        elif index==2 or index==3:# 已经可以免密码登录，则可以清除相关的检查数据unchecked*
            pass
        elif index==4:# 缓冲区没有数据了
            pass
        elif index==5:# 连接超时
            self.child.read()
            self.child.close()
            sys.exit(-1)

if __name__=='__main__':
    pass