import numpy as np
import pandas as pd
import random

def gen_schedule_to_file(file_name):

    '''
    function generating schedule,
    for dates between 01.06.2022 and 31.05.2023, based on 
    'match_opponents_v3.csv' and saving them to new file
    
    takes
    -----
    file_name - name of the file to which the schedule will be written

    returns
    -------
    csv file with home team name, date and opponent team name
    '''

    teams = pd.read_csv('../data/backup/match_opponents_v3.csv')
    home = teams[teams['facility_id'].notnull()]

    dates = pd.date_range('2022-06-01','2023-05-31',freq='D').strftime('%Y-%m-%d')

    with open(file_name,'w') as file:

        file.write('team_name,date,address_id,opponent_name\n')
        dict_dates = {}

        for index, row in home.iterrows():

            team = row['team_name']
            category = row['category']

            teams_cat = teams[teams['category']==category]
            n = np.random.randint(2,19)

            for _ in range(n):

                date = random.choice(dates)
                opponent_name = np.random.choice(teams_cat[teams_cat['team_name'] != team]['team_name'])

                if team not in dict_dates:
                    dict_dates[team] = []
                if opponent_name not in dict_dates:
                    dict_dates[opponent_name] = []

                if  date not in dict_dates[team] and date not in dict_dates[opponent_name]:
                    dict_dates[team].append(date)
                    dict_dates[opponent_name].append(date)  

                    address_id = teams_cat[teams_cat['team_name'] == opponent_name].iloc[0]['address_id']

                    future_match = '{},{},{},{}\n'.format(team,date,address_id,opponent_name)
                    file.write(future_match)

                    if opponent_name in np.array(home['team_name']):

                        future_match = '{},{},{},{}\n'.format(opponent_name,date,address_id,team)
                        file.write(future_match)


if  __name__ == "__main__":
    gen_schedule_to_file('../data/backup/schedule.csv')