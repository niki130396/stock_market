from pymongo import MongoClient


class StockMarketDBConnector:
    COLLECTION = None

    def __init__(self):
        self.client = MongoClient('mongodb://127.0.0.1:27017')
        self.db = self.client.stock_market
        if getattr(self, 'COLLECTION'):
            self.collection = eval(f'self.db.{self.COLLECTION}')
        else:
            raise AttributeError('Please provide a collection to work with')
