#!/bin/bash

# Create necessary directories
mkdir -p .vercel/output/static
mkdir -p .vercel/output/functions/api

# Copy static files
cp -r assets .vercel/output/static/
cp *.html .vercel/output/static/
cp *.md .vercel/output/static/

# Create serverless function
cp chatbot.py .vercel/output/functions/api/
cp requirements.txt .vercel/output/functions/api/
cp -r api/* .vercel/output/functions/api/

# Create config file
cat > .vercel/output/config.json << EOL
{
  "version": 3,
  "routes": [
    { "src": "/api/(.*)", "dest": "/api" },
    { "handle": "filesystem" },
    { "src": "/(.*)", "dest": "/api" }
  ]
}
EOL

# Create .env file for Vercel if it doesn't exist
if [ ! -f ".vercel/output/functions/api/.env" ]; then
  cat > .vercel/output/functions/api/.env << EOL
GEMINI_API_KEY=your_api_key_here
ENABLE_AI_ANALYSIS=true
FLASK_ENV=production
EOL
fi

echo "Build completed successfully!"
