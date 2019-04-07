from mtgsdk import Card
from mtgsdk import Set
import urllib
import os
import click
import shutil

sets = Set.all()
SETS = [s.code for s in sets if s.type in ['expansion', 'core']]
DICT = {s.code:s.name for s in sets}

def save(card, output):
    print(f"{output} \033[50Gfrom {DICT[card.set]} ({card.set})")
    try:
        data = urllib.request.urlopen(card.image_url)
        image = data.read()
        with open(output, "wb") as wf:
            wf.write(image)
    except:
        print(card.name, card.set, card.image_url)
        print("DOWNLOAD ERROR")

def search(card, path, flag=False):
    if path == "cardchunk":
        output = os.path.join(path, card.set, card.name + ".jpg")
    else:
        output = os.path.join(path, card.name + ".jpg")

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
                save(card, output)
        else:
            print(f"{output} ALREADY EXISTS!")

    else: 
        save(card, output)


@click.command()
@click.option("-e", "--edition")
@click.option("-n", "--name")
@click.option("-p", "--path", default="cardchunk")
@click.option("-s", "--single", is_flag ="False")
@click.option("-h", "--hr", is_flag="False")
def main(edition, name, path, single, hr):
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
            search(card, path, True)
        else:
            search(card, path)
        if card.layout=="transform":
            card_ = Card.where(set=card.set).where(name=card.names[1]).all()[0]
            search(card_, path)

if __name__ == "__main__":
    main()

