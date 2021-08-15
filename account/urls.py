from .views import  RegisterAPI
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

app_name='accounts'

urlpatterns = [
    path('register/', RegisterAPI.as_view(), name='register'),
    path('login/', obtain_auth_token)

]