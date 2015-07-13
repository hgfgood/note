#vim编辑器使用

##快捷配置使用
[spf13](https://github.com/spf13/spf13-vim),自动下载并配置vim。
1.  安装：`curl https://j.mp/spf13-vim3 -L > spf13-vim.sh && sh spf13-vim.sh`
2.  更新：`curl https://j.mp/spf13-vim3 -L -o - | sh`

###spf13使用

1.  系统自带的`<leader`健是`\`，spf13的`<leader`健是`,`，可以在配置文件中修改`let mapleader`的值，来修改`<leader`健。
2.  快捷键
  * HTML-AutoCloseTag
    + `>`:自动闭合html标签
  * CtrlP 快速查找文件
    + `Ctrl P`:快速查找文件
    + `Ctrl j`:向下选择文件
    + `Ctrl k`:向上选择文件
  * NERDTree
    + `ctrl e `打开nerdtree
    + `q`:离开nerdree
    + `o`:显示子目录
    + `x`:关闭子目录
    + `c`:当前子目录作为根
    
##vim插件管理器
[pathogen](https://github.com/tpope/vim-pathogen)是一款方便管理vim插件的vim插件，使其他的插件在各自的目录中运行，互不影响，方便卸载。
###安装pathogen
1.  下载插件
```shell
mkdir -p ~/.vim/autoload ~/.vim/bundle && \
curl -LSso ~/.vim/autoload/pathogen.vim https://tpo.pe/pathogen.vim
```
2.  使插件生效
在`～/.vimrc`中添加如下语句（如果没有`～/.vimrc`文件，使用`vim ～/.vimrc`创建文件），添加的语句：
  ```
  execute pathogen#infect()
  # 如果没有 ~/.vimrc 文件，还需要添加以下几句
  syntax on
  filetype plugin indent on
  ```
3.  以后要安装什么插件，只需要把插件安装在 `~/.vim/bundle`子目录下，就可以了。
例如安装`sensible`：
```
cd ~/.vim/bundle
git clone git://github.com/tpope/vim-sensible.git
```
4.  自定义插件安装目录
在`～/.vimrc`中，修改原来的`  execute pathogen#infect()`为`  execute pathogen#infect('direcotry/{}')`，也可以在这个配置语句中添加多个目录，也可添加不再`~/.vim`目录下的路径作为插件安装的位置。
例如：`execute pathogen#infect('bundle/{}', '~/src/vim/bundle/{}')`
