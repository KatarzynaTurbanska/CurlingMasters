from tkinter.font import names
import numpy as np
import pandas as pd

def download_names():

    global names_female, names_male, last_names
   
    names_female = pd.read_csv('names_female.csv')
    names_male = pd.read_csv('names_male.csv')
    last_names = pd.read_csv('last_names.csv',names=['last names'],encoding='latin')

    names_female = np.array(names_female['Name'])
    names_male = np.array(names_male['Name'])
    last_names = [last_names['last names'][i].split(' ') for i in range(len(last_names))]
    last_names = [last_names[i][1] for i in range(len(last_names))]
    last_names = np.array(last_names)

def gen_name_to_file(file_name1, file_name2, n):

    genders = list(n.keys())
    genders = sorted(genders)
    names = {genders[0]:names_female,genders[1]:names_female,'last name':last_names}

    with open(file_name1,'w') as file1:
        with open(file_name2,'w') as file2:
            for g in genders:
                for i in range(n[g]):
                    first = np.random.choice(names[g])

                    firs_last = '{},{}\n'.format(first,np.random.choice(names['last name']))
                    gender_first = '{},{}\n'.format(g,first)

                    file1.write(firs_last)
                    file2.write(gender_first)

if __name__ == '__main__':
    download_names()
    numbers = {'M':20,'F':20}
    gen_name_to_file('test1.csv','test2.csv',numbers)