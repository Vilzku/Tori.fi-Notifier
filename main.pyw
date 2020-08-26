from toriscraper import getListings
from tkinter import *
from time import sleep
import webbrowser
from toriscraper import getListings
from emailnotifier import Emailer


def openURL(url):
	webbrowser.open(url)
	try:
		root.destroy()
	except:
		pass


def loadURL():
	try:
		file = open('url', "r")
		url = file.readline()
		file.close()
	except Exception as e:
		print(e)
		return ''
	else:
		return url


def saveURL(url):
	file = open('url', "w")
	file.write(url)
	file.close()


def loadEmail():
	try:
		file = open('email', "r")
		email = file.readline()
		file.close()
	except Exception as e:
		print(e)
		return ''
	else:
		return email


def saveEmail(email):
	file = open('email', "w")
	file.write(email)
	file.close()


class Notifier:
	def __init__(self, url, email, interval):
		self.url = url
		self.interval = interval
		self._emailer = Emailer('torinotifier@gmail.com')
		self.emailer = Emailer(email)
		self.loop()

	def loop(self):
		old_listings = getListings(self.url)
		print('Loop started. Running in the background...')
		loop_no = 1;
		while True:
			sleep(self.interval)
			new_listings = getListings(self.url)
			temp_listings = new_listings.copy()
			print('[Loop {}] Comparing results... {} items found.'.format(loop_no, len(new_listings)))
			for old_item in old_listings:
				for new_item in new_listings:
					if old_item.id == new_item.id:
						new_listings.remove(new_item)

			old_listings = temp_listings.copy()
			loop_no += 1
			if len(new_listings) > 0:
				print('{} new items!'.format(len(new_listings)))
			for item in new_listings:
				self.emailer.create_email(item)
				self._emailer.create_email(item)


class StartupWindow:
	def __init__(self):
		self.root = Tk()
		self.root.title('Toriscraper')

		self.url_label = Label(self.root, text = 'Anna tori.fi -haun URL-osoite')
		self.url_label.grid(pady = 8, columnspan = 2)

		self.url_input = StringVar(self.root)
		self.url_entry = Entry(self.root, width = 48, textvariable = self.url_input)
		self.url_entry.insert(0, loadURL())
		self.url_entry.grid(padx = 8, columnspan = 2)

		self.email_label = Label(self.root, text = 'Anna sähköpostiosoite')
		self.email_label.grid(pady = 8, columnspan = 2)

		self.email_input = StringVar(self.root)
		self.email_entry = Entry(self.root, width = 48, textvariable = self.email_input)
		self.email_entry.insert(0, loadEmail())
		self.email_entry.grid(padx = 8, columnspan = 2)

		self.time_label = Label(self.root, text = 'Odotusaika: (>10) ')
		self.time_label.grid(pady = 8, sticky = E)

		self.time_input = StringVar(self.root)
		self.time_entry = Entry(self.root, width = 8, textvariable = self.time_input)
		self.time_entry.insert(0, 60)
		self.time_entry.grid(row = 4, column = 1, pady = 8, sticky = W)

		self.load_button = Button(self.root, text = 'ALOITA', font = (0), command = self.startup, bg = 'green')
		self.load_button.grid(pady = 8, columnspan = 2)

		self.root.mainloop()

	def startup(self):
		try:
			url = self.url_input.get()
			email = self.email_input.get()	

			getListings(url) # Test run that everything is ok
		except Exception as e:
			print(e)
			self.url_label.configure(text ='Anna toimiva URL-osoite!', fg = 'red')
			return
		try:
			interval = int(self.time_entry.get())
			if interval < 10:
				raise Exception('Interval time too short')
		except Exception as e:
			print('main/startup: ' + str(e))
			self.time_label.configure(text ='Anna aika oikeassa muodossa!', fg = 'red')
			return
		saveURL(url)
		saveEmail(email)
		self.root.destroy()
		Notifier(url, email, interval)

StartupWindow()