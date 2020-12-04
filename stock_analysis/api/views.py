from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from api.serializers import (
    StockSerializer,
    AggregatedDataSerializer,
    SingleFinancialStatementSerializer,
    IncomeStatementSerializer,
    BalanceSheetSerializer,
    CashFlowSerializer
)
from api.models import (
    StockData,
    AggregatedData,
    FinancialsData
)
from utils.mixins import (
    RetrieveSpecificStatementView,
    JsonObjectMixin,
    FilterStatementsMixin
)
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


class StockPriceLister(APIView, JsonObjectMixin):
    """Returns stock daily stock prices for 5 years back for a chosen company"""
    def get(self, request, symbol):
        param = self.kwargs['symbol']
        queryset = StockData.objects.get(symbol=param)
        serialized_queryset = StockSerializer(queryset).data
        refactored_queryset = self.to_list(serialized_queryset['info'], ['Date', 'Adj_Close'])
        return Response(refactored_queryset)


class ListStockReturns(APIView):
    """Returns the top 20 companies by returns"""
    def get(self, request):
        queryset = AggregatedData.objects.all().order_by('-date')[:1]
        serialized = AggregatedDataSerializer(queryset, many=True).data
        s = sorted(serialized[0]['aggregated_returns'], key=lambda x: -x["average_returns"])
        refactored = {
            'Symbol': [item['symbol'] for item in s[:20]],
            'Returns': [item['average_returns']*100 for item in s[:20]]
        }
        return Response(refactored)


class SingleFinancialStatementView(RetrieveSpecificStatementView):
    """Returns the full set of financial statements for a given company"""
    model = FinancialsData
    lookup_field = 'symbol'
    serializer_class = SingleFinancialStatementSerializer
    queryset = FinancialsData.objects.all()


class FilteredStatementsView(FilterStatementsMixin):
    serializer_class = SingleFinancialStatementSerializer
    model = FinancialsData
