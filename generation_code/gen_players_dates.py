import numpy as np
import pandas as pd
import random, math

def gen_birthdays(today, n_jun, n_adu, file_name):
    '''
    function appending birthdays to base file with id,
    appends birthdates for n_jun juniors and n_adu adults 
    according to our previously generated teams

    takes
    -----
    today - date of database creation
    n_jun - number of juniors birthdays to generate
    n_adu - number of adults birthdays to generate
    file_name - name of file we want to save generated data in

    returns
    -------
    csv file with birthdays, age and category

    '''
    dates = pd.DataFrame(columns=['birthdate'], index=range(n_adu+n_jun))

    dates_junior = pd.date_range('2001-05-30','2015-05-30',freq='D') # range dates for juniors: 7 < birthdate < 21
    dates_adult = pd.date_range('1972-05-30','2000-05-30',freq='D') # range dates for adults: 22 < birthdate < 50

    birthdates = random.choices(dates_junior, k=n_jun) + random.choices(dates_adult, k=n_adu) # 149 juniors & 118 seniors

    for index, row in dates.iterrows():
        dates.loc[index, 'birthdate'] = birthdates[index]
        age = math.floor((today - birthdates[index])/np.timedelta64(1, 'Y'))
        dates.loc[index, 'age'] = age # also supplementary already calculated age
        if age > 21:
            dates.loc[index, 'category'] = 'adult' # assigning categories
        else:
            dates.loc[index, 'category'] = 'junior'

    dates['birthdate'] = dates['birthdate'].dt.strftime('%Y-%m-%d')
    dates['age'] = dates['age'].astype(int)
    dates.to_csv(file_name, index=False)

def assign_facility(dates, file_name, index_junior, index_adult):
    '''
    function assigning facility numbers to players according
    to previosly generated teams (so how many juniors and aduts are 
    in which facility)

    takes
    -----
    dates - csv file with id, birthdate, age and category
    file_name - name of file we want to save generated data in
    index_junior/index_adult - lists of facility numbers we want each players in

    returns
    -------
    dates csv file with new column facility_id

    '''
    dates = pd.read_csv(dates)

    for index, row in dates.iterrows():
        if index < len(index_junior):
            dates.loc[index, 'facility_id'] = index_junior[index]
        else:
            dates.loc[index, 'facility_id'] = index_adult[index-len(index_junior)]

    dates.to_csv(file_name, index=False)


def gen_join_retire_dates(active, today, establishment, dates, file_name):
    '''
    function generating dates for players when
    they joined the club and left it or if player is active 
    it appends nan as retire date

    takes
    -----
    active[bool] - are we generating active or retired players
    today - date of database creation
    establishment - date of club establishment
    dates - csv base file with players
    file_name - name of file we want to save generated data in

    returns
    -------
    csv file with join_dates and retire_dates

    '''
    dates = pd.read_csv(dates)
    dates['join_date'] = np.nan
    dates['retire_date'] = np.nan
    join_dates = pd.date_range(establishment, today, freq='D')

    for index, row in dates.iterrows():
        if pd.to_datetime(row['birthdate']) + np.timedelta64(7, 'Y') < establishment:
            join = random.choice(join_dates)
            dates.loc[index, 'join_date'] = join
        else: 
            join_dates_2 = pd.date_range(pd.to_datetime(row['birthdate']) + np.timedelta64(7, 'Y'), today, freq='D')
            join = random.choice(join_dates_2)
            dates.loc[index, 'join_date'] = join
    
        if not active:
            retire_dates = pd.date_range(pd.to_datetime(join) + np.timedelta64(1, 'D'), today, freq='D')
            dates.loc[index, 'retire_date'] = random.choice(retire_dates)

    dates['join_date'] = dates['join_date'].dt.strftime('%Y-%m-%d')
    if not active:
        dates['retire_date'] = dates['retire_date'].dt.strftime('%Y-%m-%d')
    dates.to_csv(file_name, index=False)

if __name__ == "__main__" :
    today = pd.to_datetime('2022-05-30')
    establishment = pd.to_datetime('2019-06-01') 

    # for active players
    '''
    gen_birthdays(today, 149, 118, '../data/backup/active_players_v1.csv')
    index_junior = [1 for _ in range(20)] + [2 for _ in range(42)] + [3 for _ in range(17)] + [4 for _ in range(33)] + [5 for _ in range(37)] 
    index_adult = [1 for _ in range(26)] + [2 for _ in range(23)] + [3 for _ in range(36)] + [4 for _ in range(18)] + [5 for _ in range(15)] 
    assign_facility('../data/backup/active_players_v1.csv', '../data/backup/active_players_v1.csv', index_junior, index_adult)
    gen_join_retire_dates(True, today, establishment, '../data/backup/active_players_v1.csv', '../data/backup/active_players_v2.csv')
    '''
    
    # for retired players
    '''
    gen_birthdays(today, 42, 61, '../data/backup/retired_players_v1.csv')
    index_junior = random.choices([1,2,3,4,5], k=42)
    index_adult = random.choices([1,2,3,4,5], k=61)
    index_junior.sort()
    index_adult.sort()
    assign_facility('../data/backup/retired_players_v1.csv','../data/backup/retired_players_v1.csv', index_junior, index_adult) 
    gen_join_retire_dates(False, today, establishment,'../data/backup/retired_players_v1.csv','../data/backup/retired_players_v2.csv')
    '''