#! /usr/bin/python
# coding:utf-8

import pexpect
import sys
import copy

__author__ = 'hgf'

class Host:
    def __init__(self,ip,user,password):
        self.ip=ip
        self.user=user
        self.userpass=password

class AutoPassword:
    '''
     一个一个输入，实现初始化,server 为Host的一个对象，slaves时Host对象列表,all表示是否只能服务器免密钥访问slaves
    '''
    def __init__(self, server, slaves, all):
        self.sever=server
        self.slaves=slaves
        self.all = all
        self.fout = file('log.txt','w')
        fout = file('log.txt','w')

    def readhostsfromfile(self, filenamepath, all):
        '''
        文件初始化server和slave,文件的格式IP:username:password。其中username和password中不能出现:号，默认第一行是server，其余为slaves;all同上
        :param filenamepath:从文件读取服务器信息
        :param all:
        :return:
        '''
        self.all = all
        self.slaves=[]
        self.fout = file('log.txt','w')
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

    def check_hosts_files(self):
        '''
        将所有的主机全部检查一遍，若all=True，则将所有其他主机生成的密钥scp到server；若all=False，则server把密钥发到其他主机，并且设置免密钥登录
        1.  对每一个slaves主机：
        3.  将摄制好的sshd——config传到slave主机：1》传到某个目录；2》sudo mv到系统目录
        4.  将slave的公钥传到server
        5.  将所有的slave主机的公钥》authorised_keys
        6.  all=True
        7.  将server的密钥也放入authorised_keys文件
        8. 将authorised_keys文将复制到每个slave文件
        9.  ssh到slave主机
            》修改.ssh目录的权限，authorized_keys的权限
        10.  重起slave的ssh服务
        11.
        :return:
        '''
        # 创建authorized_keys文件，并间server的公钥复制进去
        server_home = self.generatepath(server)+'/'
        self.child = pexpect.spawn('touch '+ server_home+'authorized_keys')
        self.child.logfile = self.fout
        index = self.child.expect(['#', pexpect.EOF])
        if index == 0:
            print index,':OK'
        else:
            print 'OK'

        self.cat2file(server_home+'.ssh/id_rsa.pub', server_home+'authorized_keys', True, True)#server的公钥拷贝到authorized_keys文件，直接覆盖，以免里面有之前的数据
        for slave in self.slaves:
            home = self.generatepath(slave)+'/'
            sshd_conf_file = 'sshd_config'
            self.scp_local_file(sshd_conf_file, home, slave)# 将本地的sshd配置文件传到slave主机
            self.scp2local_file(home+'.ssh/id_rsa.pub', server_home+'id_rsa.pub.'+slave.ip, slave)# 将slave的公钥复制到server
            self.cat2file(server_home+'id_rsa.pub.'+slave.ip, server_home+'authorized_keys', False, True)# 将slaves的公钥拷贝进authorized_keys文件

        for slave in self.slaves:# 将authorized_keys复制到每个slave主机
            home = self.generatepath(slave)+'/'
            self.scp_local_file(server_home+'authorized_keys', home+'.ssh/',slave)

        for slave in self.slaves:
            home = self.generatepath(slave)+'/'
            sshd_conf_file = 'sshd_config'
            sshd_conf_dir = '/etc/ssh/'
            self.ssh_remote(slave)
            self.mv_file(home+sshd_conf_file, sshd_conf_dir+ sshd_conf_file, slave, True)
            self.chmod(home+'.ssh', '700')
            self.chmod(home+'.ssh/authorized_keys', '600')
            self.child.close()
        if all:# 如果全部互相免密钥连接
            self.child = pexpect.spawn('ls')# 将authorized_keys复制到server的.ssh目录下
            self.child.logfile = self.fout
            index = self.child.expect(['autho',pexpect.EOF])
            print index
            self.mv_file(server_home+'authorized_keys', server_home+'.ssh/authorized_keys', server)
            self.chmod(server_home+'.ssh/authorized_keys', '600')
            self.chmod(server_home+'.ssh', '700')

    def mv_file(self, frompath, topath, host, needroot=False):
        '''
        移动一个文件
        :param frompath: 移动的文件原来的路径
        :param topath: 文件移动后的路径
        :param host:移动文件的主机
        :param needroot:是否需要root权限，True需要，默认为False
        :return:
        '''
        str = 'mv '+ frompath+' '+ topath
        if needroot:
            str = 'sudo '+ str
        self.child.sendline(str)
        index = self.child.expect(['(?i)password', '#', pexpect.EOF])
        if index == 0:
            self.child.sendline(host.userpass)
            self.child.expect('#')
        elif index == 1:
            pass
        elif index==2:
            print '缓冲区没有数据，host ip：'+host.ip

    def cat2file(self, srcpath, destpath, overriwter=True, isserver=False):
        '''
        将文件重定向到文件
        :param srcpath:源文件路径
        :param destpath:目标文件路径
        :param overriwter 是否覆盖，True，直接覆盖
        :param isserver 是否是时主控端
        :return:
        '''
        if overriwter:
            self.childcat = pexpect.spawn('/bin/bash -c "cat '+ srcpath+' > '+ destpath+'"')
        else:
            self.childcat = pexpect.spawn('/bin/bash -c "cat '+ srcpath+' >> '+ destpath+'"')

        self.childcat.logfile=self.fout
        if isserver:
            self.child.expect(pexpect.EOF)
        else:
            self.child.expect('#')
        self.childcat.close()
        self.child.logfile = self.fout

    def chmod(self, filepath, mod):
        '''
        修改文件权限
        :param filepath:文件路径
        :param mod:赋予的权限
        :return:
        '''
        self.child.sendline('chmod '+ mod +' '+ filepath)
        index = self.child.expect(['#',pexpect.EOF])
        if index ==1:
            print '缓冲区无数据'


    def scp2local_file(self, filefrompath, filetopath, hostfrom):
        '''
        将远程文件传送到本地
        :param filefrompath:远程主机上的路径
        :param filetopath:本地主机上的路径
        :param hostfrom:文件来源主机
        :return:
        '''
        self.childscp = pexpect.spawn('scp '+hostfrom.user +'@' + hostfrom.ip + ':' + filefrompath +' '+filetopath)
        self.childscp.logfile = self.fout
        index = self.childscp.expect(['(?i)are you', '(?i)password', pexpect.EOF, pexpect.TIMEOUT])
        print index
        if index==0:# 以前从未登录过这个IP
            self.childscp.sendline('yes')
            self.childscp.expect('(?i)password')
            self.childscp.sendline(hostfrom.userpass)
            self.childscp.expect('%')
        elif index==1:
            self.childscp.sendline(hostfrom.userpass)
            self.childscp.expect('%')
        elif index==2:# 缓冲区没有数据了
            print 'EOF, check log file please.'
        elif index==3:# 连接超时
            print 'connection timeout, check log file please.'
        self.childscp.close()
        self.child.logfile = self.fout

    def scp_local_file(self, filefrompath, filetopath, hostto):
        '''
        使用scp传输本地文件文件
        :param filefrompath: 文件源路径
        :param filetopath: 文件移动到目的主机上的路径
        :param hostto: 想要移动到的主机的名字
        :return:
        '''
        self.childscp = pexpect.spawn('scp '+ filefrompath +' '+hostto.user +'@' + hostto.ip+':'+filetopath)
        self.childscp.logfile = self.fout
        index = self.childscp.expect(['(?i)are you', '(?i)password', pexpect.EOF, pexpect.TIMEOUT])
        print index
        if index==0:# 以前从未登录过这个IP
            self.childscp.sendline('yes')
            self.childscp.expect('(?i)password')
            self.childscp.sendline(hostto.userpass)
            self.childscp.expect('%')
        elif index==1:
            self.childscp.sendline(hostto.userpass)
            self.childscp.expect('%')
        elif index==2:# 缓冲区没有数据了
            print 'EOF, check log file please.'
        elif index==3:# 连接超时
            print 'connection timeout, check log file please.'
        self.childscp.close()
        self.child.logfile=self.fout

    def generate_rsa(self, hostfrom, hostto):
        '''
        产生密钥文件
        :param hostfrom: 生成rsa密钥的主机
        :param hostto: rsa公钥的传送目的地
        :return:
        '''
        self.child.sendline('rm -rf '+ self.generatepath(hostfrom)+'/.ssh')
        self.child.expect('#')
        self.child.sendline('ssh-keygen -t rsa')
        self.child.expect('(?i)enter')
        self.child.sendline('\r\n')
        index = self.child.expect('(?i)enter')
        self.child.sendline('\r\n')
        self.child.expect('(?i)enter')
        self.child.sendline('\r\n')
        self.scp_local_file(self.generatepath(hostfrom)+'/.ssh/id_rsa.pub', self.generatepath(hostto)+'id_rsa.pub'+hostfrom.ip, hostto )

    def generatepath(self, host):
        '''
        根据用户名获得用户目录
        :param host: 当前操作的主机
        :return:
        '''
        if host.user=='root':
            return '/root'
        else:
            return '/home/'+host.user

    def ssh_remote(self, hostto):
        '''
        使用ssh连接到远程主机
        :param hostto: 想要连接的主机
        :return:
        '''
        self.child = pexpect.spawn( str( 'ssh %s@%s' % (hostto.user, hostto.ip) ) )
        self.child.logfile = self.fout
        index = self.child.expect(['(?i)are you', '(?i)password', '(?i)continue connecting (yes/no)?','(?i)Last login', pexpect.EOF, pexpect.TIMEOUT])
        print index
        if index==0:# 以前从未登录过这个IP
            self.child.sendline('yes')
            self.child.expect('(?i)password')
            self.child.sendline(hostto.userpass)
            self.child.expect('#')
        elif index==1:
            self.child.sendline(hostto.userpass)
            self.child.expect('#')
        elif index==2 or index==3:# 已经可以免密码登录，
            print "already ssh without password, remove from unchcecked list"
            self.child.expect('#')
        elif index==4:# 缓冲区没有数据了
            print 'EOF, check log file please.'
        elif index==5:# 连接超时
            self.child.read()
            self.child.close()
            print 'connection timeout, check log file please.'
            sys.exit(-1)

if __name__=='__main__':
    # test ssh_remote
    server=Host('192.168.122.1','hgf','hgfgood')
    slave=Host('192.168.122.190','root','hgfgood')
    slaves=[]
    slaves.append(slave)
    inst = AutoPassword(server,slaves, False)
    inst.check_hosts_files()
