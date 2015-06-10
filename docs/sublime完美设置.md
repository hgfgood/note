#sublime text完美配置

[TOC]

##安装包管理工具
ctrl+~（Esc下面那个键）同时按住，弹出一个输入框，粘贴下面代码，回车。
>**sublime text3:**
>`import urllib.request,os; pf = 'Package Control.sublime-package'; ipp = sublime.installed_packages_path(); urllib.request.install_opener( urllib.request.build_opener( urllib.request.ProxyHandler()) ); open(os.path.join(ipp, pf), 'wb').write(urllib.request.urlopen( 'http://sublime.wbond.net/' + pf.replace(' ','%20')).read())`
>
>**sublime text2:**
>`import urllib2,os; pf='Package Control.sublime-package'; ipp = sublime.installed_packages_path(); os.makedirs( ipp ) if not os.path.exists(ipp) else None; urllib2.install_opener( urllib2.build_opener( urllib2.ProxyHandler( ))); open( os.path.join( ipp, pf), 'wb' ).write( urllib2.urlopen( 'http://sublime.wbond.net/' +pf.replace( ' ','%20' )).read()); print( 'Please restart Sublime Text to finish installation')

>**TIPS:**
>如果包管理被墙了，修改hosts文件，加入下面这一句话：
>++50.116.34.243 sublime.wbond.net++
>*（ubuntu下面的hosts文件放在`/etc/hosts`，windows的在系统盘-》system32-》etc-》hosts）*

##有用的插件
1. prettify
	HTML、CSS、JS、JSON.....Ctrl+Shift+H 一键就能格式化了
2. ConvertToUTF8：解决sublimetext不支持中文的特性
3. Emmet
	使用HTML，CSS必备