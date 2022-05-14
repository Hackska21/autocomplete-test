#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# =============================================================================
"""Contains bussines logic to generate suggest"""
# -----------------------------------------------------------------------------
# Libraries
# -----------------------------------------------------------------------------
from decimal import Decimal

from django.conf import settings
from django.contrib.postgres.search import TrigramDistance
from django.db.models import QuerySet, DecimalField, ExpressionWrapper
from django.db.models.functions import Power, Sin, Cos, ATan2, Sqrt, Radians
from django.db.models import F

from search_app.models import Cities


# -----------------------------------------------------------------------------
# Classes
# -----------------------------------------------------------------------------


class ScoreService:
    # This parameter determines the magnitude of the distance,
    # increasing this value will decrease the precision  of location based score, increasing its final score.
    distance_normalizing_size = settings.DISTANCE_NORMALIZING_SIZE

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
