import requests
from lxml import html
import pandas as pd
import redis

from pipeline.db_connections import StockMarketDBConnector

from schedulers.celery import celery_app


redis_instance = redis.Redis()


class Financials(StockMarketDBConnector):
    COLLECTION = 'api_financialsdata'

    def __init__(self):
        super().__init__()
        self.from_id = self.get_last_id()


def toValidInt(string):
    if string:
        symbols_to_replace = (',', '.')
        for symbol_to_replace in symbols_to_replace:
            string = string.replace(symbol_to_replace, '')
        return int(string)
    return None


def toValidFloat(string):
    if string:
        return float(string)
    return None


class YahooFinancialStatementParser:
    TABLE_ROW_NAMES = None

    def __init__(self, url):
        self.url = url

    @staticmethod
    def make_get_request(url):
        response = requests.get(url).content
        return response

    @staticmethod
    def build_html_tree(response):
        tree = html.fromstring(response)
        return tree

    @staticmethod
    def get_table_div(tree, table_xpath="//div[contains(@class, 'D(tbr)')]"):
        table = tree.xpath(table_xpath)
        return table

    @staticmethod
    def parse_rows(table):
        if not table:
            return
        parsed_rows = []
        for row in table:
            element = row.xpath("./div")
            parsed_row = []
            for item in element:
                try:
                    text = item.xpath(".//span/text()[1]")
                    if text:
                        parsed_row.extend(text)
                    else:
                        parsed_row.append(None)
                except ValueError:
                    parsed_row.append(None)
            parsed_rows.append(parsed_row)
        return parsed_rows

    def extract_elements_by_column(self, rows: list):
        container = []
        for column in range(1, len(rows[0])):
            period = rows[0][column]
            rows_by_period = {}
            for row in rows[1:]:
                if row[0] in self.TABLE_ROW_NAMES:
                    rows_by_period.update({row[0]: row[column]})
            validated_statement = self.validate_rows(rows_by_period, period)
            container.append(validated_statement)
        return container

    def validate_rows(self, rows: dict, period: str):
        validated_statement = {'period': period}
        for row in self.TABLE_ROW_NAMES:
            if row not in rows:
                validated_statement.update({self.TABLE_ROW_NAMES[row][0]: None})
            else:
                row_name, row_type = self.TABLE_ROW_NAMES[row]
                validated_statement.update({row_name: row_type(rows[row])})
        return validated_statement

    def fetch_statement(self):
        response = self.make_get_request(self.url)
        tree = self.build_html_tree(response)
        table = self.get_table_div(tree)
        parsed_rows = self.parse_rows(table)
        extracted_statement = self.extract_elements_by_column(parsed_rows)
        return extracted_statement


class IncomeStatementParser(YahooFinancialStatementParser):
    TABLE_ROW_NAMES = {
        'Total Revenue': ('total_revenue', toValidInt),
        'Cost of Revenue': ('cost_of_revenue', toValidInt),
        'Gross Profit': ('gross_profit', toValidInt),
        'Operating Expense': ('operating_expense', toValidInt),
        'Operating Income': ('operating_income', toValidInt),
        'Net Non Operating Interest Income Expense': ('net_non_operating_interest_income_expense', toValidInt),
        'Other Income Expense': ('other_income_expense', toValidInt),
        'Pretax Income': ('pretax_income', toValidInt),
        'Tax Provision': ('tax_provision', toValidInt),
        'Net Income Common Stockholders': ('net_income_common_stockholders', toValidInt),
        'Diluted NI Available to Com Stockholders': ('diluted_ni_available_to_com_stockholders', toValidInt),
        'Basic EPS': ('basic_eps', toValidFloat),
        'Diluted EPS': ('diluted_eps', toValidFloat),
        'Basic Average Shares': ('basic_average_shares', toValidInt),
        'Diluted Average Shares': ('diluted_average_shares', toValidInt),
        'Total Operating Income as Reported': ('total_operating_income_as_reported', toValidInt),
        'Total Expenses': ('total_expenses', toValidInt),
        'Net Income from Continuing & Discontinued Operation': ('net_income_from_continuing_and_discontinued_operation', toValidInt),
        'Normalized Income': ('normalized_income', toValidInt),
        'Interest Income': ('interest_income', toValidInt),
        'Interest Expense': ('interest_expense', toValidInt),
        'Net Interest Income': ('net_interest_income', toValidInt),
        'EBIT': ('ebit', toValidInt),
        'EBITDA': ('ebitda', toValidInt),
        'Reconciled Cost of Revenue': ('reconciled_cost_of_revenue', toValidInt),
        'Reconciled Depreciation': ('reconciled_depreciation', toValidInt),
        'Net Income from Continuing Operation Net Minority Interest': ('net_income_from_continuing_operation_net_minority_interest', toValidInt),
        'Normalized EBITDA': ('normalized_ebitda', toValidInt),
        'Tax Rate for Calcs': ('tax_rate_for_calcs', toValidInt),
        'Tax Effect of Unusual Items': ('tax_effect_of_unusual_items', toValidInt)
    }


class BalanceSheetParser(YahooFinancialStatementParser):
    TABLE_ROW_NAMES = {
        'Total Assets': ('total_assets', toValidInt),
        'Total Liabilities Net Minority Interest': ('total_liabilities_net_minority_interest', toValidInt),
        'Total Equity Gross Minority Interest': ('total_equity_gross_minority_interest', toValidInt),
        'Total Capitalization': ('total_capitalization', toValidInt),
        'Common Stock Equity': ('common_stock_equity', toValidInt),
        'Net Tangible Assets': ('net_tangible_assets', toValidInt),
        'Working Capital': ('working_capital', toValidInt),
        'Invested Capital': ('invested_capital', toValidInt),
        'Tangible Book Value': ('tangible_book_value', toValidInt),
        'Total Debt': ('total_debt', toValidInt),
        'Net Debt': ('net_debt', toValidInt),
        'Share Issued': ('share_issued', toValidInt),
        'Ordinary Shares Number': ('ordinary_shares_number', toValidInt),
    }


class CashFlowParser(YahooFinancialStatementParser):
    TABLE_ROW_NAMES = {
        'Operating Cash Flow': ('operating_cash_flow', toValidInt),
        'Investing Cash Flow': ('investing_cash_flow', toValidInt),
        'Financing Cash Flow': ('financing_cash_flow', toValidInt),
        'End Cash Position': ('end_cash_position', toValidInt),
        'Income Tax Paid Supplemental Data': ('income_tax_paid_supplemental_data', toValidInt),
        'Interest Paid Supplemental Data': ('interest_paid_supplemental_data', toValidInt),
        'Capital Expenditure': ('capital_expenditure', toValidInt),
        'Issuance of Capital Stock': ('issuance_of_capital_stock', toValidInt),
        'Issuance of Debt': ('issuance_of_debt', toValidInt),
        'Repayment of Debt': ('repayment_of_debt', toValidInt),
        'Repurchase of Capital Stock': ('repurchase_of_capital_stock', toValidInt),
        'Free Cash Flow': ('free_cash_flow', toValidInt)
    }


def filter_out_present_symbols(haystack, needle):
    output = []
    for item in haystack:
        if item['Symbol'] not in needle:
            output.append(item)
    return output


def check_faults_status(faults):
    if faults > 10:
        return False
    return True


def check_if_active(symbol):
    if not redis_instance.exists(symbol):
        redis_instance.set(symbol, 1)
    else:
        redis_instance.incr(symbol, 1)
    if int(redis_instance.get(symbol)) >= 2:
        return False
    return True


celery_app.conf.beat_schedule = {
    'run-every-ten-secs': {
        'task': 'financials_spider.yahoo_spider.run',
        'schedule': 299
    }
}


@celery_app.task
def run():
    initial_data = pd.read_csv('~/PycharmProjects/stock_market_project/nasdaq.csv')
    active_data = initial_data.loc[initial_data['IsActive'] == True][['Symbol', 'Name', 'Sector', 'Industry']].to_dict('records')
    cursor = Financials()

    data_to_work = filter_out_present_symbols(active_data, cursor.get_present_symbols())
    statements = {
        'financials': ('financials', IncomeStatementParser),
        'balance-sheet': ('balance_sheet', BalanceSheetParser),
        'cash-flow': ('cash_flow', CashFlowParser)
    }

    from_id = cursor.from_id
    faults = 0
    for dict_ in data_to_work:
        status = True
        document = {
            'id': from_id,
            'symbol': dict_['Symbol'],
            'name': dict_['Name'],
            'sector': dict_['Sector'],
            'industry': dict_['Industry']
        }

        for statement in statements:
            statement_type, obj = statements[statement]
            url = f'https://finance.yahoo.com/quote/{dict_["Symbol"]}/{statement}?p={dict_["Symbol"]}'
            try:
                statement_data = obj(url).fetch_statement()
                document.update({statement_type: statement_data})
            except TypeError:
                print(f'{statement} FOR {document["name"]} MISSING')
                if not check_if_active(dict_['Symbol']):
                    initial_data.loc[initial_data['Symbol'] == dict_['Symbol'], 'IsActive'] = False
                faults += 1
                status = check_faults_status(faults)
                break
        else:
            from_id += 1
            cursor.collection.insert_one(document)
            faults = 0
            print(f'{document["name"]} DOWNLOADED SUCCESSFULLY')
        if not status:
            initial_data.to_csv('~/PycharmProjects/stock_market_project/nasdaq.csv', index=False)
            return
