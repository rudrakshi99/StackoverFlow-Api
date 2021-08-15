 
from rest_framework import generics, permissions
from rest_framework.response import Response
from .serializers import  RegisterSerializer
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

# Register API
class RegisterAPI(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    
@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    """Creates token when a new User is created"""
    if created:
        Token.objects.create(user=instance)