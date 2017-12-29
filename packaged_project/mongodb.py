import pandas as pd
import pymongo
from pymongo import MongoClient

def save_to_mongodb(df, username, userpassword, dbname, collectionname):
    try:
        connection = pymongo.MongoClient(
            'mongodb://%s:%s@ec2-13-125-106-155.ap-northeast-2.compute.amazonaws.com' % (username, userpassword))
        db = connection[dbname]
        collection = db[collectionname]
        collection.insert_many(df.to_dict('records'))
        connection.close()
    except:
        raise ConnectionError("Something is wrong on local - db connection")
        
        
def mongo_find_to_df(username, userpassword, dbname, collectionname, query=None):
    connection = pymongo.MongoClient('mongodb://%s:%s@ec2-13-125-106-155.ap-northeast-2.compute.amazonaws.com' % (username, userpassword))
    db = connection[dbname]
    collection = db[collectionname]
    df = pd.DataFrame(list(collection.find(query))).drop_duplicates(['longitude', 'latitude', 'title'])
    connection.close()
    return df    