from django.urls import path
from .views import LoginView, UserCreateView, RetrieveUserView, LogOutView, LogOutAllView, \
    UpdateUserPNumber
from rest_framework_simplejwt.views import TokenRefreshView

app_name = 'authenticateUser'

urlpatterns = [
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogOutView.as_view(), name="logout"),
    path('token/refresh/', TokenRefreshView.as_view(), name="token-refresh"),
    path('change-number-plan/', UpdateUserPNumber.as_view(), name='change-number-plan'),
    path('logout_all/', LogOutAllView.as_view(), name="logout_all"),
    path('create-user/', UserCreateView.as_view(), name="create-user"),
    path('me/', RetrieveUserView.as_view(), name="me"),
]
