from toriscraper import getListings
from tkinter import *
from time import sleep
import webbrowser

# URL
# https://www.tori.fi/uusimaa/asunnot/vuokrattavat_asunnot?ca=18&cg=1010&st=u&c=1014&at=tenant&mre=5&w=109&m=157

def openURL(url):
	webbrowser.open(url)
	try:
		root.destroy()
	except:
		pass


def loadURL():
	try:
		file = open('url.txt', "r")
		url = file.readline()
		file.close()
	except Exception as e:
		print(e)
		return ''
	else:
		return url


def saveURL(url):
	file = open('url.txt', "w")
	file.write(url)
	file.close()


class Notifier:
	def __init__(self, url, interval):
		self.url = url
		self.interval = interval
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
			self.notify(new_listings)

	def notify(self, listings):
		for item in listings:
			root = Tk()
			root.title('Toriscraper - Uusi ilmoitus!')
			title = Label(root, text = item.title, font = ('Arial', 12))
			title.grid(padx = 8, pady = 8)
			n = 0;
			for param in item.params:
				n += 1
				if n == len(item.params):
					price = Label(root, text = param, font = ('Arial', 18, 'bold'))
					price.grid(pady = 8)
				else:
					param_label = Label(root, text = param)
					param_label.grid()
			open_button = Button(root, text = 'Avaa', font = (0), command = lambda: openURL(item.url))
			open_button.grid(pady = 8)
			root.mainloop()

class startupWindow:
	def __init__(self):
		self.root = Tk()
		self.root.title('Toriscraper')

		self.url_label = Label(self.root, text = 'Anna tori.fi -haun URL-osoite')
		self.url_label.grid(pady = 8, columnspan = 2)

		self.url_input = StringVar(self.root)
		self.url_entry = Entry(self.root, width = 48, textvariable = self.url_input)
		self.url_entry.insert(0, loadURL())
		self.url_entry.grid(padx = 8, columnspan = 2)

		self.interval_label = Label(self.root, text = 'Odotusaika: (60) ')
		self.interval_label.grid(pady = 8, sticky = E)

		self.time_input = StringVar(self.root)
		self.time_entry = Entry(self.root, width = 8, textvariable = self.time_input)
		self.time_entry.insert(0, 60)
		self.time_entry.grid(row = 2, column = 1, pady = 8, sticky = W)

		self.load_button = Button(self.root, text = 'ALOITA', font = (0), command = self.startup, bg = 'green')
		self.load_button.grid(pady = 8, columnspan = 2)

		self.root.mainloop()

	def startup(self):
		try:
			url = self.url_input.get()
			
			getListings(url) # Test run that everything is ok
		except Exception as e:
			print(e)
			self.url_label.configure(text ='Anna toimiva URL-osoite!', fg = 'red')
			return
		try:
			interval = int(self.time_entry.get())
		except Exception as e:
			print(e)
			self.time_label.configure(text ='ANNA AIKA NUMEROINA', fg = 'red')
		saveURL(url)
		self.root.destroy()
		Notifier(url, interval)

startupWindow()