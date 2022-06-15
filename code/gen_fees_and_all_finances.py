import pandas as pd
from dateutil.relativedelta import relativedelta

def player_fees(id, join_date, retire_date, fee):
    '''
    function generating player's fees

    takes
    -----
    id - player id
    join_date - join date of a player
    retire_date - retire date of a player; if player is active, retire_date is 2022-05-30
    fee - size of fee

    returns
    -------
    dataframe with player's fees

    '''

    fee_dates_list = [join_date]
    i = 1

    while True:
        fee_date = join_date + relativedelta(months=i)
        if fee_date < retire_date:
            fee_dates_list.append(fee_date)
            i += 1
        else:
            break
    
    return pd.DataFrame(list(zip([id]*len(fee_dates_list), fee_dates_list, [fee]*len(fee_dates_list))), columns=["person_id", "date", "financial_flow"])

def gen_fees(people_filename, fees_filename):
    '''
    function generating players' fees

    takes
    -----
    people_filename - name of file with people
    fees_filename - name of file we want to save generated data in

    returns
    -------
    csv file with players' fees

    '''

    fees = {"junior":240/12, "adult":660/12}

    people = pd.read_csv(people_filename)
    is_player = people["position"].isnull()
    people["retire_date"].fillna(pd.Timestamp(2022, 5, 30), inplace=True)

    players_fees = pd.DataFrame()

    for i in range(len(people)):
        if is_player[i]:
            players_fees = pd.concat([players_fees, player_fees(i, pd.Timestamp(people["join_date"][i]), pd.Timestamp(people["retire_date"][i]), fees[people["category"][i]])])

    players_fees = players_fees.sort_values(["date", "person_id"])
    players_fees.to_csv(fees_filename, index=False)

def combine_salaries_with_fees(salaries_filename, fees_filename, filename):
    '''
    function combining csv with salaries and fees

    takes
    -----
    salaries_filename - name of file with salaries
    fees_filename - name of file with fees
    filename - name of file we want to save data in

    returns
    -------
    csv file with all financial flows

    '''

    salaries = pd.read_csv(salaries_filename)
    fees = pd.read_csv(fees_filename)

    financial_flows = pd.concat([salaries, fees])
    financial_flows = financial_flows.sort_values(["date", "person_id"])
    financial_flows.to_csv(filename, index=False)


if __name__ == "__main__":
    people_filename = "../data/full_people.csv"
    fees_filename = "../data/backup/fees.csv"
    salaries_filename = "../data/backup/salaries.csv"
    gen_fees(people_filename, fees_filename)
    filename = "../data/finances.csv"
    combine_salaries_with_fees(salaries_filename, fees_filename, filename)