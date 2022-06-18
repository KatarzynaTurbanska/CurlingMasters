import pandas as pd
import numpy as np

def gen_fac_equipment(people_filename, filename):
    '''
    function generating equipment in facility

    takes
    -----
    people_filename - name of file with people
    filename - name of file we want to save generated data in

    returns
    -------
    csv file with equipment in facility

    '''

    people = pd.read_csv(people_filename)

    teams_in_fac = dict(people.groupby(["facility_id"]).nunique()["team_name"])
    players_in_fac = dict(people[people["retire_date"].isnull() & people["position"].isnull()].groupby(["facility_id"]).count().iloc[:,0])

    brooms = [np.random.choice(np.arange(4*teams_in_fac[i], 8*teams_in_fac[i])) for i in range(1, 6)]
    stones = [np.random.choice(np.arange(8*teams_in_fac[i], 16*teams_in_fac[i])) for i in range(1, 6)]
    shoes = [np.random.choice(np.arange(players_in_fac[i], 2*players_in_fac[i])) for i in range(1, 6)]

    equip = list(zip(list(teams_in_fac), np.arange(5), brooms, stones, shoes))
    fac = pd.DataFrame(equip, columns=["facility_id", "address_id", "brooms", "stones", "shoes"])

    fac.to_csv(filename, index=False)


if __name__ == "__main__":
    people_filename = "../data/full_people.csv"
    filename = "../data/facility.csv"
    gen_fac_equipment(people_filename, filename)