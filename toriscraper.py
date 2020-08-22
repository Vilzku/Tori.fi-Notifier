from bs4 import BeautifulSoup as bs
import urllib.request


class Item:
	def __init__(self, item_id, item_title, item_params, item_url):
		self.id = item_id
		self.title = item_title
		self.params = item_params
		self.url = item_url


class Scraper:
	def __init__(self):
		pass

	def getSoup(self, url):
		source = urllib.request.urlopen(url).read()	
		soup = bs(source, 'html.parser')
		return soup

	def getItems(self, soup):
		table = soup.find('div', {'class': 'list_mode_thumb'})

		items = table.find_all('a')

		listings = []
		n = 0;
		for item in items:

			# new listings are always found on top of the list
			if n > 10:
				break
			n += 1

			try:
				item_id = item['id']
				item_url = item['href']
				item_title = item.find('div', {'class': 'li-title'}).text

				details = item.find('div', {'class': 'list-details-container'})
				item_param_elements = details.find_all('p')
				item_params = [i.text for i in item_param_elements]

				listing = Item(item_id, item_title, item_params, item_url)
				listings.append(listing)
			except Exception as e:
				continue
		return listings


def getListings(search_url):
	scraper = Scraper()
	soup = scraper.getSoup(search_url)
	listings = scraper.getItems(soup)
	return listings

test_url = 'https://www.tori.fi/koko_suomi/autot?cg=2010'
getListings(test_url)