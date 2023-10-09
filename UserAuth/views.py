from rest_framework import generics, views
from rest_framework.response import Response
from rest_framework import permissions
from .serializers import UserSerializer
import os

from . import services

"""
Views for user API
"""

class CreateUserView(generics.CreateAPIView):
    """ Create a new user in the system """
    serializer_class = UserSerializer

class createUserPortalView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user_instance = request.user

        return Response(services.createCustomerPortal(user_instance))
