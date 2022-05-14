from django.db.models import Value, DecimalField
from rest_framework import mixins

from rest_framework.viewsets import GenericViewSet

from search_app.models import Cities
from search_app.api.drf.serializers.cities import CitiesSerializer
from search_app.api.drf.filters import CustomSearchFilter, FilterByCoordinates


class SearchViewSet(GenericViewSet, mixins.ListModelMixin):
    queryset = Cities.objects.all().annotate(score=Value("1.0", output_field=DecimalField(decimal_places=6)))
    filter_backends = [
        CustomSearchFilter,
        FilterByCoordinates
    ]
    search_fields = ["name"]

    serializer_class = CitiesSerializer
