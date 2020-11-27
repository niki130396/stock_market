from django.shortcuts import render
from django.views.generic import View, TemplateView
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin

from accounts.permissions import is_premium

from api.models import FinancialsData

from api.serializers import SingleFinancialStatementSerializer

# Create your views here.


def get_single_financial_statement(model, serializer, ticker):
    queryset = model.objects.get(symbol=ticker)
    serialized_queryset = serializer(queryset).data
    return serialized_queryset


class StockPriceGraph(LoginRequiredMixin, View):
    login_url = '/accounts/sign-up'

    @is_premium
    def get(self, request, *args, **kwargs):
        return render(request, 'price_graph.html')


class StockReturnsGraph(LoginRequiredMixin, View):
    login_url = '/accounts/sign-up'

    @is_premium
    def get(self, request, *args, **kwargs):
        return render(request, 'returns_graph.html')


class FinancialStatementGraph(LoginRequiredMixin, View):
    login_url = '/accounts/sign-up'

    @is_premium
    def get(self, request, *args, **kwargs):
        return render(request, 'financial_statement_graph.html')


class FinancialStatementBarPlot(LoginRequiredMixin, View):
    login_url = '/accounts/sign-up'

    @is_premium
    def get(self, request, *args, **kwargs):
        return render(request, 'financial_statement_bar_plot.html')


class IncomeStatementKeyMetricsAreaPlot(LoginRequiredMixin, TemplateView):
    login_url = '/accounts/sign-up'
    template_name = 'income_statement_area.html'
