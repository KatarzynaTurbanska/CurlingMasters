import numpy as np
import pandas as pd

def gen_match(n):

    '''
    function generating curling match
    
    takes
    -----
    n - number of ends

    returns
    -------
    team and opponent scores as lists of scores obtained in each end
    '''

    team_scores = []
    opponent_scores = []

    scores = [i for i in range(1,9)]
    distr = [0.3,0.3,0.18,0.1,0.05,0.05,0.01,0.01] # ?????

    for _ in range(n):
        U = np.random.randint(0,2) # the same probability or not ?
        if U == 1:
            team_scores.append(np.random.choice(scores,p=distr))
            opponent_scores.append(0)
        else:
            team_scores.append(0)
            opponent_scores.append(np.random.choice(scores,p=distr))

    return team_scores, opponent_scores


def gen_matches_to_file(file_name):

    '''
    function generating matches,
    for dates between 01.06.2019 and 31.05.2022, based on 
    'home_team_names.csv' and 'opponent_team_names.csv'
    and saving them to new file
    
    takes
    -----
    file_name - name of the file to which the matches will be written

    returns
    -------
    csv file with team name, date, opponent name, team score, opponent score
    '''

    home = pd.read_csv('../data/home_team_names.csv')
    opponent = pd.read_csv('../data/opponent_team_names.csv')
    dates = np.array(pd.date_range('2019-06-01','2022-05-31',freq='D').strftime("%Y-%m-%d").tolist())
    lockdown_dates = np.array(pd.date_range('2020-03-01','2020-06-30',freq='D').strftime("%Y-%m-%d").tolist())
    dates2 = np.setdiff1d(dates,lockdown_dates,assume_unique=True)

    with open(file_name,'w') as file:

        for team in home['team_name']:

            n = np.random.randint(10,31)

            for _ in range(n):
                date = np.random.choice(dates2)
                opponent_name = np.random.choice(opponent['team_name'])

                scores = gen_match(9)
                team_score = np.sum(scores[0])
                opponent_score = np.sum(scores[1])
                match = '{},{},{},{},{}\n'.format(team,date,opponent_name,team_score,opponent_score)
                file.write(match)


if  __name__ == "__main__":
    gen_matches_to_file('../data/matches.csv')