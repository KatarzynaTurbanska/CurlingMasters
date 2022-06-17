import numpy as np
import pandas as pd

def gen_ranking_to_file():

    teams = pd.read_csv('../data/backup/match_opponents_v1.csv')

    teams['ranking'] = np.random.randint(1,100,len(teams))
    
    teams.to_csv('../data/backup/match_opponents_v2.csv')


if __name__ == '__main__':
    gen_ranking_to_file()