python 集群运行维护

[TOC]

---
##环境搭建
###单机环境搭建
####安装python
```apt-get install python python-dev python-setuptools```
####安装pip
```apt-get install python-pip```
---
##简单主机信息
说明：主要参考网站[psutil文档](http://pythonhosted.org/psutil/#cpu)
###安装psutil
```pip install psutil```

###cpu
####cpu times

```python
import psutil
cputimes = psutil.cpu_times()
psutil.cpu_times().user
```
结果如下：
```
scputimes(user=1751.49, nice=57.5, system=1126.75, idle=61666.12, iowait=745.43, irq=0.0, softirq=1.58, steal=0.0, guest=0.0, guest_nice=0.0)
```
>解释：
>   user:用户cpu time；
>   nice:   ;
>   system:系统cpu time;
>   idle:cpu空闲状态cpu time;
>   iowait:io等待时间;

取出cpu_times()中的参数，例如用户cpu时间
```python
psutil.cpu_times().user
```

####获取物理cpu个数
```python
psutil.cpu_count(lgicol=False)
```



###内存和交换分区

####内存信息
```python
psutil.virtual_memory()
```
结果如下：

`svmem(total=8288972800L, available=6737719296L, percent=18.7, used=3927216128L, free=4361756672L, active=2380361728, inactive=1244004352, buffers=150831104L, cached=2225131520)`
>**解释**
total: 所有物理内存
available: 实际上可以立刻使用的内存（单位是byte）
percent:内存使用的内存(total - available) / total * 100.
used: 使用的内存
free: 空闲内存
Platform-specific fields:特定平台的属性

active: (UNIX): memory currently in use or very recently used, and so it is in RAM.
inactive: (UNIX): 未被使用的内存
buffers: (Linux, BSD): 文件缓存
cached: (Linux, BSD): 缓存
wired: (BSD, OSX):常驻内存 在RAM中的
shared: (BSD): 共享内存



####交换分区
```python
psutil.virtual_memory()
```
结果：
`sswap(total=4999606272L, used=0L, free=4999606272L, percent=0.0, sin=0, sout=0)`


###硬盘
####分区信息
```python
psutil.disk_partitions()
```

结果：
`[sdiskpart(device='/dev/sda4', mountpoint='/', fstype='ext4', opts='rw,errors=remount-ro')]`

####使用信息
```python
psutil.disk_usage('/')
```
结果：
`sdiskusage(total=202632327168, used=6518771712, free=185796829184, percent=3.2)`

###进程信息
```python
pid=3923
p = psutil.Process(pid)

#print process name
p.name()

#print process execuable file path
p.exe()

#print process current work directory
p.cwd()

#print process children process
p.get_children()
```

###net IO
```python
psutil.net_io_counters()
```
结果：
`snetio(bytes_sent=4469434, bytes_recv=64367107, packets_sent=40469, packets_recv=53242, errin=0, errout=0, dropin=0, dropout=0)`

##Ip information
IPy模块处理IP信息

1.	安装`sudo pip install Ipy`
2.	IPy包中的IP类
2.1	列出网段中的IP数目：
```python
    ip = IP('8.8.8.8')
    for i in ip:
    	print (x)
```
2.2 IP转换
```python
	ip.int()#将IP转为整数型
    ip.strHex()#将IP转为十六进制
    ip.strBIn()#将IP转为二进制
```
2.3 将十六进制的IP地址转换成为常见的淀粉十进制
```python
	print(IP(0x8080808))#输出为8.8.8.8
```
2.4 生成子网掩码
```python
	IP('8.8.8.8').make_net('255.255.255.0)
    IP('8.8.8.8/255.255.255.0',make_net=True)
```


- - -

##dns information

1. 安装dnspython
	`sudo pip install dnspython`
2.	域名解析知识清理：
	+ A记录：域名转为IP地址
	+ MX记录：邮件交换记录，定义邮件服务器的域名信息
	+ CNAME记录：实现域名见的映射。别名记录
	+ NS记录：标记区域的域名服务器授权服务器和授权子域
	+ PTR记录：反响解析，与A记录相反
	+ SOA记录：标记一个其实授权去的定义

###	A记录解析过程：
```python
	import dns.resolver
    domain = "www.google.com"
    A = dns.resolver.query(domain,'A')
    for x in A.response.answer:
    	for i in x:
        	print (i.address)
```

###	MX记录解析

```python
	#! /usr/bin/python
	import dns.resolver

	domain="163.com"
	MX = dns.resolver.query(domain,'MX')
	for i in MX:
		print i.preference, i.exchange
```


### NS记录解析

```python
	#! /usr/bin/python
	import dns.resolver

	domain= "baidu.com"
	NC = dns.resolver.query(domain,'Ns')
	for x in NC.response.answer:
		for i in x.items:
			print i.to_text()
```

###	CNAME记录解析
```python
	#!/usr/bin/python
	import dns.resolver

	domain = "www.baidu.com"
	cname = dns.resolver.query(domain,'CNAME')
	for i in cname.response.answer:
        for j in i.items:
        	print (j.to_text())
```

- - -
###实例：DNS轮循服务业务监控
```python
#! /usr/bin/python
import dns.resolver
import os
import httplib

iplist=[]
domain = "baidu.com"

def getIpList(domain=""):
        try:
                A = dns.resolver.query(domain,'A')
        except Exception,e:
                print "dns resolver error:"+str(e)
                return
        for x in A.response.answer:
                for i in x.items:
                        iplist.append(i.address)
        return True

def checkIp(ip):
        checkurl = ip + ":80"
        getcontent = ""
        httplib.socket.setdefaulttimeout(5)
        conn = httplib.HTTPConnection(checkurl)

        try:
                conn.request("GET","/",headers={"Host":domain})
                r = conn.getresponse()
                getcontent = r.read(15)
        finally:
                if getcontent == "<!doctype html>":
                        print ip+"[OK]"
                else:
                        print ip+"[Error]"
                        print getcontent+"\n"

if __name__ =="__main__":
        if(getIpList(domain) and len(iplist)>0):
                for ip in iplist:
                        checkIp(ip)
        else:
                print "dns resolver error."
```

##业务服务质量监控

###文本内容对比工具
```python
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

```

###文件目录差异对比工具
`python`自带的`filecmp`满足需求。

####filecmp模块常见的方法的说明
`filecmp`常见的方法有：cmp（单文件对比），cmpfiles（多文件对比），dircmp（目录对比）
    + `filecmp.cmp(f1,f2[,shallow=True])`:对比文件f1和f2是否相同，相同就返回True，不同为False。shallow为可选的参数，默认为True。shallow为True时表示根据文件的属性值（最后修改时间，作者，状态改变时间等）进行对比判断两文件是否相同;shallow为false时，同时对比os.stat()和对比两文件的内容判断是否相同。
    + filecmp.cmpfiles(dir1,dir2[,shallow=True]).对比dir1和dir2给定的文件清单。该方法返回三个列表：匹配，不匹配，错误（目录中不存在，读写权限不够，或其他原因导致的不能比较的清单）。
    + filecmp.dircmp(a,b[,ignore[,hide]])创建一个目录比较对象，a,b,是参加比较的目录名，ignore是忽略的文件列表，并默认为['RCS','CVS',tags'];hide表示隐藏的文件爱你列表，默认为[os.curdir,os.pardir]。dircmp类可以获得目录比较的详细信息，如只有a含有的文件。dircmp提供3个输出报告的方式：
    	* report():比较当前目录的内容
        * report_partial_closure()：比较当前目录和第一级子目录的内容
        * report_full_clourse():递归比较所有的文件

####校验源与备份目录的差异





>**python `shutil` 模块常见函数：**
>+ `copyfile( src, dst)` 	 从源src复制到dst中去。当然前提是目标地址是具备可写权限。抛出的异常信息为IOException. 如果当前的dst已存在的话就会被覆盖掉
>+ `copymode( src, dst)` 	 只是会复制其权限其他的东西是不会被复制的
>+ `copystat( src, dst)` 	 复制权限、最后访问时间、最后修改时间
>+ `copy( src, dst) `   	 复制一个文件到一个文件或一个目录
>+ `copy2( src, dst)`  	 在copy上的基础上再复制文件最后访问时间与修改时间也复制过来了，类似于cp –p的东西
>+ `copy2( src, dst)`  	 如果两个位置的文件系统是一样的话相当于是rename操作，只是改名；如果是不在相同的文件系统的话就是做move操作
>+ `copytree(olddir,newdir,True/Flase)` 	 把olddir拷贝一份newdir，如果第3个参数是True，则复制目录时将保持文件夹下的符号连接，如果第3个参数是False，则将在复制的目录下生成物理副本来替代符号连接


###使用python发送邮件

####简单测试邮件发送o
1.`smtplib.SMTP(host,port[,local_hostname[,timeout]])`构造smtp类,每个参数的含义：
+ host:邮件服务器地址
+ port：邮件服务器端口
+ local_hostname:在本地主机的FQDN发送HELO/EHLO（标识身份）指令
+ timeout:超时时间，单位s（秒）


```python
#! /usr/bin/python

# coding:utf-8

import smtplib
import string

HOST = "smtp.google.com"
SUBJECT = "TEST EMAIL"
TO = "980673553@qq.com"
FROM = "hgfgooda@gmail.com"
text = "this is the mail body main test!"
other = "other info"		#BODY中的other如果包含字符，则收到的邮件中没有内容，为什么？这个字段是什么意思？
BODY = string.join(
    (
        "From: %s" % FROM,
        "TO: %s" % TO,
        "Subject: %s" % SUBJECT,
        other,
        text
    ), "\r\n"
)
server = smtplib.SMTP()
server.connect(HOST, 25)
server.starttls()
server.login("hgfgooda@gmail.com", "password")
server.sendmail(FROM, TO, BODY)
server.quit()

```


####定制丰富内容的邮件
1.使用html编写邮件内容
```python
#! /usr/bin/python
# coding:utf-8

import smtplib
from email.mime.text import MIMEText

HOST = "smtp.qq.com"
SUBJECT = u"官方流量数据报表"
FROM = "980673553@qq.com"
TO = "hgfgoodcreate@163.com"
msg = MIMEText("""
<table width="800" b cellspacing="0" order="0">
    <tr>
        <td bgcolor="gray" style="font-size:14px">
            *官网数据
        </td>
    </tr>
    <tr>
        <td>
            <ol>
                <li>日访问量：<font color=red>152433</font> 访问次数：23651 页面浏览量：45123 点击数：545122 数据流量：504Mb</li>
                <li>状态码信息：<br></li>&nbsp;&nbsp;&nbsp;500：105 404：3264 503：214
                <li>浏览器浏览信息：<br></li>&nbsp;&nbsp;&nbsp;IE:50% firefox:10% chrome:30% other:10%
                <li>页面信息：<br></li>&nbsp;&nbsp;&nbsp;/index.php 42153<br>&nbsp;&nbsp;&nbsp;/view.php 21451<br>&nbsp;&nbsp;&nbsp;/login.php 5122<br>
            </ol>
        </td>
    </tr>
</table>
""", "html", "utf-8"
)

msg['Subject'] = SUBJECT
msg['From'] = FROM
msg['TO'] = TO

try:
    server = smtplib.SMTP()
    server.connect(HOST, "25")
    server.starttls()
    server.login("980673553@qq.com", "password")
    server.sendmail(FROM, TO, msg.as_string())
    server.quit()
    print("邮件发送成功！")
except Exception, e:
    print("失败！原因："+str(e))
```
>**注意点**
>在使用`email.mime.text.MIMEText`对象的时候，需要将MIMEText对象的内容，**编码**和内容使用的语言交代清楚。



2.在邮件中添加图片
+ 定义一个`email.mime.multipart.MIMEMultipart`对象
+ 使用`MIMEMultipart`对象的`attach`函数，将`html`内容嵌入到邮件中，其中使用`contentID`来访问嵌入到邮件中的图片信息
+ 使用`MIMEImage`对象，将图片文件从本地以二进制的形式读入到内存，并用图像文件的二进制序列初始化`MIMEImage`对象，使用`MIMEImage`的`add_header()`方法给`MIMEImage`对象设置`contentID`
+ 使用`MIMEMultipart`对象的`attach`函数，将`MIMEImage`对象嵌入到邮件中

```python
#! /usr/bin/python
# coding:utf-8

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText

__author__ = 'hgf'

HOST = "smtp.qq.com"
SUBJECT = u"业务性能数据表"
FROM = "980673553@qq.com"
TO = "hgfgoodcreate@163.com"

def addimg(src, imgid):
    fp = open(src, 'rb')
    msgImg = MIMEImage(fp.read())
    fp.close()
    msgImg.add_header('Content-ID', imgid)
    return msgImg

# 使用related定义内嵌资源
msg = MIMEMultipart('related')

msgtext = MIMEText("""
<table width="800" b cellspacing="0" order="0">
    <tr>
        <td bgcolor="gray" style="font-size:14px">
            *官网logo
        </td>
    </tr>
    <tr bgcolor="#EFEBDE" height="100" style="font-size:13px">
        <td>
           <img src="cid:p1">
        </td>
        <td>
            <img src="cid:p2">
        </td>
    </tr>
    <tr bgcolor="#EFEBDE" height="100" style="font-size:13px">
        <td>
           <img src="cid:p3">
        </td>
        <td>
            <img src="cid:p4">
        </td>
    </tr>
</table>
""", "html", "utf-8")
msg.attach(msgtext)
msg.attach(addimg("/home/hgf/Pictures/program/logo/1.PNG", "p1"))
msg.attach(addimg("/home/hgf/Pictures/program/logo/2.PNG", "p2"))
msg.attach(addimg("/home/hgf/Pictures/program/logo/3.PNG", "p3"))
msg.attach(addimg("/home/hgf/Pictures/program/logo/4.PNG", "p4"))

msg['Subject'] = SUBJECT
msg['From'] = FROM
msg['To'] = TO


try:
    server = smtplib.SMTP()
    server.connect(HOST, 25)
    server.starttls()
    server.login(FROM, "password")
    server.sendmail(FROM, TO, msg.as_string())
    server.quit()
    print("发送成功")
except Exception, e:
    print("失败！原因："+str(e))
```



3.在邮件中添加附件
```python

```


- - -


##web服务器性能
###安装pycurl
###常见错误解决方法
1.  错误`__main__.ConfigurationError: Could not run curl-config: [Errno 2] No such file or directory`
```
Downloading/unpacking pycurl
  Running setup.py egg_info for package pycurl
    Traceback (most recent call last):
      File "<string>", line 16, in <module>
      File "/tmp/pip-build-root/pycurl/setup.py", line 563, in <module>
        ext = get_extension()
      File "/tmp/pip-build-root/pycurl/setup.py", line 368, in get_extension
        ext_config = ExtensionConfiguration()
      File "/tmp/pip-build-root/pycurl/setup.py", line 65, in __init__
        self.configure()
      File "/tmp/pip-build-root/pycurl/setup.py", line 100, in configure_unix
        raise ConfigurationError(msg)
    __main__.ConfigurationError: Could not run curl-config: [Errno 2] No such file or directory
    Complete output from command python setup.py egg_info:
    Traceback (most recent call last):

  File "<string>", line 16, in <module>
  File "/tmp/pip-build-root/pycurl/setup.py", line 563, in <module>
    ext = get_extension()
  File "/tmp/pip-build-root/pycurl/setup.py", line 368, in get_extension
    ext_config = ExtensionConfiguration()
  File "/tmp/pip-build-root/pycurl/setup.py", line 65, in __init__
    self.configure()
  File "/tmp/pip-build-root/pycurl/setup.py", line 100, in configure_unix
    raise ConfigurationError(msg)
__main__.ConfigurationError: Could not run curl-config: [Errno 2] No such file or directory
```

**解决方案**：

在debian系列操作系统中需要安装openssl

```sudo apt-get install libcurl4-openssl-dev```
