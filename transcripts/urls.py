""" URL mappings for the Transcripts Application """

from django.urls import path
from . import views

urlpatterns = [
    path('create/<str:video_id>/', views.TranscriptBuilderViewset.as_view(), name='create'),
    path('generate/', views.GenerateOpenAIResponse.as_view(), name='generate'),
    path('documents/', views.GetDocumentsByUser.as_view(), name='getDocuments'),
    path('test/', views.TestToken.as_view(), name='test'),
]