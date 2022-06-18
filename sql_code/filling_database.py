import mysql.connector as mysql
import pandas as pd

def fill_table(table_name, query, password):
    conn = password
    data = pd.read_csv('../final_data/{}.csv'.format(table_name))
    data = data.where(pd.notnull(data), None)

    cursor = conn.cursor()
    sql = "INSERT INTO team3.{} VALUES {}".format(table_name, query)
    val = data.itertuples(index=False)
    cursor.executemany(sql, val)
    conn.commit()
    print("Records inserted")

if __name__ == '__main__':
    fill_table('gender', '(%s,%s)')
    fill_table('people', '(%s,%s,%s)')
    fill_table('phone_book', '(%s,%s)')
    fill_table('finances', '(%s,%s,%s)')
    fill_table('address_book', '(%s,%s,%s,%s)')
    fill_table('address', '(%s,%s)')
    fill_table('facility', '(%s,%s)')
    fill_table('equipment', '(%s,%s,%s,%s)')
    fill_table('teams', '(%s,%s,%s,%s)')
    fill_table('personal_info', '(%s,%s,%s,%s,%s,%s)')
    fill_table('matches', '(%s,%s,%s,%s,%s,%s,%s)')
    fill_table('opponents', '(%s,%s,%s)')
    fill_table('positions', '(%s,%s,%s)')