from django.urls import path
from rest_framework_simplejwt.views import token_obtain_pair, token_refresh
from .views import *

urlpatterns = [
    path('register/', RegisterAPIView.as_view()),
    path('token/', token_obtain_pair),
    path('token/refresh/', token_refresh),
]

urlpatterns += [
    path('account/me/', AccountRetrieveUpdateDestroyAPIView.as_view()),
    path('account/student/', StudentRetrieveUpdateDestroyAPIView.as_view()),
    path('account/change-password/', ChangePasswordAPIView.as_view()),
]