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
+ 初始化`MIMEText`对象作为附件：将本地的文件以读取二进制的方式，将文件内容用于初始化`MIMEText`对象，设置`MIMEText`的格式为`base64编码`，文字编码为`utf-8`
+ 设置`MIMEText`实例的`Content-Type`属性为`application/octet-stream`(专用来说明不知道文件类型的二进制流),
+ 设置`MIMEText`实例的`Content-Disposition`属性为`attachment;filename=文件名`，使得附件可以用来下载
+ 将`MIMEText`实例`attach`到MIMEMultipart对象中

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

msg = MIMEMultipart('related')

msgtext = MIMEText("""
<font>官网业务平均时延图表：<br><img src=\"cid:p1\" border =\"1\"><br>详细内附件图表</font>
""", "html", "utf-8")

msg.attach(msgtext)
msg.attach(addimg("/home/hgf/Pictures/program/logo/1.PNG", "p1"))

attach = MIMEText(open("/home/hgf/test.xlsx", 'rb').read(), "base64", "utf-8")
attach["Content-type"] = "application/octet-stream"
# 指定文件格式类型

# 指定ContentDisposition 属性值为attachement 则会出现自爱在保存对话框
# qqmail使用gb18030编码，为保证中文不会乱码，对文件名进行编码转换
attach["Content-Disposition"] = "attachment;filename=\"测试excel.xlsx\"".decode("utf-8").encode("gb18030")

msg.attach(attach)
msg['Subject'] = SUBJECT
msg['From'] = FROM
msg['To'] = TO

try:
    server = smtplib.SMTP()
    server.connect(HOST, 25)
    server.starttls()
    server.login(FROM, "passwprd")
    server.sendmail(FROM, TO, msg.as_string())
    server.quit()
    print("发送成功！")
except Exception, e:
    print("发送失败："+str(e))
```


- - -


###web服务器性能
####安装pycurl
1.	安裝curl：`sudo apt-get install curl`
2.	安裝openssl：`apt-get install openssl`
3.	安裝pycurl:`sudo pip install pycurl`

>**TIPS:**
>```python
>In [2]: pycurl.version
>Out[2]: 'PycURL/7.19.5.1 libcurl/7.35.0 OpenSSL/1.0.1f zlib/1.2.8 libidn/1.28 librtmp/2.3'
>```

####安裝问题
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

```
sudo apt-get install libcurl4-openssl-dev
```
####简单使用curl
```python
#! /usr/bin/python
# coding:utf-8

import pycurl


__author__ = 'hgf'


c = pycurl.Curl()
c.setopt(pycurl.URL, "http://www.baidu.com")
c.setopt(pycurl.CONNECTTIMEOUT, 5)
c.setopt(pycurl.NOPROGRESS, 0)
c.setopt(pycurl.FORBID_REUSE, 1)
f = open("a.txt",'wb')
c.setopt(pycurl.WRITEHEADER, f)
c.setopt(pycurl.WRITEDATA, f)
c.setopt(pycurl.DNS_CACHE_TIMEOUT, 30)

c.perform()
c.close()
```
>** 注意： **
>使用pycurl必须定义pycurl.URL的值，必须调用perform函数使pycurl生效，并且一般需要定义处理pycurl返回的结果。


####使用curl探测web服务质量
```python
#! /usr/bin/python
# coding:utf-8

import pycurl
import os
import sys

__author__="hgf"

URL = "http://www.baidu.com"
c = pycurl.Curl()
c.setopt(pycurl.URL, URL)
c.setopt(pycurl.CONNECTTIMEOUT, 5)
c.setopt(pycurl.TIMEOUT, 5)
c.setopt(pycurl.NOPROGRESS, 1)
c.setopt(pycurl.FORBID_REUSE, 1)
c.setopt(pycurl.DNS_CACHE_TIMEOUT, 30)
c.setopt(pycurl.MAXREDIRS, 1)

indexfile = open(os.path.dirname(os.path.realpath(__file__))+"/content.txt",'wb')

c.setopt(pycurl.WRITEHEADER, indexfile)
c.setopt(pycurl.WRITEDATA, indexfile)

try:
	c.perform()
except Exception, e:
	print ("error:"+str(e))
	indexfile.close()
	c.close()
	sys.exit()

NAMELOOKUP_TIME = c.getinfo(c.NAMELOOKUP_TIME)
CONNECT_TIME = c.getinfo(c.CONNECT_TIME)
PRETRANSFER_TIME = c.getinfo(c.PRETRANSFER_TIME)
STARTTRANSFER_TIME = c.getinfo(c.STARTTRANSFER_TIME)
TOTAL_TIME = c.getinfo(c.TOTAL_TIME)
HTTP_CODE = c.getinfo(c.HTTP_CODE)
SIZE_DOWNLOAD = c.getinfo(c.SIZE_DOWNLOAD)
HEADER_SIZE = c.getinfo(c.HEADER_SIZE)
SPEED_DOWNLOAD = c.getinfo(c.SPEED_DOWNLOAD)

print "HTTP状态码：%s" % HTTP_CODE
print "DNS解析时间：%.2f ms" % (NAMELOOKUP_TIME*1000)
print "建立连接时间：%.2f ms" % (CONNECT_TIME*1000)
print "准备传输时间： %.2f ms" % (PRETRANSFER_TIME*1000)
print "传输开始时间：%.2f ms" % (STARTTRANSFER_TIME*1000)
print "传输结束时间： %.2f ms" % ((TOTAL_TIME - STARTTRANSFER_TIME)*1000)
print "下载数据包大小： %.2f bytes/s" % SIZE_DOWNLOAD
print "HTTP 头部大小： %.2f byte" % HEADER_SIZE
print "下载速度：%.2f bytes/s" % SPEED_DOWNLOAD
indexfile.close()
c.close()

```


##定制报表

###python处理excel
####安装slsxwriter

`pip install XlsxWriter`

####XlsxWriter常见方法的使用

1.	Workbook类
	+ `Worlbook`对象代表了电子表格的整个文件，并且存储在磁盘上，
	+ 构造方法：`Workbook(filename[, option])`
	+ 主要的方法：
		- `add_Worksheet([sheetname])`:添加一个新的工作表，不定义`sheetname`时，默认为`sheet[工作表序号]`。
		- `add_format([proprties])`:创建一个新的格式对象来格式化单元格，参数`proprties`为dict类型， 指定一个单元格属性的字典。
			* 例如：`workbook.add_format({'bold':True})`,设置加粗的单元格。
			* 上述设置等价方式：`bold = workbook.add_format()`和`bold.set_bold()`
		- `add_chart(options)`:在工作表中创建一个图表对象，内部通过`insert_chart()`实现。option为dict类型。
		- `close()`:关闭工作表文件。

2.	WorkSheet类
	+ `write(row, col, *args)`:将普通数据写道单元格中，其中`(row, col)`为单元格在表格中的位置，起始位置为`(0,0)`;`×args`为要写入的数据内容， 可以为数字，字符串，格式对象。
	+ `set_row(row, height, cell_format, option)`:设置行单元格的属性，`row`指定行位置;`height`设置行高，单位为像素;`cell_format`为`format`类型，指定格式对象;参数`option`是dict类型，设置行`hiden`(隐藏),`level`(组合分级)，`collapsed`（折叠）。
	+ `set_column(first_col, last_col, wodth, cell_format, option)`:设置一列或多列单元格属性。参数`wodth`（float类型）设置列宽，`cell_format`和`options`同上。
	+ `insert_image(row, col, image[, option])`:插入图片到指定单元格，支持`PNG`,`JPEG`,`BMP`等图片格式。`image`（String类型）表示图片的路径。`options`（dist类型）：制定图片的位置、比例、链接URL等。
		- 例如：worksheet.insert_image('B5', 'img/python-logo.jpg', {'url':'http://python.org'})`
3.	Chart类
	+ 支持的图表类型包括面积，条形图，柱形图，饼状图，散点图，股票，雷达。
	+ 图表通过`worksheet`的`add_chart`方法创建图表。`chart = worksheet.add_chart({type,'column'})`创建一个柱形图。
>图表类型说明：
|类型关键字|图表类型|
|--------|-------|
|area|面积样式图表|
|bar|条形态|
|column|柱形图|
|line|条形图|
|pie|饼状图|
|scatter|散点图|
|stock|股票图|
|radar|雷达图|

	+ 通过`insert_chart()`方法将图标插入到指定的地方。
	+ 主要的方法：
		- `chat.add_series(options)`:添加一个数据系列到图表。
			* 例子：
			```python
			chat.add_series({
     		   	'categories':	'=Sheet1!$a$1:$A$5',
     	       'values':		'=Sheet1!$B$1:$B$5'，
     	       'line':			{'color':'red'},
    	    })
```
>说明：
>`add_series`最长见的option是
>`categories`：表示图表标签的范围[将表格中的对应位置的内容作为图表的横轴];
>`value`:图表的数据范围[表格中的范围内的数据作为画图的数据]
>`line`：图标的线条属性，包括颜色，宽度等。
>`name`:图例项，[一个图的多种内容的区分]
		- `set_x_axis(options)`:设置X轴选项，
			* 例子
			```python
            char.set_x_axis({
            	'name':	'Earning_per_!Quater',#设置X轴标题名字
                'name_font':	{'size':14, 'bold':True},#设置X轴标题字体
                'num_foont':	{'italic':True},#设置X轴数字字体
            })
```
		- `set_size(options)`:设置图表大小。例如`chart.set_size({'width':720, 'height':576})`
		- `set_title`:设置图表的标题。`chart.set_title({'name':'Year End Result'})`
		- `set_styke(style_id))':`style_id`为不同数字代表不同的样式。
		- `set_table(options)`:设置X轴为数字表格样式

####实例：定制自动化业务流量报表


###python与rrdtool结合

#### 安装rrdtool
`pip install python-rrdtool`
>可能的错误：
>1.	I found a copy of pkgconfig, but there is no libxml-2.0.pc file around.
>You may want to set the PKG_CONFIG_PATH variable to point to its
>location.
>原因：没有安装libxml
>解决方案：`sudo apt-get install libxml2` `sudo apt-get install libxml2-dev`
>2.	出现`cannot find -lrrd`
>原因：库文件没有导入到ld检索目录中，或者是库文件是在so后面加上了序号，导致找不到库文件
>解决方案：只需要使用ln命令，将带号码的so文件软链接到不带序号的库文件，如`sudo ln -sv librrd.so.4 librrd.so`

##python与系统安全
###病毒扫描

###nmap端口扫描
在使用python-nmap前，需要在操作系统上安装namp：`yum install namp`
1. 模块说明
  + PortScanner类【nmap端口扫描的封装】
    * `scan(self, host='127.0.0.1', ports=None, arguments='-sV')`：制定扫描的主机端口，nmap命令行扫描的参数。其中`host`的参数形式可以是域名（'scanne.nmap.org'），网段（'192.168.0-255.1-127'或'192.168.128.20/20'），IP地址；ports表示扫描的端口，可以用`22,53,110,143-4564`来表示；arguments为字符串类型，是nmap命令行下的扫描参数。
    * `comman_line(self)`：返回扫描方法对应的命令行下面的nmap命令。
    * `scaninfo(self)`：扫描的信息，字典类型
    * `all_hosts(self)`：返回nmap扫描的主机清单，格式为list
    * `hostname(self)`：返回扫描对西那个的名字
    * `state(self)`：返回扫描对象的状态(主要包括up，down，unknow，skipped)
    * `all_protocals(self)`：返回扫描协议
    * `all_tcp(self)`：返回TCP协议端口
    * `tcp(self,port)`：返回TCP协议port端口的信息
  + PortScannerHostDict类【存储与访问主机的扫描结果】
2. 示例
  ```python

  #! /usr/bin/python
  # -*- coding:utf-8 -*-

  import nmap
  import sys

  __author__ = 'hgf'

  def detailinfo(hosts, ports):
      '''
      使用nmap测试hosts中的所有的ports，并输出详细的信息
      :param hosts: 所有主机
      :param ports:所有端口号
      :return:
      '''
      try:
          nm.scan(hosts = hosts, arguments='-v -sS -p'+ports)
      except Exception,e:
          print("Scan error:"+ str(e))

      for host in nm.all_hosts():
          print('-------------------------------------------------------------------------------------------------------')
          print('Host: %s (%s)'% (host, nm[hosts].hostname()))
          print('State: %s' % nm[host].state())
          for proto in nm[host].all_protocols():
              print('------------------------------------------------')
              print('Protocal: %s'% proto)

              iport = nm[host][proto].keys()
              iport.sort()
              for port in iport:
                  print('Port: %s \tstate: %s' %(port, nm[host][proto][port]['state']))

  def printcsv(nm):
      '''
      将nmap的结果以excel表的格式输出
      :param nm: namp实例
      :return:
      '''
      print('-----------------------------------------------------------------------------------------------------------')
      print('print result as csv')
      print(nm.csv())

  def pingsweep(hosts,ports):
      '''
      根据ports端口，查询网段内存活主机
      :param hosts:网段
      :param ports:端口
      :return:
      '''
      nm.scan(hosts=hosts, arguments='-n -sP -PE -PA'+ports)
      host_list=[(x,nm[x]['status']['state']) for x in nm.all_hosts()]
      for host, state in host_list:
          print('{0}:{1}'.format(host,state))

  def call_back(host, scan_result):
      print("----------------------------------")
      print host, scan_result
  def arsynNmap(hosts):
      '''
      异步Nmap
      :param hosts:
      :return:
      '''
      nma = nmap.PortScannerAsync()
      nma.scan(hosts=hosts, arguments='-sP', callback=call_back)
      while nma.still_scanning():
          print('wait')
          nma.wait(2)
          # do some other things

  scan_row=[]
  input_data = raw_input("Please input hosts and ports:")
  scan_row = input_data.split(' ')
  if len(scan_row)!=2:
      print("input error, example input \"192.168.1.0/24 80,433-560\"")
      sys.exit(0)
  hosts = scan_row[0]
  ports = scan_row[1]

  try:
      nm = nmap.PortScanner()
  except nmap.PortScannerError:
      print("Nmap not found ", sys.exc_info()[0])
      sys.exit(0)
  except:
      print("Unexcepted error!")
      sys.exit(0)

  arsynNmap(hosts)
  ```

  ##pexpect
  纯python编写的系统批量运维管理器。

  ###安装
  `sudo pip install pexpect`

  ###pexpect使用
  pexpect主要有两大功能：

  ####run方法
  `run`方法主要替代原来的'os.system()'

  ####spawn 类
  `spawn`主要实现了自动交互的功能。
  > **注意：**
  >`spawn`；类不会解析shell命令中的元字符，包括重定向`>`，管道`|`，或者是通配符`*`，但是我们可以使用给`/bin/bash`传递参数的形式使用元字符。
  >例如：`pexpect.spawn('/bin/bash -c "ls -al | grep LOG > logs.txt"')`

  * pexpect日志输出到文件：```
  child = pexpect.spawn('some_command')
  fout = file('mylog.txt','w')
  child.logfile(fout)
  ````

  * pexpect日志输出到标准输出流：```
  child = pexpect.spawn('some_command')
  child.logfile = sys.stout
  ````

  ####使用pexpect的注意事项
  1.  注意使用`scp`时，传送文件的权限，当使用pexpect的命令中，包含用scp传送权限比较高，或者传送文件的所有者不是运行pexpect程序的人的时候，需要考虑处理文件权限的问题。特别是传送系统配置文件时，就算root运行程序也不能传送文件成功。
  2. 一般的使用步骤：
    + 保证目录下有那个文件
    * 保证执行py的用户有那个传送文件的权限

  ##paramiko
  基于python实现的SSH2安全连接，支持认证及密钥方式，可以实现远程命令执行，文件传输，中间ssh代理等。

  ###安装paramiko
  `sudo pip install paramiko`

  ###paramiko的简单测试
  ```python
  #/usr/bin/python
  # coding:utf-8
  import paramiko
  import sys

  __author__='hgf'

  try:
      data =  raw_input("Please input hostname username and password:").split()
      if len(data)!=3:
          print("input error! make sure your input like \"192.168.1.1 root 123456\"")
          sys.exit(0)
  except Exception,e:
      print("Exception occourred!")
      print (str(e))
  hostname = data[0]
  username = data[1]
  password = data[2]

  paramiko.util.log_to_file('sys.log')

  ssh = paramiko.SSHClient()
  ssh.load_system_host_keys()

  ssh.connect(hostname = hostname, username = username, password = password)
  stdin, stdout, stderr = ssh.exec_command('free -m')
  print stdout.read()
  ssh.close()

  ```

  ###paramiko的核心组件
  1.  SSHClient
    * connect方法
        + `connect(self, hostname, port=22, username=None, password=None, pkey=None, key_filename=None, timeout=None, allow=True, look_for_keys=True. compress=False)`
        + 各个参数的含义：
          - `hostname`：（str类型）目的主机
          - `port`：（int类型）端口号
          - `username`：（str类型）目的主机的用户名（默认与当前的本地主机用户名相同）
          - `password`：（str类型）密码用于身份校验或解锁私钥
          - `pkey`：（PKey类型）私钥方式进行验证
          - `key_filename`：（list(str))或者是str类型）一个文件名或是文件列表，用于私钥的身分验证
          - `timeout`：（int类型）设定链接的超时信息
          - `allow_agent`：(bool类型)设置为False时，禁止连接到SSH代理
          - `look_for_keys`：(bool类型)False时禁止在～/.ssh目录中搜索私钥文件
          - `compress`：(bool类型) 设置为True打开压缩
    * `exec_command`方法：远程执行命令的方法，输入输出流为标准的的输入输出流，错误流（stdin，stdout，stderr）
        + `exec_command(self, command, bufsize=-1)`
        + `command`:(str类型)，执行的命令
    * `load_system_host_keys`方法，指定远程主机的公钥记录文件（默认为`~/.ssh/known_hosts`）
        + `load_system_host_keys(self, filename=None)`
    * `set_missing_host_key_policy`方法：设置远程主机没有本地主机密钥或Hostskye的情况时的策略，目前支持3种。
        + `AutoAddPolicy`，自动添加主机名及主机密钥到本地hostsKeys对象（具体时那个文件？？？？），并保存。不依赖于`load_system_host_keys()`的配置。
        + `RejectPolicy`，自动拒绝未知主机名和密钥， 依赖`load_system_host_keys`的配置。
        + `WarningPolicy`，用于记录一个位置的主机名和密钥的python警告，并接受。功能上与`AutoAddPolicy`相似但是未知主机会有警告。

        > 使用方法：
        >```python
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        >```

  >**说明：**
  >可以通过`SSHClient`对象的`invoke_shell`方法获取`paramiko`的`Channel`，开启命令调用.即使用`Channel`的`send()`方法，可以发送一系列的shell命令。例如：
  >```python
  ssh = paramiko.SSHClient()
  ssh.connect(hostname,username,password)
  channel = ssh.invoke_shell()
  channel.send('ls')
  >```

  2.  SFTPClient
    * `from_transport`方法:创建爱哪一个已经连通的SFTP客户端通道
        + `from_transport(self, t)`
        + 参数`t`表和isyige已经验证过的传输对象(`paramiko.Transport`对象)
        + 例子：```python
        t = paramiko.Transport(('192.168.1.22',22))
        t.connect(username='root', password = '123456')
        sftp = paramiko.SFTPClient.from_transport(t)
        ```
    * `put`方法：上传本地文件到远程SFTP服务端
        + `put(self, localpath, remotepath, callback=None, confirm=True)`
        + 参数说明：
          - `localpath`: （str类型）需要上传的本地文件
          - `remotepath`：（str类型）远程路径
          - `callback(function (int, int))`：获取已经接收的字节数及宗的传输字节数， 以便毁掉函数调用
          - `confirm`：文件上传完毕后是否使用`stat()`方法，以便确认文件的大小
        >**注意：**
        >`remotepath`必须是文件路径+文件名+文件扩展名的完整形式，不能只指定文件夹的名字

        + 例子：
        ```python
        localpath = '/home/access.log'
        remotepath = '/data/logs/access.log'
        sftp.put(localpath, remotepath)
        ```
    * get方法:从远程sftp服务端下载文件到本地
          + `get(self, remotepath, localpath, callback=None)`
          + 参数说明：
            - `remotepath`：（str类型）远程文件路径
            - `localpath`: （str类型）本地保存路径
            - `callback(function (int, int))`：获取已经接收的字节数及宗的传输字节数， 以便毁掉函数调用
            >**注意：**
            >`localpath`必须是文件路径+文件名+文件扩展名的完整形式，不能只指定文件夹的名字
          + 例子：
          ```python
          localpath = '/home/access.log'
          remotepath = '/data/logs/access.log'
          sftp.put(localpath, remotepath)
          ```
    * `mkdir`：在远程服务器上创建文件夹
    * `remove`：删除SFTP服务端指定的目录
    * `rename`：重命名SFTP服务端的文件或目录
    * `stat`：获取SFTP服务端指定文件的信息
    * `listdir`：获取SFTP服务端指定的目录列表，以python list的形式返回。

      ```python
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
      ```

  ##Fabric

  `Fabric`在`paramiko`的基础上，做了更高一层的封装

  ###安装

  `pip install fabric`

  ###全局属性的设置

  与全局属性有关的是`env`对象。


  ###常用API


  ###例子1
  **查看本地与远程主机信息**

  ###例子2
  **动态获取远程目录列表**

  ###例子3

  **网关模式文件的上传**


  ##编写webserver

  ###python处理命令行提示

  python主要是使用optparse处理命令行的提示功能，并且响应命令行的输入参数。
  例子：
  ```python
  MSG_USAGE = "program [-v] [-h]"
  parser = OptionParser(MSG_USAGE)
  parser.add_option("-v", "--version", action="store_true", dest="verbose", help="描述命令参数的用途")
  opts, args = parser.parse_args()

  if opts.verbose:
    # 执行满足参数-v后的运行程序
    print "输出系统的版本"
    sys.exit()
  ```
  ###python处理配置文件

  python主要是使用configobj库来处理配置文件。
  详细的使用请看《python配置文件configobj使用》

  ###BaseHTTPServer.py源码分析
  `BaseHTTPServer.py`源码分析主要是方便理解如何自己编写webserver。

  从`SocketServer.py`分析中可以知道其设计思想是将socket编程的监听循环和客户端处理划分成`Server`类和`RequestHandler`类，而`BaseHTTPServer`是基于`SocketServer`基础之上的，因此可以知道`BaseHTTPServer`就是分别扩展`Server`类和`RequestHandler`类。`BaseHTTPServer`实现了一个简单的`HTTP Server`，可以知道主要工作应该是扩展`RequestHandler`的功能，处理客户端的`HTTP`请求，具体包括`HTTP`协议解析，给客户端返回`HTTP`响应，日志记录等功能。

  1.  HTTPServer

  该类只是简单包装了`SocketServer`中的`TCPServer`类

  2.  BaseHTTPRequestHandler

  类定义:
  `class BaseHTTPRequestHandler(SocketServer.StreamRequestHandler):`

  扩展`RequestHandler`需要覆盖一个接口`handler()`，定义如下：
  ```python
  def handle(self):
      """Handle multiple requests if necessary."""
      self.close_connection = 1
      self.handle_one_request()
      while not self.close_connection:
          self.handle_one_request()
  ```
  主要处理的是HTTP是否保持连接的问题，如果保持连接就持续处理客户请求，否则就结束了。

  `handle_one_request()`比较重要语句：
  ```python
  self.raw_requestline = self.rfile.readline(65537)
  self.parse_request()
  mname = 'do_' + self.command
  if not hasattr(self, mname)
      self.send_error(501, "Unsupported method (%r)" % self.command)
      return
  method = getattr(self, mname)
  method()
  self.wfile.flush() #actually send the response if not already done.
  ```
  * 读取第一行`raw_requestline`，一般格式应该是：`COMMAND PATH VERSION\r\n`；
  * 解析请求，`parse_request()`主要的代码都在处理`raw_requestline`，最终得到`self.command`, `self.path`, `self.request_version`几个变量，然后就是利用`mimetools.Message`解析头部。
  * 后面几行代码意思是根据HTTP方法获取对应处理函数，其实就是根据GET或POST请求调用对应的`do_GET()`或`do_POST()`方法，然后刷新输出。

  下面还有几个的函数，功能都比较简单：
  ```python
  def send_error(self, code, message=None):
  def send_response(self, code, message=None):
  def send_header(self, keyword, value):
  def end_headers(self):
  def log_request(self, code='-', size='-'):
  def log_error(self, format, *args):
  def log_message(self, format, *args):
  ```
  总结：可以看到，`BaseHTTPRequestHandler`主要实现了客户端HTTP请求解析，以及一些辅助功能，如日志记录、错误处理、发送响应代码等。
  但是还没有实现如何执行HTTP请求，简单来说就是还需要实现诸如`do_GET()`,`do_POST()`等函数，具体执行对应的HTTP命令。

  ###HTTP协议返状态码含义
  1.  1xx 状态码

    表示临时响应并需要请求者继续执行操作的状态码。

    * `100（继续）` 请求者应当继续提出请求。服务器返回此代码表示已收到请求的第一部分，正在等待其余部分。
    * `101（切换协议）` 请求者已要求服务器切换协议，服务器已确认并准备切换。

  2.  2xx 状态码

    表示成功处理了请求的状态码。

    * `200（成功）` 服务器已成功处理了请求。通常，这表示服务器提供了请求的网页。如果针对您的 robots.txt 文件显示此状态码，则表示 Googlebot 已成功检索到该文件。
    * `201（已创建）` 请求成功并且服务器创建了新的资源。
    * `202（已接受）` 服务器已接受请求，但尚未处理。
    * `203（非授权信息）` 服务器已成功处理了请求，但返回的信息可能来自另一来源。
    * `204（无内容）` 服务器成功处理了请求，但没有返回任何内容。
    * `205（重置内容）` 服务器成功处理了请求，但没有返回任何内容。与 204 响应不同，此响应要求请求者重置文档视图（例如，清除表单内容以输入新内容）。
    * `206（部分内容）` 服务器成功处理了部分 GET 请求。

  3.  3xx 状态码

    要完成请求，需要进一步操作。通常，这些**状态码用来重定向**。建议您在每次请求中使用重定向不要超过 5 次。您可以使用网站管理员工具查看一下 Googlebot 在抓取重定向网页时是否遇到问题。诊断下的网络抓取页列出了由于重定向错误导致 Googlebot 无法抓取的网址。

    * `300（多种选择）` 针对请求，服务器可执行多种操作。服务器可根据请求者 (`user-agent`) 选择一项操作，或提供操作列表供请求者选择。
    * `301（永久移动）` 请求的网页已永久移动到新位置。服务器返回此响应（对 GET 或 HEAD 请求的响应）时，会自动将请求者转到新位置。您应使用此代码告诉 Googlebot 某个网页或网站已永久移动到新位置。
    * `302（临时移动）` 服务器目前从不同位置的网页响应请求，但申请人应当继续使用原有位置来响应以后的请求。此代码与响应 GET 和 HEAD 请求的 301 代码类似，会自动将请求者转到不同的位置，但不应使用此代码来告诉 Googlebot 页面或网站已经移动，因为 Googlebot 要继续抓取原来的位置并编制索引。
    * `303（查看其他位置）` 请求者应当对不同的位置使用单独的 GET 请求来检索响应时，服务器返回此代码。对于除 HEAD 之外的所有请求，服务器会自动转到其他位置。
    * `304（未修改）` 自从上次请求后，请求的网页未修改过。服务器返回此响应时，不会返回网页内容。如果网页自请求者上次请求后再也没有更改过，您应当将服务器配置为返回此响应（称为 `If-Modified-Since HTTP` 标头）。由于服务器可以告诉 Googlebot 自从上次抓取后网页没有变更，因此可节省带宽和开销。
    * `305（使用代理）` 请求者只能使用代理访问请求的网页。如果服务器返回此响应，还表示请求者应当使用代理。
    * `307（临时重定向）` 服务器目前从不同位置的网页响应请求，但请求者应当继续使用原有位置来响应以后的请求。此代码与响应 GET 和 HEAD 请求的 301 代码类似，会自动将请求者转到不同的位置，但您不应使用此代码来告诉 Googlebot 某个网页或网站已经移动，因为 Googlebot 会继续抓取原有位置并编制索引。

  4.  4xx 状态码

    这些状态码表示请求可能出错，这妨碍了服务器的处理。

    * `400（错误请求）` 服务器不理解请求的语法。
    * `401（身份验证错误）` 此页要求授权。您可能不希望将此网页纳入索引。如果您的 Sitemap 中列出该网页，您可以将其删除。但如果您将其保留在您的 Sitemap 中，我们就不会抓取或索引该网页（尽管该网页将继续保持错误状态在此处列出）。如果我们将其作为搜索抓取的一部分抓取，您可以在我们的网站管理员信息中查阅其原因。
    * `403（禁止）` 服务器拒绝请求。如果您在 Googlebot 尝试抓取您网站上的有效网页时看到此状态码，可能是您的服务器或主机拒绝 Googlebot 访问。
    * `404（未找到）` 服务器找不到请求的网页。例如，对于服务器上不存在的网页经常会返回此代码。
    * `405（方法禁用）` 禁用请求中指定的方法。
    * `406（不接受）` 无法使用请求的内容特性响应请求的网页。
    * `407（需要代理授权）` 此状态码与 401 类似，但指定请求者必须授权使用代理。如果服务器返回此响应，还表示请求者应当使用代理。
    * `408（请求超时）` 服务器等候请求时发生超时。
    * `409（冲突）` 服务器在完成请求时发生冲突。服务器必须在响应中包含有关冲突的信息。服务器在响应与前一个请求相冲突的 PUT 请求时可能会返回此代码，以及两个请求的差异列表。
    * `410（已删除）` 请求的资源永久删除后，服务器返回此响应。该代码与 404（未找到）代码相似，但在资源以前存在而现在不存在的情况下，有时会用来替代 404 代码。如果资源已永久删除，您应当使用 301 指定资源的新位置。
    * `411（需要有效长度）` 服务器不接受不含有效内容长度标头字段的请求。
    * `412（未满足前提条件）` 服务器未满足请求者在请求中设置的其中一个前提条件。
    * `413（请求实体过大）` 服务器无法处理请求，因为请求实体过大，超出服务器的处理能力。
    * `414（请求的 URI 过长）` 请求的 URI（通常为网址）过长，服务器无法处理。
    * `415（不支持的媒体类型）` 请求的格式不受请求页面的支持。
    * `416（请求范围不符合要求）` 如果页面无法提供请求的范围，则服务器会返回此状态码。
    * `417（未满足期望值）` 服务器未满足"期望"请求标头字段的要求。

  5.  5xx 状态码

    这些状态码表示服务器在处理请求时发生内部错误。这些错误可能是服务器本身的错误，而不是请求出错。

    * `500（服务器内部错误）` 服务器遇到错误，无法完成请求。
    * `501（尚未实施）` 服务器不具备完成请求的功能。例如，服务器无法识别请求方法时则会返回此代码。
    * `502（错误网关）` 服务器作为网关或代理，从上游服务器收到无效响应。
    * `503（服务不可用）` 服务器目前无法使用（由于超载或停机维护）。通常，这只是暂时状态。
    * `504（网关超时）` 服务器作为网关或代理，但是没有及时从上游服务器收到请求。
    *  `505（HTTP 版本不受支持）` 服务器不支持请求中所用的 HTTP 协议版本。

  ###自己的webserver hgfserver代码
