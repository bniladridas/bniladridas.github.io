# SyntharaAI Architecture Documentation

## Introduction

This documentation provides a comprehensive overview of the SyntharaAI architecture, including the frontend, backend, AI integration, and deployment architecture.

## Table of Contents

1. [Overview](overview.md)
2. [Backend Architecture](backend.md)
3. [Frontend Architecture](frontend.md)
4. [AI Integration](ai-integration.md)
5. [Deployment Architecture](deployment.md)
6. [Architecture Diagrams](diagram.md)

## Quick Start

To run the application locally:

1. Clone the repository
2. Create a `.env` file with your Gemini API key:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Run the application:
   ```
   python chatbot.py
   ```
5. Access the application at http://localhost:8080

## Architecture Diagram

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │
│  Web Browser    │◄────┤  Flask Server   │◄────┤  Gemini API     │
│  (Frontend)     │     │  (Backend)      │     │  (AI Service)   │
│                 │─────►                 │─────►                 │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                              │
                              │
                        ┌─────▼─────┐
                        │           │
                        │ File      │
                        │ Storage   │
                        │           │
                        └───────────┘
```

## Key Technologies

- **Frontend**: HTML, CSS, JavaScript (Vanilla)
- **Backend**: Python, Flask
- **AI**: Google Gemini API
- **Deployment**: Vercel

## Contributing

To contribute to the architecture:

1. Review the existing architecture documentation
2. Propose changes through pull requests
3. Update documentation to reflect architectural changes
4. Ensure backward compatibility or provide migration paths

## License

The SyntharaAI architecture and documentation are licensed under the terms specified in the LICENSE file.
