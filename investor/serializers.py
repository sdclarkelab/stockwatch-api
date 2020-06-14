from rest_framework import serializers

from .models import Investor


class InvestorSerializer(serializers.ModelSerializer):
    #  password field is write only. It will not be displayed in the response
    password = serializers.CharField(write_only=True)

    #  Should not be modified
    is_staff = serializers.BooleanField(read_only=True)

    class Meta:
        model = Investor
        fields = (
            'id', 'username', 'first_name', 'last_name', 'email', 'date_joined', 'last_login', 'is_staff',
            'password', 'gender', 'ipo_notification')

    def create(self, validated_data):
        user = super(InvestorSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, investor, validated_data):
        investor.first_name = validated_data.get('first_name', investor.first_name)
        investor.last_name = validated_data.get('last_name', investor.last_name)
        investor.email = validated_data.get('email', investor.email)
        investor.gender = validated_data.get('gender', investor.gender)
        investor.ipo_notification = validated_data.get('ipo_notification', investor.ipo_notification)
        investor.save()

        return investor
