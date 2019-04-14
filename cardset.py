from mtgsdk import Set
import click

# this have to be updated. (2019/04)
STANDARD = ['XLN', 'RIX', 'DOM', 'M19', 'GRN', 'RNA']

@click.command()
@click.option('-c', '--code')
@click.option('-n', '--name')
@click.option('-b', '--block')
@click.option('-m', '--mkm_id')
@click.option('-f', '--format_')
@click.option('-t', '--type_')
def main(code, name, block, mkm_id, format_, type_):
    sets = Set.all()
    lst = []
    if code:
        [lst.append(s) for s in sets if s.code.lower().count(code)]
    elif name:
        [lst.append(s) for s in sets if s.name.lower().count(name)]
    elif block:
        [lst.append(s) for s in sets if s.block.lower().count(block)]
    elif format_:
        expcore = [s for s in sets if s.type in ['expansion', 'core']]
        if format_ =='standard':
            [lst.append(s) for s in sets if s.code in STANDARD]
        elif format_ =='modern':
            [lst.append(s) for s in expcore if int(s.release_date.replace('-','')) > 20030727]
        elif format_ in ['legacy', 'vintage']:
            portal = ['PK', 'PTK', 'P2', 'P02', 'P1', 'POR']
            [lst.append(s) for s in expcore]
            [lst.append(s) for s in sets if s.code in portal]
            [lst.append(s) for s in sets if s.type == 'duel_deck']
            [lst.append(s) for s in sets if s.type == 'from_the_vault']
        else:
            lst.append([s for s in sets])
    for s in lst:
        print(s.code, '|', s.name)

if __name__ == '__main__':
    main()

