from bs4 import BeautifulSoup as bs
import urllib.request


class Item:
	def __init__(self, item_id, item_url):
		self.id = item_id
		self.url = item_url


class Info:
	def __init__(self, img_url, title, price, lower_title, params_table, details, url):
		self.img_url = img_url
		self.title = title
		self.price = price
		self.lower_title = lower_title
		self.params_table = params_table
		self.details = details
		self.url = url


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
			if n > 15:
				break
			n += 1

			try:
				item_id = item['id']
				item_url = item['href']
				listing = Item(item_id, item_url)
				listings.append(listing)
			except Exception as e:
				continue
		return listings

	def getInfo(self, soup, url):
			try:
				img_url = soup.find('img', {'itemprop': 'image'})['src']
			except:
				img_url = ''
			title = soup.find('h1', {'itemprop': 'name'}).getText().strip()
			price = soup.find('span', {'itemprop': 'price'}).getText().split('€')[0]
			lower_title = ''
			try:
				lower_title = soup.find('div', {'class': 'ad_param'}).getText().strip()
			except:
				pass
			params_table = soup.find('table', {'class': 'tech_data'})
			_details = soup.find('div', {'class': 'body'})
			_details.find('b').decompose()
			details = _details.getText().strip()
			return Info(img_url, title, price, lower_title, params_table, details, url)



def getListings(search_url):
	scraper = Scraper()
	soup = scraper.getSoup(search_url)
	listings = scraper.getItems(soup)
	return listings

def getListingInfo(listing_url):
	scraper = Scraper()
	soup = scraper.getSoup(listing_url)
	info = scraper.getInfo(soup, listing_url)
	return info

test_url = 'https://www.tori.fi/koko_suomi/autot?cg=2010'
test_url2 = 'https://www.tori.fi/pirkanmaa/Hyundai_Tucson_71044467.htm?ca=18&w=3'

#getListings(test_url)
#info = getListingInfo(test_url2)
#print(info.title, info.price, info.lower_title, info.params_table, info.url)