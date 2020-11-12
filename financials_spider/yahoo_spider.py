import requests
from lxml import html
import pandas as pd

from pipeline.mongo_pipeline import MongoConnector


class Financials(MongoConnector):
    def __init__(self):
        super().__init__()
        self.collection = self.db.visualisations_financialsdata


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


STATEMENT_COLUMNS = {

    'financials': {
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
    },

    'balance-sheet': {
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
    },

    'cash-flow': {
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

                     }


def parse_yahoo_data(url, statement_type):
    response = requests.get(url).content
    tree = html.fromstring(response)
    table = tree.xpath("//div[contains(@class, 'D(tbr)')]")
    if not table:
        return
    parsed_rows = []
    for item in table:
        element = item.xpath("./div")
        parsed_row = []
        for rs in element:
            try:
                text = rs.xpath(".//span/text()[1]")
                if text:
                    parsed_row.extend(text)
                else:
                    parsed_row.append(None)
            except ValueError:
                parsed_row.append(None)
        parsed_rows.append(parsed_row)

    container = []
    for column in range(1, len(parsed_rows[0])):
        period = {}
        for row in parsed_rows[1:]:
            if row[0] in STATEMENT_COLUMNS[statement_type]:
                period.update({row[0]: row[column]})
        validated_statement = {'period': parsed_rows[0][column]}
        for row in STATEMENT_COLUMNS[statement_type]:
            if row not in period:
                validated_statement.update({STATEMENT_COLUMNS[statement_type][row][0]: None})
            else:
                row_name, row_type = STATEMENT_COLUMNS[statement_type][row]
                validated_statement.update({row_name: row_type(period[row])})
        container.append(validated_statement)
    return container


if __name__ == '__main__':
    initial_data = pd.read_csv('~/PycharmProjects/stock_market/barchart.csv')[['Symbol', 'Name', 'Sector', 'Industry']].to_dict('records')
    cursor = Financials()


    # id_ = 1
    # statement_types = {'financials': 'financials',
    #                    'balance-sheet': 'balance_sheet',
    #                    'cash-flow': 'cash_flow'}
    #
    # for dict_ in initial_data:
    #     document = {'id': id_,
    #                 'symbol': dict_['Symbol'],
    #                 'name': dict_['Name'],
    #                 'sector': dict_['Sector'],
    #                 'industry': dict_['Industry']}
    #
    #     for statement_type in statement_types:
    #         document[statement_types[statement_type]] = []
    #         url = f'https://finance.yahoo.com/quote/{dict_["Symbol"]}/{statement_type}?p={dict_["Symbol"]}'
    #         statement_data = parse_yahoo_data(url, statement_type)
    #         if not statement_data:
    #             print('FAULT')
    #             break
    #         document[statement_types[statement_type]].extend(statement_data)
    #     else:
    #         cursor.collection.insert_one(document)
    #         id_ += 1
    #         print(dict_['Symbol'])



"""
from visualisations.models import FinancialsData
from visualisations.serializers import IncomeStatementSerializer, BalanceSheetSerializer, CashFlowSerializer
serializers_dict = {'financials': IncomeStatementSerializer,
                                'balance_sheet': BalanceSheetSerializer,
                                'cash_flow': CashFlowSerializer}
param = 'cash_flow'
sector = 'Finance'
q = FinancialsData.objects.values('symbol', 'name', 'sector', 'industry', param)
s = serializers_dict[param](q, many=True).data
ttm = {}
for ordered_dict in s:
    if ordered_dict['sector'] == sector:
        ttm[ordered_dict['name']] = ordered_dict[param][0]
"""


"""
from visualisations.models import FinancialsData
from visualisations.serializers import SingleFinancialStatementSerializer
serializers_dict = {'financials': IncomeStatementSerializer,
                                'balance_sheet': BalanceSheetSerializer,
                                'cash_flow': CashFlowSerializer}
param = 'GOOG'
q = FinancialsData.objects.get(symbol=param)
s = SingleFinancialStatementSerializer(q).data
"""


"""
from visualisations.models import FinancialsData
q = FinancialsData.revenues.get_revenues(1000000)
"""