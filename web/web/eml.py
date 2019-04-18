import smtplib
from email.mime.text import MIMEText
from email.header import Header
import random
import time

# 第三方 SMTP 服务
mail_host = "smtp.qq.com"  # 设置服务器
mail_user = "791956236@qq.com"  # 用户名
mail_pass = "bjchyjtrbkasbbhi"  # 口令

sender = '791956236@qq.com'
receivers = ['m18811627539@163.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

random.seed(time.time_ns())
message = MIMEText('Verify code: '+str(random.randint(1000,9999)), 'plain', 'utf-8')
message['From'] = 'Airplane'
message['To'] = 'Dear Guest'

subject = 'Verify code from airplane'
message['Subject'] = Header(subject, 'utf-8')

try:
	smtpObj = smtplib.SMTP()
	print(1)
	smtpObj.connect(mail_host, 25)  # 25 为 SMTP 端口号
	print(2)
	smtpObj.login(mail_user, mail_pass)
	print(3)
	smtpObj.sendmail(sender, receivers, message.as_string())
	print("Sucess")
except smtplib.SMTPException:
	print("Fail")
