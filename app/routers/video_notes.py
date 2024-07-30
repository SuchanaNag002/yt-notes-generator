from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import google.generativeai as genai
import os
import logging
from google.oauth2 import service_account
from google.auth.transport.requests import Request as GoogleRequest

from app.services.youtube_transcript import extract_transcript
from app.schemas.video import VideoConvertRequest, VideoConvertResponse, Video

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure templates directory
templates = Jinja2Templates(directory="app/templates")

# Initialize router for API routes
router = APIRouter()

# Configure Google Generative AI with the API key from environment variables
api_key = os.getenv("GOOGLE_API_KEY")
if api_key:
    genai.configure(api_key=api_key)  # Set the API key for Google Generative AI
else:
    logger.error("GOOGLE_API_KEY environment variable is not set.")  # Log an error if the API key is not found

# Path to the service account key JSON file
credentials_path = 'services.json'

# Load and refresh the service account credentials
credentials = service_account.Credentials.from_service_account_file(
    credentials_path,
    scopes=['https://www.googleapis.com/auth/cloud-platform']
)

# Create a GoogleRequest instance to refresh the credentials
google_request = GoogleRequest()
credentials.refresh(google_request)  # Refresh credentials to ensure they are valid

print("Access Token:", credentials.token)  # Print the access token for debugging purposes

# Function to generate notes from the transcript text
def generate_notes(transcript_text: str, subject: str) -> str:
    # If a subject is provided, create a detailed prompt
    if subject:
        prompt = f"""
            Title: Detailed Notes on {subject} from YouTube Video Transcript

            As an expert in {subject}, your task is to provide detailed notes based on the transcript of a YouTube video I'll provide. Assume the role of a student and generate comprehensive notes covering the key concepts discussed in the video.

            Your notes should:

            - Analyze and explain the main ideas, theories, or concepts presented in the video.
            - Provide examples, illustrations, or case studies to support the understanding of the topic.
            - Offer insights or practical applications of the subject matter discussed.
            - Use clear language and concise explanations to facilitate learning.

            Please provide the notes based on the following transcript:

            {transcript_text}
        """
    # If no subject is provided, create a general overview prompt
    else:
        prompt = f"""
            Title: General Overview of the YouTube Video

            Your task is to provide a general overview of the transcript of a YouTube video I'll provide. Assume the role of a summarizer and generate a concise summary covering the key points discussed in the video.

            Your summary should:

            - Capture the main ideas and themes presented in the video.
            - Highlight important aspects or messages conveyed.
            - Provide a clear and concise overview for general understanding.

            Please provide the summary based on the following transcript:

            {transcript_text}
        """
        
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')  # Initialize the GenerativeModel with the specific model identifier
        response = model.generate_content(prompt)  # Generate content based on the prompt
        return response.text  # Return the generated text
    except Exception as e:
        logger.error(f"Error generating notes: {str(e)}")  # Log any errors encountered
        logger.error(f"Error details: {getattr(e, 'details', 'No additional details')}")  # Log additional error details if available
        return "Error generating notes. Please check server logs for more information."  # Return a user-friendly error message

# Define an endpoint to convert a video by extracting and processing its transcript
@router.post("/convert_video/", response_model=VideoConvertResponse)
async def convert_video(request: VideoConvertRequest):
    try:
        # Extracting the video ID from the YouTube URL
        video_id = str(request.youtube_link).split("=")[-1]
        # Constructing the thumbnail URL
        thumbnail_url = f"http://img.youtube.com/vi/{video_id}/0.jpg"

        # Extracting the transcript text from the YouTube video
        transcript_text = extract_transcript(str(request.youtube_link))
        if not transcript_text:
            logger.warning(f"Transcript extraction failed for video URL: {request.youtube_link}")
            raise HTTPException(status_code=400, detail="Failed to extract transcript from the video")

        # Generating notes from the transcript text
        notes = generate_notes(transcript_text, request.subject)

        # Creating a Video object 
        video = Video(url=request.youtube_link, thumbnail_url=thumbnail_url, notes=notes)

        # Returning the generated notes in the response
        return VideoConvertResponse(notes=notes)
    except HTTPException as e:
        logger.error(f"HTTPException: {e.detail}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to convert video: {str(e)}")

# Define an endpoint to render the HTML form
@router.get("/form", response_class=HTMLResponse)
async def form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
