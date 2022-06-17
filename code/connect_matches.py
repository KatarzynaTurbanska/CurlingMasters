from matplotlib.pyplot import connect
import pandas as pd
import numpy as np


def connect_matches():
    matches = pd.read_csv('../data/full_matches.csv')
    schedule = pd.read_csv('../data/schedule.csv')

    data = pd.concat([matches,schedule])

    data = data.sort_values(by=['date'])
    data.reset_index(inplace=True,drop=True)

    data.to_csv('../data/matches.csv')


if __name__ == '__main__':
    connect_matches()