#虚拟环境开发


##安装虚拟环境

`pip install virtualenv`

## 使用虚拟环境

1.  创建虚拟环境

    `virtualenv [envname]`

2.  激活虚拟环境

    `source envname/bin/activate`
    >说明：使用`deactivate`，停止并推出虚拟环境

3.  自动化虚拟环境脚本

    自动安装虚拟环境，并安装程序的依赖项。
    例子：
    ```shell
    virtualenv myappenv
    source myappenv/bin/activate
    pip install -r requirements.txt
    deactivate

    ```
