#!/usr/bin/env python3
"""
Simple HTTP server for OTOP Thailand web application
Usage: python server.py [port]
"""

import http.server
import socketserver
import os
import sys

# Default port
PORT = 8000

# Get port from command line argument if provided
if len(sys.argv) > 1:
    try:
        PORT = int(sys.argv[1])
    except ValueError:
        print("Invalid port number. Using default port 8000.")

# Change to the directory containing this script
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Create a custom handler to set proper MIME types
class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Add CORS headers for local development
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()
    
    def guess_type(self, path):
        # Ensure proper MIME types
        result = super().guess_type(path)
        if isinstance(result, tuple):
            mimetype, encoding = result
        else:
            mimetype, encoding = result, None
            
        if path.endswith('.json'):
            return 'application/json', encoding
        return mimetype, encoding

# Start the server
try:
    with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
        print(f"✅ OTOP Thailand server running at http://localhost:{PORT}")
        print(f"📁 Serving files from: {os.getcwd()}")
        print("🌐 Open http://localhost:{} in your browser".format(PORT))
        print("⏹️  Press Ctrl+C to stop the server")
        httpd.serve_forever()
except KeyboardInterrupt:
    print("\n🛑 Server stopped.")
except OSError as e:
    if e.errno == 48:  # Address already in use
        print(f"❌ Port {PORT} is already in use. Try a different port:")
        print(f"   python server.py {PORT + 1}")
    else:
        print(f"❌ Error starting server: {e}")
    sys.exit(1)