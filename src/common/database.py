import pymongo


class Database(object):
    URI = "mongodb://127.0.0.1:27017"
    CLIENT = None
    DB = None

    @staticmethod
    def initialize():
        if Database.DB == None:
            Database.CLIENT = pymongo.MongoClient(Database.URI)
            Database.DB = Database.CLIENT['pricealerts']

    @staticmethod
    def close_connection():
        Database.CLIENT.close()
        Database.DB = None

    @staticmethod
    def remove(collection, query):
        Database.DB[collection].remove(query)

    @staticmethod
    def insert(collection, data):
        Database.DB[collection].insert(data)

    @staticmethod
    def find(collection, query):
        return Database.DB[collection].find(query)

    @staticmethod
    def find_one(collection, query):
        return Database.DB[collection].find_one(query)

    @staticmethod
    def update(collection, query, data):
        Database.DB[collection].update(query, data, upsert=True)
