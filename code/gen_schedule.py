import numpy as np
import pandas as pd
import random

def gen_schedule_to_file(file_name):

    '''
    function generating schedule,
    for dates between 01.06.2022 and 31.05.2023, based on 
    'home_team_names.csv' and 'opponent_team_names.csv'
    and saving them to new file
    
    takes
    -----
    file_name - name of the file to which the schedule will be written

    returns
    -------
    csv file with home team name, date and opponent team name
    '''

    home = pd.read_csv('../data/home_team_names.csv')
    opponent = pd.read_csv('../data/opponent_team_names.csv')

    with open(file_name,'w') as file:

        for team in home['team_name']:

            n = np.random.randint(2,19)

            for _ in range(n):
                date = pd.date_range('2022-06-01','2023-05-31',freq='D')
                future_match = '{},{},{}\n'.format(team,random.choice(date).strftime('%Y-%m-%d'),np.random.choice(opponent['team_name']))
                file.write(future_match)


if  __name__ == "__main__":
    gen_schedule_to_file('../data/schedule.csv')