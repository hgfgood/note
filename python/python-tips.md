#Python TIPS

##实际技巧
1.  python不支持函数重载。。。
2.  python类中，类的函数的第一个参数self不是必须的，只是人们习惯了，给一个别的名字也是OK
的，例如：
```python
class MyTest:
  myname = 'peter'
  def sayhello(hello):
    print "say hello to %s" % hello.myname
if __name__ == "__main__":
MyTest().sayhello()
```
用`hello`替换掉`self`，返回的结果和原来一样。

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
