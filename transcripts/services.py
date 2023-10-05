from youtube_transcript_api import YouTubeTranscriptApi


def getVideoTranscript(video_id):
    transcript_raw = []
    transcript_parse = ""

    transcript_raw = YouTubeTranscriptApi.get_transcript(video_id)

    for sentence in transcript_raw:
        transcript_parse += f"{sentence['text']} "

    return transcript_parse