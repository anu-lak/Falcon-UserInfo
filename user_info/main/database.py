from pymongo import MongoClient

client = MongoClient('mongodb://user:pwd@localhost:27017/')
db = client['UserInfo']

#UserInfo?authSource=admin