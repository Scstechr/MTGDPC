import subprocess as sp

def convert(deckname):
    l = []
    side = []
    flag = 0
    with open(deckname, 'r') as rf:
        for r in rf:
            if r[0] == 'サ':
                flag = 1
            if r.count('\t') > 0:
                r = r.replace('\t',' ')
                if r.count('/') > 0:
                    r = r[:r.find(' ')] + ' ' + r[r.find('/') + 1:]
                l.append(r) if not flag else side.append(r)

    l = l + ['\nSideboard\n'] + side
    sp.call(f'rm -rf {deckname}', shell=True)
    for item in l:
        if item == '\nSideboard\n':
            sp.call(f'echo "" >> {deckname}', shell=True)
        sp.call(f'echo "{item.strip()}" >> {deckname}', shell=True)

if __name__ == '__main__':
    deckname = '5-Color-Aggro.txt'
    convert(deckname)
