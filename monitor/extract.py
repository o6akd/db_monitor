
import json
import pandas as pd

def unwrap(table, timestamps, table_name):
    features = list(table[0].keys()) #get the feature names from the first entry of the table
    for feature in features:
        feature_list = list(map(lambda record: pd.Series(record[feature]), table))
        time_series = pd.DataFrame(feature_list)
        time_series.index = timestamps
        time_series.to_csv("./time_series/{}_{}.csv".format(table_name,feature))

def main():
    snapshots =  pd.read_json('./snapshots/snap.json')
    timestamps =  snapshots.loc[:, 'timestamp']
    for table in snapshots.loc[:, snapshots.columns != "timestamp"]: # calculate deltas for each table
        unwrap(snapshots.loc[:, table] , timestamps, table)            

if __name__ == "__main__":
    main()

'''
timeseries for table features
table:
date | feature | stats 
'''