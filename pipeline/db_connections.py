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

    def get_last_id(self):
        ids = [document['id'] for document in self.collection.find({}, {'id': 1, '_id': 0}).sort([('id', -1)]).limit(1)]
        if not ids:
            return 1
        return ids[0] + 1

    def get_present_symbols(self):
        symbols = set([document['symbol'] for document in self.collection.find({}, {'symbol': 1, '_id': 0})])
        return symbols


if __name__ == "__main__":

    class Cursor(StockMarketDBConnector):
        COLLECTION = 'api_financialsdata'

    cursor = Cursor()
    response = cursor.collection.aggregate(
        [
            {
                "$group":
                    {
                        "_id": "$sector",
                        "industries_count": {
                            "$sum": {

                            }
                        }
                    }
            }
        ]
    )

    for item in response:
        print(item)
