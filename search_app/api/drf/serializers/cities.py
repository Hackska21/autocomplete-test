from rest_framework import serializers

from search_app.models import Cities


class CitiesSerializer(serializers.ModelSerializer):
    latitude = serializers.DecimalField(source='lat', max_digits=9, decimal_places=6)
    longitude = serializers.DecimalField(source='long', max_digits=9, decimal_places=6)
    score = serializers.DecimalField(max_digits=2, decimal_places=1, default=0)

    class Meta:
        model = Cities
        fields = (
            'name',
            'latitude',
            'longitude',
            'score',
        )

        read_only_fields = fields
