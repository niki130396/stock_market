import operator
from functools import reduce

from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from rest_framework.generics import (
    RetrieveAPIView,
    ListAPIView
)

from api.serializers import (
    IncomeStatementSerializer,
    BalanceSheetSerializer,
    CashFlowSerializer
)


SERIALIZERS_DICT = {
    'financials': IncomeStatementSerializer,
    'balance_sheet': BalanceSheetSerializer,
    'cash_flow': CashFlowSerializer
}


class RetrieveSpecificStatementView(RetrieveAPIView):
    """
    Checks if a query parameter is provided and if so filters the queryset
    and returns the specified statement and some meta data.
    If a query parameter is not provided it returns all three statements.
    """

    def get_queryset(self):
        statement_type = self.request.GET.get('statement')
        if statement_type:
            self.serializer_class = SERIALIZERS_DICT[statement_type]
            return self.queryset.values('symbol', 'name', 'sector', 'industry', statement_type)
        return self.queryset

    @method_decorator(cache_page(60*60))
    def dispatch(self, request, *args, **kwargs):
        return super(RetrieveSpecificStatementView, self).dispatch(request, *args, **kwargs)


class FilterStatementsMixin(ListAPIView):

    def get_queryset(self):
        if not hasattr(self, 'model'):
            raise AttributeError('Please provide a model')
        self.queryset = self.model.objects.all()
        query_parameters = self.request.GET
        if query_parameters:
            query = self.build_query(query_parameters)
            self.queryset = self.queryset.filter(reduce(operator.or_, query))
        return self.queryset

    def build_query(self, query_params):
        query = []
        for key in query_params:
            values = query_params.getlist(key)
            for value in values:
                query.append(Q(**{key: value}))
        return query

    @method_decorator(cache_page(60*60))
    def dispatch(self, request, *args, **kwargs):
        return super(FilterStatementsMixin, self).dispatch(request, *args, **kwargs)


class JsonObjectMixin:

    @staticmethod
    def to_list(list_of_dicts: list, required_fields: list):
        """
        This method converts a list of dictionaries
        into a dictionary of lists, which is a proper
        format when visualising time-series data
        """
        result = {}
        for field in required_fields:
            result.update({field: []})
            for dict_ in list_of_dicts:
                result[field].append(dict_[field])
        return result


"""
from django.db.models import Q
from api.models import FinancialsData

q = Q(symbol='GOOG') | Q(symbol='MSFT')
data = FinancialsData.objects.filter(q)
"""