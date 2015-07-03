#vncserver 使用

##安装tigervnc
`yum isntall vnc-server`

##常规配置
配置文件所在的目录：`/etc/sysconfig/vncservers`

##常见问题
1.  vnc配置成功，在本地可以使用vncviewer 进入vncserver开的vnc服务，但是局域网其他主机无法登陆
  解决办法：此时应该是iptables防火墙设置的问题，修改防火墙设置，定义可信赖的public服务，以允许主机提供vncserver服务。
  具体步骤：
    + 使用`netstat -tulp|grep vnc`查看vnc占用的端口；或者使用`ps -ef| grep vnc`仔细查看后面的参数，会有端口现实，一般书59**
    + 使用iptable设置，使得iptables的规则允许端口对外开放。
