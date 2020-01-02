import pymongo
from cryptography.fernet import Fernet
import sqlite3
from sqlite3 import Error
 
'''
TODO:
 Implement connection to db
 Receive the dataset 

'''
def mongo_connect():
    cred = open("credentials").readlines()
    key = bytes("{}".format(cred[1].strip("\n")),'utf-8')
    decrypt = bytes("{}".format(cred[0].strip("\n")),'utf-8')
    cipher_suite = Fernet(key)
    password = (cipher_suite.decrypt(decrypt)).decode("utf-8") 

    client = pymongo.MongoClient("mongodb+srv://akd:{}@cluster0-5o3i2.mongodb.net/test?retryWrites=true&w=majority".format(password))
    db = client.test
    return db

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print("connected ")
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        conn.text_factory = str
        return conn
        
 
    