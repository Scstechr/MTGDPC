# MTGDPC
Magic the Gathering Deck Price Checker (for JPN Players).  

Consists of `mtgdpc.py` and `carddl.py`, which `carddl.py` could be utilized independently.  
`mtgdpc.py` calls `carddl.py` within process if `-s` argument is triggered.  
Both of them supports `--help` option in order to check arguments and its individual function.

## About

MTGDPC (`mtgdpc`) enables users to search the cheapest price of given card name via [Wisdom Guild](http://www.wisdom-guild.net).

### Requirements

- Python 3.6 (or above)
- Beautiful Soup
- lxml
- tqdm
- requests
- mtgsdk

Simply, `pip install -r requirements.txt` to install above mentioned modules.

## How to use

### 1. Prepare decklist
- `.txt` file of decklist must fit either Format (A) or (B).
- `decklist/` directory contains some sample `.txt` files.  
#### Format (A) Basic Format
Note that card name must be in English.  
```
<# of cards> <card name>
...

Sideboard
<# of cards> <card name>
...
```
Also, other format will be automatically converted to this format.
#### Format (B) M:TG Wiki Style
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

### 2. Execute `mtgdpc.py` with argument of prepared `.txt` file
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

## Sample Decklist & Output

### `decklist/MoMa.txt`
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

#### Output

<img src="https://user-images.githubusercontent.com/28348249/55680838-183b9f00-595a-11e9-8973-c0ddb1dfa372.png" alt="MoMa_Snapshot" title="MoMa">

### `decklist/`[5-Color-Aggro](http://mtgwiki.com/wiki/%EF%BC%95%E8%89%B2%E3%83%87%E3%83%83%E3%82%AD)
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
#### Output

<img src="https://user-images.githubusercontent.com/28348249/55680837-140f8180-595a-11e9-96b1-88fac430a149.png" alt="5ColorAggro_Snapshot" title="5ColorAggro">

## Future Enhancements

- Introduce:
	- `Pandas` to manage it with `DataFrames`.
	- `Click` for better CUI experience.
- Handle more format of decklists.
- Add:
	- Card info screen with capability of searching individual prices.
	- Mana info such as ratio and pie.

