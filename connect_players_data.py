import numpy as np
import pandas as pd
import random

def teams_for_group(teams_group):
    '''
    supplementary function for add_active_players
    creating new dataframe with teams and genders 
    for each active player, used later for join 

    takes
    -----
    teams_group - datafarame with team info gruped depending 
    on age of players (either adults or juniors)

    returns
    -------
    datafrme with team name and gender for each active player in group

    '''
    teams_for_group = np.array([])
    team_genders = np.array([])
    for index, row in teams_group.iterrows():
        num = int(row['num_of_players'])
        team = np.repeat(teams_group.loc[index, 'team_name'], num)
        teams_for_group = np.concatenate((teams_for_group, team), axis=None)
        if row['category'] == 'men' or row['category'] == 'junior men':
            gender = np.repeat('M', num)
        elif row['category'] == 'women' or row['category'] == 'junior women':
            gender = np.repeat('F', num)
        else:
            gender = random.choices(['M', 'F'], k=num)
        team_genders = np.concatenate((team_genders, gender), axis=None)
    teams = pd.DataFrame({'team_name':teams_for_group, 'gender':team_genders}, columns=['team_name', 'gender'])
    return teams


def add_active_to_team(players, teams):
    '''
    function assigning each ACTIVE player from group
    (either adult or junior) a team and gender

    takes
    -----
    players - previously made dataframe with active players info
    teams - previously made dataframe with teams info

    returns
    -------
    csv file for active adults and file for active juniors
    with added columns: team name and gender
    '''
    
    adults = players[(players['category'] == 'adult')]
    adults.reset_index(inplace=True, drop=True)
    #print(len(adults))
    juniors = players[(players['category'] == 'junior')]

    adult_teams = teams[teams['category'].isin(['men', 'women', 'mixed'])] 
    adult_teams = adult_teams.sort_values(by=['facility_id', 'category']).reset_index(drop=True)
    junior_teams = teams[teams['category'].isin(['junior men', 'junior women', 'junior mixed'])]
    junior_teams = junior_teams.sort_values(by=['facility_id', 'category']).reset_index(drop=True)

    teams_for_adults = teams_for_group(adult_teams)
    #print(len(teams_for_adults))
    teams_for_juniors = teams_for_group(junior_teams)

    full_adults = adults.join(teams_for_adults, how='outer')
    full_adults.to_csv('active_adults_teams_v1.csv', index=False)
    full_juniors = juniors.join(teams_for_juniors, how="outer")
    full_juniors.to_csv('active_juniors_teams_v1.csv', index=False)


def add_retired_to_team(players, teams):
    '''
    function assigning each RETIRED player from group
    (either adult or junior) a team and gender

    takes
    -----
    players - previously made dataframe with retired players info
    teams - previously made dataframe with teams info

    returns
    -------
    csv file for retired adults and file for retired juniors
    with added columns: team name and gender
    '''

    adults = players[(players['category'] == 'adult')]
    adults.reset_index(inplace=True, drop=True)
    juniors = players[(players['category'] == 'junior')]    

    adult_teams = teams[teams['category'].isin(['men', 'women', 'mixed'])] 
    junior_teams = teams[teams['category'].isin(['junior men', 'junior women', 'junior mixed'])]

    adult_teams_in_facility = {}
    junior_teams_in_facility = {}

    for id in range(1,6):
        adult_teams_in_facility[id] = adult_teams[adult_teams['facility_id'] == id][['team_name', 'category']].values.tolist()
        junior_teams_in_facility[id] = junior_teams[junior_teams['facility_id'] == id][['team_name', 'category']].values.tolist()

    for index, row in adults.iterrows():
        id = int(row['facility_id'])
        team = random.choice(adult_teams_in_facility[id])
        adults.loc[index, 'team_name'] = team[0]
        if team[1] == 'men' or team[1] == 'junior men':
            gender = 'M'
        elif team[1] == 'women' or team[1] == 'junior women':
            gender = 'F'
        else:
            gender = random.choice(['M', 'F'])
        adults.loc[index, 'gender'] = gender

    for index, row in juniors.iterrows():
        id = int(row['facility_id'])
        team = random.choice(junior_teams_in_facility[id])
        juniors.loc[index, 'team_name'] = team[0]
        if team[1] == 'men' or team[1] == 'junior men':
            gender = 'M'
        elif team[1] == 'women' or team[1] == 'junior women':
            gender = 'F'
        else:
            gender = random.choice(['M', 'F'])
        juniors.loc[index, 'gender'] = gender

    adults.to_csv('retired_adults_teams_v1.csv', index=False)
    juniors.to_csv('retired_juniors_teams_v1.csv', index=False)

if __name__ == "__main__" :
    # for active players
    '''
    teams = pd.read_csv('teams_structure_v2.csv')
    #print(len(teams['team_name'].unique()))
    players = pd.read_csv('active_players_v2.csv')
    players = players[['birthdate','age','category','facility_id','join_date','retire_date']]
    add_active_to_team(players, teams)
    '''
    # for retired players
    '''
    teams = pd.read_csv('teams_structure_v2.csv')
    players = pd.read_csv('retired_players_v2.csv')
    players = players[['birthdate','age','category','facility_id','join_date','retire_date']]
    add_retired_to_team(players, teams)
    '''
    # to connect all togehter
    active_adult = pd.read_csv('active_adults_teams_v1.csv')
    active_junior = pd.read_csv('active_juniors_teams_v1.csv')
    retired_adult = pd.read_csv('retired_adults_teams_v1.csv')
    retired_junior = pd.read_csv('retired_juniors_teams_v1.csv')

    full_players = pd.concat([active_adult,retired_adult,active_junior,retired_junior])
    full_players = full_players.sort_values(by=['facility_id', 'team_name']).reset_index(drop=True)
    full_players.to_csv('full_players_teams_v1.csv', index=False)