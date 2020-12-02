from pandas_datareader import DataReader
from pandas_datareader._utils import RemoteDataError
from datetime import datetime
import pandas as pd
import numpy as np
from pipeline.db_connections import StockMarketDBConnector


class MongoConnector(StockMarketDBConnector):
    COLLECTION = 'api_stockdata'


class DocumentInserter(MongoConnector):
    ID = 1

    def __init__(self):
        super().__init__()
        self.db_symbols = set([i['symbol'] for i in self.collection.find({}, {'symbol': 1, '_id': 0})])
        self.from_id = self.get_last_id()

    def insert_document(self, df, symbol):
        if symbol not in self.db_symbols:
            info = df.to_dict('records')
            document = {'id': self.from_id, 'symbol': symbol, 'info': info}
            self.collection.insert_one(document)
            self.from_id += 1
            return
        raise Exception()

    def get_last_id(self):
        ids = [document['id'] for document in self.collection.find({}, {'id': 1, '_id': 0}).sort([('id', -1)]).limit(1)]
        if not ids:
            return 1
        return ids[0] + 1

    @property
    def present_symbols(self):
        symbols = [document['symbol'] for document in self.collection.find({}, {'symbol': 1, '_id': 0})]
        return symbols


class DocumentUpdater(MongoConnector):
    def __init__(self):
        super().__init__()

    @staticmethod
    def __get_new_data(symbol, start_date) -> pd.DataFrame:
        return StockDataDownloader.get_data(symbol, start_date)

    def update_document(self, symbol):
        document = self.collection.find_one({'symbol': symbol})
        last_date = document['info'][-1]['Date']
        new_document = self.__get_new_data(symbol, last_date).to_dict('records')
        document['info'] = document['info'][len(new_document):]
        document['info'].extend(new_document)
        self.collection.update_one({'symbol': symbol}, {'$set': document})


class StockDataDownloader:
    COLUMNS = ['Date', 'High', 'Low', 'Open', 'Close', 'Volume', 'Adj_Close', 'Daily_Returns', 'Daily_Log_Returns']

    @staticmethod
    def get_data(symbol, start_date=datetime(year=2015, month=1, day=1)):

        data = DataReader(symbol, 'yahoo', start_date).reset_index()
        data['Daily_Returns'] = data['Adj Close'].pct_change()
        data['Daily_Log_Returns'] = np.log(data['Adj Close']) - np.log(data['Adj Close'].shift(1))
        data.drop(data.index[:1], inplace=True)
        data.columns = StockDataDownloader.COLUMNS
        return data


def get_non_existent_symbols(symbols_list, present_symbols):
    return set(symbols_list).difference(present_symbols)


if __name__ == '__main__':
    engine = DocumentInserter()
    symbols = pd.read_csv('~/PycharmProjects/test_stock_market/barchart.csv')['Symbol'].to_list()
    downloader = StockDataDownloader()
    symbols = get_non_existent_symbols(symbols, engine.present_symbols)

    for symbol in symbols:
        try:
            df = downloader.get_data(symbol)
            engine.insert_document(df, symbol)
            print(f'INSERTED {symbol}')
        except RemoteDataError:
            print(f'Could not fetch data for symbol {symbol}')
        except KeyError as key_error:
            print(f'Missing fields {key_error.args} for {symbol}')
