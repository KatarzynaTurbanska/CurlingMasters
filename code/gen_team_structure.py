import pandas as pd
import random

def gen_structure(home, teams_names, file_name):
    '''
    function connecting names of teams, adding in which 
    facility they are, how many members they have and
    what category the team is

    takes
    -----
    home[bool] - if true generates structure for home teams
    else for opponents
    teams_names - csv file with team names
    file_name - name of file we want to save generated data in

    returns
    -------
    csv file with team structure

    '''
    names = pd.read_csv(teams_names)['team_name']
    teams = pd.DataFrame(columns=['team_name'], index=range(len(names)))
    cat = ['junior men', 'junior women', 'junior mixed', 'mixed', 'men', 'women']
    fac = {'Toronto':1, 'Montreal':2, 'Calgary':3, 'Ottawa':4, 'Vancouver':5}

    for index, row in teams.iterrows():
        teams.loc[index, 'team_name'] = names[index]
        teams.loc[index, 'category'] = random.choice(cat)
        if home:
            city = names[index].split(' ')[0]
            if city in fac.keys():
                teams.loc[index, 'facility_id'] = fac[city]
            else:
                teams.loc[index, 'facility_id'] = random.randint(1,5)
            teams.loc[index, 'num_of_players'] = random.randint(4,8)
        
    teams.to_csv(file_name, index=False)

def connect_adresses(home, teams_data, addreses, file_name):
    '''
    function connecting teams data with adresses of facilities they from

    takes
    -----
    home[bool] - if true generates structure for home teams
    else for opponents
    teams_data - csv base file with only id column
    adresses - csv file with addresses of facilities
    file_name - name of file we want to save generated data in

    returns
    -------
    csv file with team structure and address

    '''
    teams = pd.read_csv(teams_data) 
    address = pd.read_csv(addreses)
    fac = {1:'Toronto', 2:'Montreal', 3:'Calgary', 4:'Ottawa', 5:'Vancouver'}

    if home: 
        address = address[:5]
        for index, row in teams.iterrows():
            city = fac[row['facility_id']]
            teams.loc[index, 'city'] = city
            teams.loc[index, 'street'] = address[address['city'] == city].iloc[0]['street']
            teams.loc[index, 'street_number'] = address[address['city'] == city].iloc[0]['street_number']
        
    else:
        address = address[5:].reset_index(drop=True)
        for index, row in teams.iterrows():
            teams.loc[index, 'city'] = address.loc[index, 'city']
            teams.loc[index, 'street'] = address.loc[index, 'street'] 
            teams.loc[index, 'street_number'] = address.loc[index, 'street_number']
        

    teams.to_csv(file_name, index=False)
      
if __name__ == "__main__" :
    # home teams
    '''
    gen_structure(True, '../data/backup/home_team_names.csv', '../data/backup/home_teams_structure_v1.csv') 
    connect_adresses(True, '../data/backup/home_teams_structure_v1.csv', '../data/addresses_facilities.csv','../data/home_teams_structure_v2.csv')
    '''
    # opponents
    '''
    gen_structure(False, '../data/backup/opponent_team_names.csv', '../data/backup/opponent_teams_structure_v1.csv') 
    connect_adresses(False, '../data/backup/opponent_teams_structure_v1.csv', '../data/addresses_facilities.csv','../data/backup/opponent_teams_structure_v2.csv')
    '''
    # connecting data toogether for full oponents for matches list
    '''
    home = pd.read_csv('../data/home_teams_structure_v2.csv')
    opponents = pd.read_csv('../data/backup/opponent_teams_structure_v2.csv')
    
    full_match_opponents = pd.concat([home, opponents])
    full_match_opponents = full_match_opponents.sort_values(by=['category']).reset_index(drop=True)
    full_match_opponents.to_csv('../data/backup/match_opponents_v1.csv', index=False)
   '''