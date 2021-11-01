from django.db.models import query
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.generics import CreateAPIView
from . import models
from . import serializers


class NumberView(viewsets.ModelViewSet):
    serializer_class = serializers.NumberSerializer

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.NumberDetailsSerializer
        return self.serializer_class

    def get_queryset(self):
        return models.Number.objects.filter(user=self.request.user)
    


class PlanView(viewsets.ModelViewSet):
    serializer_class = serializers.PlanSerializer
    queryset = models.Plan.objects.all()


class CompanyView(viewsets.ModelViewSet):
    serializer_class = serializers.CompanySerializer
    queryset = models.Company.objects.all()


class UserSubscriptionView(viewsets.ModelViewSet):
    serializer_class = serializers.UserSubscriptionSerializer
    queryset = models.UserSubscription.objects.all()

    def get_queryset(self):
        return models.UserSubscription.objects.filter(user=self.request.user)
    

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.UserSubscriptionDetailsSerializer
        return self.serializer_class
