
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.stock_finder
stocks = db.stocks
sectors = db.sectors


# all stocks trading within 20% of yearly low


