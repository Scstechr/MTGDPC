# MTGDPC
Magic the Gathering Deck Price Checker (for JPN Players).  

### About

MTGDPC (`mtgdpc`) enables users to search the cheapest price of given card name via [Wisdom Guild](http://www.wisdom-guild.net).

#### Requirements

- Python 3.6 (or above)
- Beautiful Soup
- lxml

Simply, `pip install -r requirements.txt` to install above mentioned modules.

### How to use

#### 1. Prepare decklist
- `.txt` file of decklist must fit either Format (A) or (B).
- `decklist/` directory contains some sample `.txt` files.  
##### Format (A) Basic Format
Note that card name must be in English.  
```
<# of cards> <card name>
...

Sideboard
<# of cards> <card name>
...
```
Also, other format will be automatically converted to this format.
##### Format (B) M:TG Wiki Style
If you copy and paste from [M:TG Wiki](http://mtgwiki.com/wiki/%E3%83%A1%E3%82%A4%E3%83%B3%E3%83%9A%E3%83%BC%E3%82%B8), some will look like:

```
<deck name>[?]
土地 (#)
<# of cards>	<card name [JPN]/[EN]>
クリーチャー (#)
<# of cards>	<card name [JPN]/[EN]>
呪文 (#)
<# of cards>	<card name [JPN]/[EN]>
サイドボード (#)
<# of cards>	<card name [JPN]/[EN]>
```
In this case, `mtgdpc` will automatically convert it and replace it with Basic Format.

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

#### `decklist/MoMa.txt`
```
4 Tundra
4 Volcanic Island
3 City of Brass
4 Ancient Tomb
4 Tolarian Academy
4 Lotus Petal
4 Mox Diamond
4 Mana Vault
3 Voltaic Key
2 Scroll Rack
3 Mind Over Matter
4 Windfall
4 Time Spiral
3 Abeyance
3 Intuition
3 Power Sink
4 Stroke of Genius

Sideboard
4 Gorilla Shaman
4 Chill
2 Red Elemental Blast
1 Arcane Denial
4 Wasteland
```

##### Output
```
$ python mtgdpc.py decklist/MoMa.txt

------------------------------ MAIN DECK ------------------------------

23800 x 4 = 95200    Tundra
37999 x 4 = 151996   Volcanic Island
240 x 3 = 720        真鍮の都/City of Brass
2580 x 4 = 10320     古えの墳墓/Ancient Tomb
2800 x 4 = 11200     トレイリアのアカデミー/Tolarian Academy
310 x 4 = 1240       水蓮の花びら/Lotus Petal
13900 x 4 = 55600    モックス・ダイアモンド/Mox Diamond
900 x 4 = 3600       魔力の櫃/Mana Vault
70 x 3 = 210         通電式キー/Voltaic Key
1950 x 2 = 3900      巻物棚/Scroll Rack
1010 x 3 = 3030      精神力/Mind Over Matter
10 x 4 = 40          意外な授かり物/Windfall
40 x 4 = 160         時のらせん/Time Spiral
280 x 3 = 840        中断/Abeyance
4280 x 3 = 12840     直観/Intuition
15 x 3 = 45          魔力消沈/Power Sink
36 x 4 = 144         天才のひらめき/Stroke of Genius

main ) price: 351085

------------------------------ SIDEBOARD ------------------------------

40 x 4 = 160         ゴリラのシャーマン/Gorilla Shaman
30 x 4 = 120         寒け/Chill
25 x 2 = 50          赤霊破/Red Elemental Blast
25 x 1 = 25          秘儀の否定/Arcane Denial
2200 x 4 = 8800      不毛の大地/Wasteland

side ) price: 9155

total price (main + side): 360240

```
#### `decklist/`[5-Color-Aggro](http://mtgwiki.com/wiki/%EF%BC%95%E8%89%B2%E3%83%87%E3%83%83%E3%82%AD)
```
5-Color-Aggro [2]
土地 (24)
4	古代の聖塔/Ancient Ziggurat
1	秘儀の聖域/Arcane Sanctum
4	風変わりな果樹園/Exotic Orchard
1	森/Forest
1	島/Island
4	ジャングルの祭殿/Jungle Shrine
1	山/Mountain
1	平地/Plains
3	野蛮な地/Savage Lands
3	海辺の城塞/Seaside Citadel
1	沼/Swamp
クリーチャー (29)
4	血編み髪のエルフ/Bloodbraid Elf
3	若き群れのドラゴン/Broodmate Dragon
2	戦争のアスラ、ジェナーラ/Jenara, Asura of War
4	貴族の教主/Noble Hierarch
4	朽ちゆくヒル/Putrid Leech
4	ロウクスの戦修道士/Rhox War Monk
4	セドラクシスの死霊/Sedraxis Specter
4	長毛のソクター/Woolly Thoctar
呪文 (7)
3	ナヤの魔除け/Naya Charm
4	流刑への道/Path to Exile
サイドボード (15)
2	呪詛術士/Anathemancer
2	戦誉の天使/Battlegrace Angel
4	天界の粛清/Celestial Purge
3	妨げる光/Hindering Light
2	クァーサルの群れ魔道士/Qasali Pridemage
2	領土を滅ぼすもの/Realm Razer
```
##### Output
```
$ python mtgdpc.py decklist/5-Color-Aggro.txt

------------------------------ MAIN DECK ------------------------------

790 x 4 = 3160       古代の聖塔/Ancient Ziggurat
9 x 1 = 9            秘儀の聖域/Arcane Sanctum
10 x 4 = 40          風変わりな果樹園/Exotic Orchard
8 x 1 = 8            森/Forest
9 x 1 = 9            島/Island
9 x 4 = 36           ジャングルの祭殿/Jungle Shrine
5 x 1 = 5            山/Mountain
9 x 1 = 9            平地/Plains
9 x 3 = 27           野蛮な地/Savage Lands
9 x 3 = 27           海辺の城塞/Seaside Citadel
8 x 1 = 8            沼/Swamp
360 x 4 = 1440       血編み髪のエルフ/Bloodbraid Elf
20 x 3 = 60          若き群れのドラゴン/Broodmate Dragon
140 x 2 = 280        戦争のアスラ、ジェナーラ/Jenara, Asura of War
5790 x 4 = 23160     貴族の教主/Noble Hierarch
20 x 4 = 80          朽ちゆくヒル/Putrid Leech
9 x 4 = 36           ロウクスの戦修道士/Rhox War Monk
10 x 4 = 40          セドラクシスの死霊/Sedraxis Specter
9 x 4 = 36           長毛のソクター/Woolly Thoctar
9 x 3 = 27           ナヤの魔除け/Naya Charm
690 x 4 = 2760       流刑への道/Path to Exile

main ) price: 31257

------------------------------ SIDEBOARD ------------------------------

10 x 2 = 20          呪詛術士/Anathemancer
30 x 2 = 60          戦誉の天使/Battlegrace Angel
10 x 4 = 40          天界の粛清/Celestial Purge
10 x 3 = 30          妨げる光/Hindering Light
80 x 2 = 160         クァーサルの群れ魔道士/Qasali Pridemage
20 x 2 = 40          領土を滅ぼすもの/Realm Razer

side ) price: 350

total price (main + side): 31607
```

### Future Enhancements

- Introduce:
	- `Pandas` to manage it with `DataFrames`.
	- `Click` for better CUI experience.
- Handle more format of decklists.
- Add:
	- Card info screen with capability of search individual prices.
	- Mana info such as ratio and pie.

