import pandas as pd
import random

# how real_names was prepared
'''
real_names.replace(';', ',')
    for index, row in real_names.iterrows(): #419
        team = row['real_teams']
        if ("/" not in team) and ("'" not in team) and (team.startswith('St.') == False):
            words = team.split(' ')
            if len(words) == 2:
                real_names.loc[index, 'first_word'] = words[0]
                real_names.loc[index, 'second_word'] = words[1]

            elif len(words) == 3:
                real_names.loc[index, 'first_word'] = words[0] + ' ' + words[1]
                real_names.loc[index, 'second_word'] = words[2]
real_names.to_csv('real_names.csv', index=False)
'''

def gen_names(base_file, team, n):
    '''
    function generating team names based on 
    real team names from given file and saving them to file
    can generate names for our and opponents teams

    takes
    -----
    base_file - file with some real names for reference
    team - 'home' for our teams and 'opponent' for opponent teams
    n - how many names to generate (min 14)

    returns
    -------
    csv file with names 

    '''
    real_names = pd.read_csv(base_file)
    real_names.replace('', float("NaN"), inplace=True)
    real_names.replace('???', float("NaN"), inplace=True)
    real_names.dropna(inplace=True)

    second_words = real_names['second_word'] # all possible second parts of the team name
    
    if team == 'opponent':
        first_words = real_names['first_word']
        with open('test2.csv', 'a') as file: #'opponent_team_names.csv'
            file.write('team_name')
            file.write('\n')
            teams = []
            while len(teams) < n:
                name = str(random.choice(first_words) + ' ' + random.choice(second_words))
                if name not in teams:
                    teams.append(name)
                    file.write(name)
                    file.write('\n')
             
    if team == 'home':
        cities = ['Toronto', 'Montreal', 'Calgary', 'Ottawa', 'Vancouver', 'Toronto', 'Montreal', 'Calgary', 'Ottawa', 'Vancouver'] # we want min 2 teams from 1 city 
        first_words = ['Toronto', 'Montreal', 'Calgary', 'Ottawa', 'Vancouver', 'Broom', 'Stone', 'Ice', 'Cold', 'Curlers', 'Super'] # all possible first parts of team name
        with open('test1.csv', 'a') as file: #'home_team_names.csv'
            file.write('team_name')
            file.write('\n')
            teams = ['Ice Unicorns', 'Baby Broomers', 'Rolling Stones', 'Game of Stones'] # some names we just had to add because of how lovely they are
            file.write('Ice Unicorns\nBaby Broomers\nRolling Stones\nGame of Stones\n')
            while len(teams) < 14: 
                for city in cities:
                    name = str(city + ' ' + random.choice(second_words))
                    if name not in teams:
                        teams.append(name)
                        file.write(name)
                        file.write('\n')
            while len(teams) < n:
                name = str(random.choice(first_words) + ' ' + random.choice(second_words)) #
                if name not in teams:
                    teams.append(name)
                    file.write(name)
                    file.write('\n')

    

           
if __name__ == "__main__" :
    # real_names.csv is a list of real Canadian Junior Hockey League team names
    gen_names('real_team_names.csv', 'home', 43) 
    gen_names('real_team_names.csv', 'opponent', 100)
