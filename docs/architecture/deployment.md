# SyntharaAI Deployment Architecture

## Overview

SyntharaAI is designed to be deployed on Vercel, a cloud platform for static sites and serverless functions. This document describes the deployment architecture and configuration.

## Deployment Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │
│  Vercel Edge    │◄────┤  Vercel         │◄────┤  Gemini API     │
│  Network        │     │  Serverless     │     │  (Google Cloud) │
│                 │─────►                 │─────►                 │
└─────────────────┘     └─────────────────┘     └─────────────────┘
        │                      │
        │                      │
┌───────▼──────────┐    ┌──────▼───────┐
│                  │    │              │
│  Static Assets   │    │  Vercel      │
│  (HTML, CSS, JS) │    │  Storage     │
│                  │    │              │
└──────────────────┘    └──────────────┘
```

## Key Components

### 1. Vercel Serverless Functions

The Flask application is deployed as a serverless function on Vercel:

- **Entry Point**: The Flask application in `chatbot.py`
- **API Routes**: Configured in `vercel.json`
- **Cold Start**: Initial request may have a slight delay
- **Timeout**: Functions have a maximum execution time

### 2. Vercel Edge Network

Static assets are served through Vercel's global edge network:

- **CDN**: Content delivery network for fast global access
- **Caching**: Automatic caching of static assets
- **SSL**: Automatic SSL certificate management
- **Custom Domain**: Support for custom domains

### 3. Vercel Storage

Temporary file storage is handled by Vercel's ephemeral storage:

- **Limitations**: Storage is ephemeral and not persistent
- **Size Limits**: Limited storage capacity
- **Cleanup**: Files are automatically cleaned up

### 4. External Services

The application integrates with external services:

- **Gemini API**: Google's AI service for natural language processing
- **GitHub API**: For fetching user and repository information

## Configuration

### Vercel Configuration (`vercel.json`)

```json
{
  "version": 2,
  "buildCommand": "chmod +x build_vercel.sh && ./build_vercel.sh",
  "outputDirectory": ".vercel/output",
  "builds": [
    {
      "src": "chatbot.py",
      "use": "@vercel/python"
    },
    {
      "src": "assets/**",
      "use": "@vercel/static"
    },
    {
      "src": "*.html",
      "use": "@vercel/static"
    },
    {
      "src": "*.md",
      "use": "@vercel/static"
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "chatbot.py"
    },
    {
      "src": "/(.*\\.(js|css|svg|jpg|png|ico|json))",
      "dest": "/$1"
    },
    {
      "src": "/(.*)",
      "dest": "chatbot.py"
    }
  ],
  "env": {
    "PYTHONUNBUFFERED": "1"
  }
}
```

### Build Script (`build_vercel.sh`)

```bash
#!/bin/bash
set -e

# Create output directory structure
mkdir -p .vercel/output/static
mkdir -p .vercel/output/functions/api

# Copy static files
cp -r assets .vercel/output/static/
cp *.html .vercel/output/static/
cp *.md .vercel/output/static/

# Copy API files
cp chatbot.py .vercel/output/functions/api/
cp -r api .vercel/output/functions/

# Create config file
cat > .vercel/output/config.json << EOF
{
  "version": 3,
  "routes": [
    { "src": "/api/(.*)", "dest": "/api/chatbot.py" },
    { "handle": "filesystem" },
    { "src": "/(.*)", "dest": "/api/chatbot.py" }
  ]
}
EOF

echo "Build completed successfully"
```

### Environment Variables

The application requires the following environment variables:

- `GEMINI_API_KEY`: The API key for the Gemini API
- `ENABLE_AI_ANALYSIS`: Whether to enable AI-powered file analysis
- `FLASK_ENV`: The Flask environment (development or production)
- `PORT`: The port to run the server on (default: 8080)

These variables can be configured in Vercel's environment settings.

## Deployment Process

### 1. GitHub Integration

The application is deployed from a GitHub repository:

- **Automatic Deployments**: Changes to the main branch trigger deployments
- **Preview Deployments**: Pull requests create preview deployments
- **Rollbacks**: Easy rollback to previous deployments

### 2. Build Process

The build process consists of the following steps:

1. Clone the repository
2. Install dependencies from `requirements.txt`
3. Execute the build script (`build_vercel.sh`)
4. Deploy the built assets to Vercel's infrastructure

### 3. Monitoring and Logs

Vercel provides monitoring and logging capabilities:

- **Function Logs**: Logs from serverless functions
- **Deployment Logs**: Logs from the deployment process
- **Error Tracking**: Automatic error tracking and reporting
- **Analytics**: Basic analytics for requests and performance

## Scaling

The application scales automatically on Vercel:

- **Horizontal Scaling**: Automatic scaling of serverless functions
- **Global Distribution**: Content served from the nearest edge location
- **Load Balancing**: Automatic load balancing across instances
- **Auto-scaling**: Scales up or down based on traffic

## Limitations

The Vercel deployment has some limitations:

- **Execution Time**: Serverless functions have a maximum execution time
- **Memory Limits**: Limited memory for serverless functions
- **Cold Starts**: Initial requests may have a slight delay
- **File Storage**: Limited ephemeral storage for file uploads

## Local Development

For local development, the application can be run using:

```bash
python chatbot.py
```

This will start the Flask server on port 8080, which can be accessed at http://localhost:8080.
