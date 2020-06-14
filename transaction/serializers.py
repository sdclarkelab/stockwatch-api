from rest_framework import serializers

from .models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'


class TransactionInfoSerializer(serializers.ModelSerializer):
    total_shares = serializers.ReadOnlyField()
    average_price = serializers.ReadOnlyField()
    total_value = serializers.ReadOnlyField()

    class Meta:
        model = Transaction
        fields = ('id', 'total_shares', 'average_price', 'total_value')


class TransactionInfoSerializers(serializers.ModelSerializer):
    total_shares = serializers.ReadOnlyField()
    average_price = serializers.ReadOnlyField()
    total_value = serializers.ReadOnlyField()
    stock = serializers.ReadOnlyField()
    symbol = serializers.ReadOnlyField()

    class Meta:
        model = Transaction
        fields = ('total_shares', 'average_price', 'total_value', 'stock', 'symbol')
