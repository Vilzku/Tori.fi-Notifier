import smtplib
import login_details
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class Emailer():
	def __init__(self, receiver):
		self.email = login_details.EMAIL
		self.password = login_details.PASSWORD
		self.receiver = receiver

	def create_email(self, item):
		message = MIMEMultipart('alternative')
		message['Subject'] = 'UUSI ILMOITUS - {}'.format(item.title)
		message['From'] = self.email
		message['To'] = self.receiver

		text = '''
		{0}
		{1}
		{2}
		'''.format(item.title, item.params, item.url)

		html = '''
		<html>
			<a href="{2}">{0}
			{1}
			</a>
		</html>
		'''.format(item.title, item.params, item.url)

		text_part = MIMEText(text, 'plain')
		html_part = MIMEText(html, 'html')

		message.attach(text_part)
		message.attach(html_part)

		self.send(message)

	def send(self, message):
		try:
			with smtplib.SMTP('smtp.gmail.com', 587) as server:
				server.starttls()
				server.login(self.email, self.password)
				server.sendmail(self.email, self.receiver, message.as_string())
				server.close()
		except Exception as e:
			print(e)
		else:
			print('Email sent')
