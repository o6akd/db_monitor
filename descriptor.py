
'''
TODO:
Compare the descripitive parameters
Store in a file
'''
import pandas as pd
import json
import connector
from re import search
from datetime import datetime

def get_table_names(cursor):
    result = cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
    table_names = sorted(list(zip(*result))[0])
    return table_names #return table names 

def get_col_names(table_names,cur):
    newline_indent = '\n   '
    for table_name in table_names:
        result = cur.execute("PRAGMA table_info('%s')" ,(table_name,)).fetchall()
        column_names = list(zip(*result))[1]
        print (("\ncolumn names for %s:" % table_name)
            +newline_indent
            +(newline_indent.join(column_names)))
    return None

import numpy
def describe_tables(table_names, db):
    snap_current = {}
    for table in table_names:
        current_table = pd.read_sql_query("SELECT * FROM %s;" % table, db) #pandas acts weird trying to pass parameters this should be fixed
        current_table = current_table.astype(float)
        current_table= current_table.loc[:,~current_table.columns.str.contains('id')]     
        snap_current[table] = (current_table.describe()).to_dict() #describe the whole table and convert to json object
    return snap_current #a dictionary

def configure():
    config = {}
    try:
        with open("config.json") as json_file: # open configuration file
            config = json.load(json_file) #configuration information for the db connection
    except:
        print("Configuration (config.json) file is not found! ")
    return config

def main():
    config = configure() #configuration information stored as json
    db_name = config['source'] #get database name from the config file
    db =  connector.create_connection(r"%s"%db_name) # returns sqlite3.connect(db_file)
    cur = db.cursor()
    table_names = get_table_names(cur) #get table names
    #### get descriptions
    snap_current = describe_tables(table_names, db) # current snapshot of the database stored as a table_name: description key/value pair 
    #time stamp snap_current
    # datetime object containing current date and time
    now = datetime.now()
    # dd/mm/YY H:M:S
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    snap_current['time'] = dt_string
    with open('./snapshots/snap.json', 'a+') as outfile: #save the current snapshot to a json file 
        json.dump(snap_current, outfile, indent=2)
    db.close() #close the database 

if __name__ == "__main__":
    main()
    with open("snapshots/snap.json") as json_file:
        snap_pre = json.load(json_file) # previous snapshot