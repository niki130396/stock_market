from djongo import models

from pipeline.db_connections import StockMarketDBConnector
# Create your models here.


class FinancialsDataConnector(StockMarketDBConnector):
    COLLECTION = 'api_financialsdata'


class CustomManager(models.DjongoManager):
    def get_revenues(self, n):
        cursor = FinancialsDataConnector()
        result = cursor.collection.find({'financials.total_revenue': {'$gt': n}}, {'_id': 0})
        result_list = []
        for item in result:
            result_list.append(item)
        return result_list


# ##################################################################
"""STOCK PRICES DATA"""


class Info(models.Model):
    Date = models.DateTimeField()
    High = models.DecimalField()
    Low = models.DecimalField()
    Open = models.DecimalField()
    Close = models.DecimalField()
    Volume = models.DecimalField()
    Adj_Close = models.DecimalField()
    Daily_Returns = models.DecimalField()
    Daily_Log_Returns = models.DecimalField()

    class Meta:
        abstract = True


class StockData(models.Model):
    symbol = models.CharField(max_length=50)
    info = models.ArrayField(model_container=Info)


#######################################################################################
"""AGGREGATED DATA COLLECTION"""


class AggregatedYearlyReturns(models.Model):
    symbol = models.CharField(max_length=50)
    average_returns = models.DecimalField()

    class Meta:
        abstract = True


class AggregatedData(models.Model):
    date = models.CharField(max_length=50)
    aggregated_returns = models.ArrayField(model_container=AggregatedYearlyReturns)
#####################################################################################


"""FINANCIAL STATEMENTS DATA"""


class IncomeStatement(models.Model):
    period = models.CharField(max_length=50)
    total_revenue = models.IntegerField()
    cost_of_revenue = models.IntegerField()
    gross_profit = models.IntegerField()
    operating_expense = models.IntegerField()
    operating_income = models.IntegerField()
    net_non_operating_interest_income_expense = models.IntegerField()
    other_income_expense = models.IntegerField()
    pretax_income = models.IntegerField()
    tax_provision = models.IntegerField()
    net_income_common_stockholders = models.IntegerField()
    diluted_ni_available_to_com_stockholders = models.IntegerField()
    basic_eps = models.DecimalField()
    diluted_eps = models.DecimalField()
    basic_average_shares = models.IntegerField()
    diluted_average_shares = models.IntegerField()
    total_operating_income_as_reported = models.IntegerField()
    total_expenses = models.IntegerField()
    net_income_from_continuing_and_discontinued_operation = models.IntegerField()
    normalized_income = models.IntegerField()
    interest_income = models.IntegerField()
    interest_expense = models.IntegerField()
    net_interest_income = models.IntegerField()
    ebit = models.IntegerField()
    ebitda = models.IntegerField()
    reconciled_cost_of_revenue = models.IntegerField()
    reconciled_depreciation = models.IntegerField()
    net_income_from_continuing_operation_net_minority_interest = models.IntegerField()
    normalized_ebitda = models.IntegerField()
    tax_rate_for_calcs = models.IntegerField()
    tax_effect_of_unusual_items = models.IntegerField()

    class Meta:
        abstract = True


class BalanceSheet(models.Model):
    period = models.CharField(max_length=50)
    total_assets = models.IntegerField()
    total_liabilities_net_minority_interest = models.IntegerField()
    total_equity_gross_minority_interest = models.IntegerField()
    total_capitalization = models.IntegerField()
    common_stock_equity = models.IntegerField()
    net_tangible_assets = models.IntegerField()
    working_capital = models.IntegerField()
    invested_capital = models.IntegerField()
    tangible_book_value = models.IntegerField()
    total_debt = models.IntegerField()
    net_debt = models.IntegerField()
    share_issued = models.IntegerField()
    ordinary_shares_number = models.IntegerField()

    class Meta:
        abstract = True


class CashFlow(models.Model):
    period = models.CharField(max_length=50)
    operating_cash_flow = models.IntegerField()
    investing_cash_flow = models.IntegerField()
    financing_cash_flow = models.IntegerField()
    end_cash_position = models.IntegerField()
    income_tax_paid_supplemental_data = models.IntegerField()
    interest_paid_supplemental_data = models.IntegerField()
    capital_expenditure = models.IntegerField()
    issuance_of_capital_stock = models.IntegerField()
    issuance_of_debt = models.IntegerField()
    repayment_of_debt = models.IntegerField()
    repurchase_of_capital_stock = models.IntegerField()
    free_cash_flow = models.IntegerField()

    class Meta:
        abstract = True


class FinancialsData(models.Model):
    symbol = models.CharField(max_length=10)
    name = models.CharField(max_length=50)
    sector = models.CharField(max_length=50)
    industry = models.CharField(max_length=50)
    financials = models.ArrayField(model_container=IncomeStatement)
    balance_sheet = models.ArrayField(model_container=BalanceSheet)
    cash_flow = models.ArrayField(model_container=CashFlow)
    objects = models.DjongoManager()
    revenues = CustomManager()
