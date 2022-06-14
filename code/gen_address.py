import numpy as np
import pandas as pd
from faker import Faker

def download_streets():

    '''function to download and prepare data'''
    
    global streets_toronto, streets_ottawa, streets_vancouer, streets_calgary, streets_montreal
   
    streets_toronto = pd.read_csv('../data/backup/streets/streets_toronto.csv',names=['street'],encoding='latin')
    streets_ottawa = pd.read_csv('../data/backup/streets/streets_ottawa.csv',names=['street'],encoding='latin')
    streets_vancouer = pd.read_csv('../data/backup/streets/streets_vancouver.csv',names=['street'],encoding='latin')
    streets_calgary = pd.read_csv('../data/backup/streets/streets_calgary.csv',names=['street'],encoding='latin')
    streets_montreal = pd.read_csv('../data/backup/streets/streets_montreal.csv',names=['street'],encoding='latin')

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

    streets = {'toronto':streets_toronto,'ottawa':streets_ottawa,'vancouver':streets_vancouer,
    'calgary':streets_calgary,'montreal':streets_montreal}

    return np.random.choice(streets[city])

def gen_address_to_file(file_name,file_name2,n):

    '''
    function generating addresses based on 
    real names and faker package

    takes
    -----
    file_name - name of the file to which the addresses of players will be written
    file_name2 - name of the file to which the addresses of facilities will be written
    n - how many addresses to generate foreach city (given in dictionary)
        e.g. {'tornto':5,'ottawa':6,'vancouver':2,'calgary':10,'montreal':1,'random':20}

    returns
    -------
    csv file with city name, street name and building number
    '''
    
    # Toronto: 1, Montreal: 2, Calgary:3, Ottawa:4, Vancouver: 5
    cities = ['toronto','ottawa','vancouver','calgary','montreal']

    with open(file_name,'w',encoding='utf-8') as file:
        file.write('city,street,street_number\n')
        for c in cities:
            for i in range(n[c]):
                address = '{},{},{}\n'.format(c.capitalize(),random_street(c),np.random.randint(100,10000))
                file.write(address)

    with open(file_name2,'w',encoding='utf-8') as file2:
        file2.write('city','street','street_number\n')

        for c in cities:
            address = '{},{},{}\n'.format(c.capitalize(),random_street(c),np.random.randint(100,10000))
            file2.write(address)

        for _ in range(n['random']):
            fake = Faker(['en-CA'])
            address = '{},{},{}\n'.format(fake.city(),fake.street_name(),fake.building_number())
            file2.write(address)


if __name__ == '__main__':
    Faker.seed(0)
    download_streets()
    numbers = {'toronto':99,'ottawa':104,'vancouver':106,'calgary':113,'montreal':125,'random':99}
    gen_address_to_file('../data/addreses.csv','facilities.csv',numbers)