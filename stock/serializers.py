from rest_framework import serializers

from .models import Stock


class StockSerializer(serializers.ModelSerializer):
    # portfolio = serializers.IntegerField(write_only=True)

    class Meta:
        model = Stock
        fields = '__all__'
