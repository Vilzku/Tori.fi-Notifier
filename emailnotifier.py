import smtplib
import login_details
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.utils import formataddr
from toriscraper import getListingInfo
import emailmaker


class Emailer():
	def __init__(self, receiver):
		self.email = login_details.EMAIL
		self.password = login_details.PASSWORD
		self.receiver = receiver

	def create_email(self, item):
		info = getListingInfo(item.url)

		message = MIMEMultipart('alternative')
		message['Subject'] = 'UUSI ILMOITUS - {}'.format(info.title)
		message['From'] = formataddr((str(Header('Tori Notifier', 'utf-8')), self.email))
		message['To'] = self.receiver

		text = '{} {} {}'.format(info.title, info.price, info.url)
		html = emailmaker.make(info)

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
			print('email_notifier/send: ' + str(e))
		else:
			print('Email sent to {}'.format(self.receiver))

