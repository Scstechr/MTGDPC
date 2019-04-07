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

def downloader(card, output, url, language, replace=False):
    print(f"{output} \033[70G| {DICT[card.set]} ({card.set})")
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
    for card in lst:
        dirname = os.path.dirname(output)
        output = os.path.join(dirname, f"{card.name}_en.jpg")
        downloader(card, output, card.image_url, 'en')

def hr_save(card, output, language):
    html = f"https://scryfall.com/card/{card.set.lower()}/{card.number}/{card.name.lower().replace(' ','-')}"
    if card.layout == 'transform':
        card_ = Card.where(set=card.set).where(name=card.names[1]).all()[0]
        html += f"-{card_.name.lower().replace(' ','-')}?back"
    r = requests.get(html)
    soup = BeautifulSoup(r.text, 'lxml')
    img_url = soup.find_all("div", class_="card-image-front")[0].find('img')['src']
    print("HIGH",end=' | ')
    downloader(card, output, img_url.replace('/en/',f'/{language}/'), language, True)
    if card.layout == 'transform':
        img_url = soup.find_all("div", class_="card-image-back")[0].find('img')['src']
        dirname = os.path.dirname(output)
        output = os.path.join(dirname, f"{card_.name}_{language}.jpg")
        print("HIGH",end=' | ')
        downloader(card, output, img_url.replace('/en/',f'/{language}/'), language, True)

def search(card, path, high, language, flag=False):
    if path == "cardchunk":
        output = os.path.join(path, card.set, f"{card.name}_{language}.jpg")
    else:
        output = os.path.join(path, f"{card.name}_{language}.jpg")

    if os.path.exists(output):
        if flag:
            d = []
            for f in os.listdir(os.path.join(path, card.set)):
                if f.count(card.name):
                    d.append(f)
            if len(d):
                if d[-1].count("_"):
                    head = d[-1].split("_")
                    num = int(head[1][0]) + 1
                    output = head[0] + f"_{num}.jpg"
                else:
                    head, ext = os.path.splitext(d[0])
                    output = head + "_1" + ext
                    shutil.move(d[0], head + "_0" + ext)
                output = os.path.join(path, card.set, output)
                hr_save(card, output, language) if high else save(card, output)
                
        else:
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
def main(edition, name, path, single, high, language):
    if edition:
        cards = Card.where(set=edition).all()
        if name:
            cards = cards.where(name=name).all()
    else:
        cards = Card.where(name=name).all()

    cards = [card for card in cards if card.image_url]
    cards = [card for card in cards if card.set in SETS]

    if name:
        cards = [card for card in cards if card.name == name]

    if single:
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

    for card in cards:
        if card.name in dlist:
            search(card, path, high, language, True)
        else:
            search(card, path, high, language)

if __name__ == "__main__":
    main()

