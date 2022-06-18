import pandas as pd

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
    fees_filename = "../data/backup/fees.csv"
    salaries_filename = "../data/backup/salaries.csv"
    filename = "../data/finances.csv"
    combine_salaries_with_fees(salaries_filename, fees_filename, filename)