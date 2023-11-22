""" URL mappings for the User API """

from django.urls import path
from . import views

app_name = 'UserAuth'

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('portal/', views.createUserPortalView.as_view(), name='portal'),
    path('token/', views.JWTCookieObtainPairView.as_view(), name='obtain_jwt'),
    path('token/refresh/', views.JWTCookieRefreshView.as_view(), name='refresh_jwt'),
    path('token/remove/', views.JWTRemoveCookiesView.as_view(), name='refresh_jwt'),
]
