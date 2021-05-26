# importing pymongo
from pymongo import MongoClient
import urllib.parse

# establing connection
try:
    connect = MongoClient('localhost:27017')
    connect.demoDB.authenticate('root', 'example')
    print("Connected successfully!!!")
except:
    print("Could not connect to MongoDB")


# connecting or switching to the database
db = connect.demoDB

# creating or switching to demoCollection
collection = db.demoCollection

# first document
document1 = {
        "name":"John",
        "age":24,
        "location":"New York"
        }
#second document
document2 = {
        "name":"Sam",
        "age":21,
        "location":"Chicago"
        }

# Inserting both document one by one
collection.insert_one(document1)
collection.insert_one(document2)



# Printing the data inserted
cursor = collection.find()
for record in cursor:
    print(record)