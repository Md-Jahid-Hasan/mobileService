from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'number', views.NumberView, basename='number')
router.register(r'plan', views.PlanView, basename='plan')
router.register(r'company', views.CompanyView, basename='company')
router.register(r'user-subscription', views.UserSubscriptionView, basename='user-subscription')

urlpatterns = [
    path('', include(router.urls))
]