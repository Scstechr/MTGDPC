import sys

from search import *
from convert import convert

deckname = sys.argv[1]

def main():
    with open(deckname, 'r') as rf:
        lst = ''.join(r for r in rf).split('\n\nSideboard\n')
        if len(lst) != 2:
            convert(deckname)
            with open(deckname, 'r') as rf2:
                lst = ''.join(r for r in rf2).split('\n\nSideboard\n')

    main = deck(lst[0])
    total = printout(main)

    if len(lst) == 2 and lst[1] != '':
        side = deck(lst[1][:-1])
        s_total = printout(side, mode = "side")
    else:
        print("side ) price: 0")
        s_total = 0

    print("\ntotal price (main + side):", total + s_total)

if __name__ == "__main__":
    main()
