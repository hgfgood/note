#! /usr/bin/python
# coding:utf-8

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText

__author__ = 'hgf'

HOST = "smtp.qq.com"
SUBJECT = u"业务性能数据表"
FROM = "980673553@qq.com"
TO = "hgfgoodcreate@163.com"


def addimg(src, imgid):
    fp = open(src, 'rb')
    msgImg = MIMEImage(fp.read())
    fp.close()
    msgImg.add_header('Content-ID', imgid)
    return msgImg

msg = MIMEMultipart('related')

msgtext = MIMEText("""
<font>官网业务平均时延图表：<br><img src=\"cid:p1\" border =\"1\"><br>详细内附件图表</font>
""", "html", "utf-8")

msg.attach(msgtext)
msg.attach(addimg("/home/hgf/Pictures/program/logo/1.PNG", "p1"))

attach = MIMEText(open("/home/hgf/test.xlsx", 'rb').read(), "base64", "utf-8")
attach["Content-type"] = "application/octet-stream"
# 指定文件格式类型

# 指定ContentDisposition 属性值为attachement 则会出现自爱在保存对话框
# qqmail使用gb18030编码，为保证中文不会乱码，对文件名进行编码转换
attach["Content-Disposition"] = "attachment;filename=\"测试excel.xlsx\"".decode("utf-8").encode("gb18030")

msg.attach(attach)
msg['Subject'] = SUBJECT
msg['From'] = FROM
msg['To'] = TO

try:
    server = smtplib.SMTP()
    server.connect(HOST, 25)
    server.starttls()
    server.login(FROM, "passwprd")
    server.sendmail(FROM, TO, msg.as_string())
    server.quit()
    print("发送成功！")
except Exception, e:
    print("发送失败："+str(e))