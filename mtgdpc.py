import sys

from search import *
from convert import convert

deckname = sys.argv[1]

def main():
    with open(deckname, 'r') as rf:
        try:
            main, side = ''.join(r for r in rf).split('\n\nSideboard\n')
        except:
            convert(deckname)
            with open(deckname, 'r') as rf2:
                main, side = ''.join(r for r in rf2).split('\n\nSideboard\n')

    main, side = deck(main), deck(side[:-1])

    total = printout(main)

    s_total = printout(side, mode = "side")

    print("\ntotal price (main + side):", total + s_total)

if __name__ == "__main__":
    main()
