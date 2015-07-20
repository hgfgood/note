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
