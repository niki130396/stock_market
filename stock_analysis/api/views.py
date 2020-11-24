from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from api.serializers import \
    StockSerializer,\
    AggregatedDataSerializer,\
    SingleFinancialStatementSerializer,\
    IncomeStatementSerializer,\
    BalanceSheetSerializer,\
    CashFlowSerializer
from api.models import StockData, AggregatedData, FinancialsData

# Create your views here.


SERIALIZERS_DICT = {
    'financials': IncomeStatementSerializer,
    'balance_sheet': BalanceSheetSerializer,
    'cash_flow': CashFlowSerializer
}


class CompaniesByRevenueLister(APIView):
    """Returns companies' financial statements whose revenues are above the given param value"""
    def get(self, request, revenue):
        param = self.kwargs['revenue']
        data = FinancialsData.revenues.get_revenues(param)
        return Response(data)


class StockPriceLister(APIView):
    """Returns stock daily stock prices for 5 years back for a chosen company"""
    def get(self, request, symbol):
        param = self.kwargs['symbol']
        queryset = StockData.objects.get(symbol=param)
        serialized_queryset = StockSerializer(queryset).data
        refactored_queryset = {'Date': [item['Date'] for item in serialized_queryset['info']],
                               'Adj_Close': [item['Adj_Close'] for item in serialized_queryset['info']]}
        return Response(refactored_queryset)


class ListStockReturns(APIView):
    """Returns the top 20 companies by returns"""
    def get(self, request):
        queryset = AggregatedData.objects.all().order_by('-date')[:1]
        serialized = AggregatedDataSerializer(queryset, many=True).data
        s = sorted(serialized[0]['aggregated_returns'], key=lambda x: -x["average_returns"])
        refactored = {'Symbol': [item['symbol'] for item in s[:20]],
                      'Returns': [item['average_returns']*100 for item in s[:20]]}
        return Response(refactored)


class SingleFinancialStatementView(APIView):
    """Returns the full set of financial statements for a given company"""
    def get(self, request, symbol):
        param = self.kwargs['symbol']
        queryset = FinancialsData.objects.get(symbol=param)
        serialized_queryset = SingleFinancialStatementSerializer(queryset).data
        return Response(serialized_queryset)


class FinancialStatementTTMView(APIView):
        def get(self, request, type):
            param = self.kwargs['type']
            queryset = FinancialsData.objects.values('symbol', 'name', 'sector', 'industry', param)
            serialized_queryset = SERIALIZERS_DICT[param](queryset, many=True).data
            ttm = {}
            for ordered_dict in serialized_queryset:
                ttm[ordered_dict['symbol']] = ordered_dict[param][0]
            return Response(ttm)


class FinancialStatementBySector(APIView):
    def get(self, request, type, sector):
        type_ = self.kwargs['type']
        sector = self.kwargs['sector']

        queryset = FinancialsData.objects.values('symbol', 'name', 'sector', 'industry', type_)
        serialized_queryset = SERIALIZERS_DICT[type_](queryset, many=True).data
        response = {}
        for ordered_dict in serialized_queryset:
            if ordered_dict['sector'] == sector:
                response[ordered_dict['name']] = ordered_dict[type_][0]
        return Response(response)
