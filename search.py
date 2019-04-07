import requests
import lxml
from bs4 import BeautifulSoup

class Card():
    def __init__(self, string):
        lst = string.split(' ')
        self.num = int(lst[0])
        self.name = ' '.join(s for s in lst[1:])
        self.jname = ''
        self.price = 0

    def __repr__(self):
        return f"{self.num}, {self.name}, {self.price}"

def search(card):
    html = htmlgen(card.name.replace(' (b)',''), 'w')
    r = requests.get(html)
    soup = BeautifulSoup(r.text, 'lxml')

    tables = soup.find_all('table')
    try:
        card.price = int(tables[3].find_all('b')[0].text.replace(',',''))
    except:
        card.price = int(tables[1].find_all('b')[0].text.replace(',',''))

    for table in tables[:2]:
        info = table.find_all('tr')
        if info[0].text.count('カード名'):
            string = info[0].text.replace('\n', '')[4:]
            string = string.replace('\t', '').replace('（','_').replace('）','_')
            lst = string.split('_')[:-1]
            card.name = ' '.join([s for idx, s in enumerate(lst) if not idx%2])
            break

    return card

def proc(deck):
    import multiprocessing as multi

    maxproc = multi.cpu_count()

    with multi.Pool(processes=maxproc) as p:
       lst = p.map(search, deck)

    return lst

def htmlgen(cardname, shop = 's'):
    searchname = '+'.join(cardname.split(' '))
    html = f"http://whisper.wisdom-guild.net/card/{searchname}/"

    return html

def printout(deck, mode='MAIN DECK'):
    l = ''.join('-' for _ in range(30))
    print(f"\n{l} {mode} {l}\n")
    total = 0
    for card in deck:
        add = card.price * card.num
        total += add
        print(f"{card.price} x {card.num} = {add}".ljust(20), card.name)
    print(f"\n{mode} ) PRICE:", total)
    return total

