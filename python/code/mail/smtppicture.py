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

# 使用related定义内嵌资源
msg = MIMEMultipart('related')

msgtext = MIMEText("""
<table width="800" b cellspacing="0" order="0">
    <tr>
        <td bgcolor="gray" style="font-size:14px">
            *官网logo
        </td>
    </tr>
    <tr bgcolor="#EFEBDE" height="100" style="font-size:13px">
        <td>
           <img src="cid:p1">
        </td>
        <td>
            <img src="cid:p2">
        </td>
    </tr>
    <tr bgcolor="#EFEBDE" height="100" style="font-size:13px">
        <td>
           <img src="cid:p3">
        </td>
        <td>
            <img src="cid:p4">
        </td>
    </tr>
</table>
""", "html", "utf-8")
msg.attach(msgtext)
msg.attach(addimg("/home/hgf/Pictures/program/logo/1.PNG", "p1"))
msg.attach(addimg("/home/hgf/Pictures/program/logo/2.PNG", "p2"))
msg.attach(addimg("/home/hgf/Pictures/program/logo/3.PNG", "p3"))
msg.attach(addimg("/home/hgf/Pictures/program/logo/4.PNG", "p4"))

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