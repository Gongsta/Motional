from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv

def connect():
    db_password = os.getenv('MONGO_DB_KEY')

    client = MongoClient(db_password)
    print("Successfully Connected")
    return client


# Making a CRUD API

# Create
def write(db, data):
    if type(data) == None:
        print("No data")
        return
    # for loop to add multiple pieces of data
    # if type(data) == list:
    #     for doc in data:
    #         db.insert_one(doc)
    #         return
    db.insert_one(data)

# Read
def read(db, id):
    if not id:
        print("No email provided")
        return
    if type(db["main"].find_one({"id": id})) == str:
        return db["main"].find_one({"id": id})
    else:
        return False

# Update
def update(db, email, data, dataType):
    if email is None or data is None:
        print(f"Provide valid data\nEmail: {email} | Data: {data}")
        return
    
    db.update_one({"email": email}, {"$set":{dataType: data}})

# Delete
def delete(db, email):
    if type(email) == None:
        print("No email provided")
        return
    db.delete_one({"email": email})


# print(read(db, "ayushrgarg@gmail.com")['name']) Works!

# update(db, "ayushrgarg@gmail.com", "Ayush") Works!

# delete(db, "ayushrgarg@gmail.com") Works!

