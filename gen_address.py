import numpy as np
import pandas as pd
from faker import Faker

def download_streets():

    '''function to download and prepare data'''
    
    global streets_toronto, streets_ottawa, streets_vancouer, streets_calgary, streets_montreal
   
    streets_toronto = pd.read_csv('streets/streets_toronto.csv',names=['street'],encoding='latin')
    streets_ottawa = pd.read_csv('streets/streets_ottawa.csv',names=['street'],encoding='latin')
    streets_vancouer = pd.read_csv('streets/streets_vancouver.csv',names=['street'],encoding='latin')
    streets_calgary = pd.read_csv('streets/streets_calgary.csv',names=['street'],encoding='latin')
    streets_montreal = pd.read_csv('streets/streets_montreal.csv',names=['street'],encoding='latin')

    streets_toronto = np.array(streets_toronto).transpose()[0]
    streets_ottawa = np.array(streets_ottawa).transpose()[0]
    streets_vancouer = np.array(streets_vancouer).transpose()[0]
    streets_calgary = np.array(streets_calgary).transpose()[0]
    streets_montreal = np.array(streets_montreal).transpose()[0]

    
def random_street(city):
    '''
    function to generate random street in Toronto, Ottawa, 
    Vancouver, Calgary or Montreal

    takes
    -----
    city - city name
    
    returns
    --------
    street name
    '''

    streets = {'tornto':streets_toronto,'ottawa':streets_ottawa,'vancouver':streets_vancouer,
    'calgary':streets_calgary,'montreal':streets_montreal}

    return np.random.choice(streets[city])

def gen_address_to_file(file_name,n):

    '''
    function generating addresses based on 
    real names and faker package

    takes
    -----
    file_name - name of the file to which the address will be written
    n - how many addresses to generate foreach city (given in dictionary)
        e.g. {'tornto':5,'ottawa':6,'vancouver':2,'calgary':10,'montreal':1,'random':20}

    returns
    -------
    csv file with city name, street name and building number
    '''

    cities = ['tornto','ottawa','vancouver','calgary','montreal','random']

    with open(file_name,'w',encoding='utf-8') as file:
        for c in cities:
            for i in range(n[c]):
                if c == 'random':
                    fake = Faker(['en-CA'])
                    address = '{},{},{}\n'.format(fake.city(),fake.street_name(),fake.building_number())
                    file.write(address)
                else:
                    address = '{},{},{}\n'.format(c.capitalize(),random_street(c),np.random.randint(100,10000))
                    file.write(address)

if __name__ == '__main__':
    Faker.seed(0)
    download_streets()
    numbers = {'tornto':66,'ottawa':67,'vancouver':72,'calgary':78,'montreal':87,'random':20}
    gen_address_to_file('addreses.csv',numbers)