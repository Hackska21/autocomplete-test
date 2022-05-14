from decimal import Decimal

from rest_framework import filters

from search_app.services.autocomplete_engine import ScoreService


class CustomSearchFilter(filters.SearchFilter):
    def filter_queryset(self, request, queryset, view):
        # Use default fiter logic to make a fast subset
        queryset = super(CustomSearchFilter, self).filter_queryset(request, queryset, view)
        search_terms = self.get_search_terms(request)
        if not search_terms:
            return queryset
        # Use Search Logic to add score and order
        queryset = ScoreService().annotate_similarity(queryset, " ".join(search_terms))

        return queryset


class FilterByCoordinates(filters.BaseFilterBackend):
    def get_schema_operation_parameters(self, view):
        return [
            "latitude",
            "longitude"

        ]

    def get_schema_fields(self, view):
        return [
            "latitude",
            "longitude"

        ]

    def get_decimal_param(self, request, param_name: 'str'):
        params = request.query_params.get(param_name, None)
        if params is None:
            return None

        params = params.replace('\x00', '')  # strip null characters
        params = params.replace(',', ' ')
        try:
            value = Decimal(params)
        except:
            return None
        return value

    def get_parameter_values(self, request):
        lat = self.get_decimal_param(request, "latitude")
        long = self.get_decimal_param(request, "longitude")
        # print("lat", lat, "long", long)
        return lat, long

    def filter_queryset(self, request, queryset, view):
        lat, long = self.get_parameter_values(request)
        if lat is None or long is None:
            return queryset
        return ScoreService().annotate_distance(queryset, lat, long)