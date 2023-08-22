import sqlite3

"""
get Chinook.db from :https://github.com/openai/openai-cookbook/tree/main/examples/data
Schema : https://www.sqlitetutorial.net/sqlite-sample-database/
"""
connection = sqlite3.connect("Chinook.db")


def get_table_names():
    """return a list of table names in database"""
    table_names = []
    tables = connection.execute("select name from sqlite_master where type='table';")

    for table in tables.fetchall():
        # table is tuple
        # print("table object type is  is : ", type(table))
        table_names.append(table[0])
    return table_names


def get_column_names(table_name):
    """return list of table names"""
    column_names = []
    columns = connection.execute(f"PRAGMA table_info('{table_name}');").fetchall()

    for col in columns:
        # print("col type is : ", type(col)) # tuple of 4 values
        # print("col object is : ", col)
        column_names.append(col[1])

    return column_names


# print(get_column_names("Artist"))
def get_database_info():
    """
    return a list of dicts/maps containing the table name and columns for
    each table in database
    """
    table_dicts = []
    for table in get_table_names():
        column_names = get_column_names(table)
        table_dicts.append({"table_name": table, "column_names": column_names})

    return table_dicts
