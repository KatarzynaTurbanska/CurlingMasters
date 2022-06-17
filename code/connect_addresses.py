from matplotlib.pyplot import connect
import pandas as pd
import numpy as np


def connect_addresses():
    facility = pd.read_csv('../data/addresses_facilities.csv')
    people = pd.read_csv('../data/addresses_people.csv')
    match = pd.read_csv('../data/match_opponents_v2.csv')

    data = pd.concat([facility,people])
    data.reset_index(inplace=True)
    data.rename(columns={'index':'address_id'},inplace=True)

    data2 = pd.merge(data,match, on=['city','street','street_number'],)
    data2.drop(['Unnamed: 0'],axis=1,inplace=True)
    data2.to_csv('../data/match_opponents_v3.csv')

    data.index.name = 'address_id'
    data = data.iloc[:,1:4]
    data.to_csv('../data/addresses.csv')


if __name__ == '__main__':
    connect_addresses()