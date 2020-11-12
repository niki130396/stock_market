from pipeline.mongo_pipeline import MongoConnector
from pymongo import MongoClient
from datetime import datetime


class DBSource(MongoConnector):
    def __init__(self):
        super().__init__()


class DBTarget:
    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.stock_market
        self.collection = self.db.visualisations_aggregateddata
        self.target_document = self.collection.find_one({})

    def insert_one(self, document):
        self.collection.insert_one(document)


def aggregate(document):
    average_yearly_return = 0
    for item in document['info'][-255:]:
        average_yearly_return += item['Daily_Returns']
    average_yearly_return /= 255
    return average_yearly_return


if __name__ == '__main__':
    cursor = DBSource()
    target = DBTarget()

    ready_document = {'id': cursor.collection.find_one({}, {'id': 1, '_id': 0})['id'] + 1,
                      'date': str(datetime.now().date()),
                      'aggregated_returns': []}
    for doc in cursor.collection.find({}, {'symbol': 1, '_id': 0}):
        document = cursor.collection.find_one({'symbol': f"{doc['symbol']}"})
        average_yearly_return = aggregate(document)
        ready_document['aggregated_returns'].append({'symbol': doc['symbol'],
                                                  'average_returns': average_yearly_return})
    target.insert_one(ready_document)

