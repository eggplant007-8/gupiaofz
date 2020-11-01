# coding:utf-8
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from twilio.rest import Client

def send_message_mail(message):
    # 第三方 SMTP 服务
    mail_host = "smtp.qq.com"  # 设置服务器
    mail_user = "690048787@qq.com"  # 用户名
    mail_pass = "exwtaifbdkwlbdjh"  # 口令,QQ邮箱是输入授权码，在qq邮箱设置 里用验证过的手机发送短信获得，不含空格

    sender = '690048787@qq.com'
    receivers = ['690048787@qq.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

    message = MIMEText(message, 'plain', 'utf-8')
    message['From'] = Header(sender, 'utf-8')
    message['To'] = Header("690048787@qq.com", 'utf-8')

    subject = '好把手头上的股票卖啦'
    message['Subject'] = Header(subject, 'utf-8')

    try:
        smtpObj = smtplib.SMTP_SSL(mail_host, 465)
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        smtpObj.quit()
        print("邮件发送成功")
    except smtplib.SMTPException as e:
        print(e)

def send_message_twilio(message):
    from twilio.rest import TwilioRestClient

    # 下面认证信息的值在你的 twilio 账户里可以找到
    account_sid = "ACXXXXXXXXXXXXXXXXX"
    auth_token = "YYYYYYYYYYYYYYYYYY"
    client = TwilioRestClient(account_sid, auth_token)

    message = client.messages.create(to="+8615912345678",  # 区号+你的手机号码
                                     from_="+15555555555",  # 你的 twilio 电话号码
                                     body="Do you know who I am ?")