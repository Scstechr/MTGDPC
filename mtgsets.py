from mtgsdk import Card
from mtgsdk import Set
import pandas as pd
pd.set_option('display.max_columns', 100)
pd.set_option('display.max_rows', 500)

def main():
    setlist = Set.all()
    d = {}
    d['date'] = []
    d['type'] = []
    d['name'] = []
    d['code'] = []
    
    for s in setlist:
        if s.type in ['core', 'expansion']:
            d['date'].append(s.release_date)
            d['type'].append(s.type)
            d['name'].append(s.name)
            d['code'].append(s.code)

    df = pd.DataFrame(d).sort_values('date').set_index('date')
    print(df)
if __name__ == "__main__":
    main()

