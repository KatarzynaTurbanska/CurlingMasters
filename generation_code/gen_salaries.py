import calendar
import numpy as np
import pandas as pd
from dateutil.relativedelta import relativedelta

def reference_salary(position, avg_monthly_salaries, avg_daily_salaries, minimum_wage):
    '''
    function generating reference salary depending on job in 2022

    takes
    -----
    position - position of an employee
    avg_monthly_salaries - average monthly salaries in 2022 for position
    avg_daily_salaries - average daily salaries in 2022 for position
    minimum_wage - minimum wage in Canada in 2022

    returns
    -------
    reference salary depending on position in 2022, greater that minimum wage

    '''

    return round(max(np.random.normal(avg_monthly_salaries[position], avg_daily_salaries[position]/2), minimum_wage), 2)

def gen_reference_salaries(filename):
    '''
    function generating reference salaries depending on year and job

    takes
    -----
    filename - name of file we want to save generated data in

    returns
    -------
    csv file with salaries depending on year and job

    '''

    avg_monthly_salaries = {'cleaner':2437.5, 'director':6513, 'manager':3711.5, 'medic':6087.25, 'psychologist':5443.75, 'accountant':4676.75, 'coach':4062.5}
    avg_daily_salaries = {'cleaner':120, 'director':320.64, 'manager':182.75, 'medic':299.68, 'psychologist':268, 'accountant':230.24, 'coach':200}
    positions_list = list(avg_daily_salaries)
    minimum_wage = 1600

    # Dla każdej grupy zawodowej losujemy stałą stawkę na dany rok.
    salaries_2022 = [reference_salary(job, avg_monthly_salaries, avg_daily_salaries, minimum_wage) for job in positions_list]

    cleaners_rises = [0]
    for i in range(3):
        cleaners_rises.append(round(1/11 * (salaries_2022[0] - cleaners_rises[i]), 2))
    cleaners_rises.reverse()

    salaries_rises = [cleaners_rises]
    
    for _ in range(len(positions_list[1:])):
        job_rises = [0]
        for i in range(3):
            job_rises.append(np.random.normal(cleaners_rises[2-i], 50))
        job_rises.reverse()
        salaries_rises.append(job_rises)

    salaries_2021 = [round(salaries_2022[i] - salaries_rises[i][2], 2) for i in range(len(positions_list))]
    salaries_2020 = [round(salaries_2021[i] - salaries_rises[i][1], 2) for i in range(len(positions_list))]
    salaries_2019 = [round(salaries_2020[i] - salaries_rises[i][0], 2) for i in range(len(positions_list))]

    df = pd.DataFrame(list(zip(salaries_2019,salaries_2020,salaries_2021,salaries_2022)), columns=[2019,2020,2021,2022])
    df.index = positions_list

    df.to_csv(filename)

def salaries_dates(join_date, retire_date):
    '''
    function generating dates of salaries of an employee

    takes
    -----
    join_date - join date of an employee

    returns
    -------
    dates of salaries of an employee

    '''

    if retire_date == "":
        # Dla aktulanych pracowników zakładamy, że teraz to 30 maja 2022.
        today = pd.Timestamp(2022, 5, 30)
    else:
        today = retire_date

    dates = [join_date]
    year, month = join_date.year, join_date.month

    while dates[-1] < today:
        d = calendar.monthrange(year, month)[1]
        weekday = pd.Timestamp(year,month,d).weekday()
        if weekday < 5:
            dates.append(pd.Timestamp(year,month,d))
        else:
            dates.append(pd.Timestamp(year,month,d-(weekday-4)))

        if month < 12:
            month += 1
        else:
            year += 1
            month = 1

    if (retire_date == "") or (retire_date >= pd.Timestamp(2022, 5, 1)):
        return dates[1:-1]
    return dates[1:]

def working_days(start, end):
    '''
    function counting working days between two dates

    takes
    -----
    start - beginning of period
    end - end of period

    returns
    -------
    amount of working days between two dates

    '''

    return np.busday_count(start.date(), end.date())

def finance_history(join_date, position, retire_date, salaries_filename):
    '''
    function generating finance history for an employee

    takes
    -----
    join_date - join date of an employee
    position - position of an employee
    salaries_filename - name of file with reference salaries
    filename - name of file we want to save generated data in

    returns
    -------
    dataframe with finance history for an employee

    '''

    reference_salaries_df = pd.read_csv(salaries_filename, index_col=0)
    person_salaries = []

    if retire_date != "":
        if (join_date.month, join_date.year) == (retire_date.month, retire_date.year):
            last_day = salaries_dates(join_date, retire_date+relativedelta(months=1))[0]
            workdays = working_days(pd.Timestamp(join_date.year, join_date.month, 1), last_day) + 1
            person_salaries.append(round(reference_salaries_df[str(join_date.year)][position] * (working_days(join_date, retire_date) + 1)/workdays))
            df = pd.DataFrame(list(zip([last_day], person_salaries)), columns=["date", "financial_flow"])
            return df

    dates = salaries_dates(join_date, retire_date)

    days_from_join = working_days(join_date, dates[0]) + 1
    workdays = working_days(pd.Timestamp(dates[0].year, dates[0].month, 1), dates[0]) + 1

    person_salaries.append(round(reference_salaries_df[str(join_date.year)][position] * days_from_join/workdays, 2))

    if retire_date == "":
        n = len(dates)
    else:
        n = len(dates)-1

    for i in range(1, n):
        workdays = working_days(dates[i-1], dates[i])

        U = np.random.random()

        if U < 0.7:
            salary_for_date = reference_salaries_df[str(dates[i].year)][position]
        else:
            days = np.random.choice([-7,-6,-5,-4,-3,-2,-1,1,2,3,4])
            salary_for_date = round(reference_salaries_df[str(dates[i].year)][position] * (workdays + days)/workdays, 2)

        if dates[i].month == 12:
            salary_for_date += 250

        person_salaries.append(salary_for_date)

    if retire_date != "" and (retire_date < pd.Timestamp(2022, 5, 1)):
        days_to_retire = working_days(dates[-2], retire_date)
        workdays = working_days(dates[-2], dates[-1])
        person_salaries.append(round(reference_salaries_df[str(retire_date.year)][position] * days_to_retire/workdays, 2))

    df = pd.DataFrame(list(zip(dates, person_salaries)), columns=["date", "financial_flow"])
    return df

def gen_finances(people_filename, salaries_filename, filename):
    '''
    function generating finance history for an employee

    takes
    -----
    people_filename - name of file with people
    salaries_filename - name of file with reference salaries
    filename - name of file we want to save generated data in

    returns
    -------
    csv file with finance history for an employee

    '''

    people = pd.read_csv(people_filename, index_col=0)
    is_present_employees_list = people["retire_date"].isnull()
    is_employees_list = people["position"].notnull()

    finances = pd.DataFrame()

    for i in range(len(people)):
        is_present_employee = is_present_employees_list[i]
        if (is_employees_list[i]) and (pd.Timestamp(people["join_date"][i]) < pd.Timestamp(2022, 5, 1)):
            if is_present_employee:
                emp_fin = finance_history(pd.Timestamp(people["join_date"][i]), people["position"][i], "", salaries_filename)
            else:
                emp_fin = finance_history(pd.Timestamp(people["join_date"][i]), people["position"][i], pd.Timestamp(people["retire_date"][i]), salaries_filename)

            ids = pd.DataFrame([i]*len(emp_fin), columns=["person_id"])
            ids_fin = pd.concat([ids, emp_fin], axis=1)
            finances = pd.concat([finances, ids_fin])

    finances = finances.reset_index(drop=True)
    finances["financial_flow"] *= -1
    finances = finances.sort_values(["date", "person_id"])
    finances.to_csv(filename, index=False, float_format='%.2f')

if __name__ == "__main__":
    salaries_filename = "../data/backup/reference_salaries.csv"
    #gen_reference_salaries(salaries_filename)
    people_filename = "../data/full_people.csv"
    filename = "../data/backup/salaries.csv"
    gen_finances(people_filename, salaries_filename, filename)
