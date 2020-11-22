from rest_framework import serializers

from .models import Stock, StockCalculatedDetail


class StockSerializer(serializers.ModelSerializer):
    # portfolio = serializers.IntegerField(write_only=True)

    class Meta:
        model = Stock
        fields = '__all__'


class StockCalculatedDetailSerializer(serializers.ModelSerializer):

    symbol = serializers.CharField(max_length=10)
    total_shares = serializers.DecimalField(decimal_places=2, max_digits=10, default=0.0, coerce_to_string=False)
    total_net_amount = serializers.DecimalField(decimal_places=2, max_digits=10, default=0.0, coerce_to_string=False)
    avg_net_price = serializers.DecimalField(decimal_places=2, max_digits=10, default=0.0, coerce_to_string=False)
    current_value = serializers.DecimalField(decimal_places=2, max_digits=10, default=0.0, coerce_to_string=False)

    class Meta:
        model = StockCalculatedDetail
        fields = ('symbol', 'total_shares', 'avg_net_price', 'current_value', 'total_net_amount')
