#Python TIPS

##实际技巧
1.  python不支持函数重载。。。

##代码风格

###类之间的关系

###函数间关系
1.  每个函数间空一行，例如

  ```python
  def a():
    pass

  def b():
    pass
  ```

2.  

###注释：
1.  注释是在类或者是函数后的第一行，使用`'''`或`"""`来写一段完整的话，表示类或函数的功能，然后可以使用相关的标签，表示参数和返回值的注释
例如：
```python
def chmod(self, filepath, mod):
    '''
    修改文件权限
    :param filepath:文件路径
    :param mod:赋予的权限
    :return:
    '''
    self.child.sendline('chmod '+ mod +' '+ filepath)
    index = self.child.expect(['#',pexpect.EOF])
    if index ==1:
        print '缓冲区无数据'
```
2.  在每个python文件的开始，加上`__author__ = 'hgf'`表述文件的作者
3.  在使用`#`编写注释的时候，`#`后面空格然后再写注释
