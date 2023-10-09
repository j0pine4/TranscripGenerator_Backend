from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import permissions
from . import services, throttles
import openai
import os

from . import models
from . import serializers

class TranscriptBuilderViewset(APIView):

    throttle_classes = [throttles.Transcript_Throttle]

    def get(self, request, *args, **kwargs):

        video_id = kwargs["video_id"]
        transcript = services.getVideoTranscript(video_id)

        data = {
            'transcript': transcript,
            'tokenCount': services.countTokens(transcript)
        }

        return Response(data)
    
class GenerateOpenAIResponse(APIView):

    throttle_classes = [throttles.Generator_Throttle]

    def post(self, request, *args, **kwargs):

        openai.api_key = os.environ.get('OPENAI_SECRET_KEY')
        body = request.data['query']

        chat_completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", 
            temperature=0.5,
            messages=[
                {"role": "system", "content": "Assistant is a large language model trained by OpenAI."},
                {"role": "user", "content": body},
            ])
        
        output = chat_completion.choices[0].message.content.replace('\n', '<br/>').replace('<br/><br/>', '<br/>')

        return Response(output)
    
class TestToken(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        return Response(str(request.user))
    

class GetDocumentsByUser(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user_instance = request.user
        docType = request.query_params.get('type')

        queryset = models.Document.objects.filter(user=user_instance, type=docType)
        serializer = serializers.DocumentThumbnailSerializer(queryset, many=True)

        return Response(serializer.data)

class CreateDocumentByUser(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user_instance = request.user
        docType = request.query_params.get('type')
        body = request.data

        new_document = models.Document.objects.create(
            user=user_instance, 
            type=docType, 
            videoID=body['videoID'], 
            title=body['title'], 
            description=body['description'], 
            content=body['content'])
        
        new_document.save()
        serializer = serializers.DocumentThumbnailSerializer(new_document, many=True)

        return Response(serializer.data)
