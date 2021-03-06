import os
import click
import subprocess as sp
import requests
from bs4 import BeautifulSoup
import lxml
import sys
import tqdm

from src.convert import convert
from src.search import *

exp_s = "Save images of cards from decklist."
exp_h = "Use high-res option of carddl.py.  "
exp_f = "Select format e.g, modern, vintage."
exp_l = "Select language from en/ja .       "
@click.command()
@click.argument("deckname")
@click.option("-s", "--save", is_flag="False", help=exp_s)
@click.option("-h", "--high", is_flag="False", help=exp_h)
@click.option("-f", "--frmt", default="standard", help=exp_f)
@click.option("-l", "--lang", default="en", help=exp_l)
def main(deckname, save, high, frmt, lang):
    with open(deckname, 'r') as rf:
        lst = ''.join(r for r in rf).split('\n\nSideboard\n')
        if len(lst) != 2:
            convert(deckname)
            with open(deckname, 'r') as rf2:
                lst = ''.join(r for r in rf2).split('\n\nSideboard\n')

    deck = proc([Card(card) for card in lst[0].split('\n')])
    if save:
        dllist = [deck]

    total = printout(deck)

    if len(lst) == 2 and lst[1] != '':
        side = proc([Card(card) for card in lst[1][:-1].split('\n')])
        if save:
            dllist += [side]
        s_total = printout(side, mode = "SIDEBOARD")
    else:
        print("side ) price: 0")
        s_total = 0

    total += s_total
    num = len(str(total))
    print(TABLH,end='')
    [print(TABBR,end='') for _ in range(NUM1)]
    print(TABRH, TABWL, end='', sep='\n')
    print(f"\033[{NUM3-12}GTOTAL PRICE {TABBW}", f"\033[{WIDTH-num-1}G{total}", end='')
    print(f"\033[{WIDTH}G{TABWL}", f"\033[{WIDTH}G{TABWL}")
    print(TABLB,end='')
    [print(TABBR,end='') for _ in range(NUM1)]
    print(TABRB)

    if save:
        print()
        basename = os.path.basename(deckname)
        title, ext = os.path.splitext(basename)
        head, ext = os.path.splitext(deckname)
        for board, deck in enumerate(dllist):
            for idx, card in enumerate(deck):
                arg = '-h' if high else ''
                arg += f' -f {frmt}' if frmt != 'standard'  else ''
                arg += f' -l {lang}' if lang != 'en' else ''
                num = str(idx).zfill(2)
                arg += f' -c {title}_M{num}' if not board else f' -c {title}_S{num}'
                cmd = f'python carddl.py -n "{card.ename}" -p "{head}" -s {arg}'
                sp.call(cmd, shell=True)

if __name__ == '__main__':
    main()
