from rest_framework.generics import (
    RetrieveAPIView,
    ListAPIView
)

from api.serializers import (
    IncomeStatementSerializer,
    BalanceSheetSerializer,
    CashFlowSerializer
)

from rest_framework.views import APIView

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


class JsonObjectMixin:

    @staticmethod
    def to_list(list_of_dicts: list, required_fields: list) -> dict[list]:
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
