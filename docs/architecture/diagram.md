# SyntharaAI Architecture Diagrams

## High-Level Architecture

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

## Backend Components

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

## AI Integration

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │
│  Flask Backend  │◄────┤  Google Genai   │◄────┤  Gemini API     │
│                 │     │  Client Library  │     │  (Google Cloud) │
│                 │─────►                 │─────►                 │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

## Frontend Components

```
┌─────────────────────────────────────┐
│ Chatbot Interface                   │
├─────────────────────────────────────┤
│                                     │
│  ┌───────────────────────────────┐  │
│  │ Message History               │  │
│  │                               │  │
│  │                               │  │
│  │                               │  │
│  │                               │  │
│  └───────────────────────────────┘  │
│                                     │
├─────────────────────────────────────┤
│ ┌─────────────────────┐ ┌─────────┐ │
│ │ Message Input       │ │ Send    │ │
│ └─────────────────────┘ └─────────┘ │
└─────────────────────────────────────┘
```

## File Analysis Flow

```
┌───────────┐     ┌───────────┐     ┌───────────┐     ┌───────────┐
│           │     │           │     │           │     │           │
│  Upload   │────►│  Basic    │────►│  AI       │────►│  Display  │
│  File     │     │  Analysis │     │  Analysis │     │  Results  │
│           │     │           │     │           │     │           │
└───────────┘     └───────────┘     └───────────┘     └───────────┘
                                         │
                                         │
                                    ┌────▼────┐
                                    │         │
                                    │ Fallback│
                                    │         │
                                    └─────────┘
```

## Data Flow

```
┌───────────┐     ┌───────────┐     ┌───────────┐     ┌───────────┐
│           │     │           │     │           │     │           │
│  User     │────►│  Frontend │────►│  Backend  │────►│  AI       │
│  Input    │     │  (JS)     │     │  (Flask)  │     │  (Gemini) │
│           │     │           │     │           │     │           │
└───────────┘     └───────────┘     └───────────┘     └───────────┘
                       ▲                 │                 │
                       │                 │                 │
                       └─────────────────┴─────────────────┘
                                     │
                                     │
                                ┌────▼────┐
                                │         │
                                │ Response│
                                │         │
                                └─────────┘
```

## File Structure

```
bniladridas.github.io/
├── chatbot.py           # Main Flask application
├── api/
│   └── index.py         # Vercel serverless entry point
├── uploads/             # Temporary file storage
├── assets/              # Static assets
│   ├── css/             # CSS styles
│   ├── js/              # JavaScript files
│   └── images/          # Image assets
├── docs/                # Documentation
│   └── architecture/    # Architecture documentation
├── *.html               # HTML pages
├── vercel.json          # Vercel configuration
├── requirements.txt     # Python dependencies
└── .env                 # Environment variables
```
