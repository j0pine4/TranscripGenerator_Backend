from rest_framework import generics, views
from rest_framework.response import Response
from .serializers import UserSerializer
import os

from root import services

"""
Views for user API
"""

class CreateUserView(generics.CreateAPIView):
    """ Create a new user in the system """
    serializer_class = UserSerializer
