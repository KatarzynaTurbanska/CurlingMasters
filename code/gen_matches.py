import numpy as np
import pandas as pd

def download_data():

    '''
    function to download and prepare data

    '''

    global teams, home, players

    teams = pd.read_csv('../data/backup/match_opponents_v3.csv')
    home = teams[teams['facility_id'].notnull()]

    people = pd.read_csv('../data/full_people.csv')
    players = people[people['team_name'].notnull()]


def gen_match(team1,team2):

    '''
    function generating curling match with 10 ends

    returns
    -------
    team and opponent scores as lists of scores obtained in each end, 
    the number of ends, the number of endings won by our team
    '''

    r1 = home[home['team_name'] == team1].iloc[0]['ranking']
    r2 = teams[teams['team_name'] == team2].iloc[0]['ranking']
    p = (r1-r2)/200 + 0.5 # probability of winning

    team_scores = []
    opponent_scores = []

    scores = [i for i in range(9)]

    # probabilities
    distr = [0.158,0.473989,0.270,0.068,0.026,0.003,0.001,0.00001,0.000001]

  
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

        # possibility of breaking the match
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
    'match_opponents_v3.csv' and 'full_people.csv'
    and saving them to new file
    
    takes
    -----
    file_name - name of the file to which the matches will be written

    returns
    -------
    csv file with team name, date, address_id, opponent name, 
    team score, opponent score, number_of_ends,number_of_ends_won,
    id of the lead, the second, the vice and the skip
    '''

    dates = np.array(pd.date_range('2019-06-01','2022-05-30',freq='D').strftime("%Y-%m-%d").tolist())
    lockdown_dates = np.array(pd.date_range('2020-03-01','2020-06-30',freq='D').strftime("%Y-%m-%d").tolist())
    dates2 = np.setdiff1d(dates,lockdown_dates,assume_unique=True)

    with open(file_name,'w') as file:

        file.write('team_name,date,address_id,opponent_name,team_score,opponent_score,number_of_ends,number_of_ends_won,lead_id,second_id,vice_id,skip_id\n')

        for index, row in home.iterrows():
            team = row['team_name']
            category = row['category']
            teams_cat = teams[teams['category']==category]

            team_players = players[players['team_name']==team]

            n = np.random.randint(20,45)
            n_dates = np.random.choice(dates2,size=n,replace=False)
            
            for i in range(n):

                date = n_dates[i]
                cond = ((team_players['join_date'] <= date) & ((team_players['retire_date'] >= date) | (team_players['retire_date'].isnull())))
                team_active = team_players[cond]

                opponent_name = np.random.choice(teams_cat[teams_cat['team_name'] != team]['team_name'])
                
                our_opponent = False

                # checking if opponent is one of our teams
                if opponent_name in np.array(home['team_name']):

                    opponent_players = players[players['team_name']==opponent_name]
                    cond2 = ((opponent_players['join_date'] <= date) & ((opponent_players['retire_date'] >= date) | (opponent_players['retire_date'].isnull())))
                    opponent_active = opponent_players[cond2]

                    our_opponent = True
                
                # checking if we can complete a team
                if len(team_active) >= 4 and (our_opponent == False or len(opponent_active) >= 4):
                    
                    address_id = teams_cat[teams_cat['team_name'] == opponent_name].iloc[0]['address_id']

                    scores = gen_match(team,opponent_name)

                    team_score = np.sum(scores[0])
                    opponent_score = np.sum(scores[1])
                    n_ends = scores[2]
                    n_wins = scores[3]

                    lineup = np.random.choice(list(team_active.index),size=4,replace=False)

                    match = '{},{},{},{},{},{},{},{},{},{},{},{}\n'.format(team,date,address_id,opponent_name,team_score,opponent_score,n_ends,n_wins,lineup[0],lineup[1],lineup[2],lineup[3])
                    file.write(match)

                    if our_opponent:

                        lineup = np.random.choice(list(opponent_active.index),size=4,replace=False)

                        match = '{},{},{},{},{},{},{},{},{},{},{},{}\n'.format(opponent_name,date,address_id,team,opponent_score,team_score,n_ends,n_ends-n_wins,lineup[0],lineup[1],lineup[2],lineup[3])
                        file.write(match)

                    


if  __name__ == "__main__":
    download_data()

    gen_matches_to_file('../data/backup/full_matches.csv')