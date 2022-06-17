from matplotlib.pyplot import connect
import pandas as pd
import numpy as np


def connect_people():
    players = pd.read_csv('../data/backup/full_players_teams_v1.csv')
    employees = pd.read_csv('../data/backup/full_employees_v1.csv')

    data = pd.concat([players,employees])

    data = data.sort_values(by=['join_date'])
    data.reset_index(inplace=True)

    data = data.iloc[:,1:12]
    data.index.name = 'person_id'
    data.to_csv('../data/full_people.csv')

if __name__ == '__main__':
    connect_people()