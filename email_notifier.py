import smtplib
import login_details

email = login_details.EMAIL
password = login_details.PASSWORD

msg = 'test email'

try:
	with smtplib.SMTP('smtp.gmail.com', 587) as server:
		server.starttls()
		server.login(email, password)
		server.sendmail(email, email, msg)
		server.close()
except Exception as e:
	print(e)