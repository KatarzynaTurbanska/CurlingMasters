import numpy as np
import pandas as pd

def phone_number(area):
    '''
    function generating canadian phone number depending on area

    takes
    -----
    area - area from which we generate phone number

    returns
    -------
    string with canadian phone number

    '''

    area_codes = {"Calgary": [403, 587, 825], "Vancouver": [236, 604, 672, 778], "Toronto": [416, 437, 647], "Ottawa": [343, 613], "Montreal": [438, 514]}
    number_part2 = np.arange(0, 1000)
    number_part3 = np.arange(0, 10000)

    p1 = str(np.random.choice(area_codes[area]))
    p2 = str(np.random.choice(number_part2)).zfill(3)
    p3 = str(np.random.choice(number_part3)).zfill(4)
    return "({}) {}-{}".format(p1,p2,p3)

def gen_ph_nums(area, n=1):
    '''
    function generating unique canadian phone numbers for people from one area

    takes
    -----
    area - area from people are
    n - amount of people from area, default=1

    returns
    -------
    list with unique canadian phone numbers

    '''
    numbers_list = []

    while len(numbers_list) < n:
        ph = phone_number(area)
        if ph not in numbers_list:
            numbers_list.append(ph)

    return numbers_list

def save_phone_numbers(people_filename, filename):
    '''
    function generating phone numbers for all people

    takes
    -----
    people_filename - name of file with people
    filename - name of file we want to save generated data in

    returns
    -------
    csv file with phone numbers

    '''

    fac = {1:'Toronto', 2:'Montreal', 3:'Calgary', 4:'Ottawa', 5:'Vancouver'}
    people = pd.read_csv(people_filename)
    amounts = dict(people["facility_id"].value_counts().sort_index())

    ph_nums = [gen_ph_nums(fac[i], amounts[i]) for i in range(1,len(amounts)+1)]

    ph_nums_by_id = [ph_nums[int(people["facility_id"][i] - 1)].pop() for i in range(len(people))]

    df = pd.DataFrame(ph_nums_by_id, columns=["phone"])
    df.index.name = "person_id"
    df.to_csv(filename)


if __name__ == "__main__":
    people_filename = "../data/full_people.csv"
    filename = "../data/phone_book.csv"
    save_phone_numbers(people_filename, filename)