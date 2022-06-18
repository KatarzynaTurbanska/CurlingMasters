import numpy as np
import pandas as pd

def gen_position_to_file():

    matches = pd.read_csv('../data/backup/full_matches.csv')
    n = len(matches)

    lead = matches[['lead','date']]
    lead.rename(columns={'lead':'person_id'},inplace=True)
    lead = lead.assign(position=['lead' for _ in range(n)])

    second = matches[['second','date']]
    second.rename(columns={'second':'person_id'},inplace=True)
    second = second.assign(position=['second' for _ in range(n)])

    vice = matches[['vice','date']]
    vice.rename(columns={'vice':'person_id'},inplace=True)
    vice = vice.assign(position=['vice' for _ in range(n)])

    skip = matches[['skip','date']]
    skip.rename(columns={'skip':'person_id'},inplace=True)
    skip = skip.assign(position=['skip' for _ in range(n)])

    positions = pd.concat([lead,second,vice,skip])

    positions = positions.sort_values(by=['date'])

    positions.to_csv('../data/positions.csv',index=False)
    


if __name__ == '__main__':
    gen_position_to_file()