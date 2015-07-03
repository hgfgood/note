#linux 修改默认java jdk

1.	安装jdk
	从oracle 官网下载jdk，安装，确认安装位置。
	>**注意**:rpm包的安装位置是：`/usr/java/`目录下
	
2.	将jdk的相关参数添加到环境变量中
	```
		export JAVA_HOME=/usr/java/jdk1.8.0_20
		export CLASSPATH=.:$JAVA_HOME/jre/lib/rt.jar:$JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar
		export PATH=$PATH:$JAVA_HOME/bin
	```
3.	使用`update-alternatives`命令修改默认jdk
	使用命令`sudo update-alternatives --install /usr/bin/javap javap /usr/java/jdk1.8.0_20/bin/javap 300`安装可选项
	使用命令`sudo update-alternatives --config java`选择需要使用的java版本。
	>**TIPS**:其他java相关的同3一样设置。