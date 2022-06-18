import numpy as np
import pandas as pd
import random, math

def gen_employees(active, today, establishment, n, positions_list, facility_list, file_name):
    '''
    function appending birthdays, hire daes, retire dates,
    supplementary age, position and facility_id to base file with id

    takes
    -----
    active[bool] - are we generating active or retired players
    today - date of database creation
    establishment - date of club establishment
    n - number of employees to generate
    positions_list - list of positions for the employees
    facility_list - list of facilities coressponding to positions
    file_name - name of file we want to save generated data in

    returns
    -------
    csv file with birthdays, join date, retire date, age, position
    and facility_id

    '''
    dates = pd.DataFrame(columns=['birthdate'], index=range(n))
    dates['birthdate'] = np.nan
    dates['join_date'] = np.nan
    dates['retire_date'] = np.nan

    birthday_range_1 = pd.date_range('1967-05-30','2004-05-30',freq='D')
    birthday_range_2 = pd.date_range('1957-05-30','1997-05-30',freq='D')
    join_dates = pd.date_range(establishment, today, freq='D')

    for index, row in dates.iterrows():
        dates.loc[index, 'position'] = positions_list[index]
        dates.loc[index, 'facility_id'] = facility_list[index]

        if positions_list[index] == 'coach' or positions_list[index] == 'cleaner':
            birthdate = random.choice(birthday_range_1)
        else:
            birthdate = random.choice(birthday_range_2)

        dates.loc[index, 'birthdate'] = birthdate
        age = math.floor((today - birthdate)/np.timedelta64(1, 'Y'))
        dates.loc[index, 'age'] = age 

        if pd.to_datetime(birthdate) + np.timedelta64(18, 'Y') < establishment:
            join = random.choice(join_dates)
            dates.loc[index, 'join_date'] = join
        else: 
            join_dates_2 = pd.date_range(pd.to_datetime(birthdate) + np.timedelta64(18, 'Y'), today, freq='D')
            join = random.choice(join_dates_2)
            dates.loc[index, 'join_date'] = join
    
        if not active:
            retire_dates = pd.date_range(pd.to_datetime(join) + np.timedelta64(1, 'D'), today, freq='D')
            dates.loc[index, 'retire_date'] = random.choice(retire_dates)

    dates['birthdate'] = dates['birthdate'].dt.strftime('%Y-%m-%d')
    dates['age'] = dates['age'].astype(int)
    dates['join_date'] = dates['join_date'].dt.strftime('%Y-%m-%d')
    if not active:
        dates['retire_date'] = dates['retire_date'].dt.strftime('%Y-%m-%d')
    dates.to_csv(file_name, index=False)


if __name__ == "__main__" :
    today = pd.to_datetime('2022-05-30')
    establishment = pd.to_datetime('2019-06-01') 

    # for active employees
    '''
    positions_1 = ['cleaner' for _ in range(8)] + ['director'] + ['manager' for _ in range(7)] + ['medic' for _ in range(2)] + ['psychologist' for _ in range(1)] + ['accountant' for _ in range(1)] + ['coach' for _ in range(4)]
    positions_2 = ['cleaner' for _ in range(5)] + ['director'] + ['manager' for _ in range(10)] + ['medic' for _ in range(3)] + ['psychologist' for _ in range(1)] + ['accountant' for _ in range(2)] + ['coach' for _ in range(5)]
    positions_3 = ['cleaner' for _ in range(6)] + ['director'] + ['manager' for _ in range(10)] + ['medic' for _ in range(2)] + ['psychologist' for _ in range(2)] + ['accountant' for _ in range(1)] + ['coach' for _ in range(6)]
    positions_4 = ['cleaner' for _ in range(9)] + ['director'] + ['manager' for _ in range(8)] + ['medic' for _ in range(1)] + ['psychologist' for _ in range(2)] + ['accountant' for _ in range(2)] + ['coach' for _ in range(4)]
    positions_5 = ['cleaner' for _ in range(10)] + ['director'] + ['manager' for _ in range(8)] + ['medic' for _ in range(2)] + ['psychologist' for _ in range(1)] + ['accountant' for _ in range(2)] + ['coach' for _ in range(3)]
    positions_list = positions_1 + positions_2 + positions_3 + positions_4 + positions_5
    facility_list = [1 for _ in range(len(positions_1))] + [2 for _ in range(len(positions_2))] + [3 for _ in range(len(positions_3))] + [4 for _ in range(len(positions_4))] + [5 for _ in range(len(positions_5))]
    gen_employees(True, today, establishment, len(positions_list), positions_list, facility_list, '../data/backup/active_employees_v1.csv')
    '''
   
    # for retired employees
    '''
    positions = ['cleaner', 'director', 'manager', 'medic', 'psychologist', 'accountant', 'coach']
    positions_list = random.choices(positions, weights=[10, 1, 10, 3, 2, 2, 6], k=44)
    facilities = [1, 2, 3, 4, 5]
    facility_list = random.choices(facilities, k=44)
    gen_employees(False, today, establishment, len(positions_list), positions_list, facility_list, '../data/backup/retired_employees_v1.csv')
    '''

    # to conect everything
    '''
    active = pd.read_csv('../data/backup/active_employees_v1.csv')
    retired = pd.read_csv('../data/backup/retired_employees_v1.csv')
    full_employees = pd.concat([active, retired])
    full_employees = full_employees[['birthdate', 'age', 'join_date', 'retire_date', 'position', 'facility_id']]
    full_employees = full_employees.sort_values(by=['facility_id', 'position']).reset_index(drop=True)
    full_employees.to_csv('../data/backup/full_employees_v1.csv', index=False)
    '''