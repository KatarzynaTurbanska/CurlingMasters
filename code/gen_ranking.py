from turtle import home
import numpy as np
import pandas as pd

def gen_ranking_to_file():

    teams = pd.read_csv('../data/match_opponents_v1.csv')

    teams['ranking'] = np.random.randint(1,100,len(teams))
    
    teams.to_csv('../data/match_opponents_v2.csv')


if __name__ == '__main__':
    gen_ranking_to_file()