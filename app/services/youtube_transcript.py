from youtube_transcript_api import YouTubeTranscriptApi

# Function to extract transcript from a YouTube video
def extract_transcript(youtube_video_url):
    try:
        # Extracting the video ID from the YouTube URL
        video_id = youtube_video_url.split("=")[-1]

        # Fetching the transcript using the YouTubeTranscriptApi
        transcript = YouTubeTranscriptApi.get_transcript(video_id)

        # Combining the transcript text into a single string
        transcript_text = ""
        for i in transcript:
            transcript_text += " " + i["text"]

        return transcript_text  # Returning the combined transcript text
    except Exception as e:
        print(f"Error extracting transcript: {e}")  # Printing error message
        return None  # Returning None if an error occurs
