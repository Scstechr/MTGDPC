# MTGDPC
Magic the Gathering Deck Price Checker (mainly for JPN Players).  

Consists of `mtgdpc.py` and `carddl.py`, which `carddl.py` could be utilized independently.  
`mtgdpc.py` calls `carddl.py` within process if `-s`(`--save`) argument is triggered.  
Both of them supports `--help` option in order to check arguments and its individual function.

## About

MTGDPC (`mtgdpc`) enables users to search the cheapest price for a given card name via [Wisdom Guild](http://www.wisdom-guild.net).  
If `-s`(`--save`) option is triggered, it scrapes card image contained in the decklist via:

- `mtgsdk` (official API) 
- [scryfall.com](https://scryfall.com/) (if `-h`(`--high`, high-res option) is active).

### Requirements

- [x] Python 3.6 (or above)

- [x] Beautiful Soup
- [x] lxml
- [x] tqdm
- [x] requests
- [x] mtgsdk

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



## Future Enhancements

- Introduce:
  - [ ] Pandas` to manage it with `DataFrames`.
  - [x] Click` for better CUI experience.
- [ ] Handle more format of decklists.
- [ ] Refactoring for a more sophisticated structure.
- Add:
  - [ ] Card info screen with capability of searching individual prices.
  - [ ] Mana info such as ratio and pie.

