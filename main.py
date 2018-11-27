from mtgsdk import Card
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
        pass

    def print(self):
        print(self.num, self.name)

def deck(string):
    deck = string.split('\n')
    return [Card(card) for card in deck]

from multiprocessing import Pool
import multiprocessing as multi

maxproc = multi.cpu_count()

with open(deckname, 'r') as rf:
    main, side = ''.join(r for r in rf).split('\n\nSideboard\n')

    main, side = deck(main), deck(side[:-1])

    for card in main:
        search(card.name)


'''
from time import sleep

def process(i):
    print('start:', i)
    sleep(5)
    print('end:', i)
    return i
    
print('proc:', maxproc)
    result = p.map(process, list(range(5)))
    print(result)
'''
