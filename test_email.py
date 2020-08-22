from email_notifier import *
from toriscraper import Item

item = Item('00000', 'test_item', ['param1', 'param2'], 'www.test.com')
e = Emailer('torinotifier@gmail.com')
e.create_email(item)