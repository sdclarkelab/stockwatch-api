from rest_framework import serializers

from .models import Stock, StockCalculatedDetail


class StockSerializer(serializers.ModelSerializer):
    # portfolio = serializers.IntegerField(write_only=True)

    class Meta:
        model = Stock
        fields = '__all__'


class StockCalculatedDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = StockCalculatedDetail
        fields = '__all__'
