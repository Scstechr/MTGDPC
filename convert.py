deckname = 'MoMa.txt'

l = []
side = []
flag = 0
with open(deckname, 'r') as rf:
    for r in rf:
        if r[0] == 'サ':
            flag = 1
        try:
            int(r[0])
            r = r.replace('\t',' ')
            if r.count('/') > 0:
                r = r[:r.find(' ')] + ' ' + r[r.find('/') + 1:]
            l.append(r) if not flag else side.append(r)
        except:
            pass

l = l + ['\nSideboard\n'] + side
for item in l:
    print(item, end = '')

'''
MoMa [1]
土地 (19)
4	Tundra
4	Volcanic Island
3	真鍮の都/City of Brass
4	古えの墳墓/Ancient Tomb
4	トレイリアのアカデミー/Tolarian Academy
クリーチャー (0)
呪文 (41)
4	水蓮の花びら/Lotus Petal
4	モックス・ダイアモンド/Mox Diamond
4	魔力の櫃/Mana Vault
3	通電式キー/Voltaic Key
2	巻物棚/Scroll Rack
3	精神力/Mind Over Matter
4	意外な授かり物/Windfall
4	時のらせん/Time Spiral
3	中断/Abeyance
3	直観/Intuition
3	魔力消沈/Power Sink
4	天才のひらめき/Stroke of Genius
サイドボード (15)
4	ゴリラのシャーマン/Gorilla Shaman
4	寒け/Chill
2	赤霊破/Red Elemental Blast
1	秘儀の否定/Arcane Denial
4	不毛の大地/Wasteland
'''
