from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin

from accounts.permissions import is_premium
# Create your views here.


class StockPriceGraph(LoginRequiredMixin, View):
    login_url = 'accounts/sign-up'

    @is_premium
    def get(self, request, *args, **kwargs):
        return render(request, 'price_graph.html')


class StockReturnsGraph(LoginRequiredMixin, View):
    login_url = 'accounts/sign-up'

    def get(self, request, *args, **kwargs):
        return render(request, 'returns_graph.html')


class FinancialStatementGraph(LoginRequiredMixin, View):
    login_url = 'accounts/sign-up'

    @is_premium
    def get(self, request, *args, **kwargs):
        return render(request, 'financial_statement_graph.html')


class FinancialStatementBarPlot(LoginRequiredMixin, View):
    login_url = 'accounts/sign-up'

    @is_premium
    def get(self, request, *args, **kwargs):
        return render(request, 'financial_statement_bar_plot.html')
