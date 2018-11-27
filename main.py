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

deckname = 'decklist.txt'

with open(deckname, 'r') as rf:
    main, side = ''.join(r for r in rf).split('\n\nSideboard\n')

    main, side = deck(main), deck(side[:-1])

    for card in main:
        card.print()

    for card in side:
        card.print()


