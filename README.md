## MTGDPC

Magic the Gathering Deck Price Checker (for JPN Players).  
Price check is done by [Wisdom Guild](http://www.wisdom-guild.net).

### Requirements

- Python 3.6 (or above)
- Beautiful Soup
- lxml

Simply, `pip install -r requirements.txt` to install above mentioned modules.

### How to use

#### 1. Prepare decklist
`.txt` file of decklist must fit the following format:
```
<# of cards> <card name>
...

Sideboard
<# of cards> <card name>
...
```
Note that card name must be in English.  
`decklist/` directory contains some sample `.txt` files.

#### 2. Execute `mtgdpc.py` with argument of prepared `.txt` file
```
$ python mtgdpc.py <.txt file>
------------------------------ MAIN DECK ------------------------------

<price> x <# of cards> = <price of card(s)> <Card Name(JPN)/(EN)>
...

main ) price: < (A) total price of main deck >

------------------------------ SIDEBOARD ------------------------------

<price> x <# of cards> = <price of card(s)> <Card Name(JPN)/(EN)>
...

side ) price: < (B) total price of sideboard >

total price (main + side): (A) + (B)
```

### Sample Decklist & Output

#### `decklist/gorgari_midrange.txt`
```
7 Swamp
5 Forest
4 Overgrown Tomb
4 Woodland Cemetery
4 Llanowar Elves
4 Pelt Collector
4 Stitcher's Supplier
4 Glowspore Shaman
4 Merfolk Branchwalker
2 Graveyard Marshal
2 Kraul Harpooner
4 Charnel Troll
4 Midnight Reaper
4 Plaguecrafter
4 Gruesome Menagerie

Sideboard
3 Kitesail Freebooter
3 Plague Mare
2 Deathgorge Scavenger
1 Reclamation Sage
3 Necrotic Wound
2 Shapers' Sanctuary
1 Mark of the Vampire
```

#### Output
```
------------------------------ MAIN DECK ------------------------------

8 x 8 = 64           森/Forest
8 x 7 = 56           沼/Swamp
666 x 4 = 2664       草むした墓/Overgrown Tomb
550 x 4 = 2200       森林の墓地/Woodland Cemetery
9 x 4 = 36           ラノワールのエルフ/Llanowar Elves
144 x 4 = 576        マーフォークの枝渡り/Merfolk Branchwalker
50 x 3 = 150         探求者の従者/Seekers' Squire
9 x 2 = 18           野茂み歩き/Wildgrowth Walker
980 x 4 = 3920       翡翠光のレインジャー/Jadelight Ranger
9 x 1 = 9            管区の案内人/District Guide
45 x 3 = 135         貪欲なチュパカブラ/Ravenous Chupacabra
9 x 2 = 18           ゴルガリの拾売人/Golgari Findbroker
1580 x 4 = 6320      破滅を囁くもの/Doom Whisperer
14 x 1 = 14          千の目、アイゾーニ/Izoni, Thousand-Eyed
1280 x 2 = 2560      暗殺者の戦利品/Assassin's Trophy
119 x 2 = 238        採取/Find （さいしゅ）  最終/Finality
880 x 2 = 1760       ゴルガリの女王、ヴラスカ/Vraska, Golgari Queen
1180 x 3 = 3540      秘宝探究者、ヴラスカ/Vraska, Relic Seeker

main ) price: 24278

------------------------------ SIDEBOARD ------------------------------

9 x 1 = 9            野茂み歩き/Wildgrowth Walker
14 x 1 = 14          千の目、アイゾーニ/Izoni, Thousand-Eyed
8 x 3 = 24           強迫/Duress
10 x 3 = 30          渇望の時/Moment of Craving
180 x 1 = 180        アルゲールの断血/Arguel's Blood Fast
1280 x 2 = 2560      ヴラスカの侮辱/Vraska's Contempt
30 x 2 = 60          最古再誕/The Eldest Reborn
119 x 1 = 119        採取/Find （さいしゅ）  最終/Finality
2490 x 1 = 2490      ビビアン・リード/Vivien Reid

side ) price: 5486

total price (main + side): 29764
```
