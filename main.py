import pickle
import os
import sys

from search import search

deckname = sys.argv[1]

class Card():
    def __init__(self, string):
        lst = string.split(' ')
        self.num = lst[0]
        self.name = ' '.join(s for s in lst[1:])

    def print(self):
        print(self.num, self.name)

def deck(string):
    deck = string.split('\n')
    return [Card(card) for card in deck]

def proc(d):
    from multiprocessing import Pool
    import multiprocessing as multi

    maxproc = multi.cpu_count()

    with Pool(processes=maxproc) as p:
       lst = p.map(search, d)

    return lst

def printout(d, mode = "main"):
    lst = proc(d)
    l = ''.join('-' for _ in range(30))
    print(f"\n{l} MAIN DECK {l}\n") if mode == "main" else print(f"\n{l} SIDEBOARD {l}\n")
    total = 0
    for card, d in zip(d, lst):
        price = int(d['price'].replace(',',''))
        num = int(card.num)
        total += price * num
        print(f"{price} x {num} = {price*num}".ljust(20), end=' ')
        print(d['name'])
    string = 'main' if mode == 'main' else 'side'
    print(f"\n{string} ) price:", total)
    return total

def main():
    with open(deckname, 'r') as rf:
        main, side = ''.join(r for r in rf).split('\n\nSideboard\n')

    main, side = deck(main), deck(side[:-1])

    total = printout(main)

    s_total = printout(side, mode = "side")

    print("\ntotal price (main + side):", total + s_total)

if __name__ == "__main__":
    main()
