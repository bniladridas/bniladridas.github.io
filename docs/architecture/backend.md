# SyntharaAI Backend Architecture

## Overview

The SyntharaAI backend is built using Python with the Flask framework. It serves as both an API server for the chatbot and file analysis features, as well as a static file server for the frontend assets.

## Core Components

### Flask Application (`chatbot.py`)

The main Flask application is defined in `chatbot.py` and serves as the entry point for the backend. It includes:

- API endpoints for chat and file upload
- Static file serving
- Error handling and logging
- Integration with the Gemini API

### API Endpoints

```
┌─────────────────┐
│                 │
│  Flask Server   │
│                 │
└─────────────────┘
        │
        ├─── GET  /                 (Serve index.html)
        ├─── GET  /<path>           (Serve static files)
        ├─── GET  /api/chat         (Chat API info)
        ├─── POST /api/chat         (Chat interaction)
        └─── POST /api/upload       (File upload and analysis)
```

#### Chat API (`/api/chat`)

- **GET**: Returns information about the chat API
- **POST**: Accepts a message and returns a response
  - If the message matches a keyword in `FALLBACK_RESPONSES`, returns a pre-defined response
  - Otherwise, calls the Gemini API to generate a response

#### File Upload API (`/api/upload`)

- **POST**: Accepts file uploads, analyzes them, and returns the analysis results
  - Validates file types and sizes
  - Performs basic analysis based on file type
  - If AI analysis is enabled, calls the Gemini API for enhanced analysis

### File Analysis System

The file analysis system is a key component of the backend, providing:

- File type detection
- Basic analysis based on file type
- AI-powered analysis using the Gemini API
- Fallback to basic analysis when AI is unavailable

#### File Type Support

| File Category | Extensions | Analysis Capabilities |
|---------------|------------|----------------------|
| Image | png, jpg, jpeg, gif, bmp, webp, tiff | Metadata analysis, AI-powered content prediction |
| Document | pdf, doc, docx, txt, rtf, odt | Word count, topic detection, document type classification |
| Data | csv, xls, xlsx, json, xml | Structure analysis, data type detection, key column identification |
| Code | py, js, html, css, java, cpp, c, php, rb, go, ts, jsx, tsx | Language detection, complexity analysis, purpose identification |

### AI Integration

The backend integrates with Google's Gemini API for AI-powered features:

- **Chat Responses**: Generating context-aware responses to user messages
- **File Analysis**: Analyzing file content and providing insights
- **Fallback Mechanism**: Using pre-defined responses when AI is unavailable

#### AI Configuration

The AI integration is configured using environment variables:

- `GEMINI_API_KEY`: The API key for the Gemini API
- `ENABLE_AI_ANALYSIS`: Whether to enable AI-powered file analysis

### Error Handling and Logging

The backend includes comprehensive error handling and logging:

- **Logging**: Using Python's logging module to log application events
- **Error Handling**: Try-except blocks to catch and handle errors
- **User Feedback**: Providing user-friendly error messages

### Security Features

The backend includes several security features:

- **Input Validation**: Validating user inputs to prevent injection attacks
- **File Validation**: Checking file types and sizes before processing
- **API Key Management**: Secure storage of API keys using environment variables
- **CORS Configuration**: Proper configuration to prevent cross-origin issues

## Deployment

The backend is designed to be deployed on Vercel using serverless functions:

- **Entry Point**: The Flask application in `chatbot.py`
- **API Routes**: Configured in `vercel.json`
- **Static Files**: Served directly by Vercel
- **Environment Variables**: Configured in Vercel's environment settings

## File Structure

```
bniladridas.github.io/
├── chatbot.py           # Main Flask application
├── api/
│   └── index.py         # Vercel serverless entry point
├── uploads/             # Temporary file storage
├── assets/              # Static assets
├── vercel.json          # Vercel configuration
├── requirements.txt     # Python dependencies
└── .env                 # Environment variables
```

## Dependencies

The backend depends on the following Python packages:

- **Flask**: Web framework
- **google-genai**: Google Generative AI client library
- **python-dotenv**: Environment variable management
- **flask-cors**: Cross-origin resource sharing
- **requests**: HTTP client
