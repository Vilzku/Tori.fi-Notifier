from bs4 import BeautifulSoup as bs


def make(info):
	html = open('email_template.html', 'r').read()
	soup = bs(html, 'html.parser')

	img_src = info.img_url
	img = soup.new_tag('img')
	img['src'] = img_src
	soup.find('td', {'class': 'image'}).insert(1, img)

	title = info.title
	soup.find('td', {'class': 'title'}).find('b').insert(1, title)

	if len(info.price) > 0:
		price = info.price + '€'
	else:
		price = ''
	soup.find('td', {'class': 'price'}).find('b').insert(1, price)

	lower_title = info.lower_title
	soup.find('td', {'class': 'lower_title'}).insert(1, lower_title)

	params_table = info.params_table
	soup.find('td', {'class': 'params'}).insert(1, params_table)

	details = info.details
	soup.find('td', {'class': 'details'}).insert(1, details)

	url = info.url
	link = soup.new_tag('a')
	link['href'] = url
	link['class'] = 'tori_link'
	soup.find('td', {'class': 'link'}).insert(1, link)
	soup.find('a', {'class': 'tori_link'}).insert(1, 'Avaa Torissa')

	return soup