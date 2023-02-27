import smtplib
from email.mime.text import MIMEText


msg_from = "1649028630@qq.com"
password = "dqrurwvkbeyeecda"
msg_to = "1033537867@qq.com"

subject = "邮箱主题"
content = "邮箱内容"

msg = MIMEText(content)
msg["Subject"] = subject
msg["From"] = msg_from
msg["To"] = msg_to




try:
	print(3)
	s = smtplib.SMTP_SSL("smtp.qq.com", 465)
	print(2)
	s.login(msg_from, password)
	print(1)
	s.sendmail(msg_from, msg_to, msg.as_string())
	print("发送成功")
except smtplib.EMTPException as e:
	print("发送失败")
finally:
	s.quit()
