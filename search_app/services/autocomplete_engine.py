#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# =============================================================================
"""Contains bussines logic to generate suggest"""
# -----------------------------------------------------------------------------
# Libraries
# -----------------------------------------------------------------------------
from decimal import Decimal


from django.contrib.postgres.search import TrigramDistance
from django.db.models import QuerySet, DecimalField, ExpressionWrapper, Value
from rest_framework import filters
from django.db.models.functions import Radians, Power, Sin, Cos, ATan2, Sqrt, Radians, Round
from django.db.models import F

from search_app.models import Cities

from django.db.models import Func

class RoundWithPlaces(Func):
    function = 'ROUND'

# -----------------------------------------------------------------------------
# Classes
# -----------------------------------------------------------------------------

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


class ScoreService:
    # This parameter determines the magnitude of the distance,
    # increasing this value will decrease the pressure of the filter, increasing its final score.
    distance_normalizing_size = 100

    # def suggest_words(self, word):
    #    return self.model.objects.filter(body_text__search=word)

    def annotate_similarity(self, queryset: 'QuerySet[Cities]', word: 'str'):
        queryset = queryset.annotate(
            score=ExpressionWrapper(
                (1 - TrigramDistance('name', word)),
                output_field=DecimalField())
        )
        return queryset.order_by("-score")


    def annotate_distance(self, queryset: 'QuerySet[Cities]', lat: 'Decimal', long: 'Decimal'):
        """
            Implements haversine formula to get distances and normalizes it 1 to 0
        :param queryset:
        :param lat:
        :param long:
        :return:
        """
        dlat = Radians(F('lat') - lat)
        dlong = Radians(F('long') - long)

        a = (Power(Sin(dlat / 2), 2) + Cos(Radians(lat))
             * Cos(Radians(F('lat'))) * Power(Sin(dlong / 2), 2)
             )

        c = 2 * ATan2(Sqrt(a), Sqrt(1 - a))
        d = 6371 * c

        # Normalization
        queryset = queryset.annotate(distance=1 / (1 + d / self.distance_normalizing_size))
        # print(queryset[0].distance)
        # use this with score
        queryset = queryset.annotate(score=(F("distance") + F("score")) / 2, )

        return queryset.order_by("-score")
