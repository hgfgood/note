#常用软件
##主要参考：
[https://copr.fedoraproject.org/coprs/mosquito/myrepo/](https://copr.fedoraproject.org/coprs/mosquito/myrepo/)

>**主要软件包括：QQ，搜狗输入法，百度王盘，deepin截图工具，歌词显示工具，deepinmusic，xwinddesktop（类似迅雷），为知笔记，有到笔记
豆瓣音乐，grub4doc等实用软件。**

##安装shadowsocks-qt
直接使用[fedora的安装源](https://copr.fedoraproject.org/coprs/librehat/shadowsocks/)：
1.  新建文件`/etc/yum.repos.d/libredhat-shadowsocks-fedora.repo`
2.  将下面的源输入到1中的文件```
[librehat-shadowsocks]
name=Copr repo for shadowsocks owned by librehat
baseurl=https://copr-be.cloud.fedoraproject.org/results/librehat/shadowsocks/fedora-$releasever-$basearch/
skip_if_unavailable=True
gpgcheck=1
gpgkey=https://copr-be.cloud.fedoraproject.org/results/librehat/shadowsocks/pubkey.gpg
enabled=1
```
>**注意:**
>此处需要修改上述内容的`baseurl`的值，将`$releasever`直接改为`21`（fedora的版本号），不然就会报错：`https://copr-be.cloud.fedoraproject.org/results/librehat/shadowsocks/fedora-7-x86_64/repodata/repomd.xml: [Errno 14] HTTPS Error 404 - Not Found`

3.  使用安装命令安装shadowsocks-qt5：`sudo yum install shadowsocks-qt5`
4.  安装完成后，将2中的文件的最后一行`enable`设置为`0`
