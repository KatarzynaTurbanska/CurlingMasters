import numpy as np
import pandas as pd
import random

def gen_birthdays(dates, n_jun, n_adu):
    '''
    function appending birthdays to base file with id,
    appends birthdates for n_jun juniors and n_adu adults 
    according to our previously generated teams

    takes
    -----
    dates - csv base file only id column
    n_jun - number of juniors birthdays to generate
    n_adu - number of adults birthdays to generate

    returns
    -------
    csv file with birthdays

    '''
    today = pd.to_datetime('2022-05-30') # will be our 'today' date for database
    dates_junior = pd.date_range('2001-05-30','2015-05-30',freq='D') # range dates for juniors: 7 < birthdate < 21
    dates_adult = pd.date_range('1972-05-30','2000-05-30',freq='D') # range dates for adults: 22 < birthdate < 50

    birthdates = random.choices(dates_junior, k=n_jun) + random.choices(dates_adult, k=n_adu) # 149 juniors & 118 seniors

    for index, row in dates.iterrows():
        dates.loc[index, 'birthdate'] = birthdates[index]
        age = round((today - birthdates[index])/np.timedelta64(1, 'Y'))
        dates.loc[index, 'age'] = round((today - birthdates[index])/np.timedelta64(1, 'Y')) # also supplementary already calculated age
        if age > 21:
            dates.loc[index, 'category'] = 'adult' # assigning categories
        else:
            dates.loc[index, 'category'] = 'junior'

    dates['birthdate'] = dates['birthdate'].dt.strftime('%Y-%m-%d')
    dates['age'] = dates['age'].astype(int)
    dates.to_csv('dates.csv', index=False)

def assign_facility(dates):
    '''
    function assigning facility numbers to birthday according
    to previosly generated teams (so how many juniors and aduts are 
    in which facility)

    takes
    -----
    dates - csv file with id, birthdate, age and category

    returns
    -------
    dates csv file with new column facility_id

    '''
    index_junior = [1 for _ in range(20)] + [2 for _ in range(42)] + [3 for _ in range(17)] + [4 for _ in range(33)] + [5 for _ in range(37)] 
    index_adult = [1 for _ in range(26)] + [2 for _ in range(23)] + [3 for _ in range(36)] + [4 for _ in range(18)] + [5 for _ in range(15)] 

    for index, row in dates.iterrows():
        if index < len(index_junior):
            dates.loc[index, 'facility_id'] = index_junior[index]
        else:
            dates.loc[index, 'facility_id'] = index_adult[index-len(index_junior)]

    dates.to_csv('dates.csv', index=False)
         
if __name__ == "__main__" :
    dates = pd.read_csv('dates.csv')
    #gen_birthdays(dates, 149, 118)
    #assign_facility(dates)
    #gen_join_retire_dates(dates)
    