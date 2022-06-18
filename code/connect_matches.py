import pandas as pd
import numpy as np


def connect_matches():
    matches = pd.read_csv('../data/backup/full_matches.csv')
    schedule = pd.read_csv('../data/backup/schedule.csv')

    data = pd.concat([matches.iloc[:,0:8],schedule])

    data = data.sort_values(by=['date'])
    data.reset_index(inplace=True,drop=True)

    data.to_csv('../data/matches.csv',index=False)


if __name__ == '__main__':
    connect_matches()