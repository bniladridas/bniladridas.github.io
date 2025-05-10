# SyntharaAI Documentation

## Overview

SyntharaAI is an advanced AI-powered chatbot and file analysis system designed to provide intelligent responses and detailed file analysis. The system combines natural language processing with specialized file analysis capabilities to deliver insights across various file types and domains, with particular expertise in supply chain management.

## System Architecture

### Frontend
- **Technologies**: HTML5, CSS3, JavaScript (Vanilla)
- **Design Philosophy**: Mobile-first, responsive design with clean typography
- **Key Components**:
  - Interactive chat interface
  - File upload system
  - Analysis display components
  - Responsive layout adapters

### Backend
- **Technologies**: Python, Flask, Google Gemini API
- **Design Philosophy**: Modular, API-first architecture with fallback mechanisms
- **Key Components**:
  - RESTful API endpoints
  - File processing engine
  - AI integration layer
  - Domain-specific knowledge base

### Integration Points
- **AI Services**: Google Gemini API for natural language processing and content analysis
- **File Processing**: Native Python libraries for file parsing and analysis
- **Frontend-Backend Communication**: RESTful API with JSON payloads

## Features

### Chatbot Capabilities
- **Natural Language Understanding**: Comprehension of user queries and context
- **Domain Knowledge**: Specialized knowledge in supply chain management
- **Contextual Responses**: Maintains conversation context for coherent interactions
- **GitHub Integration**: Provides information about the developer's GitHub projects

### File Analysis System

#### Upload Capabilities
- Multiple file upload support
- Progress tracking
- File type validation
- Size limitations and handling

#### Analysis Types
1. **Text Document Analysis**
   - Word and line counting
   - Topic extraction
   - Document type classification
   - Section identification
   - Content summarization

2. **CSV Data Analysis**
   - Row and column counting
   - Data type detection
   - Key column identification
   - Category detection
   - Structure analysis

3. **JSON Data Analysis**
   - Structure detection (object vs array)
   - Schema analysis
   - Property extraction
   - Validation

4. **Code File Analysis**
   - Language detection
   - Complexity scoring
   - Purpose identification
   - Function and class extraction
   - Import/dependency analysis

5. **Image Analysis**
   - Metadata extraction
   - Content prediction (AI-based)
   - Format analysis

#### AI Analysis
- **Capabilities**: Deep content understanding, pattern recognition, contextual analysis
- **Fallback Mechanism**: Graceful degradation to basic analysis when AI is unavailable
- **Accuracy Disclaimer**: Clear communication about AI limitations

## Technical Details

### API Endpoints

#### Chat Endpoint
```
POST /api/chat
```
- **Request Body**: `{"message": "user message here"}`
- **Response**: `{"response": "AI response here"}`

#### File Upload Endpoint
```
POST /api/upload
```
- **Request Body**: FormData with file(s)
- **Response**: JSON with analysis results

### Environment Configuration
- `GEMINI_API_KEY`: Google Gemini API key
- `ENABLE_AI_ANALYSIS`: Toggle for AI-powered analysis (true/false)
- `PORT`: Server port (default: 8080)

### File Analysis Process
1. File upload and temporary storage
2. File type detection and categorization
3. Basic metadata extraction
4. Content-specific analysis based on file type
5. AI analysis (if enabled)
6. Result compilation and return

## Usage Guide

### Starting the Server
```bash
python chatbot.py
```

### Accessing the Interface
- Web Interface: `http://localhost:8080`
- API Endpoint: `http://localhost:8080/api/chat`

### Using the Chatbot
1. Type messages in the input field
2. Press Enter or click Send
3. For file analysis, click the upload button
4. Select files and click Analyze

### File Analysis Tips
- Upload multiple files for batch analysis
- Supported formats: txt, csv, json, js, py, html, css, jpg, png, pdf, etc.
- For best results with code files, ensure complete files rather than fragments
- CSV analysis works best with properly formatted files with headers

## Implementation Details

### AI Integration
The system uses Google's Gemini API for two primary purposes:
1. **Chatbot Responses**: Processing user queries and generating contextual responses
2. **File Analysis**: Analyzing file content for deeper insights

The AI integration includes:
- Prompt engineering for specific analysis types
- Context management for coherent conversations
- Fallback mechanisms for reliability

### File Processing
File processing uses a combination of:
- Native Python libraries for parsing
- Regular expressions for pattern matching
- Heuristic algorithms for structure detection
- AI for content understanding

### Error Handling
The system implements comprehensive error handling:
- Input validation
- File size and type restrictions
- API failure recovery
- Graceful degradation of features

## Extending the System

### Adding New File Types
1. Update the `allowed_file` function in `chatbot.py`
2. Add file type detection in `get_file_category`
3. Implement analysis logic in `analyze_file_content`
4. Update frontend display in HTML files

### Enhancing AI Capabilities
1. Modify AI prompts in `analyze_file_with_ai`
2. Adjust token limits and parameters
3. Update response processing

### Adding New Features
1. Implement backend endpoints in `chatbot.py`
2. Add frontend components in HTML/JS
3. Update documentation and changelog
