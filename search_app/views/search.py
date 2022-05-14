from decimal import Decimal

from django.db.models import Value, DecimalField
from rest_framework import mixins, filters

from rest_framework.viewsets import GenericViewSet

from search_app.models import Cities
from search_app.serializers.cities import CitiesSerializer
from search_app.services.autocomplete_engine import CustomSearchFilter, FilterByCoordinates


class SearchViewSet(GenericViewSet, mixins.ListModelMixin):
    queryset = Cities.objects.all().annotate(score=Value("1.0", output_field=DecimalField(decimal_places=6)))
    filter_backends = [
        CustomSearchFilter,
        FilterByCoordinates
    ]
    search_fields = ["name"]

    serializer_class = CitiesSerializer
