import pymongo

class MongoConfig:
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["property_Investors"]
    Usersdb = mydb["User Register"]
