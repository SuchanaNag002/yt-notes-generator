from pydantic import BaseModel

# Define a model for the request payload when converting a video
class VideoConvertRequest(BaseModel):
    youtube_link: str  # URL of the YouTube video to be processed
    subject: str        # Subject or topic of the video for generating notes

# Define a model for the response payload when returning the generated notes
class VideoConvertResponse(BaseModel):
    notes: str  # The generated notes or summary of the video

# Define a model for the Video object, used for returning detailed video information
class Video(BaseModel):
    url: str             # URL of the YouTube video
    thumbnail_url: str   # URL of the video's thumbnail image
    notes: str           # Generated notes or summary of the video
