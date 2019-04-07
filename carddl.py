from mtgsdk import Card
from mtgsdk import Set
import urllib
import os
import click
import shutil
import subprocess as sp
from bs4 import BeautifulSoup
import requests

sets = Set.all()
SETS = [s.code for s in sets if s.type in ['expansion', 'core']]
DICT = {s.code:s.name for s in sets}
dct = {s.code:s.release_date.replace('-','') for s in sets if s.code in SETS}
SORTSET = {c:r for c, r in sorted(dct.items(), key=lambda x: x[1])}
MODERN = {c for c in SORTSET if int(SORTSET[c]) > 20030526}
BASIC = ['Plains', 'Swamp', 'Island', 'Mountain', 'Forest']

def downloader(card, output, url, language, replace=False):
    if len(output) > 50:
        out = output[:40] + '...' 
    else:
        out = output
    print(f"{out} \033[70G| {DICT[card.set]} ({card.set})")
    if replace and os.path.exists(output):
        os.remove(output)
    try:
        try:
            data = urllib.request.urlopen(url)
        except:
            output = output.replace(f"{language}", "en")
            print(f"DOWNLOADING ENGLISH VER as {output}")
            url = url.replace(f"/{language}/", "/en/")
            data = urllib.request.urlopen(url)
        image = data.read()
        with open(output, "wb") as wf:
            wf.write(image)
    except:
        print(card.name, card.set, url)
        print("DOWNLOAD ERROR")

def save(card, output):
    lst = [card]
    if card.layout == 'transform':
        lst.append(Card.where(set=card.set).where(name=card.names[1]).all()[0])
    for idx, card in enumerate(lst):
        dirname = os.path.dirname(output)
        if card.layout == 'split':
            card_ = Card.where(set=card.set).where(name=card.names[1]).all()[0]
            output = os.path.join(dirname, f"{card.name}+{card_.name}_en.jpg")
        elif card.layout == 'transform':
            card_ = Card.where(set=card.set).where(name=card.names[1]).all()[0]
            if not idx:
                output = os.path.join(dirname, f"{card.name}_{card_.name}_en_a.jpg")
            else:
                output = os.path.join(dirname, f"{card.name}_{card_.name}_en_b.jpg")
        elif card.name not in BASIC:
            output = os.path.join(dirname, f"{card.name}_en.jpg")
        downloader(card, output, card.image_url, 'en')

def hr_save(card, output, language):
    html = f"https://scryfall.com/card/{card.set.lower()}/{card.number}/{card.name.lower().replace(' ','-')}"
    if card.layout == 'transform':
        card_ = Card.where(set=card.set).where(name=card.names[1]).all()[0]
        html += f"-{card_.name.lower().replace(' ','-')}?back"
        dirname = os.path.dirname(output)
        output = os.path.join(dirname, f"{card.name}_{card_.name}_a_{language}.jpg")
    if card.layout == 'split':
        card_ = Card.where(set=card.set).where(name=card.names[1]).all()[0]
        html += f"-{card_.name.lower().replace(' ','-')}"
        dirname = os.path.dirname(output)
        output = os.path.join(dirname, f"{card.name}+{card_.name}_{language}.jpg")
    r = requests.get(html)
    soup = BeautifulSoup(r.text, 'lxml')
    img_url = soup.find_all("div", class_="card-image-front")[0].find('img')['src']
    print("HIGH",end=' | ')
    downloader(card, output, img_url.replace('/en/',f'/{language}/'), language, True)
    if card.layout == 'transform':
        img_url = soup.find_all("div", class_="card-image-back")[0].find('img')['src']
        dirname = os.path.dirname(output)
        output = os.path.join(dirname, f"{card.name}_{card_.name}_b_{language}.jpg")
        print("HIGH",end=' | ')
        downloader(card, output, img_url.replace('/en/',f'/{language}/'), language, True)

def search(card, path, high, language, flag=False):
    if path == "cardchunk":
        output = os.path.join(path, card.set, f"{card.name}_{language}.jpg")
    else:
        output = os.path.join(path, f"{card.name}_{language}.jpg")

    dlist = {card.number:x for x, card in enumerate(Card.where(set=card.set).where(name=card.name).all())}
    if flag and len(dlist) > 1:
        output = os.path.join(path, card.set, f'{card.name}_{language}_{dlist[card.number]}.jpg')
    if os.path.exists(output):
        if high:
            hr_save(card, output, language)
        else:
            print(f"{output} ALREADY EXISTS!")

    else: 
        hr_save(card, output, language) if high else save(card, output)

@click.command()
@click.option("-e", "--edition")
@click.option("-n", "--name")
@click.option("-p", "--path", default="cardchunk")
@click.option("-s", "--single", is_flag ="False")
@click.option("-h", "--high", is_flag="False")
@click.option("-l", "--language", default='en')
@click.option("-f", "--frmt", default='standard')
@click.option("-u", "--unleash", is_flag="False")
def main(edition, name, path, single, high, language, frmt, unleash):
    if name:
        if name.count("+"):
            name = name.split('+')[0]

    if edition:
        cards = Card.where(set=edition.lower()).all()
        if name:
            cards = Card.where(set=edition.lower()).where(name=name).all()
    else:
        cards = Card.where(name=name).all()

    cards = [card for card in cards if card.image_url]
    if unleash:
        sets = Set.all()
        SETS_ = [s.code for s in sets]
        DICT_ = {s.code:s.name for s in sets}
        dct_ = {s.code:s.release_date.replace('-','') for s in sets if s.code in SETS_}
        SORTSET_ = {c:r for c, r in sorted(dct_.items(), key=lambda x: x[1])}

        # chronological sort editions
        sets = {card.set:SORTSET_[card.set] for card in cards}

    else:
        cards = [card for card in cards if card.set in SETS]
        if frmt == 'modern':
            cards = [card for card in cards if card.set in MODERN]

        # chronological sort editions
        sets = {card.set:SORTSET[card.set] for card in cards}

    sortset = {c:r for c, r in sorted(sets.items(), key=lambda x: x[1])}
    cards = [c for s in sortset for c in cards if c.set == s]
    if not len(cards):
        print(f"\033[31m{name} does not exist in format: {frmt}\033[0m")
        exit()

    if name:
        cards = [card for card in cards if card.name == name]

    if single:
        if frmt == 'standard':
            cards = cards[-1:]
        else:
            cards = cards[:1]

    if path == "cardchunk":
        for card in cards:
            outdir = os.path.join(path, card.set)
            if not os.path.exists(outdir):
                os.makedirs(outdir)
    else:
        outdir = path
        if not os.path.exists(outdir):
            os.makedirs(outdir)

    for card in cards:
        if not edition:
            sets = Card.where(set=card.set).all()
        else:
            sets = cards
        names = [card.name for card in sets]
        dlist = set(card for card in names if names.count(card) > 1)

    print(f"RESULTS :{len(cards)}")
    for card in cards:
        if single:
            search(card, path, high, language)
        else:
            search(card, path, high, language, True)

if __name__ == "__main__":
    main()

