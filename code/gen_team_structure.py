import pandas as pd
import random

def gen_structure(template, teams_names):
    '''
    function connecting names of teams, adding in which 
    facility they are, how many members they have and
    what category the team is

    takes
    -----
    template - csv base file with only id column up to 43
    teams_names - csv file with team names

    returns
    -------
    csv file with team structure

    '''
    teams = pd.read_csv(template) 
    names = pd.read_csv(teams_names)['team_name']
    cat = ['junior men', 'junior women', 'junior mixed', 'mixed', 'men', 'women']
    fac = {'Toronto':1, 'Montreal':2, 'Calgary':3, 'Ottawa':4, 'Vancouver':5}

    for index, row in teams.iterrows():
        teams.loc[index, 'team_name'] = names[index]
        city = names[index].split(' ')[0]
        if city in fac.keys():
            teams.loc[index, 'facility_id'] = fac[city]
        else:
            teams.loc[index, 'facility_id'] = random.randint(1,5)
        teams.loc[index, 'category'] = random.choice(cat)
        teams.loc[index, 'num_of_players'] = random.randint(4,8)
        
    teams.to_csv('teams_structure.csv', index=False)

      
if __name__ == "__main__" :
    # "teams.csv" is just a ready template with id up to 43, NOT INCLUDED
    gen_structure('teams.csv', 'home_teams_names.csv') 
 