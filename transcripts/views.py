from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from . import services
from googleapiclient.discovery import build
import openai
import os

from . import models
from . import serializers

class TranscriptBuilderViewset(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):

        video_id = kwargs["video_id"]
        
        try:
            transcript = services.getVideoTranscript(video_id)
            tokens = services.countTokens(transcript)
            token_counter_instance = services.token_counter_check(request)
            
            token_check = services.userTokenCheck(request, tokens, token_counter_instance)

            data = {
                'transcript': transcript,
                'allowed': token_check['allowed'],
                'token_limit': token_check['token_limit'],
                'new_transcript_token_amount': token_check['new_transcript_token_amount'],
                'tokensUsed': token_check['current_tokens'],
                'tokensLeft': token_check['remaining_tokens'],
            }

            return Response(data)
        
        except:
            return Response("Could not find a valid transcript for this video.", status=status.HTTP_400_BAD_REQUEST)   
    
class GenerateOpenAIResponse(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):

        try:

            # Fetch the users daily token count and how many tokens this transcript uses
            user_instance = request.user
            daily_token_counter = models.DailyTokenCount.objects.filter(user=user_instance).latest('id')
            transcript_token_amount = request.data['transcript_token_amount']

            # Ensure that the incoming tokens are within the user limit
            token_check = services.userTokenCheck(request, transcript_token_amount, daily_token_counter)
            if token_check['allowed'] == False:
                return Response('This user does not have enough tokens for this transcript', status=status.HTTP_400_BAD_REQUEST)
            
            # Add to the counter and save
            daily_token_counter.token_count += transcript_token_amount
            daily_token_counter.save()

            openai.api_key = os.environ.get('OPENAI_SECRET_KEY')
            body = request.data['query'] + 'Lets think step by step \n\n html: '

            chat_completion = openai.chat.completions.create(
                model="gpt-3.5-turbo-1106", 
                temperature=0.5,
                messages=[
                    {"role": "system", "content": "Assistant is a large language model trained by OpenAI."},
                    {"role": "user", "content": body},
                ])
            
            output = chat_completion.choices[0].message.content.replace('\n', '<br/>').replace('<br/><br/>', '<br/>')

            return Response(output)
    
        except:
            return Response("Error occured while generating notes for this transcript", status=status.HTTP_400_BAD_REQUEST)
    

class CreateConversation(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):

        body = request.data

        openai.api_key = os.environ.get('OPENAI_SECRET_KEY')
        body = request.data['query'] + 'Lets think step by step \n\n output: '

        chat_completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-1106", 
            temperature=0.5,
            messages=[
                {"role": "system", "content": "Assistant is a large language model trained by OpenAI."},
                {"role": "user", "content": body},
            ])
        
        output = chat_completion.choices[0].message.content.replace('\n', '<br/>').replace('<br/><br/>', '<br/>')

        return Response(output)

class GetConversationMessages(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):

        conversationID = kwargs['id']

        messages_queryset = models.Message.objects.filter(conversation__id=conversationID).order_by("id")[1:]

        serializer = serializers.MessageSerializer(messages_queryset, many=True)

        return Response(serializer.data)
    
class CreateNewMessage(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):

        body = request.data
        conversationID = kwargs['id']

        conversation_instance = models.Conversation.objects.get(id=conversationID)

        # Create new message
        new_message = models.Message.objects.create(
            conversation = conversation_instance,
            role = models.Message.USR,
            content = body["content"]
        )

        new_message.save()

        # Query the new message and send it off to chatgpt with full context
        messages_queryset = models.Message.objects.filter(conversation__id=conversationID).order_by("id").values("role", "content")

        openai.api_key = os.environ.get('OPENAI_SECRET_KEY')

        chat_completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-1106", 
            temperature=0.5,
            messages=list(messages_queryset)
        )
            
        output = chat_completion.choices[0].message.content.replace('\n', '<br/>').replace('<br/><br/>', '<br/>')

        # Create a new message based on this response
        gptResponse = models.Message.objects.create(
            conversation = conversation_instance,
            role = models.Message.ASS,
            content = output
        )

        gptResponse.save()

        serializer = serializers.MessageSerializer(gptResponse, many=False)

        return Response(serializer.data)
    


class GetDocumentsByUser(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user_instance = request.user
        docType = request.query_params.get('type')

        queryset = models.Document.objects.filter(user=user_instance, type=docType)
        
        serializer = serializers.DocumentThumbnailSerializer(queryset, many=True)

        return Response(serializer.data)
    
class DocumentView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user_instance = request.user
        documentID = kwargs['id']
        queryset = models.Document.objects.get(id=documentID)

        if queryset.user != user_instance:
            return Response("User not associated with this document", status=status.HTTP_403_FORBIDDEN)

        serializer = serializers.DocumentSerializer(queryset, many=False)

        return Response(serializer.data)
    
    def delete(self, request, *args, **kwargs):
        user_instance = request.user
        documentID = kwargs['id']

        queryset = models.Document.objects.get(id=documentID)
        print(queryset)

        if queryset.user != user_instance:
            return Response("User not associated with this document", status=status.HTTP_403_FORBIDDEN)

        queryset.delete()

        return Response("Document deleted")

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
        serializer = serializers.DocumentThumbnailSerializer(new_document, many=False)

        return Response(serializer.data)

class CreateTestMessage(APIView):

    def post(self, request, *args, **kwargs):
        body = request.data

        newMessage = models.MessageTest.objects.create(
            body=body['message']
        )

        return Response("Message Created")
    
class YoutubeSearchViewset(APIView):

    YOUTUBE_API_KEY = os.environ.get('YOUTUBE_API_KEY')

    def post(self, request):
        body = request.data
        query = body['query']

        # Creat the service for the youtube api
        youtube = build('youtube', 'v3', developerKey=self.YOUTUBE_API_KEY)

        # Search youtube for videos matching this query
        request = youtube.search().list(part='snippet', q=body, maxResults=20, pageToken="CBQQAA")

        response = request.execute()
        youtube.close()

        return Response(response)

class AssistantViewset(APIView):

    openai.api_key = os.environ.get('OPENAI_SECRET_KEY')

    def get(self, request):

        assistant = openai.beta.assistants.create(
            name="Math Tutor",
            instructions="You are a personal math tutor. Write and run code to answer math questions.",
            tools=[{"type": "code_interpreter"}],
            model="gpt-3.5-turbo-1106", 
        )

        # Create our thread

class TokenCounterTest(APIView):

    def get(self, request):

        return Response(services.token_counter_check(request))
