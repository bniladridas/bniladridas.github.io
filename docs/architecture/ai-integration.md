# SyntharaAI AI Integration

## Overview

SyntharaAI integrates with Google's Gemini API to provide AI-powered features such as chatbot responses and file analysis. This document describes the architecture and implementation of this integration.

## Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │
│  Flask Backend  │◄────┤  Google Genai   │◄────┤  Gemini API     │
│                 │     │  Client Library  │     │  (Google Cloud) │
│                 │─────►                 │─────►                 │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

## Key Components

### 1. Gemini API Client

The application uses the `google-genai` Python client library to interact with the Gemini API:

```python
from google import genai
from google.genai import types

# Initialize Gemini API client
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
```

### 2. Chat Integration

The chat integration uses the Gemini API to generate responses to user messages:

```python
# Chat endpoint
@app.route('/api/chat', methods=['POST', 'GET'])
def chat():
    # ... (request handling)
    
    # Call Gemini API
    model = "gemini-1.5-flash"
    
    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=combined_prompt)]
        ),
    ]
    
    generate_content_config = types.GenerateContentConfig(
        response_mime_type="text/plain",
        temperature=0.4,
        top_p=0.85,
        top_k=20,
        max_output_tokens=100,
    )
    
    response = client.models.generate_content(
        model=model,
        contents=contents,
        config=generate_content_config,
    )
    
    # ... (response handling)
```

### 3. File Analysis Integration

The file analysis integration uses the Gemini API to analyze file content:

```python
def analyze_file_with_ai(file_path, file_category, filename, file_content=None):
    # ... (prompt preparation)
    
    # Call Gemini API
    model = "gemini-1.5-flash"
    
    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=ai_prompt)]
        ),
    ]
    
    generate_content_config = types.GenerateContentConfig(
        response_mime_type="text/plain",
        temperature=0.2,
        top_p=0.85,
        top_k=20,
        max_output_tokens=150,
    )
    
    response = client.models.generate_content(
        model=model,
        contents=contents,
        config=generate_content_config,
    )
    
    # ... (response handling)
```

## Prompt Engineering

### Chat Prompts

The chat prompts are designed to provide context and instructions to the AI:

```
You are an assistant for SyntharaAI, supporting mental health professionals.
Provide brief, clear answers (2-3 sentences) focused on mental health tech or resources.
Use bullet points for lists and include an emoji where appropriate. 😊

SyntharaAI has a comprehensive supply chain that connects data sources, AI processing, and delivery of insights:
- Data flows from secure collection points through ethical AI processing to actionable insights
- Security includes end-to-end encryption, anonymization, and strict access controls
- The system complies with healthcare regulations including HIPAA and GDPR

... (additional context)

User query: {user_input}
```

### File Analysis Prompts

The file analysis prompts are tailored to the file type and content:

```
Analyze this file based on its metadata and content:
Filename: {filename}
File type: {file_category}
File size: {file_size_kb:.2f} KB
Content preview: {content_snippet}

Your task:
1. Provide a detailed summary of what this file contains based on the content preview
2. Identify the main purpose, topic, or function of this file
3. For code files: identify the programming language, key functions, classes, or algorithms
4. For data files: describe the data structure, key fields, and what the data represents
5. For text documents: summarize the main topics, key points, and document type
6. Identify any domain-specific terminology or concepts (e.g., medical, scientific, business)

Be specific and detailed in your analysis. Focus on the actual content rather than making generic statements.
Highlight any patterns, structures, or important elements in the file.
If the file appears to be part of a larger system or project, explain its likely role.
```

## Model Configuration

The application uses different model configurations for different use cases:

### Chat Configuration

```python
generate_content_config = types.GenerateContentConfig(
    response_mime_type="text/plain",
    temperature=0.4,      # Moderate creativity
    top_p=0.85,           # Diverse but relevant responses
    top_k=20,             # Consider top 20 tokens
    max_output_tokens=100, # Short, concise responses
)
```

### File Analysis Configuration

```python
generate_content_config = types.GenerateContentConfig(
    response_mime_type="text/plain",
    temperature=0.2,      # Low creativity for factual analysis
    top_p=0.85,           # Diverse but relevant analysis
    top_k=20,             # Consider top 20 tokens
    max_output_tokens=150, # Slightly longer for detailed analysis
)
```

## Fallback Mechanisms

The application includes several fallback mechanisms for when the AI is unavailable:

### 1. API Key Validation

```python
# Validate API key
api_key = os.environ.get("GEMINI_API_KEY")
# Check if API key is missing or placeholder
invalid_key = not api_key or api_key == "your_api_key_here"
if invalid_key:
    logger.info("Using fallback mode - no valid GEMINI_API_KEY found")
    logger.info("AI features will use pre-defined responses")
    os.environ["ENABLE_AI_ANALYSIS"] = "false"  # Disable AI analysis if no valid API key
```

### 2. Pre-defined Responses

```python
# Fallback responses for common queries
FALLBACK_RESPONSES = {
    "help": "I can help with information about SyntharaAI, mental health resources, and more. Just ask! 💬",
    "about": "SyntharaAI is a platform focused on creating tools and spaces for clarity and connection in mental health. 🧠",
    # ... (additional responses)
}

# Check for fallback responses
for keyword, response in FALLBACK_RESPONSES.items():
    if keyword in user_input:
        return jsonify({"response": response})
```

### 3. Basic File Analysis

When AI analysis is disabled, the application falls back to basic file analysis:

```python
def analyze_file_content(file_path, file_category, filename):
    # ... (file analysis logic)
    
    # Basic analysis without AI
    basic_analysis = f"This appears to be a {doc_type} with approximately {word_count} words across {line_count} lines."
    if topics:
        basic_analysis += f" Key topics include: {', '.join(topics)}."
    if headings and len(headings) <= 5:
        basic_analysis += f" Document sections: {', '.join(headings[:5])}."
    
    # Get AI analysis if available
    ai_analysis = analyze_file_with_ai(file_path, file_category, filename, content)
    
    # Return results with or without AI analysis
    return {
        # ... (analysis results)
        "analysis": basic_analysis,
        "ai_analysis": ai_analysis  # Will be None if AI is disabled
    }
```

## Error Handling

The application includes comprehensive error handling for AI integration:

```python
try:
    # Call Gemini API
    # ...
except Exception as api_error:
    # Log the error
    error_type = type(api_error).__name__
    error_msg = str(api_error)
    logger.error(f"Gemini API error: {error_type}: {error_msg}")
    
    # Check for specific error types
    if "blocked" in error_msg.lower():
        return jsonify({"response": "I can't respond to that type of request. Let's talk about mental health tech instead. 🙂"}), 400
    elif "stop" in error_msg.lower():
        return jsonify({"response": "I had to stop generating a response. Could you rephrase your question? 🤔"}), 400
    else:
        # Generic error response with fallback
        # ...
```

## Configuration

The AI integration is configured using environment variables:

- `GEMINI_API_KEY`: The API key for the Gemini API
- `ENABLE_AI_ANALYSIS`: Whether to enable AI-powered file analysis

These variables can be set in the `.env` file or in the deployment environment.
