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

# Create .env file for Vercel using the local .env file if it exists
if [ -f ".env" ]; then
  cp .env .vercel/output/functions/api/.env
  echo "Copied existing .env file to functions/api/"
else
  # Create default .env file if local one doesn't exist
  cat > .vercel/output/functions/api/.env << EOL
GEMINI_API_KEY=REMOVED_API_KEY
ENABLE_AI_ANALYSIS=true
FLASK_ENV=production
EOL
  echo "Created default .env file with provided Gemini API key"
fi

echo "Build completed successfully!"
