
---

# YouTube Video Notes Generator

## Overview

This project provides a FastAPI application that generates detailed notes or summaries from YouTube video transcripts using Google Generative AI. Users can input a YouTube video URL and optionally specify a subject to receive comprehensive notes or a general overview based on the video's content.

## Features

- Extracts transcripts from YouTube videos.
- Generates detailed notes or general summaries using Google Generative AI.
- Supports both API key and service account authentication.

## Getting Started

### Prerequisites

- Python 3.11 or later
- A Google Cloud Project with access to Google Generative AI

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/yt-notes-generator.git
   cd yt-notes-generator
   ```

2. **Create and activate a virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install the required packages:**

   ```bash
   pip install -r requirements.txt
   ```

### Configuration

#### Using Google API Key

1. **Obtain a Google API Key:**

   - Go to the [Google Cloud Console](https://console.cloud.google.com/).
   - Navigate to the API & Services section.
   - Create or select an existing project.
   - Enable the Google Generative AI API.
   - Generate an API key.

2. **Set up environment variables:**

   Create a `.env` file in the root directory of the project and add the following line:

   ```env
   GOOGLE_API_KEY=your_api_key_here
   ```

3. **Configure the application to use the API key:**

   Ensure the `google.generativeai` library is configured to use the API key. This is handled in the application code as shown below:

   ```python
   import os
   import google.generativeai as genai

   api_key = os.getenv("GOOGLE_API_KEY")
   if api_key:
       genai.configure(api_key=api_key)
   else:
       logger.error("GOOGLE_API_KEY environment variable is not set.")
   ```

#### Using a Service Account

1. **Set up a Service Account:**

   - Go to the [Google Cloud Console](https://console.cloud.google.com/).
   - Navigate to IAM & Admin > Service Accounts.
   - Create a new service account and assign it the appropriate roles (e.g., `Editor` or `AI Platform Admin`).
   - Generate a JSON key for the service account and download it.

2. **Save the JSON key file:**

   Place the downloaded JSON key file in the project directory and name it `services.json`.

3. **Configure the application to use the service account:**

   Ensure the application code is set up to use the service account credentials as shown below:

   ```python
   from google.oauth2 import service_account
   from google.auth.transport.requests import Request as GoogleRequest

   credentials_path = 'services.json'
   credentials = service_account.Credentials.from_service_account_file(
       credentials_path,
       scopes=['https://www.googleapis.com/auth/cloud-platform']
   )
   google_request = GoogleRequest()
   credentials.refresh(google_request)
   ```

### Running the Application

1. **Start the FastAPI server:**

   ```bash
   uvicorn app.main:app --reload
   ```

2. **Access the application:**

   Open your browser and go to `http://127.0.0.1:8000/form` to use the application.

### API Endpoints

- **POST /convert_video/**: Convert a YouTube video to detailed notes or summary.
  - **Request Body**: `youtube_link` (str), `subject` (str, optional)
  - **Response**: Generated notes or summary

- **GET /form**: Render the HTML form for user input.

## Contributing

If you want to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a feature branch.
3. Commit your changes.
4. Push to the branch.
5. Create a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/)
- [Google Generative AI](https://cloud.google.com/generative-ai)
- [Pydantic](https://pydantic-docs.helpmanual.io/)

---
