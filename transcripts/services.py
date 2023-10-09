from youtube_transcript_api import YouTubeTranscriptApi
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