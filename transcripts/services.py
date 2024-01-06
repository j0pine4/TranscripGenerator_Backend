from youtube_transcript_api import YouTubeTranscriptApi
from UserAuth.models import SUBSCRIPTION_TIERS_ENUM
from .models import DailyTokenCount
from django.utils import timezone
import tiktoken

def getVideoTranscript(video_id):
    transcript_raw = []
    transcript_parse = ""

    transcript_raw = YouTubeTranscriptApi.get_transcript(video_id)

    for sentence in transcript_raw:
        transcript_parse += f"{sentence['text']} "

    return transcript_parse

def countTokens(inputText):
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    token_count = len(encoding.encode(inputText))
    return token_count

def token_counter_check(request):
    user_instance = request.user

    # Query the token_count table and see if the object exists for this user on this day
    # If not, create one
    try:
        token_count_instance = DailyTokenCount.objects.get(user=user_instance, created_on__day=timezone.now().day)
    except:
        token_count_instance = DailyTokenCount.objects.create(user=user_instance, created_on=timezone.now())

    return token_count_instance

def calculateTokenPercentage(token_limit, current_tokens, token_amount):

    remaining_tokens = token_limit - current_tokens

    # Return false for all transcripts above the chatgpt limit
    if token_amount > 16_000:
        return {
            "allowed": False,
            "current_tokens": current_tokens,
            "new_transcript_token_amount": token_amount,
            "remaining_tokens": remaining_tokens,
            "token_limit": token_limit
        }

    if (current_tokens + token_amount) > token_limit:
        return {
            "allowed": False,
            "current_tokens": current_tokens,
            "new_transcript_token_amount": token_amount,
            "remaining_tokens": remaining_tokens,
            "token_limit": token_limit
        }
    
    else:
        return {
            "allowed": True,
            "current_tokens": current_tokens,
            "new_transcript_token_amount": token_amount,
            "remaining_tokens": remaining_tokens,
            "token_limit": token_limit
        }


def userTokenCheck(request, tokenCount, token_counter):
    FREE_TOKEN_LIMIT = 20_000
    PREMIUM_TOKEN_LIMIT = 60_000
    ENHANCED_TOKEN_LIMIT = 120_000
    ULTIMATE_TOKEN_LIMIT = 500_000
    ADMIN_TOKEN_LIMIT = 500_000

    user = request.user

    # Current numbers of tokens this user has generated for the day
    current_tokens_used = token_counter.token_count
    
    if user.subscription_tier == SUBSCRIPTION_TIERS_ENUM.FREE.value:
        return calculateTokenPercentage(FREE_TOKEN_LIMIT, current_tokens_used, tokenCount)
    elif user.subscription_tier == SUBSCRIPTION_TIERS_ENUM.PREMIUM.value:
        return calculateTokenPercentage(PREMIUM_TOKEN_LIMIT, current_tokens_used, tokenCount)
    elif user.subscription_tier == SUBSCRIPTION_TIERS_ENUM.ENHANCED.value:
        return calculateTokenPercentage(ENHANCED_TOKEN_LIMIT, current_tokens_used, tokenCount)
    elif user.subscription_tier == SUBSCRIPTION_TIERS_ENUM.ULTIMATE.value:
        return calculateTokenPercentage(ULTIMATE_TOKEN_LIMIT, current_tokens_used, tokenCount)
    elif user.subscription_tier == SUBSCRIPTION_TIERS_ENUM.ADMIN.value:
        return calculateTokenPercentage(ADMIN_TOKEN_LIMIT, current_tokens_used, tokenCount)
 