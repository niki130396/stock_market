from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse, HttpResponseRedirect

from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from visualisations.serializers import \
    StockSerializer,\
    AggregatedDataSerializer,\
    SingleFinancialStatementSerializer,\
    IncomeStatementSerializer,\
    BalanceSheetSerializer,\
    CashFlowSerializer
from visualisations.models import StockData, AggregatedData, FinancialsData

# Create your views here.


SERIALIZERS_DICT = {'financials': IncomeStatementSerializer,
                                'balance_sheet': BalanceSheetSerializer,
                                'cash_flow': CashFlowSerializer}


class CompaniesByRevenue(APIView):
    def get(self, request, revenue):
        param = self.kwargs['revenue']
        data = FinancialsData.revenues.get_revenues(param)
        return Response(data)


class ListStocks(APIView):
    def get(self, request, symbol):
        param = self.kwargs['symbol']
        queryset = StockData.objects.get(symbol=param)
        serialized_queryset = StockSerializer(queryset).data
        refactored_queryset = {'Date': [item['Date'] for item in serialized_queryset['info']],
                               'Adj_Close': [item['Adj_Close'] for item in serialized_queryset['info']]}
        return Response(refactored_queryset)


class ListStockReturns(APIView):
    def get(self, request):
        queryset = AggregatedData.objects.all().order_by('-date')[:1]
        serialized = AggregatedDataSerializer(queryset, many=True).data
        s = sorted(serialized[0]['aggregated_returns'], key=lambda x: -x["average_returns"])
        refactored = {'Symbol': [item['symbol'] for item in s[:20]],
                      'Returns': [item['average_returns']*100 for item in s[:20]]}
        return Response(refactored)


class SingleFinancialStatementView(APIView):
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


class StockPriceGraph(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return render(request, 'price_graph.html')
        return HttpResponseRedirect('/accounts/sign-up')


class StockReturnsGraph(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return render(request, 'returns_graph.html')
        return HttpResponseRedirect('/accounts/sign-up')


class FinancialStatementGraph(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return render(request, 'financial_statement_graph.html')
        return HttpResponseRedirect('/accounts/sign-up')


class FinancialStatementBarPlot(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return render(request, 'financial_statement_bar_plot.html')
        return HttpResponseRedirect('/accounts/sign-up')
