import numpy as np
import pandas as pd

def download_streets():

    global streets_toronto, streets_ottawa, streets_vancouer, streets_calgary, streets_montreal
   
    streets_toronto = pd.read_csv('streets/streets_toronto.csv',names=['street'])
    streets_ottawa = pd.read_csv('streets/streets_ottawa.csv',names=['street'])
    streets_vancouer = pd.read_csv('streets/streets_vancouver.csv',names=['street'])
    streets_calgary = pd.read_csv('streets/streets_calgary.csv',names=['street'])
    streets_montreal = pd.read_csv('streets/streets_montreal.csv',names=['street'],encoding='latin')

    streets_toronto = np.array(streets_toronto).transpose()[0]
    streets_ottawa = np.array(streets_ottawa).transpose()[0]
    streets_vancouer = np.array(streets_vancouer).transpose()[0]
    streets_calgary = np.array(streets_calgary).transpose()[0]
    streets_montreal = np.array(streets_montreal).transpose()[0]

    
def random_street(city):
    streets = {'tornto':streets_toronto,'ottawa':streets_ottawa,'vancouver':streets_vancouer,
    'calgary':streets_calgary,'montreal':streets_montreal}

    return np.random.choice(streets[city])

def gen_address_to_file(file_name,n):

    cities = ['tornto','ottawa','vancouver','calgary','montreal']

    with open(file_name,'w') as file:
        for c in cities:
            for i in range(n[c]):
                address = '{},{},{}\n'.format(c.capitalize(),random_street(c),np.random.randint(100,10000))
                file.write(address)

if __name__ == '__main__':
    download_streets()
    numbers = {'tornto':5,'ottawa':6,'vancouver':2,'calgary':10,'montreal':1}
    gen_address_to_file('test.csv',numbers)