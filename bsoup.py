import requests
import lxml
from bs4 import BeautifulSoup

cardname = 'Marsh Flats'
searchname = '+'.join(cardname.split(' '))

html = f"https://www.suruga-ya.jp/search?category=&search_word=mtg+{searchname}&adult_s=1&rankBy=price%3Aascending&restrict[]=brand=%E3%82%A6%E3%82%A3%E3%82%B6%E3%83%BC%E3%82%BA%E3%83%BB%E3%82%AA%E3%83%96%E3%83%BB%E3%82%B6%E3%83%BB%E3%82%B3%E3%83%BC%E3%82%B9%E3%83%88"

r = requests.get(html)
soup = BeautifulSoup(r.text, 'lxml')
first_item = soup.find('div', class_='item_box first_item')

l = first_item.find_all('div')[0]
item = l.text.split('\n')
for i in item[-5:-1]:
    print(i)
