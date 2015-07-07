#! /usr/bin/python
# coding:utf-8

import pexpect
import sys

def copy2remote_file(ssh_conf, remote_ip, remote_dir, remote_user, remote_password):
	'''ssh_conf：用于替换原来电脑上的ssh_config 文件的路径；
	sshdconf:用来替换电脑上'sshd_config'文件的文件的路径。
	'''

	childscp = pexpect.spawn(str(('scp %s %s@%s:%s') % (ssh_conf, remote_user, remote_ip, remote_dir)))
	childscp.outfile = sys.stdout
	index = childscp.expect(['(?i)are you', '(?i)continue connecting (yes/no)?', '(?i)password', pexpect.EOF, pexpect.TIMEOUT])
	if index == 0:
		# 已经免密钥了
		return 0
	elif index== 1:
		# 从未登录过这个IP
		childscp.sendline('yes')
		childscp.expect('(?i)password')
		childscp.sendline(remote_password)
		x = childscp.expect(['sshd_config', 'id_rsa.pub'])
		print x
	elif index == 2:
		# 登录过这个IP
		childscp.sendline(remote_password)
		x = childscp.expect(['sshd_config', 'id_rsa.pub'])
		print x
	elif index == 3:
		# 缓冲区尾----没有消息就是好消息【可能是文件已经存在】
		childscp.expect(pexpect.EOF)
	elif index ==4:
		# 超时
		return -1
	childscp.sendline('\r\n')
	childscp.read()
	childscp.expect(pexpect.EOF)
	childscp.close()

if __name__ == '__main__':
	remote_password='hgfgood'
	remote_ip = '192.168.122.8'
	remote_user = 'root'
	child = pexpect.spawn('ls')
	#child = pexpect.spawn('ssh-keygen -t rsa')
	# 记日志
	fout = file('sshlog.txt','w')
	child.logfile=fout
	# 多次回车，产生公私密钥对
	child.sendline('\r\n\r\n\r\n\r\n')
	path=""
	if(remote_user == 'root'):
		path="/root/"
	else:
		path = str("/home/"+remote_user+"/")

	# 复制ssh配置文件
	flag = copy2remote_file('sshd_config', remote_ip, path, remote_user, remote_password)
	if(flag == -1):
		print "scp %s encounter a problem" % '/etc/ssh/sshd_config'
		sys.exit(-1)
	# 覆盖原来的配置文件

	flag = copy2remote_file(str('/home/hgf/.ssh/id_rsa.pub'), remote_ip, path, remote_user, remote_password)
	if( flag == -1):
		print "scp %s encounter a problem" % 'public key'
		sys.exit(-1)
	child.close()
	# 远程登录
	child=pexpect.spawn('ssh root@192.168.122.8')
	child.logfile=fout
	index = child.expect(['password:','root','(?i)Last login',pexpect.EOF])
	if index == 0:
		child.sendline(remote_password)
		child.expect('#')
	elif (index==1 or index ==2):
		print("already OK")
		print index
		child.sendline('who am i')
		child.sendline('\r\n\r\n')
		i = child.expect(['root','hgf', pexpect.EOF])
		if i==0:
			print 'ok, root'
		elif i ==1:
			print 'ok, hgf'
		elif i==2:
			print '输出空'
		else:
			print 'error'
		child.close()
		sys.exit(0)
	else:
		print "缓冲区没有内容，是否时已经成功？"
	# 登录后，创建相应的文件夹
	child.sendline('mkdir -p .ssh')
	child.expect('#')
	# 复制公钥到对应的目录的授权文件
	child.sendline('/bin/bash -c "cat id_rsa.pub > .ssh/authorized_keys"')
	child.expect('#')
	child.sendline('chmod 700 .ssh')
	child.expect('#')
	child.sendline('chmod 600 .ssh/authorized_keys')
	child.expect('#')
	# 复制ssh配置文件到/etc/ssh目录下
	child.sendline('sudo mv ~/sshd_config /etc/ssh/sshd_config')
	index = child.expect(['password:', pexpect.EOF])
	if index == 0:
		child.sendline(remote_password)
	elif index == 1:
		pass
	child.expect('#')
	#重起ssh服务
	child.sendline('sudo service sshd restart')
	child.expect('password for')
	child.sendline(remote_password)
	child.close()
	#测试是否可以免密钥登录
	test=pexpect.spawn('ssh root@192.168.122.8')
	index = test.expect(['(?i)Last login','password',pexpect.EOF,pexpect.TIMEOUT])
	if index == 0:
		print "OK"
	elif index == 1:
		print "connected, but config failure"
	else:
		print "other exception"