from turtle import home
import numpy as np
import pandas as pd

def gen_ranking_to_file():

    home = pd.read_csv('../data/home_team_names.csv')
    opponent = pd.read_csv('../data/opponent_team_names.csv')

    home['ranking'] = np.random.randint(1,100,len(home))
    opponent['ranking'] = np.random.randint(1,100,len(opponent))
    
    #home.to_csv('../data/home_team_names2.csv')
    #opponent.to_csv('../data/opponent_team_names2.csv')


if __name__ == '__main__':
    gen_ranking_to_file()