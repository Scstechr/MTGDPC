from tqdm import tqdm
import requests
import lxml
from bs4 import BeautifulSoup

TABBR = '\033[0m\u2500'
TABBW = '\033[0m\u2502'
TABLH = '\033[0m\u2553'
TABRH = '\033[0m\u2556'
TABLB = '\033[0m\u2559'
TABRB = '\033[0m\u255C'
TABWL = '\033[0m\u2551'
TABLM = '\033[0m\u255F'
TABRM = '\033[0m\u2562'
TABMD = '\033[0m\u2565'
TABMU = '\033[0m\u2568'
TABDW = '\033[0m\u252C'

WIDTH = 70
NUM1 = WIDTH - 2
NUM2 = int((WIDTH)/2 - 4)
NUM3 = int(WIDTH*0.7)

class Card():
    def __init__(self, string):
        lst = string.split(' ')
        self.num = int(lst[0])
        self.name = ' '.join(s for s in lst[1:])
        self.ename = self.name
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
        try:
            info = table.find_all('tr')
            if info[0].text.count('カード名'):
                string = info[0].text.replace('\n', '')[4:]
                string = string.replace('\t', '').replace('（','_').replace('）','_')
                lst = string.split('_')
                if len(lst) > 2:
                    lst = lst[:-1]
                card.name = ' '.join([s for idx, s in enumerate(lst) if not idx%2])
                break
        except:
            pass

    return card

=======

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
            lst = string.split('_')
            if len(lst) > 2:
                lst = lst[:-1]
            card.name = ' '.join([s for idx, s in enumerate(lst) if not idx%2])
            break

    return card

>>>>>>> bd56cfab4d1855c059cd64e6c18e5fa5e3f8b347
def proc(deck):
    import multiprocessing as multi

    maxproc = multi.cpu_count()

    #with multi.Pool(processes=maxproc) as p:
    #   lst = p.map(search, deck)
    lst = [search(card) for card in tqdm(deck)]
    print("\033[1A",end='\033[0K')

    return lst

def htmlgen(cardname, shop = 's'):
    searchname = '+'.join(cardname.split(' '))
    html = f"http://whisper.wisdom-guild.net/card/{searchname}/"

    return html

def header(mode):
    # HEADER
    print(TABLH,end='')
    [print(TABBR,end='') for _ in range(NUM1)]
    print(TABRH, TABWL, end='', sep='\n')
    print(f"\033[{NUM2}G{mode}",end='')
    print(f"\033[{WIDTH}G{TABWL}")
    print(TABLM,end='')
    [print(TABBR,end='') for _ in range(NUM1)]
    print(f"\033[{WIDTH}G{TABRM}")

def printout(deck, mode='MAINBOARD'):

    header(mode)

    total = 0
    for card in deck:
        add = card.price * card.num
        total += add
        print(TABWL, card.name, end='')
        print(f"\033[{NUM3}G{TABBW} {card.price:5d} x {card.num} = {add}", end='')
        print(f"\033[{WIDTH}G{TABWL}")

    print(f"{TABLM}",end='')
    [print(TABBR,end='') for _ in range(NUM1)]
    print(f"{TABRM}")
    num = len(str(total))
    print(TABWL, f"\033[{NUM3-6}GPRICE {TABBW}", f"\033[{WIDTH-num-1}G{total}", f"\033[{WIDTH}G{TABWL}")
    print(TABLB,end='')
    [print(TABBR,end='') for _ in range(NUM1)]
    print(f"\033[{WIDTH}G{TABRB}")
    return total

