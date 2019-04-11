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
    if len(output) > 60:
        out = output[:50] + '...' 
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

def save(card, output, language, custom):
    numstr = custom if custom else card.number.zfill(3)
    lst = [card]
    if card.layout == 'transform':
        lst.append(Card.where(set=card.set).where(name=card.names[1]).all()[0])
    for idx, card in enumerate(lst):
        dirname = os.path.dirname(output)
        if card.layout == 'split':
            card_ = Card.where(set=card.set).where(name=card.names[1]).all()[0]
            output = os.path.join(dirname, f"{numstr}_{card.name}+{card_.name}_en.jpg")
        elif card.layout == 'transform':
            card_ = Card.where(set=card.set).where(name=card.names[1]).all()[0]
            if not idx:
                output = os.path.join(dirname, f"{numstr}_{card.name}_{card_.name}_en_a.jpg")
            else:
                output = os.path.join(dirname, f"{numstr}_{card.name}_{card_.name}_en_b.jpg")
        elif card.name not in BASIC:
            output = os.path.join(dirname, f"{numstr}_{card.name}_en.jpg")
        if language != 'en':
            output = output.replace('_en.jpg', f'_{language}.jpg')
        downloader(card, output, card.image_url, 'en')

def hr_save(card, output, language, custom):
    numstr = custom if custom else card.number.zfill(3)
    html = f"https://scryfall.com/card/{card.set.lower()}/{card.number}/{card.name.lower().replace(' ','-')}"
    flag = True
    dirname = os.path.dirname(output)
    if card.names:
        card_ = Card.where(set=card.set).where(name=card.names[1]).all()[0]
        html += f"-{card_.name.lower().replace(' ','-')}"

    r = requests.get(html)
    soup = BeautifulSoup(r.text, 'lxml')
    img_tag = soup.find_all("div", class_="card-image-front")[0].find('img')
    img_url = img_tag['src'].replace('/en/',f'/{language}/')
    alt_title = img_tag['title'].replace(f' ({card.set.upper()})', '').split(' // ')

    if len(alt_title) > 1:
        flag = validDuplit(card, output, alt_title, language)
        if card.layout == 'transform':
            output = os.path.join(dirname, f"{numstr}a_{alt_title[0]}_{language}.jpg")
            output2 = os.path.join(dirname, f"{numstr}b_{alt_title[1]}_{language}.jpg")
        elif card.layout == 'split':
            output = os.path.join(dirname, f"{numstr}_{alt_title[0]}+{alt_title[1]}_{language}.jpg")
    else:
        output = os.path.join(dirname, f"{numstr}_{alt_title[0]}_{language}.jpg")

    print("HIGH",end=' | ')
    downloader(card, output, img_url, language, True)
    if card.layout == 'transform':
        img_tag = soup.find_all("div", class_="card-image-back")[0].find('img')
        img_url = img_tag['src'].replace('/en/',f'/{language}/')
        print("HIGH",end=' | ')
        downloader(card, output2, img_url, language, True)

def search(card, path, high, language, custom, flag=False):

    if path == "cardchunk":
        output = os.path.join(path, card.set, f"{card.name}_{language}.jpg")
        if flag:
            output = os.path.join(path, card.set, f"{card.number.zfill(3)}_{card.name}_{language}.jpg")
    else:
        output = os.path.join(path, f"{card.name}_{language}.jpg")
        if custom:
            output = os.path.join(path, f"{custom}_{card.name}_{language}.jpg")
        if flag:
            output = os.path.join(path, f"{card.number.zfill(3)}_{card.name}_{language}.jpg")

    if os.path.exists(output):
        if high:
            hr_save(card, output, language, custom)
        else:
            print(f"{output} ALREADY EXISTS!")

    else: 
        hr_save(card, output, language, custom) if high else save(card, output, language, custom)

exp_e = "Give specific name of a set."
exp_n = "Give specific name of a card."
exp_p = "Set path of where to save card if needed."
exp_s = "Only search for single card."
exp_h = "High-res option for images."
exp_l = "Select en/ja (en is default)."
exp_f = "Select format such as 'modern'."
exp_u = "Unbound to all cards ever released."
exp_c = "Custom Header"
@click.command()
@click.option("-e", "--edition", help=exp_e)
@click.option("-n", "--name", help=exp_n)
@click.option("-p", "--path", default="cardchunk", help=exp_p)
@click.option("-s", "--single", is_flag ="False", help=exp_s)
@click.option("-h", "--high", is_flag="False", help=exp_h)
@click.option("-l", "--language", default='en', help=exp_l)
@click.option("-f", "--frmt", default='standard', help=exp_f)
@click.option("-u", "--unleash", is_flag="False", help=exp_u)
@click.option("-c", "--custom", default=None, help=exp_u)
def main(edition, name, path, single, high, language, frmt, unleash, custom):
    if name:
        if name.count("+"):
            name = name.split('+')[0]

    if edition:
        cards = Card.where(set=edition.lower()).all()
        if name:
            cards = Card.where(set=edition.lower()).where(name=name).all()
    else:
        cards = Card.where(name=name).all()

    if not name and not edition:
        print("Give at least name (w/ -n) or edition (w/ -e).\nBoth of them is also welcome.")
        exit()
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

    for card in cards[20:30]:
        if not edition:
            sets = Card.where(set=card.set).all()
        else:
            sets = cards
        names = [card.name for card in sets]

    if not single:
        print(f"RESULTS :{len(cards)}")
    for card in cards:
        if single:
            search(card, path, high, language, custom)
        else:
            search(card, path, high, language, custom, True)

if __name__ == "__main__":
    main()

