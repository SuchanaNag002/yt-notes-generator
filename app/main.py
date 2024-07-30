from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from app.routers import video_notes

app = FastAPI()

# Middleware for CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount the static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Jinja2 Templates
templates = Jinja2Templates(directory="app/templates")

# Include the video notes router
app.include_router(video_notes.router)

# Home route
@app.get("/")
async def read_root():
    return {"message": "Welcome to the Video Notes Generator API!"}
