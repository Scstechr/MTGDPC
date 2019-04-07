
import requests
from bs4 import BeautifulSoup
import lxml
import sys

from convert import convert
from search import *

def main(deckname):
    with open(deckname, 'r') as rf:
        lst = ''.join(r for r in rf).split('\n\nSideboard\n')
        if len(lst) != 2:
            convert(deckname)
            with open(deckname, 'r') as rf2:
                lst = ''.join(r for r in rf2).split('\n\nSideboard\n')

    deck = proc([Card(card) for card in lst[0].split('\n')])

    total = printout(deck)

    if len(lst) == 2 and lst[1] != '':
        side = proc([Card(card) for card in lst[1][:-1].split('\n')])
        s_total = printout(side, mode = "SIDEBOARD")
    else:
        print("side ) price: 0")
        s_total = 0

    total += s_total
    num = len(str(total))
    print(TABLH,end='')
    [print(TABBR,end='') for _ in range(NUM1)]
    print(TABRH, TABWL, end='', sep='\n')
    print(f"\033[{NUM3-12}GTOTAL PRICE {TABBW}", f"\033[{WIDTH-num-1}G{total}", f"\033[{WIDTH}G{TABWL}", end="")
    print(f"\033[{WIDTH}G{TABWL}")
    print(TABLB,end='')
    [print(TABBR,end='') for _ in range(NUM1)]
    print(TABRB)

if __name__ == "__main__":
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        print("ERROR ON ARGUMENT(S)")
