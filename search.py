import requests
import lxml
from bs4 import BeautifulSoup

class Card():
    def __init__(self, string):
        lst = string.split(' ')
        self.num = lst[0]
        self.name = ' '.join(s for s in lst[1:])

    def print(self):
        print(self.num, self.name)

def deck(string):
    deck = string.split('\n')
    return [Card(card) for card in deck]

def proc(d):
    from multiprocessing import Pool
    import multiprocessing as multi

    maxproc = multi.cpu_count()

    with Pool(processes=maxproc) as p:
       lst = p.map(search, d)

    return lst

def printout(d, mode = "main"):
    lst = proc(d)
    l = ''.join('-' for _ in range(30))
    print(f"\n{l} MAIN DECK {l}\n") if mode == "main" else print(f"\n{l} SIDEBOARD {l}\n")
    total = 0
    for card, d in zip(d, lst):
        price = int(d['price'].replace(',',''))
        num = int(card.num)
        total += price * num
        print(f"{price} x {num} = {price*num}".ljust(20), end=' ')
        print(d['name'])
    string = 'main' if mode == 'main' else 'side'
    print(f"\n{string} ) price:", total)
    return total
def replacetags(string):
    string = string.replace('カード名', '')
    string = string.replace('マナコスト', '')
    string = string.replace('タイプ', '')
    string = string.replace('テキスト', '')
    string = string.replace('オラクル', '')
    string = string.replace('フレーバ', '')
    string = string.replace('イラスト', '')
    string = string.replace('セット等', '')
    string = string.replace('\n',' ')
    string = string.replace('\t','')
    return string[1:]

def htmlgen(cardname, shop = 's'):
    searchname = '+'.join(cardname.split(' '))
    html = f"http://whisper.wisdom-guild.net/card/{searchname}/"

    return html
        
def search(card):
    cardname = card.name
    l = []
    html = htmlgen(cardname.replace(' (b)',''), 'w')
    r = requests.get(html)
    soup = BeautifulSoup(r.text, 'lxml')

    d = {}
    tables = soup.find_all('table')
    try:
        d['price'] = tables[3].find_all('b')[0].text
    except:
        d['price'] = tables[1].find_all('b')[0].text
    for table in tables:
        try:
            info = table.find_all('tr')
            if info[0].text.count('カード名') > 0:
                name = replacetags(info[0].text.strip())[:-1]
                st   = replacetags(info[7].text.strip()).split(", ")
                d['name']     = name[1:name.rfind('（') - 1]
                d['cost']     = replacetags(info[1].text.strip())
                d['type']     = replacetags(info[2].text.strip())[1:]
                d['text']     = replacetags(info[3].text.strip())
                d['oracle']   = replacetags(info[4].text.strip())
                d['flavor']   = replacetags(info[5].text.strip())
                d['illust']   = replacetags(info[6].text.strip())
                d['rarelity'] = st[0]
                d['sets']     = st[1]
                break
        except:
            pass
    return d

