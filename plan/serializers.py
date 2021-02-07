from rest_framework import serializers

from .models import Plan, PlanStatus


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = '__all__'


class PlanStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanStatus
        fields = '__all__'
