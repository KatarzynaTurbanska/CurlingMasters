from tkinter.font import names
import numpy as np
import pandas as pd

def download_names():

    '''
    function to download and prepare data

    '''

    global names_female_2, names_male_2, last_names
   
   # downloading data
    names_female = pd.read_csv('names_female.csv',encoding='latin')
    names_male = pd.read_csv('names_male.csv',encoding='latin')
    last_names = pd.read_csv('last_names.csv',names=['last names'],encoding='latin')

    # first names - preparing data
    names_female = names_female[['Name']]
    names_male = names_male[['Name']]

    # removing unnecessary spaces
    names_female['Name'] = names_female['Name'].str.strip()
    names_male['Name'] = names_male['Name'].str.strip()
    names_male['Name'] = names_male['Name'].astype(str)

    # removing duplicates
    names_male = names_male.drop_duplicates()
    names_female = names_female.drop_duplicates()

    df = names_female.append(names_male)

    names_female_ar = np.array(names_female)[:,0]
    names_male_ar = np.array(names_male)[:,0]
    duplicated_ar = np.array(df[df.duplicated()])[:,0]

    names_female_2 = np.setdiff1d(names_female_ar,duplicated_ar)
    names_male_2 = np.setdiff1d(names_male_ar,duplicated_ar)

    # last names - preparing data
    last_names = [last_names['last names'][i].split(' ') for i in range(len(last_names))]
    last_names = [last_names[i][1] for i in range(len(last_names))]
    last_names = np.array(last_names)

def gen_name_to_file(file_name1, file_name2, n):
    '''
    function generating first names and last names based on 
    real names from files 'names_female.csv', 'names_male.csv'
    and 'last_names.csv' and saving them to new files

    takes
    -----
    file_name1 - name of the file to which the first names 
                 and the last names will be written
    file_name2 - name of the file to which the first names 
                 and genders will be written
    n - how many names to generate for male and female (given in dictionary)
        e.g. {'Male':30,'Female':20}

    returns
    -------
    two csv files with first names, last names and genders
    '''

    genders = list(n.keys())
    genders = sorted(genders)
    names = {genders[0]:names_female_2,genders[1]:names_female_2,'last name':last_names}

    with open(file_name1,'w',encoding='utf-8') as file1:
        with open(file_name2,'w',encoding='utf-8') as file2:
            for g in genders:
                for i in range(n[g]):
                    first = np.random.choice(names[g])

                    firs_last = '{},{}\n'.format(first,np.random.choice(names['last name']))
                    gender_first = '{},{}\n'.format(g,first)

                    file1.write(firs_last)
                    file2.write(gender_first)

if __name__ == '__main__':
    download_names()
    numbers = {'M':209,'F':161}
    gen_name_to_file('people.csv','gender.csv',numbers)