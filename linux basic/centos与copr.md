#在centos中使用copr

##安装copr
1.  官方安装帮助：[官网安装帮助文档](https://copr.fedoraproject.org/coprs/mosquito/myrepo/)
2.  我的安装步骤：
  + 添加源：`yum-config-manager --add-repo=https://copr.fedoraproject.org/coprs/mosquito/myrepo/repo/epel-$(rpm -E %?rhel)/mosquito-myrepo-epel-$(rpm -E %?rhel).repo `
  + 安装eple源：`yum install epel-release`
  + `sudo yum localinstall http://li.nux.ro/download/nux/dextop/el$(rpm -E %rhel)/x86_64/nux-dextop-release-0-2.el$(rpm -E %rhel).nux.noarch.rpm ` 官网还有来嗯个rpm包，但是我下在不了，那两个是`http://download1.rpmfusion.org/nonfree/el/updates/$(rpm -E %rhel)/x86_64/rpmfusion-nonfree-release-$(rpm -E %rhel)-1.noarch.rpm http://download1.rpmfusion.org/free/el/updates/$(rpm -E %rhel)/x86_64/rpmfusion-free-release-$(rpm -E %rhel)-1.noarch.rpm`

  >注意：某些源放在一起可能会产生冲突
  >解决办法：设置源的优先级，建议 base, updates, epel, mosquito-myrepo 优先级为 1，其他源 (rpmfusion, remi, Nux Dextop, RPMforge 等) 设为 2。这样会减少源之间的软件包冲突。
  >设置源的优先级，具体流程：
  > 1.  `yum install yum-plugin-priorities`
  >2.   `vim /etc/yum.repos.d/RepoName.repo `，该文档有多个如下格式的内容组成：
  ```[repo_name]
name= Repo Full Name
baseurl= Repo URL
enabled= 1(enable) 0(disable)
priority= priority number (range: 1-99, 1 high priority)```
  >3.   每块的最后面加上一行`priority=优先级的值`
