# Firebase
import os
from rest_framework import authentication, exceptions
from .exceptions import InvalidAuthToken
from django.contrib.auth import get_user_model
from django.conf import settings
from supabase import create_client, Client
from . import services

SUPABASE_URL = os.environ.get('SUPABASE_URL')
SUPABASE_ANON_KEY = os.environ.get('SUPABASE_ANON_KEY')
supabase = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

class SupabaseAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        
        token = request.headers.get("authorization", "").replace("Bearer ", "")

        if not token:
          return None

        try:
            auth = supabase.auth.get_user(token) 
            user_id = auth.user.id
        except Exception:
            raise InvalidAuthToken("Invalid auth token")

        try:
            user = get_user_model().objects.get(supabaseID=user_id)
        except:
            user = get_user_model().objects.create(
                supabaseID=user_id, 
                email=auth.user.email,
                firstName=auth.user.user_metadata['firstName'], 
                lastName=auth.user.user_metadata['lastName'], 
                )
            
            # Generate stripe customer ID
            customer = services.createNewCustomer(user)
            user.stripeCustomerID = customer.id

            user.save()

        return (user, None)