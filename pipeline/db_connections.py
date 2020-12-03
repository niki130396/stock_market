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
