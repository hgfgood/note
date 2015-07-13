#强大的linux自带工具

##rsync

###常见的使用方法
1.  传文件
`rsync filenamepath user@ip:/path`

2.  传文件夹
`rsync -r documents user@ip:/path`

3.  自动过滤已经传输好的
`rsync -t file user@ip:/path`

4.  备份软链接
`-l` :实现只备份软链接本身，不会“follow link”到指向的实体文件。
`-L`:“follow link”到指向的实体文件。
