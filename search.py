import requests
import lxml
from bs4 import BeautifulSoup

Basic_Land = ['Forest', 'Swamp', 'Island', 'Plains', 'Mountain', 'Wastes']

def htmlgen(cardname, shop = 's'):
    if shop == 's':
        searchname = '+'.join(cardname.split(' ')) + '+日本語'
        if cardname in Basic_Land:
            searchname += '+基本土地'
        html = f"https://www.suruga-ya.jp/search?category=&search_word=mtg+{searchname}&adult_s=1&rankBy=price%3Aascending&restrict[]=brand=%E3%82%A6%E3%82%A3%E3%82%B6%E3%83%BC%E3%82%BA%E3%83%BB%E3%82%AA%E3%83%96%E3%83%BB%E3%82%B6%E3%83%BB%E3%82%B3%E3%83%BC%E3%82%B9%E3%83%88"

    else:
        searchname = '+'.join(cardname.split(' ')).lower() + '+jpn'
        html = f"http://www.hareruyamtg.com/jp/goods/search.aspx?image=%EE%A4%84&sort=sp&name={searchname}&search=x&name_type=2"

    return html

def suruga(soup):
    first_item = soup.find('div', class_='item_box first_item')

    s_card = ''
    try:
        l = first_item.find_all('div')[0]
        item = l.text.split('\n')
        s_card = ' '.join(i for i in item[-5:-1])
    except:
        s_card = 'NOT FOUND'

    return s_card    
        

def hareruya(soup):
    h_card = ''
    for item in soup.find_all('a', class_='spTopPopup popup_product'):
        l = item.text.split('\n')
        if l[-3] != 'SOLD OUT':
            h_card = item.text.replace('\r','').replace('\t','').split('\n')
            break

    #h_card = ' '.join(s for s in h_card.split('\n') if s != '')
    if h_card == '':
        return 'NOT FOUND'
    else:
        return h_card[3] + h_card[7]   

def search(cardname):
    l = []
    for shop in ['s', 'h']:
        html = htmlgen(cardname, shop)
        r = requests.get(html)
        soup = BeautifulSoup(r.text, 'lxml')
        l.append(suruga(soup)) if shop == 's' else l.append(hareruya(soup))

    for item in l:
        print(item)



