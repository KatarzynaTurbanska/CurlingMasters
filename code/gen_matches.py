import numpy as np
import pandas as pd

def download_data():
    global home, opponent

    home = pd.read_csv('../data/home_team_names2.csv')
    opponent = pd.read_csv('../data/opponent_team_names2.csv')


def gen_match(team1,team2):

    '''
    function generating curling match with 10 ends

    returns
    -------
    team and opponent scores as lists of scores obtained in each end
    '''

    r1 = home[home['team_name'] == team1].iloc[0]['ranking']
    r2 = opponent[opponent['team_name'] == team2].iloc[0]['ranking']
    p = (r1-r2)/200 + 0.5

    team_scores = []
    opponent_scores = []

    scores = [i for i in range(9)]

    distr = [0.158,0.473989,0.270,0.068,0.026,0.003,0.001,0.00001,0.000001]

    # kobiety: 0 -> 66|1 -> 217|2 -> 129|3 -> 35|4 -> 14|5 -> 1|6 -> 0|7 -> 0|8 -> 0||suma -> 462||
    # mężczyźni: 0 -> 79|1 -> 217|2 -> 118|3 -> 27|4 -> 10|5 -> 2|6 -> 1|7 -> 0|8 -> 0||suma -> 454||
    # suma: 916

    # sprawdzać czy drużyny są z tej samej kategorii
    # generować skład - 4 kolumny z pozycjami i do każej kolumny losować zawodników z drużyny
    # uwzględnić mecze między naszymi druzynami

    n = 1
    n_wins = 0
    con = True
    while con:

        if n >= 10 and (sum(team_scores) != sum(opponent_scores)):
            break

        U = np.random.uniform(0,1)

        if U <= p:
            score = np.random.choice(scores,p=distr)
            team_scores.append(score)
            opponent_scores.append(0)
            if score != 0:
                n_wins += 1
        else:
            team_scores.append(0)
            opponent_scores.append(np.random.choice(scores,p=distr))

        if n >=5 and np.abs(sum(team_scores) - sum(opponent_scores)) >= 6:
            U2 = np.random.uniform(0,1)
            if U2 <= 0.7:
                break
            else:
                pass

        n += 1

    
    return team_scores, opponent_scores, n, n_wins 


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

    # home = pd.read_csv('../data/home_team_names.csv')
    # opponent = pd.read_csv('../data/opponent_team_names.csv')
    dates = np.array(pd.date_range('2019-06-01','2022-05-31',freq='D').strftime("%Y-%m-%d").tolist())
    lockdown_dates = np.array(pd.date_range('2020-03-01','2020-06-30',freq='D').strftime("%Y-%m-%d").tolist())
    dates2 = np.setdiff1d(dates,lockdown_dates,assume_unique=True)

    with open(file_name,'w') as file:

        for team in home['team_name']:

            n = np.random.randint(10,31)

            for _ in range(n):

                date = np.random.choice(dates2)
                opponent_name = np.random.choice(opponent['team_name'])

                scores = gen_match(team,opponent_name)

                team_score = np.sum(scores[0])
                opponent_score = np.sum(scores[1])
                n_ends = scores[2]
                n_wins = scores[3]
                match = '{},{},{},{},{},{},{}\n'.format(team,date,opponent_name,team_score,opponent_score,n_ends,n_wins)
                file.write(match)


if  __name__ == "__main__":
    download_data()
    # match = gen_match('Ottawa Victorias','Melfort Bruins')
    # print(match[0])
    # print(match[1])
    # print(match[2],match[3])

    gen_matches_to_file('../data/matches.csv')