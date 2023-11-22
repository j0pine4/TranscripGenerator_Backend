from django.conf import settings
from rest_framework import generics, views
from rest_framework.response import Response
from rest_framework import permissions
from .serializers import UserSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import status
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
    
class JWTSetCookieMixin:
    def finalize_response(self, request, response, *args, **kwargs):
        
        # Refresh Token
        if response.data.get("refresh"):
            response.set_cookie(
                settings.SIMPLE_JWT["REFRESH_TOKEN_NAME"],
                response.data.get("refresh"),
                httponly=True,
                samesite=settings.SIMPLE_JWT["JWT_COOKIE_SAMESITE"],
                
            )
            
        # Access Token
        if response.data.get("access"):
            response.set_cookie(
                settings.SIMPLE_JWT["ACCESS_TOKEN_NAME"],
                response.data.get("access"),
                httponly=True,
                samesite=settings.SIMPLE_JWT["JWT_COOKIE_SAMESITE"]
            )
        
        return super().finalize_response(request, response, *args, **kwargs)

class JWTCookieObtainPairView(JWTSetCookieMixin, TokenObtainPairView):
    pass

class JWTRemoveCookiesView(views.APIView):

    authentication_classes = []

    def get(self, request, *args, **kwargs):
        response = Response('User Logged Out')
        response.delete_cookie(settings.SIMPLE_JWT["REFRESH_TOKEN_NAME"])
        response.delete_cookie(settings.SIMPLE_JWT["ACCESS_TOKEN_NAME"])

        return response

class JWTCookieRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):

        refresh_token = request.COOKIES.get(settings.SIMPLE_JWT["REFRESH_TOKEN_NAME"])

        if refresh_token:
            request.data['refresh'] = refresh_token

        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:

            response.set_cookie(
                settings.SIMPLE_JWT["ACCESS_TOKEN_NAME"],
                response.data.get("access"),
                httponly=True,
                samesite=settings.SIMPLE_JWT["JWT_COOKIE_SAMESITE"]
            )
        else:
            raw_token = request.COOKIES.get(settings.SIMPLE_JWT["ACCESS_TOKEN_NAME"]) or None

            if raw_token is None:
                response.status_code = status.HTTP_401_UNAUTHORIZED
            else: 
                response.delete_cookie(settings.SIMPLE_JWT["REFRESH_TOKEN_NAME"])
                response.delete_cookie(settings.SIMPLE_JWT["ACCESS_TOKEN_NAME"])

        return response