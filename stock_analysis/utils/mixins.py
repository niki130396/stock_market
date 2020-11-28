from rest_framework.generics import (
    RetrieveAPIView,
    ListAPIView
)
from rest_framework.views import APIView


class FilterQuerysetViewMixin(RetrieveAPIView):

    def get_queryset(self):
        if not hasattr(self, 'model'):
            raise AttributeError('A model has to be provided')
        query_params = self.request.GET
        self.lookup_field = 'symbol'
        if query_params:
            self.queryset = self.model.objects.get(**{self.lookup_field: query_params[self.lookup_field]})
            return self.queryset
        data = self.model.objects.all()
        return data


class JsonObjectMixin(APIView):

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
