# !/usr/bin/python
# -*- coding: UTF-8 -*-

import smtplib
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


if __name__ == '__main__':
    try:
        my_sender = '1830883597@qq.com'  # 发件人邮箱账号
        my_pass = 'mmuljzlcwjbzeaif'  # 发件人邮箱密码
        my_receive = my_receive = ['1830883597@qq.com', '1830883597@qq.com']  # 收件人邮箱账号，我这边发送给自己 需要改成收件人

        #创建一个带附件的实例
        message = MIMEMultipart()
        message['From'] = my_sender
        message['To'] = ','.join(my_receive)
        message['Subject'] = Header('Python SMTP 邮件测试', 'utf-8')
        #邮件正文内容
        message.attach(MIMEText('正文', 'plain', 'utf-8'))

        # 构造附件1，传送当前目录下的 tmp_order_order.json 文件
        att1 = MIMEText(open('../data/tmp_order_order.json', 'rb').read(), 'base64', 'utf-8')
        att1["Content-Type"] = 'application/octet-stream'
        att1["Content-Disposition"] = 'attachment; filename="tmp_order_order.json"'
        message.attach(att1)

        server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是25
        server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
        server.sendmail(my_sender, message['To'].split(','), message.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()  # 关闭连接
        print("邮件发送成功")
    except Exception:
        print("邮件发送失败")

