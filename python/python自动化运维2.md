#python自动化运维


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
