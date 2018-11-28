import requests
import lxml
from bs4 import BeautifulSoup

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

