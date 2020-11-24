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

    def __init__(self, *args, **kwargs):
        super(IncomeStatementKeyMetricsAreaPlot, self).__init__(*args, **kwargs)
        self.ticker = None

    def get(self, request, *args, **kwargs):
        ticker = self.request.GET.get('ticker', 'GOOG')
        self.ticker = ticker
        print(self.request.GET)
        return super(IncomeStatementKeyMetricsAreaPlot, self).get(request, *args, *kwargs)

    def get_context_data(self, **kwargs):
        context = super(IncomeStatementKeyMetricsAreaPlot, self).get_context_data(**kwargs)

        financial_statement = get_single_financial_statement(
            FinancialsData,
            SingleFinancialStatementSerializer,
            self.ticker
        )
        income_statement = financial_statement['financials']
        extra_context = {
            'period': ['1111', '2222', '3333', '4444', '5555'],#[period['period'] for period in income_statement][::-1],
            'revenue': [period['total_revenue'] for period in income_statement][::-1],
            'gross_profit': [period['gross_profit'] for period in income_statement][::-1],
            'ebit': [period['ebit'] for period in income_statement][::-1]
        }
        context.update(extra_context)
        return context
