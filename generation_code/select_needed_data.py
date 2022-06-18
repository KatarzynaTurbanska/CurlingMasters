from dataclasses import replace
import pandas as pd

phone_book = pd.read_csv('../data/phone_book.csv')
phone_book.to_csv('../final_data/phone_book.csv', index=False)

gender = pd.read_csv('../data/gender.csv')
gender = gender[['name', 'gender']]
gender.rename(columns={'name':'first_name'}, inplace=True)
gender.to_csv('../final_data/gender.csv', index=False)

finances = pd.read_csv('../data/finances.csv')
finances.to_csv('../final_data/finances.csv', index=False)

people = pd.read_csv('../data/people.csv')
people.rename(columns={'name':'first_name', 'id':'person_id'}, inplace=True)
people.to_csv('../final_data/people.csv', index=False)

def connect_people_addresses():
    cities = {1:'Toronto', 2:'Montreal', 3:'Calgary', 4:'Ottawa', 5:'Vancouver'}
    address_id = pd.read_csv('../data/addresses.csv')
    address_id = address_id.iloc[104:,:] 
    people_id = pd.read_csv('../data/full_people.csv')
    address = []
    for id in range(1,6):
        p = people_id[people_id['facility_id'] == id]
        a = address_id[address_id['city'] == cities[id]]
        p.reset_index(inplace=True,drop=True)
        a.reset_index (inplace=True,drop=True)

        address.append(pd.concat([p[['person_id']],a[['address_id']]],axis=1))

    address[0].to_csv('../final_data/address.csv', index=False)

connect_people_addresses()

personal_info = pd.read_csv('../data/full_people.csv')
personal_info = personal_info[['person_id', 'team_name', 'position', 'birthdate', 'join_date', 'retire_date']]
personal_info.to_csv('../final_data/personal_info.csv', index=False)

positions = pd.read_csv('../data/positions.csv')
positions.to_csv('../final_data/positions.csv', index=False)

address_book = pd.read_csv('../data/addresses.csv')
address_book.to_csv('../final_data/address_book.csv', index=False)

def format_teams():
    teams = pd.read_csv('../data/backup/home_teams_structure_v1.csv')
    for index, row in teams.iterrows():
        cat = row['category'].split(' ')
        if len(cat) == 1:
            teams.loc[index, 'age_category'] = 'adult'
            teams.loc[index, 'gender_category'] = cat[0]
        else:
            teams.loc[index, 'age_category'] = cat[0]
            teams.loc[index, 'gender_category'] = cat[1]
    teams = teams[['team_name', 'facility_id', 'age_category', 'gender_category']]
    teams.to_csv('../final_data/teams.csv', index=False)

format_teams()

mat = pd.read_csv('../data/matches.csv')
matches = mat[['team_name', 'date', 'address_id', 'team_score', 'opponent_score', 'number_of_ends', 'number_of_ends_won']]
matches.rename(columns={ 'number_of_ends_won': 'ends_won'}, inplace=True)
matches.to_csv('../final_data/matches.csv', index=False)
opponents = mat[['team_name', 'date', 'opponent_name']]
opponents.to_csv('../final_data/opponents.csv', index=False)

age_category = pd.DataFrame({'age_category':['junior', 'adult'], 'age_min':[7, 22], 'age_max':[21, 50]})
age_category.to_csv('../final_data/age_category.csv', index=False)

fac = pd.read_csv('../data/facility.csv')
facility = fac[['facility_id', 'address_id']]
facility.to_csv('../final_data/facility.csv', index=False)
equipment = fac[['facility_id', 'brooms', 'stones', 'shoes']]
equipment.to_csv('../final_data/equipment.csv', index=False)
