# !/usr/bin/python
# -*- coding: UTF-8 -*-

import smtplib
from email.mime.text import MIMEText

if __name__ == '__main__':
    my_sender = '1830883597@qq.com'  # 发件人邮箱账号
    my_pass = 'mmuljzlcwjbzeaif'  # 发件人邮箱密码
    my_receive = ['1830883597@qq.com', '1830883597@qq.com']  # 收件人邮箱账号，我这边发送给自己

    try:
        msg = MIMEText('这是菜鸟教程Python 邮件发送测试……', 'plain', 'utf-8')  # 邮件正文
        msg['From'] = my_sender  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To'] = ','.join(my_receive)  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject'] = "菜鸟教程发送邮件测试"  # 邮件的主题，也可以说是标题

        server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是25
        server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
        server.sendmail(my_sender, msg['To'].split(','), msg.as_string().encode("utf-8"))  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()
        print("邮件发送成功")
    except Exception:
        print("邮件发送失败")
