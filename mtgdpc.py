import sys

from search import *

deckname = sys.argv[1]

def main():
    with open(deckname, 'r') as rf:
        main, side = ''.join(r for r in rf).split('\n\nSideboard\n')

    main, side = deck(main), deck(side[:-1])

    total = printout(main)

    s_total = printout(side, mode = "side")

    print("\ntotal price (main + side):", total + s_total)

if __name__ == "__main__":
    main()
