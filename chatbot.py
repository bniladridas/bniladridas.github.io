"""
SyntharaAI Chatbot for Mental Health Professionals
- Install dependencies: pip install google-genai flask python-dotenv requests
- Create a .env file with GEMINI_API_KEY=your_key_here
- Run: python app.py
- Access: http://localhost:8080 (website) or http://localhost:8080/api/chat (API)
"""

import os
import requests
import random
import logging
import json
import csv
import re
from flask import Flask, request, jsonify, send_from_directory
from google import genai
from google.genai import types
from dotenv import load_dotenv
from flask_cors import CORS
from html import escape
from werkzeug.utils import secure_filename

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Set default environment variables if not present
if "ENABLE_AI_ANALYSIS" not in os.environ:
    os.environ["ENABLE_AI_ANALYSIS"] = "true"  # Enable AI analysis by default

# Log AI analysis status
logger.info(f"AI file analysis is {'enabled' if os.environ.get('ENABLE_AI_ANALYSIS', 'true').lower() == 'true' else 'disabled'}")

# Validate API key
api_key = os.environ.get("GEMINI_API_KEY")
# Check if API key is missing or placeholder
invalid_key = not api_key or api_key == "your_api_key_here"
if invalid_key:
    logger.info("Using fallback mode - no valid GEMINI_API_KEY found")
    logger.info("AI features will use pre-defined responses")
    os.environ["ENABLE_AI_ANALYSIS"] = "false"  # Disable AI analysis if no valid API key

app = Flask(__name__, static_folder='.')
CORS(app)  # Enable cross-origin requests

# File upload configuration
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
ALLOWED_EXTENSIONS = {
    'image': ['png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp', 'tiff'],
    'document': ['pdf', 'doc', 'docx', 'txt', 'rtf', 'odt'],
    'data': ['csv', 'xls', 'xlsx', 'json', 'xml'],
    'code': ['py', 'js', 'html', 'css', 'java', 'cpp', 'c', 'php', 'rb', 'go', 'ts', 'jsx', 'tsx']
}

# Create upload folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Basic security headers
@app.after_request
def add_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response

# Initialize Gemini API client
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

# Helper functions for file handling
def allowed_file(filename):
    """Check if the file extension is allowed"""
    if '.' not in filename:
        return False
    ext = filename.rsplit('.', 1)[1].lower()
    for category in ALLOWED_EXTENSIONS.values():
        if ext in category:
            return True
    return False

def get_file_category(filename):
    """Determine the category of the file based on its extension"""
    if '.' not in filename:
        return "unknown"
    ext = filename.rsplit('.', 1)[1].lower()
    for category, extensions in ALLOWED_EXTENSIONS.items():
        if ext in extensions:
            return category
    return "unknown"

def get_file_type_description(filename):
    """Get a detailed description of the file type"""
    if '.' not in filename:
        return "Unknown file type"

    ext = filename.rsplit('.', 1)[1].lower()
    category = get_file_category(filename)

    descriptions = {
        'image': {
            'png': 'PNG (Portable Network Graphics) - Lossless compression image format',
            'jpg': 'JPEG (Joint Photographic Experts Group) - Compressed image format',
            'jpeg': 'JPEG (Joint Photographic Experts Group) - Compressed image format',
            'gif': 'GIF (Graphics Interchange Format) - Animated image format',
            'bmp': 'BMP (Bitmap) - Uncompressed raster image format',
            'webp': 'WebP - Modern image format with superior compression',
            'tiff': 'TIFF (Tagged Image File Format) - High-quality image format'
        },
        'document': {
            'pdf': 'PDF (Portable Document Format) - Document format for sharing',
            'doc': 'DOC - Microsoft Word Document (older format)',
            'docx': 'DOCX - Microsoft Word Document (XML-based)',
            'txt': 'TXT - Plain text file',
            'rtf': 'RTF (Rich Text Format) - Formatted text document',
            'odt': 'ODT (OpenDocument Text) - Open-source document format'
        },
        'data': {
            'csv': 'CSV (Comma-Separated Values) - Tabular data format',
            'xls': 'XLS - Microsoft Excel Spreadsheet (older format)',
            'xlsx': 'XLSX - Microsoft Excel Spreadsheet (XML-based)',
            'json': 'JSON (JavaScript Object Notation) - Data interchange format',
            'xml': 'XML (Extensible Markup Language) - Structured data format'
        },
        'code': {
            'py': 'Python source code file',
            'js': 'JavaScript source code file',
            'html': 'HTML (HyperText Markup Language) file',
            'css': 'CSS (Cascading Style Sheets) file',
            'java': 'Java source code file',
            'cpp': 'C++ source code file',
            'c': 'C source code file',
            'php': 'PHP source code file',
            'rb': 'Ruby source code file',
            'go': 'Go source code file',
            'ts': 'TypeScript source code file',
            'jsx': 'JSX (JavaScript XML) file',
            'tsx': 'TSX (TypeScript XML) file'
        }
    }

    if category in descriptions and ext in descriptions[category]:
        return descriptions[category][ext]
    return f"{ext.upper()} file"

def analyze_file_with_ai(file_path, file_category, filename, file_content=None):
    """Use Gemini AI to analyze file content with fallback to basic analysis"""
    # Check if AI is enabled via environment variable (default to enabled)
    ai_enabled = os.environ.get("ENABLE_AI_ANALYSIS", "true").lower() == "true"

    if not ai_enabled:
        logger.info(f"AI analysis disabled by configuration for file: {filename}")
        return None

    try:
        # Prepare a prompt for the AI based on file type and content
        file_size = os.path.getsize(file_path)
        file_size_kb = file_size / 1024

        # If file is too large, don't send content to AI
        if file_size_kb > 100:  # Limit to 100KB
            ai_prompt = f"""Analyze this file based on its metadata:
Filename: {filename}
File type: {file_category}
File size: {file_size_kb:.2f} KB
(Content too large to include)

Your task:
1. Determine the likely purpose and content of this file based on its name and extension
2. Identify any domain-specific information (e.g., medical, scientific, programming, business)
3. Explain what information this file might contain and how it might be used
4. Note any specific formats, standards, or conventions this file likely follows

Be specific and detailed in your analysis. Avoid generic descriptions.
If the filename contains technical terms or abbreviations, explain what they mean.
If you can't determine something with confidence, acknowledge the limitations of analyzing without content.
"""
        else:
            # Include file content in the prompt if available
            content_snippet = ""
            if file_content:
                # Limit content to a reasonable size
                content_snippet = f"\nContent preview:\n{file_content[:1000]}"
                if len(file_content) > 1000:
                    content_snippet += "...(truncated)"

            ai_prompt = f"""Analyze this file based on its metadata and content:
Filename: {filename}
File type: {file_category}
File size: {file_size_kb:.2f} KB{content_snippet}

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
"""

        # Check if API key is available
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            logger.warning("No Gemini API key found, using fallback analysis")
            return None

        # Call Gemini API
        try:
            model = "gemini-1.5-flash"

            contents = [
                types.Content(
                    role="user",
                    parts=[types.Part.from_text(text=ai_prompt)]
                ),
            ]

            generate_content_config = types.GenerateContentConfig(
                response_mime_type="text/plain",
                temperature=0.2,  # Lower temperature for more factual responses
                top_p=0.85,
                top_k=20,
                max_output_tokens=150,  # Keep it concise
            )

            logger.info(f"Calling Gemini API for file analysis: {filename}")

            response = client.models.generate_content(
                model=model,
                contents=contents,
                config=generate_content_config,
            )

            if hasattr(response, 'text') and response.text:
                return response.text.strip()
            else:
                logger.error("Empty response from Gemini API for file analysis")
                return None

        except Exception as api_error:
            logger.error(f"Gemini API error during file analysis: {str(api_error)}")
            return None

    except Exception as e:
        logger.error(f"Error in AI file analysis: {str(e)}")
        return None

def analyze_file_content(file_path, file_category, filename):
    """Analyze the content of a file based on its category"""
    try:

        if file_category == "image":
            # For images, we can only analyze metadata without additional libraries
            file_size = os.path.getsize(file_path)

            # Get AI analysis for the image based on filename and metadata
            ai_analysis = analyze_file_with_ai(file_path, file_category, filename)

            return {
                "type": "image",
                "filename": filename,
                "size": f"{file_size / 1024:.2f} KB",
                "analysis": "This is an image file. With proper image processing libraries, I could analyze the content, detect objects, or extract text.",
                "ai_analysis": ai_analysis
            }

        elif file_category == "document":
            file_size = os.path.getsize(file_path)

            # For text files, we can read and analyze the content
            if filename.endswith('.txt'):
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read(3000)  # Read first 3000 chars for better context
                    word_count = len(content.split())
                    line_count = len(content.splitlines())

                    # Enhanced topic detection based on word frequency
                    words = re.findall(r'\b\w+\b', content.lower())
                    word_freq = {}
                    stop_words = {'the', 'and', 'this', 'that', 'with', 'from', 'have', 'for', 'not', 'are', 'but', 'was', 'were', 'they', 'will', 'what', 'when', 'where', 'how', 'which'}
                    for word in words:
                        if len(word) > 3 and word not in stop_words:  # Skip short words and stop words
                            word_freq[word] = word_freq.get(word, 0) + 1

                    # Get top 8 words for better topic coverage
                    top_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:8]
                    topics = [word for word, _ in top_words]

                    # Extract potential document structure
                    lines = content.splitlines()
                    headings = []
                    for line in lines:
                        # Look for potential headings (all caps, numbered, or ending with colon)
                        if (line.isupper() and len(line) > 3 and len(line) < 50) or \
                           (re.match(r'^\d+\.', line)) or \
                           (line.endswith(':') and len(line) < 50):
                            headings.append(line.strip())

                    # Detect document type based on content patterns
                    doc_type = "general text"
                    if any(word in content.lower() for word in ['dear', 'sincerely', 'regards']):
                        doc_type = "letter or email"
                    elif any(word in content.lower() for word in ['abstract', 'introduction', 'conclusion', 'references']):
                        doc_type = "academic or research document"
                    elif any(word in content.lower() for word in ['chapter', 'scene', 'character']):
                        doc_type = "creative writing or story"
                    elif re.search(r'\d+\.\s+', content):
                        doc_type = "list or instructions"

                    # Get AI analysis with enhanced content
                    ai_analysis = analyze_file_with_ai(file_path, file_category, filename, content)

                    # Create enhanced analysis text
                    basic_analysis = f"This appears to be a {doc_type} with approximately {word_count} words across {line_count} lines."
                    if topics:
                        basic_analysis += f" Key topics include: {', '.join(topics)}."
                    if headings and len(headings) <= 5:
                        basic_analysis += f" Document sections: {', '.join(headings[:5])}."

                    return {
                        "type": "text document",
                        "filename": filename,
                        "size": f"{file_size / 1024:.2f} KB",
                        "word_count": word_count,
                        "line_count": line_count,
                        "document_type": doc_type,
                        "frequent_words": topics,
                        "headings": headings[:5] if headings else [],
                        "sample": content[:250] + "..." if len(content) > 250 else content,
                        "analysis": basic_analysis,
                        "ai_analysis": ai_analysis
                    }

            return {
                "type": "document",
                "filename": filename,
                "size": f"{file_size / 1024:.2f} KB",
                "analysis": "This is a document file. With proper document processing libraries, I could extract and analyze the text content.",
                "ai_analysis": analyze_file_with_ai(file_path, file_category, filename)
            }

        elif file_category == "data":
            file_size = os.path.getsize(file_path)

            # For CSV files, we can read and analyze the structure and content
            if filename.endswith('.csv'):
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read(3000)  # Read first 3000 chars for AI analysis
                    f.seek(0)  # Reset file pointer

                    # Parse CSV data
                    csv_reader = csv.reader(f)
                    headers = next(csv_reader, [])

                    # Read a sample of rows for analysis (up to 20)
                    sample_rows = []
                    for i, row in enumerate(csv_reader):
                        if i < 20:  # Limit to 20 rows for sample
                            sample_rows.append(row)
                        else:
                            break

                    # Count total rows
                    row_count = len(sample_rows) + 1  # +1 for header
                    if len(sample_rows) == 20:
                        # We only read a sample, so estimate total by file size
                        f.seek(0, os.SEEK_END)
                        file_size = f.tell()
                        f.seek(0)
                        header_line = f.readline()
                        avg_row_size = sum(len(','.join(row)) for row in sample_rows) / len(sample_rows) if sample_rows else len(header_line)
                        estimated_rows = int(file_size / avg_row_size) if avg_row_size > 0 else 0
                        row_count = f"~{estimated_rows}" if estimated_rows > 20 else len(sample_rows) + 1

                    # Analyze data types in each column
                    column_types = {}
                    for header in headers:
                        column_types[header] = "unknown"

                    for row in sample_rows:
                        for i, value in enumerate(row):
                            if i < len(headers):
                                header = headers[i]
                                # Skip empty values
                                if not value.strip():
                                    continue

                                # Try to determine data type
                                if column_types[header] == "unknown":
                                    # Check if numeric
                                    if re.match(r'^-?\d+(\.\d+)?$', value):
                                        if '.' in value:
                                            column_types[header] = "decimal"
                                        else:
                                            column_types[header] = "integer"
                                    # Check if date
                                    elif re.match(r'^\d{1,4}[-/]\d{1,2}[-/]\d{1,4}', value) or \
                                         re.match(r'^\d{1,2}[-/]\d{1,2}[-/]\d{2,4}', value):
                                        column_types[header] = "date"
                                    # Check if boolean
                                    elif value.lower() in ('true', 'false', 'yes', 'no', '0', '1'):
                                        column_types[header] = "boolean"
                                    else:
                                        column_types[header] = "text"
                                # If already determined as text, keep it
                                elif column_types[header] != "text":
                                    # If previously thought to be numeric but now contains text
                                    if column_types[header] in ("integer", "decimal") and not re.match(r'^-?\d+(\.\d+)?$', value):
                                        column_types[header] = "text"
                                    # If previously thought to be date but now doesn't match
                                    elif column_types[header] == "date" and not (re.match(r'^\d{1,4}[-/]\d{1,2}[-/]\d{1,4}', value) or \
                                                                               re.match(r'^\d{1,2}[-/]\d{1,2}[-/]\d{2,4}', value)):
                                        column_types[header] = "text"
                                    # If previously thought to be boolean but now contains other values
                                    elif column_types[header] == "boolean" and value.lower() not in ('true', 'false', 'yes', 'no', '0', '1'):
                                        column_types[header] = "text"

                    # Identify potential key columns
                    key_columns = []
                    for i, header in enumerate(headers):
                        # Check if all values in this column are unique
                        if i < len(headers):
                            values = [row[i] for row in sample_rows if i < len(row)]
                            if len(values) == len(set(values)) and len(values) > 0:
                                key_columns.append(header)

                    # Identify potential categories
                    category_columns = []
                    for i, header in enumerate(headers):
                        if i < len(headers) and column_types[header] == "text":
                            values = [row[i] for row in sample_rows if i < len(row)]
                            unique_values = set(values)
                            # If number of unique values is small compared to total, it's likely a category
                            if 1 < len(unique_values) <= 10 and len(values) > 0:
                                category_columns.append(header)

                    # Create enhanced analysis text
                    data_types_summary = []
                    for data_type in set(column_types.values()):
                        count = list(column_types.values()).count(data_type)
                        if count > 0:
                            data_types_summary.append(f"{count} {data_type}")

                    basic_analysis = f"This CSV file contains {row_count} rows and {len(headers)} columns."
                    if data_types_summary:
                        basic_analysis += f" Column types: {', '.join(data_types_summary)}."
                    if key_columns:
                        basic_analysis += f" Potential key columns: {', '.join(key_columns[:3])}."
                    if category_columns:
                        basic_analysis += f" Categorical columns: {', '.join(category_columns[:3])}."

                    # Get AI analysis with enhanced content
                    # Include sample data for better analysis
                    enhanced_content = f"CSV Headers: {', '.join(headers)}\n\n"
                    enhanced_content += "Sample data (first 5 rows):\n"
                    for i, row in enumerate(sample_rows[:5]):
                        enhanced_content += f"Row {i+1}: {', '.join(row)}\n"
                    enhanced_content += f"\nColumn types: {str(column_types)}\n"

                    ai_analysis = analyze_file_with_ai(file_path, file_category, filename, enhanced_content)

                    return {
                        "type": "CSV data",
                        "filename": filename,
                        "size": f"{file_size / 1024:.2f} KB",
                        "columns": len(headers),
                        "rows": row_count,
                        "headers": headers[:10],  # First 10 headers
                        "column_types": column_types,
                        "key_columns": key_columns[:3] if key_columns else [],
                        "category_columns": category_columns[:3] if category_columns else [],
                        "analysis": basic_analysis,
                        "ai_analysis": ai_analysis
                    }

            # For JSON files, we can read and analyze the structure
            elif filename.endswith('.json'):
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read(2000)  # Read first 2000 chars for AI analysis

                    try:
                        data = json.loads(content)
                        if isinstance(data, list):
                            item_count = len(data)
                            sample_keys = list(data[0].keys())[:5] if item_count > 0 and isinstance(data[0], dict) else []

                            # Get AI analysis
                            ai_analysis = analyze_file_with_ai(file_path, file_category, filename, content)

                            return {
                                "type": "JSON data (array)",
                                "filename": filename,
                                "size": f"{file_size / 1024:.2f} KB",
                                "items": item_count,
                                "sample_keys": sample_keys,
                                "analysis": f"This JSON file contains an array with {item_count} items. " +
                                           f"Each item appears to have properties like: {', '.join(sample_keys)}.",
                                "ai_analysis": ai_analysis
                            }
                        elif isinstance(data, dict):
                            top_keys = list(data.keys())[:5]

                            # Get AI analysis
                            ai_analysis = analyze_file_with_ai(file_path, file_category, filename, content)

                            return {
                                "type": "JSON data (object)",
                                "filename": filename,
                                "size": f"{file_size / 1024:.2f} KB",
                                "top_keys": top_keys,
                                "analysis": f"This JSON file contains an object with top-level properties: {', '.join(top_keys)}.",
                                "ai_analysis": ai_analysis
                            }
                    except json.JSONDecodeError:
                        return {
                            "type": "JSON data (invalid)",
                            "filename": filename,
                            "size": f"{file_size / 1024:.2f} KB",
                            "analysis": "This file has a .json extension but does not contain valid JSON data.",
                            "ai_analysis": analyze_file_with_ai(file_path, file_category, filename)
                        }

            return {
                "type": "data file",
                "filename": filename,
                "size": f"{file_size / 1024:.2f} KB",
                "analysis": "This is a data file. With proper data processing libraries, I could analyze the structure and content.",
                "ai_analysis": analyze_file_with_ai(file_path, file_category, filename)
            }

        elif file_category == "code":
            file_size = os.path.getsize(file_path)

            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read(5000)  # Read first 5000 chars
                line_count = len(content.splitlines())

                # Detect language features
                language_features = {}

                # Python features
                if filename.endswith('.py'):
                    language_features["imports"] = re.findall(r'import\s+(\w+)', content)
                    language_features["functions"] = re.findall(r'def\s+(\w+)\s*\(', content)
                    language_features["classes"] = re.findall(r'class\s+(\w+)', content)

                # JavaScript/TypeScript features
                elif filename.endswith(('.js', '.ts', '.jsx', '.tsx')):
                    language_features["imports"] = re.findall(r'import\s+.*?from\s+[\'"](.+?)[\'"]', content)
                    language_features["functions"] = re.findall(r'function\s+(\w+)\s*\(', content)
                    language_features["arrow_functions"] = bool(re.search(r'=>', content))
                    language_features["classes"] = re.findall(r'class\s+(\w+)', content)

                # HTML features
                elif filename.endswith('.html'):
                    language_features["doctype"] = bool(re.search(r'<!DOCTYPE', content, re.IGNORECASE))
                    language_features["tags"] = re.findall(r'<(\w+)[>\s]', content)
                    language_features["scripts"] = re.findall(r'<script.*?>(.*?)</script>', content, re.DOTALL)
                    language_features["styles"] = re.findall(r'<style.*?>(.*?)</style>', content, re.DOTALL)

                # CSS features
                elif filename.endswith('.css'):
                    language_features["selectors"] = re.findall(r'([.#]?\w+)\s*{', content)
                    language_features["properties"] = re.findall(r'(\w+-?\w+)\s*:', content)

                # Java/C++/C features
                elif filename.endswith(('.java', '.cpp', '.c')):
                    language_features["includes"] = re.findall(r'#include\s+[<"](.+?)[>"]', content)
                    language_features["imports"] = re.findall(r'import\s+(.+?);', content)
                    language_features["functions"] = re.findall(r'(\w+)\s+(\w+)\s*\([^)]*\)\s*{', content)
                    language_features["classes"] = re.findall(r'class\s+(\w+)', content)

                # PHP features
                elif filename.endswith('.php'):
                    language_features["php_tags"] = bool(re.search(r'<\?php', content))
                    language_features["functions"] = re.findall(r'function\s+(\w+)\s*\(', content)
                    language_features["classes"] = re.findall(r'class\s+(\w+)', content)

                # Detect code complexity
                complexity_score = 0

                # Count nested blocks/indentation
                max_indent = 0
                current_indent = 0
                for line in content.splitlines():
                    stripped = line.strip()
                    if not stripped or stripped.startswith(('#', '//', '/*', '*')):  # Skip comments and empty lines
                        continue

                    # Count leading spaces
                    indent = len(line) - len(line.lstrip())
                    current_indent = indent // 4  # Assuming 4 spaces per indent level
                    max_indent = max(max_indent, current_indent)

                # Complexity based on nesting
                if max_indent > 5:
                    complexity_score += 3  # High nesting
                elif max_indent > 3:
                    complexity_score += 2  # Medium nesting
                else:
                    complexity_score += 1  # Low nesting

                # Complexity based on function/class count
                function_count = len(language_features.get("functions", []))
                class_count = len(language_features.get("classes", []))

                if function_count > 10 or class_count > 5:
                    complexity_score += 3  # High complexity
                elif function_count > 5 or class_count > 2:
                    complexity_score += 2  # Medium complexity
                else:
                    complexity_score += 1  # Low complexity

                # Determine complexity level
                complexity_level = "Low"
                if complexity_score >= 5:
                    complexity_level = "High"
                elif complexity_score >= 3:
                    complexity_level = "Medium"

                # Detect code purpose
                code_purpose = "Unknown"

                # Python purpose detection
                if filename.endswith('.py'):
                    if any(imp in str(language_features.get("imports", [])) for imp in ['flask', 'django', 'fastapi']):
                        code_purpose = "Web Backend/API"
                    elif any(imp in str(language_features.get("imports", [])) for imp in ['pandas', 'numpy', 'matplotlib', 'sklearn', 'tensorflow', 'torch']):
                        code_purpose = "Data Science/ML"
                    elif any(imp in str(language_features.get("imports", [])) for imp in ['unittest', 'pytest']):
                        code_purpose = "Testing"
                    elif any(imp in str(language_features.get("imports", [])) for imp in ['tkinter', 'PyQt', 'wx']):
                        code_purpose = "GUI Application"

                # JavaScript purpose detection
                elif filename.endswith(('.js', '.jsx', '.ts', '.tsx')):
                    if any(word in content.lower() for word in ['react', 'component', 'render', 'usestate', 'useeffect']):
                        code_purpose = "React Frontend"
                    elif any(word in content.lower() for word in ['vue', 'component', 'template', 'methods']):
                        code_purpose = "Vue.js Frontend"
                    elif any(word in content.lower() for word in ['angular', 'component', 'ngmodule']):
                        code_purpose = "Angular Frontend"
                    elif any(word in content.lower() for word in ['express', 'app.get', 'app.post', 'router']):
                        code_purpose = "Node.js Backend"
                    elif any(word in content.lower() for word in ['test', 'describe', 'it(', 'expect']):
                        code_purpose = "Testing"

                # HTML purpose detection
                elif filename.endswith('.html'):
                    if '<body' in content and '<head' in content:
                        if any(tag in str(language_features.get("tags", [])) for tag in ['form', 'input', 'button']):
                            code_purpose = "Web Form/Interactive Page"
                        elif any(tag in str(language_features.get("tags", [])) for tag in ['article', 'section', 'header', 'footer']):
                            code_purpose = "Content/Article Page"
                        else:
                            code_purpose = "Web Page"

                # Generate enhanced analysis
                analysis = f"This {get_file_type_description(filename)} contains approximately {line_count} lines of code with {complexity_level.lower()} complexity. "

                if code_purpose != "Unknown":
                    analysis += f"Purpose: {code_purpose}. "

                if "imports" in language_features and language_features["imports"]:
                    analysis += f"It imports/includes: {', '.join(language_features['imports'][:5])}. "

                if "functions" in language_features and language_features["functions"]:
                    analysis += f"It defines {len(language_features['functions'])} functions"
                    if len(language_features['functions']) <= 5:
                        analysis += f": {', '.join(language_features['functions'])}. "
                    else:
                        analysis += f", including: {', '.join(language_features['functions'][:5])}... "

                if "classes" in language_features and language_features["classes"]:
                    analysis += f"It defines {len(language_features['classes'])} classes"
                    if len(language_features['classes']) <= 3:
                        analysis += f": {', '.join(language_features['classes'])}. "
                    else:
                        analysis += f", including: {', '.join(language_features['classes'][:3])}... "

                if "tags" in language_features and language_features["tags"]:
                    unique_tags = list(set(language_features["tags"]))
                    analysis += f"It uses {len(unique_tags)} HTML tags"
                    if len(unique_tags) <= 5:
                        analysis += f": {', '.join(unique_tags)}. "
                    else:
                        analysis += f", including: {', '.join(unique_tags[:5])}... "

                if "selectors" in language_features and language_features["selectors"]:
                    unique_selectors = list(set(language_features["selectors"]))
                    analysis += f"It defines {len(unique_selectors)} CSS selectors"
                    if len(unique_selectors) <= 5:
                        analysis += f": {', '.join(unique_selectors)}. "
                    else:
                        analysis += f", including: {', '.join(unique_selectors[:5])}... "

                # Get AI analysis with enhanced context
                enhanced_content = f"Code type: {get_file_type_description(filename)}\n"
                enhanced_content += f"Code purpose: {code_purpose}\n"
                enhanced_content += f"Complexity: {complexity_level}\n"
                enhanced_content += f"Lines of code: {line_count}\n\n"

                if "imports" in language_features and language_features["imports"]:
                    enhanced_content += f"Imports/Includes: {', '.join(language_features['imports'])}\n"

                if "functions" in language_features and language_features["functions"]:
                    enhanced_content += f"Functions: {', '.join(language_features['functions'])}\n"

                if "classes" in language_features and language_features["classes"]:
                    enhanced_content += f"Classes: {', '.join(language_features['classes'])}\n"

                enhanced_content += f"\nCode preview:\n{content[:2500]}"

                ai_analysis = analyze_file_with_ai(file_path, file_category, filename, enhanced_content)

                return {
                    "type": "code file",
                    "filename": filename,
                    "size": f"{file_size / 1024:.2f} KB",
                    "lines": line_count,
                    "complexity": complexity_level,
                    "purpose": code_purpose,
                    "features": language_features,
                    "analysis": analysis,
                    "ai_analysis": ai_analysis
                }

        # Default analysis for unknown file types
        return {
            "type": "unknown",
            "filename": filename,
            "size": f"{os.path.getsize(file_path) / 1024:.2f} KB",
            "analysis": "This file type is not supported for detailed analysis.",
            "ai_analysis": analyze_file_with_ai(file_path, file_category, filename)
        }

    except Exception as e:
        logger.error(f"Error analyzing file {filename}: {str(e)}")
        return {
            "type": "error",
            "filename": filename,
            "error": str(e),
            "analysis": "An error occurred while analyzing this file."
        }

# GitHub username
GITHUB_USERNAME = "bniladridas"

# Cache for GitHub data
github_user_cache = None
github_repos_cache = None

# Fetch GitHub user data
def fetch_github_user():
    global github_user_cache
    if github_user_cache:
        return github_user_cache
    try:
        response = requests.get(
            f"https://api.github.com/users/{GITHUB_USERNAME}",
            timeout=5  # 5 second timeout
        )
        if response.status_code == 200:
            github_user_cache = response.json()
            return github_user_cache
        elif response.status_code == 403:
            print("GitHub API rate limit exceeded")
            return None
        else:
            print(f"GitHub API error: {response.status_code}")
            return None
    except requests.exceptions.Timeout:
        print("GitHub API request timed out")
        return None
    except Exception as e:
        print(f"Error fetching GitHub user: {e}")
        return None

# Fetch GitHub repositories
def fetch_github_repos():
    global github_repos_cache
    if github_repos_cache:
        return github_repos_cache
    try:
        response = requests.get(
            f"https://api.github.com/users/{GITHUB_USERNAME}/repos",
            timeout=5  # 5 second timeout
        )
        if response.status_code == 200:
            github_repos_cache = response.json()
            return github_repos_cache
        elif response.status_code == 403:
            print("GitHub API rate limit exceeded")
            return None
        else:
            print(f"GitHub API error: {response.status_code}")
            return None
    except requests.exceptions.Timeout:
        print("GitHub API request timed out")
        return None
    except Exception as e:
        print(f"Error fetching GitHub repos: {e}")
        return None

# Provide info about Niladri Das
def get_niladri_info():
    user_data = fetch_github_user()
    repos_data = fetch_github_repos()
    if not user_data:
        return "Unable to retrieve Niladri Das's info."

    bio = user_data.get('bio', 'No bio available')
    name = user_data.get('name', 'Niladri Das')
    followers = user_data.get('followers', 0)
    public_repos = user_data.get('public_repos', 0)

    repos_info = ""
    if repos_data:
        sorted_repos = sorted(repos_data, key=lambda x: x.get('stargazers_count', 0), reverse=True)
        top_repos = sorted_repos[:3]
        repos_info = "\n\nKey Projects:\n"
        for repo in top_repos:
            repo_name = repo.get('name', 'Unknown')
            repo_stars = repo.get('stargazers_count', 0)
            repo_url = repo.get('html_url', '')
            repos_info += f"- {repo_name} ({repo_stars} stars): {repo_url}\n"

    return f"{name}: Developer of mental health tech solutions.\nBio: {bio}\nFollowers: {followers} | Repos: {public_repos}{repos_info}"

# Greetings for users
GREETINGS = [
    "Hello! 👋 How can I assist with mental health tech?",
    "Hi! 🌟 Ready to explore SyntharaAI?",
    "Welcome! 🤝 How can I support you today?",
    "Hey! 🚀 SyntharaAI assistant here!",
    "Greetings! ✨ What's on your mind?"
]

# Fallback responses for common queries
FALLBACK_RESPONSES = {
    "help": "I can help with information about SyntharaAI, mental health resources, and more. Just ask! 💬",
    "about": "SyntharaAI is a platform focused on creating tools and spaces for clarity and connection in mental health. 🧠",
    "mental health": "Mental health is essential for overall wellbeing. SyntharaAI provides tools to support mental health professionals. 💙",
    "resources": "Some helpful mental health resources include the NIMH, Psychology Today, and Mental Health America. 📚",
    "tools": "SyntharaAI offers various tools for mental health professionals, including assessment tools and therapy resources. 🛠️",
    "therapy": "Therapy is a collaborative process between a person and a mental health professional. SyntharaAI supports therapists with digital tools. 🤝",
    "meditation": "Meditation is a practice that can help reduce stress and improve mental clarity. Try apps like Headspace or Calm. 🧘",
    "anxiety": "Anxiety is a common feeling of worry or fear. SyntharaAI provides resources for anxiety management. 😰",
    "depression": "Depression is a common but serious mood disorder. SyntharaAI offers tools to help professionals support those with depression. 💙",
    "stress": "Stress management techniques include deep breathing, meditation, and physical activity. 🌬️",
    "sleep": "Good sleep is essential for mental health. Establish a regular sleep schedule and create a restful environment. 😴",
    "exercise": "Regular physical activity can help reduce anxiety and depression while improving mood and sleep. 🏃‍♀️",
    "nutrition": "A balanced diet can support brain health and affect mood. Consider foods rich in omega-3s and antioxidants. 🥗",
    "community": "SyntharaAI's Community Infrastructure provides guidelines for respectful and supportive interactions. 👥",
    "contact": "You can reach out to SyntharaAI through the GitHub profile: https://github.com/bniladridas 📧",
    "github": "Check out Niladri's GitHub profile at https://github.com/bniladridas for more projects. 💻",

    # Supply Chain related responses
    "supply chain": "SyntharaAI's supply chain connects data sources, AI processing, and delivery of mental health insights to professionals and users. 🔄",
    "data flow": "In SyntharaAI, data flows from secure collection points through ethical AI processing to actionable insights for mental health professionals. 📊",
    "data sources": "SyntharaAI ethically sources data from consenting users, anonymized health records, and published research to train its models. 📑",
    "processing": "SyntharaAI processes mental health data using secure, privacy-preserving AI models that prioritize user confidentiality. 🔒",
    "delivery": "SyntharaAI delivers insights through secure APIs, dashboards, and integration with existing mental health platforms. 📲",
    "security": "Data security in SyntharaAI includes end-to-end encryption, anonymization, and strict access controls throughout the supply chain. 🛡️",
    "ethics": "Ethical considerations are built into every stage of SyntharaAI's supply chain, from data collection to insight delivery. ⚖️",
    "compliance": "SyntharaAI's supply chain complies with healthcare regulations including HIPAA, GDPR, and other relevant data protection laws. 📜",

    # Fair Policy related responses
    "fair policy": "SyntharaAI's Fair Policy ensures equitable access to mental health resources, transparent pricing, and unbiased AI systems for all users. ⚖️",
    "fairness": "Fairness at SyntharaAI means equal treatment regardless of background, balanced AI training data, and accessible mental health tools for diverse populations. 🌈",
    "equity": "SyntharaAI promotes equity by designing tools that work for people of all backgrounds, abilities, and socioeconomic statuses. 🤝",
    "accessibility": "Our accessibility commitment ensures mental health tools are available to users with different abilities, languages, and technical resources. ♿",
    "pricing": "SyntharaAI implements transparent, fair pricing with sliding scale options to ensure mental health resources are accessible to all income levels. 💰",
    "bias": "We actively work to identify and eliminate bias in our AI systems through diverse training data and regular fairness audits. 🔍",
    "discrimination": "SyntharaAI has zero tolerance for discrimination and employs rigorous testing to ensure our tools serve all users equally. 🚫",

    # Honesty related responses
    "honesty": "SyntharaAI commits to complete transparency about our capabilities, limitations, data usage, and business practices. 📝",
    "transparency": "We practice radical transparency by clearly communicating how our AI works, what data we collect, and how we use it. 🔎",
    "limitations": "SyntharaAI openly acknowledges the limitations of our technology and provides clear guidance on when professional human support is needed. ⚠️",
    "accuracy": "We're committed to accuracy in all communications and regularly verify the performance of our AI systems against real-world outcomes. ✓",
    "claims": "SyntharaAI makes only evidence-based claims about our technology's capabilities and effectiveness in supporting mental health. 📊",
    "marketing": "Our marketing materials accurately represent our services without exaggeration or misleading promises about mental health outcomes. 📢",
    "data transparency": "We provide clear, accessible information about what user data we collect, how we use it, and who has access to it. 📋",

    # Copyright and Legal responses
    "copyright": "SyntharaAI's content is protected under copyright law. We respect intellectual property rights and expect the same from our users. ©️",
    "legal": "SyntharaAI operates in compliance with all applicable laws and regulations governing mental health technology, data privacy, and AI systems. ⚖️",
    "terms of service": "Our Terms of Service outline user rights and responsibilities, including acceptable use policies and limitations of liability. 📜",
    "privacy policy": "SyntharaAI's Privacy Policy details how we collect, use, store, and protect user data in compliance with global privacy regulations. 🔒",
    "licensing": "Our technology is available under specific licensing terms that protect both our intellectual property and user rights to access mental health tools. 🔑",
    "disclaimer": "SyntharaAI provides tools to support mental health but is not a substitute for professional medical advice, diagnosis, or treatment. 🏥",
    "liability": "While we strive for accuracy and reliability, SyntharaAI has limited liability as detailed in our Terms of Service and user agreements. ⚠️",
    "intellectual property": "SyntharaAI respects intellectual property rights and has policies to address any potential infringement concerns. 📋",
    "compliance": "We maintain compliance with healthcare regulations, data protection laws, and industry standards for mental health technology. ✅",
    "data rights": "Users maintain specific rights regarding their data, including access, correction, deletion, and portability as outlined in our policies. 🛡️",

    # Terms and definitions
    "terms": "SyntharaAI's key terms include Clarity Metrics, Connection Pathways, Insight Nodes, and Ethical AI Frameworks. Ask about any specific term! 📘",
    "clarity metrics": "Clarity Metrics: Quantifiable measures of how well mental health information is understood by users and professionals. 📏",
    "connection pathways": "Connection Pathways: Secure channels through which mental health professionals and clients communicate and share information. 🔗",
    "insight nodes": "Insight Nodes: Key points in the data processing pipeline where meaningful patterns are identified and translated into actionable information. 💡",
    "ethical ai": "Ethical AI Framework: SyntharaAI's system for ensuring AI models operate fairly, transparently, and with respect for user privacy and autonomy. 🤖",
    "mental health data": "Mental Health Data: Information related to psychological wellbeing, collected with explicit consent and handled with strict privacy controls. 📊",
    "user consent": "User Consent Framework: SyntharaAI's comprehensive system for obtaining, tracking, and honoring user permissions for data usage. ✅",
    "anonymization": "Data Anonymization: The process of removing personally identifiable information from mental health data before analysis. 🔍",
    "integration": "System Integration: How SyntharaAI connects with existing mental health platforms and electronic health records. 🔄",
    "api": "SyntharaAI API: The interface that allows secure, controlled access to SyntharaAI's capabilities for authorized applications. 🔌",
    "dashboard": "Professional Dashboard: The interface mental health professionals use to access insights and tools from SyntharaAI. 📊",
    "feedback loop": "Feedback Loop: The system by which user and professional input improves SyntharaAI's models and recommendations over time. 🔁",
    "fairness metrics": "Fairness Metrics: Quantitative measures used to evaluate whether AI systems provide consistent and unbiased results across different demographic groups. 📊",
    "transparency report": "Transparency Report: Regular documentation that discloses SyntharaAI's data practices, algorithmic decision-making processes, and business operations. 📑",
    "equity framework": "Equity Framework: Structured approach to ensuring SyntharaAI's tools and resources are accessible and beneficial to all users regardless of background or ability. 🌈",
    "intellectual property rights": "Intellectual Property Rights: Legal rights that protect creations of the mind, including SyntharaAI's software, algorithms, content, and methodologies. ©️",
    "data processing agreement": "Data Processing Agreement: Legal contract that defines the rights and obligations regarding the processing of personal data, particularly in healthcare contexts. 📝",
    "compliance framework": "Compliance Framework: Structured system of policies, procedures, and controls that ensures SyntharaAI's operations adhere to all applicable laws and regulations. ✅"
}

# File upload endpoint
@app.route('/api/upload', methods=['POST'])
def upload_file():
    # Check if the post request has the file part
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']

    # If user does not select file, browser also submits an empty part without filename
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Get file category
        file_category = get_file_category(filename)

        # Analyze file content
        # Note: analyze_file_content provides basic analysis
        # If AI analysis is enabled, it will also include AI-powered analysis
        # If AI analysis fails or is disabled, only basic analysis will be provided
        analysis_result = analyze_file_content(file_path, file_category, filename)

        # Add file type description
        analysis_result["file_type_description"] = get_file_type_description(filename)

        # Add disclaimer
        analysis_result["disclaimer"] = "This analysis is based on file structure and metadata. For a more comprehensive analysis, specialized tools would be required."

        # Log whether AI was used
        if "ai_analysis" in analysis_result and analysis_result["ai_analysis"]:
            logger.info(f"File analysis for {filename} used AI capabilities")
        else:
            logger.info(f"File analysis for {filename} used basic analysis only")

        return jsonify(analysis_result)

    return jsonify({"error": "File type not allowed"}), 400

# Chat endpoint
@app.route('/api/chat', methods=['POST', 'GET'])
def chat():
    # Handle GET requests
    if request.method == 'GET':
        return jsonify({
            "status": "online",
            "message": "SyntharaAI chat API is running. Send a POST request with a 'message' field to interact with the chatbot.",
            "example": {
                "message": "Tell me about SyntharaAI"
            }
        })

    # Handle POST requests
    data = request.json
    user_input = escape(data.get('message', '').lower()) if data else ''  # Sanitize input

    if not user_input:
        return jsonify({"response": "Please enter a message to continue. 😊"}), 400

    # Handle queries about Niladri or GitHub
    if any(keyword in user_input for keyword in ['who is niladri', 'about niladri', 'niladri das', 'creator', 'developer', 'github profile']):
        response_text = get_niladri_info()
        return jsonify({"response": response_text})

    # Handle greetings
    if any(greeting in user_input for greeting in ['hello', 'hi', 'hey', 'greetings']):
        return jsonify({"response": random.choice(GREETINGS)})

    # Check for fallback responses
    for keyword, response in FALLBACK_RESPONSES.items():
        if keyword in user_input:
            return jsonify({"response": response})

    # Use a simple fallback if API key is missing or invalid
    api_key = os.environ.get("GEMINI_API_KEY")
    # Check if API key is missing or placeholder
    invalid_key = not api_key or api_key == "your_api_key_here"
    if invalid_key:
        logger.warning("No valid API key found, using fallback response")
        return jsonify({
            "response": "I'm currently operating in fallback mode without AI capabilities. I can answer basic questions about mental health and SyntharaAI. Try asking about resources, tools, or therapy. 🤖"
        })

    try:
        # For debugging - return a simple response without calling Gemini API
        # Uncomment this to test if the API is the issue
        # return jsonify({"response": "This is a test response without using the Gemini API. 🧪"})

        # Check if API key is available
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            logger.error("GEMINI_API_KEY not found in environment variables")
            return jsonify({"response": "API key not configured. Please check server configuration. ⚠️"}), 500

        # Log API key length (not the actual key) for debugging
        logger.info(f"API key length: {len(api_key)}")

        # Instead of using system role, include instructions in the user prompt
        # This is compatible with all versions of the Gemini API
        model = "gemini-1.5-flash"

        # Combine system instructions with user input
        combined_prompt = """You are an assistant for SyntharaAI, supporting mental health professionals.
Provide brief, clear answers (2-3 sentences) focused on mental health tech or resources.
Use bullet points for lists and include an emoji where appropriate. 😊

SyntharaAI has a comprehensive supply chain that connects data sources, AI processing, and delivery of insights:
- Data flows from secure collection points through ethical AI processing to actionable insights
- Security includes end-to-end encryption, anonymization, and strict access controls
- The system complies with healthcare regulations including HIPAA and GDPR

SyntharaAI's Fair Policy ensures equitable access to mental health resources:
- Equal treatment regardless of background, with tools designed for diverse populations
- Transparent pricing with sliding scale options for all income levels
- Regular audits to identify and eliminate bias in AI systems

SyntharaAI is committed to honesty and transparency:
- Clear communication about capabilities and limitations of our technology
- Evidence-based claims about effectiveness in supporting mental health
- Complete transparency about data usage and business practices

SyntharaAI's copyright and legal framework protects both the company and users:
- All content is protected under copyright law with specific licensing terms
- Terms of Service outline user rights, responsibilities, and liability limitations
- Privacy Policy details data collection, usage, storage, and protection practices
- Disclaimer clarifies that our tools support but don't replace professional medical advice

SyntharaAI uses specific terminology including:
- Clarity Metrics: Measures of how well mental health information is understood
- Connection Pathways: Secure communication channels between professionals and clients
- Insight Nodes: Points where patterns are identified and translated into actionable information
- Ethical AI Framework: System ensuring fair, transparent AI with respect for privacy

User query: """ + user_input

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

        try:
            # Log that we're about to call the API
            logger.info(f"Calling Gemini API with model: {model}")

            response = client.models.generate_content(
                model=model,
                contents=contents,
                config=generate_content_config,
            )

            # Log successful response
            logger.info("Received successful response from Gemini API")

            # Check if response has text
            if hasattr(response, 'text') and response.text:
                return jsonify({"response": response.text})
            else:
                logger.error("Empty response from Gemini API")
                return jsonify({"response": "I received an empty response. Please try again. 🤔"}), 500

        except Exception as api_error:
            # Log the error
            error_type = type(api_error).__name__
            error_msg = str(api_error)
            logger.error(f"Gemini API error: {error_type}: {error_msg}")

            # Check for specific error types in the error message
            if "blocked" in error_msg.lower():
                return jsonify({"response": "I can't respond to that type of request. Let's talk about mental health tech instead. 🙂"}), 400
            elif "stop" in error_msg.lower():
                return jsonify({"response": "I had to stop generating a response. Could you rephrase your question? 🤔"}), 400
            else:
                # Generic error response with fallback
                # Try to find a relevant fallback response
                for keyword in user_input.split():
                    if keyword in FALLBACK_RESPONSES:
                        return jsonify({"response": f"I encountered an issue with the AI service, but I can tell you that {FALLBACK_RESPONSES[keyword]} 🔄"})

                # If no relevant fallback found, use generic response
                return jsonify({"response": "I encountered an issue with the AI service. I can answer questions about mental health, resources, or SyntharaAI. 🔄"})

    except requests.exceptions.Timeout:
        logger.error("Gemini API request timed out")
        return jsonify({"response": "The request timed out. Please try again later. ⏱️"}), 503
    except Exception as e:
        logger.error(f"Error in chat endpoint: {type(e).__name__}: {str(e)}")
        return jsonify({"response": "Sorry, something went wrong. Please try again! 😔"}), 500

# Serve static files
@app.route('/', defaults={'path': 'index.html'})
@app.route('/<path:path>')
def serve_static(path):
    try:
        return send_from_directory('.', path)
    except Exception as e:
        logger.error(f"Error serving static file {path}: {str(e)}")
        return "File not found", 404

# Error handlers
@app.errorhandler(404)
def page_not_found(_):
    logger.warning(f"404 error: {request.path}")
    return jsonify({"error": "Resource not found"}), 404

@app.errorhandler(500)
def internal_server_error(_):
    logger.error(f"500 error occurred")
    return jsonify({"error": "Internal server error"}), 500

# For local development
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    logger.info(f"Server running at http://localhost:{port}")
    logger.info(f"- Website: http://localhost:{port}")
    logger.info(f"- Chatbot API: http://localhost:{port}/api/chat")

    # Production settings
    if os.environ.get("FLASK_ENV") == "production":
        # In production, disable debug mode
        app.run(debug=False, port=port, host='0.0.0.0', threaded=True)
    else:
        # In development, enable debug mode
        app.run(debug=True, port=port, host='0.0.0.0')

# For Vercel serverless deployment
# This is the entry point that Vercel looks for
app.logger = logger