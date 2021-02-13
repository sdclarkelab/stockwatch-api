from rest_framework import serializers

from .models import Portfolio


class PortfolioSerializer(serializers.ModelSerializer):
    #  TODO: Hide user value from get response
    class Meta:
        model = Portfolio
        fields = ('id', 'name', 'status', 'user', 'is_default')

    def update(self, instance, validated_data):
        instance.status = validated_data.get('status', instance.status)
        instance.name = validated_data.get('name', instance.name)
        instance.save()

        return instance
