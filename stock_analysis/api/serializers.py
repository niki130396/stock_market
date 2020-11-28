from abc import ABC

from rest_framework import serializers
from api.models import StockData, AggregatedData, IncomeStatement, BalanceSheet, CashFlow, FinancialsData

from datetime import datetime, timedelta


def date_handler(date_string):
    if date_string == 'ttm':
        return str(datetime.now().date().strftime('%m/%d/%Y'))
    return date_string


class NormalizedInfoField(serializers.RelatedField, ABC):
    queryset = StockData.objects.all()

    def to_representation(self, value):
        dict_ = {
            'Date': datetime.strftime(value['Date'], '%Y-%m-%d'),
            'High': float(value['High']),
            'Low': float(value['Low']),
            'Open': float(value['Open']),
            'Volume': float(value['Volume']),
            'Adj_Close': float(value['Adj_Close']),
            'Daily_Returns': float(value['Daily_Returns']),
            'Daily_Log_Returns': float(value['Daily_Log_Returns'])
        }
        return dict_


class StockSerializer(serializers.ModelSerializer):
    info = NormalizedInfoField(many=True)

    class Meta:
        model = StockData
        fields = ['symbol', 'info']


class AggregatedReturnsField(serializers.RelatedField, ABC):
    queryset = AggregatedData.objects.all()

    def to_representation(self, value):
        dict_ = {'symbol': value['symbol'],
                 'average_returns': value['average_returns']}
        return dict_


class AggregatedDataSerializer(serializers.ModelSerializer):
    aggregated_returns = AggregatedReturnsField(many=True)

    class Meta:
        model = AggregatedData
        fields = ['date', 'aggregated_returns']


class IncomeStatementField(serializers.RelatedField, ABC):
    queryset = FinancialsData.objects.all()

    def to_representation(self, value):
        dict_ = {
        'period': date_handler(value['period']),
        'total_revenue': value['total_revenue'],
        'cost_of_revenue': value['cost_of_revenue'],
        'gross_profit': value['gross_profit'],
        'operating_expense': value['operating_expense'],
        'operating_income': value['operating_income'],
        'net_non_operating_interest_income_expense': value['net_non_operating_interest_income_expense'],
        'other_income_expense': value['other_income_expense'],
        'pretax_income': value['pretax_income'],
        'tax_provision': value['tax_provision'],
        'net_income_common_stockholders': value['net_income_common_stockholders'],
        'diluted_ni_available_to_com_stockholders': value['diluted_ni_available_to_com_stockholders'],
        'basic_eps': value['basic_eps'],
        'diluted_eps': value['diluted_eps'],
        'basic_average_shares': value['basic_average_shares'],
        'diluted_average_shares': value['diluted_average_shares'],
        'total_operating_income_as_reported': value['total_operating_income_as_reported'],
        'total_expenses': value['total_expenses'],
        'net_income_from_continuing_and_discontinued_operation': value['net_income_from_continuing_and_discontinued_operation'],
        'normalized_income': value['normalized_income'],
        'interest_income': value['interest_income'],
        'interest_expense': value['interest_expense'],
        'net_interest_income': value['net_interest_income'],
        'ebit': value['ebit'],
        'ebitda': value['ebitda'],
        'reconciled_cost_of_revenue': value['reconciled_cost_of_revenue'],
        'reconciled_depreciation': value['reconciled_depreciation'],
        'net_income_from_continuing_operation_net_minority_interest': value['net_income_from_continuing_operation_net_minority_interest'],
        'normalized_ebitda': value['normalized_ebitda'],
        'tax_rate_for_calcs': value['tax_rate_for_calcs'],
        'tax_effect_of_unusual_items': value['tax_effect_of_unusual_items']
        }

        return dict_


class BalanceSheetField(serializers.RelatedField, ABC):
    queryset = FinancialsData.objects.all()

    def to_representation(self, value):
        dict_ = {
        'period': date_handler(value['period']),
        'total_assets': value['total_assets'],
        'total_liabilities_net_minority_interest': value['total_liabilities_net_minority_interest'],
        'total_equity_gross_minority_interest': value['total_equity_gross_minority_interest'],
        'total_capitalization': value['total_capitalization'],
        'common_stock_equity': value['common_stock_equity'],
        'net_tangible_assets': value['net_tangible_assets'],
        'working_capital': value['working_capital'],
        'invested_capital': value['invested_capital'],
        'tangible_book_value': value['tangible_book_value'],
        'total_debt': value['total_debt'],
        'net_debt': value['net_debt'],
        'share_issued': value['share_issued'],
        'ordinary_shares_number': value['ordinary_shares_number'],
        }

        return dict_


class CashFlowField(serializers.RelatedField, ABC):
    queryset = FinancialsData.objects.all()

    def to_representation(self, value):
        dict_ = {
        'period': date_handler(value['period']),
        'operating_cash_flow': value['operating_cash_flow'],
        'investing_cash_flow': value['investing_cash_flow'],
        'financing_cash_flow': value['financing_cash_flow'],
        'end_cash_position': value['end_cash_position'],
        'income_tax_paid_supplemental_data': value['income_tax_paid_supplemental_data'],
        'interest_paid_supplemental_data': value['interest_paid_supplemental_data'],
        'capital_expenditure': value['capital_expenditure'],
        'issuance_of_capital_stock': value['issuance_of_capital_stock'],
        'issuance_of_debt': value['issuance_of_debt'],
        'repayment_of_debt': value['repayment_of_debt'],
        'repurchase_of_capital_stock': value['repurchase_of_capital_stock'],
        'free_cash_flow': value['free_cash_flow']
        }

        return dict_


class SingleFinancialStatementSerializer(serializers.ModelSerializer):
    financials = IncomeStatementField(many=True)
    balance_sheet = BalanceSheetField(many=True)
    cash_flow = CashFlowField(many=True)

    class Meta:
        model = FinancialsData
        fields = ('__all__')


class IncomeStatementSerializer(serializers.ModelSerializer):
    financials = IncomeStatementField(many=True)

    class Meta:
        model = FinancialsData
        fields = ('symbol', 'name', 'sector', 'industry', 'financials')


class BalanceSheetSerializer(serializers.ModelSerializer):
    balance_sheet = BalanceSheetField(many=True)

    class Meta:
        model = FinancialsData
        fields = ('symbol', 'name', 'sector', 'industry', 'balance_sheet')


class CashFlowSerializer(serializers.ModelSerializer):
    cash_flow = CashFlowField(many=True)

    class Meta:
        model = FinancialsData
        fields = ('symbol', 'name', 'sector', 'industry', 'cash_flow')


"""
from visualisations.models import AggregatedData
from visualisations.serializers import AggregatedDataSerializer
q = AggregatedData.objects.all().order_by('-date')[:1]
s = AggregatedDataSerializer(q, many=True).data
sorted = sorted(s[0]['aggregated_returns'], key=lambda x: -x["average_returns"])
r = {'Date': [item['symbol'] for item in sorted, 'average_returns': [item['Open'] for item in sorted}
"""

"""
from visualisations.models import StockData
from visualisations.serializers import StockSerializer
q = StockData.objects.filter(symbol="GOOG")
s = StockSerializer(q, many=True).data
r = {'Date': [item['Date'] for item in serialized_queryset[0]['info']],
                       'Open': [item['Open'] for item in serialized_queryset[0]['info']]}
"""