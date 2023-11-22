from youtube_transcript_api import YouTubeTranscriptApi
from UserAuth.models import SUBSCRIPTION_TIERS_ENUM
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

def userTokenCheck(request, tokenCount):
    user = request.user

    if user.is_authenticated:
        if user.subscription_tier == SUBSCRIPTION_TIERS_ENUM.FREE.value:
            if tokenCount > 4096:
                return False
            else:
                return True
        elif user.subscription_tier == SUBSCRIPTION_TIERS_ENUM.PREMIUM.value:
            if tokenCount > 8000:
                return False
            else:
                return True
        elif user.subscription_tier == SUBSCRIPTION_TIERS_ENUM.ENHANCED.value:
            if tokenCount > 12000:
                return False
            else:
                return True
        elif user.subscription_tier == SUBSCRIPTION_TIERS_ENUM.ULTIMATE.value:
            if tokenCount > 16000:
                return False
            else:
                return True
        elif user.subscription_tier == SUBSCRIPTION_TIERS_ENUM.ADMIN.value:
            if tokenCount > 16000:
                return False
            else:
                return True
    else:
        if tokenCount > 2048:
            return False
        else:
            return True