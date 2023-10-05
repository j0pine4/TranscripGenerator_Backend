from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

""" 
Serializers for the user API 
"""

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['name'] = f'{user.firstName} {user.lastName}'
        token['subscription'] = f'{user.subscription_tier}'

        return token

class UserSerializer(serializers.ModelSerializer):
    """ Serializer for the User object"""

    class Meta:
        model = get_user_model()
        fields = [
            'email',
            'password',
            'firstName',
            'lastName',
        ]
        extra_kwargs = {
            'password': {
                'write_only': True, 
                'min_length': 5
                }
            }

    def create(self, validated_data):
        """ Create and return user with encrypted password """
        print(**validated_data)
        return get_user_model().objects.create_user(**validated_data)
    