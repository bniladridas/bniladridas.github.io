import sys
import os
from http.server import BaseHTTPRequestHandler
from flask import Flask

# Add the parent directory to the path so we can import the chatbot module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the Flask app from chatbot.py - this is used by Vercel
try:
    from chatbot import app
except ImportError:
    # Fallback for local testing
    app = Flask(__name__)

    @app.route('/')
    def home():
        return "SyntharaAI API is running"

# This is the handler that Vercel will call
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write('SyntharaAI API is running'.encode())
        return

# For local testing
if __name__ == '__main__':
    from http.server import HTTPServer
    server = HTTPServer(('localhost', 8000), Handler)
    print('Starting server at http://localhost:8000')
    server.serve_forever()
