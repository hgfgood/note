#python打包和分发

##setuptools打包

都是在hello目录下新建setup.py的文件。

distutils虽然在python的标准库中，但是已经停止开发了，setuptools提供向distutils的兼容，并且有一些有用的，有效率的命令。

常用的setuptools打包命令有：
+ 源码打包(tar.gz):`python setup.py sdist`
+ 可执行文件打包
    -  windows下使用的格式：`python setup.py bdist_wininst`
    - linux redhat系列格式：`python setup.py bdist_rpm`
    - 通用egg格式：`python setup.py bdist`
    - 通用whell格式：`python setup.py bdist_wheel`


1.  使用distutils

    例子：
    ```python
    from distutils.core import setup

    setup(name="hgf",
            version="0.1",
            description="brief introduce",
            author="hgf",
            author_email="hgf@a.com",
            packages=['hello']
    )

    ```
    >说明：
    1.  使用distutils打包python，需要知名的参数有`name`，`author`，`version`，`url`


2.  使用setuptools

    例子：
    ```python
    import setuptools

    setuptools.setup(
        name="hello",
        version="0.1",
        author="hgf",
        author_email="hgfgood@gmail.com",
        description="this is a hello test about setuptools",
        license="GPL",
        package=["test"],
        entry_point={
            "consol_script":[
                "sayhello = test.hello:say_hello"
            ]
        }
    )

    ```
    >说明，可以不用entry_point

##使用pbr打包

pbr在`setuptools`的基础上做了一些改进：
1.  基于`requirements.txt`的自动依赖安装
2.  利用`sphinx`实现文档自动化
3.  基于git history自动生成 `authors` 和 `ChangeLog`
4.  基于git 自动创建文件列表
5.  基于git tags的版本管理
6.  基于setuptools的思想，将配置信息全部放到`setup.cfg`文件里面

pbr的打包例子：

`setup.py`:
```python
import setuptools

setuptools.setup(setup_requires=['pbr'],pbr=True)

```

`setup.cfg`
```
[metadata]
name=hello
author=hgf
author_email=hgfdodo@gmail.com
licens=MIT
description-file=README.rst
requires-python= >=2.6
classifier=
    Development Status :: 4 - Beta
    Environment :: Console
    Intended Audience :: Developers
    Intended Audience :: Information Technology
    license ::OSI Approved :: Apache Software license
    Operating System :: Os Independent
    Programming Lauguage :: python

[files]
packages =
    test

```
>注意：使用pbr打包，源程序一定要**使用git**，并且源码的根目录下一定要有 ** `README.rst` ** 文件


##使用pypi服务器共享包
1.  在`https://testpypi.python.org/pypi`上注册一个自己的帐号
2.  在开发主机的`~/.pypi`中加入作者信息
```
[distutils]
index-server =
    pypi
    testpypi

[pypi]
username = hgfgood
password = password

[testpypi]
username = hgfgood
password = password
repository = https://testpypi.python.org/pypi
```
>说明：
        1.  设置索引服务器
        2.  分别写索引服务器的用户名密码
        3.  testpypi是测试服务器

3.  在pypi的索引中注册自己的项目
`python setup.py register -r hello`

4.  上传分发代码
`python setup.py sdist upload -r hello`(tar源码版)
`python setup.py bdist_wheel upload -r hello`(wheel版)
