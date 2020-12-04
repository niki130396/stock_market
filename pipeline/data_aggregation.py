from pipeline.db_connections import StockMarketDBConnector

from datetime import datetime


class DBSource(StockMarketDBConnector):
    COLLECTION = 'api_stockdata'


class DBTarget(StockMarketDBConnector):
    COLLECTION = 'api_aggregateddata'


def aggregate(document):
    average_yearly_return = 0
    for item in document['info'][-255:]:
        average_yearly_return += item['Daily_Returns']
    average_yearly_return /= 255
    return average_yearly_return


if __name__ == '__main__':
    source = DBSource()
    target = DBTarget()

    ready_document = {'id': source.collection.find_one({}, {'id': 1, '_id': 0})['id'] + 1,
                      'date': str(datetime.now().date()),
                      'aggregated_returns': []}
    for doc in source.collection.find({}, {'symbol': 1, '_id': 0}):
        document = source.collection.find_one({'symbol': doc['symbol']})
        average_yearly_return = aggregate(document)
        ready_document['aggregated_returns'].append({
            'symbol': doc['symbol'],
            'average_returns': average_yearly_return
        })
    target.collection.insert_one(ready_document)

