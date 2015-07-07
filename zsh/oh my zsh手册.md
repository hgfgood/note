#oh my Zsh使用手册
[TOC]
##简单使用oh my zsh
###安装oh my Zsh
1.	安装zsh
2.	安装curl或者wget
3.	下载并安装oh my zsh:
+ curl 下载方式`curl -L https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh | sh`
+ wget下载`wget https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh -O - | shoh`

###使用oh my zsh插件

1.	编辑`~/.zshr.c`文件，添加一行使插件在加载oh my zsh时初始化，格式`plugins=(git bundler osx rake ruby)`
2.	查看plugins的README文件，看看怎么使用插件
3.	有名的插件有：
	+ git：当前目录如果是受git控制的目录下，会显示[git]，对很多git 命令进行了简化，例如`gco=git checkout`,`gd=git diff`,`gst=git status`,`g=git`
	+ textmate：`mr`创建ruby的框架项目，`tx filename` 使用`textmate`打开文件
	+ osx：tab的增强，使用`quick-look filename`直接预览文件
	+ autojump：强大的文件夹跳转工具。

4.	插件的使用方法
	修改`～/.zshrc`文件，在文件末尾加上：
	+ 配置sublime默认打开python文件：`aliaa -s py=st`
	+ 配置sublime默认打开markdown文件：`aliaa -s md=st`

>**上面所有的配置做好以后，需要执行`source ~/.zshrc`，是的配置的效果显示出来**

###主题
1.	在[wiki可以查看主题的截图](https://github.com/robbyrussell/oh-my-zsh/wiki/Themes)，找到自己喜欢的主题
2.	在`~/.zshr.c`文件中有一个关于主题设置的参数，例如`ZSH_THEME=“robbyrussell”`，如果想使用自己喜欢的主题，只需要将这行的变量的值改为自己喜欢的主题的名字

###自定义安装oh my zsh
1.	默认安装路径`~/.oh-my-zsh`
2.	修改安装路径，
+ 方法一：在安装前，使用`export ZSH=/your/path`
+ 方法二：在安装时，采用管道命令安装`curl -L https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh | ZSH=~/.dotfiles/zsh sh`

###手动安装
+ clone oh my zsh的repository
`git clone git://github.com/robbyrussell/oh-my-zsh.git ~/.oh-my-zsh`

+ 可选项，备份已经存在的安装文件和配置
`cp ~/.zshr ~/.zshr.orig`

+ 创建一个新的zsh配置文件，可以通过简单的复制一个程序提供的模板配置文件
`cp ~/.oh-my-zsh/templates/zshrc.zsh-template ~/.zshrc`

+ 修改默认shell
`chsh -s /bin/zsh`

+ 初始化新的配置文件


###自定义插件
1.	在`custom/`文件夹中添加一个`.zsh`类型文件
2.	如果有许多功能添加或改变，可以将在`custom/plugins`文件夹中加入一个`abccryzeae.plugins.zsh`文件（其中abccryzeae是文件名）
3.	如果想中写Oh my zsh提供的插件，则在`custom/plugins`文件夹中定义一个与要修改插件同名的插件，这样zsh shell就会加载自定义的插件，而不是在`plugins`里面的插件

###升级
1.	自动升级管理：
	在`~/.zshrc`中有类似这样的字段`DISABLE_UPDATE_PROMPT=true`,想取消自动升级，可以在`~/.zshr`中添加`DISABLE_AUTO_UPDATE=true`
2.	手动升级：
	运行命令:`upgrade_oh_my_zsh`

###卸载oh my zsh
直接在终端中，运行`uninstall_oh_my_zsh`,既可以卸载。


##oh my zsh高级模式---oh-my-fish

###安装
	`curl -L https://github.com/oh-my-fish/oh-my-fish/raw/master/tools/install.fish | fish`

###主题设置
在fish的模式下，输入`theme --help`

###设置oh-my-fish
oh-my-fish的配置文件为`/home/username/.config/fish/config.fish`,
>注意：在添加完主题和茶间后，运行`omf install`来自东下在安装相应的插件和主题。

##power_line

###[安装](https://powerline.readthedocs.org/en/latest/installation/linux.html#font-installation)
1.	`pip install --user powerline-status`或者下载最新的power——line版本的字体。
2.	将想要的字体移动到``～/.fonts`目录，例如：`mv PowerlineSymbols.otf ~/.fonts/`
3.	更新字体缓存,`fc-cache -vf ~/.fonts/`
