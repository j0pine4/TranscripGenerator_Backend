""" URL mappings for the Transcripts Application """

from django.urls import path
from . import views

urlpatterns = [
    path('create/<str:video_id>/', views.TranscriptBuilderViewset.as_view(), name='create'),
    path('generate/', views.GenerateOpenAIResponse.as_view(), name='generate'),
    path('documents/', views.GetDocumentsByUser.as_view(), name='getDocuments'),
    path('documents/create/', views.CreateDocumentByUser.as_view(), name='createDocuments'),
    path('documents/<int:id>/', views.DocumentView.as_view(), name='getDocument'),
    path('conversations/<int:id>/', views.GetConversationMessages.as_view(), name='getConversation'),
    path('conversations/<int:id>/messages/', views.GetConversationMessages.as_view(), name='getMessages'),
    path('conversations/<int:id>/messages/create/', views.CreateNewMessage.as_view(), name='createMessage'),
    path('message/create/', views.CreateTestMessage.as_view(), name='createTestMessage'),
]