from datetime import timedelta
from django.utils import timezone
from django.db.models import fields
from rest_framework import serializers
from . import models
from authenticateUser.serializers import UserDetailsSerializer


class NumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Number
        fields = '__all__'


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Plan
        fields = '__all__'


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Company
        fields = '__all__'


class UserSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserSubscription
        fields = '__all__'
        read_only_fields = ['end_date', 'number']

    def create(self, validated_data):
        """before confirming payment check that if already have a plan and
        user have primary number"""
        user = validated_data['user']
        last_subscription = user.subscription.last()

        if last_subscription.end_date > timezone.now():
            raise serializers.ValidationError("You already have a plan")

        if user.primary_number:
            validated_data['number'] = user.primary_number
        else:
            raise serializers.ValidationError("User has no primary number")

        if validated_data['plan'].name != "Gold":
            validated_data['end_date'] = timezone.now() + timedelta(30)
        return super().create(validated_data)


class NumberDetailsSerializer(NumberSerializer):
    company = CompanySerializer(read_only=True)
    user = UserDetailsSerializer(read_only=True)


class UserSubscriptionDetailsSerializer(UserSubscriptionSerializer):
    user = UserDetailsSerializer(read_only=True)
    plan = PlanSerializer(read_only=True)